---
description: Build/implement a plan file
argument-hint: [path-to-plan]
allowed-tools: Read, Write, Edit, Bash
---

# Build

Implement the plan at the specified path.

## Variables

PATH_TO_PLAN: $ARGUMENTS

## Workflow

1. If no PATH_TO_PLAN provided, STOP and ask user
2. Read the plan at PATH_TO_PLAN
3. Ultrathink about implementation
4. Execute step by step
5. Report results

## Report

- Summarize work done (bullet points)
- Report files changed: `git diff --stat`
