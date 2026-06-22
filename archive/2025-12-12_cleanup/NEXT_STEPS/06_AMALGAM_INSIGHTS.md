# Amalgam Analysis: Extracted Insights & Observations

This document captures all key insights, patterns, and observations extracted from `/docs/amalgam/` during the migration planning process.

---

## 1. Documents Analyzed

| Document | Size | Lines | Key Focus |
|:---------|:-----|:------|:----------|
| `markdown_agents/prd.md` | 43KB | 751 | Super Agent Monitor PRD v1.0 |
| `markdown_agents/agent_definition.md` | 26KB | 1083 | CIO Pattern deployment |
| `Generic Agent Monitoring & Deployment Architecture.md` | 91KB | 2961 | Three-layer monitoring |
| `Strategic Analysis SwarmForge Implementation Roadmap.md` | 140KB | 2691 | SwarmForge PRD v3.1 |
| `MACS/NOTES_ITEM_1.md` | 4KB | 111 | Hub-spoke topology |
| `ADVERSARIAL_VALIDATION_RESEARCH.md` | 8KB | 171 | Council patterns |
| `ORCHESTRATOR_METHODOLOGY.md` | 2KB | 44 | Swarm orchestration |

---

## 2. Core Architectural Patterns Extracted

### 2.1 Three-Layer Monitoring Architecture
**Source:** `Generic Agent Monitoring & Deployment Architecture.md`

```
┌─────────────────────────────────────────────────────┐
│         Layer 3: Monitoring Hub                      │
│         (Aggregates data, detects hangs,            │
│          controls routing, deploys agents)          │
└───────────────────┬─────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ↓                       ↓
┌─────────────────────┐  ┌──────────────────────┐
│  Layer 2: Hooks     │  │  Layer 1: Proxy      │
│  (Success Path)     │  │  (Failure Detection) │
│  - Tool lifecycle   │  │  - API interception  │
│  - Event telemetry  │  │  - Model routing     │
└─────────────────────┘  └──────────────────────┘
```

**Key Insight:** Hooks capture successful operations; Proxy catches failures when hooks are silent.

### 2.2 MACS Hub-and-Spoke Topology
**Source:** `MACS/NOTES_ITEM_1.md`

- Root orchestrator (CLAUDE.md) stays alive
- Subagents are ephemeral workers
- "Leaves cannot branch" - workers can't spawn workers
- Pattern: **Isolate → Inject → Ignite**

### 2.3 Context-Injected Orchestration (CIO) Pattern
**Source:** `agent_definition.md`

```
Predefined Solution + Runtime Prompt = Executed Action
      ↓                    ↓                ↓
  .claude folder      User's intent    Claude Code runs
```

**Three Components:**
1. Static Context: `.claude/` folder with agent definitions
2. Dynamic Intent: User's runtime prompt
3. Orchestrator: Claude Code CLI (headless execution)

---

## 3. Script-Based Progressive Disclosure
**Source:** `Strategic Analysis SwarmForge Implementation Roadmap.md`

**Critical Constraint:**
> "DO NOT READ THE SCRIPTS THEMSELVES; rely only on --help output"

**Why:** Achieves <2k token overhead per tool (vs 10k for MCP)

**Implementation Pattern:**
```
readme.md (intent→script mapping)
    ↓
Agent executes: uv run scripts/{name}.py --json
    ↓
Only output enters context (never source code)
```

**Token Savings:**
- MCP approach: ~10k tokens per tool
- Progressive disclosure: ~2k tokens per tool
- **94% reduction**

---

## 4. Council Voting with Byzantine Fault Tolerance
**Source:** `Strategic Analysis SwarmForge`, `ADVERSARIAL_VALIDATION_RESEARCH.md`

**Vote Schema:**
```json
{
  "agent_id": "validator-1",
  "target_id": "code-reviewer",
  "score": 0.5,
  "rationale": "Missing edge case coverage"
}
```

