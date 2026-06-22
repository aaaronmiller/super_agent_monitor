#!/usr/bin/env python3
"""Memory MCP Alternative - Persistent state management"""
import argparse, json, os
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

def store(key: str, value: str) -> dict:
    file = MEMORY_DIR / f"{key}.json"
    with open(file, 'w') as f:
        json.dump({"key": key, "value": value}, f)
    return {"success": True, "key": key}

def retrieve(key: str) -> dict:
    file = MEMORY_DIR / f"{key}.json"
    if not file.exists():
        return {"error": f"Key not found: {key}"}
    with open(file) as f:
        return json.load(f)

def list_keys() -> dict:
    keys = [f.stem for f in MEMORY_DIR.glob("*.json")]
    return {"keys": keys, "count": len(keys)}

def main():
    parser = argparse.ArgumentParser(description="Memory operations (MCP alternative)")
    parser.add_argument("command", choices=["store", "retrieve", "list"])
    parser.add_argument("--key", help="Memory key")
    parser.add_argument("--value", help="Value to store")
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()
    
    if args.command == "store":
        result = store(args.key, args.value)
    elif args.command == "retrieve":
        result = retrieve(args.key)
    else:
        result = list_keys()
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
