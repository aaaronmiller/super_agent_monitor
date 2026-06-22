#!/usr/bin/env python3
import requests
import sys

def query_prometheus(query, prometheus_url="http://prometheus:9090"):
    response = requests.get(
        f"{prometheus_url}/api/v1/query",
        params={'query': query}
    )
    result = response.json()
    if result['status'] == 'success':
        print(result['data']['result'])
    else:
        print(f"Error: {result}", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: metrics-query.py <promql_query>")
        sys.exit(1)
    query_prometheus(sys.argv[1])
