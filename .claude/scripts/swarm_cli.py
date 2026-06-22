#!/usr/bin/env python3
"""
Swarm CLI - Parallel Agent Orchestration

Core infrastructure for spawning and managing parallel claude processes.
This is the "Swarm Generator Pattern" from MACS architecture.

Key Capabilities:
1. PID tracking for all spawned claude processes
2. p-limit style concurrency control (batch size)
3. STDOUT stream aggregation
4. Emergency kill switch (--nuke)
5. Rate limit backoff

Usage:
    # Spawn 10 agents with concurrency of 3
    python scripts/swarm_cli.py spawn --agent scout --count 10 --concurrency 3 --prompt "Analyze {url}"
    
    # List running processes
    python scripts/swarm_cli.py ps
    
    # Kill all swarm processes
    python scripts/swarm_cli.py nuke
    
    # Run a batch from a task file
    python scripts/swarm_cli.py batch --file tasks.json --concurrency 5
"""

import argparse
import asyncio
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class SwarmProcess:
    """A single swarm worker process."""
    pid: int
    task_id: str
    agent: str
    prompt: str
    status: str = "running"  # running, completed, failed, killed
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    ended_at: Optional[str] = None
    exit_code: Optional[int] = None
    output_file: Optional[str] = None


@dataclass
class SwarmBatch:
    """A batch of swarm tasks."""
    batch_id: str
    tasks: List[Dict[str, Any]]
    concurrency: int
    status: str = "pending"  # pending, running, completed, failed
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    total: int = 0
    completed: int = 0
    failed: int = 0


