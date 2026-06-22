# Hook: session-start
## Purpose
Initialize run metadata and prepare for Delobotomize execution.

## Trigger
At the beginning of delobotomize-orchestrator execution.

## Initialization Tasks
1. **Generate Session ID**
   - Create unique identifier: `delobo_<timestamp>_<random>`
   - Store in context for all subsequent operations

2. **Setup Logging**
   - Create session directory: `.delobotomize/runs/<session_id>/`
   - Initialize run log file
   - Set up audit trail

3. **Environment Validation**
   - Verify Node.js >= 18
   - Check TypeScript build (if needed)
   - Validate project structure

4. **Create Baseline**
   - Record git commit hash (if repo)
   - Capture initial file count
   - Note start time

## Session Metadata Template
```json
{
  "session_id": "delobo_20251107_abc123",
  "start_time": "2025-11-07T00:00:00Z",
  "project_path": "/path/to/project",
  "git_commit": "abc123def",
  "initial_state": {
    "file_count": 150,
    "branch": "main"
  },
  "config": {
    "auto_apply": false,
    "verify_enabled": true,
    "memory_enabled": true
  }
}
```

## Actions
- Write metadata to `.delobotomize/runs/<session_id>/session.json`
- Log session-start event via agentic-log-event
- Notify monitor agent

## Error Handling
- If session creation fails, attempt cleanup
- Log error and exit gracefully
- Never proceed without valid session
