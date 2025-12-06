# **Product Requirements Document: SwarmForge – Intelligent Multi-Agent Orchestration Platform**

**PRD Version:** 3.0  
**Date:** 2025-11-12  
**Authors:** Product & Engineering Team  
**Status:** Pre-Development – Ready for Implementation  
**Classification:** Internal – Engineering & Product Alignment

---

## 1. Executive Summary

SwarmForge is an enterprise-grade orchestration platform that transforms Claude Code from a single-agent assistant into a resilient, cost-efficient swarm of specialized AI agents. By replacing traditional MCP servers with progressive disclosure patterns and implementing council-based consensus protocols, SwarmForge achieves **10× faster task completion** at **98% lower cost** while scaling to 100+ concurrent tools.

The platform introduces four market-differentiating capabilities: (1) **Autonomous Council Governance** where underperforming agents are terminated by peer vote, (2) **Project Mining** that extracts unfinished ideas from developer notes and auto-spawns initiatives, (3) **Completion Assessment** via vision-language models analyzing live application screenshots, and (4) **Model-Agnostic Routing** enabling dynamic provider switching (OpenRouter, local models, Claude) without code changes.

Target users are senior engineers, dev leads, and platform teams managing complex codebases with 5–50 microservices. SwarmForge will ship as a **polyglot system**: prototype in Python/TypeScript for rapid iteration, production core in Rust/Go for performance.

---

## 2. Product Vision & Goals

### 2.1 Vision Statement

*Every developer deserves a self-managing team of expert agents that think collectively, act decisively, and never waste a token.*

### 2.2 Primary Goals

| Goal | Success Metric | Timeline |
|------|----------------|----------|
| **10× Latency Reduction** | 880ms per complex task vs. 8s baseline | Production v1.0 |
| **98% Cost Optimization** | $242/month for 1M tasks vs. $15,000 GPT-4 baseline | Production v1.0 |
| **90%+ SWE-Bench Score** | Exceed wshobson/agents (84.8%) via council validation | Production v1.0 |
| **Autonomous Project Lifecycle** | Mine 10+ new projects/week from notes; auto-resolve 50% of GitHub issues | Enterprise v2.0 |
| **Developer Net Promoter Score** | >70 NPS from beta cohort of 100 engineers | Beta v0.9 |

### 2.3 Anti-Goals

- **Replace human engineers**: System augments, not replaces. Engineers review council decisions and architecture.
- **Support non-technical users**: Initial target is senior developers comfortable with CLI and configuration.
- **Generic AI chat interface**: No monolithic conversation; focus is swarm visualization and task-level UX.

---

## 3. Target Users & Personas

### 3.1 Primary Persona: "Architect Alex"

*Senior Staff Engineer, 15 YoE, manages 20-service microservices platform*

- **Pain Points**: Context window exhaustion with 8 MCP servers; agents stall on complex tasks; manual QA of agent-generated code.
- **Jobs-to-be-Done**: Delegate refactoring to Rust-specialized agents; validate completion via screenshot comparison; mine Confluence for forgotten initiatives.
- **Success Criteria**: 30% reduction in code review time; 50% fewer agent hallucinations.

### 3.2 Secondary Persona: "Platform Priya"

*Dev Tools Lead, builds internal AI platform for 200-engineer org*

- **Pain Points**: MCP servers drift; hard to enforce security policies; no visibility into agent costs per team.
- **Jobs-to-be-Done**: Deploy SwarmForge as shared service; route teams to different model pools; monitor council debates.
- **Success Criteria**: $10k/month cost savings vs. OpenAI direct; 99.9% uptime.

### 3.3 Tertiary Persona: "Indie Dev Dan"

*Solo founder, building SaaS with AI-first workflow*

- **Pain Points**: Can't afford Claude at scale; needs deterministic tools; wants to preserve context for 50+ tools.
- **Jobs-to-Done**: Use script-based tools for <2k token overhead; council QA on every PR; auto-complete TODOs from Obsidian.
- **Success Criteria**: $200/month operational cost; ship features 3× faster.

---

## 4. Key Features & Requirements

### 4.1 Core Orchestration Engine

#### 4.1.1 Council Voting & Agent Termination

**Description**: Implements Byzantine fault tolerance via peer review. Agents vote on completion quality; lowest-voted agent terminated if consensus fails.

**Functional Requirements**:
- **FR-COU-01**: Council size configurable (default `n=5` agents). [^1]
- **FR-COU-02**: Vote casting via structured JSON: `{"agent_id": "a1", "target_id": "a3", "score": 0.0/0.5/1.0, "rationale": "..."}`.
- **FR-COU-03**: Quorum threshold configurable (default `ceil(n/2) + 1 = 3`).
- **FR-COU-04**: Consensus threshold configurable (default `0.8`).
- **FR-COU-05**: If quorum < threshold, identify lowest-voted agent (excluding self-votes) and execute termination: `bash: pkill -f agent-{id}`.
- **FR-COU-06**: Support encrypted votes via GPG to prevent retaliation. [^2]
- **FR-COU-07**: Termination triggers graceful state handoff: agent writes `agent-{id}.jsonl` transcript, hub redistributes pending tasks.
- **FR-COU-08**: Visual UI shows vote timeline, scores, and termination events.

**Non-Functional Requirements**:
- **NFR-COU-01**: Voting round latency <200ms end-to-end.
- **NFR-COU-02**: Termination must be atomic: no partial task commits.
- **NFR-COU-03**: Council token overhead ≤5× single-agent cost (acceptable for critical tasks).

**User Story**: Alex delegates a complex DB migration to a council. The `schema-migrator` agent proposes a flawed migration; peers vote it down (score 0.3). It is terminated, and the `rollback-expert` agent inherits its state, preventing a production outage.

**Technical Inspiration**: Derived from openrouter-deep-research-mcp’s ensemble consensus; enhanced with Byzantine termination from distributed systems literature.

---

#### 4.1.2 Agent Subagent Delegation

**Description**: Hierarchical task decomposition with isolated contexts and explicit trust graphs.