class SwarmCLI:
    """
    Swarm orchestrator with p-limit style concurrency control.
    
    Key design principles from MACS:
    - The Orchestrator doesn't *do* the work - it *spawns processes* that do
    - Layer 3 workers are stateless and lobotomized
    - Process Groups (setsid) for clean termination
    """
    
    STATE_DIR = Path(".super_agent_monitor/swarm")
    PID_FILE = STATE_DIR / "active_pids.json"
    BATCH_DIR = STATE_DIR / "batches"
    OUTPUT_DIR = STATE_DIR / "outputs"
    
    # Rate limiting
    MIN_SPAWN_INTERVAL = 0.5  # seconds between spawns
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 2
    
    def __init__(self):
        self.STATE_DIR.mkdir(parents=True, exist_ok=True)
        self.BATCH_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self._active_processes: Dict[int, SwarmProcess] = {}
        self._load_state()
        self._semaphore = None  # Set by spawn commands
    
    def _load_state(self):
        """Load active PIDs from disk."""
        if self.PID_FILE.exists():
            try:
                with open(self.PID_FILE) as f:
                    data = json.load(f)
                    for pid_str, proc_data in data.items():
                        pid = int(pid_str)
                        self._active_processes[pid] = SwarmProcess(**proc_data)
            except Exception:
                self._active_processes = {}
    
    def _save_state(self):
        """Save active PIDs to disk."""
        data = {str(pid): asdict(proc) for pid, proc in self._active_processes.items()}
        with open(self.PID_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _check_process_alive(self, pid: int) -> bool:
        """Check if a process is still running."""
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    
    def _cleanup_dead_processes(self):
        """Remove dead processes from tracking."""
        dead_pids = []
        for pid, proc in self._active_processes.items():
            if proc.status == "running" and not self._check_process_alive(pid):
                proc.status = "completed"
                proc.ended_at = datetime.utcnow().isoformat()
                dead_pids.append(pid)
        
        # Don't remove, just update status
        self._save_state()
        return len(dead_pids)
    
    async def _spawn_single(
        self,
        task_id: str,
        agent: str,
        prompt: str,
        model_tier: str = "SMALL",
        timeout: int = 600
    ) -> SwarmProcess:
        """
        Spawn a single claude process with rate limiting.
        
        Uses setsid for process group management (clean kill).
        """
        output_file = self.OUTPUT_DIR / f"{task_id}.json"
        
        # Build command
        cmd = [
            "claude",
            "-p", prompt,
            "--output-format", "stream-json",
            "--dangerously-skip-permissions"
        ]
        
        # Add agent if available
        agent_file = Path(f".claude/agents/{agent}.md")
        if agent_file.exists():
            cmd.extend(["--agent", agent])
        
        try:
            # Spawn with new process group (setsid equivalent)
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=True  # Creates new process group
            )
            
            swarm_proc = SwarmProcess(
                pid=process.pid,
                task_id=task_id,
                agent=agent,
                prompt=prompt[:200] + "..." if len(prompt) > 200 else prompt,
                status="running",
                output_file=str(output_file)
            )
            
            self._active_processes[process.pid] = swarm_proc
            self._save_state()
            
            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                # Save output
                with open(output_file, 'w') as f:
                    json.dump({
                        "task_id": task_id,
                        "stdout": stdout.decode() if stdout else "",
                        "stderr": stderr.decode() if stderr else "",
                        "exit_code": process.returncode
                    }, f, indent=2)
                
                swarm_proc.status = "completed" if process.returncode == 0 else "failed"
                swarm_proc.exit_code = process.returncode
                swarm_proc.ended_at = datetime.utcnow().isoformat()
                
            except asyncio.TimeoutError:
                # Kill the process group
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                swarm_proc.status = "failed"
                swarm_proc.exit_code = -1
                swarm_proc.ended_at = datetime.utcnow().isoformat()
            
            self._save_state()
            return swarm_proc
            
        except FileNotFoundError:
            # Claude CLI not installed
            return SwarmProcess(
                pid=0,
                task_id=task_id,
                agent=agent,
                prompt=prompt[:200],
                status="failed",
                exit_code=-2,
                ended_at=datetime.utcnow().isoformat()
            )
    
    async def spawn_batch(
        self,
        agent: str,
        prompts: List[str],
        concurrency: int = 5,
        model_tier: str = "SMALL",
        timeout: int = 600,
        rate_limit_delay: float = 0.5
    ) -> List[SwarmProcess]:
        """
        Spawn multiple agents with p-limit style concurrency control.
        
        This is the core "Swarm Generator Pattern".
        """
        semaphore = asyncio.Semaphore(concurrency)
        results = []
        
        async def limited_spawn(idx: int, prompt: str):
            async with semaphore:
                # Rate limiting
                await asyncio.sleep(rate_limit_delay)
                
                task_id = f"swarm-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{idx:04d}"
                print(f"🚀 [{idx+1}/{len(prompts)}] Spawning {agent} → {task_id}")
                
                return await self._spawn_single(
                    task_id=task_id,
                    agent=agent,
                    prompt=prompt,
                    model_tier=model_tier,
                    timeout=timeout
                )
        
        # Create tasks
        tasks = [limited_spawn(i, p) for i, p in enumerate(prompts)]
        
        # Execute with concurrency limit
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        valid_results = []
        for r in results:
            if isinstance(r, Exception):
                print(f"❌ Task failed: {r}")
            else:
                valid_results.append(r)
        
        return valid_results
    
    def list_processes(self, include_completed: bool = False) -> List[Dict]:
        """List all swarm processes."""
        self._cleanup_dead_processes()
        
        processes = []
        for pid, proc in self._active_processes.items():
            if include_completed or proc.status == "running":
                processes.append({
                    "pid": pid,
                    "task_id": proc.task_id,
                    "agent": proc.agent,
                    "status": proc.status,
                    "started_at": proc.started_at,
                    "ended_at": proc.ended_at
                })
        
        return sorted(processes, key=lambda p: p["started_at"], reverse=True)
    
    def kill_process(self, pid: int) -> bool:
        """Kill a specific process."""
        if pid not in self._active_processes:
            return False
        
        try:
            # Kill the entire process group
            os.killpg(os.getpgid(pid), signal.SIGTERM)
            self._active_processes[pid].status = "killed"
            self._active_processes[pid].ended_at = datetime.utcnow().isoformat()
            self._save_state()
            return True
        except (OSError, ProcessLookupError):
            self._active_processes[pid].status = "completed"
            self._save_state()
            return False
    
    def nuke(self) -> int:
        """
        Emergency kill switch - terminate ALL swarm processes.
        
        This is the "Nuke Everything" button from MACS.
        """
        killed = 0
        
        for pid, proc in list(self._active_processes.items()):
            if proc.status == "running":
                try:
                    os.killpg(os.getpgid(pid), signal.SIGKILL)
                    killed += 1
                except (OSError, ProcessLookupError):
                    pass
                
                proc.status = "killed"
                proc.ended_at = datetime.utcnow().isoformat()
        
        self._save_state()
        print(f"☢️ NUKED {killed} processes")
        return killed
    
    def get_stats(self) -> Dict:
        """Get swarm statistics."""
        self._cleanup_dead_processes()
        
        stats = {
            "running": 0,
            "completed": 0,
            "failed": 0,
            "killed": 0,
            "total": len(self._active_processes)
        }
        
        for proc in self._active_processes.values():
            if proc.status in stats:
                stats[proc.status] += 1
        
        return stats


