---
description: Prime context by reading key project files and summarizing capabilities
---

# Prime

Execute the following to understand the Super Agent Monitor codebase.

## Run
```bash
git ls-files | head -50
```

## Read Project Context
@README.md
@CLAUDE.md

## Read Available Agents
```bash
ls -la components/agents/*.md | head -10
```

## Read Available Tools
@scripts/tools/readme.md

## Read Current Tasks
@NEXT_STEPS/01_TASK_TRACKER.md

## Summarize

After reading, summarize:
1. Project purpose
2. Available agents (count and types)
3. Available tools
4. Current sprint status
5. Key implementation patterns
