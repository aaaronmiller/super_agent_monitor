I want a project that uses Claude code in a headless mode or together with agents and the claude.md file in an orchestration mode to deploy headless instances of Claud Code to perform auditing on a folder full of markdown files and perform analysis as in indicated by the user.

The user will say something like look at all the files and find all the ones that are PRD files and find all the files that are related to those files. And then the program will make a scratch pad file where they'll analyze each project file and write a quick summary of it in the markdown file sketchpad and then based on that they'll go back and determine what projects they're looking for.ct is identified, they'll then know that that's a project they should be looking for and so they'll maybe flag with different hashtag markers for use those as tags to indicate which projects are associated with which files, as certain files, even if they don't mention a project, might be obviously relevant to a project given the contents of the file, although it's gonna be need to be termined on an individual. basis.

Doesn't need to be exactly perfect, but as close to as perfect as we can get is the goal here. And just move through the projects in an iterative and logical manner is the goal. And then finally produce a consolidated list of all the PRD files along with their a rating of how good they are and then the user could then send another prompt and go back and look at all those PRD files and then do an analysis of each one, how to improve it.

It would look for other GitHub repos that perform the same feet the same function, see what they do, if there's other features that could be implemented, it would do so. You know know, I like not writing this tool from scratch if it's already written, you know, if there's other projects doing what we want it to do, then decide if we've got actual unique elements in o'surs.

If there if there's j if we are just copying something that's already been done then just link us to that project if it really is superior in every way. But if we can improve it with some of our ideas then that's what we wanna want do to but do, but we can use that project as a baseline.

So first goal will be to analyze all the files in the the folder, and then the second goal will be to analyze the files just in GitHub in general, the other repos that might be able to be useful in improving the PRD files to build bring them to an optimal state. so each of these tasks is gonna be configured as a dot clawed either a plug-in, which I think is just a combination of all the stuff that's inside a dot claude folder like the hooks, skills, skill documents, agent folder, and scripts and mcp tools along with a claude.md prompt and maybe a sess settings.json file.

We need to put the s orchestration logic in the claude.md file because we can't have agents deploy other sub-agents. So each individual Claude Code session is a s warm architecture multi-agent or orchestration system in itself and it can deploy subagents to automate and accelerate the analysis of all the files. that I want to be analyzing in the first phase of this project to give you an example of the scope that this will be used on.

It should have a nice little u web user interface to deploy this and allow for the selection of the files or the folders, either f full folders or individual files from the folder, and then also to set the system prompts and configurations and then also to define the template or the the plugin formats and then select which plugin or w they want to use with which session and deploy that way. progress meter would be cool as well. see the referenced projects for information on the multi agent workflow interface that might be good for something like this. though so we don't want to spend too much time on that if possible.

Just use the existing setup as it is, modify it slightly for our needs, but focus on the agent files and their function because that will eventually be imported into a more complex agent monitoring s solution that uses the same methodology the, the combination of the two projects and Claude Code to deploy agents, but it's a general format project rather than what I want you to do is more build these specific plug-in or agent orchestration layers so that they f perform a single task, which I already said was to analyze all the files and f pull out the workflows and then analyze the workflows and improve 'em based on the web stuff.

And when you're pulling out the workflows, you're also pulling out files that are similar to the workflows. So when you find a workflow, you t give it a tag, then you tag the that file on the scratch pad full folder or scratch pad file, and then now you know in your memory that you're looking for that project, so then you as you're reading all the files you, you give prior anytime you find something that's links to one of the projects that you're already looking for, you know to check it out.

And so you can set your subagents out with that system prompt information because you can deploy a clawed code headless instance with a s user prompt when you deploy it, which is how that would probably be done best. You should preferentially sort the markdown files in the folder for the ones that say PRD or what means the I can't even remember what it is right now.

But yeah, look for those ones first. So it's not all of them are labeled, but a lot but a of lot them are of them are and that way you can get a head start without having to reassess files later on when you 'cause you won't know to be tagging projects that are useful for other projects until you've I d identified all the projects.

So m and you may need to go through the whole list twice, first time to identify the projects and the second time to tag useful files for said projects. But you can make some of the work less on that second pass by iteratively getting better at tagging those as you go through it, if that makes sense.

Turn this concept into a PRD file and create the project. Like I said, focus on the specific tasks that I outlined, but also make it functional in a generalistic form, as I described with those other projects and we'll go from there.     https://github.com/apolopena/multi-agent-workflow

