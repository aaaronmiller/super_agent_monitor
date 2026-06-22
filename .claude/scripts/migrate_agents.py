#!/usr/bin/env python3
"""
Agent Template Migration Tool

Migrates existing agents to the v2.0 optimal template format (~450 tokens).

Features:
    - Token counting per agent
    - Automatic field additions (model, complexity, icon)
    - Verbose content extraction to skills
    - Validation against schema

Usage:
    python migrate_agents.py --analyze              # Analyze current agents
    python migrate_agents.py --migrate              # Run migration
    python migrate_agents.py --validate             # Validate all agents
"""

import os
import sys
import re
import json
import yaml
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


# Constants
AGENTS_DIR = Path(__file__).parent.parent / "components" / "agents"
SKILLS_DIR = Path(__file__).parent.parent / "components" / "skills"
TOKEN_TARGET = 500  # Target ~500 tokens per agent
TOKEN_MAX = 800  # Max allowed tokens


@dataclass
class AgentAnalysis:
    """Analysis result for a single agent."""
    path: Path
    name: str
    token_count: int
    has_model: bool
    has_complexity: bool
    has_icon: bool
    has_version: bool
    issues: List[str]


def count_tokens(text: str) -> int:
    """Rough token count: ~4 chars per token."""
    return len(text) // 4


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            body = match.group(2)
            return frontmatter, body
        except yaml.YAMLError:
            return {}, content
    return {}, content


def generate_frontmatter(data: Dict[str, Any]) -> str:
    """Generate YAML frontmatter string."""
    return f"---\n{yaml.dump(data, default_flow_style=False, sort_keys=False)}---\n"


def infer_model_tier(agent_name: str, frontmatter: Dict, body: str) -> str:
    """Infer model tier based on agent characteristics."""
    name_lower = agent_name.lower()
    
    # Keywords suggesting high complexity
    if any(kw in name_lower for kw in ['architect', 'lead', 'orchestrator', 'consolidator', 'master']):
        return 'opus'
    
    # Keywords suggesting low complexity
    if any(kw in name_lower for kw in ['scanner', 'scraper', 'formatter', 'monitor', 'docs']):
        return 'haiku'
    
    # Default to sonnet
    return 'sonnet'


def infer_complexity(agent_name: str, token_count: int) -> str:
    """Infer complexity based on agent name and size."""
    name_lower = agent_name.lower()
    
    if any(kw in name_lower for kw in ['architect', 'lead', 'orchestrator', 'master']):
        return 'high'
    
    if token_count > 600 or any(kw in name_lower for kw in ['analyzer', 'reviewer', 'auditor']):
        return 'medium'
    
    return 'low'


def suggest_icon(agent_name: str) -> str:
    """Suggest emoji icon based on agent name."""
    icon_map = {
        'research': '🔬',
        'code': '💻',
        'review': '👁️',
        'security': '🔒',
        'test': '🧪',
        'architec': '🏛️',
        'document': '📄',
        'monitor': '📊',
        'scraper': '🕷️',
        'analyzer': '🔍',
        'auditor': '✅',
        'web': '🌐',
        'database': '🗄️',
        'devops': '⚙️',
        'backend': '🖥️',
        'frontend': '🎨',
        'memory': '🧠',
        'github': '🐙',
        'file': '📁',
        'organizer': '📋',
        'promotion': '📢',
        'publication': '📰',
        'tester': '🔧',
    }
    
    name_lower = agent_name.lower()
    for keyword, icon in icon_map.items():
        if keyword in name_lower:
            return icon
    
    return '🤖'  # Default


def analyze_agent(path: Path) -> AgentAnalysis:
    """Analyze a single agent file."""
    content = path.read_text()
    frontmatter, body = parse_frontmatter(content)
    
    name = frontmatter.get('name', path.stem)
    token_count = count_tokens(content)
    
    issues = []
    
    # Check required fields
    has_model = 'model' in frontmatter
    has_complexity = 'complexity' in frontmatter
    has_icon = 'icon' in frontmatter
    has_version = 'version' in frontmatter
    
    if not has_model:
        issues.append("Missing 'model' field")
    if not has_complexity:
        issues.append("Missing 'complexity' field")
    if not has_version:
        issues.append("Missing 'version' field")
    
    # Check token count
    if token_count > TOKEN_MAX:
        issues.append(f"Token count {token_count} exceeds max {TOKEN_MAX}")
    elif token_count > TOKEN_TARGET:
        issues.append(f"Token count {token_count} exceeds target {TOKEN_TARGET}")
    
    # Check for standard sections
    if '## Mission' not in body:
        issues.append("Missing '## Mission' section")
    if '## Workflow' not in body:
        issues.append("Missing '## Workflow' section")
    
    return AgentAnalysis(
        path=path,
        name=name,
        token_count=token_count,
        has_model=has_model,
        has_complexity=has_complexity,
        has_icon=has_icon,
        has_version=has_version,
        issues=issues
    )


