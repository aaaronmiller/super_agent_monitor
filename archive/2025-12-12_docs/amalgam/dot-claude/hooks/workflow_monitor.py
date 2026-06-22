#!/usr/bin/env python3
# ---
# name: workflow-monitor
# description: Monitors document organization and publication workflow. Triggers next steps automatically.
# ---

import sys, json, os
from pathlib import Path
from datetime import datetime

def check_workflow_status():
    """Check current status of document workflow"""
    status = {
        'timestamp': datetime.now().isoformat(),
        'stages': {
            'documents_scanned': False,
            'organized_by_topic': False,
            'series_identified': False,
            'authoritative_versions_created': False,
            'publication_candidates': False,
            'assessed_for_publication': False,
            'ready_for_submission': False,
            'submitted': False,
            'promoted': False
        },
        'next_actions': []
    }

    # Check if documents are organized
    if Path('documents/index.json').exists():
        status['stages']['documents_scanned'] = True

    if Path('documents/by_topic').exists() or Path('documents/by_date').exists():
        status['stages']['organized_by_topic'] = True

    if Path('documents/series').exists():
        status['stages']['series_identified'] = True
        # Check for authoritative versions
        authoritative_count = len(list(Path('documents/series').glob('*_authoritative.md')))
        if authoritative_count > 0:
            status['stages']['authoritative_versions_created'] = True

    # Check for publication candidates
    if Path('documents/series').exists():
        authoritative_files = list(Path('documents/series').glob('*_authoritative.md'))
        for auth_file in authoritative_files:
            # Check if this has been assessed
            auth_id = auth_file.stem.replace('_authoritative', '')
            assessment_file = Path(f'publications/assessment_{auth_id}.md')
            if assessment_file.exists():
                status['stages']['publication_candidates'] = True
                status['stages']['assessed_for_publication'] = True

    # Check publication queue
    if Path('publications/publication_queue.json').exists():
        with open('publications/publication_queue.json') as f:
            queue = json.load(f)

        for candidate in queue.get('candidates', []):
            if candidate.get('grade') in ['A', 'B']:
                status['stages']['ready_for_submission'] = True
                break

    # Check submissions
    if Path('publications/submissions.json').exists():
        with open('publications/submissions.json') as f:
            submissions = json.load(f)

        for sub in submissions.get('submissions', []):
            if sub.get('status') == 'accepted':
                status['stages']['submitted'] = True
                status['stages']['promoted'] = True
                break

    # Determine next actions
    if not status['stages']['documents_scanned']:
        status['next_actions'].append("Run document-organizer agent to scan and organize documents")
    elif not status['stages']['authoritative_versions_created']:
        status['next_actions'].append("Continue document organization to create authoritative versions")
    elif not status['stages']['assessed_for_publication']:
        status['next_actions'].append("Run publication-assessor agent to evaluate authoritative versions")
    elif status['stages']['ready_for_submission']:
        status['next_actions'].append("Run daily-submission agent to submit high-grade articles")
    elif status['stages']['submitted']:
        status['next_actions'].append("Run promotion-agent to promote published articles")

    return status

def main():
    try:
        status = check_workflow_status()

        # Print status summary
        print("# Document Workflow Status", file=sys.stderr)
        print(f"Generated: {status['timestamp']}", file=sys.stderr)
        print("\nCompleted Stages:", file=sys.stderr)

        for stage, completed in status['stages'].items():
            status_str = "✓" if completed else "○"
            print(f"  {status_str} {stage.replace('_', ' ').title()}", file=sys.stderr)

        if status['next_actions']:
            print("\nNext Actions:", file=sys.stderr)
            for i, action in enumerate(status['next_actions'], 1):
                print(f"  {i}. {action}", file=sys.stderr)
        else:
            print("\n✓ Workflow complete! All stages finished.", file=sys.stderr)

        # Write status to file
        status_file = Path('.claude/memory/workflow_status.json')
        status_file.parent.mkdir(exist_ok=True)
        with open(status_file, 'w') as f:
            json.dump(status, f, indent=2)

        # Output as JSON for integration
        print(json.dumps(status, indent=2))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
