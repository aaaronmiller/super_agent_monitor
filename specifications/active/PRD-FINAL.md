# **Product Requirements Document: Super Agent Monitor**
## **Autonomous Multi-Agent Workflow Management & Monitoring Platform**

**Version:** 2.0 (Final)
**Date:** 2025-11-19
**Status:** Implementation Ready
**Classification:** Internal - Production Specification

---

## 📋 Executive Summary

Super Agent Monitor is a **workflow orchestration and monitoring platform** for autonomous, headless Claude Code agent swarms. The system enables users to configure, launch, monitor, and manage complex multi-agent workflows through an intuitive dashboard interface, eliminating manual `.claude` folder configuration and providing real-time observability of autonomous operations.

### Core Value Propositions

1. **One-Click Workflow Deployment**: Mix-and-match from 100+ pre-configured components to create custom agent environments
2. **Autonomous Operation**: Headless sessions run without user interaction, with intelligent stall detection and auto-recovery
3. **Visual Monitoring**: Real-time dashboard showing token usage, costs, agent coordination, and system health
4. **Model Flexibility**: Configure any model (Claude, GPT, Gemini, local) via claude-code-proxy routing
5. **Workflow Portability**: Share complete workflows as `.workflow` packages across teams
6. **Multi-Pattern Orchestration**: CEO-Worker, Star Topology, Round-Robin, Congress (later), Mesh (later)

### Reference Architecture Integration

**Built on proven open-source foundations**:

- **multi-agent-workflow**: Monitoring dashboard, hooks system, event tracking (70% retained, 30% custom overlay)
- **claude-code-proxy**: Model routing, token tracking, provider abstraction (globally installed, data consumed)

**MVP Strategy**: Copy reference implementations verbatim initially, then iteratively enhance while maintaining upstream compatibility via git submodules.

---

## 🏗️ System Architecture

### Architecture Diagram (CORRECTED)

```
┌─────────────────────────────────────────────────────────────┐
│                  USER INTERFACE (Vue 3)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Workflow    │  │  Component   │  │  Monitor     │      │
│  │  Selector    │  │  Library     │  │  Dashboard   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬────────────────────────────────────────────────┘
             │ REST API + SSE
             ↓
┌─────────────────────────────────────────────────────────────┐
│              BACKEND SERVICES (Bun/Node.js)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Workflow    │  │  Session     │  │  Component   │      │
│  │  Generator   │  │  Manager     │  │  Registry    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────────────────────────────────────────┐      │
│  │  Multi-Agent-Workflow Backend (Git Submodule)     │      │
│  │  - Event Collection  - Hook Processing           │      │
│  │  - SQLite Storage   - WebSocket Streaming        │      │
│  └──────────────────────────────────────────────────┘      │
└────────────┬───────────────────────┬────────────────────────┘
             │                       │
     ┌───────▼────────┐      ┌──────▼──────────────┐
     │  PostgreSQL    │      │  Temp Workflows     │
     │  + pgvector    │      │  .super_agent_      │
     │  (RAG Memory)  │      │   monitor/          │
     └────────────────┘      │    workflows/       │
                             │     {id}/.claude/   │
                             │      ├─ agents/     │
                             │      ├─ skills/     │
                             │      ├─ hooks/      │
                             │      └─ CLAUDE.md   │
                             └──────────┬──────────┘
                                        │
                             ┌──────────▼──────────┐
                             │   Claude Code CLI   │
                             │   (Headless Mode)   │
                             │   ANTHROPIC_BASE_   │
                             │   URL=localhost:..  │
                             └──────────┬──────────┘
                                        │ API Requests
                                        ↓
                             ┌──────────▼──────────┐
                             │  Claude Code Proxy  │ ← INTERCEPTION LAYER
                             │  (Global Install)   │
                             │  - Captures tokens  │
                             │  - Routes models    │
                             │  - Logs requests    │
                             └──────────┬──────────┘
                                        │ Proxied to API
                                        ↓
                             ┌──────────▼──────────┐
                             │   Anthropic API     │
                             │   (or OpenRouter,   │
                             │    vLLM, Ollama)    │
                             └─────────────────────┘
```

### Key Architectural Decisions

**Decision 1: Claude Code Proxy Positioning**
- **Position**: Between Claude Code CLI and Anthropic API (interception layer)
- **Configuration**: `ANTHROPIC_BASE_URL=http://localhost:8082` points Claude to proxy
- **Data Flow**: CLI → Proxy (capture) → API → Proxy (capture) → CLI
- **Rationale**: Transparent to Claude Code, captures all metrics (tokens, cost, latency, model routing)

**Decision 2: Git Submodules for Reference Repos**
- **Implementation**: `external/multi-agent-workflow/` as submodule
- **Update Strategy**: `git submodule update --remote` pulls upstream improvements
- **Wrapper Pattern**: Our API layer extends their endpoints without forking

**Decision 3: Dynamic Workflow Generation**
- **Location**: `.super_agent_monitor/workflows/{workflow-id}/.claude/`
- **Generation**: Copy components from library → Assemble into temp folder → Launch Claude
- **Lifecycle**: Keep 30 days OR until 1GB storage threshold

