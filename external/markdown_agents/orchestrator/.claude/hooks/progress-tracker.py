#!/usr/bin/env python3
"""
Progress Tracker Hook - Markdown Agent Auditor

Tracks progress through the analysis workflow by monitoring file states
and updating the session log. This hook can be called periodically to
report current status.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def read_projects_json():
    """Read the current projects.json file."""
    project_root = get_project_root()
    projects_path = project_root / "output" / "projects.json"

    if not projects_path.exists():
        return None

    with open(projects_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def count_markdown_files():
    """Count total markdown files in target directory."""
    project_root = get_project_root()
    target_dir = project_root / "target"

    if not target_dir.exists():
        return 0

    md_files = list(target_dir.rglob("*.md"))
    return len(md_files)


def analyze_progress():
    """Analyze current progress through the workflow."""

    projects_data = read_projects_json()

    if not projects_data:
        return {
            "phase": "Not Started",
            "status": "waiting",
            "progress": 0
        }

    projects = projects_data.get("projects", [])
    total_files = count_markdown_files()
    total_projects = len(projects)

    # Determine current phase based on project states
    if total_projects == 0:
        phase = "Phase 1: File Discovery"
        progress = 10
        status = "in_progress"
    else:
        # Check if all projects have ratings
        rated_count = sum(1 for p in projects if "rating" in p and p["rating"])
        compared_count = sum(1 for p in projects if "github_comparison" in p and p["github_comparison"])

        if compared_count == total_projects:
            phase = "Phase 6: Final Report Generation"
            progress = 95
            status = "finalizing"
        elif rated_count == total_projects:
            phase = "Phase 5: GitHub Comparison"
            progress = 70 + (compared_count / total_projects * 20)
            status = "in_progress"
        elif rated_count > 0:
            phase = "Phase 4: PRD Rating"
            progress = 50 + (rated_count / total_projects * 20)
            status = "in_progress"
        else:
            # Check if files have associations
            files_with_associations = sum(
                len(p.get("related_files", [])) for p in projects
            )
            if files_with_associations > total_projects:
                phase = "Phase 3: Project Association"
                progress = 40
                status = "in_progress"
            else:
                phase = "Phase 2: File Analysis"
                progress = 20 + (total_projects / max(total_files, 1) * 20)
                status = "in_progress"

    return {
        "phase": phase,
        "status": status,
        "progress": int(progress),
        "total_files": total_files,
        "total_projects": total_projects,
        "rated_projects": rated_count if total_projects > 0 else 0,
        "compared_projects": compared_count if total_projects > 0 else 0
    }


def log_progress(progress_data):
    """Log progress to session log."""
    project_root = get_project_root()
    log_path = project_root / "output" / "session.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = (
        f"{timestamp} - {progress_data['phase']} - "
        f"{progress_data['progress']}% complete - "
        f"Projects: {progress_data['total_projects']} - "
        f"Status: {progress_data['status']}\n"
    )

    # Append to log
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_line)


def display_progress_bar(progress, width=50):
    """Display a visual progress bar."""
    filled = int(width * progress / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {progress}%"


def main():
    """Main entry point for progress tracker hook."""
    try:
        progress_data = analyze_progress()

        print(f"\n{'='*60}")
        print(f"  Markdown Agent Auditor - Progress Report")
        print(f"{'='*60}")
        print(f"\n  Current Phase: {progress_data['phase']}")
        print(f"  Status: {progress_data['status'].upper()}")
        print(f"\n  {display_progress_bar(progress_data['progress'])}")
        print(f"\n  Files Found: {progress_data['total_files']}")
        print(f"  Projects Identified: {progress_data['total_projects']}")

        if progress_data['total_projects'] > 0:
            print(f"  PRDs Rated: {progress_data['rated_projects']}/{progress_data['total_projects']}")
            print(f"  GitHub Comparisons: {progress_data['compared_projects']}/{progress_data['total_projects']}")

        print(f"\n{'='*60}\n")

        # Log progress
        log_progress(progress_data)

        return 0

    except Exception as e:
        print(f"[Progress Tracker] ERROR: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
