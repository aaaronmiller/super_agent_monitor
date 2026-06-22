# Skill: remediation-plan
## Purpose
Summarize and prioritize the remediation plan for operator review.

## Implementation
- Input: triage plan JSON (from triage-findings)
- Produce:
  - Top critical issues summary
  - File-level actions
  - Explicit "will-edit" vs "read-only" scope
- This skill only reasons; it does not write files

## Input
- `triage_results` (JSON from triage-findings)
- `review_options` (optional)

## Output
- Human-readable remediation summary
- Categorized action items
- Risk assessment for each action

## Safety
- Read-only operation
- No file modifications
