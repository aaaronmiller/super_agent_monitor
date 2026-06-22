# Hook: pre-remediation-apply
## Purpose
Validate and approve remediation operations before execution.

## Trigger
Before remediation-apply skill runs or remediation-specialist agent makes changes.

## Validation Rules
1. **Scope Validation**
   - Only allow edits within configured whitelist
   - Reject operations outside allowed directories
   - Verify file patterns match expected targets

2. **Plan Validation**
   - Require explicit plan summary in prompt
   - Verify proposed changes are well-scoped
   - Check for overlapping edits

3. **Risk Assessment**
   - If plan is missing → reject
   - If diff is too broad → request refinement
   - If high-risk changes without approval → reject

4. **Safety Checks**
   - Verify --dry-run completed successfully
   - Check backup/rollback strategy exists
   - Confirm no destructive operations

## Approval Process
- **Auto-approve**: Low-risk changes (docs, comments, whitespace)
- **Require approval**: Medium/high-risk changes
- **Always require approval**: Logic changes, API modifications

## Response Format
```json
{
  "approved": true|false,
  "reason": "explanation",
  "conditions": ["specific constraints"],
  "required_changes": ["items needing approval"],
  "audit_id": "unique validation id"
}
```

## Audit
Log all decisions to `.delobotomize/audit/hook-decisions.json`