**Configuration:**
- Council size: 5 agents (configurable)
- Quorum: ceil(n/2) + 1 = 3 votes
- Consensus threshold: 0.8
- Termination: **Two-strike rule** (consecutive failures)

**Council Patterns from Research:**
1. **CEO Pattern**: Single orchestrator, parallel workers
2. **Playoff/Tournament**: Elimination brackets
3. **RCR (Reflect-Critique-Refine)**: Iterative improvement

---

## 5. Color-Coded Strategic Routing
**Source:** `Strategic Analysis SwarmForge Implementation Roadmap.md`

| Lane | Color | Task Type | Model | Token Budget |
|:-----|:------|:----------|:------|:-------------|
| GREEN | Direct execution | haiku | 1k |
| YELLOW | Pattern matching | sonnet | 5k |
| RED | Deep planning | opus | 50k |
| GRAY | Summarization | haiku | 2k |

**Routing Logic:**
```yaml
# In agent YAML frontmatter
color_lane: GREEN  # Direct file ops
color_lane: YELLOW # Pattern-based dev
color_lane: RED    # CEO-level planning
```

---

## 6. Hook System Requirements
**Source:** `Generic Agent Monitoring & Deployment Architecture.md`

**Required Hooks:**
1. `SessionStart` - Context gathering, project registration
2. `SessionEnd` - Completion metrics, TTS notification
3. `PreToolUse` - Tool invocation logging
4. `PostToolUse` - Tool completion logging
5. `SubagentStop` - Subagent lifecycle tracking

**Hook Configuration (settings.json):**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "uv run .claude/hooks/send_event.py --event-type PreToolUse"}]
    }]
  }
}
```

---

## 7. Agent Resume Capability
**Source:** `Strategic Analysis SwarmForge Implementation Roadmap.md`

**Pattern:**
1. Agent writes context to `agent-{id}.jsonl` on termination
2. On resume, transcript rehydrated from AgentDB
3. Cross-session persistence (weekend shutdown → Monday restart)

**Benefits:**
- Zero context loss between sessions
- Enables long-running tasks
- Supports graceful failure recovery

---

## 8. Output Standardization
**Source:** `Generic Agent Monitoring & Deployment Architecture.md`

**Analysis Phase Outputs (ALL REQUIRED):**
1. `ANALYSIS.md` - Human-readable findings
2. `WORKFILE.json` - Machine-readable structure
3. `DIFFS.txt` - Patch-style proposed changes

**Output Directory Structure:**
```
.super_agent_monitor/
├── cache/          # 30min TTL
├── audit/          # Audit phase outputs
├── analysis/       # Analysis phase outputs
├── recovery/       # Recovery plans
├── fix/            # Fix phase logs
└── runs/           # Session logs
```

---

## 9. Hang Detection Algorithm
**Source:** `Generic Agent Monitoring & Deployment Architecture.md`

**Detection Matrix:**

| Proxy Status | Hook Status | Diagnosis | Action |
|:-------------|:------------|:----------|:-------|
| Active | Active | Normal | None |
| Active | Silent (2min+) | Agent stuck | Check/restart |
| Silent (2min+) | Active | User wait | None (normal) |
| Silent (2min+) | Silent (2min+) | Complete hang | Force restart |

---

## 10. Model Sizing Strategy
**Source:** Various amalgam docs

**Tier Mapping:**
```yaml
opus:    # Architecture, research, synthesis
  - architect
  - lead
  - orchestrator
  - master

sonnet:  # Analysis, refactoring, testing
  - analyzer
  - reviewer
  - auditor

haiku:   # File ops, scanning, formatting
  - scanner
  - scraper
  - formatter
  - monitor
