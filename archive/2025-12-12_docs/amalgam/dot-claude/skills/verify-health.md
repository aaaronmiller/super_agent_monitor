# Skill: verify-health
## Purpose
Re-run the scanner and confirm improvement.

## Implementation
- Run scan-project skill again
- Compare metrics vs previous run
- Emit a short verification report

## Input
- `previous_scan` (optional, for comparison)
- `current_project_path`
- `verification_options` (optional)

## Output
- Health score comparison
- List of resolved issues
- Remaining issues
- Verification report

## Safety
- Read-only operation
- No file modifications