**Decision 4: Headless Autonomous Operation**
- **Launch**: `claude --headless --config=workflows/{id}/.claude/`
- **Monitoring**: Poll claude-code-proxy logs for API activity timestamps
- **Recovery**: Detect stall (no activity 5min) → Inject kick prompt OR restart gracefully

**Decision 5: Component-Based Architecture**
- **Library Size**: 20-30 items per category (agents/skills/hooks/scripts/orchestrators)
- **Format**: Markdown files with YAML frontmatter metadata
- **Smart Recommendations**: UI suggests compatible components based on dependencies

**Decision 6: RAG Memory System**
- **Storage**: PostgreSQL + pgvector for semantic search
- **Injection**: On session start, retrieve top-5 relevant memories from past workflows
- **Learning**: On session end, capture outputs + user annotations as new memories

---

## 🎯 MVP Features (18 Weeks)

### 1. Workflow Management

**Core Functionality:**
- Create workflows from scratch or templates
- Edit workflow metadata (name, description, tags)
- Configure components (agents, skills, hooks, scripts)
- Save custom workflows for reuse
- Export workflows as `.workflow` files (ZIP: JSON + component files)
- Import workflows with conflict resolution (overwrite/merge/skip)

**Workflow Schema:**
```yaml
id: deep-research-v1
name: Deep Research Agent
description: Multi-agent research with web scraping and synthesis
version: 1.0.0
author: system
tags: [research, autonomous, web-scraping]

orchestration:
  pattern: ceo-worker  # ceo-worker | star | round-robin
  model: claude-sonnet-4
  systemPrompt: orchestrators/research-coordinator.md
  thinkingBudget: 10000

components:
  agents:
    - researcher-primary
    - web-scraper
    - citation-analyzer
  skills:
    - web-search-advanced
    - academic-citation
  hooks:
    - cost-tracker
    - stall-detector
  scripts:
    - fetch-url.py
    - parse-pdf.py

memory:
  enabled: true
  persistence: session  # session | permanent
  rag: true
  retrievalK: 5

lifecycle:
  haltDetectionSeconds: 300
  autoRestart: true
  maxRetries: 3
  kickPrompt: "Continue with your task. Review progress and proceed."
```

---

### 2. Component Library System

**Categories & Target Sizes:**

| Category | Target Count | Examples |
|----------|--------------|----------|
| **Agents** | 20 | researcher-primary, web-scraper, code-reviewer, tester, analyzer |
| **Skills** | 20 | web-search-advanced, api-design, db-optimization, security-audit |
| **Hooks** | 10 | cost-tracker, stall-detector, format-enforcer, permission-gate |
| **Scripts** | 20 | fetch-url.py, parse-pdf.py, extract-citations.py, analyze-sentiment.py |
| **Orchestrators** | 5 | research-coordinator, dev-coordinator, ops-coordinator |
| **Subagent Prompts** | 10 | focused-coder, thorough-reviewer, creative-brainstormer |

**Component Format (Agent Example):**
```markdown
---
name: researcher-primary
displayName: Primary Research Agent
description: Lead researcher coordinating information gathering
category: agent
tags: [research, coordination, autonomous]
dependencies: []
incompatibilities: [researcher-solo]
model: claude-sonnet-4
tools: [Read, Write, Bash, WebSearch]
version: 1.0.0
---

# Primary Research Agent

You are the lead research coordinator responsible for:

1. **Task Decomposition**: Break research questions into subtasks
2. **Delegation**: Assign to specialists (web-scraper, citation-analyzer)
3. **Synthesis**: Integrate findings into coherent output
4. **Quality Control**: Verify sources and fact-check

## Workflow
When given a research task:
1. Analyze scope and identify information needs
2. Delegate to specialist agents via @mentions
3. Monitor progress through agent outputs
4. Synthesize findings into structured markdown report
5. Generate citations in APA format

## Constraints
- NEVER fabricate sources - only cite verified URLs
- ALWAYS cross-reference facts across 3+ sources
- Maintain research log in `research-log.md`
```

