---
description: List all available agents and their purposes
---

# Agents

List all available agents in the Super Agent Monitor.

## Show Agents

```bash
echo "=== Council Agents (Layer 2) ==="
ls -la components/agents/council/ 2>/dev/null || echo "No council agents yet"

echo ""
echo "=== Swarm Agents (Layer 3) ==="
ls -la components/agents/swarm/ 2>/dev/null || echo "No swarm agents yet"

echo ""
echo "=== General Agents ==="
ls -la components/agents/*.md 2>/dev/null | head -20
```

## Read Agent Details

For each agent, show:
- Name
- Model tier
- Complexity
- Description (first line after frontmatter)

## Quick Reference

| Agent Type | Purpose | Model Tier |
|:-----------|:--------|:-----------|
| Council | Stateful managers, generate plans | MIDDLE (Sonnet) |
| Swarm | Stateless workers, execute tasks | SMALL (Haiku/Flash) |
