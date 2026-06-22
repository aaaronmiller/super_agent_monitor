---
name: deep-audit
description: Forensic code analysis when AI says "looks good" but didn't actually look
category: validation
tags: [audit, code-quality, drift-detection]
priority: high
---

# Deep Audit Filter

Perform forensic analysis when surface-level review is insufficient.

## Execution

1. **Scope Definition**:
   - Analyze ONLY user-created files
   - IGNORE: node_modules, boilerplate, lockfiles, vendor/

2. **Detection Targets**:
   - Orphaned files (unused imports/exports)
   - Unused variables and dead code
   - `any` types (TypeScript)
   - Logic gaps and "happy path" assumptions
   - Missing error handling
   - Hardcoded values that should be config

3. **PRD Drift Verification**:
   - Cross-reference implemented code against PRD
   - Identify missing features ("drift")
   - Flag features implemented differently than specified

4. **Output: Remediation Matrix**

| Priority | File | Issue | Fix |
|----------|------|-------|-----|
| CRITICAL | path/to/file | Description | Specific fix |
| HIGH | path/to/file | Description | Specific fix |
| LOW | path/to/file | Description | Specific fix |

## Anti-Patterns
- Do NOT say "looks good" without evidence
- Do NOT skip any user-created files
- Do NOT ignore edge cases
