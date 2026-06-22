#!/usr/bin/env python3
"""
Skill Loader - Progressive Disclosure for Skills

Implements the progressive disclosure pattern from SwarmForge:
- Agent reads only SKILL.md metadata first (lightweight)
- Full content loaded only if skill matches task
- Dependency resolution between skills

Usage:
    python scripts/skill_loader.py list
    python scripts/skill_loader.py match --query "analyze code quality"
    python scripts/skill_loader.py load --skill adversarial-validation
    python scripts/skill_loader.py inject --skills "scan-project,remediation-plan" --mission-dir /tmp/mission
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, List, Dict, Any


@dataclass
class SkillMetadata:
    """Lightweight skill metadata from YAML frontmatter."""
    name: str
    description: str
    version: str = "1.0.0"
    category: str = "general"
    dependencies: List[str] = None
    tags: List[str] = None
    complexity: str = "medium"
    token_estimate: int = 500
    file_path: str = ""
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []


class SkillLoader:
    """
    Skill Loader with progressive disclosure.
    
    Key principles from SwarmForge:
    1. "DO NOT READ THE FULL SKILL" - Parse only frontmatter first
    2. Match skills to intent via tags/description
    3. Load full content only when needed
    """
    
    SKILLS_DIR = Path(".claude/skills")
    DOT_CLAUDE_SKILLS = Path("docs/amalgam/dot-claude/skills")
    CLAUDE_CODE_SKILLS = Path("docs/amalgam/claude-code/skills")
    
    def __init__(self):
        self._cache: Dict[str, SkillMetadata] = {}
        self._scan_skills()
    
    def _parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """Parse YAML frontmatter from markdown."""
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            return {}
        
        frontmatter = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Handle lists
                if value.startswith('[') and value.endswith(']'):
                    try:
                        value = json.loads(value.replace("'", '"'))
                    except:
                        value = [v.strip() for v in value[1:-1].split(',')]
                
                frontmatter[key] = value
        
        return frontmatter
    
    def _scan_skills(self):
        """Scan all skill directories and cache metadata."""
        skill_dirs = [
            self.SKILLS_DIR,
            self.DOT_CLAUDE_SKILLS,
            self.CLAUDE_CODE_SKILLS
        ]
        
        for skill_dir in skill_dirs:
            if not skill_dir.exists():
                continue
            
            # Handle both files and directories
            for item in skill_dir.iterdir():
                if item.is_file() and item.suffix == '.md':
                    self._process_skill_file(item)
                elif item.is_dir():
                    skill_file = item / "SKILL.md"
                    if skill_file.exists():
                        self._process_skill_file(skill_file)
    
    def _process_skill_file(self, path: Path):
        """Process a skill file and extract metadata."""
        try:
            content = path.read_text()
            frontmatter = self._parse_frontmatter(content)
            
            # Generate name from filename or frontmatter
            name = frontmatter.get('name', path.stem)
            
            metadata = SkillMetadata(
                name=name,
                description=frontmatter.get('description', ''),
                version=frontmatter.get('version', '1.0.0'),
                category=frontmatter.get('category', 'general'),
                dependencies=frontmatter.get('dependencies', []),
                tags=frontmatter.get('tags', []),
                complexity=frontmatter.get('complexity', 'medium'),
                token_estimate=self._estimate_tokens(content),
                file_path=str(path)
            )
            
            self._cache[name] = metadata
            
        except Exception as e:
            print(f"⚠️ Failed to process {path}: {e}")
    
    def _estimate_tokens(self, content: str) -> int:
        """Estimate token count (rough: 4 chars per token)."""
        return len(content) // 4
    
    def list_skills(self) -> List[Dict]:
        """List all available skills with metadata."""
        skills = []
        for name, meta in sorted(self._cache.items()):
            skills.append({
                "name": name,
                "description": meta.description[:100] + "..." if len(meta.description) > 100 else meta.description,
                "category": meta.category,
                "complexity": meta.complexity,
                "tokens": meta.token_estimate
            })
        return skills
    
    def match_skills(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Match skills to a query using keyword matching.
        
        For production, this would use embeddings/vector search.
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scores = []
        for name, meta in self._cache.items():
            score = 0
            
            # Name match (highest weight)
            if query_lower in name.lower():
                score += 10
            
            # Description match
            desc_lower = meta.description.lower()
            for word in query_words:
                if word in desc_lower:
                    score += 2
            
            # Tag match
            for tag in meta.tags:
                if tag.lower() in query_lower or any(w in tag.lower() for w in query_words):
                    score += 5
            
            if score > 0:
                scores.append({
                    "name": name,
                    "score": score,
                    "description": meta.description[:100],
                    "category": meta.category,
                    "file_path": meta.file_path
                })
        
        # Sort by score descending
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:limit]
    
    def load_skill(self, name: str) -> Optional[str]:
        """Load full skill content."""
        if name not in self._cache:
            return None
        
        meta = self._cache[name]
        try:
            return Path(meta.file_path).read_text()
        except Exception:
            return None
    
    def resolve_dependencies(self, skill_names: List[str]) -> List[str]:
        """
        Resolve skill dependencies recursively.
        
        Returns ordered list with dependencies first.
        """
        resolved = []
        seen = set()
        
        def resolve(name: str):
            if name in seen:
                return
            seen.add(name)
            
            if name in self._cache:
                for dep in self._cache[name].dependencies:
                    resolve(dep)
                resolved.append(name)
        
        for name in skill_names:
            resolve(name)
        
        return resolved
    
    def inject_skills(self, skill_names: List[str], mission_dir: Path) -> int:
        """
        Inject skills into a mission directory.
        
        Creates symlinks in mission_dir/.claude/skills/
        """
        target_dir = mission_dir / ".claude" / "skills"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Resolve dependencies
        all_skills = self.resolve_dependencies(skill_names)
        injected = 0
        
        for name in all_skills:
            if name not in self._cache:
                print(f"⚠️ Skill not found: {name}")
                continue
            
            meta = self._cache[name]
            source = Path(meta.file_path)
            
            if source.is_file():
                target = target_dir / source.name
            else:
                target = target_dir / name
            
            try:
                if target.exists():
                    target.unlink()
                
                # Use relative symlink
                rel_source = os.path.relpath(source, target.parent)
                target.symlink_to(rel_source)
                injected += 1
                print(f"  ✓ {name}")
                
            except Exception as e:
                print(f"  ❌ {name}: {e}")
        
        return injected
    
    def get_stats(self) -> Dict:
        """Get skill statistics."""
        categories = {}
        total_tokens = 0
        
        for meta in self._cache.values():
            cat = meta.category
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
            total_tokens += meta.token_estimate
        
        return {
            "total_skills": len(self._cache),
            "categories": categories,
            "total_tokens": total_tokens,
            "avg_tokens": total_tokens // max(len(self._cache), 1)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Skill Loader - Progressive Disclosure for Skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all skills')
    list_parser.add_argument('--category', '-c', help='Filter by category')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Match command
    match_parser = subparsers.add_parser('match', help='Match skills to query')
    match_parser.add_argument('--query', '-q', required=True, help='Query string')
    match_parser.add_argument('--limit', '-n', type=int, default=5, help='Max results')
    match_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load full skill content')
    load_parser.add_argument('--skill', '-s', required=True, help='Skill name')
    
    # Inject command
    inject_parser = subparsers.add_parser('inject', help='Inject skills into mission')
    inject_parser.add_argument('--skills', '-s', required=True, help='Comma-separated skill names')
    inject_parser.add_argument('--mission-dir', '-m', required=True, help='Mission directory')
    inject_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show skill statistics')
    stats_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    loader = SkillLoader()
    
    try:
        if args.command == 'list':
            skills = loader.list_skills()
            
            if args.category:
                skills = [s for s in skills if s['category'] == args.category]
            
            if args.json:
                print(json.dumps({"skills": skills}, indent=2))
            else:
                print(f"📚 {len(skills)} skills available:")
                for s in skills:
                    print(f"  • {s['name']:<30} [{s['category']}] {s['tokens']} tokens")
        
        elif args.command == 'match':
            matches = loader.match_skills(args.query, args.limit)
            
            if args.json:
                print(json.dumps({"matches": matches}, indent=2))
            else:
                print(f"🔍 Top matches for '{args.query}':")
                for m in matches:
                    print(f"  • {m['name']:<30} (score: {m['score']}) - {m['description'][:50]}...")
        
        elif args.command == 'load':
            content = loader.load_skill(args.skill)
            if content:
                print(content)
            else:
                print(f"❌ Skill not found: {args.skill}")
                sys.exit(1)
        
        elif args.command == 'inject':
            skills = [s.strip() for s in args.skills.split(',') if s.strip()]
            mission_dir = Path(args.mission_dir)
            
            print(f"💉 Injecting {len(skills)} skills into {mission_dir}")
            injected = loader.inject_skills(skills, mission_dir)
            
            result = {"success": True, "injected": injected, "requested": len(skills)}
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Injected {injected}/{len(skills)} skills")
        
        elif args.command == 'stats':
            stats = loader.get_stats()
            
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                print("📊 Skill Statistics:")
                print(f"  📚 Total skills: {stats['total_skills']}")
                print(f"  📝 Average tokens: {stats['avg_tokens']}")
                print("  📁 Categories:")
                for cat, count in stats['categories'].items():
                    print(f"      • {cat}: {count}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
