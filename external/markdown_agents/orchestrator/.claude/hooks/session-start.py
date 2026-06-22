#!/usr/bin/env python3
"""
Session Start Hook - Markdown Agent Auditor

Initializes the workspace for markdown analysis by creating necessary
directories and files at the start of each session.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path


def initialize_workspace():
    """Initialize output directory and files for analysis session."""

    # Get project root (3 levels up from hooks/)
    project_root = Path(__file__).parent.parent.parent.parent
    output_dir = project_root / "output"
    target_dir = project_root / "target"

    print(f"[Session Start] Initializing Markdown Agent Auditor")
    print(f"[Session Start] Project Root: {project_root}")
    print(f"[Session Start] Output Directory: {output_dir}")
    print(f"[Session Start] Target Directory: {target_dir}")

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[Session Start] ✓ Output directory ready")

    # Create target directory if it doesn't exist
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"[Session Start] ✓ Target directory created (empty)")
    else:
        # Count markdown files in target
        md_files = list(target_dir.rglob("*.md"))
        print(f"[Session Start] ✓ Target directory exists ({len(md_files)} markdown files found)")

    # Initialize scratchpad.md
    scratchpad_path = output_dir / "scratchpad.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    scratchpad_content = f"""# Markdown Audit Scratchpad
**Scan Date**: {timestamp}
**Target Directory**: {target_dir}
**Status**: Initializing

---

## Session Log

{timestamp} - Session started
{timestamp} - Workspace initialized

---

## Phase 1: File Discovery

*Waiting for orchestrator to begin file discovery...*

---

## Phase 2: File Analysis

*Files will be analyzed and documented here...*

---

## Phase 3: Project Association

*Project associations will be documented here...*

---

## Phase 4: PRD Ratings

*PRD quality ratings will be documented here...*

---

## Phase 5: GitHub Comparisons

*GitHub comparison analysis will be documented here...*

---

## Summary

*Session summary will be added upon completion...*
"""

    with open(scratchpad_path, 'w', encoding='utf-8') as f:
        f.write(scratchpad_content)
    print(f"[Session Start] ✓ Scratchpad initialized: {scratchpad_path}")

    # Initialize projects.json
    projects_path = output_dir / "projects.json"

    projects_data = {
        "scan_date": timestamp,
        "target_directory": str(target_dir),
        "status": "in_progress",
        "projects": []
    }

    with open(projects_path, 'w', encoding='utf-8') as f:
        json.dump(projects_data, f, indent=2)
    print(f"[Session Start] ✓ Project registry initialized: {projects_path}")

    # Create session log
    log_path = output_dir / "session.log"
    log_content = f"{timestamp} - Session initialized successfully\n"

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
    print(f"[Session Start] ✓ Session log created: {log_path}")

    print(f"[Session Start] ✓ Workspace initialization complete!")
    print(f"[Session Start] Ready for markdown analysis.")

    return 0


def main():
    """Main entry point for session start hook."""
    try:
        exit_code = initialize_workspace()
        sys.exit(exit_code)
    except Exception as e:
        print(f"[Session Start] ERROR: Failed to initialize workspace", file=sys.stderr)
        print(f"[Session Start] ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
