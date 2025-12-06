# The `.claude` Architecture
## Overview
The `.claude` directory is the central repository for all your autonomous agents (Orchestrators). Unlike a standard Claude Code setup where configuration is hidden or global, Super Agent Monitor treats each subfolder in `.claude` as a distinct, deployable agent "persona".

## Folder Structure
```
.claude/
├── [Agent Name]/
│   ├── CLAUDE.md           # The Brain (Instructions)
│   ├── config.json         # The Body (Configuration)
│   ├── scripts/            # The Hands (Custom Tools)
│   └── memory/             # The Memory (Local Context)
```

### 1. `CLAUDE.md` (The Brain)
This file contains the **System Prompt** and **Operational Instructions**.
- **Role Definition**: "You are a Senior Python Engineer..."
- **Rules**: "Always write tests first."
- **Knowledge**: "Use the `utils` library for X."

### 2. `config.json` (The Body)
This file defines the runtime parameters of the agent.
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "temperature": 0.5,
  "max_tokens": 4096,
  "tools": ["mcp-server-1", "script-2"],
  "runtime": "local" // or "e2b"
}
```

### 3. `scripts/` (The Hands)
Any Python or Bash script in this directory is automatically exposed to the agent as a tool.
- `scripts/search_web.py` -> `search_web()`
- `scripts/deploy.sh` -> `deploy()`

## Subagent Orchestration
You can create "Swarms" by having one agent call another.
1. Create a `Manager` agent in `.claude/manager`.
2. Create a `Worker` agent in `.claude/worker`.
3. Give the Manager a tool to launch the Worker (using the `SessionLauncher` API or CLI).

## Monitor Hooks
The Super Agent Monitor injects "hooks" into the agent's runtime to capture:
- **Thoughts**: The `<thinking>` blocks from Claude.
- **Tool Use**: Which tool was called and with what arguments.
- **Output**: The final response.

These hooks stream data to the **Session Monitor** UI in real-time via WebSockets.
