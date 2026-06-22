#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
# ]
# ///

"""
Fetch URL Tool

Fetches web page content and returns structured data.

Usage:
    uv run scripts/tools/fetch_url.py --url "https://example.com" --json
    uv run scripts/tools/fetch_url.py --help
"""

import argparse
import json
import sys
from typing import Optional


def fetch_url(
    url: str,
    timeout: int = 30,
    headers: Optional[dict] = None
) -> dict:
    """Fetch URL and return structured content."""
    import requests
    from bs4 import BeautifulSoup
    
    try:
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AgentTool/1.0)'
        }
        if headers:
            default_headers.update(headers)
        
        response = requests.get(url, timeout=timeout, headers=default_headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else None
        
        # Extract main text content
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator='\n', strip=True)
        
        # Limit text length
        if len(text) > 10000:
            text = text[:10000] + "...[truncated]"
        
        return {
            "success": True,
            "data": {
                "url": url,
                "title": title,
                "content_length": len(response.text),
                "text_length": len(text),
                "status_code": response.status_code,
                "text": text
            },
            "error": None
        }
        
    except requests.RequestException as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Fetch URL content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--url', '-u', required=True, help='URL to fetch')
    parser.add_argument('--timeout', '-t', type=int, default=30, help='Request timeout in seconds')
    parser.add_argument('--headers', type=str, default=None, help='JSON headers dict')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    headers = None
    if args.headers:
        headers = json.loads(args.headers)
    
    result = fetch_url(args.url, args.timeout, headers)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"Title: {result['data']['title']}")
            print(f"Length: {result['data']['content_length']} bytes")
            print("-" * 40)
            print(result['data']['text'][:500])
        else:
            print(f"Error: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
