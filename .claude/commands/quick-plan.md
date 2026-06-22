---
description: Create a quick implementation plan and save to specs/
argument-hint: [description of what to build]
allowed-tools: Read, Write, Glob, Grep
---

# Quick Plan

Create a detailed implementation plan based on the user's requirements.

## Variables

USER_PROMPT: $ARGUMENTS
PLAN_OUTPUT_DIRECTORY: specs/

## Instructions

1. Analyze USER_PROMPT to understand requirements
2. Think deeply (ultrathink) about implementation approach
3. Create plan with:
   - Problem statement
   - Technical approach
   - Step-by-step implementation
   - Testing strategy
   - Success criteria
4. Generate kebab-case filename
5. Save to `specs/<name>.md`

## Report Format

```
✅ Implementation Plan Created

File: specs/<filename>.md
Topic: <brief description>
Key Components:
- <component 1>
- <component 2>
- <component 3>
```
