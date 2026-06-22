# Optimized Integration Plan: Post-Validation

**Date:** 2025-12-08
**Source:** Adversarial Validation (10-member, 2-round, web-grounded)
**Status:** Ready for Execution

---

## Executive Summary

After adversarial validation, the deferred elements have been optimized into a 4-phase integration plan that prioritizes high-value items while deferring unvalidated complexity.

### Key Decisions

| Category | Original Count | Integrate Now | Defer | Reject |
|:---------|:---------------|:--------------|:------|:-------|
| Swarm Agents | 34 | 6 | 28 | 0 |
| Skills | 29 | 5 | 24 | 0 |
| Dot-Claude Agents | 13 | 3 | 3 | 7 |
| RAG Files | 3 | 1 (phased) | 2 | 0 |
| Commands | 6 | 0 | 6 | 0 |
| MACS Files | 2 | Sample | 2 | 0 |
| **TOTAL** | **87** | **15+sample** | **65** | **7** |

---

## Phase B: Skills Framework (Week 2)

### B.1: Create Skill Loader

**File:** `scripts/skill_loader.py`

```python
# Required functionality:
# 1. Scan .claude/skills/ for SKILL.md files
# 2. Parse YAML frontmatter (metadata only)
# 3. Match skill to current task context
# 4. Load full content only if matched
```

**Schema:** (Create as `.claude/skills/SKILL_SCHEMA.md`)

```yaml
---
name: skill-name           # Required: kebab-case identifier
description: |             # Required: What + When trigger
  Does X when Y condition is met.
  Use this skill when user asks for Z.
category: remediation      # Required: remediation|analysis|memory|validation|observability
priority: high             # Required: high|medium|low
triggers:                  # Optional: explicit activation phrases
  - "when user asks for..."
  - "when error occurs in..."
test_cases:                # Optional: validation cases
  - input: "..."
    expected: "..."
resources:                 # Optional: additional files
  - ./scripts/helper.py
  - ./data/lookup.json
---

[Skill instructions in Markdown below frontmatter]
```

### B.2: Skills to Integrate

| Skill | Source | Priority | Description |
|:------|:-------|:---------|:------------|
| `memory-ingest` | dot-claude/skills | HIGH | Ingest documents into memory |
| `remediation-plan` | dot-claude/skills | HIGH | Generate fix plans |
| `adversarial-validation` | claude-code/skills | HIGH | Multi-persona validation |
| `agentic-log-event` | dot-claude/skills | HIGH | Structured event logging |
| `scan-project` | dot-claude/skills | MEDIUM | Project structure analysis |

### B.3: Commands

```bash
# Port each skill
cp docs/amalgam/dot-claude/skills/memory-ingest.md .claude/skills/
cp docs/amalgam/dot-claude/skills/remediation-plan.md .claude/skills/
cp docs/amalgam/claude-code/skills/adversarial-validation.md .claude/skills/
cp docs/amalgam/dot-claude/skills/agentic-log-event.md .claude/skills/
cp docs/amalgam/dot-claude/skills/scan-project.md .claude/skills/
```

---

## Phase C: Agent Extraction (Week 2-3)

### C.1: From Legacy Swarms (6 agents)

| Agent | Source | Why Selected |
|:------|:-------|:-------------|
| `vulnerability-scanner` | security-swarm | Core security capability |
| `unit-test-generator` | test-swarm | Test automation |
| `coverage-analyzer` | test-swarm | Quality metrics |
| `code-quality-checker` | code-review-swarm | Code quality |
| `api-doc-generator` | documentation-swarm | Documentation automation |
| `dependency-optimizer` | refactoring-swarm | Dependency management |

**Commands:**
```bash
# Extract each agent to components/agents/
cp docs/amalgam/markdown_agents/legacy-swarms-v1/security-swarm/.claude/agents/vulnerability-scanner.md components/agents/
cp docs/amalgam/markdown_agents/legacy-swarms-v1/test-swarm/.claude/agents/unit-test-generator.md components/agents/
cp docs/amalgam/markdown_agents/legacy-swarms-v1/test-swarm/.claude/agents/coverage-analyzer.md components/agents/
cp docs/amalgam/markdown_agents/legacy-swarms-v1/code-review-swarm/.claude/agents/code-quality-checker.md components/agents/
cp docs/amalgam/markdown_agents/legacy-swarms-v1/documentation-swarm/.claude/agents/api-doc-generator.md components/agents/
cp docs/amalgam/markdown_agents/legacy-swarms-v1/refactoring-swarm/.claude/agents/dependency-optimizer.md components/agents/
```

### C.2: From Dot-Claude (3 agents)

| Agent | Why Selected |
|:------|:-------------|
| `master-consolidator` | Synthesis of multiple outputs |
| `memory-curator` | Memory management |
| `remediation-specialist` | Fix implementation |

