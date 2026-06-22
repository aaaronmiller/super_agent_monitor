#!/usr/bin/env python3
"""AST parsing utilities for source code analysis"""

import ast
import json
import sys

def parse_python_file(filepath):
    """Parse Python file and extract structure"""
    with open(filepath, 'r') as f:
        source_code = f.read()

    tree = ast.parse(source_code, filepath)

    analysis = {
        'file': filepath,
        'imports': [],
        'functions': [],
        'classes': [],
        'globals': []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                analysis['imports'].append({
                    'module': alias.name,
                    'alias': alias.asname
                })
        elif isinstance(node, ast.ImportFrom):
            analysis['imports'].append({
                'module': node.module,
                'names': [alias.name for alias in node.names]
            })
        elif isinstance(node, ast.FunctionDef):
            analysis['functions'].append({
                'name': node.name,
                'args': [arg.arg for arg in node.args.args],
                'lineno': node.lineno,
                'async': isinstance(node, ast.AsyncFunctionDef),
                'decorators': [get_decorator_name(d) for d in node.decorator_list]
            })
        elif isinstance(node, ast.ClassDef):
            methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
            analysis['classes'].append({
                'name': node.name,
                'bases': [get_base_name(base) for base in node.bases],
                'methods': methods,
                'lineno': node.lineno
            })

    return analysis

def get_decorator_name(node):
    """Extract decorator name"""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return node.attr
    return str(node)

def get_base_name(node):
    """Extract base class name"""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return node.attr
    return str(node)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ast-parser.py <python_file>")
        sys.exit(1)

    result = parse_python_file(sys.argv[1])
    print(json.dumps(result, indent=2))