**Functional Requirements**:
- **FR-DEL-01**: Subagent configuration via YAML frontmatter in `.claude/agents/*.md`. [^3]
- **FR-DEL-02**: Support `delegatees: [agent-a, agent-b]` field defining explicit delegation graph.
- **FR-DEL-03**: Subagent context isolation: each spawn receives clean slate, no parent context pollution.
- **FR-DEL-04**: Resume capability: subagent transcripts stored as `agent-{id}.jsonl`, resumable via `resume: {agentId}`.
- **FR-DEL-05**: PreToolUse/PostToolUse hooks can intercept delegation for audit/logging (see 4.3.1).
- **FR-DEL-06**: Automatic delegation via semantic matching: agent `description` fields indexed in AgentDB, matched against task embeddings.
- **FR-DEL-07**: Max delegation depth configurable (default `3`) to prevent infinite recursion.

**Non-Functional Requirements**:
- **NFR-DEL-01**: Subagent spawn latency <500ms (including context priming).
- **NFR-DEL-02**: Independent tool access: subagent tools restricted to `tools` field; parent tools not inherited unless specified.
- **NFR-DEL-03**: Memory overhead per subagent <50MB.

**User Story**: Priya defines a `security-auditor` agent that automatically delegates static analysis to `bandit-agent`, dependency scanning to `snyk-agent`, and secret detection to `trufflehog-agent`. Each runs in parallel, returning JSON reports that the auditor synthesizes.

**Technical Inspiration**: wshobson/agents three-tier hierarchy; claude-flow queen-worker architecture.

---

#### 4.1.3 Model-Agnostic Task Routing

**Description**: Proxy shim that intercepts model calls and routes based on task signature, cost, and latency.

**Functional Requirements**:
- **FR-RTR-01**: Claude Code proxy implements `ModelProvider` interface; transparent to agents.
- **FR-RTR-02**: Task classification via ONNX model (DistilBERT, 50MB) with 92% accuracy.
- **FR-RTR-03**: Routing rules configurable in `.claude/settings.json`:
  ```json
  {
    "routing_rules": [
      {"pattern": "tool_call.*", "model": "local-qwen2.5-3b", "max_cost": 0.001},
      {"pattern": "planning.*", "model": "claude-sonnet", "min_confidence": 0.9}
    ]
  }
  ```
- **FR-RTR-04**: Fallback logic: if `local-qwen2.5-3b` returns low confidence (`<0.7`), auto-retry with `claude-sonnet`.
- **FR-RTR-05**: Provider abstraction: support OpenRouter, local vLLM, Claude API, Gemini via unified interface.
- **FR-RTR-06**: Cost tracking per agent per task; exposed via `/cost` slash command.
- **FR-RTR-07**: Latency SLO enforcement: if routing to `local-qwen2.5-3b` exceeds 100ms, timeout and fallback.

**Non-Functional Requirements**:
- **NFR-RTR-01**: Routing latency <5ms per call.
- **NFR-RTR-02**: No API calls during optimization (<5ms decision overhead).
- **NFR-RTR-03**: Support 27+ model providers (OpenRouter, Anthropic, Google, local).

**User Story**: Alex runs a load test script. The proxy routes 1000 calls to `local-qwen2.5-3b` at $0.01 total cost. One call hits an edge case (low confidence); it auto-fallbacks to Claude Sonnet, spending $0.15 to ensure correctness. Total cost $0.16 vs. $200 with Claude-only.

**Technical Inspiration**: agentic-flow transparent proxies; claude-code-router Python implementation.

---

### 4.2 Tool Integration & Progressive Disclosure

#### 4.2.1 Script-Based Tool Execution (Primary Pattern)

**Description**: Most advanced pattern; agent reads only intent→script mapping; script source never enters context.

**Functional Requirements**:
- **FR-SCR-01**: Single `readme.md` maps conditions (user intents) to script files.
- **FR-SCR-02**: Prime prompt explicitly forbids reading script source: "DO NOT READ THE SCRIPTS THEMSELVES".
- **FR-SCR-03**: Agent calls scripts via `uv run scripts/{name}.py --json ...`; only output enters context.
- **FR-SCR-04**: Scripts must be self-contained: dependencies in `pyproject.toml`, arg parsing via `argparse`/`click`.
- **FR-SCR-05**: `--help` flag mandatory; agent queries it for usage on ambiguity.
- **FR-SCR-06**: Support script versioning: `scripts/v1/search.py`, `scripts/v2/search.py`; agent uses latest unless specified.
- **FR-SCR-07**: Script registry: `scripts/index.json` with metadata for auto-discovery.

**Non-Functional Requirements**:
- **NFR-SCR-01**: Context overhead <2k tokens per tool activation.
- **NFR-SCR-02**: Script execution overhead <100ms (excluding tool logic).
- **NFR-SCR-03**: Script failure (non-zero exit) triggers agent retry with `--help` parse.

**User Story**: Alex’s agent needs 50 tools (GitHub, Slack, DB, deploy, monitor). Rather than loading 50k tokens of MCP schemas, it loads a <2k token `readme.md`. Each script is called on demand; context grows only with output, not code.

**Technical Inspiration**: Indie Dev Dan transcript; Anthropic progressive disclosure blog.

---

#### 4.2.2 CLI-First Priming Pattern (Secondary)

**Description**: Agent reads `readme.md` + `cli.py` on-demand; full control, moderate context cost.

**Functional Requirements**:
- **FR-CLI-01**: Prime prompt command, e.g., `/prime-kshi-cli-tools`, instructs agent to read two files.
- **FR-CLI-02**: Agent summarizes capabilities after reading; user can issue natural language commands.
- **FR-CLI-03**: Agent translates commands to CLI calls: "market search trillionaire" → `market search "trillionaire"`.
- **FR-CLI-04**: Support argument inference: agent maps synonyms (e.g., "find" → "search").

**Non-Functional Requirements**:
- **NFR-CLI-01**: Context reduction from 10% → 5.6% (44% savings).
- **NFR-CLI-02**: Priming latency <2s for 2-file read + summarize.