**Smart Recommendations:**
- When user selects "researcher-primary", suggest "web-scraper" (dependency)
- When selecting "code-reviewer", suggest "tester" (common pairing)
- Highlight incompatibilities in red (can't select both "researcher-solo" + "researcher-primary")

---

### 3. Orchestration Patterns (MVP: 3 Essential)

**Pattern 1: CEO-Worker** (80% of use cases)
```yaml
pattern: ceo-worker
ceo:
  model: claude-sonnet-4
  role: planner
  systemPrompt: orchestrators/ceo-coordinator.md
workers:
  - agent: backend-expert
    model: claude-haiku-3
    triggers: [api, database, server]
  - agent: frontend-expert
    model: gpt-4o-mini
    triggers: [ui, component, styling]
  - agent: devops-expert
    model: qwen2.5-3b
    triggers: [deploy, docker, ci]
```

**How It Works:**
1. CEO receives task: "Build user authentication"
2. CEO decomposes: [Backend: JWT tokens, Frontend: Login form, DevOps: Environment vars]
3. CEO delegates to workers in parallel
4. Workers execute independently
5. CEO synthesizes results

**Pros**: Efficient, proven (84.8% SWE-Bench), clear hierarchy
**Cons**: CEO hallucination cascades to workers

---

**Pattern 2: Star Topology** (Parallel execution)
```yaml
pattern: star
hub:
  model: claude-sonnet-4
  role: task-dispatcher
  queue: redis
agents:
  - backend-expert
  - frontend-expert
  - devops-expert
  - tester
pullInterval: 5s
```

**How It Works:**
1. Hub broadcasts: "5 tasks available"
2. Agents pull work based on capability: backend-expert pulls "Create API endpoint"
3. Agents execute independently
4. Hub aggregates results
5. No coordination between agents (pure parallel)

**Pros**: Fault-tolerant (one crash doesn't block), scales horizontally
**Cons**: No inter-agent communication

---

**Pattern 3: Round-Robin** (Simple cycling)
```yaml
pattern: round-robin
agents:
  - web-scraper-1
  - web-scraper-2
  - web-scraper-3
healthCheckInterval: 30s
```

**How It Works:**
1. Tasks arrive: [Scrape page A, Scrape page B, Scrape page C]
2. Task 1 → Agent 1, Task 2 → Agent 2, Task 3 → Agent 3
3. Task 4 → Agent 1 (cycles back)
4. Health check skips unresponsive agents

**Pros**: Simplest, zero coordination cost, predictable
**Cons**: No intelligence, assumes agents equivalent

---

### 4. Model Configuration (Flexible via claude-code-proxy)

**User Configures Models Globally:**
```yaml
# ~/.claude-code-proxy/config.yml (User manages this)
models:
  large:
    provider: anthropic
    model: claude-sonnet-4
    maxTokens: 8192
    cost_per_1m_input: 3.00
    cost_per_1m_output: 15.00

  medium:
    provider: openrouter
    model: google/gemini-1.5-pro
    maxTokens: 4096
    cost_per_1m_input: 1.25
    cost_per_1m_output: 5.00

  small:
    provider: ollama
    model: qwen2.5:3b-instruct-q4_K_M
    maxTokens: 2048
    cost_per_1m_input: 0.00  # Local
    cost_per_1m_output: 0.00

routing:
  tool_calling: small      # 95% of operations
  reasoning: medium        # Complex logic
  architecture: large      # High-stakes decisions
  fallback: large          # If small model confidence < 0.7
```

**Our Workflows Reference Tiers:**
```yaml
# Workflow definition
agents:
  - name: backend-expert
    modelTier: medium  # User's config maps to gemini-1.5-pro
  - name: tester
    modelTier: small   # User's config maps to qwen2.5-3b
```

**Dashboard Display:**
- "Agent: backend-expert used google/gemini-1.5-pro (medium tier) - 1,234 tokens - $0.15"
- "Agent: tester used qwen2.5:3b (small tier) - 890 tokens - $0.00"

---

### 5. Session Management

**Launching Headless Sessions:**
```bash
# System configures proxy
export ANTHROPIC_BASE_URL="http://localhost:8082"

# Launch Claude Code
claude --headless \
  --config=.super_agent_monitor/workflows/{workflow-id}/.claude \
  --session-id={session-id} \
  --output-format=json
```

**Stall Detection & Recovery:**
1. Monitor claude-code-proxy logs: Parse `~/.claude-proxy/requests.log`
2. Track last API request timestamp
3. If `now - lastRequest > 300s` → STALLED
4. Recovery attempt 1: Inject prompt via Claude Code session API (if available)
5. Recovery attempt 2: Graceful restart (`SIGTERM`, wait for state save, relaunch)
6. Recovery attempt 3: Force restart (`SIGKILL` after 30s, relaunch fresh)
7. Max retries: 3 (configurable)
8. After 3 failures: Mark session as FAILED, alert user

**Session Lifecycle:**
- `STARTING` → `RUNNING` → `COMPLETED` (success)
- `STARTING` → `RUNNING` → `STALLED` → `RECOVERING` → `RUNNING` (auto-fixed)
- `STARTING` → `RUNNING` → `STALLED` → `FAILED` (recovery failed)

---

### 6. Monitoring Dashboard (Multi-Agent-Workflow + 30% Custom)

**Base Features (70% Retained from multi-agent-workflow):**
- ✅ Real-time event stream (PreToolUse, PostToolUse, SubagentSpawn)
- ✅ SQLite event storage
- ✅ WebSocket/SSE streaming
- ✅ Hook event tracking
- ✅ Filterable event log (by agent, severity, type)
- ✅ Live pulse metrics

**Custom Overlays (30% New):**
- 🆕 **Workflow Selector Dropdown** (top bar): Switch active workflow without reload
- 🆕 **Component Library Panel** (left sidebar): Browse/filter components
- 🆕 **Model Usage Widget** (right sidebar): Show which models used, tokens, costs
- 🆕 **Agent Hierarchy Tree** (collapsible): CEO → Workers → Subagents
- 🆕 **Memory/RAG Status** (bottom panel): Show retrieved memories, relevance scores
- 🆕 **Session Controls** (toolbar): Start/Stop/Restart/Kick buttons
- 🆕 **Cost Accumulation Graph** (real-time line chart)

**Claude-Code-Proxy Data Integration:**
```javascript
// Poll proxy logs every 5s
fetch('/api/proxy/metrics')
  .then(data => {
    dashboard.updateTokens(data.total_tokens)
    dashboard.updateCost(data.total_cost_usd)
    dashboard.updateModelDistribution(data.model_usage)
  })
```

---

### 7. RAG Memory System

**Storage:**
- **Vector DB**: PostgreSQL + pgvector extension
- **Embedding Model**: OpenAI `text-embedding-3-small` (1536-dim) OR local ONNX
- **Query Latency Target**: <200ms for top-5 retrieval

**Memory Schema:**
```sql
CREATE TABLE memories (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES sessions(id),
  workflow_id UUID REFERENCES workflows(id),
  content_type VARCHAR(50), -- output | learning | pattern | error
  content TEXT NOT NULL,
  embedding vector(1536),
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  retrieval_score FLOAT DEFAULT 1.0  -- Boost for user annotations
);

CREATE INDEX idx_memories_embedding
  ON memories USING ivfflat (embedding vector_cosine_ops);
```

**Context Injection (On Session Start):**
```sql
-- Semantic search
SELECT content, metadata,
       1 - (embedding <=> query_embedding) AS similarity
FROM memories
WHERE workflow_id = $1 OR workflow_id IS NULL  -- Cross-workflow learning
ORDER BY similarity DESC
LIMIT 5;
```

**Injected into CLAUDE.md:**
```markdown
# Research Workflow

## Relevant Past Experience

### Similar Task from 2025-11-10
**Task**: Deep research on AI safety regulations
**Outcome**: Successfully synthesized 50+ sources into 10k word report
**Key Learning**: Use citation-analyzer early to avoid duplicate source fetching
**Similarity Score**: 0.89

### Pattern from 2025-11-15
**Context**: When web-scraper encounters paywalls
**Resolution**: Delegate to pdf-fetcher with DOI lookup
**Similarity Score**: 0.76

---

## Your Task
[User's research question...]
```

**Learning Capture (On Session End):**
1. Extract outputs from workflow folder
2. Generate embeddings
3. Store in memories table
4. Prompt user: "What worked well? What didn't?"
5. Store annotations with `retrieval_score = 2.0` (2x boost in future retrievals)

---

### 8. Workflow Lifecycle & Cleanup

**Cleanup Policies:**
```yaml
cleanup:
  ageBasedDays: 30        # Delete if unused for 30 days
  sizeBasedGB: 1.0         # Delete oldest when total > 1GB
  checkInterval: "3:00am"  # Daily job

priority:
  # Deletion order (oldest first within each group)
  1: failed_sessions
  2: completed_sessions
  3: user_saved_workflows  # NEVER auto-delete
```

**Cleanup Process:**
1. Daily job runs at 3am
2. Query workflows: `last_used_at < NOW() - INTERVAL '30 days'`
3. Filter out `is_permanent = true`
4. Sort by `last_used_at ASC`
5. Archive to `.super_agent_monitor/archive/{workflow-id}.tar.gz` (90-day retention)
6. Delete temp folder
7. Update database: Mark as `archived`

**Pre-Cleanup Notification:**
- 7 days before deletion: Show banner in UI
- "Workflow 'Deep Research v1' will be deleted on 2025-11-26. Click to save permanently."
- User clicks → Set `is_permanent = true`

**Manual Export/Import:**
```bash
# Export
POST /api/workflows/{id}/export
# Returns: deep-research-v1.workflow (ZIP file)
# Contains: workflow.json + components/ + README.md

# Import
POST /api/workflows/import
# Upload: deep-research-v1.workflow
# UI shows conflicts: "agent 'researcher-primary' exists, overwrite?"
# Options: overwrite | merge (rename to researcher-primary-imported) | skip
```

---

## 🗄️ Database Schema

### Workflows Table
```sql
CREATE TABLE workflows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  version VARCHAR(20),
  author VARCHAR(255),
  tags TEXT[],
  definition JSONB NOT NULL,  -- Full YAML as JSON
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_used_at TIMESTAMP,
  is_template BOOLEAN DEFAULT FALSE,
  is_permanent BOOLEAN DEFAULT FALSE,
  storage_bytes BIGINT DEFAULT 0
);

CREATE INDEX idx_workflows_last_used ON workflows(last_used_at);
CREATE INDEX idx_workflows_tags ON workflows USING GIN(tags);
```

### Sessions Table
```sql
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES workflows(id),
  status VARCHAR(20), -- starting | running | stalled | recovering | completed | failed
  started_at TIMESTAMP DEFAULT NOW(),
  ended_at TIMESTAMP,
  last_activity_at TIMESTAMP,
  stall_count INTEGER DEFAULT 0,
  retry_count INTEGER DEFAULT 0,
  total_tokens INTEGER DEFAULT 0,
  total_cost_usd DECIMAL(10,4) DEFAULT 0,
  config_snapshot JSONB,  -- Frozen workflow definition
  output_path VARCHAR(500),
  error_message TEXT
);

CREATE INDEX idx_sessions_status ON sessions(status, started_at DESC);
CREATE INDEX idx_sessions_workflow ON sessions(workflow_id);
```

### Components Table
```sql
CREATE TABLE components (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) UNIQUE NOT NULL,
  display_name VARCHAR(255),
  category VARCHAR(50), -- agent | skill | hook | script | orchestrator | subagent
  description TEXT,
  tags TEXT[],
  dependencies TEXT[],
  incompatibilities TEXT[],
  content TEXT NOT NULL,  -- Full markdown
  metadata JSONB,          -- Parsed frontmatter
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  usage_count INTEGER DEFAULT 0  -- Track popularity
);

CREATE INDEX idx_components_category ON components(category);
CREATE INDEX idx_components_tags ON components USING GIN(tags);
CREATE INDEX idx_components_usage ON components(usage_count DESC);
```

### Memories Table
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES sessions(id),
  workflow_id UUID REFERENCES workflows(id),
  content_type VARCHAR(50), -- output | learning | pattern | error
  content TEXT NOT NULL,
  embedding vector(1536),
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  retrieval_score FLOAT DEFAULT 1.0
);

CREATE INDEX idx_memories_embedding
  ON memories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_memories_workflow
  ON memories(workflow_id, created_at DESC);
```

---

## 🔌 API Endpoints

### Workflows
```
POST   /api/workflows              - Create new workflow
GET    /api/workflows              - List workflows (filters: tags, template, recent)
GET    /api/workflows/:id          - Get workflow details
PUT    /api/workflows/:id          - Update workflow
DELETE /api/workflows/:id          - Delete workflow
POST   /api/workflows/:id/export   - Export as .workflow file
POST   /api/workflows/import       - Import .workflow file
POST   /api/workflows/:id/clone    - Duplicate workflow
```

### Components
```
GET    /api/components                      - List components (filter: category, tags)
GET    /api/components/:id                  - Get component details
POST   /api/components                      - Create custom component
PUT    /api/components/:id                  - Update component
DELETE /api/components/:id                  - Delete component
GET    /api/components/recommend?selected=  - Smart recommendations
GET    /api/components/validate?ids=        - Check compatibility
```

### Sessions
```
POST   /api/sessions               - Create session (launches headless Claude)
GET    /api/sessions               - List sessions (filters: status, workflow)
GET    /api/sessions/:id           - Get session details
POST   /api/sessions/:id/kick      - Inject kick prompt
POST   /api/sessions/:id/restart   - Graceful restart
DELETE /api/sessions/:id           - Terminate session
GET    /api/sessions/:id/logs      - Get session logs
GET    /api/sessions/:id/export    - Export session report (JSON/MD)
```

### Memory/RAG
```
GET    /api/memory/search?q=       - Semantic search
POST   /api/memory                 - Manually add memory
GET    /api/memory/sessions/:id    - Get session memories
DELETE /api/memory/:id              - Delete memory
POST   /api/memory/annotate/:id    - Add user annotation (boosts retrieval)
```

### Monitoring (Proxied from multi-agent-workflow)
```
GET    /api/events                 - List events (filters: session, agent, type)
GET    /api/events/:sessionId      - Get session events
GET    /stream/:sessionId          - SSE stream (real-time)
GET    /api/metrics/:sessionId     - Aggregate metrics
```

### Proxy Data
```
GET    /api/proxy/metrics/:sessionId  - Get token/cost data from claude-code-proxy
GET    /api/proxy/models              - List available models
```

---

## 📁 Directory Structure

```
super_agent_monitor/
├── frontend/                              # Vue 3 UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── WorkflowSelector.vue      # NEW: Dropdown switcher
│   │   │   ├── ComponentLibrary.vue      # NEW: Browse/filter components
│   │   │   ├── MonitorDashboard.vue      # MODIFIED: 70% original, 30% overlay
│   │   │   ├── MemoryViewer.vue          # NEW: RAG visualization
│   │   │   ├── SessionControls.vue       # NEW: Start/stop/restart
│   │   │   └── ModelUsageWidget.vue      # NEW: Show model distribution
│   │   ├── views/
│   │   │   ├── WorkflowEditor.vue
│   │   │   ├── ComponentBrowser.vue
│   │   │   └── SessionMonitor.vue
│   │   ├── stores/
│   │   │   ├── workflows.ts
│   │   │   ├── components.ts
│   │   │   └── sessions.ts
│   │   └── App.vue
│   └── package.json
│
├── backend/                               # Bun/Node.js API
│   ├── src/
│   │   ├── api/
│   │   │   ├── workflows.ts              # Workflow CRUD
│   │   │   ├── components.ts             # Component registry
│   │   │   ├── sessions.ts               # Session management
│   │   │   ├── memory.ts                 # RAG endpoints
│   │   │   └── monitoring.ts             # Proxy to multi-agent-workflow
│   │   ├── services/
│   │   │   ├── workflow-generator.ts     # Generate .claude folders
│   │   │   ├── session-launcher.ts       # Launch headless Claude
│   │   │   ├── stall-detector.ts         # Monitor + recovery
│   │   │   ├── rag-engine.ts             # Embedding + search
│   │   │   └── cleanup-scheduler.ts      # Daily cleanup job
│   │   ├── db/
│   │   │   ├── schema.sql
│   │   │   └── client.ts                 # PostgreSQL connection
│   │   └── index.ts                      # Main server
│   └── package.json
│
├── external/                              # Git submodules
│   └── multi-agent-workflow/             # Submodule: monitoring backend
│       ├── server/                        # Event collection, SQLite
│       ├── client/                        # Vue components
│       └── hooks/                         # PreToolUse, PostToolUse scripts
│
├── components/                            # Component library (seed)
│   ├── agents/                            # 20 items
│   │   ├── researcher-primary.md
│   │   ├── web-scraper.md
│   │   ├── code-reviewer.md
│   │   ├── tester.md
│   │   └── ... (16 more)
│   ├── skills/                            # 20 items
│   │   ├── web-search-advanced/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   ├── api-design/
│   │   └── ... (18 more)
│   ├── hooks/                             # 10 items
│   │   ├── cost-tracker.py
│   │   ├── stall-detector.py
│   │   └── ... (8 more)
│   ├── scripts/                           # 20 items
│   │   ├── fetch-url.py
│   │   ├── parse-pdf.py
│   │   └── ... (18 more)
│   ├── orchestrators/                     # 5 items
│   │   ├── ceo-coordinator.md
│   │   ├── research-coordinator.md
│   │   └── ... (3 more)
│   └── subagents/                         # 10 items
│       └── ... (10 prompts)
│
├── workflows/                             # Pre-built templates
│   ├── deep-research.yaml
│   ├── fast-coder.yaml
│   ├── security-audit.yaml
│   └── ... (7 more)
│
├── .super_agent_monitor/                  # Runtime data (gitignored)
│   ├── workflows/                         # Temp .claude folders
│   │   └── {workflow-id}/
│   │       └── .claude/
│   │           ├── agents/
│   │           ├── skills/
│   │           ├── hooks/
│   │           ├── scripts/
│   │           └── CLAUDE.md
│   ├── archive/                           # Deleted workflows (90-day)
│   └── logs/
│
├── docs/                                  # Documentation
│   ├── architecture.md
│   ├── api-reference.md
│   └── user-guide.md
│
├── docker-compose.yml                     # Local development setup
├── README.md
└── PRD-FINAL.md                           # This document
```

---

## 📅 Implementation Roadmap (18 Weeks)

### Phase 0: Foundation (Weeks 1-2)
- [x] Repository setup
- [x] Add `external/multi-agent-workflow` as git submodule
- [x] Database schema design + migrations
- [x] Create 5 example components per category (total 25)
- [x] Write 3 workflow templates (deep-research, fast-coder, security-audit)

### Phase 1: Workflow Engine (Weeks 3-5)
- [ ] Workflow schema validator
- [ ] Workflow generator service (YAML → .claude folder)
- [ ] Component registry with filesystem scanner
- [ ] Smart component recommendations
- [ ] REST API: workflows + components
- [ ] Basic UI: Component library browser

### Phase 2: Session Management (Weeks 6-8)
- [ ] Session launcher (headless Claude Code)
- [ ] Claude Code installation detection + auto-install helper
- [ ] Stall detection service (monitor claude-code-proxy logs)
- [ ] Recovery strategies (kick, graceful restart, force restart)
- [ ] Session API endpoints
- [ ] UI: Session list + control panel

### Phase 3: Monitoring Dashboard (Weeks 9-11)
- [ ] Integrate multi-agent-workflow backend (git submodule)
- [ ] API wrapper layer (Express/Fastify)
- [ ] Custom UI overlays (30%):
  - Workflow selector dropdown
  - Component library sidebar
  - Model usage widget
  - Session controls toolbar
- [ ] Real-time SSE streaming
- [ ] Claude-code-proxy data integration (token/cost display)

### Phase 4: RAG Memory (Weeks 12-14)
- [ ] PostgreSQL + pgvector setup
- [ ] Embedding service (OpenAI API or local ONNX)
- [ ] Memory CRUD operations
- [ ] Semantic search endpoint (top-K retrieval)
- [ ] Context injection on session start
- [ ] Learning capture on session end
- [ ] UI: Memory viewer + search

### Phase 5: Lifecycle & Polish (Weeks 15-17)
- [ ] Cleanup policy service (age + size based)
- [ ] Daily cleanup scheduler (3am cron)
- [ ] Workflow export (.workflow ZIP format)
- [ ] Workflow import with conflict resolution UI
- [ ] Pre-cleanup notifications (7-day warning)
- [ ] Archive system (90-day retention)

### Phase 6: Testing & Documentation (Week 18)
- [ ] Populate component library (100+ total items)
- [ ] Write 10 workflow templates
- [ ] User documentation (README, guides, videos)
- [ ] API documentation (OpenAPI spec)
- [ ] Docker Compose setup
- [ ] Beta testing with 5 users

---

## 🚀 Phase 2 Features (Months 6-9) - VIRAL POTENTIAL

### Model Debates (Month 7-8) 🔥 **PRIORITY #1**

**Feature**: Multi-model deliberation before decisions

```yaml
debate:
  participants:
    - model: claude-sonnet-4
      role: architect
      systemPrompt: "You favor simple, maintainable solutions"

    - model: gpt-4
      role: optimizer
      systemPrompt: "You prioritize performance and scalability"

    - model: gemini-1.5-pro
      role: judge
      systemPrompt: "You evaluate both arguments and decide"

  maxRounds: 5
  finalDecision: judge-decides  # or majority-vote | consensus-required

  prompt: "Should we use PostgreSQL or MongoDB for user data?"
```

**UI Mockup:**
```
┌─────────────────────────────────────────────────────────┐
│ Model Debate: Database Choice                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌─────────────────────┐  ┌─────────────────────┐       │
│ │ Claude Sonnet 4     │  │ GPT-4               │       │
│ │ (Architect)         │  │ (Optimizer)         │       │
│ ├─────────────────────┤  ├─────────────────────┤       │
│ │ Round 1:            │  │ Round 1:            │       │
│ │ "Use PostgreSQL.    │  │ "Use MongoDB.       │       │
│ │ ACID guarantees are │  │ Flexible schema for │       │
│ │ critical for user   │  │ rapid iteration."   │       │
│ │ data integrity."    │  │                     │       │
│ ├─────────────────────┤  ├─────────────────────┤       │
│ │ Round 2:            │  │ Round 2:            │       │
│ │ "MongoDB lacks      │  │ "PostgreSQL's JSON  │       │
│ │ transactions across │  │ type gives us both  │       │
│ │ documents."         │  │ structure + flex."  │       │
│ └─────────────────────┘  └─────────────────────┘       │
│                                                          │
│ ┌──────────────────────────────────────────────┐       │
│ │ Gemini 1.5 Pro (Judge)                       │       │
│ ├──────────────────────────────────────────────┤       │
│ │ Final Decision (Round 3):                    │       │
│ │                                               │       │
│ │ "Use PostgreSQL with JSONB columns.          │       │
│ │ This provides ACID + flexibility.            │       │
│ │ Architect's integrity concerns are valid,    │       │
│ │ while Optimizer's flexibility need is met    │       │
│ │ by JSONB support."                           │       │
│ └──────────────────────────────────────────────┘       │
│                                                          │
│ [Apply Decision]  [Export Debate Transcript]            │
└─────────────────────────────────────────────────────────┘
```

**Use Cases:**
- Architecture decisions (debate best approach)
- Code review (2 models debate if code is production-ready)
- Research validation (3 models cross-check facts)
- Security analysis (red team vs blue team debate)

**Viral Potential**: **EXTREMELY HIGH**
- Shareable: "Watch AI models debate architecture"
- Memeable: "Claude roasts GPT-4's MongoDB suggestion"
- Educational: Shows reasoning behind decisions
- Unique: Nobody's visualizing multi-model deliberation

---

### Congress Voting (Month 6-7)

**Feature**: Byzantine fault tolerance via peer review

```yaml
pattern: congress
size: 5
quorum: 0.8  # 80% consensus required
termination: true  # Terminate lowest-voted on failure
encryptedVotes: true  # GPG for whistleblowing
```

**How It Works:**
1. 5 agents execute same task independently
2. Each agent produces output
3. Agents vote on each other's quality (0.0/0.5/1.0)
4. Aggregate scores (excluding self-votes)
5. If consensus >= 80%: Accept highest-voted output
6. If consensus < 80%: Terminate lowest-voted agent, retry with 4
7. Repeat until consensus or min agents (3)

**Example Vote Matrix:**
```
          Agent A  Agent B  Agent C  Agent D  Agent E
Agent A     -       0.5      1.0      0.0      0.5
Agent B    1.0       -       1.0      0.5      0.5
Agent C    1.0      0.5       -       0.0      0.5
Agent D    0.0      0.0      0.0       -       0.0
Agent E    1.0      0.5      1.0      0.5       -
─────────────────────────────────────────────────────
Scores:    0.75     0.375    0.75     0.25     0.375

Consensus: 60% (below 80% threshold)
Action: Terminate Agent D (lowest score)
Retry: Congress of 4 agents
```

**Timeline**: Month 6-7

---

### Advanced Model Routing (Month 7-9)

**Confidence-Based Fallback:**
```yaml
routing:
  small:
    model: qwen2.5-3b
    confidenceThreshold: 0.7
    fallbackTo: medium
  medium:
    model: gemini-1.5-pro
    confidenceThreshold: 0.85
    fallbackTo: large
  large:
    model: claude-sonnet-4
```

**How It Works:**
1. Small model executes task
2. Parse output: `{"answer": "...", "confidence": 0.65}`
3. If confidence < 0.7: Auto-escalate to medium
4. Track escalation rate: "12% of tasks escalated to large"

**Dynamic Cost Optimization:**
- Monitor OpenRouter real-time pricing
- If Claude Sonnet spikes 2x: Alert user, suggest Gemini
- Auto-switch if user enabled auto-optimization
- Show savings: "Switched to Gemini, saved $0.15/request"

**Timeline**: Month 7-9

---

## 🔮 Future Enhancements (Phase 3+)

See `FUTURE-FEATURES.md` for comprehensive list including:

- **Workflow Marketplace** (Month 13-15): Community-shared workflows, revenue sharing
- **Visual Workflow Editor** (Month 16-18): Drag-and-drop component assembly
- **Multi-Tenancy & RBAC** (Month 13-14): Organizations, roles, team sharing
- **CI/CD Integration** (Month 12-13): GitHub Actions, GitLab CI
- **Session Recording** (Month 16-17): VCR for agents, scrub timeline
- **Mesh Topology** (Month 8-9): Any-to-any agent communication
- **Graph Memory** (Month 11-12): Neo4j for concept relationships
- **Voice Synthesis** (Month 18-20): Audio narration of workflow progress
- **Autonomous Company** (24+ months): Self-managing agent organization

---

## 📊 Success Metrics

### MVP (18 Weeks)
- [ ] Generate .claude folder in <5 seconds
- [ ] Launch headless session in <10 seconds
- [ ] Detect stall within 30 seconds of occurrence
- [ ] Dashboard load time <2 seconds
- [ ] Real-time event latency <100ms
- [ ] RAG semantic search <200ms
- [ ] Component library: 100+ items
- [ ] Workflow templates: 10+
- [ ] Beta users: 10

### Phase 2 (Months 6-9)
- [ ] Model debates implemented + documented
- [ ] Congress voting tested with 50+ sessions
- [ ] Cost savings tracked: Target 90% reduction vs naive approach
- [ ] Session recovery success rate: >90%
- [ ] User retention: 50% weekly active users

### Long-Term (Year 1+)
- [ ] Workflow marketplace: 50+ community workflows
- [ ] Active users: 500+
- [ ] Component contributions: 20+ from community
- [ ] Enterprise pilots: 3+
- [ ] Viral content: 1M+ impressions on model debate videos

---

## ⚠️ Open Questions & Research

**Technical Unknowns:**

1. **Claude Code Session Control:**
   - Can we inject prompts to running headless sessions?
   - How does native resume work after restart?
   - What signals does it handle gracefully?
   - **Action**: Week 1 - Test headless mode, document findings

2. **Claude-Code-Proxy Log Format:**
   - Where are logs stored? (`~/.claude-proxy/requests.log`?)
   - What's the log schema?
   - Real-time tailing or polling?
   - **Action**: Week 1 - Inspect proxy installation, document schema

3. **Multi-Agent-Workflow API Compatibility:**
   - Can we extend endpoints via wrapper without forking?
   - Breaking changes in upstream updates?
   - **Action**: Week 2 - Complete codebase analysis

4. **Model Debate Implementation:**
   - How to enforce turn-taking in headless mode?
   - Store debate history in session transcript?
   - **Action**: Month 7 - Design + prototype

---

## 🎯 Critical Path

**Week 1-2**: Foundation + Component Library Seed
- Set up repo, database, submodules
- Create 25 example components (5 per category)
- Write 3 workflow templates

**Week 3-8**: Core Engine
- Workflow generator + session launcher
- Stall detection + recovery
- Component registry + smart recommendations

**Week 9-14**: Monitoring + Memory
- Integrate multi-agent-workflow
- Build custom UI overlays (30%)
- RAG memory system

**Week 15-18**: Polish + Beta
- Lifecycle management + cleanup
- Populate component library (100+ items)
- Documentation + testing
- Beta launch with 10 users

**Month 6-9**: Phase 2 - Viral Features
- Model debates (PRIORITY #1)
- Congress voting
- Advanced routing

---

## 🚀 Why This Will Go Viral

**Unique Positioning:**
- **First** visual orchestration platform for Claude Code
- **First** multi-model debate visualization
- **Only** real-time swarm monitoring with cost optimization

**Shareability:**
- Model debate videos (Claude vs GPT arguing)
- Cost savings screenshots ("$15K → $250")
- Agent hierarchy visualizations (beautiful graphs)
- Session replay time-lapses (hypnotic)

**Network Effects:**
- Component library grows with community
- Workflow marketplace creates lock-in
- Enterprise adoption validates platform

**Comparison Positioning:**
- "Zapier for AI agents"
- "Datadog for agent swarms"
- "What Cursor did for coding, Super Agent Monitor does for orchestration"

**Target Launch Strategy:**
1. MVP (Week 18): Hacker News, r/ClaudeAI, Twitter
2. Model Debates (Month 8): ProductHunt, Demo videos on Twitter
3. Marketplace (Month 15): Y Combinator application, TechCrunch pitch

---

**END OF PRD v2.0 (FINAL)**
