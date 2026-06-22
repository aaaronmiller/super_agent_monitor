#!/usr/bin/env python3
"""
Find Files Tool

Searches for files by pattern with optional filters.

Usage:
    uv run scripts/tools/find_files.py --pattern "*.py" --directory "/path" --json
    uv run scripts/tools/find_files.py --help
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, List
import fnmatch


def find_files(
    pattern: str,
    directory: str = ".",
    max_depth: Optional[int] = None,
    file_type: str = "all",
    exclude: Optional[List[str]] = None
) -> dict:
    """Find files matching pattern and return structured results."""
    try:
        root_path = Path(directory).resolve()
        if not root_path.exists():
            return {
                "success": False,
                "data": None,
                "error": f"Directory not found: {directory}"
            }
        
        exclude = exclude or []
        results = []
        
        def should_exclude(path: Path) -> bool:
            for exc in exclude:
                if fnmatch.fnmatch(path.name, exc) or fnmatch.fnmatch(str(path), f"*{exc}*"):
                    return True
            return False
        
        def scan_dir(current_path: Path, depth: int = 0):
            if max_depth is not None and depth > max_depth:
                return
            
            try:
                for item in current_path.iterdir():
                    if should_exclude(item):
                        continue
                    
                    if fnmatch.fnmatch(item.name, pattern):
                        if file_type == "all":
                            results.append(item)
                        elif file_type == "file" and item.is_file():
                            results.append(item)
                        elif file_type == "dir" and item.is_dir():
                            results.append(item)
                    
                    if item.is_dir() and not item.is_symlink():
                        scan_dir(item, depth + 1)
            except PermissionError:
                pass
        
        scan_dir(root_path)
        
        # Format results
        items = []
        for path in sorted(results)[:100]:  # Limit to 100 results
            stat = path.stat()
            items.append({
                "path": str(path),
                "name": path.name,
                "type": "directory" if path.is_dir() else "file",
                "size": stat.st_size if path.is_file() else None,
                "modified": stat.st_mtime
            })
        
        return {
            "success": True,
            "data": {
                "pattern": pattern,
                "directory": str(root_path),
                "total_found": len(results),
                "returned_count": len(items),
                "items": items
            },
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Find files by pattern',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--pattern', '-p', required=True, help='Glob pattern (e.g., "*.py")')
    parser.add_argument('--directory', '-d', default='.', help='Directory to search')
    parser.add_argument('--max-depth', type=int, default=None, help='Maximum directory depth')
    parser.add_argument('--type', '-t', default='all', choices=['all', 'file', 'dir'],
                        help='Filter by type')
    parser.add_argument('--exclude', '-e', action='append', default=None,
                        help='Patterns to exclude')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = find_files(
        args.pattern,
        args.directory,
        args.max_depth,
        args.type,
        args.exclude
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"Found {result['data']['total_found']} files matching: {args.pattern}")
            print("-" * 40)
            for item in result['data']['items'][:20]:
                size = f"{item['size']:>8} bytes" if item['size'] else "       <dir>"
                print(f"{size} | {item['path']}")
        else:
            print(f"Error: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
