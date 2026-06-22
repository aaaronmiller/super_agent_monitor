#!/usr/bin/env python3
"""
Filesystem MCP Alternative - Script-based file operations
Progressive disclosure alternative to @modelcontextprotocol/server-filesystem
"""

import argparse
import os
import json
import sys
from pathlib import Path

def list_directory(path: str, recursive: bool = False, pattern: str = "*") -> dict:
    """List directory contents"""
    target = Path(path)
    
    if not target.exists():
        return {"error": f"Path does not exist: {path}"}
    
    if not target.is_dir():
        return {"error": f"Not a directory: {path}"}
    
    if recursive:
        files = list(target.rglob(pattern))
    else:
        files = list(target.glob(pattern))
    
    return {
        "path": str(target.absolute()),
        "count": len(files),
        "files": [str(f.relative_to(target)) for f in files if f.is_file()],
        "directories": [str(d.relative_to(target)) for d in files if d.is_dir()]
    }

def read_file(path: str, lines: int = None, offset: int = 0) -> dict:
    """Read file contents"""
    target = Path(path)
    
    if not target.exists():
        return {"error": f"File does not exist: {path}"}
    
    if not target.is_file():
        return {"error": f"Not a file: {path}"}
    
    try:
        with open(target, 'r') as f:
            if lines:
                all_lines = f.readlines()
                content_lines = all_lines[offset:offset+lines]
                content = ''.join(content_lines)
            else:
                content = f.read()
        
        return {
            "path": str(target.absolute()),
            "size": target.stat().st_size,
            "lines": len(content.splitlines()),
            "content": content
        }
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}

def write_file(path: str, content: str, mode: str = "write") -> dict:
    """Write file contents"""
    target = Path(path)
    
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        
        if mode == "append":
            with open(target, 'a') as f:
                f.write(content)
        else:
            with open(target, 'w') as f:
                f.write(content)
        
        return {
            "path": str(target.absolute()),
            "size": target.stat().st_size,
            "mode": mode,
            "success": True
        }
    except Exception as e:
        return {"error": f"Failed to write file: {e}"}

def search_files(path: str, pattern: str, content: str = None) -> dict:
    """Search for files by name or content"""
    target = Path(path)
    
    if not target.exists():
        return {"error": f"Path does not exist: {path}"}
    
    matches = []
    
    for file in target.rglob(pattern):
        if file.is_file():
            match_info = {"path": str(file.relative_to(target))}
            
            if content:
                try:
                    with open(file, 'r') as f:
                        file_content = f.read()
                        if content in file_content:
                            match_info["matched"] = True
                            matches.append(match_info)
                except:
                    pass
            else:
                matches.append(match_info)
    
    return {
        "search_path": str(target.absolute()),
        "pattern": pattern,
        "content_filter": content,
        "matches": len(matches),
        "files": matches
    }

def main():
    parser = argparse.ArgumentParser(description="Filesystem operations (MCP alternative)")
    parser.add_argument("command", choices=["list", "read", "write", "search"])
    parser.add_argument("path", help="File or directory path")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recursive operation")
    parser.add_argument("--pattern", default="*", help="File pattern")
    parser.add_argument("--content", help="Content to write or search")
    parser.add_argument("--lines", type=int, help="Number of lines to read")
    parser.add_argument("--offset", type=int, default=0, help="Line offset for reading")
    parser.add_argument("--mode", choices=["write", "append"], default="write")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    result = None
    
    if args.command == "list":
        result = list_directory(args.path, args.recursive, args.pattern)
    elif args.command == "read":
        result = read_file(args.path, args.lines, args.offset)
    elif args.command == "write":
        if not args.content:
            print("Error: --content required for write command", file=sys.stderr)
            sys.exit(1)
        result = write_file(args.path, args.content, args.mode)
    elif args.command == "search":
        result = search_files(args.path, args.pattern, args.content)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
