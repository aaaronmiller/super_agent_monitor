# Skill: agentic-log-event
## Purpose
Send lifecycle events to the agentic-delobotomize backend/UI if enabled.

## Implementation
- POST to local agentic server (if running) with:
  - session_id, phase, status, metrics
- Never required for correctness; best-effort only

## Input
- `event_type` (phase_start|phase_end|error|success)
- `session_id` (unique run identifier)
- `phase` (scan|triage|remediate|verify|iterate)
- `data` (structured event data)

## Output
- API response (if server available)
- Local fallback log
- Success/failure status

## Safety
- Best-effort only
- Never blocks main workflow
- Graceful degradation if server unavailable
