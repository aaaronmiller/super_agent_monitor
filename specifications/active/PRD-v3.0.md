# **Super Agent Monitor PRD v3.0**
## **Autonomous Multi-Agent Workflow Orchestration Platform**

**Version:** 3.0
**Date:** 2025-12-12
**Status:** Implementation Complete (Phase 1) / Active Development
**Classification:** Internal - Authoritative Specification

---

## 📋 Executive Summary

Super Agent Monitor is a **workflow orchestration and monitoring platform** for autonomous Claude Code agent swarms. It provides:

1. **Pre-built Toolbox** (`.claude/`): 245 portable components (agents, skills, hooks, commands)
2. **Dashboard UI** (Disler): Real-time monitoring via external/disler
3. **Model Routing** (claude-code-proxy): Multi-model orchestration
4. **CLI Automation** (`sam.py`): Programmatic workflow control

### Architectural Philosophy

| Layer | Contents | Portability |
|:------|:---------|:------------|
| **Toolbox** (`.claude/`) | Agents, skills, hooks, commands | **Copy directly** to any project |
| **Dashboard** (`external/disler/`) | Vue UI + Bun server | External dependency |
| **Routing** (`external/claude-code-proxy/`) | Model proxy | Global install |
| **Backend** (`backend/`) | Custom FastAPI services | Recreate from spec |
| **Entry Points** | `start.sh`, `deploy.sh` | Recreate from spec |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │         Disler Dashboard (external/disler/apps/client)       │    │
│  │  - Real-time event stream     - Session monitoring           │    │
│  │  - Agent hierarchy tree       - Cost tracking                │    │
│  └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ REST API + SSE (:3001)
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       BACKEND SERVICES                               │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐    │
│  │ Disler Server            │  │ Custom Backend (backend/)     │    │
│  │ external/disler/apps/    │  │ - routes/   - services/       │    │
│  │ server (:3001)           │  │ - db/       - scripts/        │    │
│  └──────────────────────────┘  └──────────────────────────────┘    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
┌────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│ .claude/       │  │ Claude Code CLI  │  │ claude-code-proxy    │
│ TOOLBOX        │  │ (Headless Mode)  │  │ (Model Routing)      │
│ 245 components │  │                  │  │ external/claude-     │
│ agents/skills/ │  │ ANTHROPIC_BASE_  │  │ code-proxy           │
│ hooks/commands │  │ URL → proxy      │  │                      │
└────────────────┘  └────────┬─────────┘  └──────────┬───────────┘
                             │                       │
                             └───────────┬───────────┘
                                         ▼
                              ┌──────────────────────┐
                              │   LLM Providers      │
                              │ Claude / GPT / Gemini│
                              │ Ollama / vLLM        │
                              └──────────────────────┘
```

---

## 📦 Component Inventory

### The Toolbox (`.claude/`) — PORTABLE

> **These files are copied verbatim to any deployment. They are NOT recreated from this PRD.**

| Directory | Count | Purpose |
|:----------|:------|:--------|
| `.claude/agents/` | 57 | Agent personality definitions |
| `.claude/skills/` | 51 | Capability/skill protocols |
| `.claude/hooks/` | 22 | Event handlers (budget, session, etc.) |
| `.claude/commands/` | 13 | Slash commands (/cleanup, /validate, etc.) |
| `.claude/scripts/` | 11 | Automation (sam.py, phylogeny.py, etc.) |
| `.claude/tools/` | 10 | MCP tool scripts (brave-search, fetch, etc.) |
| `.claude/swarms/` | 12 dirs | Pre-configured swarm setups |
| `.claude/rag/` | 3 | RAG pipeline components |
| `.claude/templates/` | varies | Agent templates |

**Total: ~245 files**

### Key Skills (Validated)

| Skill | Purpose |
|:------|:--------|
| `project-gardener.md` | Non-destructive file cleanup with phylogeny |
| `file-phylogeny.md` | Track file evolution and relationships |
| `adversarial-council.md` | 8-10 persona validation protocol |
| `anti-lazy.md` | Enforce exhaustive completeness |
| `codebase-resuscitation.md` | Diagnose and repair broken projects |

---

## 🔌 External Dependencies

### 1. Disler (Dashboard)

**Location:** `external/disler/`
**Purpose:** Real-time monitoring dashboard

```
external/disler/
├── apps/
│   ├── client/     # Vue 3 frontend (:5173)
│   └── server/     # Bun backend (:3001)
├── CLAUDE.md       # Agent instructions
└── README.md
```

**Integration:**
- `start.sh` launches both client and server
- Apply patches from `patches/` after cloning

### 2. claude-code-proxy (Model Routing)

**Location:** `external/claude-code-proxy/`
**Purpose:** Route requests to different LLM providers, track tokens/costs

**Usage:**
```bash
export ANTHROPIC_BASE_URL="http://localhost:8082"
# Claude Code now routes through proxy
```

### 3. Other Subprojects

| Subproject | Purpose |
|:-----------|:--------|
| `agent-sandbox-skill/` | Sandbox execution patterns |
| `agent-sandboxes/` | Execution environments |
| `beyond-mcp/` | Alternative tool protocols |
| `markdown_agents/` | Agent format reference |

---

## 🚀 Entry Points (RECREATE FROM SPEC)

### start.sh

```bash
#!/usr/bin/env bash
# Start all Super Agent Monitor services

