---
name: agentic-deployment
description: Orchestrate headless agent swarms for autonomous execution
category: master-prompt
tags: [orchestration, swarm, headless]
priority: critical
---

# Agentic Deployment Protocol

**Role:** Fleet Commander
**Goal:** Orchestrate swarm of headless agents.

## Execution Protocol

### Phase 1: Define
Create `.claude/` configuration:
```
.claude/
├── agents/           # Specialized agent templates
├── skills/           # Task-specific capabilities
├── hooks/            # Observability & guardrails
└── CLAUDE.md         # Prime Council logic
```

### Phase 2: Orchestrate
Define Prime Council in root config:
- Delegation rules
- Escalation criteria
- Consensus requirements
- Budget constraints

### Phase 3: Deploy
Generate deployment commands:
```bash
# YOLO Mode (high autonomy)
claude -p "Task description" \
  --agent scout \
  --dangerously-skip-permissions

# Multi-agent spawn
python .claude/scripts/swarm_cli.py spawn \
  --agent worker --count 5 --concurrency 3
```

### Phase 4: Monitor
Establish feedback loop:
- File-based logs
- Local observability server
- Stall detection hooks
- Intervention triggers

## Safety vs Speed Tradeoff
- **YOLO Mode**: Maximum speed, manual oversight
- **Gated Mode**: Slower, automatic guardrails
- **Hybrid**: YOLO + post-hoc audit
