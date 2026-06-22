#!/usr/bin/env python3
"""Brave Search MCP Alternative - Web search"""
import argparse, json, urllib.request, os

def search(query: str, api_key: str = None) -> dict:
    api_key = api_key or os.getenv('BRAVE_API_KEY')
    if not api_key:
        return {"error": "BRAVE_API_KEY not set"}
    
    url = f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url)
    req.add_header('X-Subscription-Token', api_key)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Brave Search (MCP alternative)")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--api-key", help="Brave API key")
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()
    result = search(args.query, args.api_key)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