DISLER_DIR="$SCRIPT_DIR/external/disler"

# Start Disler server
cd "$DISLER_DIR/apps/server"
bun install --silent
bun run src/index.ts &

# Start Disler client  
cd "$DISLER_DIR/apps/client"
bun install --silent
bun run dev &

# Optional: Start proxy
if [[ "$1" == "--proxy" ]]; then
    cd "$PROXY_DIR" && bun run start &
fi
```

### deploy.sh

Deploys agent configuration to target directory:
```bash
# Copy .claude/ toolbox to target
cp -r .claude/ "$TARGET_DIR/"
```

---

## 📁 Project Structure (Clean)

```
super_agent_monitor/
├── .claude/                    # 🛠️ TOOLBOX (245 files) - PORTABLE
│   ├── agents/                 # 57 agent definitions
│   ├── commands/               # 13 slash commands
│   ├── hooks/                  # 22 event handlers
│   ├── rag/                    # RAG pipeline
│   ├── scripts/                # sam.py, phylogeny.py, etc.
│   ├── skills/                 # 51 skill protocols
│   ├── swarms/                 # 12 swarm configs
│   ├── templates/              # Agent templates
│   └── tools/                  # MCP tools
│
├── backend/                    # Custom API services
│   ├── db/                     # Database layer
│   ├── routes/                 # API endpoints
│   ├── services/               # Business logic
│   └── scripts/                # Utility scripts
│
├── external/                   # External dependencies (6 subprojects)
│   ├── disler/                 # Dashboard UI
│   ├── claude-code-proxy/      # Model routing
│   ├── agent-sandbox-skill/
│   ├── agent-sandboxes/
│   ├── beyond-mcp/
│   └── markdown_agents/
│
├── workflows/                  # YAML workflow definitions
│   ├── deep-research.yaml
│   ├── fast-coder.yaml
│   └── security-audit.yaml
│
├── patches/                    # Patches for external deps
│   └── 001-vibevoice-tts.patch
│
├── archive/                    # Archived files (not deleted)
│   └── 2025-12-12_*/
│
├── tests/                      # Integration tests
├── docs/                       # Active documentation
│
├── start.sh                    # Launch all services
├── deploy.sh                   # Deploy agent to target
├── docker-compose.yml          # Container orchestration
├── Dockerfile                  # Build instructions
├── README.md                   # Project documentation
└── .lineage.json               # File phylogeny data
```

---

## 🔧 CLI Interface

### Main Entry: `sam.py`

```bash
# Show system status
python .claude/scripts/sam.py --status

# Spawn an agent
python .claude/scripts/sam.py spawn --agent researcher-primary

# Deploy a swarm
python .claude/scripts/sam.py swarm --deploy deep-research

# Run phylogeny scan
python .claude/scripts/phylogeny.py scan
```

---

## 🧪 Verification

### Integration Tests

```bash
cd tests/
python test_prd_integration.py
```

### Health Checks

```bash
# Verify toolbox
python .claude/scripts/sam.py --status
# Expected: 49 skills, 78 agents, 12 swarms

# Verify Disler
curl http://localhost:3001/health

# Verify lineage
python .claude/scripts/phylogeny.py show README.md
```

---

## 📊 Component Statistics

| Category | Count |
|:---------|:------|
| Agents | 57 |
| Skills | 51 |
| Hooks | 22 |
| Commands | 13 |
| Scripts | 11 |
| Tools | 10 |
| Swarms | 12 |
| **Total Toolbox Files** | **~245** |

---

## 🔄 Recreation Instructions

To recreate this project from scratch:

1. **Clone repository**
2. **Copy `.claude/` toolbox** (no modification needed)
3. **Initialize external dependencies:**
   ```bash
   git submodule update --init --recursive
   # OR clone each external/ project manually
   ```
4. **Apply patches:**
   ```bash
   bash .claude/scripts/apply-patches.sh
   ```
5. **Install dependencies:**
   ```bash
   cd external/disler/apps/server && bun install
   cd external/disler/apps/client && bun install
   ```
6. **Start services:**
   ```bash
   ./start.sh
   ```

---

## 📝 Change Log

| Version | Date | Changes |
|:--------|:-----|:--------|
| v2.0 | 2025-11-19 | Original PRD (multi-agent-workflow reference) |
| v3.0 | 2025-12-12 | Reorganized: .claude/ toolbox, external/ deps, removed redundant frontend/, added phylogeny |

---

**END OF PRD v3.0**
