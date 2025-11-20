# Super Agent Monitor

**Autonomous multi-agent workflow orchestration and monitoring platform for Claude Code**

[![License: Elastic-2.0](https://img.shields.io/badge/License-Elastic--2.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](package.json)
[![Progress](https://img.shields.io/badge/MVP_Progress-80%25-brightgreen)](IMPLEMENTATION-TASKS.md)

The Super Agent Monitor transforms Claude Code from a single-session tool into an intelligent orchestration platform capable of managing autonomous agent swarms with persistent memory and real-time monitoring.

---

## 🚀 Overview

Super Agent Monitor provides:

- **🤖 Headless Execution** - Run Claude Code sessions autonomously without user interaction
- **👁️ Real-Time Monitoring** - WebSocket-based live updates with token tracking and cost calculation
- **🧠 RAG Memory System** - Semantic search over accumulated session knowledge using vector embeddings
- **🔄 Stall Detection** - Automatic detection and recovery of frozen sessions
- **🎯 Component Library** - Mix-and-match agents, skills, hooks, and scripts into custom workflows
- **📋 Workflow Templates** - Reusable configurations for common automation patterns
- **💰 Cost Tracking** - Real-time token usage and cost monitoring per session and workflow
- **📚 Cross-Session Learning** - Workflows learn from past executions to avoid repeated mistakes

---

## 📋 Quick Start

### Prerequisites

- **Node.js 18+** or **Bun 1.0+**
- **PostgreSQL 14+** with **pgvector** extension
- **OpenAI API key** (for RAG memory embeddings)
- **Claude Code CLI** installed and configured

### Installation

```bash
# Clone the repository
git clone https://github.com/aaaronmiller/super_agent_monitor.git
cd super_agent_monitor

# Backend setup
cd backend
bun install
cp ../.env.example .env
# Edit .env with your configuration

# Run database migrations
bun run db:migrate

# Start backend server
bun run dev

# Frontend setup (in new terminal)
cd ../frontend
bun install

# Start frontend dev server
bun run dev
```

The application will be available at `http://localhost:3000` with API at `http://localhost:3001`

### First Workflow

1. Open http://localhost:3000
2. Navigate to "Components" to browse available agents, skills, and hooks
3. Go to "Workflows" → "Create New Workflow"
4. Select a template (e.g., "Deep Research")
5. Click "Start Workflow" to launch autonomous execution
6. Monitor real-time progress in the "Sessions" view

---

## 🏗️ Architecture

### System Overview

```
User Browser (Vue 3 + Tailwind)
    ↓ REST API + WebSocket
Backend (Bun + Express + TypeScript)
    ├─ SessionLauncher (headless Claude Code)
    ├─ SessionMonitor (stall detection)
    ├─ MemoryIngestion (RAG embeddings)
    └─ WebSocketService (real-time streaming)
    ↓
PostgreSQL 14+ with pgvector
    ├─ Workflows & Sessions
    ├─ Events & Metrics
    └─ Vector Embeddings (1536-dim)
    ↓
Claude Code (Headless Execution)
    ↓
Anthropic API (Claude Sonnet 4)
```

### Tech Stack

**Backend:**
- Runtime: Bun
- Framework: Express + TypeScript
- Database: PostgreSQL 14+ with pgvector extension
- Vector Search: HNSW indexing for similarity search
- Embeddings: OpenAI text-embedding-3-small
- Real-time: WebSocket (ws library)

**Frontend:**
- Framework: Vue 3 Composition API + TypeScript
- State Management: Pinia
- Routing: Vue Router
- Styling: Tailwind CSS
- Real-time: WebSocket composable

**Key Services:**
- `SessionLauncher` - Spawns headless Claude Code processes, captures output, tracks costs
- `SessionMonitor` - Detects stalls (300s inactivity) and auto-restarts (max 3 retries)
- `MemoryIngestion` - Ingests tool outputs, completions, errors into vector DB
- `RAGRetrieval` - Semantic search, session context, workflow history
- `EmbeddingService` - OpenAI integration with LRU caching
- `WebSocketService` - Real-time event broadcasting to clients

---

## 🎯 Component System

Components are modular building blocks for workflows:

### Component Types

- **Agents** (`.md`) - Specialized AI personas (researcher, coder, analyzer)
- **Skills** (`.md`) - Domain knowledge and techniques (web-search, API design)
- **Hooks** (`.py`, `.sh`) - Lifecycle handlers (cost tracking, stall detection)
- **Scripts** (`.py`) - Utility scripts (URL fetch, PDF parse, GitHub API)
- **Orchestrators** (`.md`) - Coordination patterns (CEO-Worker, Star, Round-Robin)

### Component Metadata

Each component includes YAML frontmatter:

```yaml
---
name: "Research Coordinator"
category: "orchestrator"
description: "CEO-Worker pattern for complex research tasks"
tags: ["research", "coordination", "delegation"]
dependencies: ["researcher-primary"]
incompatible: []
---
```

### Current Library (30+ Components)

**Agents (10):**
- researcher-primary, web-scraper, code-reviewer, tester, analyzer
- prd-finder, file-analyzer, project-tagger, prd-rater, github-searcher

**Skills (5):**
- web-search-advanced, api-design, db-optimization, security-audit, testing-patterns

**Hooks (5):**
- cost-tracker.py, stall-detector.py, format-enforcer.sh, progress-tracker.py, session-start.py

**Scripts (5):**
- fetch-url.py, parse-pdf.py, extract-tags.py, github-api.py, scan-files.py

**Orchestrators (3):**
- research-coordinator.md (CEO-Worker), star-coordinator.md, round-robin-coordinator.md

**Workflow Templates (3):**
- deep-research.yaml, fast-coder.yaml, security-audit.yaml

---

## 🧠 RAG Memory System

The memory system enables cross-session learning through semantic search.

### How It Works

1. **Automatic Ingestion** - Tool outputs, completions, and errors are queued for ingestion
2. **Embedding Generation** - Content transformed into 1536-dimensional vectors (OpenAI)
3. **Vector Storage** - Embeddings stored in PostgreSQL with HNSW indexing
4. **Semantic Retrieval** - Natural language queries find relevant memories via cosine similarity
5. **Importance Scoring** - Automatic scoring (0-1) based on content type, length, keywords

### Memory Types

- **tool_output** - Tool execution results
- **completion** - Claude's responses
- **error** - Error messages (high importance 0.8)
- **user_input** - User instructions
- **system_message** - System-generated messages

### Search Features

- **Semantic Search** - Natural language queries
- **Session Context** - All memories from a specific session
- **Workflow History** - High-importance memories from previous runs
- **Hybrid Search** - Combines semantic + keyword matching
- **Similar Memories** - Find related entries

### Example Query

Query: "authentication errors in the login flow"

Returns semantically related memories even if they don't contain exact words, ranked by cosine similarity.

---

## 🎮 Session Management

### Headless Execution

Sessions spawn Claude Code as autonomous child processes:

```bash
claude --headless --config=/path/to/.claude --session-id=<uuid>
```

The SessionLauncher:
- Spawns child processes with headless flag
- Captures stdout/stderr in real-time
- Parses JSON events from Claude Code
- Logs all events to database
- Tracks token usage and calculates costs
- Automatically ingests important content into memory

### Real-Time Monitoring

WebSocket streaming provides live updates:

- `session:launched` - Session started
- `session:tool_use` - Tool executed (with tool name and output)
- `session:error` - Error occurred
- `session:stalled` - No activity for 300 seconds
- `session:restarted` - Auto-recovery triggered
- `session:exit` - Session completed or failed

### Cost Tracking

Costs calculated using Claude Sonnet 4 pricing:
- **Input tokens**: $3.00 per million tokens
- **Output tokens**: $15.00 per million tokens

Real-time display shows:
- Input token count and cost
- Output token count and cost
- Total cost accumulation
- Cost per session, workflow, and across all sessions

### Stall Detection & Auto-Recovery

SessionMonitor checks every 60 seconds for inactive sessions:

1. **Detection**: No activity for 300+ seconds
2. **Alert**: Session marked as `stalled`
3. **Recovery**: Auto-restart triggered (if retries < 3)
4. **Retry Limit**: After 3 failures, marked as `failed`
5. **Notification**: Events broadcast via WebSocket

---

## 📊 API Endpoints

### Components

- `GET /api/components` - List all components with filtering
- `GET /api/components/:id` - Get component details
- `POST /api/components/recommendations` - Get smart recommendations based on selected components

### Workflows

- `GET /api/workflows` - List all workflows
- `POST /api/workflows` - Create new workflow
- `GET /api/workflows/:id` - Get workflow details
- `PATCH /api/workflows/:id` - Update workflow
- `DELETE /api/workflows/:id` - Delete workflow

### Sessions

- `GET /api/sessions` - List sessions with filtering
- `POST /api/sessions` - Create new session
- `GET /api/sessions/:id` - Get session details
- `POST /api/sessions/:id/start` - Start pending session
- `POST /api/sessions/:id/stop` - Stop active session
- `POST /api/sessions/:id/restart` - Restart session (creates new session)
- `GET /api/sessions/:id/status` - Get real-time status with live data
- `GET /api/sessions/:id/events` - Get event log
- `GET /api/sessions/:id/metrics` - Get session metrics

### Memory

- `POST /api/memory/ingest` - Manually ingest memory entry
- `POST /api/memory/retrieve` - Semantic search with filters
- `GET /api/memory/session/:id/context` - Get session memories
- `GET /api/memory/workflow/:id/history` - Get workflow history
- `GET /api/memory/:id` - Get memory details with access stats
- `GET /api/memory/:id/similar` - Find similar memories
- `POST /api/memory/collections` - Create memory collection
- `POST /api/memory/collections/:id/entries` - Add entries to collection
- `GET /api/memory/collections/:id/stats` - Get collection statistics
- `GET /api/memory/workflow/:id/stats` - Get workflow memory statistics
- `POST /api/memory/prune` - Prune old memories (retention policy)

### Monitor

- `GET /api/sessions/monitor/stats` - Get monitor statistics
- `PUT /api/sessions/monitor/config` - Update monitor configuration
- `POST /api/sessions/monitor/start` - Start session monitor
- `POST /api/sessions/monitor/stop` - Stop session monitor

---

## ⚙️ Configuration

### Environment Variables

See `.env.example` for all available options.

**Required:**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/super_agent_monitor

# OpenAI (for RAG embeddings)
OPENAI_API_KEY=sk-...

# Server
PORT=3001
NODE_ENV=development
```

**Optional:**
```env
# Embedding Configuration
EMBEDDING_MODEL=text-embedding-3-small

# Session Monitor
STALL_DETECTION_SECONDS=300
MONITOR_CHECK_INTERVAL_SECONDS=60
MAX_SESSION_RETRIES=3

# WebSocket
WS_PATH=/ws
```

---

## 🗄️ Database

### Setup PostgreSQL with pgvector

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Run Migrations

```bash
cd backend
bun run db:migrate
```

### Migration Commands

```bash
bun run db:migrate          # Apply all pending migrations
bun run db:migrate:status   # Check migration status
bun run db:migrate:rollback # Rollback last migration
```

### Schema Overview

**Core Tables:**
- `workflows` - Workflow configurations
- `sessions` - Session instances
- `session_events` - Event log
- `session_metrics` - Performance metrics

**Memory Tables:**
- `memory_entries` - Vector embeddings and content (1536-dim)
- `memory_collections` - Grouped memories
- `memory_access_log` - Usage analytics
- `schema_migrations` - Migration tracking

---

## 🚀 Development

### Backend Development

```bash
cd backend
bun run dev  # Hot reload enabled
```

### Frontend Development

```bash
cd frontend
bun run dev  # Vite dev server with hot reload
```

### Running Tests

```bash
# Backend
cd backend
bun test

# Frontend
cd frontend
bun test
```

---

## 📈 Project Status

**Current Phase:** Phase 2 Complete (80% toward MVP)

**Completed:**
- ✅ Phase 0: Component library, licensing, project setup
- ✅ Phase 1: Backend API + Frontend UI
- ✅ Phase 2 Week 1: Headless sessions, monitoring, WebSocket
- ✅ Phase 2 Week 2-3: RAG memory system with full UI
- ✅ Infrastructure: Database migrations, deployment tools

**Remaining (20% to MVP):**
- Documentation and deployment guides
- Docker Compose for production deployment
- End-to-end testing and polish
- Performance optimization

**Post-MVP Features:**
- Cost analytics dashboard with charts
- Session replay for debugging
- Multi-user support with access control
- Workflow marketplace
- Visual workflow editor

---

## 📄 License

This project is licensed under the **Elastic License 2.0**.

You may use, copy, modify, and distribute the software for any purpose, EXCEPT:
- You may NOT provide the software to third parties as a hosted or managed service
- You may NOT circumvent license key functionality or remove/obscure licensing notices

See [LICENSE](LICENSE) for complete terms.

### Why Elastic License 2.0?

The Elastic License 2.0 allows:
- ✅ Internal enterprise use
- ✅ Modification and customization
- ✅ Source code inspection
- ✅ Community contributions

But prevents:
- ❌ Offering as competing SaaS
- ❌ Selling hosted versions without permission

This protects the project's sustainability while keeping source available.

---

## 🤝 Contributing

Contributions are welcome! Areas where we need help:

- Adding components to the library (agents, skills, hooks)
- Improving workflow templates
- Documentation enhancements
- Bug reports and feature requests
- Performance optimization
- Testing and QA

Please open an issue before starting major work.

---

## 📚 Documentation

- [PRD-FINAL.md](PRD-FINAL.md) - Complete product requirements
- [IMPLEMENTATION-TASKS.md](IMPLEMENTATION-TASKS.md) - Task breakdown and progress
- [backend/database/README.md](backend/database/README.md) - Database setup and migrations
- [NOTICE](NOTICE) - Third-party attributions

---

## 🙋 FAQ

**Q: How is this different from running Claude Code manually?**
A: We add autonomous execution, real-time monitoring, cost tracking, persistent memory, and stall recovery.

**Q: Does this replace Claude Code?**
A: No, it orchestrates Claude Code. You still need Claude Code CLI installed.

**Q: What about costs?**
A: You pay for Anthropic API usage. The platform itself is self-hosted and free (Elastic License 2.0).

**Q: Can I use different models?**
A: Yes, Claude Code supports model selection. The platform works with any model Claude Code supports.

**Q: How does the memory system help?**
A: It prevents repeated mistakes. If a session solves a problem, future sessions can search that knowledge.

**Q: Is my data private?**
A: Yes, everything runs on your infrastructure. Embeddings go to OpenAI but the memory stays in your database.

---

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/aaaronmiller/super_agent_monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/aaaronmiller/super_agent_monitor/discussions)

---

## 🙏 Acknowledgments

- Built on [Claude Code](https://claude.ai/code) by Anthropic
- Uses [pgvector](https://github.com/pgvector/pgvector) for vector similarity search
- Inspired by multi-agent workflow patterns

---

**Built for the AI agent community**

*"Making autonomous agent orchestration accessible and intelligent"*