https://github.com/aaaronmiller/claude-code-proxy   this is the project that I will be porting your Claude plugins/agents (not sure terminology yet) into:  <start other project prd> Product Requirements Document: Super Agent Monitor
Autonomous Multi-Agent Workflow Management & Monitoring Platform
Version: 1.0 Date: 2025-11-19 Status: Pre-Development - Architectural Design Phase Classification: Internal - Implementation Ready

1. Executive Summary
Super Agent Monitor is a workflow management and monitoring platform for autonomous, headless Claude Code agent swarms. The system enables users to configure, launch, monitor, and manage complex multi-agent workflows through an intuitive dashboard interface, eliminating manual .claude folder configuration and providing real-time observability of autonomous agent operations.
Core Value Propositions
1. One-Click Workflow Deployment: Select from pre-built workflows or mix-and-match components to instantly create configured agent environments
2. Autonomous Operation: Headless Claude Code sessions run without user interaction, monitored and auto-recovered when stalled
3. Component Library: 20-30 pre-configured agents, skills, hooks, and scripts ready for immediate use
4. Production Monitoring: Real-time dashboard showing API activity, token usage, agent coordination, and system health
5. Workflow Portability: Share and import complete workflow configurations across users and teams
Reference Architecture
The platform builds upon two proven open-source projects:
* multi-agent-workflow (github.com/apolopena/multi-agent-workflow): Monitoring dashboard, hooks system, event tracking → Used as foundation, 70% retained with 30% overlay
* claude-code-proxy (globally installed): API interception, token tracking, model routing → Leveraged as-installed, data consumed for monitoring
MVP Strategy: Copy reference implementations verbatim initially, then iteratively enhance with custom features while maintaining update compatibility through git submodules.

2. System Architecture Overview
High-Level Component Diagram
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
└────────────┬────────────────────────────────────────────────┘
             │
     ┌───────┴────────┐
     ↓                ↓
┌──────────────┐  ┌──────────────────────────────┐
│  RAG Memory  │  │   Temp Workflow Folders      │
│  (pgvector)  │  │  .super_agent_monitor/       │
│              │  │    workflows/{id}/.claude/   │
└──────────────┘  └──────────────────────────────┘
                              ↓
                  ┌──────────────────────┐
                  │  Claude Code Proxy   │  THIS IS ACTUALLY DOWN THERRE!!
                  │  (Global Install)    │
                  └──────────┬───────────┘
                             ↓
                  ┌──────────────────────┐
                  │  Claude Code CLI     │
                  │  (Headless Mode)     │
                  └──────────┬───────────┘
                             ↓
                              |                         ┌──────────────────────┐
                              ——————— │  Claude Code Proxy   │
                              |                          │  (Global Install)    │.         ACTUALLY HERE!!!!!
                              ↓                         └──────────┬───────────
                  ┌──────────────────────┐
                  │   Anthropic API      │
                  └──────────────────────┘
Key Architectural Decisions
Decision 1: Git Submodules for Reference Repos
* Rationale: Maintain update compatibility while enabling local modifications
* Implementation:
    * external/multi-agent-workflow/ as submodule
    * Wrapper API layer for extensions
    * Upstream updates via git submodule update --remote
Decision 2: Temporary Workflow Folders
* Rationale: Isolated environments prevent configuration conflicts
* Location: .super_agent_monitor/workflows/{workflow-id}/.claude/
* Lifecycle: Auto-cleanup after 30 days inactive OR 1GB storage threshold
Decision 3: Headless Autonomous Operation
* Rationale: User monitors but doesn't interact during execution
* Implementation: claude --headless --workflow-id={id} with session monitoring
* Recovery: Auto-kick stalled sessions via prompt injection or graceful restart
Decision 4: Component-Based Configuration
* Rationale: Mix-and-match approach scales better than monolithic templates
* Library Size: 20-30 items per category (agents, skills, hooks, scripts)
* Smart Recommendations: UI suggests compatible components based on selections
Decision 5: RAG Memory System
* Rationale: Persistent learning across workflow executions
* Storage: pgvector for semantic search + SQLite for structured metadata
* Integration: Auto-inject relevant context into orchestrator prompts

3. Core Features & Requirements
3.1 Workflow Management System
3.1.1 Workflow Definition Schema
Functional Requirements:
* FR-WF-01: Workflows defined as JSON/YAML with metadata, components, orchestrator config, and lifecycle rules
* FR-WF-02: Support three workflow sources:
    1. Pre-built templates (10-20 shipped defaults)
    2. User-saved custom workflows
    3. Ad-hoc component mixing (save optional)