```

---

## 11. PRD Feature Requirements Extracted

### From `markdown_agents/prd.md`:

**Workflow Management (FR-WF):**
- Workflow JSON/YAML schema
- Pre-built templates (10-20)
- User-saved custom workflows
- Workflow versioning
- Export/import with conflict resolution

**Component Library (FR-CR):**
- 20-30 agents ✓ (we have 33)
- 20-30 skills ✓ (we have 44)
- 10-15 hooks ✓ (we have 29)
- 20-30 scripts (need audit)
- 10-15 MCP tools (need audit)

**Session Management (FR-SL):**
- Headless launcher ✓ (deploy.sh)
- Stall detection (300s timeout)
- Kick prompt injection
- Graceful restart

**RAG Memory (FR-VM):**
- Vector store (pgvector)
- Embedding service
- Semantic search
- Context injection

**Lifecycle (FR-CL):**
- Age-based cleanup
- Size-based cleanup
- Pre-cleanup notification
- Export/import

---

## 12. Voice System Integration
**Source:** Web search + `observability/utils/tts/`

### Current State:
- ElevenLabs TTS (observability/utils/tts/elevenlabs_tts.py)
- OpenAI TTS (observability/utils/tts/openai_tts.py)
- pyttsx3 offline (observability/utils/tts/pyttsx3_tts.py)

### Target State:
- **TTS**: Microsoft VibeVoice via Replicate API
- **STT**: NVIDIA Parakeet v3 via NeMo

### VibeVoice Availability:
- Official GitHub: Temporarily disabled (responsible AI review)
- Alternative APIs: Replicate, Fal.ai, AI/ML API

### Parakeet Details:
- Model: `nvidia/parakeet-tdt-0.6b-v3`
- Languages: 25 European languages
- Requirements: CUDA GPU recommended

---

## 13. Key Decisions Made

1. **Voice Provider**: Use Replicate API for VibeVoice (stable, easy integration)
2. **STT Provider**: Local NeMo for Parakeet (free, high quality)
3. **Council Size**: Default 5 agents, configurable
4. **Termination**: Two-strike rule (prevents false positives)
5. **Script Isolation**: Enforce "DO NOT READ SCRIPTS" constraint
6. **Model Routing**: ONNX classifier for task complexity (planned)
7. **Token Target**: 450-500 tokens per agent (optimal context efficiency)

---

## 14. Conflicts & Resolutions

### Conflict 1: Skills Lock-in
- **Issue**: Claude Code skills create ecosystem lock-in
- **Resolution**: Implement as portable directories first, defer native integration to v2.0

### Conflict 2: Resumption Logic
- **Issue**: `--resume` flags may cause incomplete task execution
- **Resolution**: Remove resumption logic; phases must complete or restart from scratch

### Conflict 3: Agent Token Bloat
- **Issue**: Many agents exceed 500-token target (avg 1055)
- **Resolution**: Extract verbose content to skills, trim bodies

---

## 15. Implementation Priority

| Priority | Feature | Source |
|:---------|:--------|:-------|
| P0 | Script isolation constraint | SwarmForge |
| P0 | Voice system upgrade | User request |
| P1 | Agent template standardization | PRD + Agent Definition |
| P1 | Hook migration | Generic Agent Monitoring |
| P2 | Council voting | SwarmForge + Adversarial |
| P2 | MACS mission isolation | MACS notes |
| P3 | RAG memory system | PRD |
| P3 | Cost-aware routing | SwarmForge |

---

## 16. Files Created from Analysis

| File | Purpose |
|:-----|:--------|
| `NEXT_STEPS/00_SCRATCH.md` | File inventory |
| `NEXT_STEPS/01_TASK_TRACKER.md` | Progress tracking |
| `NEXT_STEPS/02_VOICE_INTEGRATION.md` | Voice research |
| `NEXT_STEPS/03_FEATURE_GAP_ANALYSIS.md` | PRD vs current |
| `NEXT_STEPS/04_AGENT_TEMPLATE_SPEC.md` | 450-token format |
| `NEXT_STEPS/05_MIGRATION_PRD.md` | 7-week plan |
| `NEXT_STEPS/06_AMALGAM_INSIGHTS.md` | **This document** |
