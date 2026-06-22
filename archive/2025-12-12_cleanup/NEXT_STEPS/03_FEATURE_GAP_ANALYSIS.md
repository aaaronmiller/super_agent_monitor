# Feature Gap Analysis: Old PRD vs Current Implementation

## Source Document
`docs/amalgam/markdown_agents/prd.md` - Super Agent Monitor PRD v1.0 (43KB, 751 lines)

---

## PRD Feature Matrix

### 3.1 Workflow Management System

| Feature | PRD Requirement | Current Status | Gap |
|:--------|:---------------|:---------------|:----|
| Workflow JSON/YAML schema | FR-WF-01 | ❓ Check `workflows/` | |
| Pre-built templates (10-20) | FR-WF-02 | ❓ | Count templates |
| User-saved custom workflows | FR-WF-02 | ❓ | Check persistence |
| Ad-hoc component mixing | FR-WF-02 | ❓ | Check UI |
| Workflow versioning | FR-WF-03 | ❓ | Verify |
| Export .workflow files | FR-WF-04 | ❓ | |
| Import with conflict resolution | FR-WF-05 | ❓ | |
| Generator (<5s) | NFR-WG-01 | ❓ | Benchmark |

### 3.2 Component Library System

| Feature | PRD Requirement | Current Status | Gap |
|:--------|:---------------|:---------------|:----|
| 20-30 Agents | FR-CR | ✅ 33 agents | Exceeds |
| 20-30 Skills | FR-CR | ✅ 44 skills | Exceeds |
| 10-15 Hooks | FR-CR | ✅ 29 hooks | Exceeds |
| 20-30 Scripts | FR-CR | ❓ | Count scripts |
| 10-15 MCP Tools | FR-CR | ❓ | Count MCP |
| Component discovery | FR-CR-03 | ❓ | Verify |
| Component search | FR-CR-05 | ❓ | Check API |
| Smart recommendations | FR-SCR | ❓ | Check implementation |

### 3.3 Session Management

| Feature | PRD Requirement | Current Status | Gap |
|:--------|:---------------|:---------------|:----|
| Headless launcher | FR-SL-01 | ✅ `deploy.sh` | |
| Claude Code detection | FR-SL-05 | ❓ | |
| Session database | FR-SL-04 | ✅ SQLite | |
| Stall detection (300s) | FR-SD-02 | ❓ | Check implementation |
| Kick prompt injection | FR-SD-03.1 | ❓ | |
| Graceful restart | FR-SD-03.2 | ❓ | |
| Max retries | FR-SD-04 | ❓ | |

### 3.4 Memory & RAG System

| Feature | PRD Requirement | Current Status | Gap |
|:--------|:---------------|:---------------|:----|
| Vector store | FR-VM-01 | ❓ | Check pgvector |
| Embedding service | FR-VM-03 | ❓ | |
| Semantic search | FR-VM-05 | ❓ | |
| Context injection | FR-CI-01 | ❓ | |
| Learning capture | FR-LC-01 | ❓ | |

### 3.5 Workflow Lifecycle

| Feature | PRD Requirement | Current Status | Gap |
|:--------|:---------------|:---------------|:----|
| Age-based cleanup | FR-CL-02.1 | ❓ | |
| Size-based cleanup | FR-CL-02.2 | ❓ | |
| Pre-cleanup notification | FR-CL-04 | ❓ | |
| Export/Import | FR-WS | ❓ | |

---

## PRD Roadmap vs Current State

| Phase | PRD Target | Weeks | Current Status |
|:------|:-----------|:------|:---------------|
| Phase 0: Foundation | Submodules, schema, examples | 1-2 | ✅ Complete |
| Phase 1: Workflow Generator | Validator, generator, registry | 3-4 | ⚠️ Partial |
| Phase 2: Session Management | Launcher, stall detection | 5-7 | ⚠️ Partial |
| Phase 3: Monitoring Dashboard | MAW integration, overlays | 8-10 | ✅ Disler frontend |
| Phase 4: RAG Memory | Vector DB, injection | 11-13 | ❓ Unknown |
| Phase 5: Lifecycle | Cleanup, export/import | 14-15 | ❓ Unknown |
| Phase 6: Polish | Full library, docs | 16-18 | ⚠️ Ongoing |

---

## Component Category Targets (PRD Section 3.2.1)

| Category | PRD Target | Current | Status |
|:---------|:-----------|:--------|:-------|
| Agents | 20-30 | 33 | ✅ Exceeds |
| Skills | 20-30 | 44 | ✅ Exceeds |
| Hooks | 10-15 | 29 | ✅ Exceeds |
| Scripts | 20-30 | ❓ | Audit needed |
| MCP Tools | 10-15 | ❓ | Audit needed |
| Orchestrator Prompts | 5-10 | ❓ | Audit needed |
| Subagent Prompts | 10-15 | ❓ | Audit needed |

---

## Technology Stack Alignment

| Layer | PRD Spec | Current | Status |
|:------|:---------|:--------|:-------|
| Frontend | Vue 3 + TypeScript | Vue 3 | ✅ |
| UI Framework | Ant Design / Element Plus | ❓ | Check |
| Backend | Bun (Node compatible) | Node/Bun | ✅ |
| Database | SQLite → PostgreSQL | SQLite | ✅ |
| Vector DB | pgvector | ❓ | Verify |
| Real-time | SSE | SSE | ✅ |
| Container | Docker Compose | ✅ | Exists |

---

## Key Open Questions from PRD (Section 8)

### Technical Unknowns
1. [x] Claude Code session control - `deploy.sh` exists
2. [ ] Multi-agent-workflow modifications - Needs analysis
3. [ ] Claude-code-proxy data access - Log location?
4. [ ] Component template variables - `{{PROJECT_NAME}}` handling

### Product Decisions (PRD Made)
1. ✅ Semantic versioning for workflows
2. ✅ Unique names for components
3. ✅ Session-only memory default
4. ✅ In-app cleanup notifications

---

## Action Items

1. [ ] Audit `scripts/` directory - count against target
2. [ ] Audit MCP tools - count against target
3. [ ] Check RAG/pgvector implementation
4. [ ] Verify stall detection implementation
5. [ ] Test workflow export/import
6. [ ] Document current vs target feature state
