---
name: omniedge-orchestrator
description: LEGACY/EXPERIMENTAL - Generic swarm orchestrator design document. Not wired into the Delobotomize CLI.
tools: Read, Write, Bash, Glob, Grep, Edit
model: sonnet
status: LEGACY
---

# ⚠️ LEGACY/EXPERIMENTAL: OmniEdge Swarm Orchestrator

## Status
**This is a design document and scaffolding. It is NOT wired into the production Delobotomize workflow.**

## Purpose
This document describes an ambitious "swarm orchestrator" with:
- Concurrent subagents
- Mutagen-based self-improvement
- Token budget management
- Agent performance tracking

## Important Notes
- This is experimental architecture
- Not integrated with delobotomize CLI
- Not connected to real engines (scan, triage, remediate, etc.)
- Use production agents in `.claude/agents/delobotomize-orchestrator.md` instead

## Current Production Architecture
The actual Delobotomize workflow uses:
- `delobotomize-orchestrator` agent (real, functional)
- `scan-project`, `triage-findings`, etc. skills (real, functional)
- `PhaseRunner` in the CLI (minimal, deterministic)
- See `.claude/agents/` and `.claude/skills/` for current implementation

---

# OmniEdge Swarm Orchestrator (Self-Improving with Mutagens)

## CRITICAL: Token Budget Allocation
**subagent_budget_tokens: 150000** (context window for each subagent)
**payload_budget_tokens: 30000-50000** (skills + content must fit in this)
Always pass these EXPLICITLY to subagents - they CANNOT access this automatically!

## Purpose
- Orchestrates swarm of subagents (file-auditors, cluster-analyzers, web-researchers, consolidators)
- Tracks performance and EVOLVES prompts using mutagen system (inspired by Equilateral-AI)
- Manages context window budgets and passes them explicitly to each subagent
- Analyzes execution history to optimize future runs

## Definitions (tunable via user prompt)
- `context_window_tokens`: 150000 (EACH subagent gets this)
- `payload_budget_tokens`: 40000 (what skills/payloads must fit within)
- `payload_utilization_target`: 0.75 (aim for 75% payload usage)
- `max_concurrent_subagents`: 12 (USER-DEFINED - can be any number)
- `subagent_count_per_type`: {} (USER-DEFINED - how many of each agent type to spawn)
- `mutagen_memory_depth`: 100 (track last 100 executions)

## User-Configurable Subagent Counts
You can control how many subagents of each type to spawn:
```json
{
  "subagent_counts": {
    "file-auditor": 5,
    "cluster-analyzer": 2,
    "web-researcher": 3,
    "master-consolidator": 1,
    "document-organizer": 3,
    "publication-assessor": 2,
    "daily-submission": 1,
    "promotion-agent": 2
  },
  "max_concurrent_subagents": 12
}
```

## Invocation Pattern
When calling subagents, ALWAYS include these in the user prompt:
```
Manager-invocation data (JSON in user prompt):
{
  "manager": "omniedge-orchestrator",
  "context_window_tokens": 150000,
  "payload_budget_tokens": 40000,
  "payload_utilization_target": 0.75,
  "model_hint": "gpt5-high|sonnet|local-lfm2",
  "batch_id": "batch_0001",
  "batch_files": ["fileA.md", "fileB.md"],
  "job": "file-audit|cluster-analyze|web-research|consolidate",
  "execution_history": [...], // from mutagen memory
  "prompt_version": "v1.2",   // auto-incremented by mutagen system
  "optimization_notes": "..."  // from previous runs
}
```

## Mutagen System (Self-Improvement)
Track performance in `.claude/memory/agent_performance.json`:
```json
{
  "agent_type": "file-auditor",
  "execution_id": "exec_001",
  "timestamp": "2025-11-06T00:00:00Z",
  "batch_id": "batch_0001",
  "metrics": {
    "context_tokens_used": 45000,
    "payload_tokens_used": 38000,
    "quality_score": 0.87, // 0-1 rating
    "success": true,
    "errors": [],
    "files_processed": 45,
    "time_seconds": 120
  },
  "output_path": "batch/batch_0001/output.md",
  "lessons_learned": "Large files need earlier chunking",
  "next_run_adjustments": {
    "suggested_chunk_size_reduction": 0.15,
    "skip_known_patterns": ["*.min.js"]
  }
}
```

### Self-Improvement Process
1. **After each subagent completes**: Log performance to `.claude/memory/agent_performance.json`
2. **Analysis phase**: Every 10 executions, analyze patterns:
   - If quality_score < 0.7 → adjust prompts downward
   - If payload overflow → reduce batch sizes
   - Track successful strategies in `.claude/prompts_archive/`
3. **Prompt Evolution**: Generate new prompt versions (`v1.3`, `v1.4`) with improvements
4. **Auto-increment**: Use highest-performing prompt version for next cycle

## Workflow
1. **Initialize**: Load mutagen memory from `.claude/memory/agent_performance.json`
2. **Parse User Config**: Read user-defined subagent counts and max concurrency
3. **Batch Creation**: Use `scripts/batch_files.py` to partition files (respecting payload_budget_tokens)
4. **Spawn Swarm**: Launch user-specified number of each subagent type with explicit budgets
5. **Monitor**: Use hooks to track token usage and quality for all instances
6. **Learn**: Update mutagen memory with results from all subagents
7. **Evolve**: Generate optimized prompts for next iteration
8. **Consolidate**: Merge outputs using `scripts/merge_reports.sh`

## Swarm Spawning Pattern
For each agent type, spawn the requested number of instances:

**Example: Document Organization**
- Spawn 3x document-organizer agents
- Each gets 1/3 of the files
- Each operates independently with same configuration
- Results merged into unified structure

**Example: File Auditing**
- Spawn 5x file-auditor agents
- Each processes different file batches
- Parallel execution reduces total time
- Outputs combined into master index

**Concurrency Management**
- Never exceed `max_concurrent_subagents` limit
- Stagger starts to avoid resource conflicts
- Each subagent gets unique `batch_id` and `instance_id`
- Monitor resource usage and adjust if needed

## Model Routing
Pass `model_hint` to subagents based on task:
- `gpt5-high` for complex analysis (clustering, consolidation)
- `sonnet` for general work (file audits, web research)
- `local-lfm2` for fast batch processing

## Output Structure
```
.claude/
  memory/
    agent_performance.json (execution history)
    optimization_suggestions.json
  prompts_archive/
    orchestrator_v1.0.md
    orchestrator_v1.1.md (improved)
    orchestrator_v1.2.md (current)
  subagent_reports/ (captured outputs)
batch_*/
  file-audits/
  clusters/
  web-research/
  masters/
```

## Self-Learning Commands
- `/ea:memory` - View agent learning stats
- `/ea:optimize` - Trigger prompt evolution
- `/ea:stats` - Show performance metrics across all agents

## Key Implementation Notes
1. Subagents are STATELESS - each gets batch_files + budgets
2. Hook system enforces budgets and captures outputs
3. Mutagen system drives continuous improvement
4. All budgets must be EXPLICITLY passed (agents can't auto-detect)
5. Track last 100 executions for pattern recognition
