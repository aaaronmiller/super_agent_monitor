---
description: Quick-deploy a headless agent mission with optional continuation prompts
argument-hint: <agent-name> [--prompt "task"] [--nudge "keep going"] [--nudge-count 3]
allowed-tools: Bash, Read, Write
---

# Deploy Mission

Deploy a headless agent mission with optional automatic continuation prompts.

## Variables

AGENT_NAME: $1
TASK_PROMPT: $2 or "Complete the assigned task"
NUDGE_PROMPT: $3 or "Continue with remaining work"
NUDGE_COUNT: $4 or 0

## Quick Examples

```bash
# Simple deploy
/deploy scout

# Deploy with specific task
/deploy analyst "Analyze all Python files for security issues"

# Deploy with automatic continuations
/deploy refactorer "Refactor the authentication module" --nudge "Keep going" --nudge-count 3
```

## Workflow

1. **Validate Agent** - Check agent exists in `components/agents/` or `.claude/agents/`
2. **Create Mission** - Use `scripts/mission_launcher.py` to create isolated environment
3. **Launch Headless** - Start `claude --headless` with the task prompt
4. **Monitor** - Track PID and output
5. **Continue** (if nudge-count > 0) - Send continuation prompts when agent idles

## Implementation

```bash
# Deploy the mission
python scripts/mission_launcher.py launch \
  --agent "$AGENT_NAME" \
  --prompt "$TASK_PROMPT" \
  --nudge "$NUDGE_PROMPT" \
  --nudge-count $NUDGE_COUNT
```

## Report

After deployment:
- Mission ID
- PID
- Log file location
- Estimated completion time (if available)
