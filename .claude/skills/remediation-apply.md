# Skill: remediation-apply
## Purpose
Apply safe, atomic fixes using existing remediation orchestrator.

## Implementation
- Only run when pre-remediation-apply hook approves
- Use:
  - `node dist/cli/delobotomize.js remediate --plan <path> --dry-run`
  - If validated, run without `--dry-run`
- Log all edits to `.delobotomize/changesets/*.json`

## Input
- `remediation_plan` (path or JSON)
- `apply_options` (optional)
- `dry_run` (default: true)

## Output
- List of applied changes
- Audit log of modifications
- Verification of changes

## Safety
- Governed by pre-remediation-apply hook
- Only edits within configured whitelist
- All changes logged for audit
