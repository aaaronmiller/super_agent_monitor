---
description: Forensic audit - find orphaned code, drift, logic gaps
argument-hint: $TARGET_DIRECTORY
---

# Deep Audit

Perform **Forensic Code Analysis** on: $ARGUMENTS

## Scope
- Analyze ONLY user-created files
- IGNORE: node_modules, boilerplate, lockfiles

## Detection Targets
1. Orphaned files (unused imports/exports)
2. Unused variables and dead code
3. `any` types (TypeScript)
4. Logic gaps and "happy path" assumptions
5. Missing error handling
6. PRD drift (implemented != specified)

## Output Format

Create **Remediation Matrix**:

| Priority | File | Issue | Fix |
|----------|------|-------|-----|
| CRITICAL | | | |
| HIGH | | | |
| LOW | | | |

Do NOT say "looks good" without evidence.