* FR-WF-03: Workflow versioning with semantic versions (v1.0.0)
* FR-WF-04: Export workflows as .workflow files (JSON + bundled component files)
* FR-WF-05: Import workflows with conflict resolution (overwrite/merge/skip)
* FR-WF-06: Workflow metadata includes: name, description, author, tags, created/modified dates
Schema Example:
id: deep-research-v1
name: Deep Research Agent
description: Multi-agent research workflow with web scraping and synthesis
version: 1.0.0
author: system
tags: [research, autonomous, web-scraping]

orchestrator:
  model: claude-sonnet-4
  systemPrompt: orchestrators/research-coordinator.md
  thinkingBudget: 10000
  temperature: 0.7

components:
  agents:
    - researcher-primary
    - web-scraper
    - citation-analyzer
    - synthesizer
  skills:
    - web-search-advanced
    - academic-citation
    - markdown-formatting
  hooks:
    - session-start-init
    - cost-tracker
    - stall-detector
  scripts:
    - fetch-url.py
    - parse-pdf.py
    - extract-citations.py
  mcp:
    - browser-automation
    - google-scholar

memory:
  enabled: true
  persistence: session
  rag: true
  retrievalK: 5

lifecycle:
  haltDetectionSeconds: 300
  autoRestart: true
  maxRetries: 3
  kickPrompt: "Continue with your research task. Review progress and proceed with next logical step."
