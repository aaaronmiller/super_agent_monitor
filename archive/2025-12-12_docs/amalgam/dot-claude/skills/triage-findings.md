# Skill: triage-findings
## Purpose
Convert scan results into a concrete remediation plan using existing triage logic.

## Implementation
- Input: scan-results JSON (from scan-project skill)
- Run: `node dist/cli/delobotomize.js phase-triage --from scan --format json`
  or TypeScript equivalent in dev mode
- Output: structured list of issues and suggested actions

## Input
- `scan_results` (JSON from scan-project)
- `triage_options` (optional)

## Output
- Remediation plan with categorized issues
- Suggested fix strategies per issue
- Priority levels

## Safety
- Read-only operation on project files
- Generates only plans, no modifications
