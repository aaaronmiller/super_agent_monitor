#!/usr/bin/env python3
"""Complexity Analysis Script"""
import sys, ast, json
from pathlib import Path

def analyze_complexity(file_path):
    """Calculate cyclomatic complexity"""
    with open(file_path) as f:
        tree = ast.parse(f.read())
    
    complexity = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            decisions = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler)))
            complexity[node.name] = decisions + 1
    
    return complexity

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze-complexity.py <file>")
        sys.exit(1)
    result = analyze_complexity(sys.argv[1])
    print(json.dumps(result, indent=2))
