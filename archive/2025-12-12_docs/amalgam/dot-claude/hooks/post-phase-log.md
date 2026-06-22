# Hook: post-phase-log
## Purpose
Record phase completion and metrics after each major workflow phase.

## Trigger
After each major phase completes:
- scan-project
- triage-findings
- remediation-apply
- verify-health
- iterate-lessons

## Data Collected
```json
{
  "session_id": "unique run identifier",
  "phase": "scan|triage|remediate|verify|iterate",
  "status": "success|error|partial",
  "timestamp": "ISO timestamp",
  "duration_ms": 1234,
  "metrics": {
    "files_scanned": 150,
    "issues_found": 23,
    "changes_applied": 5,
    "health_score_before": 0.75,
    "health_score_after": 0.82
  },
  "artifacts": {
    "output_path": "path to results",
    "log_path": "path to logs"
  }
}
```

## Actions
1. Write JSON entry to `.delobotomize/runs/<timestamp>.json`
2. Optionally call agentic-log-event with phase completion
3. Update run dashboard (if enabled)

## Error Handling
- If logging fails, continue execution
- Log errors to console
- Never block main workflow

## Retention
- Keep last 100 run logs
- Archive older logs to `.delobotomize/archives/`
