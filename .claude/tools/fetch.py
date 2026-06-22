#!/usr/bin/env python3
"""Fetch MCP Alternative - HTTP requests"""
import argparse, json, urllib.request, urllib.error

def fetch(url: str, method: str = "GET", headers: dict = None, data: str = None) -> dict:
    try:
        req = urllib.request.Request(url, method=method)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        if data:
            req.data = data.encode()
        
        with urllib.request.urlopen(req) as response:
            return {
                "status": response.status,
                "headers": dict(response.headers),
                "body": response.read().decode()
            }
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}

def main():
    parser = argparse.ArgumentParser(description="HTTP fetch (MCP alternative)")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--method", default="GET", choices=["GET", "POST", "PUT", "DELETE"])
    parser.add_argument("--headers", help="JSON headers")
    parser.add_argument("--data", help="Request body")
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()
    headers = json.loads(args.headers) if args.headers else None
    result = fetch(args.url, args.method, headers, args.data)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