**User Story**: Dan has a custom CLI for his startup's infra. He primes the agent; it learns 10 commands. He can now say "deploy staging" instead of memorizing `deploy.py --env staging --branch main`.

---

#### 4.2.3 Skills-Based Bundling (Tertiary)

**Description**: Self-contained directory with `SKILL.md`, scripts, resources; native Claude Code integration.

**Functional Requirements**:
- **FR-SKL-01**: Directory structure: `skills/{name}/SKILL.md`, `scripts/`, `resources/`.
- **FR-SKL-02**: `SKILL.md` uses YAML frontmatter: `name`, `description`, `triggers`.
- **FR-SKL-03**: Three-tier loading (Anthropic pattern):
  - Level 1: Metadata (100 tokens, always loaded).
  - Level 2: `SKILL.md` instructions loaded when triggered (<5k tokens).
  - Level 3: Scripts/resources loaded on-demand (unbounded, zero token cost if unused).
- **FR-SKL-04**: Auto-discovery: Claude Code scans `~/.claude/skills/` and `./.claude/skills/` on startup.
- **FR-SKL-05**: Hooks integration: `PostToolUse` can auto-activate skill if tool pattern matches.

**Non-Functional Requirements**:
- **NFR-SKL-01**: Portable: `cp -r skills/kshi-markets .claude/skills/` activates instantly.
- **NFR-SKL-02**: Isolated: skill dependencies (Python venv, Node modules) contained within directory.

**User Story**: Priya builds a "security-scan" skill with 5 scripts and 20MB of CVE databases. It costs 100 tokens at idle; when triggered, loads <5k tokens of instructions; CVE DB is queried via script, never loaded into context.

**Technical Inspiration**: Anthropic Agent Skills docs; wshobson/agents 47-skills implementation.

---

#### 4.2.4 MCP Server Support (Legacy)

**Description**: Standard MCP protocol for external tools; high context cost but maximum interoperability.

**Functional Requirements**:
- **FR-MCP-01**: Config in `.claude/mcp.json` or `.claude/settings.json#mcpServers`.
- **FR-MCP-02**: Support stdio, SSE, HTTP transports.
- **FR-MCP-03**: Capability negotiation: agent requests tools, server grants subset.
- **FR-MCP-04**: Permission management: granular allow/deny per tool per agent.

**Non-Functional Requirements**:
- **NFR-MCP-01**: Context overhead 10k+ tokens per server (documented limitation).
- **NFR-MCP-02**: Use only for external tools where modification is not needed (80% heuristic).

**User Story**: Dan needs GitHub integration. He adds official MCP server; it "just works" but costs 10k tokens. He accepts this for 1-2 critical external tools.

---

### 4.3 Hooks & Extensibility

#### 4.3.1 Pre/Post Tool Use Hooks

**Description**: Execute bash scripts or LLM prompts before/after tool execution for validation, logging, auto-fix.

**Functional Requirements**:
- **FR-HOOK-01**: Config in `.claude/settings.json#hooks`:
  ```json
  {
    "PreToolUse": [
      {
        "matcher": "Write(src/**.rs)",
        "hooks": [{"type": "command", "command": ".claude/hooks/rust-fmt-check.sh"}]
      }
    ]
  }
  ```
- **FR-HOOK-02**: Environment variables: `$CLAUDE_PROJECT_DIR`, `$CLAUDE_TOOL_NAME`, `$CLAUDE_TOOL_INPUT`.
- **FR-HOOK-03**: Exit codes: `0` = success, `2` = block action, other = non-blocking error.
- **FR-HOOK-04**: JSON output for granular control: `{"decision": "allow|deny|block", "updatedInput": {...}}`.
- **FR-HOOK-05**: Prompt hooks: LLM evaluation of tool input/output for context-aware decisions (uses Haiku).
- **FR-HOOK-06**: **SessionStart/End hooks**: Initialize/cleanup, persist env vars via `$CLAUDE_ENV_FILE`.

**Non-Functional Requirements**:
- **NFR-HOOK-01**: Hook execution latency <100ms for command hooks, <500ms for prompt hooks.
- **NFR-HOOK-02**: Timeout configurable (default 30s); abort tool if hook times out.

**User Story**: Alex configures a `PreToolUse` hook on `Write(**.py)` that runs `ruff check --fix`. Every agent code edit is auto-linted; agent sees fix output and learns.

**Technical Inspiration**: disler/claude-code-hooks-multi-agent-observability; diet103/claude-code-infrastructure-showcase.

---

#### 4.3.2 Slash Commands

**Description**: Built-in commands for agent management, cost tracking, swarm control.

**Functional Requirements**:
- **FR-CMD-01**: `/agents` – list, create, edit, delete subagents; manage tool permissions.
- **FR-CMD-02**: `/cost` – show per-agent token usage, cost breakdown by model.
- **FR-CMD-03**: `/council spawn --size=5 --task="..."` – manually trigger council.
- **FR-CMD-04**: `/mine` – manually trigger project mining from notes.
- **FR-CMD-05**: `/clear` – clear context window (prevent pollution).
- **FR-CMD-06**: `/hooks` – list, enable/disable hooks mid-session.
- **FR-CMD-07**: `/validate {url}` – manually trigger completion assessment.

**Non-Functional Requirements**:
- **NFR-CMD-01**: Command response latency <200ms.

**User Story**: Priya types `/cost` and sees that `security-auditor` spent $12 this session; she realizes it's using Sonnet for simple grep tasks and updates routing rules.

---

### 4.4 Autonomous Project Management

#### 4.4.1 Project Mining from Notes

**Description**: Parse Obsidian/Roam/Notion notes for `TODO: Project Idea:` blocks; auto-spawn projects.

