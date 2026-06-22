#!/usr/bin/env python3
"""
Swarm Registry - Discovery and Management of Swarm Configurations

Provides a centralized registry for discovering, listing, and deploying
pre-configured swarm configurations.

Usage:
    python scripts/swarm_registry.py list
    python scripts/swarm_registry.py info --swarm security-swarm
    python scripts/swarm_registry.py deploy --swarm api-swarm --target /tmp/mission
"""

import argparse
import json
import os
import shutil
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class SwarmConfig:
    """A swarm configuration from the registry."""
    name: str
    path: Path
    agents: List[str]
    hooks: List[str]
    scripts: List[str]
    description: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "path": str(self.path),
            "agents": self.agents,
            "hooks": self.hooks,
            "scripts": self.scripts,
            "description": self.description
        }


class SwarmRegistry:
    """
    Registry for discovering and managing swarm configurations.
    
    Swarms are pre-configured multi-agent setups for specific domains:
    - api-swarm: API development and maintenance
    - security-swarm: Security auditing and vulnerability scanning
    - test-swarm: Test generation and coverage analysis
    - etc.
    """
    
    SWARMS_DIR = Path(".claude/swarms")
    
    def __init__(self):
        self._swarms: Dict[str, SwarmConfig] = {}
        self._scan_swarms()
    
    def _scan_swarms(self):
        """Scan for swarm configurations."""
        if not self.SWARMS_DIR.exists():
            return
        
        for swarm_dir in self.SWARMS_DIR.iterdir():
            if not swarm_dir.is_dir() or swarm_dir.name.startswith('.'):
                continue
            
            claude_dir = swarm_dir / ".claude"
            if not claude_dir.exists():
                continue
            
            # Collect components
            agents = []
            hooks = []
            scripts = []
            description = ""
            
            # List agents
            agents_dir = claude_dir / "agents"
            if agents_dir.exists():
                agents = [f.stem for f in agents_dir.glob("*.md")]
            
            # List hooks
            hooks_dir = claude_dir / "hooks"
            if hooks_dir.exists():
                hooks = [f.name for f in hooks_dir.glob("*.py")]
            
            # List scripts
            scripts_dir = claude_dir / "scripts"
            if scripts_dir.exists():
                scripts = [f.name for f in scripts_dir.glob("*.py")]
            
            # Get description from CLAUDE.md
            claude_md = claude_dir / "CLAUDE.md"
            if claude_md.exists():
                content = claude_md.read_text()
                # First line after # header
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('#'):
                        if i + 1 < len(lines) and lines[i + 1].strip():
                            description = lines[i + 1].strip()
                        break
            
            self._swarms[swarm_dir.name] = SwarmConfig(
                name=swarm_dir.name,
                path=swarm_dir,
                agents=agents,
                hooks=hooks,
                scripts=scripts,
                description=description
            )
    
    def list_swarms(self) -> List[Dict]:
        """List all available swarms."""
        swarms = []
        for name, config in sorted(self._swarms.items()):
            swarms.append({
                "name": name,
                "agents": len(config.agents),
                "hooks": len(config.hooks),
                "scripts": len(config.scripts),
                "description": config.description[:80] if config.description else ""
            })
        return swarms
    
    def get_swarm_info(self, name: str) -> Optional[Dict]:
        """Get detailed info about a swarm."""
        if name not in self._swarms:
            return None
        return self._swarms[name].to_dict()
    
    def deploy_swarm(self, name: str, target: Path, dry_run: bool = False) -> Dict:
        """
        Deploy a swarm configuration to a target directory.
        
        Creates the .claude directory structure with all components.
        """
        if name not in self._swarms:
            return {"success": False, "error": f"Swarm not found: {name}"}
        
        config = self._swarms[name]
        source = config.path / ".claude"
        target_claude = target / ".claude"
        
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "source": str(source),
                "target": str(target_claude),
                "components": {
                    "agents": config.agents,
                    "hooks": config.hooks,
                    "scripts": config.scripts
                }
            }
        
        # Copy .claude directory
        if target_claude.exists():
            shutil.rmtree(target_claude)
        shutil.copytree(source, target_claude)
        
        return {
            "success": True,
            "deployed": name,
            "target": str(target),
            "agents": len(config.agents),
            "hooks": len(config.hooks)
        }
    
    def get_stats(self) -> Dict:
        """Get registry statistics."""
        total_agents = 0
        total_hooks = 0
        total_scripts = 0
        
        for config in self._swarms.values():
            total_agents += len(config.agents)
            total_hooks += len(config.hooks)
            total_scripts += len(config.scripts)
        
        return {
            "total_swarms": len(self._swarms),
            "total_agents": total_agents,
            "total_hooks": total_hooks,
            "total_scripts": total_scripts
        }


def main():
    parser = argparse.ArgumentParser(
        description='Swarm Registry',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all swarms')
    list_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get swarm info')
    info_parser.add_argument('--swarm', '-s', required=True, help='Swarm name')
    info_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy a swarm')
    deploy_parser.add_argument('--swarm', '-s', required=True, help='Swarm to deploy')
    deploy_parser.add_argument('--target', '-t', required=True, help='Target directory')
    deploy_parser.add_argument('--dry-run', '-n', action='store_true', help="Don't copy")
    deploy_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.add_argument('--json', action='store_true', help='JSON output')
    
    args = parser.parse_args()
    registry = SwarmRegistry()
    
    if args.command == 'list':
        swarms = registry.list_swarms()
        
        if args.json:
            print(json.dumps({"swarms": swarms}, indent=2))
        else:
            print(f"🐝 {len(swarms)} swarms available:")
            for s in swarms:
                print(f"  • {s['name']:<25} {s['agents']} agents, {s['hooks']} hooks")
                if s['description']:
                    print(f"    {s['description']}")
    
    elif args.command == 'info':
        info = registry.get_swarm_info(args.swarm)
        
        if not info:
            print(f"❌ Swarm not found: {args.swarm}")
            return 1
        
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print(f"🐝 {info['name']}")
            print(f"   📁 Path: {info['path']}")
            print(f"   👤 Agents ({len(info['agents'])}):")
            for agent in info['agents']:
                print(f"      • {agent}")
            if info['hooks']:
                print(f"   🔧 Hooks: {', '.join(info['hooks'])}")
            if info['scripts']:
                print(f"   📜 Scripts: {', '.join(info['scripts'])}")
    
    elif args.command == 'deploy':
        target = Path(args.target)
        result = registry.deploy_swarm(args.swarm, target, args.dry_run)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result['success']:
                action = "Would deploy" if args.dry_run else "Deployed"
                print(f"✅ {action} {args.swarm} to {target}")
                if 'agents' in result:
                    print(f"   {result['agents']} agents, {result['hooks']} hooks")
            else:
                print(f"❌ {result['error']}")
    
    elif args.command == 'stats':
        stats = registry.get_stats()
        
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("📊 Swarm Registry Statistics:")
            print(f"  🐝 Total swarms: {stats['total_swarms']}")
            print(f"  👤 Total agents: {stats['total_agents']}")
            print(f"  🔧 Total hooks: {stats['total_hooks']}")
            print(f"  📜 Total scripts: {stats['total_scripts']}")


if __name__ == "__main__":
    main()
