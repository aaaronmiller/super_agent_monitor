# Hook: session-end
## Purpose
Finalize run, summarize results, and cleanup resources.

## Trigger
When delobotomize-orchestrator completes or encounters fatal error.

## Cleanup Tasks
1. **Generate Final Report**
   - Compile all phase results
   - Calculate overall metrics
   - Document applied changes
   - List remaining issues

2. **Close Session**
   - Record end time
   - Calculate total duration
   - Write final session data
   - Mark session as complete

3. **Archive Artifacts**
   - Move logs to archive
   - Compress large outputs
   - Generate summary document

4. **Notify Completion**
   - Log session-end event via agentic-log-event
   - Update monitor dashboard
   - Send notifications (if configured)

## Final Report Template
```json
{
  "session_id": "delobo_20251107_abc123",
  "end_time": "2025-11-07T00:00:00Z",
  "duration_ms": 123456,
  "status": "success|error|partial",
  "summary": {
    "phases_completed": 5,
    "files_scanned": 150,
    "issues_found": 23,
    "changes_applied": 5,
    "health_score_before": 0.75,
    "health_score_after": 0.82
  },
  "artifacts": {
    "report_path": "path/to/report",
    "changesets": ["list of change files"],
    "iterations": ["list of proposals"]
  }
}
```

## Error Handling
- If report generation fails, log basic summary
- Always mark session as ended
- Never leave dangling sessions

## Retention
- Keep final reports indefinitely
- Archive after 90 days
- Compress old archives