**Functional Requirements**:
- **FR-MINE-01**: Configurable notes directories: `.claude/config.json#notes_dirs: ["~/Obsidian", "~/Roam"]`.
- **FR-MINE-02**: Regex pattern: `r'TODO: Project Idea: (.+)'` (customizable).
- **FR-MINE-03**: For each match, check if project repo exists (local or GitHub).
- **FR-MINE-04**: If not exists, spawn `project-starter` agent with context:
  - Source note path & line number.
  - Idea text.
  - Related notes (link analysis).
- **FR-MINE-05**: `project-starter` agent: scaffold repo, create `CLAUDE.md`, open GitHub issue, assign to creator.
- **FR-MINE-06**: **Frequency**: Run on `SessionStart` and via cron (daily at 09:00).
- **FR-MINE-07**: Deduplication: don't spawn if similar project created in last 30 days (embed similarity >0.9).

**Non-Functional Requirements**:
- **NFR-MINE-01**: Mining latency <5s for 1000 notes.
- **NFR-MINE-02**: False positive rate <5% (tune regex with user feedback).

**User Story**: Alex has 200 TODOs in Obsidian. SwarmForge mines them, finds "Build Rust CLI for log parsing," creates `~/projects/log-parser/`, opens issue #1, assigns to Alex. Alex reviews and approves.

**Technical Inspiration**: Manual TODO extraction in transcript summary; enhanced with similarity dedup.

---

#### 4.4.2 GitHub Issue Resolution

**Description**: Poll GitHub Issues, self-assign, execute, open PR.

**Functional Requirements**:
- **FR-GH-01**: Config: `.claude/settings.json#github_integration`: `{token, repos: ["org/repo"]}`.
- **FR-GH-02**: Poll interval: 5 minutes for assigned issues, 1 hour for unassigned.
- **FR-GH-03**: Filter: `label:in-progress` or `label:good-first-issue` (customizable).
- **FR-GH-04**: Agent self-assigns if issue matches its capabilities (description embedding similarity >0.85).
- **FR-GH-05**: Execution: spawn `issue-worker` agent with issue body as prompt.
- **FR-GH-06**: **Validation**: for issues with `label:needs-validation`, run completion assessment before PR.
- **FR-GH-07**: PR automation: create branch `swarmforge/issue-{id}`, commit, open PR with "Automated fix for #{id}".
- **FR-GH-08**: Human review gate: PR requires approval before merge (configurable).

**Non-Functional Requirements**:
- **NFR-GH-01**: Issue-to-PR latency <10 minutes for simple fixes (typos, lint).
- **NFR-GH-02**: Success rate: 50% of assigned issues resolved without human intervention.

**User Story**: Dan's repo has issue #42: "Fix typo in README." Swarmforge polls, `doc-writer` agent self-assigns, fixes, opens PR #43. Dan reviews and merges in 30 seconds.

**Technical Inspiration**: wshobson/agents GitHub tooling; enhanced with self-assignment.

---

### 4.5 Completion Assessment Pipeline

**Description**: Automated QA via browser automation + vision model; validates functionality against design docs.

**Functional Requirements**:
- **FR-VAL-01**: Trigger: agent emits `<completion_assessment>` tag or manual `/validate {url}`.
- **FR-VAL-02**: Orchestrator spawns `validation-subagent` (isolated context).
- **FR-VAL-03**: **Playwright**: launch headless browser, navigate to URL, capture screenshot, extract DOM.
- **FR-VAL-04**: **Design Docs**: load `CLAUDE.md` or `design.md` from repo.
- **FR-VAL-05**: **Vision Model**: prompt Claude Sonnet with screenshot + design docs:
  ```
  System: You are a QA engineer. Compare screenshot to design docs. 
  Score functionality 0-1. List discrepancies.
  ```
- **FR-VAL-06**: Output structured JSON: `{"score": 0.92, "discrepancies": ["Missing 'Export' button"], "pass": true/false}`.
- **FR-VAL-07**: If `pass=false`, re-open issue or alert human.
- **FR-VAL-08**: **User Story Matching**: Extract acceptance criteria from issue/user story; validate each via Playwright script.

**Non-Functional Requirements**:
- **NFR-VAL-01**: Assessment latency <1s (Playwright 500ms + LLM 300ms).
- **NFR-VAL-02**: Accuracy: 92% alignment with manual QA (benchmark target).
- **NFR-VAL-03**: Support responsive design: test at 1920×1080 and 375×667 (mobile).

**User Story**: Alex's agent claims "user profile page done." Validation spawns, loads `localhost:3000/profile`, captures screenshot, compares against Figma link in `CLAUDE.md`. Detects missing avatar upload. Reopens issue.

**Technical Inspiration**: Playwright HAR capture in high-performance transcript; claude-flow Hive Mind visual analysis.

---

### 4.6 Visual Dashboard & Interface

#### 4.6.1 Agent Monitor

**Description**: Real-time Web UI showing agent states, message streams, costs, council votes.

**Functional Requirements**:
- **FR-UI-01**: **Layout**: 3-column – Agents List (left), Agent Detail (center), System Log (right).
- **FR-UI-02**: **Agent Card**: name, status (working/waiting/completed/terminated), current task, token usage, cost.
- **FR-UI-03**: **Live Stream**: WebSocket connection to `claude --debug` output; separate pane per agent (not interleaved).
- **FR-UI-04**: **Council View**: shows live vote progress, scores, termination countdown.
- **FR-UI-05**: **Cost Dashboard**: bar chart of per-agent spend; alert if daily budget exceeded.
- **FR-UI-06**: **Task Timeline**: Gantt chart of agent tasks, dependencies, parallel execution blocks.
- **FR-UI-07**: **Kill Switch**: manual "Terminate Agent" button for rogue agents.
- **FR-UI-08**: **Mobile Friendly**: responsive for monitoring on phone.

**Non-Functional Requirements**:
- **NFR-UI-01**: Page load <100ms; WebSocket message latency <50ms.
- **NFR-UI-02**: Support 100+ concurrent agents in dashboard without jank.
- **NFR-UI-03**: Export logs as JSON for post-mortem analysis.

**User Story**: Priya opens dashboard, sees 5 agents working on feature. `performance-optimizer` agent shows high token usage; she clicks it, sees it's stuck on a regex. She hits Terminate, council redistributes task.

