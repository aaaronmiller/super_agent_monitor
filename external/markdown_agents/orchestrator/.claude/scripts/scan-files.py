#!/usr/bin/env python3
"""
Scan Files Script - Markdown Agent Auditor

Scans target directory for markdown files and prioritizes PRD files.
Returns a sorted list for analysis.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def is_prd_file(file_path):
    """
    Determine if a file is likely a PRD based on filename and content.

    Returns: tuple (is_prd, match_reason)
    """
    filename = file_path.name.lower()

    # Check filename
    if 'prd' in filename or 'product-requirements' in filename:
        return True, "filename"

    # Check content (first 1000 chars)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1000).lower()

            # Look for PRD indicators
            prd_indicators = [
                'product requirements',
                'product requirement',
                'requirements document',
                'prd:',
                'product spec',
                'product specification'
            ]

            for indicator in prd_indicators:
                if indicator in content:
                    return True, "content"

    except Exception:
        # If we can't read the file, skip content check
        pass

    return False, None


def scan_directory(target_dir):
    """
    Scan target directory recursively for markdown files.

    Returns: dict with priority and standard file lists
    """
    target_path = Path(target_dir)

    if not target_path.exists():
        print(f"ERROR: Target directory does not exist: {target_dir}", file=sys.stderr)
        return None

    if not target_path.is_dir():
        print(f"ERROR: Target path is not a directory: {target_dir}", file=sys.stderr)
        return None

    # Find all markdown files
    md_files = list(target_path.rglob("*.md"))

    priority_files = []
    standard_files = []

    for md_file in md_files:
        # Skip files in output directory
        if 'output' in md_file.parts:
            continue

        is_prd, match_reason = is_prd_file(md_file)

        file_info = {
            "path": str(md_file.relative_to(target_path.parent)),
            "size": md_file.stat().st_size,
            "modified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
        }

        if is_prd:
            file_info["match_reason"] = match_reason
            priority_files.append(file_info)
        else:
            standard_files.append(file_info)

    # Sort both lists alphabetically by path
    priority_files.sort(key=lambda x: x["path"])
    standard_files.sort(key=lambda x: x["path"])

    return {
        "total_files": len(md_files),
        "priority_files": priority_files,
        "standard_files": standard_files,
        "scan_date": datetime.now().isoformat(),
        "target_directory": str(target_path)
    }


def format_results(scan_results):
    """Format scan results as markdown."""

    if not scan_results:
        return "# Error: No scan results available"

    timestamp = datetime.fromisoformat(scan_results["scan_date"]).strftime("%Y-%m-%d %H:%M:%S")

    output = f"""# File Discovery Results
**Scan Date**: {timestamp}
**Target Directory**: {scan_results['target_directory']}
**Total Files Found**: {scan_results['total_files']}
**Priority PRD Files**: {len(scan_results['priority_files'])}
**Standard Files**: {len(scan_results['standard_files'])}

"""

    # Priority files section
    if scan_results['priority_files']:
        output += "## Priority Files (Likely PRDs)\n\n"
        for i, file_info in enumerate(scan_results['priority_files'], 1):
            match_reason = file_info.get('match_reason', 'unknown')
            output += f"{i}. {file_info['path']} (matched: {match_reason})\n"
        output += "\n"
    else:
        output += "## Priority Files (Likely PRDs)\n\nNo PRD files detected.\n\n"

    # Standard files section
    if scan_results['standard_files']:
        output += "## Standard Files\n\n"
        for i, file_info in enumerate(scan_results['standard_files'], 1):
            output += f"{i}. {file_info['path']}\n"
        output += "\n"
    else:
        output += "## Standard Files\n\nNo additional markdown files found.\n\n"

    return output


def main():
    """Main entry point."""
    # Get target directory from args or use default
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        project_root = get_project_root()
        target_dir = project_root / "target"

    print(f"Scanning directory: {target_dir}")

    # Scan directory
    scan_results = scan_directory(target_dir)

    if not scan_results:
        return 1

    # Format as markdown
    markdown_output = format_results(scan_results)

    # Print to stdout
    print("\n" + markdown_output)

    # Also save as JSON for programmatic access
    project_root = get_project_root()
    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "file-discovery.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(scan_results, f, indent=2)

    print(f"\nJSON results saved to: {json_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