3.1.2 Workflow Generator
Functional Requirements:
* FR-WG-01: Generate temporary .claude/ folder from workflow definition
* FR-WG-02: Populate folders:
    * agents/*.md - Selected subagent definitions
    * skills/*/SKILL.md - Selected skill packages
    * hooks/*.py - Selected hook scripts
    * scripts/*.py - Selected utility scripts
    * settings.json - Orchestrator configuration
    * CLAUDE.md - Project orchestration prompt
* FR-WG-03: Validate component compatibility (check dependencies)
* FR-WG-04: Generate workflow-manifest.json with resolved paths and timestamps
* FR-WG-05: Support template variables in components (e.g., {{PROJECT_NAME}})
Non-Functional Requirements:
* NFR-WG-01: Generation completes in <5 seconds
* NFR-WG-02: Atomic operation (all-or-nothing)
* NFR-WG-03: Validation errors return specific missing dependencies

3.2 Component Library System
3.2.1 Component Registry
Component Categories:
1. Agents (20-30 items): Specialized subagents with defined roles
2. Skills (20-30 items): Domain knowledge packages
3. Hooks (10-15 items): Event-driven automation scripts
4. Scripts (20-30 items): Utility functions replacing MCP
5. MCP Tools (10-15 items): Legacy Model Context Protocol integrations
6. Orchestrator Prompts (5-10 items): System-level coordination strategies
7. Subagent Prompts (10-15 items): Agent-specific behavior templates
Functional Requirements:
* FR-CR-01: Each component stored as markdown file with YAML frontmatter
* FR-CR-02: Component metadata includes:
    * name: Unique identifier
    * displayName: Human-readable name
    * description: Purpose and use cases
    * category: Agent/Skill/Hook/Script/MCP/Orchestrator/Subagent
    * tags: Searchable keywords
    * dependencies: Required other components
    * incompatibilities: Conflicting components
    * model: Recommended Claude model (Haiku/Sonnet/Opus)
    * tools: Required tool permissions
* FR-CR-03: Component discovery via filesystem scan on startup
* FR-CR-04: Component validation on registration (schema check)
* FR-CR-05: Component search by name, tags, category
* FR-CR-06: Component preview in UI (rendered markdown)
Example Component (Agent):
---
name: researcher-primary
displayName: Primary Research Agent
description: Lead researcher coordinating information gathering and synthesis
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

1. **Task Decomposition**: Break complex research questions into subtasks
2. **Delegation**: Assign subtasks to specialist agents (web-scraper, citation-analyzer)
3. **Synthesis**: Integrate findings into coherent research output
4. **Quality Control**: Verify sources and fact-check claims

## Workflow

When given a research task:
1. Analyze scope and identify information needs
2. Delegate to specialist agents via explicit @mentions
3. Monitor progress through agent outputs
4. Synthesize findings into structured markdown report
5. Generate citations in APA format

## Constraints

- NEVER fabricate sources - only cite verified URLs
- ALWAYS cross-reference facts across 3+ sources
- Maintain research log in `research-log.md`
3.2.2 Smart Component Recommendations
Functional Requirements:
* FR-SCR-01: When user selects components, suggest compatible additions
* FR-SCR-02: Recommendation algorithm based on:
    * Dependency requirements (required components)
    * Common pairings (frequently used together)
    * Category balance (e.g., 3 agents → suggest 2-3 skills)
* FR-SCR-03: Highlight incompatibilities in real-time
* FR-SCR-04: Pre-built workflow templates as starting points (editable)

3.3 Session Management & Monitoring
3.3.1 Headless Session Launcher
Functional Requirements:
* FR-SL-01: Launch Claude Code in headless mode: claude --headless --config={path}
* FR-SL-02: Configure claude-code-proxy to monitor session
* FR-SL-03: Initialize session with workflow's CLAUDE.md prompt
* FR-SL-04: Create session record in database with:
    * Session ID, Workflow ID, Start time, Status (running/stalled/completed/failed)
* FR-SL-05: Detect if Claude Code installed, prompt installation if missing
* FR-SL-06: Auto-install Claude Code if user approves (via curl install script)
Implementation Details:
# Session Launch Command
claude --headless \
  --config=.super_agent_monitor/workflows/{workflow-id}/.claude \
  --output-format=json \
  --session-id={session-id}
3.3.2 Stall Detection & Recovery
Problem: Headless sessions may halt without error (waiting for user input, context overload, rate limits)
Functional Requirements:
* FR-SD-01: Monitor claude-code-proxy logs for API activity timestamps
* FR-SD-02: Detect stall: No API requests for configurable period (default 300s)
* FR-SD-03: Recovery strategy (configurable per workflow):
    1. Kick Attempt: Inject prompt via Claude Code session API (if available)
    2. Graceful Restart: Send SIGTERM, wait for state save, relaunch with resume
    3. Force Restart: Send SIGKILL after 30s, relaunch fresh
* FR-SD-04: Max retries before marking session as failed (default 3)
* FR-SD-05: Alert user on UI when session stalled/recovered
* FR-SD-06: Log all recovery attempts with timestamps and outcomes
Technical Research Required:
* Investigate Claude Code's native session resume capability
* Determine if prompt injection to running headless session is possible
* Test graceful shutdown signal handling
3.3.3 Monitoring Dashboard (Multi-Agent-Workflow Integration)
Functional Requirements:
* FR-MD-01: Display multi-agent-workflow dashboard as base (70% retained)
* FR-MD-02: Overlay custom UI elements (30% modifications):
    * Workflow selector dropdown (top bar)
    * Component library panel (left sidebar)
    * Memory/RAG status widget (right sidebar)
    * Session lifecycle controls (start/stop/restart buttons)
* FR-MD-03: Real-time event streaming via SSE (retain from multi-agent-workflow)
* FR-MD-04: Display claude-code-proxy data:
    * Token usage (prompt/completion/thinking tokens)
    * Model routing decisions
    * API latency metrics
    * Cost accumulation
* FR-MD-05: Agent hierarchy visualization (tree/graph view)
* FR-MD-06: Filterable event log (by agent, event type, severity)
* FR-MD-07: Exportable session reports (JSON/Markdown)
Multi-Agent-Workflow Retained Features:
* SQLite event storage
* WebSocket streaming
* Vue 3 TypeScript client
* Event timeline charts
* Live pulse metrics
* Hook event tracking (PreToolUse, PostToolUse, SessionStart, SessionEnd, SubagentStop)
New Custom Features:
* Workflow switching without page reload
* Component dependency graph
* RAG retrieval visualization
* Session recording/playback
* Cost predictions based on current usage rate

3.4 Memory & RAG System
3.4.1 Vector Memory Store
Functional Requirements:
* FR-VM-01: Store workflow outputs, agent learnings, successful patterns
* FR-VM-02: Vector database options (pgvector or ChromaDB)
* FR-VM-03: Embedding model: OpenAI text-embedding-3-small or local ONNX
* FR-VM-04: Metadata schema:
    * session_id, workflow_id, agent_id, timestamp
    * content_type: output/learning/pattern/error
    * tags: user-defined or auto-extracted
    * embedding: 1536-dim vector
* FR-VM-05: Semantic search with configurable retrieval-K (default 5)
* FR-VM-06: Hybrid search: Vector similarity + keyword matching
* FR-VM-07: Memory persistence: Session (cleared on end) vs Permanent (cross-session)
3.4.2 Context Injection
Functional Requirements:
* FR-CI-01: On session start, query RAG for relevant context from similar past workflows
* FR-CI-02: Inject top-K results into orchestrator's CLAUDE.md preamble
* FR-CI-03: Format injected context:## Relevant Past Experience
* 
* ### Similar Task from 2025-11-10
* Task: Deep research on AI safety
* Outcome: Successfully synthesized 50+ sources into 10k word report
* Key Learning: Use citation-analyzer early to avoid duplicate source fetching
* 
* ### Pattern from 2025-11-15
* When web-scraper encounters paywalls, delegate to pdf-fetcher with DOI lookup
* 
* FR-CI-04: User-reviewable before session start (optional)
* FR-CI-05: Disable RAG injection per workflow (flag in schema)
3.4.3 Learning Capture
Functional Requirements:
* FR-LC-01: On session end, extract learnings via PostToolUse hooks
* FR-LC-02: Capture:
    * Successful patterns (action → positive outcome)
    * Failures (action → error + resolution)
    * Agent coordination patterns (which agents worked well together)
* FR-LC-03: User annotation: After session, prompt "What worked well? What didn't?"
* FR-LC-04: Store annotations as high-priority memories (boost retrieval score)

3.5 Workflow Lifecycle & Cleanup
3.5.1 Automatic Cleanup Policies
Functional Requirements:
* FR-CL-01: Track workflow last-used timestamp (update on session start)
* FR-CL-02: Daily cleanup job checks policies:
    1. Age-Based: Delete workflows unused for >30 days (configurable)
    2. Size-Based: If total storage >1GB, delete oldest workflows until <1GB
* FR-CL-03: Cleanup order priority:
    1. Failed sessions (oldest first)
    2. Completed sessions (oldest first)
    3. User-saved workflows (never auto-delete)
* FR-CL-04: Pre-cleanup notification: Show UI banner 7 days before deletion
* FR-CL-05: Permanent save: User can mark workflows as "keep forever"
* FR-CL-06: Cleanup logs: Record deleted workflows with metadata for audit
Non-Functional Requirements:
* NFR-CL-01: Cleanup job runs at 3am local time (low-usage window)
* NFR-CL-02: Cleanup operation is atomic (rollback on failure)
* NFR-CL-03: Deleted workflows archived to .super_agent_monitor/archive/ for 90 days
3.5.2 Workflow Sharing & Import
Functional Requirements:
* FR-WS-01: Export workflow as .workflow file (ZIP archive containing):
    * workflow.json - Definition schema
    * components/ - All referenced component files
    * README.md - Human-readable description
* FR-WS-02: Import workflow from .workflow file with conflict resolution UI:
    * Overwrite: Replace existing component versions
    * Merge: Keep both, rename imported as {name}-imported
    * Skip: Don't import conflicting components
* FR-WS-03: Workflow marketplace (future): Community-shared workflows
* FR-WS-04: Workflow validation on import (check component compatibility)

4. Technical Specifications
4.1 Technology Stack
| Layer | Technology | Rationale | |-------|-----------|-----------| | Frontend | Vue 3 + TypeScript | Retain multi-agent-workflow's implementation | | UI Framework | Ant Design / Element Plus | Rich component library for dashboards | | Backend | Bun (Node.js compatible) | Fast runtime, retain multi-agent-workflow compatibility | | Database | SQLite (dev) → PostgreSQL (prod) | Retain multi-agent-workflow's choice, upgrade for scale | | Vector DB | pgvector (PostgreSQL extension) | Single database for structured + vector data | | Alternative Vector DB | ChromaDB | Lightweight option for smaller deployments | | API Layer | Express / Fastify | Wrapper around multi-agent-workflow backend | | Real-time | Server-Sent Events (SSE) | Retain multi-agent-workflow's streaming | | Containerization | Docker + Docker Compose | Easy local development + deployment |
4.2 Database Schema
Workflows Table:
CREATE TABLE workflows (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  version VARCHAR(20),
  author VARCHAR(255),
  tags TEXT[], -- PostgreSQL array
  definition JSONB NOT NULL, -- Full workflow schema
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_used_at TIMESTAMP,
  is_template BOOLEAN DEFAULT FALSE,
  is_permanent BOOLEAN DEFAULT FALSE,
  storage_bytes BIGINT DEFAULT 0
);

CREATE INDEX idx_workflows_last_used ON workflows(last_used_at);
CREATE INDEX idx_workflows_tags ON workflows USING GIN(tags);
Sessions Table:
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  workflow_id UUID REFERENCES workflows(id),
  status VARCHAR(20), -- running/stalled/completed/failed
  started_at TIMESTAMP DEFAULT NOW(),
  ended_at TIMESTAMP,
  last_activity_at TIMESTAMP,
  stall_count INTEGER DEFAULT 0,
  retry_count INTEGER DEFAULT 0,
  total_tokens INTEGER DEFAULT 0,
  total_cost_usd DECIMAL(10,4) DEFAULT 0,
  config_snapshot JSONB, -- Frozen workflow definition
  output_path VARCHAR(500)
);

CREATE INDEX idx_sessions_status ON sessions(status, started_at DESC);
Components Table:
CREATE TABLE components (
  id UUID PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  display_name VARCHAR(255),
  category VARCHAR(50), -- agent/skill/hook/script/mcp/orchestrator/subagent
  description TEXT,
  tags TEXT[],
  dependencies TEXT[],
  incompatibilities TEXT[],
  content TEXT NOT NULL, -- Full markdown content
  metadata JSONB, -- Parsed frontmatter
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_components_category ON components(category);
CREATE INDEX idx_components_tags ON components USING GIN(tags);
Memory Table (RAG):
-- Requires pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE memories (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES sessions(id),
  workflow_id UUID REFERENCES workflows(id),
  content_type VARCHAR(50), -- output/learning/pattern/error
  content TEXT NOT NULL,
  embedding vector(1536), -- OpenAI embedding dimension
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  retrieval_score FLOAT DEFAULT 1.0 -- Boost factor for user annotations
);

CREATE INDEX idx_memories_embedding ON memories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_memories_workflow ON memories(workflow_id, created_at DESC);
4.3 API Endpoints
Workflow Management:
POST   /api/workflows              - Create new workflow
GET    /api/workflows              - List all workflows (with filters)
GET    /api/workflows/:id          - Get workflow details
PUT    /api/workflows/:id          - Update workflow
DELETE /api/workflows/:id          - Delete workflow
POST   /api/workflows/:id/export   - Export as .workflow file
POST   /api/workflows/import       - Import .workflow file
Component Library:
GET    /api/components             - List components (filterable by category/tags)
GET    /api/components/:id         - Get component details
POST   /api/components             - Create custom component
PUT    /api/components/:id         - Update component
DELETE /api/components/:id         - Delete component
GET    /api/components/recommend   - Get smart recommendations (query params)
Session Management:
POST   /api/sessions               - Create session (launches headless Claude)
GET    /api/sessions               - List sessions (with status filters)
GET    /api/sessions/:id           - Get session details
POST   /api/sessions/:id/kick      - Inject kick prompt to stalled session
POST   /api/sessions/:id/restart   - Graceful restart session
DELETE /api/sessions/:id           - Terminate session
GET    /api/sessions/:id/export    - Export session report
Memory/RAG:
GET    /api/memory/search          - Semantic search (query param)
POST   /api/memory                 - Manually add memory
GET    /api/memory/sessions/:id    - Get all memories for session
DELETE /api/memory/:id              - Delete specific memory
Monitoring (Proxied from multi-agent-workflow):
GET    /api/events                 - List all events (filterable)
GET    /stream/:sessionId          - SSE stream for real-time updates
GET    /api/metrics                - Aggregate metrics
4.4 Directory Structure
super_agent_monitor/
├── frontend/                     # Vue 3 UI (modified multi-agent-workflow)
│   ├── src/
│   │   ├── components/
│   │   │   ├── WorkflowSelector.vue      # NEW
│   │   │   ├── ComponentLibrary.vue      # NEW
│   │   │   ├── MonitorDashboard.vue      # MODIFIED (70% original)
│   │   │   └── MemoryViewer.vue          # NEW
│   │   ├── composables/
│   │   ├── stores/
│   │   └── App.vue
│   └── package.json
├── backend/                      # API wrapper + extensions
│   ├── src/
│   │   ├── api/
│   │   │   ├── workflows.ts              # NEW
│   │   │   ├── components.ts             # NEW
│   │   │   ├── sessions.ts               # NEW
│   │   │   └── memory.ts                 # NEW
│   │   ├── services/
│   │   │   ├── workflow-generator.ts
│   │   │   ├── session-manager.ts
│   │   │   ├── stall-detector.ts
│   │   │   └── rag-engine.ts
│   │   └── index.ts
│   └── package.json
├── external/                     # Git submodules
│   └── multi-agent-workflow/    # Submodule: monitoring backend
├── components/                   # Component library (20-30 each)
│   ├── agents/
│   │   ├── researcher-primary.md
│   │   ├── web-scraper.md
│   │   ├── code-reviewer.md
│   │   └── ... (27 more)
│   ├── skills/
│   │   ├── web-search-advanced/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   └── ... (29 more)
│   ├── hooks/
│   │   ├── session-monitor.py
│   │   ├── cost-tracker.py
│   │   └── ... (13 more)
│   ├── scripts/
│   │   ├── fetch-url.py
│   │   ├── parse-pdf.py
│   │   └── ... (28 more)
│   ├── mcp/
│   │   └── ... (15 tools)
│   ├── orchestrators/
│   │   ├── research-coordinator.md
│   │   └── ... (9 more)
│   └── subagents/
│       └── ... (15 prompts)
├── workflows/                    # Pre-built templates
│   ├── deep-research.yaml
│   ├── fast-coder.yaml
│   ├── ebay-deal-hunter.yaml
│   └── ... (17 more)
├── memory/                       # RAG system
│   ├── embeddings/
│   └── config.json
├── .super_agent_monitor/         # Runtime data (gitignored)
│   ├── workflows/                # Temp .claude folders
│   │   └── {workflow-id}/
│   │       └── .claude/
│   ├── archive/                  # Deleted workflows (90-day retention)
│   └── logs/
├── docker-compose.yml
├── README.md
└── prd.md                        # This document

5. Implementation Roadmap
Phase 0: Foundation & Reference Integration (Weeks 1-2)
Deliverables:
*  Repository setup with git submodules  Add [object Object] as submodule  Document claude-code-proxy installation (global, user-managed)  Analyze multi-agent-workflow codebase (see Section 6)  Design database schema  Create component library file structure with 5 examples per category  Write 3 pre-built workflow templates
Success Criteria:
* Git submodule updates work (git submodule update --remote)
* Can run multi-agent-workflow dashboard standalone
* Database schema validated with sample data
* Component examples follow schema with valid frontmatter

Phase 1: Workflow Generator & Component Library (Weeks 3-4)
Deliverables:
*  Workflow schema validator  Workflow generator service (JSON → .claude folder)  Component registry with filesystem scanner  Component metadata parser (YAML frontmatter)  REST API for workflows and components  Basic UI: Component library browser (read-only)
Success Criteria:
* Generate valid .claude folder from workflow JSON in <5s
* Component registry discovers all files on startup
* API returns filtered components by category/tags
* UI displays component details with markdown rendering

Phase 2: Session Management & Headless Launcher (Weeks 5-7)
Deliverables:
*  Session launcher (headless Claude Code execution)  Claude Code installation detection + auto-install  Session database CRUD operations  Stall detection service (monitor claude-code-proxy logs)  Recovery strategies: kick, graceful restart, force restart  Session API endpoints  UI: Session list and control panel
Success Criteria:
* Launch headless session with custom .claude folder
* Detect Claude Code not installed, show installation prompt
* Detect stalled session (no API activity for 5min)
* Successfully restart stalled session with state preserved
* UI shows session status in real-time

Phase 3: Monitoring Dashboard Integration (Weeks 8-10)
Deliverables:
*  Fork multi-agent-workflow frontend  Backend API wrapper (proxy monitoring endpoints)  Custom UI overlays (30% modifications): [object Object]  Real-time event streaming (retain SSE)  Claude-code-proxy data integration (token usage, costs)  Agent hierarchy visualization
Success Criteria:
* Dashboard displays multi-agent-workflow events unchanged (70%)
* Custom workflow selector switches sessions without reload
* Real-time token/cost metrics from claude-code-proxy
* Agent tree visualization shows subagent hierarchy

Phase 4: RAG Memory System (Weeks 11-13)
Deliverables:
*  Vector database setup (pgvector or ChromaDB)  Embedding service (OpenAI API or local ONNX)  Memory CRUD operations  Semantic search endpoint  Context injection on session start  Learning capture on session end  UI: Memory viewer and search
Success Criteria:
* Store session outputs as vector embeddings
* Semantic search returns relevant memories (top-5)
* Inject past learnings into CLAUDE.md preamble
* UI shows retrieved memories before session start
* Learning capture prompts user for annotations

Phase 5: Workflow Lifecycle & Cleanup (Weeks 14-15)
Deliverables:
*  Cleanup policy service (age + size based)  Daily cleanup job scheduler  Workflow export (.workflow ZIP format)  Workflow import with conflict resolution UI  Pre-cleanup notifications (7-day warning)  Archive system (90-day retention)
Success Criteria:
* Cleanup job runs daily at 3am
* Deletes workflows unused >30 days
* Deletes oldest workflows when storage >1GB
* Export workflow as .workflow file
* Import workflow with overwrite/merge/skip options
* UI shows cleanup warnings 7 days in advance

Phase 6: Polish & Documentation (Weeks 16-18)
Deliverables:
*  Complete 20-30 components per category  Write 10-20 pre-built workflow templates  User documentation (README, guides)  Developer documentation (API reference, architecture)  Performance optimization (database indexes, caching)  Docker Compose setup for easy deployment  Beta testing with 10 users
Success Criteria:
* Full component library (20+ each category)
* 20 workflow templates covering common use cases
* User can install and run system via docker-compose up
* Documentation covers all features
* Beta testers report successful workflow execution
* Performance targets met (see Section 5.7)

6. Reference Repository Integration Plan
6.1 Multi-Agent-Workflow Analysis (To Be Completed)
Action Items:
1. Codebase Audit: Analyze external/multi-agent-workflow/ structure
    * Backend: Identify API endpoints, database schema, hook processing logic
    * Frontend: Identify Vue components, Vuex store, SSE handling
    * Document: Which files to retain verbatim, which to modify, which to wrap
2. Integration Strategy:
    * Retain Verbatim: Core monitoring logic, event storage, hook scripts
    * Wrap: Add Express router wrapping multi-agent-workflow endpoints
    * Extend: Add new API endpoints for workflows, components, sessions
3. Update Process:
    * Weekly check: git submodule update --remote
    * Review changes: git diff external/multi-agent-workflow
    * Test: Ensure wrapper APIs still compatible
Deliverable: docs/multi-agent-workflow-integration.md with detailed file-by-file analysis

6.2 Claude-Code-Proxy Integration
Status: External dependency, globally installed by users
Integration Points:
1. Data Consumption:
    * Log file location: ~/.claude/proxy.log (assumption, verify)
    * Parse logs for: API calls, token counts, model routing, latency
    * Display in monitoring dashboard
2. Configuration:
    * Users configure proxy to point to session's .claude folder
    * System provides setup instructions in UI
3. Session Coordination:
    * Proxy logs timestamp → stall detection input
    * Proxy token usage → cost tracking
No Code Changes: Leverage as-installed, consume data outputs
Deliverable: docs/claude-code-proxy-integration.md with setup guide

7. Success Metrics & KPIs
User Experience:
* Time to first workflow deployment: <5 minutes
* Component selection to session launch: <30 seconds
* Workflow generation speed: <5 seconds
* Stall detection latency: <30 seconds
System Performance:
* Dashboard load time: <2 seconds
* Real-time event latency: <100ms
* Database query response (p95): <500ms
* RAG semantic search: <200ms
* Concurrent sessions supported: 10+
Reliability:
* Session recovery success rate: >90%
* False-positive stall detection: <5%
* Workflow generation success rate: >99%
* Zero data loss during cleanup
Adoption:
* Beta users: 10 within 1 month
* Active workflows: 50+ within 3 months
* Component library contributions: 5+ community submissions
* Workflow marketplace: 20+ shared workflows within 6 months

8. Open Questions & Research Items
Technical Unknowns:
1. Claude Code Session Control:
    * Can we inject prompts to running headless sessions?
    * How does Claude Code's native resume work?
    * What signals does it handle gracefully (SIGTERM, SIGINT)?
    * Action: Test headless mode, document findings
2. Multi-Agent-Workflow Modifications:
    * How deeply can we customize without breaking updates?
    * Can we add API endpoints via wrapper vs. forking?
    * Action: Complete codebase analysis (Section 6.1)
3. Claude-Code-Proxy Data Access:
    * Where are logs stored?
    * What log format/schema?
    * Real-time access or polling?
    * Action: Inspect proxy installation, document schema
4. Component Template Variables:
    * How to handle {{PROJECT_NAME}} in components?
    * Jinja2-style templates or custom parser?
    * Action: Define template syntax spec
Product Decisions:
1. Workflow Versioning Strategy:
    * Semantic versioning (v1.0.0)?
    * Auto-increment on save?
    * Decision: Use semantic versioning, manual increment
2. Component Conflicts:
    * Allow duplicate names with versions?
    * Enforce global uniqueness?
    * Decision: Unique names, use version suffixes (agent-v2)
3. Memory Persistence Default:
    * Session-only or permanent by default?
    * User control per workflow?
    * Decision: Session-only default, permanent opt-in
4. Cleanup Notification Method:
    * In-app banner only?
    * Email notifications?
    * Decision: In-app banner, optional email in future
 <end other project prd>     like I said ; start with doing the agent  /plugin combination (give me a folder , each with a .claude folder set up for the specific task in it). Once your’ done with that ; I’ll let you know if the other project above is ready for you to import the files into it; or if I want you to make a quick modification of the other project to make this a self contained item (so scope is plugins (I think that’s what Claude code calls .claude folder combinations of files, confirm this) first; and then the interface second after you report to me
