#!/usr/bin/env python3
"""
Super Agent Monitor CLI - Unified Command Interface

One command to discover and run all Super Agent Monitor tools.

Usage:
    sam --help
    sam spawn --agent code-reviewer --prompt "Review this"
    sam swarm --list
    sam plan --goal "Build feature X"
    sam status
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run_script(script: str, args: list):
    """Run a script with arguments."""
    cmd = [sys.executable, str(SCRIPTS_DIR / script)] + args
    return subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(
        description='Super Agent Monitor CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available subsystems:
  spawn       Spawn agents (via agent_spawner.py)
  swarm       Manage swarm configurations (via swarm_registry.py)
  mission     Manage missions (via mission_launcher.py)
  skill       Manage skills (via skill_loader.py)
  rag         RAG memory system (via rag_server.py)
  plan        Create execution plans (via orchestrator.py)
  budget      Check budget status (via budget_governor.py)
  optimize    Optimize agents (via optimize_agents.py)
  status      Show overall status
  test        Run integration tests
        """
    )
    
    parser.add_argument('subsystem', nargs='?', help='Subsystem to use')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for subsystem')
    
    # Quick status without subsystem
    parser.add_argument('--status', '-s', action='store_true', help='Show quick status')
    parser.add_argument('--version', '-v', action='store_true', help='Show version')
    
    args = parser.parse_args()
    
    if args.version:
        print("Super Agent Monitor v2.0")
        return 0
    
    if args.status or args.subsystem == 'status':
        print("📊 Super Agent Monitor Status\n")
        
        # Budget
        budget_script = SCRIPTS_DIR.parent / "hooks" / "budget_governor.py"
        subprocess.run([sys.executable, str(budget_script), "--status"])
        print()
        
        # Swarms
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "swarm_registry.py"), "stats", "--json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            print(f"🐝 Swarms: {data['total_swarms']} available ({data['total_agents']} agents)")
        
        # Skills
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "skill_loader.py"), "stats", "--json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            print(f"📚 Skills: {data['total_skills']} indexed")
        
        # Active processes
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "swarm_cli.py"), "stats", "--json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            print(f"🔄 Active: {data.get('running', 0)} processes")
        
        return 0
    
    # Map subsystems to scripts
    script_map = {
        'spawn': ('agent_spawner.py', None),
        'swarm': ('swarm_registry.py', None),
        'mission': ('mission_launcher.py', None),
        'skill': ('skill_loader.py', None),
        'rag': ('rag_server.py', None),
        'plan': ('orchestrator.py', 'plan'),
        'execute': ('orchestrator.py', 'execute'),
        'budget': ('../hooks/budget_governor.py', ['--status']),
        'optimize': ('optimize_agents.py', None),
        'test': ('../../tests/test_prd_integration.py', None),
        'ingest': ('memory_ingest.py', None),
    }
    
    if args.subsystem in script_map:
        script, default_cmd = script_map[args.subsystem]
        
        cmd_args = []
        if default_cmd:
            if isinstance(default_cmd, list):
                cmd_args.extend(default_cmd)
            else:
                cmd_args.append(default_cmd)
        
        cmd_args.extend(args.args)
        return run_script(script, cmd_args).returncode
    
    elif args.subsystem:
        print(f"Unknown subsystem: {args.subsystem}")
        print("Use --help to see available subsystems")
        return 1
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
