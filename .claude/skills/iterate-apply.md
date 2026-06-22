# Skill: iterate-apply
## Purpose
Apply accepted iteration proposals in a controlled manner.

## Implementation
- Only with explicit human approval or upstream hook approval
- Apply:
  - Updates to `.delobotomize/rules/*.json`
  - Prompt evolution configs where wired
- Log changes for audit

## Input
- `accepted_proposals` (from iterate-lessons)
- `apply_scope` (specific proposals to apply)
- `approval_context` (required)

## Output
- List of applied iterations
- Audit log
- Updated rule files

## Safety
- Requires explicit approval
- Governed by hooks
- Full audit trail
- Rollback plan required