**Technical Inspiration**: disler/claude-code-hooks-multi-agent-observability Vue UI; baryhuang/claude-code-by-agents desktop app.

---

#### 4.6.2 Slash Command Interface

**Description**: Terminal-style command bar in UI for rapid actions.

**Functional Requirements**:
- **FR-SUI-01**: Autocomplete for `/agents`, `/cost`, `/council`, `/mine`, `/validate`.
- **FR-SUI-02**: Command history (persisted in localStorage).
- **FR-SUI-03**: Keyboard shortcuts: `Ctrl+K` to focus, `Esc` to clear.

**Non-Functional Requirements**:
- **NFR-SUI-01**: Command response <200ms.

---

### 4.7 Memory & Knowledge Management

#### 4.7.1 AgentDB Integration

**Description**: Persistent SQLite + pgvector for hybrid BM25 + semantic search.

**Functional Requirements**:
- **FR-MEM-01**: **Schema**: `agent_memory(agent_id, task_id, content, embedding, access_count, created_at)`.
- **FR-MEM-02**: **Storage**: local SQLite for prototyping, PostgreSQL(pgvector) for production, Pinecone for scale.
- **FR-MEM-03**: **Search**: Hybrid query: `BM25('keywords') + cosine_similarity(embedding, query)`.
- **FR-MEM-04**: **Auto-summarization**: When `content` length >10k tokens, spawn `summarizer` agent to compress to 1k tokens.
- **FR-MEM-05**: **Eviction**: LRU based on `access_count`; oldest summarized memories archived to cold storage (S3).
- **FR-MEM-06**: **Cross-agent sharing**: Workers query CEO's `ReasoningBank` for patterns; explicit opt-in via `shared: true` flag.

**Non-Functional Requirements**:
- **NFR-MEM-01**: Query latency 2-3ms (HNSW index).
- **NFR-MEM-02**: Search speed 96×-164× faster than naive vector scan (benchmark).
- **NFR-MEM-03**: Memory reduction 4-32× via quantization.

**User Story**: Alex reopens session after weekend. `rust-executor` agent resumes from `agent-123.jsonl` transcript, reloads context from AgentDB, continues migration task. No context loss.

**Technical Inspiration**: claude-flow AgentDB; openrouter-deep-research PGlite + pgvector.

---

#### 4.7.2 Interleaved Thinking Storage

**Description**: Parse `<thinking>` tags from model output; store separately, not in context.

**Functional Requirements**:
- **FR-THINK-01**: Regex parse `<thinking>(.*?)</thinking>` from model responses.
- **FR-THINK-02**: Store parsed thinking in AgentDB linked to task ID.
- **FR-THINK-03**: UI toggle: "Show Thinking" reveals chain-of-thought in agent detail pane.
- **FR-THINK-04**: Thinking not re-inserted into context on resume; agent sees only final action.

**Non-Functional Requirements**:
- **NFR-THINK-01**: Reduce context bloat by 6× on long chains (Kimi K2 benchmark).

**User Story**: Alex debugs agent failure. He opens UI, clicks "Show Thinking" for the task, sees 8-step reasoning that led to bad decision. He corrects the logic in the prompt.

---

### 4.8 Security & Isolation

#### 4.8.1 Permission & Tool Scoping

**Description**: Principle of least privilege; agents grant only necessary tools.

**Functional Requirements**:
- **FR-PER-01**: Agent YAML: `tools: ["Read(src/**)", "Deny(Read(.env*))", "Bash(cargo *)", "Deny(Bash(rm -rf /))"]`.
- **FR-PER-02**: Glob pattern matching for tool paths.
- **FR-PER-03**: Permission inheritance: subagent inherits parent restrictions; cannot escalate.
- **FR-PER-04**: Audit log: every tool call logged with agent ID, input, output, timestamp.

**Non-Functional Requirements**:
- **NFR-PER-01**: 84% reduction in permission prompts vs. MCP (Anthropic sandboxing benchmark).

**User Story**: Priya configures `security-auditor` agent with `Deny(Write(**))` to read-only mode. Agent cannot accidentally modify code; attempts are blocked and logged.

**Technical Inspiration**: Anthropic sandboxing Linux bubblewrap; wshobson/agents tool restrictions.

---

#### 4.8.2 Sandboxing

**Description**: OS-level isolation for tool execution.

**Functional Requirements**:
- **FR-SBX-01**: Rust-based sandbox using Linux namespaces + seccomp-bpf.
- **FR-SBX-02**: Filesystem restriction: agent can only access `./.claude/` and project working directory.
- **FR-SBX-03**: Network proxy: domain allowlist; block external calls unless whitelisted.
- **FR-SBX-04**: Resource limits: CPU 1 core, RAM 2GB per agent cgroup.

**Non-Functional Requirements**:
- **NFR-SBX-01**: Sandboxed execution overhead <10ms per tool call.

**Technical Inspiration**: AutoAgents LiquidOS Vector pipelines; Temporal worker isolation.

---

## 5. Technical Architecture

