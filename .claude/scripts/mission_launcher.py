#!/usr/bin/env python3
"""
MACS Mission Launcher

Implements the Isolate-Inject-Ignite pattern for mission isolation.
Creates temporary mission directories with symlinked components.

Usage:
    python scripts/mission_launcher.py launch --agents code-reviewer,tester --prompt "Review PR"
    python scripts/mission_launcher.py list
    python scripts/mission_launcher.py cleanup --mission-id abc123
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict


@dataclass
class Mission:
    """A mission with isolated context and continuation support."""
    mission_id: str
    prompt: str
    agents: List[str]
    skills: List[str]
    status: str = "pending"  # pending, running, completed, failed, continuing
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None
    exit_code: Optional[int] = None
    output_path: Optional[str] = None
    # Continuation support
    nudge_prompt: Optional[str] = None  # The "keep going" prompt
    nudge_count: int = 0  # How many times to auto-continue
    nudges_sent: int = 0  # How many nudges have been sent
    nudge_delay: int = 5  # Seconds between nudges
    continuation_prompts: List[str] = field(default_factory=list)  # Sequenced prompts


class MissionLauncher:
    """Service for managing isolated missions."""
    
    BASE_DIR = Path(".super_agent_monitor/missions")
    COMPONENTS_DIR = Path("components")
    
    def __init__(self):
        self.BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _get_mission_dir(self, mission_id: str) -> Path:
        return self.BASE_DIR / mission_id
    
    def _get_mission_meta_path(self, mission_id: str) -> Path:
        return self._get_mission_dir(mission_id) / "mission.json"
    
    def launch(
        self,
        prompt: str,
        agents: List[str],
        skills: Optional[List[str]] = None,
        dry_run: bool = False,
        nudge_prompt: Optional[str] = None,
        nudge_count: int = 0,
        nudge_delay: int = 5,
        continuation_prompts: Optional[List[str]] = None
    ) -> Mission:
        """
        Launch a new isolated mission.
        
        Pattern: Isolate → Inject → Ignite
        
        1. ISOLATE: Create temporary mission directory
        2. INJECT: Symlink required agents/skills from pool
        3. IGNITE: Execute with scoped context
        """
        skills = skills or []
        mission_id = f"mission-{uuid.uuid4().hex[:8]}"
        mission_dir = self._get_mission_dir(mission_id)
        
        # ===== 1. ISOLATE =====
        print(f"📁 Creating isolated mission: {mission_id}")
        
        # Create directory structure
        (mission_dir / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
        (mission_dir / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
        
        # ===== 2. INJECT =====
        print(f"🔗 Injecting {len(agents)} agents and {len(skills)} skills")
        
        # Symlink agents
        for agent in agents:
            source = (self.COMPONENTS_DIR / "agents" / f"{agent}.md").resolve()
            target = mission_dir / ".claude" / "agents" / f"{agent}.md"
            
            if source.exists():
                if not dry_run:
                    # Use relative symlink for portability
                    rel_source = os.path.relpath(source, target.parent)
                    target.symlink_to(rel_source)
                print(f"  ✓ Agent: {agent}")
            else:
                print(f"  ⚠ Agent not found: {agent}")
        
        # Symlink skills
        for skill in skills:
            source = (self.COMPONENTS_DIR / "skills" / skill).resolve()
            target = mission_dir / ".claude" / "skills" / skill
            
            if source.exists():
                if not dry_run:
                    rel_source = os.path.relpath(source, target.parent)
                    target.symlink_to(rel_source)
                print(f"  ✓ Skill: {skill}")
            else:
                print(f"  ⚠ Skill not found: {skill}")
        
        # Create mission metadata
        mission = Mission(
            mission_id=mission_id,
            prompt=prompt,
            agents=agents,
            skills=skills,
            status="pending",
            output_path=str(mission_dir / "output.txt"),
            nudge_prompt=nudge_prompt,
            nudge_count=nudge_count,
            nudge_delay=nudge_delay,
            continuation_prompts=continuation_prompts or []
        )
        
        if not dry_run:
            self._save_mission(mission)
        
        # ===== 3. IGNITE =====
        if not dry_run:
            print(f"🚀 Igniting mission...")
            mission = self._execute_mission(mission)
        else:
            print(f"🔍 Dry run complete. Would execute in: {mission_dir}")
        
        return mission
    
    def _save_mission(self, mission: Mission):
        """Save mission metadata."""
        path = self._get_mission_meta_path(mission.mission_id)
        with open(path, 'w') as f:
            json.dump(asdict(mission), f, indent=2)
    
    def _load_mission(self, mission_id: str) -> Optional[Mission]:
        """Load mission metadata."""
        path = self._get_mission_meta_path(mission_id)
        if not path.exists():
            return None
        
        with open(path) as f:
            data = json.load(f)
        return Mission(**data)
    
    def _execute_mission(self, mission: Mission) -> Mission:
        """Execute the mission with Claude Code, including continuations."""
        mission_dir = self._get_mission_dir(mission.mission_id)
        
        mission.status = "running"
        self._save_mission(mission)
        
        # Build list of all prompts to execute
        all_prompts = [mission.prompt]
        
        # Add sequenced continuation prompts
        if mission.continuation_prompts:
            all_prompts.extend(mission.continuation_prompts)
        
        # Execute each prompt in sequence
        for prompt_idx, current_prompt in enumerate(all_prompts):
            print(f"📤 Prompt {prompt_idx + 1}/{len(all_prompts)}")
            
            success = self._run_single_prompt(mission, current_prompt, prompt_idx)
            
            if not success and prompt_idx < len(all_prompts) - 1:
                print(f"⚠️ Prompt {prompt_idx + 1} failed, stopping continuation chain")
                break
        
        # After initial prompts, apply nudges if configured
        if mission.nudge_prompt and mission.nudge_count > 0:
            mission.status = "continuing"
            self._save_mission(mission)
            
            for nudge_idx in range(mission.nudge_count):
                print(f"🔄 Nudge {nudge_idx + 1}/{mission.nudge_count}: waiting {mission.nudge_delay}s...")
                import time
                time.sleep(mission.nudge_delay)
                
                mission.nudges_sent = nudge_idx + 1
                self._save_mission(mission)
                
                success = self._run_single_prompt(
                    mission, 
                    mission.nudge_prompt, 
                    len(all_prompts) + nudge_idx
                )
                
                if not success:
                    print(f"⚠️ Nudge {nudge_idx + 1} failed, stopping nudge loop")
                    break
        
        # Finalize
        mission.status = "completed" if mission.exit_code == 0 else "failed"
        mission.completed_at = datetime.utcnow().isoformat()
        self._save_mission(mission)
        
        return mission
    
    def _run_single_prompt(self, mission: Mission, prompt: str, idx: int) -> bool:
        """Run a single prompt and append output."""
        mission_dir = self._get_mission_dir(mission.mission_id)
        
        try:
            cmd = [
                "claude",
                "-p", prompt,
                "--output-format", "stream-json",
                "--dangerously-skip-permissions"
            ]
            
            result = subprocess.run(
                cmd,
                cwd=mission_dir,
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            # Append output (don't overwrite)
            output_path = mission_dir / f"output_{idx}.txt"
            with open(output_path, 'w') as f:
                f.write(result.stdout)
            
            if result.stderr:
                error_path = mission_dir / f"error_{idx}.txt"
                with open(error_path, 'w') as f:
                    f.write(result.stderr)
            
            mission.exit_code = result.returncode
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            mission.exit_code = -1
            return False
        except FileNotFoundError:
            print("⚠️ Claude CLI not found.")
            mission.status = "pending"
            return False
        except Exception as e:
            print(f"❌ Execution error: {e}")
            mission.exit_code = -1
            return False
    
    def list_missions(self) -> List[Dict]:
        """List all missions."""
        missions = []
        
        for mission_dir in self.BASE_DIR.iterdir():
            if mission_dir.is_dir():
                mission = self._load_mission(mission_dir.name)
                if mission:
                    missions.append({
                        "mission_id": mission.mission_id,
                        "status": mission.status,
                        "agents": mission.agents,
                        "created_at": mission.created_at
                    })
        
        return sorted(missions, key=lambda m: m["created_at"], reverse=True)
    
    def cleanup(self, mission_id: str, force: bool = False) -> bool:
        """Clean up a mission directory."""
        mission_dir = self._get_mission_dir(mission_id)
        
        if not mission_dir.exists():
            print(f"⚠️ Mission not found: {mission_id}")
            return False
        
        mission = self._load_mission(mission_id)
        if mission and mission.status == "running" and not force:
            print(f"⚠️ Mission is running. Use --force to clean up.")
            return False
        
        shutil.rmtree(mission_dir)
        print(f"🗑️ Cleaned up mission: {mission_id}")
        return True
    
    def cleanup_all(self, older_than_hours: int = 24) -> int:
        """Clean up old missions."""
        from datetime import timedelta
        
        now = datetime.utcnow()
        threshold = now - timedelta(hours=older_than_hours)
        cleaned = 0
        
        for mission_dir in list(self.BASE_DIR.iterdir()):
            if mission_dir.is_dir():
                mission = self._load_mission(mission_dir.name)
                if mission:
                    created = datetime.fromisoformat(mission.created_at.replace('Z', '+00:00').replace('+00:00', ''))
                    if created < threshold and mission.status != "running":
                        self.cleanup(mission.mission_id)
                        cleaned += 1
        
        return cleaned


def main():
    parser = argparse.ArgumentParser(
        description='MACS Mission Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Launch command
    launch_parser = subparsers.add_parser('launch', help='Launch a new mission')
    launch_parser.add_argument('--prompt', '-p', required=True, help='Mission prompt')
    launch_parser.add_argument('--agents', '-a', required=True, 
                               help='Comma-separated list of agents')
    launch_parser.add_argument('--skills', '-s', default='',
                               help='Comma-separated list of skills')
    launch_parser.add_argument('--dry-run', '-n', action='store_true',
                               help='Prepare but do not execute')
    launch_parser.add_argument('--json', action='store_true', help='Output as JSON')
    # Continuation options
    launch_parser.add_argument('--nudge', help='Nudge prompt to send after completion')
    launch_parser.add_argument('--nudge-count', type=int, default=0,
                               help='Number of times to repeat nudge prompt')
    launch_parser.add_argument('--nudge-delay', type=int, default=5,
                               help='Seconds between nudges')
    launch_parser.add_argument('--continue-with', nargs='+',
                               help='Additional prompts to run after initial (space-separated)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all missions')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up a mission')
    cleanup_parser.add_argument('--mission-id', '-m', help='Mission ID to clean up')
    cleanup_parser.add_argument('--all', action='store_true', help='Clean up all old missions')
    cleanup_parser.add_argument('--older-than', type=int, default=24,
                                help='Clean missions older than N hours')
    cleanup_parser.add_argument('--force', '-f', action='store_true',
                                help='Force cleanup of running missions')
    cleanup_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Get mission status')
    status_parser.add_argument('--mission-id', '-m', required=True, help='Mission ID')
    status_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    launcher = MissionLauncher()
    
    try:
        if args.command == 'launch':
            agents = [a.strip() for a in args.agents.split(',') if a.strip()]
            skills = [s.strip() for s in args.skills.split(',') if s.strip()]
            
            mission = launcher.launch(
                prompt=args.prompt,
                agents=agents,
                skills=skills,
                dry_run=args.dry_run,
                nudge_prompt=args.nudge,
                nudge_count=args.nudge_count,
                nudge_delay=args.nudge_delay,
                continuation_prompts=args.continue_with
            )
            
            result = {
                "success": True,
                "mission_id": mission.mission_id,
                "status": mission.status,
                "agents": mission.agents
            }
            
        elif args.command == 'list':
            missions = launcher.list_missions()
            result = {"success": True, "missions": missions, "count": len(missions)}
            
        elif args.command == 'cleanup':
            if args.all:
                cleaned = launcher.cleanup_all(args.older_than)
                result = {"success": True, "cleaned": cleaned}
            elif args.mission_id:
                success = launcher.cleanup(args.mission_id, args.force)
                result = {"success": success}
            else:
                print("Specify --mission-id or --all")
                sys.exit(1)
                
        elif args.command == 'status':
            mission = launcher._load_mission(args.mission_id)
            if mission:
                result = {"success": True, **asdict(mission)}
            else:
                result = {"success": False, "error": "Mission not found"}
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if args.command == 'list':
                print(f"📋 {result['count']} missions:")
                for m in result['missions'][:10]:
                    status_icon = {"pending": "⏳", "running": "🔄", "completed": "✅", "failed": "❌"}.get(m['status'], "❓")
                    print(f"  {status_icon} {m['mission_id']} | {m['status']} | {', '.join(m['agents'][:3])}")
            else:
                print(f"✅ {args.command}: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        result = {"success": False, "error": str(e)}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
