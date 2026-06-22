#!/usr/bin/env python3
"""GitHub MCP Alternative - Script-based GitHub operations"""
import argparse, json, subprocess, sys

def run_gh(cmd: list) -> dict:
    try:
        result = subprocess.run(['gh'] + cmd, capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr}

def main():
    parser = argparse.ArgumentParser(description="GitHub operations (MCP alternative)")
    parser.add_argument("command", choices=["repo", "pr", "issue", "search"])
    parser.add_argument("action", help="Action to perform")
    parser.add_argument("--args", nargs="*", help="Additional arguments")
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()
    cmd = [args.command, args.action] + (args.args or [])
    result = run_gh(cmd)
    
    print(json.dumps(result, indent=2) if args.json else result.get("output", result.get("error")))

if __name__ == "__main__":
    main()