def analyze_all_agents() -> List[AgentAnalysis]:
    """Analyze all agents in the components/agents directory."""
    agents = []
    
    for path in AGENTS_DIR.glob("*.md"):
        if path.name.startswith('_'):
            continue
        agents.append(analyze_agent(path))
    
    return sorted(agents, key=lambda a: a.name)


def migrate_agent(path: Path, dry_run: bool = True) -> bool:
    """Migrate a single agent to v2.0 format."""
    content = path.read_text()
    frontmatter, body = parse_frontmatter(content)
    
    name = frontmatter.get('name', path.stem)
    token_count = count_tokens(content)
    modified = False
    
    # Add version if missing
    if 'version' not in frontmatter:
        frontmatter['version'] = '1.0.0'
        modified = True
    
    # Add model if missing
    if 'model' not in frontmatter:
        frontmatter['model'] = infer_model_tier(name, frontmatter, body)
        modified = True
    
    # Add complexity if missing
    if 'complexity' not in frontmatter:
        frontmatter['complexity'] = infer_complexity(name, token_count)
        modified = True
    
    # Add icon if missing
    if 'icon' not in frontmatter:
        frontmatter['icon'] = suggest_icon(name)
        modified = True
    
    if modified and not dry_run:
        # Reconstruct file
        new_content = generate_frontmatter(frontmatter) + body
        path.write_text(new_content)
    
    return modified


def print_analysis_report(agents: List[AgentAnalysis]):
    """Print a summary report of agent analysis."""
    print("\n" + "=" * 60)
    print("🔍 Agent Template Analysis Report")
    print("=" * 60)
    
    total = len(agents)
    over_target = sum(1 for a in agents if a.token_count > TOKEN_TARGET)
    over_max = sum(1 for a in agents if a.token_count > TOKEN_MAX)
    missing_model = sum(1 for a in agents if not a.has_model)
    missing_complexity = sum(1 for a in agents if not a.has_complexity)
    
    print(f"\n📊 Summary:")
    print(f"  Total agents: {total}")
    print(f"  Over target ({TOKEN_TARGET}): {over_target}")
    print(f"  Over max ({TOKEN_MAX}): {over_max}")
    print(f"  Missing 'model': {missing_model}")
    print(f"  Missing 'complexity': {missing_complexity}")
    
    avg_tokens = sum(a.token_count for a in agents) // total if total else 0
    print(f"  Average tokens: {avg_tokens}")
    
    if any(a.issues for a in agents):
        print(f"\n⚠️ Agents with issues:")
        for agent in agents:
            if agent.issues:
                print(f"\n  📄 {agent.name} ({agent.token_count} tokens)")
                for issue in agent.issues:
                    print(f"     ❌ {issue}")
    else:
        print(f"\n✅ All agents pass validation!")
    
    print("\n" + "=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Agent Template Migration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--analyze', '-a', action='store_true',
                        help='Analyze all agents and report issues')
    parser.add_argument('--migrate', '-m', action='store_true',
                        help='Migrate agents to v2.0 format')
    parser.add_argument('--validate', '-v', action='store_true',
                        help='Validate all agents against schema')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would be changed without modifying files')
    parser.add_argument('--agent', type=str, default=None,
                        help='Process only specified agent')
    
    args = parser.parse_args()
    
    if not any([args.analyze, args.migrate, args.validate]):
        args.analyze = True  # Default to analyze
    
    if not AGENTS_DIR.exists():
        print(f"❌ Agents directory not found: {AGENTS_DIR}")
        sys.exit(1)
    
    if args.agent:
        agent_path = AGENTS_DIR / f"{args.agent}.md"
        if not agent_path.exists():
            print(f"❌ Agent not found: {args.agent}")
            sys.exit(1)
        agents = [analyze_agent(agent_path)]
    else:
        agents = analyze_all_agents()
    
    if args.analyze or args.validate:
        print_analysis_report(agents)
    
    if args.migrate:
        print("\n🔄 Migrating agents to v2.0 format...")
        migrated = 0
        
        for analysis in agents:
            if migrate_agent(analysis.path, dry_run=args.dry_run):
                action = "Would migrate" if args.dry_run else "Migrated"
                print(f"  {action}: {analysis.name}")
                migrated += 1
        
        if args.dry_run:
            print(f"\n📝 Would migrate {migrated} agents (dry run)")
        else:
            print(f"\n✅ Migrated {migrated} agents")


if __name__ == "__main__":
    main()