**Commands:**
```bash
cp docs/amalgam/dot-claude/agents/master-consolidator.md components/agents/
cp docs/amalgam/dot-claude/agents/memory-curator.md components/agents/
cp docs/amalgam/dot-claude/agents/remediation-specialist.md components/agents/
```

### C.3: Post-Extraction Validation

```bash
# Run migration script to add v2.0 fields
python scripts/migrate_agents.py --analyze
python scripts/migrate_agents.py --migrate
```

---

## Phase D: RAG Foundation (Week 3-4)

### D.1: Embedding Pipeline (Immediate)

**File:** `scripts/embedding_pipeline.py`

```python
# Minimal embedding pipeline
# - Use text-embedding-3-small (OpenAI) or local e5-base
# - Store embeddings in JSON initially
# - Upgrade to pgvector when dataset >1000 docs
```

### D.2: pgvector Setup (Gated)

**Trigger:** Dataset exceeds 1000 documents

```sql
-- PostgreSQL setup
CREATE EXTENSION vector;
CREATE TABLE embeddings (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536),
    metadata JSONB
);
CREATE INDEX ON embeddings USING hnsw (embedding vector_cosine_ops);
```

### D.3: Port RAG Files (After pgvector)

| File | Action | Dependency |
|:-----|:-------|:-----------|
| `index_manager.py` | PORT | pgvector setup |
| `rag_pipeline.py` | PORT | index_manager |
| `mcp_interface.py` | DEFER | v2.5 (MCP integration) |

---

## Phase E: MACS Sampling (Week 4)

### E.1: Sampling Protocol

```bash
# Read first 400 lines of each file
head -400 docs/amalgam/MACS/Chat\ with\ gemini\ 3\ -\ MACS.md > /tmp/macs_sample_1.md
head -400 docs/amalgam/MACS/Chat\ with\ gemini\ 3\ -\ MACS\ -\ part\ II.md > /tmp/macs_sample_2.md
```

### E.2: Pattern Extraction Criteria

| Patterns Found | Action |
|:---------------|:-------|
| ≥3 new patterns | Continue full processing |
| <3 new patterns | Mark as fully extracted |

### E.3: Known Extracted Patterns

Already captured in `06_AMALGAM_INSIGHTS.md`:
- Hub-spoke topology
- Isolate → Inject → Ignite
- Leaves cannot branch
- Filesystem as shared memory

---

## Phase F: Deferred Items (v2.5+)

### F.1: Commands (6 items)

| Command | Reason for Deferral |
|:--------|:--------------------|
| delobotomize.run | Needs command registry |
| delobotomize.run-auto | Needs command registry |
| delobotomize.iterate | Needs command registry |
| delobotomize.memory | Needs memory system |
| audit.md | Needs audit phase |
| orchestrate.md | Needs orchestration |

### F.2: Remaining Skills (24 items)

Integrate based on usage data after core 5 are validated.

### F.3: Specialized Agents (3 items)

| Agent | Condition for Integration |
|:------|:--------------------------|
| cluster-analyzer | Clustering use case validated |
| web-researcher | Web search integration added |
| delobotomize-orchestrator | Command system built |

### F.4: Full Swarm Orchestration (28 agents)

**Condition:** Prove >20% improvement over individual agents in pilot.

---

## Execution Checklist

### Week 2: Skills Framework
- [ ] Create `scripts/skill_loader.py`
- [ ] Create `.claude/skills/SKILL_SCHEMA.md`
- [ ] Port 5 priority skills
- [ ] Validate skill loading

### Week 2-3: Agent Extraction
- [ ] Extract 6 swarm agents
- [ ] Extract 3 dot-claude agents
- [ ] Run migration script
- [ ] Validate agent definitions

### Week 3-4: RAG Foundation
- [ ] Create embedding pipeline
- [ ] Test with <1000 doc dataset
- [ ] Document pgvector upgrade path

### Week 4: MACS Sampling
- [ ] Sample first 400 lines each file
- [ ] Count new patterns found
- [ ] Document findings if >3

---

## Success Criteria

| Metric | Target |
|:-------|:-------|
| Skills integrated | 5 |
| New agents integrated | 9 |
| Skill loader functional | Yes |
| Embedding pipeline functional | Yes |
| All new agents pass validation | Yes |
| MACS sampling complete | Yes |

---

## Risk Register

| Risk | Impact | Probability | Mitigation |
|:-----|:-------|:------------|:-----------|
| Skill format inconsistency | MEDIUM | HIGH | Schema validation |
| Agent overlap with existing | LOW | MEDIUM | Pre-extraction audit |
| RAG complexity overrun | MEDIUM | LOW | Phase gating |
| MACS files empty of value | LOW | MEDIUM | Early sampling |
