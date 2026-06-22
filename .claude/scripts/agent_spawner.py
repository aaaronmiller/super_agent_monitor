#!/usr/bin/env python3
"""
Agent Spawner Integration

Unified interface for spawning agents using swarm_cli, mission_launcher,
and council orchestration.

Usage:
    python scripts/agent_spawner.py spawn --agent code-reviewer --prompt "Review this PR"
    python scripts/agent_spawner.py swarm --swarm security-swarm --prompt "Audit codebase"
    python scripts/agent_spawner.py council --topic "Best approach for migration"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional


class AgentSpawner:
    """
    Unified agent spawning interface.
    
    Modes:
    1. Single agent spawn (via mission_launcher)
    2. Swarm deployment (via swarm_registry + swarm_cli)
    3. Council decision (via council.py)
    """
    
    SCRIPTS_DIR = Path(__file__).parent
    
    def spawn_agent(
        self,
        agent: str,
        prompt: str,
        skills: List[str] = None,
        nudge: str = None,
        nudge_count: int = 0
    ) -> Dict:
        """Spawn a single agent via mission_launcher."""
        cmd = [
            sys.executable,
            str(self.SCRIPTS_DIR / "mission_launcher.py"),
            "launch",
            "--prompt", prompt,
            "--agents", agent,
            "--json"
        ]
        
        if skills:
            cmd.extend(["--skills", ",".join(skills)])
        
        if nudge:
            cmd.extend(["--nudge", nudge])
            cmd.extend(["--nudge-count", str(nudge_count)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def spawn_swarm(
        self,
        swarm: str,
        prompt: str,
        concurrency: int = 3,
        target: Path = None
    ) -> Dict:
        """Deploy and spawn a swarm."""
        import tempfile
        
        if target is None:
            target = Path(tempfile.mkdtemp(prefix="swarm_"))
        
        # Deploy swarm configuration
        deploy_cmd = [
            sys.executable,
            str(self.SCRIPTS_DIR / "swarm_registry.py"),
            "deploy",
            "--swarm", swarm,
            "--target", str(target),
            "--json"
        ]
        
        try:
            result = subprocess.run(deploy_cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return {"success": False, "error": "Failed to deploy swarm"}
            
            deploy_info = json.loads(result.stdout)
            
            # Get swarm info for agent list
            info_cmd = [
                sys.executable,
                str(self.SCRIPTS_DIR / "swarm_registry.py"),
                "info",
                "--swarm", swarm,
                "--json"
            ]
            result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=10)
            swarm_info = json.loads(result.stdout)
            
            # Spawn agents via swarm_cli
            spawn_cmd = [
                sys.executable,
                str(self.SCRIPTS_DIR / "swarm_cli.py"),
                "spawn",
                "--prompt", prompt,
                "--agent", swarm_info["agents"][0] if swarm_info["agents"] else "default",
                "--count", str(len(swarm_info["agents"])),
                "--concurrency", str(concurrency),
                "--json"
            ]
            
            result = subprocess.run(spawn_cmd, capture_output=True, text=True, timeout=300)
            
            return {
                "success": True,
                "swarm": swarm,
                "target": str(target),
                "agents_spawned": len(swarm_info["agents"]),
                "deploy_info": deploy_info
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def spawn_council(
        self,
        topic: str,
        agents: List[str] = None
    ) -> Dict:
        """Spawn council for decision making."""
        if agents is None:
            agents = ["architect", "product-manager", "security-expert"]
        
        council_cmd = [
            sys.executable,
            str(self.SCRIPTS_DIR / "council.py"),
            "vote",
            "--topic", topic,
            "--agents", ",".join(agents),
            "--json"
        ]
        
        try:
            result = subprocess.run(council_cmd, capture_output=True, text=True, timeout=600)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {"success": False, "error": result.stderr}
        except FileNotFoundError:
            return {"success": False, "error": "council.py not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self) -> Dict:
        """Get status of all spawned agents."""
        status_cmd = [
            sys.executable,
            str(self.SCRIPTS_DIR / "swarm_cli.py"),
            "ps",
            "--json"
        ]
        
        try:
            result = subprocess.run(status_cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {"processes": []}
        except Exception:
            return {"processes": []}


def main():
    parser = argparse.ArgumentParser(
        description='Agent Spawner Integration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Spawn single agent
    spawn_parser = subparsers.add_parser('spawn', help='Spawn single agent')
    spawn_parser.add_argument('--agent', '-a', required=True, help='Agent name')
    spawn_parser.add_argument('--prompt', '-p', required=True, help='Prompt')
    spawn_parser.add_argument('--skills', '-s', help='Comma-separated skills')
    spawn_parser.add_argument('--nudge', help='Nudge prompt')
    spawn_parser.add_argument('--nudge-count', type=int, default=0, help='Nudge count')
    spawn_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Spawn swarm
    swarm_parser = subparsers.add_parser('swarm', help='Deploy and spawn swarm')
    swarm_parser.add_argument('--swarm', '-s', required=True, help='Swarm name')
    swarm_parser.add_argument('--prompt', '-p', required=True, help='Prompt')
    swarm_parser.add_argument('--concurrency', '-c', type=int, default=3, help='Concurrency')
    swarm_parser.add_argument('--target', '-t', help='Target directory')
    swarm_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Spawn council
    council_parser = subparsers.add_parser('council', help='Spawn council')
    council_parser.add_argument('--topic', '-t', required=True, help='Discussion topic')
    council_parser.add_argument('--agents', '-a', help='Comma-separated agents')
    council_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Status
    status_parser = subparsers.add_parser('status', help='Get spawner status')
    status_parser.add_argument('--json', action='store_true', help='JSON output')
    
    args = parser.parse_args()
    spawner = AgentSpawner()
    
    if args.command == 'spawn':
        skills = args.skills.split(',') if args.skills else None
        result = spawner.spawn_agent(
            agent=args.agent,
            prompt=args.prompt,
            skills=skills,
            nudge=args.nudge,
            nudge_count=args.nudge_count
        )
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("success") or result.get("mission_id"):
                print(f"✅ Spawned agent: {args.agent}")
                print(f"   Mission: {result.get('mission_id', 'N/A')}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    elif args.command == 'swarm':
        target = Path(args.target) if args.target else None
        result = spawner.spawn_swarm(
            swarm=args.swarm,
            prompt=args.prompt,
            concurrency=args.concurrency,
            target=target
        )
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("success"):
                print(f"✅ Swarm deployed: {args.swarm}")
                print(f"   Target: {result.get('target')}")
                print(f"   Agents: {result.get('agents_spawned')}")
            else:
                print(f"❌ Failed: {result.get('error')}")
    
    elif args.command == 'council':
        agents = args.agents.split(',') if args.agents else None
        result = spawner.spawn_council(topic=args.topic, agents=agents)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("success") or result.get("decision"):
                print(f"🏛️ Council decision on: {args.topic}")
                print(f"   Decision: {result.get('decision', 'Pending')}")
            else:
                print(f"❌ Failed: {result.get('error')}")
    
    elif args.command == 'status':
        result = spawner.get_status()
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            processes = result.get("processes", [])
            print(f"📊 Active agents: {len(processes)}")
            for p in processes[:10]:
                print(f"   • {p.get('agent', 'unknown')}: {p.get('status', 'N/A')}")


if __name__ == "__main__":
    main()