def main():
    parser = argparse.ArgumentParser(
        description='Swarm CLI - Parallel Agent Orchestration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Spawn command (single agent, multiple prompts)
    spawn_parser = subparsers.add_parser('spawn', help='Spawn worker agents')
    spawn_parser.add_argument('--agent', '-a', required=True, help='Agent to use')
    spawn_parser.add_argument('--prompt', '-p', help='Single prompt (use {i} for index)')
    spawn_parser.add_argument('--prompts-file', '-f', help='JSON file with list of prompts')
    spawn_parser.add_argument('--count', '-n', type=int, default=1, help='Number of instances')
    spawn_parser.add_argument('--concurrency', '-c', type=int, default=5, help='Max concurrent')
    spawn_parser.add_argument('--timeout', '-t', type=int, default=600, help='Timeout per task')
    spawn_parser.add_argument('--model-tier', choices=['SMALL', 'MIDDLE', 'BIG'], default='SMALL')
    spawn_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # PS command (list processes)
    ps_parser = subparsers.add_parser('ps', help='List swarm processes')
    ps_parser.add_argument('--all', '-a', action='store_true', help='Include completed')
    ps_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Kill command
    kill_parser = subparsers.add_parser('kill', help='Kill a process')
    kill_parser.add_argument('pid', type=int, help='Process ID to kill')
    
    # Nuke command
    nuke_parser = subparsers.add_parser('nuke', help='Kill ALL swarm processes')
    nuke_parser.add_argument('--force', '-f', action='store_true', help='Skip confirmation')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show swarm statistics')
    stats_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    cli = SwarmCLI()
    
    try:
        if args.command == 'spawn':
            # Build prompt list
            if args.prompts_file:
                with open(args.prompts_file) as f:
                    prompts = json.load(f)
            elif args.prompt:
                prompts = [args.prompt.replace('{i}', str(i)) for i in range(args.count)]
            else:
                print("❌ Provide --prompt or --prompts-file")
                sys.exit(1)
            
            print(f"🐝 Spawning {len(prompts)} workers with concurrency {args.concurrency}")
            
            results = asyncio.run(cli.spawn_batch(
                agent=args.agent,
                prompts=prompts,
                concurrency=args.concurrency,
                model_tier=args.model_tier,
                timeout=args.timeout
            ))
            
            completed = sum(1 for r in results if r.status == "completed")
            failed = len(results) - completed
            
            if args.json:
                print(json.dumps({
                    "success": True,
                    "total": len(results),
                    "completed": completed,
                    "failed": failed,
                    "results": [asdict(r) for r in results]
                }, indent=2))
            else:
                print(f"\n✅ Batch complete: {completed}/{len(results)} succeeded")
        
        elif args.command == 'ps':
            processes = cli.list_processes(include_completed=args.all)
            
            if args.json:
                print(json.dumps({"processes": processes}, indent=2))
            else:
                print(f"🐝 Active swarm processes: {len(processes)}")
                for p in processes[:20]:
                    icon = {"running": "🔄", "completed": "✅", "failed": "❌", "killed": "☠️"}.get(p['status'], "❓")
                    print(f"  {icon} PID:{p['pid']} | {p['agent']} | {p['status']} | {p['task_id']}")
        
        elif args.command == 'kill':
            success = cli.kill_process(args.pid)
            print(f"{'✅ Killed' if success else '❌ Failed to kill'} PID {args.pid}")
        
        elif args.command == 'nuke':
            if not args.force:
                confirm = input("☢️ This will kill ALL swarm processes. Type 'NUKE' to confirm: ")
                if confirm != 'NUKE':
                    print("Aborted.")
                    sys.exit(0)
            
            killed = cli.nuke()
            print(f"☢️ Killed {killed} processes")
        
        elif args.command == 'stats':
            stats = cli.get_stats()
            
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                print("📊 Swarm Statistics:")
                for key, val in stats.items():
                    icon = {"running": "🔄", "completed": "✅", "failed": "❌", "killed": "☠️", "total": "📊"}.get(key, "")
                    print(f"  {icon} {key}: {val}")
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted. Use 'swarm_cli.py nuke' to kill running processes.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
