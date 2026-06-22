#!/usr/bin/env python3
"""
Agent Token Optimizer

Analyzes agent files and suggests/applies optimizations to reduce token count.
Target: <500 tokens per agent (PRD requirement).

Usage:
    python scripts/optimize_agents.py --analyze
    python scripts/optimize_agents.py --optimize --agent code-reviewer
    python scripts/optimize_agents.py --optimize-all --dry-run
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class AgentOptimizer:
    """Optimizes agent files for token efficiency."""
    
    AGENTS_DIR = Path(".claude/agents")
    TARGET_TOKENS = 500
    WARNING_TOKENS = 700
    
    # Token estimation (rough: 4 chars = 1 token)
    CHARS_PER_TOKEN = 4
    
    # Sections that can be trimmed
    TRIMMABLE_SECTIONS = [
        "## Examples",
        "## Detailed Instructions", 
        "## Notes",
        "## History",
        "## Changelog"
    ]
    
    # Required sections (should not be removed)
    REQUIRED_SECTIONS = [
        "## Mission",
        "## Workflow",
        "## Constraints",
        "## Output"
    ]
    
    def __init__(self):
        self.agents = {}
        self._scan_agents()
    
    def _scan_agents(self):
        """Scan all agent files."""
        for agent_file in self.AGENTS_DIR.glob("*.md"):
            if agent_file.is_file():
                content = agent_file.read_text()
                tokens = len(content) // self.CHARS_PER_TOKEN
                
                self.agents[agent_file.stem] = {
                    "path": agent_file,
                    "content": content,
                    "tokens": tokens,
                    "over_limit": tokens > self.TARGET_TOKENS
                }
    
    def analyze(self) -> Dict:
        """Analyze all agents and return statistics."""
        stats = {
            "total": len(self.agents),
            "under_target": 0,
            "over_target": 0,
            "over_warning": 0,
            "avg_tokens": 0,
            "agents": []
        }
        
        total_tokens = 0
        for name, info in sorted(self.agents.items(), key=lambda x: x[1]["tokens"], reverse=True):
            total_tokens += info["tokens"]
            
            if info["tokens"] <= self.TARGET_TOKENS:
                stats["under_target"] += 1
                status = "✅"
            elif info["tokens"] <= self.WARNING_TOKENS:
                stats["over_target"] += 1
                status = "⚠️"
            else:
                stats["over_warning"] += 1
                status = "❌"
            
            stats["agents"].append({
                "name": name,
                "tokens": info["tokens"],
                "status": status,
                "reduction_needed": max(0, info["tokens"] - self.TARGET_TOKENS)
            })
        
        stats["avg_tokens"] = total_tokens // max(len(self.agents), 1)
        return stats
    
    def _extract_frontmatter(self, content: str) -> Tuple[str, str]:
        """Extract YAML frontmatter from content."""
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            frontmatter = match.group(0)
            body = content[len(frontmatter):]
            return frontmatter, body
        return "", content
    
    def _find_trimmable_sections(self, content: str) -> List[str]:
        """Find sections that can be trimmed."""
        found = []
        for section in self.TRIMMABLE_SECTIONS:
            if section in content:
                found.append(section)
        return found
    
    def _optimize_content(self, content: str) -> str:
        """Apply optimizations to reduce token count."""
        frontmatter, body = self._extract_frontmatter(content)
        
        # Remove trimmable sections
        for section in self.TRIMMABLE_SECTIONS:
            # Match section header and content until next ## or end
            pattern = rf'{re.escape(section)}.*?(?=\n## |\Z)'
            body = re.sub(pattern, '', body, flags=re.DOTALL)
        
        # Remove excessive whitespace
        body = re.sub(r'\n{3,}', '\n\n', body)
        
        # Trim trailing whitespace from lines
        body = '\n'.join(line.rstrip() for line in body.split('\n'))
        
        # Remove excessive bullet point descriptions
        # Keep first sentence only for long bullet points
        lines = body.split('\n')
        optimized_lines = []
        for line in lines:
            if line.strip().startswith('-') and len(line) > 150:
                # Trim to first sentence
                first_sentence = re.match(r'^(- [^.!?]+[.!?])', line)
                if first_sentence:
                    line = first_sentence.group(1)
            optimized_lines.append(line)
        body = '\n'.join(optimized_lines)
        
        return frontmatter + body.strip() + '\n'
    
    def optimize_agent(self, name: str, dry_run: bool = False) -> Dict:
        """Optimize a single agent."""
        if name not in self.agents:
            return {"success": False, "error": f"Agent not found: {name}"}
        
        info = self.agents[name]
        original_tokens = info["tokens"]
        
        optimized_content = self._optimize_content(info["content"])
        new_tokens = len(optimized_content) // self.CHARS_PER_TOKEN
        reduction = original_tokens - new_tokens
        
        result = {
            "name": name,
            "original_tokens": original_tokens,
            "new_tokens": new_tokens,
            "reduction": reduction,
            "meets_target": new_tokens <= self.TARGET_TOKENS
        }
        
        if not dry_run and reduction > 0:
            info["path"].write_text(optimized_content)
            result["applied"] = True
        else:
            result["applied"] = False
        
        return result
    
    def optimize_all(self, dry_run: bool = False) -> List[Dict]:
        """Optimize all agents."""
        results = []
        for name in self.agents:
            result = self.optimize_agent(name, dry_run)
            results.append(result)
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Agent Token Optimizer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--analyze', action='store_true', help='Analyze all agents')
    parser.add_argument('--optimize', action='store_true', help='Optimize single agent')
    parser.add_argument('--optimize-all', action='store_true', help='Optimize all agents')
    parser.add_argument('--agent', '-a', help='Agent name for --optimize')
    parser.add_argument('--dry-run', '-n', action='store_true', help="Don't write changes")
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    optimizer = AgentOptimizer()
    
    if args.analyze:
        stats = optimizer.analyze()
        
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print(f"\n📊 Agent Token Analysis")
            print(f"{'='*50}")
            print(f"Total agents: {stats['total']}")
            print(f"Under target ({optimizer.TARGET_TOKENS}): {stats['under_target']} ✅")
            print(f"Over target: {stats['over_target']} ⚠️")
            print(f"Over warning ({optimizer.WARNING_TOKENS}): {stats['over_warning']} ❌")
            print(f"Average tokens: {stats['avg_tokens']}")
            print(f"\n{'='*50}")
            print(f"Top 10 largest agents:")
            for agent in stats["agents"][:10]:
                print(f"  {agent['status']} {agent['name']:<30} {agent['tokens']:>5} tokens")
    
    elif args.optimize:
        if not args.agent:
            print("❌ Specify --agent <name>")
            sys.exit(1)
        
        result = optimizer.optimize_agent(args.agent, args.dry_run)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("error"):
                print(f"❌ {result['error']}")
            else:
                action = "Would reduce" if args.dry_run else "Reduced"
                print(f"✅ {args.agent}: {result['original_tokens']} → {result['new_tokens']} tokens ({action} by {result['reduction']})")
    
    elif args.optimize_all:
        results = optimizer.optimize_all(args.dry_run)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            total_reduction = sum(r['reduction'] for r in results)
            improved = sum(1 for r in results if r['reduction'] > 0)
            action = "Would save" if args.dry_run else "Saved"
            print(f"✅ Optimized {improved}/{len(results)} agents")
            print(f"   {action} ~{total_reduction} tokens total")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
