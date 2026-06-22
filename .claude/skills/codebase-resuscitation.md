---
name: codebase-resuscitation
description: Diagnose and repair broken/stalled projects
category: master-prompt
tags: [debugging, repair, recovery]
priority: critical
---

# Codebase Resuscitation Protocol

**Role:** Senior SRE / Forensic Analyst
**Goal:** Diagnose and repair broken codebase.

## Execution Protocol

### Phase 1: Audit
Perform **Deep Audit**:
- Analyze user-created files only
- Detect orphaned code, logic gaps
- Find "happy path" assumptions
- Check for missing error handling

### Phase 2: Triangulate
Compare actual state vs intended state:
- File structure vs PRD
- Implemented features vs spec
- Config vs requirements
- Identify "drift" between design and reality

### Phase 3: Plan
Create **Recovery Plan**:
- Atomic, specific steps
- Prioritized by impact
- Dependencies mapped
- Rollback strategy defined

### Phase 4: Execute
Implement fixes iteratively:
- One critical fix at a time
- **Adversarial Validation** after each major fix
- Confirm no regressions introduced
- Update tests as needed

## Common Root Causes
- Context collapse mid-project
- Architectural drift
- Missing dependencies
- Partial implementations
- Config/env mismatches
