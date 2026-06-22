# OmniEdge — Claude Code Swarm Orchestrator Methodology

## Core Requirements
- **subagent_budget_tokens**: 150,000 tokens (for the agent's context window itself)
- **Skills/payload budget**: 30-50k tokens (what actually needs to fit in that budget)
- **Self-improving (mutagen enabled)**: Must learn and evolve from each run
- **Swarm capability**: Spawn many concurrent subagents
- **Skills, MCP, hooks**: Fully integrated

## Architecture
1. **Orchestrator** receives high-level task and spawns subagents
2. **Subagents** (file-auditor, cluster-analyzer, web-researcher, master-consolidator)
3. **Skills** (file-summarizer, similarity-cluster, web-scout)
4. **Hooks** (enforce budgets, capture outputs)
5. **Meta-agent** (self-improvement loop)

## Key Files
- `.claude/agents/orchestrator.md` - Main orchestrator
- `.claude/agents/file-auditor.md` - Audits file batches
- `.claude/agents/cluster-analyzer.md` - Groups related files
- `.claude/agents/web-researcher.md` - MCP-based research
- `.claude/agents/master-consolidator.md` - Consolidates output
- `.claude/skills/*.md` - Reusable skills
- `.claude/hooks/*.py` - Budget enforcement & output capture
- `scripts/*.py` - Helpers for batching, token estimation
- `scripts/merge_reports.sh` - Final consolidation

## Token Budget分配
- Each subagent gets 150k context window
- Skills/payloads must fit in 30-50k tokens
- Need to verify Claude Code agents can access this info

## Self-Improvement (Mutagen)
Need to research: https://github.com/Equilateral-AI/equilateral-agents-open-core
- Track performance (token usage, quality scores)
- Adjust prompts based on results
- Version and archive improvements
- Automate prompt evolution

## Integration
- This is an ADDITIONAL method for lovable-project
- If duplicates exist, integrate the worse into the better
- Focus on lovable-project folder, not root
