#!/usr/bin/env python3
"""
File Phylogeny Tracker
======================
Tracks file lineage, evolution, and relationships using:
- Git history analysis (renames, modifications)
- SimHash fingerprinting (content similarity)
- Manual assertions (lineage comments)
- Idea bundles (conceptual groupings)

Usage:
    python phylogeny.py scan           # Scan and generate .lineage.json
    python phylogeny.py graph          # Generate mermaid visualization
    python phylogeny.py show <file>    # Show lineage for specific file
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# ============================================================================
# SimHash Implementation (64-bit fingerprint for content similarity)
# ============================================================================

def tokenize(text: str, n: int = 3) -> List[str]:
    """Generate n-gram shingles from text."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    if len(words) < n:
        return words
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]


def hash_token(token: str) -> int:
    """Hash a token to a 64-bit integer."""
    h = hashlib.md5(token.encode()).hexdigest()
    return int(h[:16], 16)


def compute_simhash(text: str) -> str:
    """Compute 64-bit SimHash fingerprint for text content."""
    tokens = tokenize(text)
    if not tokens:
        return "0" * 16
    
    v = [0] * 64
    for token in tokens:
        h = hash_token(token)
        for i in range(64):
            if h & (1 << i):
                v[i] += 1
            else:
                v[i] -= 1
    
    fingerprint = 0
    for i in range(64):
        if v[i] > 0:
            fingerprint |= (1 << i)
    
    return format(fingerprint, '016x')


def hamming_distance(hash1: str, hash2: str) -> int:
    """Calculate Hamming distance between two SimHash fingerprints."""
    n1 = int(hash1, 16)
    n2 = int(hash2, 16)
    return bin(n1 ^ n2).count('1')


def is_similar(hash1: str, hash2: str, threshold: int = 4) -> bool:
    """Check if two files are similar based on SimHash distance."""
    return hamming_distance(hash1, hash2) <= threshold


# ============================================================================
# Git History Analysis
# ============================================================================

