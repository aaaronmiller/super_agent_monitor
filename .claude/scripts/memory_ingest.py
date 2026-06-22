#!/usr/bin/env python3
"""
Memory Ingestion Pipeline

Ingests project context into RAG for agent memory augmentation.
Supports markdown, code, and documentation files.

Phases:
1. SCAN: Discover all relevant files
2. CHUNK: Split into context-appropriate chunks
3. EMBED: Generate embeddings
4. INDEX: Store in RAG database

Usage:
    python scripts/memory_ingest.py scan --path .
    python scripts/memory_ingest.py ingest --path . --max-files 100
    python scripts/memory_ingest.py status
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict

# Import RAG server
import sys
sys.path.insert(0, str(Path(__file__).parent))
from rag_server import RAGServer


class MemoryIngestionPipeline:
    """
    Memory ingestion for agent context augmentation.
    
    Supports:
    - Markdown documentation
    - Python code files
    - Configuration files
    - Agent/skill definitions
    """
    
    # File patterns to include
    INCLUDE_PATTERNS = [
        "*.md",
        "*.py", 
        "*.txt",
        "*.yaml",
        "*.yml",
        "*.json",
    ]
    
    # Directories to exclude
    EXCLUDE_DIRS = [
        "node_modules",
        "__pycache__",
        ".git",
        "venv",
        ".venv",
        "dist",
        "build",
        ".next",
        "docs/amalgam",  # Already processed
    ]
    
    def __init__(self):
        self.rag = RAGServer()
    
    def scan(self, path: Path, max_files: int = 1000) -> List[Dict]:
        """Scan for files to ingest."""
        files = []
        count = 0
        
        for pattern in self.INCLUDE_PATTERNS:
            for file_path in path.rglob(pattern):
                # Skip excluded directories
                if any(excl in str(file_path) for excl in self.EXCLUDE_DIRS):
                    continue
                
                if count >= max_files:
                    break
                
                try:
                    stat = file_path.stat()
                    files.append({
                        "path": str(file_path),
                        "size": stat.st_size,
                        "type": file_path.suffix
                    })
                    count += 1
                except Exception:
                    continue
        
        return files
    
    def ingest(self, path: Path, max_files: int = 1000) -> Dict:
        """Ingest files into RAG."""
        files = self.scan(path, max_files)
        
        total_chunks = 0
        processed = 0
        errors = []
        
        for file_info in files:
            try:
                file_path = Path(file_info["path"])
                
                # Add file type as metadata
                metadata = {
                    "type": file_info["type"],
                    "size": file_info["size"]
                }
                
                chunks = self.rag.ingest(file_path, metadata)
                total_chunks += chunks
                processed += 1
                
            except Exception as e:
                errors.append({
                    "file": file_info["path"],
                    "error": str(e)
                })
        
        return {
            "files_scanned": len(files),
            "files_processed": processed,
            "chunks_created": total_chunks,
            "errors": len(errors)
        }
    
    def status(self) -> Dict:
        """Get ingestion status."""
        rag_stats = self.rag.get_stats()
        
        return {
            "rag": rag_stats,
            "pipeline": "ready"
        }
    
    def clear(self):
        """Clear all ingested data."""
        self.rag.clear()


def main():
    parser = argparse.ArgumentParser(
        description='Memory Ingestion Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan for files')
    scan_parser.add_argument('--path', '-p', default='.', help='Path to scan')
    scan_parser.add_argument('--max-files', '-m', type=int, default=100, help='Max files')
    scan_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest files')
    ingest_parser.add_argument('--path', '-p', default='.', help='Path to ingest')
    ingest_parser.add_argument('--max-files', '-m', type=int, default=100, help='Max files')
    ingest_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Pipeline status')
    status_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all data')
    
    args = parser.parse_args()
    pipeline = MemoryIngestionPipeline()
    
    if args.command == 'scan':
        path = Path(args.path)
        files = pipeline.scan(path, args.max_files)
        
        if args.json:
            print(json.dumps({"files": files, "count": len(files)}, indent=2))
        else:
            print(f"📂 Scanned {len(files)} files in {path}")
            by_type = {}
            for f in files:
                t = f['type']
                by_type[t] = by_type.get(t, 0) + 1
            for t, count in sorted(by_type.items()):
                print(f"  {t}: {count}")
    
    elif args.command == 'ingest':
        path = Path(args.path)
        print(f"📥 Ingesting from {path}...")
        result = pipeline.ingest(path, args.max_files)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"✅ Ingestion complete:")
            print(f"   📄 Files processed: {result['files_processed']}/{result['files_scanned']}")
            print(f"   📦 Chunks created: {result['chunks_created']}")
            if result['errors']:
                print(f"   ⚠️ Errors: {result['errors']}")
    
    elif args.command == 'status':
        status = pipeline.status()
        
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print("📊 Memory Pipeline Status:")
            print(f"   💾 Chunks indexed: {status['rag']['total_chunks']}")
            print(f"   📁 Sources: {status['rag']['total_sources']}")
            print(f"   🔧 Pipeline: {status['pipeline']}")
    
    elif args.command == 'clear':
        pipeline.clear()
        print("🗑️ Cleared all ingested data")


if __name__ == "__main__":
    main()
