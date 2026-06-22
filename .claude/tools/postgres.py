#!/usr/bin/env python3
"""PostgreSQL MCP Alternative - Database operations"""
import argparse, json, subprocess

def query(sql: str, db_url: str = None) -> dict:
    try:
        cmd = ['psql', db_url or 'postgres://localhost', '-c', sql, '-t', '-A']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr}

def main():
    parser = argparse.ArgumentParser(description="PostgreSQL operations (MCP alternative)")
    parser.add_argument("command", choices=["query", "list", "describe"])
    parser.add_argument("--sql", help="SQL query")
    parser.add_argument("--table", help="Table name")
    parser.add_argument("--db-url", help="Database URL")
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()
    
    if args.command == "query":
        result = query(args.sql, args.db_url)
    elif args.command == "list":
        result = query("\dt", args.db_url)
    elif args.command == "describe":
        result = query(f"\d {args.table}", args.db_url)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