### 5.1 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (Go)                        │
│  - REST: /api/tasks, /api/agents, /api/validate            │
│  - WebSocket: /ws/events (agent logs, votes)               │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 Orchestration Layer (Go)                    │
│  - Temporal/Cadence workflows (council votes, mining)      │
│  - Task router (star topology, round-robin)                │
│  - Cost tracker (per-agent, per-task)                      │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Execution Engine (Rust)                   │
│  - Tool executor (reqwest, tokio)                          │
│  - Playwright controller (thirtyfour)                      │
│  - Script invoker (uv, npx, cargo run)                     │
│  - Sandboxing (Linux namespaces, seccomp)                  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Model Proxy (Rust)                      │
│  - ONNX classifier (task categorization)                   │
│  - OpenRouter client                                       │
│  - Local vLLM integration                                  │
│  - Claude API client                                       │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                       Memory (AgentDB)                      │
│  - SQLite (dev) → PostgreSQL (prod) → Pinecone (scale)    │
│  - Embeddings (pgvector)                                   │
│  - ReasoningBank (pattern matching)                        │
└─────────────────────────────────────────────────────────────┘
```

---

### 5.2 Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **API Gateway** | Go `fiber` + `gorilla/websocket` | 20k req/s, low latency |
| **Orchestration** | Temporal/Cadence | Durable workflows, exactly-once execution |
| **Execution** | Rust `tokio` + `reqwest` | 20-60ms tool calls, memory safety |
| **Browser** | Playwright Rust (`thirtyfour`) | 100-300ms automation, 2-3× faster than Python |
| **Sandbox** | Linux namespaces + seccomp-bpf | OS-level isolation, <10ms overhead |
| **Model Proxy** | Rust `ort` (ONNX) + `hyper` | 5ms classification, 5ms routing |
| **Memory** | SQLite → PostgreSQL(pgvector) → Pinecone | Progressive scaling, 2-3ms query |
| **UI** | SvelteKit + WebSocket | <100ms load, <50ms updates |
| **CLI** | Python `click` (prototype) → Rust `clap` (prod) | Rapid iteration → performance |

---

## 6. User Stories (Detailed)

### 6.1 Council Termination Prevents Production Outage

**Persona**: Architect Alex

**Scenario**: Alex delegates a complex DB migration to a council of 5 agents: `schema-migrator`, `data-backup`, `validator`, `rollback-expert`, `monitor`. The `schema-migrator` proposes a migration that drops an index needed by a critical query.

**Steps**:
1. `schema-migrator` executes migration in staging, reports "success."
2. `validator` runs load test, sees query latency spike from 10ms to 2000ms.
3. `validator` votes `{"target": "schema-migrator", "score": 0.0, "rationale": "Index drop caused 200× slowdown on /api/users"}`
4. `monitor` corroborates with metrics.
5. Votes: 1.0 (backup), 0.0 (validator), 0.0 (monitor), 0.5 (rollback), 0.5 (migrator self-vote). Consensus = 0.4 < 0.8 threshold.
6. Council identifies `schema-migrator` as lowest-voted (0.5, excluding self-vote of 0.5 → 0.0).
7. Termination signal sent: `pkill -f agent-schema-migrator`.
8. `rollback-expert` inherits state, runs `ROLLBACK`, restores index.
9. Alex receives alert: "Council terminated schema-migrator; rollback complete."

**Outcome**: Production incident prevented; Alex reviews logs, updates `schema-migrator` prompt with index-preservation rule.

---

### 6.2 Project Mining Spawns Revenue Feature

**Persona**: Indie Dev Dan

**Scenario**: Dan has Obsidian note "Startup Ideas" with line: "TODO: Project Idea: Build Stripe analytics dashboard for SaaS founders."

**Steps**:
1. SwarmForge `SessionStart` hook triggers project mining.
2. Parser extracts idea, checks GitHub: no `stripe-dashboard` repo exists.
3. Spawns `project-starter` agent with context: idea text, note link, Dan's coding style from `CLAUDE.md`.
4. `project-starter` scaffolds repo:
   - `cargo new stripe-dashboard --bin`
   - Creates `CLAUDE.md` with spec derived from idea.
   - Adds dependencies: `stripe`, `axum`, `tokio`, `plotly`.
   - Generates README with mockups.
5. Opens GitHub issue: "#1: Initialize Stripe analytics dashboard" and assigns to Dan.
6. Dan reviews issue, approves, runs `swarmforge start stripe-dashboard`.
7. Council of agents builds MVP in 3 hours; completion assessment validates dashboard loads real Stripe data.

**Outcome**: Dan ships feature in 1 day that was buried in notes for 6 months; incremental MRR of $500/month.

---

### 6.3 Completion Assessment Catches UI Bug

**Persona**: Platform Priya

**Scenario**: Priya's team uses SwarmForge to build new user onboarding flow. Agent claims "onboarding complete."

**Steps**:
1. Agent emits `<completion_assessment>` tag.
2. Validation agent spawns Playwright, loads `https://staging.myapp.com/onboarding`.
3. Captures screenshot, extracts DOM.
4. Loads design doc from Figma (linked in `CLAUDE.md`).
5. Claude Sonnet vision prompt:
   ```
   Screenshot shows:
   - Email field present ✓
   - Password field present ✓
   - "Next" button disabled ✗ (design shows enabled state)
   - Missing progress indicator ✗
   Score: 0.6
   ```
6. Validation fails; issue reopened with screenshot diff.
7. `frontend-agent` fixes button state and progress bar.
8. Re-run validation: score 1.0; PR approved.

**Outcome**: UI bug caught before merge; manual QA would have taken 30 minutes.

---

## 7. Competitive Analysis Matrix

| Feature                    | SwarmForge           | wshobson/agents | openrouter-deep-research | claude-flow     | ccswarm    |
| -------------------------- | -------------------- | --------------- | ------------------------ | --------------- | ---------- |
| **Council Voting**         | ✅ Termination        | ❌               | ❌                        | ❌               | ❌          |
| **Project Mining**         | ✅ Auto-spawn         | ❌               | ❌                        | ❌               | ❌          |
| **Completion Assessment**  | ✅ Vision-based       | ❌               | ❌                        | ❌               | ❌          |
| **Model-Agnostic Routing** | ✅ Local + OpenRouter | ❌ (Claude only) | ✅ (OpenRouter only)      | ❌ (Claude only) | ❌          |
| **Script-Based Tools**     | ✅ <2k tokens         | ✅               | ❌ (MCP only)             | ❌               | ❌          |
| **Rust/Go Backend**        | ✅ 20-60ms            | ❌ (TypeScript)  | ❌ (Python)               | ❌ (Ruby)        | ❌ (Python) |
| **Visual Dashboard**       | ✅ <50ms WS           | ❌               | ❌                        | ⚠️ Basic        | ✅          |
| **SWE-Bench Target**       | 90%+                 | 84.8%           | N/A                      | 84.8%           | N/A        |
| **Cost at Scale**          | $242/mo              | $3,000+/mo      | $450/mo                  | $2,000/mo       | $1,500/mo  |

