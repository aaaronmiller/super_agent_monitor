#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "requests",
# ]
# ///

"""
Search GitHub Tool

Searches GitHub repositories, code, and issues.

Usage:
    uv run scripts/tools/search_github.py --query "agent orchestration" --json
    uv run scripts/tools/search_github.py --help
"""

import argparse
import json
import os
import sys
from typing import Optional


def search_github(
    query: str,
    search_type: str = "repositories",
    language: Optional[str] = None,
    sort: str = "stars",
    num_results: int = 10
) -> dict:
    """Search GitHub and return structured results."""
    import requests
    
    try:
        # Build search query
        search_query = query
        if language:
            search_query += f" language:{language}"
        
        # GitHub API endpoint
        endpoints = {
            "repositories": "https://api.github.com/search/repositories",
            "repos": "https://api.github.com/search/repositories",
            "code": "https://api.github.com/search/code",
            "issues": "https://api.github.com/search/issues"
        }
        
        url = endpoints.get(search_type, endpoints["repositories"])
        
        # Headers (use token if available)
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AgentTool/1.0"
        }
        
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        params = {
            "q": search_query,
            "sort": sort,
            "order": "desc",
            "per_page": min(num_results, 100)
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Format results based on type
        if search_type in ["repositories", "repos"]:
            items = [{
                "name": item["full_name"],
                "description": item.get("description", ""),
                "stars": item["stargazers_count"],
                "language": item.get("language", ""),
                "url": item["html_url"],
                "updated": item["updated_at"]
            } for item in data.get("items", [])]
        elif search_type == "code":
            items = [{
                "name": item["name"],
                "path": item["path"],
                "repository": item["repository"]["full_name"],
                "url": item["html_url"]
            } for item in data.get("items", [])]
        else:  # issues
            items = [{
                "title": item["title"],
                "state": item["state"],
                "repository": item["repository_url"].split("/")[-2] + "/" + item["repository_url"].split("/")[-1],
                "url": item["html_url"],
                "created": item["created_at"]
            } for item in data.get("items", [])]
        
        return {
            "success": True,
            "data": {
                "query": query,
                "type": search_type,
                "total_count": data.get("total_count", 0),
                "returned_count": len(items),
                "items": items
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
        description='Search GitHub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--query', '-q', required=True, help='Search query')
    parser.add_argument('--type', '-t', default='repos', 
                        choices=['repos', 'repositories', 'code', 'issues'],
                        help='Search type')
    parser.add_argument('--language', '-l', default=None, help='Filter by language')
    parser.add_argument('--sort', '-s', default='stars', 
                        choices=['stars', 'forks', 'updated'],
                        help='Sort order')
    parser.add_argument('--num-results', '-n', type=int, default=10, help='Number of results')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = search_github(
        args.query, 
        args.type, 
        args.language, 
        args.sort, 
        args.num_results
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"Found {result['data']['total_count']} results for: {args.query}")
            print("-" * 40)
            for item in result['data']['items'][:5]:
                if 'stars' in item:
                    print(f"⭐ {item['stars']:>5} | {item['name']}")
                    print(f"         {item['description'][:60] if item['description'] else 'No description'}")
                else:
                    print(f"  {item.get('name', item.get('title', 'Unknown'))}")
                print()
        else:
            print(f"Error: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