def get_git_root() -> Optional[Path]:
    """Get the root of the git repository."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True, text=True, check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        return None


def get_file_renames(filepath: str) -> List[Tuple[str, str, str]]:
    """
    Get rename history for a file using git log --follow.
    Returns list of (commit_hash, old_path, new_path).
    """
    try:
        result = subprocess.run(
            ['git', 'log', '--follow', '--name-status', '--format=%H', '--', filepath],
            capture_output=True, text=True, check=True
        )
        
        renames = []
        lines = result.stdout.strip().split('\n')
        current_commit = None
        
        for line in lines:
            if len(line) == 40 and all(c in '0123456789abcdef' for c in line):
                current_commit = line
            elif line.startswith('R'):
                # Rename: R100\told_path\tnew_path
                parts = line.split('\t')
                if len(parts) >= 3:
                    renames.append((current_commit, parts[1], parts[2]))
        
        return renames
    except subprocess.CalledProcessError:
        return []


def get_file_creation_date(filepath: str) -> Optional[str]:
    """Get the creation date of a file from git history."""
    try:
        result = subprocess.run(
            ['git', 'log', '--follow', '--format=%aI', '--reverse', '--', filepath],
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.strip().split('\n')
        if lines and lines[0]:
            return lines[0][:10]  # Just the date part
    except subprocess.CalledProcessError:
        pass
    return None


def get_files_modified_together(filepath: str, limit: int = 10) -> List[str]:
    """Get files that are often modified together with this file."""
    try:
        result = subprocess.run(
            ['git', 'log', '--name-only', '--format=', '-n', str(limit), '--', filepath],
            capture_output=True, text=True, check=True
        )
        
        files = set()
        for line in result.stdout.strip().split('\n'):
            if line and line != filepath:
                files.add(line)
        
        return list(files)
    except subprocess.CalledProcessError:
        return []


# ============================================================================
# Lineage Comment Parsing
# ============================================================================

def parse_lineage_comments(filepath: Path) -> Dict[str, List[str]]:
    """
    Parse lineage assertions from file comments.
    Syntax: <!-- lineage: ancestor=old_file.md -->
            <!-- lineage: produces=output.py -->
            <!-- lineage: related=similar.md -->
    """
    assertions = {
        'ancestors': [],
        'produces': [],
        'related': []
    }
    
    try:
        content = filepath.read_text(errors='ignore')
        
        # Match HTML-style comments
        pattern = r'<!--\s*lineage:\s*(\w+)=([^>]+)\s*-->'
        for match in re.finditer(pattern, content):
            key = match.group(1).strip()
            value = match.group(2).strip()
            
            if key == 'ancestor':
                assertions['ancestors'].append(value)
            elif key in ('produces', 'deliverable'):
                assertions['produces'].append(value)
            elif key == 'related':
                assertions['related'].append(value)
        
        # Also match Python/shell style comments
        pattern = r'#\s*lineage:\s*(\w+)=(.+)$'
        for match in re.finditer(pattern, content, re.MULTILINE):
            key = match.group(1).strip()
            value = match.group(2).strip()
            
            if key == 'ancestor':
                assertions['ancestors'].append(value)
            elif key in ('produces', 'deliverable'):
                assertions['produces'].append(value)
            elif key == 'related':
                assertions['related'].append(value)
    except Exception:
        pass
    
    return assertions


# ============================================================================
# Reference Scanning
# ============================================================================

def scan_references(filepath: Path, all_files: Set[str]) -> List[str]:
    """Find references to other project files within this file."""
    references = []
    
    try:
        content = filepath.read_text(errors='ignore')
        
        for other_file in all_files:
            if other_file != str(filepath):
                basename = os.path.basename(other_file)
                # Check if the filename is mentioned
                if basename in content:
                    references.append(other_file)
    except Exception:
        pass
    
    return references


# ============================================================================
# Data Model
# ============================================================================

@dataclass
class FileEntry:
    path: str
    simhash: str
    lineage: str  # SOURCE, MIDPOINT, DELIVERABLE, LOG, ORPHAN
    created: Optional[str]
    ancestors: List[str]
    produces: List[str]
    related: List[str]
    task: Optional[str]
    references: List[str]


@dataclass
class Task:
    name: str
    sources: List[str]
    deliverables: List[str]
    status: str  # COMPLETE, IN_PROGRESS, ABANDONED


@dataclass
class IdeaBundle:
    name: str
    files: List[str]
    description: str


@dataclass
class LineageData:
    version: str
    generated: str
    files: Dict[str, FileEntry]
    tasks: Dict[str, Task]
    idea_bundles: List[IdeaBundle]
    similarity_pairs: List[Tuple[str, str, int]]  # (file1, file2, distance)


# ============================================================================
# Main Scanner
# ============================================================================

class PhylogenyScanner:
    def __init__(self, root: Path):
        self.root = root
        self.files: Dict[str, FileEntry] = {}
        self.simhashes: Dict[str, str] = {}
        self.all_file_paths: Set[str] = set()
        
        # Patterns to ignore
        self.ignore_patterns = [
            r'node_modules', r'\.git', r'__pycache__', r'\.pyc$',
            r'\.egg-info', r'dist/', r'build/', r'\.DS_Store',
            r'\.lineage\.json$', r'venv/', r'\.env'
        ]
    
    def should_ignore(self, path: str) -> bool:
        """Check if path should be ignored."""
        for pattern in self.ignore_patterns:
            if re.search(pattern, path):
                return True
        return False
    
    def classify_lineage(self, filepath: Path, entry: FileEntry) -> str:
        """Classify file lineage type based on analysis."""
        name = filepath.name.lower()
        
        # Check for explicit assertions first
        if entry.produces:
            return "SOURCE"
        if entry.ancestors:
            if entry.produces:
                return "MIDPOINT"
            return "DELIVERABLE"
        
        # Heuristic classification
        if name.endswith(('.log', '.tmp', '_log.md')):
            return "LOG"
        if 'scratch' in name or 'draft' in name or 'wip' in name:
            return "DRAFT"
        if name.startswith(('prd', 'spec', 'requirement')):
            return "SOURCE"
        if filepath.suffix in ('.py', '.js', '.ts', '.sh'):
            return "DELIVERABLE"
        if filepath.suffix == '.md':
            # Check if it's in a docs or planning folder
            parts = filepath.parts
            if 'docs' in parts or 'NEXT_STEPS' in parts or 'specifications' in parts:
                return "SOURCE"
        
        return "ORPHAN"
    
    def scan(self) -> LineageData:
        """Scan the project and build lineage data."""
        print("🔍 Scanning project...")
        
        # Collect all files
        for root, dirs, files in os.walk(self.root):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self.should_ignore(d)]
            
            for filename in files:
                filepath = Path(root) / filename
                rel_path = str(filepath.relative_to(self.root))
                
                if self.should_ignore(rel_path):
                    continue
                
                self.all_file_paths.add(rel_path)
        
        print(f"  Found {len(self.all_file_paths)} files")
        
        # Analyze each file
        for rel_path in sorted(self.all_file_paths):
            filepath = self.root / rel_path
            
            # Compute SimHash for text files
            simhash = "0" * 16
            if filepath.suffix in ('.md', '.txt', '.py', '.js', '.ts', '.sh', '.yaml', '.json'):
                try:
                    content = filepath.read_text(errors='ignore')
                    simhash = compute_simhash(content)
                except Exception:
                    pass
            
            self.simhashes[rel_path] = simhash
            
            # Parse lineage assertions
            assertions = parse_lineage_comments(filepath)
            
            # Get git history
            created = get_file_creation_date(rel_path)
            renames = get_file_renames(rel_path)
            
            # Build entry
            entry = FileEntry(
                path=rel_path,
                simhash=simhash,
                lineage="ORPHAN",
                created=created,
                ancestors=[r[1] for r in renames] + assertions['ancestors'],
                produces=assertions['produces'],
                related=assertions['related'],
                task=None,
                references=scan_references(filepath, self.all_file_paths)
            )
            
            # Classify
            entry.lineage = self.classify_lineage(filepath, entry)
            
            self.files[rel_path] = entry
        
        # Find similar files
        print("🔬 Detecting content similarity...")
        similarity_pairs = []
        file_list = list(self.simhashes.keys())
        
        for i, f1 in enumerate(file_list):
            for f2 in file_list[i+1:]:
                if self.simhashes[f1] != "0" * 16 and self.simhashes[f2] != "0" * 16:
                    dist = hamming_distance(self.simhashes[f1], self.simhashes[f2])
                    if dist <= 6:  # Threshold for "related"
                        similarity_pairs.append((f1, f2, dist))
        
        print(f"  Found {len(similarity_pairs)} similar file pairs")
        
        # Build lineage data
        return LineageData(
            version="1.0",
            generated=datetime.now().isoformat(),
            files=self.files,
            tasks={},  # TODO: auto-detect tasks
            idea_bundles=[],  # TODO: auto-cluster
            similarity_pairs=similarity_pairs
        )
    
    def generate_mermaid(self, data: LineageData) -> str:
        """Generate mermaid diagram of file lineage."""
        lines = ["graph TD"]
        
        # Add nodes by lineage type
        for path, entry in data.files.items():
            if entry.lineage == "ORPHAN":
                continue
            
            node_id = path.replace('/', '_').replace('.', '_').replace('-', '_')
            label = os.path.basename(path)
            
            style = {
                "SOURCE": ":::source",
                "MIDPOINT": ":::midpoint",
                "DELIVERABLE": ":::deliverable",
                "LOG": ":::log",
                "DRAFT": ":::draft"
            }.get(entry.lineage, "")
            
            lines.append(f"  {node_id}[{label}]{style}")
            
            # Add edges for ancestors
            for ancestor in entry.ancestors:
                anc_id = ancestor.replace('/', '_').replace('.', '_').replace('-', '_')
                lines.append(f"  {anc_id} --> {node_id}")
            
            # Add edges for produces
            for prod in entry.produces:
                prod_id = prod.replace('/', '_').replace('.', '_').replace('-', '_')
                lines.append(f"  {node_id} --> {prod_id}")
        
        # Add similarity edges (dashed)
        for f1, f2, dist in data.similarity_pairs[:20]:  # Limit for readability
            id1 = f1.replace('/', '_').replace('.', '_').replace('-', '_')
            id2 = f2.replace('/', '_').replace('.', '_').replace('-', '_')
            lines.append(f"  {id1} -.-> {id2}")
        
        # Add styles
        lines.extend([
            "",
            "  classDef source fill:#90EE90",
            "  classDef midpoint fill:#87CEEB",
            "  classDef deliverable fill:#DDA0DD",
            "  classDef log fill:#D3D3D3",
            "  classDef draft fill:#FFE4B5"
        ])
        
        return '\n'.join(lines)


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="File Phylogeny Tracker")
    parser.add_argument('command', choices=['scan', 'graph', 'show', 'similar'],
                        help="Command to run")
    parser.add_argument('file', nargs='?', help="File to analyze (for show/similar)")
    parser.add_argument('--output', '-o', default='.lineage.json',
                        help="Output file for lineage data")
    
    args = parser.parse_args()
    
    git_root = get_git_root()
    if not git_root:
        print("❌ Not in a git repository")
        sys.exit(1)
    
    scanner = PhylogenyScanner(git_root)
    
    if args.command == 'scan':
        data = scanner.scan()
        
        # Convert to JSON-serializable format
        output = {
            'version': data.version,
            'generated': data.generated,
            'files': {k: asdict(v) for k, v in data.files.items()},
            'tasks': {k: asdict(v) for k, v in data.tasks.items()},
            'idea_bundles': [asdict(b) for b in data.idea_bundles],
            'similarity_pairs': data.similarity_pairs
        }
        
        output_path = git_root / args.output
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✅ Lineage data written to {args.output}")
        print(f"   Files analyzed: {len(data.files)}")
        print(f"   Similar pairs: {len(data.similarity_pairs)}")
        
        # Summary by lineage type
        lineage_counts = defaultdict(int)
        for entry in data.files.values():
            lineage_counts[entry.lineage] += 1
        
        print("\n📊 Lineage Summary:")
        for lineage, count in sorted(lineage_counts.items()):
            print(f"   {lineage}: {count}")
    
    elif args.command == 'graph':
        # Load existing lineage data or scan
        lineage_path = git_root / args.output
        if lineage_path.exists():
            with open(lineage_path) as f:
                raw = json.load(f)
            data = LineageData(
                version=raw['version'],
                generated=raw['generated'],
                files={k: FileEntry(**v) for k, v in raw['files'].items()},
                tasks={k: Task(**v) for k, v in raw['tasks'].items()},
                idea_bundles=[IdeaBundle(**b) for b in raw['idea_bundles']],
                similarity_pairs=[tuple(s) for s in raw['similarity_pairs']]
            )
        else:
            data = scanner.scan()
        
        mermaid = scanner.generate_mermaid(data)
        print(mermaid)
    
    elif args.command == 'show':
        if not args.file:
            print("❌ Please specify a file")
            sys.exit(1)
        
        lineage_path = git_root / args.output
        if not lineage_path.exists():
            print("❌ No lineage data found. Run 'scan' first.")
            sys.exit(1)
        
        with open(lineage_path) as f:
            raw = json.load(f)
        
        if args.file in raw['files']:
            entry = raw['files'][args.file]
            print(f"\n📄 {args.file}")
            print(f"   Lineage: {entry['lineage']}")
            print(f"   SimHash: {entry['simhash']}")
            print(f"   Created: {entry['created'] or 'Unknown'}")
            if entry['ancestors']:
                print(f"   Ancestors: {', '.join(entry['ancestors'])}")
            if entry['produces']:
                print(f"   Produces: {', '.join(entry['produces'])}")
            if entry['references']:
                print(f"   References: {', '.join(entry['references'][:5])}")
        else:
            print(f"❌ File not found in lineage data: {args.file}")
    
    elif args.command == 'similar':
        if not args.file:
            print("❌ Please specify a file")
            sys.exit(1)
        
        lineage_path = git_root / args.output
        if not lineage_path.exists():
            print("❌ No lineage data found. Run 'scan' first.")
            sys.exit(1)
        
        with open(lineage_path) as f:
            raw = json.load(f)
        
        target_hash = raw['files'].get(args.file, {}).get('simhash')
        if not target_hash:
            print(f"❌ File not found or no hash: {args.file}")
            sys.exit(1)
        
        print(f"\n🔍 Files similar to {args.file}:")
        for path, entry in raw['files'].items():
            if path != args.file and entry['simhash'] != "0" * 16:
                dist = hamming_distance(target_hash, entry['simhash'])
                if dist <= 6:
                    print(f"   [{dist}] {path}")


if __name__ == '__main__':
    main()