**Differentiation**: SwarmForge is the only system combining **council fault tolerance**, **autonomous project lifecycle**, and **polyglot performance** in one platform.

---

## 8. Implementation Phases

### Phase 0: Foundation (Weeks 1–2)

**Goal**: Core infrastructure, hooks, script-based tools.

**Deliverables**:
- Repo structure: `swarmforge/` (Rust), `swarmforge-py/` (Python prototype).
- CLI: `swarmforge init`, `swarmforge agent list`, `swarmforge run`.
- `.claude` folder scaffold with `agents/`, `skills/`, `hooks/`, `settings.json`.
- **Script executor**: Rust binary that runs `uv run scripts/{name}.py --json ...` with sandbox.
- **Hooks system**: PreToolUse, PostToolUse, SessionStart/End implemented in Go.
- **Prime prompt library**: 10 example primes for CLI-first and script-based patterns.

**Success Criteria**: Can run a single task through script-based tool; latency <200ms.

---

### Phase 1: Orchestration & Delegation (Weeks 3–5)

**Goal**: Subagent spawning, resume capability, CEO-worker pattern.

**Deliverables**:
- **Subagent manager**: Parse `.claude/agents/*.md`, spawn agents with isolated contexts.
- **Resume logic**: `agent-{id}.jsonl` transcript write/read; rehydrate context via AgentDB.
- **CEO-worker protocol**: CEO agent (Sonnet) delegates to workers (Qwen2.5-3B) via explicit `delegatees` list.
- **Hooks**: Add `OnAgentSpawn`, `OnAgentTerminate` events.

**Success Criteria**: Run 3-agent hierarchy (CEO → 2 workers) on sample refactoring task; sub-agent spawn <500ms.

---

### Phase 2: Council & Consensus (Weeks 6–8)

**Goal**: Council voting, termination, encrypted votes.

**Deliverables**:
- **Council workflow**: Temporal workflow for round-based voting.
- **Vote aggregator**: Collect votes, compute consensus, identify lowest-voted agent.
- **Termination executor**: Graceful shutdown + state handoff.
- **GPG integration**: `gpg --encrypt --recipient council@vote` for hidden messages.
- **Dashboard UI**: Real-time vote progress bar, agent cards, termination log.

**Success Criteria**: Simulate 5-agent council on 10 tasks; termination occurs on 2/10; consensus quality >0.85.

---

### Phase 3: Model Routing & Performance (Weeks 9–11)

**Goal**: Model-agnostic proxy, ONNX classifier, local model integration.

**Deliverables**:
- **Model proxy**: Rust service that intercepts calls, classifies via ONNX, routes.
- **ONNX classifier**: DistilBERT fine-tuned on 10k task examples (tool call vs. reasoning).
- **Local model support**: vLLM integration for Qwen2.5-3B, Granite-4.0-Tiny.
- **OpenRouter client**: Fallback when local models unavailable.
- **Cost tracking**: Per-agent spend accumulator; exposed via `/cost` API.

**Success Criteria**: 95% tasks route to local models; fallback <5%; classification accuracy >90%.

---

### Phase 4: Validation & Mining (Weeks 12–14)

**Goal**: Completion assessment, project mining, GitHub integration.

**Deliverables**:
- **Playwright executor**: Rust controller for headless browser automation.
- **Vision validation**: Claude Sonnet prompt with screenshot + design docs.
- **Project miner**: Cron job + `SessionStart` hook; regex parsing; similarity dedup.
- **GitHub MCP server**: Enhanced version with self-assignment logic.
- **Dashboard**: SvelteKit UI with WebSocket; agent timeline, cost chart.

**Success Criteria**: Validate 10 sample tasks; catch 2 UI bugs; mine 5 projects from notes.

---

### Phase 5: Enterprise Hardening (Weeks 15–18)

**Goal**: Scale to 10,000 agents, RBAC, SAML, audit logs.

**Deliverables**:
- **Temporal cluster**: Multi-node orchestration for 1M+ workflows/day.
- **AgentDB**: Migrate to PostgreSQL → Pinecone for 100M+ memories.
- **RBAC**: Agent roles (viewer, executor, admin), team workspaces.
- **SAML/SSO**: Okta, Azure AD integration.
- **Audit export**: SOC2-compliant logs to S3/GCS.

**Success Criteria**: Pass security review; scale test: 10,000 concurrent agents, 99.9% uptime.

---

## 9. Success Metrics & KPIs

| Metric | Baseline | Target v1.0 | Target v2.0 | Measurement |
|--------|----------|-------------|-------------|-------------|
| **Task Latency (p95)** | 8s (Python MCP) | 880ms | 500ms | Distributed tracing |
| **Cost per 1k tasks** | $45 (GPT-4) | $2.42 | $0.68 | OpenRouter + local |
| **SWE-Bench Score** | 84.8% (wshobson) | 90% | 95% | Automated benchmark |
| **Agent Uptime** | N/A | 99.5% | 99.9% | Temporal metrics |
| **Council Consensus Rate** | N/A | 80% | 90% | Vote log analysis |
| **Project Mining Yield** | 0/week | 5/week | 15/week | Issue creation log |
| **GitHub Resolution Rate** | 0% | 30% | 50% | PR merge log |
| **Context Overhead per Tool** | 10k tokens (MCP) | <2k tokens | <1k tokens | Token counter |
| **Developer NPS** | N/A | >50 | >70 | Quarterly survey |
| **Token Efficiency** | 1× (naive) | 5× | 10× | Benchmark suite |

---

## 10. Open Questions & Risks

### 10.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Council terminates productive agent** | Medium | High | Require 2 failed votes before termination; human override |
| **Model classifier misroutes complex task** | Medium | Medium | Confidence threshold + fallback; human review queue |
| **Playwright detection by anti-bot** | Low | Medium | Use stealth mode; fallback to API validation |
| **Script-based tools drift (no schema)** | High | Medium | Versioning; automated `--help` testing; migration warnings |
| **AgentDB query latency at scale** | Low | High | Shard by agent_id; add Redis cache for hot paths |
| **Encrypted votes cause deadlock** | Low | Medium | Timeout on GPG ops; fallback to public votes if delay >10s |

