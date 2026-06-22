---
description: Diagnose and repair broken/stalled project
argument-hint: $PROJECT_PATH
---

# Codebase Resuscitation

**Role:** Senior SRE / Forensic Analyst
**Task:** Diagnose and repair: $ARGUMENTS

## Execution

### Phase 1: Audit
- Deep Audit on user-created files
- Detect orphaned code, logic gaps
- Find "happy path" assumptions

### Phase 2: Triangulate
- Compare actual vs intended (PRD)
- Identify drift
- Map dependencies

### Phase 3: Recovery Plan
- Atomic, specific steps
- Prioritized by impact
- Rollback strategy

### Phase 4: Execute
- One critical fix at a time
- Adversarial Validation after each fix
- No regressions

## Common Root Causes
- Context collapse
- Architectural drift
- Missing dependencies
- Partial implementations