### 10.2 Product Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Developers distrust agent termination** | High | High | Dashboard transparency; termination only after 2 votes; opt-out mode |
| **Project mining creates noise (false positives)** | Medium | Medium | Tune regex with user feedback; similarity threshold >0.95 |
| **Cost tracking is inaccurate** | Medium | High | Reconcile with provider invoices monthly; show real-time estimates |
| **Ecosystem lock-in (Claude skills)** | High | Medium | Support MCP import/export; maintain script-based parity |
| **Visual UI is slow at 100+ agents** | Medium | High | Virtualized lists in UI; WebSocket binary framing; pagination |

### 10.3 Business Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Anthropic changes Claude Code API** | Medium | High | Abstract behind proxy; maintain feature flags for versions |
| **OpenRouter pricing increases** | Medium | Medium | Local model fallback; multi-provider routing |
| **Enterprise security review blocks** | Medium | High | Start with FedRAMP-compliant cloud; on-prem option |
| **Competitor copies features** | High | Medium | First-mover advantage; community moat (open source core) |

---

## 11. Assumptions & Constraints

### 11.1 Assumptions

- Target users are senior engineers comfortable with CLI, YAML config, and async concepts.
- Claude Code remains actively developed; APIs stable for 12 months.
- Local model inference (Qwen2.5-3B) is acceptable for 95% of tasks; edge cases escalate.
- GitHub is primary code host; GitLab support in v2.0.
- Observidian/Roam are primary note-taking tools; Notion integration in v2.0.

### 11.2 Constraints

- **Context Window**: Claude Sonnet 4.5 limit 200k tokens; we target <50k tokens per council round.
- **Rate Limits**: OpenRouter 1000 req/min; local models unlimited.
- **Hardware**: Local model inference requires GPU (RTX 4090 or A10G) for <50ms latency.
- **Budget**: Development budget $150k; cloud infra budget $500/month for v1.0.
- **Timeline**: 18 weeks to v1.0; 12 weeks to v2.0.

---

## 12. Future Roadmap (v2.0 & Beyond)

### 12.1 v2.0 Features (Q2 2026)

- **Async Coordination**: NATS message queue for pub/sub agent communication; Raft consensus for distributed council.
- **Memory Evolution**: Neo4j knowledge graph for relationship tracking; episodic memory for cross-project learning.
- **Cross-Platform**: React Native mobile app; state sync via WebSocket; Siri shortcuts for task kickoff.
- **Industry Skills**: Pre-built skills for finance (SEC filing parser), healthcare (HIPAA-compliant de-id), legal (contract analysis).
- **Voice Interface**: Whisper integration for voice commands; TTS for agent status updates.

### 12.2 v3.0 Vision (Q4 2026)

- **Autonomous Company**: Mine Notion OKRs, spawn projects, hire agents (auto-scale based on budget), report KPIs to human CEO.
- **AI-to-AI Market**: Agents can "hire" other agents from marketplace; pay per task in credits.
- **Neural Compiler**: Train model to emit directly optimized LLVM IR, bypassing borrow checker limits.

---

## 13. Glossary

- **Agent**: Specialized AI worker with YAML config, isolated context, tool restrictions.
- **Council**: Group of agents voting on completion; lowest-voted terminated if consensus fails.
- **MCP**: Model Context Protocol; standard but high-context tool integration.
- **Prime Prompt**: Command that loads tool definitions into agent context on-demand.
- **Progressive Disclosure**: Load only metadata → instructions → resources as needed.
- **Script-Based**: Agent reads intent→script map; script source never enters context.
- **Star Topology**: Central hub broadcasts tasks to agents; agents pull based on capability.
- **SWE-Bench**: Benchmark for software engineering task automation.
- **Temporal**: Durable workflow orchestration (Go).

---

## 14. Appendices

### Appendix A: Example `.claude/agents/code-reviewer.md`

```yaml
---
name: code-reviewer
description: Expert code review specialist. Proactively review code immediately after changes.
tools: Read, Grep, Glob, Bash
model: claude-sonnet
delegatees: [security-auditor, performance-checker, style-enforcer]
---

# CODE REVIEW CHECKLIST

1. **Security**: Check for SQL injection, XSS, hardcoded secrets.
2. **Performance**: Identify N+1 queries, inefficient loops.
3. **Style**: Enforce ruff, black, conventional commits.
4. **Tests**: Ensure coverage for new code.

**Workflow**:
- On `PostToolUse` for `Write(**)`, spawn self.
- Review diff via `git diff`.
- Post comments as GitHub PR review.
- If confidence <0.9, escalate to `security-auditor` agent.
```

---

### Appendix B: Example `.claude/skills/github-automation.md`

```yaml
---
name: github-automation
description: Automate issue triage, PR creation, project management. Trigger on GitHub webhook.
---

# GITHUB AUTOMATION SKILL

## Scripts
- `scripts/triage_issue.py` – Parse issue, assign agent.
- `scripts/create_pr.py` – Commit changes, open PR.
- `scripts/sync_project.py` – Mirror project board to Linear.

## Resources
- `webhooks.md` – Webhook payload schemas.
- `templates/` – PR templates, issue forms.
```

---

### Appendix C: Council Voting Flowchart

```
User Delegates Task
    ↓
Orchestrator Spawns Council (n=5)
    ↓
Agents Execute in Parallel
    ↓
Vote Submission (30s timeout)
    ↓
Votes Aggregated
    ↓
Consensus >= 0.8?
    ├─ Yes → Task Complete → Return Result
    └─ No → Identify Lowest-Voted Agent (≠ self)
            ↓
        Terminate Agent
            ↓
    Redistribute Tasks
            ↓
    Escalate to Human (if >2 terminations)
```

---

**End of PRD**