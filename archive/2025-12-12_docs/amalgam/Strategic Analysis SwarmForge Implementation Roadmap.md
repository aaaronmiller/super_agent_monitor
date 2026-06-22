# Strategic Analysis: SwarmForge Implementation Roadmap

Based on my analysis of the four documents in the context of your SwarmForge PRD, I've identified immediate implementation opportunities and strategic horizon plans. The documents reveal both tactical optimizations ready for deployment and transformative capabilities requiring longer-term investment.

---

## 🚀 **Immediate Implementation (0-3 Months)**

These concepts are battle-tested, require minimal architectural changes, and align directly with your existing PRD requirements.

### **1. CLI-First Tool Priming with Progressive Disclosure**
*Source: File 1 (Indie Dev Dan) | PRD Alignment: FR-SCR-01, FR-CLI-01*

**Implementation Readiness:** ✅ **Deploy Now**

The PRD already specifies script-based tools (`FR-SCR-01`) and CLI patterns (`FR-CLI-01`), but File 1 provides the critical implementation details:

- **Exact Prime Prompt Template**: Use the verbatim constraint from File 1:  **"DO NOT READ THE SCRIPTS THEMSELVES; rely only on `--help` flags"**  . This achieves the <2k token overhead target.
- **Trifecta Development Pattern**: Build CLIs that serve **you, your team, and your agents** simultaneously. File 1's "market search trillionaire" example maps directly to your `/prime-kshi-cli-tools` command.
- **Decision Heuristic Integration**: Your PRD mentions 80% CLI-first for new tools—codify this in `.claude/settings.json#toolbelt_heuristic` with explicit thresholds.

**Action Item**: Create a `swarmforge prime` command that auto-generates the two-file structure (`readme.md` + `cli.py`) and enforces the 5.6% context budget per tool.

### **2. Color-Coded Strategic Routing (GREEN/YELLOW/RED Lanes)**
*Source: File 4 (AIME) | PRD Alignment: All sections*

**Implementation Readiness:** ✅ **Deploy Now**

Your PRD references the Color-Coded Framework but lacks File 4's precise operational definitions:

- **GREEN Lane = Direct File Manipulation**: Map to **Roo Code environment** adaptation from File 4. Inject AST analysis directly into the actor's "Knowledge" component for zero-context file ops.
- **YELLOW Lane = Pattern Matching**: Use the `mcp-sequential-thinking-tools` for complex algorithm tasks as specified. The PRD's ONNX classifier (`FR-RTR-02`) should auto-route here when confidence >0.9.
- **RED Lane = CEO-Agent**: Implement the **Leave-Allow-Let-Sit framework** from File 1's hierarchical decomposition. The CEO agent (Claude Sonnet) should explicitly delegate to Qwen2.5-3B workers using the `delegatees: [agent-a, agent-b]` YAML syntax.

**Action Item**: Add `color_lane` field to `.claude/agents/*.md` frontmatter and enforce lane-specific tool budgets (GREEN: 1k tokens, YELLOW: 5k tokens, RED: 50k tokens).

### **3. Council Voting with Byzantine Termination**
*Source: File 4 (AIME) | PRD Alignment: FR-COU-01 to FR-COU-08*

**Implementation Readiness:** ✅ **Deploy Now**

Your PRD captures the functional requirements, but File 1's transcript reveals critical UX nuances:

- **Encrypted Votes via GPG**: File 1's "hidden messages" concept maps to `FR-COU-06`. Use gossip protocol: agents encrypt votes with council public key, preventing retaliation while maintaining auditability.
- **Two-Strike Termination**: File 1's heuristic shows termination is a **last resort**. Modify `FR-COU-05` to require **two consecutive consensus failures** before termination to avoid false positives.
- **Live Vote Timeline UI**: File 1's visual concept map should directly inform your Agent Monitor dashboard (`FR-UI-04`). Show real-time vote scores with red/yellow/green indicators.

**Action Item**: Implement the `/council spawn --size=5 --encrypted` slash command with a 30s vote window and auto-termination on second failure.

### **4. Pre/Post Tool Use Hooks for Quality Preservation**
*Source: File 3 (Degradation) + File 4 (AIME) | PRD Alignment: FR-HOOK-01*

**Implementation Readiness:** ✅ **Deploy Now**

This prevents the "structural degradation" from File 3 at the source:

- **PreToolUse Hook = Format Enforcer**: For `Write(src/**.rs)`, auto-run `rustfmt` (File 4's example). This is your "Structural Maintenance" from File 3.
- **PostToolUse Hook = Context Verifier**: Inject a prompt hook that checks if the agent's output maintains narrative flow (File 3's "Context Loss" metric). If context score drops >15%, trigger a RED lane "re-narrativize" task.
- **SessionStart Hook**: Auto-prime tools using the progressive disclosure pattern, preventing format momentum drift.

**Action Item**: Ship with 5 default hooks: `rustfmt`, `black`, `ruff`, `prettier`, and a `context-preservation` LLM guardrail.

---

## 🔭 **Horizon Plan (3-12 Months)**

These capabilities require research, infrastructure maturity, or ecosystem adoption before implementation.

### **5. Skills-Based Bundling with Ecosystem Lock-in**
*Source: File 1 (Skills-Based) | PRD Alignment: FR-SKL-01*

**Implementation Readiness:** ⚠️ **Defer to v2.0**

While the PRD includes skills (`FR-SKL-01`), File 1 warns of **"Clawed ecosystem lock-in"**. The horizon strategy should be:

- **Phase 1 (Now)**: Implement skills as **portable directories** with `SKILL.md` + `scripts/` but **do not** integrate with Claude Code's native skill system.
- **Phase 2 (Horizon)**: Only after SwarmForge reaches 1000+ users and 50+ skills, **then** consider native integration for the network effect. Until then, maintain MCP import/export parity to avoid lock-in.

**Risk Mitigation**: The PRD's "Anti-Goal: Ecosystem lock-in" is contradicted by skills. Horizon plan should include a `swarmforge export-skill` command that converts skills to script-based format for portability.

### **6. Automated Documentation Degradation Detection**
*Source: File 3 (Structural Degradation) | PRD Alignment: Not in PRD*

**Implementation Readiness:** 🔬 **Research Phase**

File 3's methodology provides a roadmap for autonomous quality monitoring:

- **Degradation Classifier**: Train a small LM (DistilBERT) on the three failure modes:
  1. Progressive Simplification (sentence complexity < threshold)
  2. Format Momentum (list density > 60%)
  3. Context Loss (concept-to-jargon ratio < 0.3)
- **Intervention Protocol**: When degradation detected >20%, spawn a `documentation-savior` agent (RED lane) that rewrites the section using progressive disclosure.

**Why Horizon**: Requires 1000+ document samples for training. Build this as an **optional audit tool** in v1.0, then graduate to auto-intervention in v2.0.

**Action Item**: Add a `/audit-docs` slash command in v1.0 that runs File 3's six metrics and generates a degradation report.

### **7. Multi-Modal Completion Assessment Enhancement**
*Source: File 2 (Visual Hooks) + File 4 (Vision Validation) | PRD Alignment: FR-VAL-01**

**Implementation Readiness:** ⚡ **Enhance Current Implementation**

Your PRD's completion assessment (`FR-VAL-01`) uses Playwright + Claude Sonnet. File 2 adds critical UX principles:

- **First 15-Second Hook**: The validation agent should **prioritize above-the-fold UI elements** in the screenshot. Weight the scoring algorithm: 40% first viewport, 30% interaction flow, 30% design fidelity.
- **Voice-Over for Accessibility**: File 2's narration strategies suggest adding an optional `audio_description` field to the validation JSON, making UI changes accessible to visually impaired developers.

**Horizon Enhancement**: Integrate with Figma API to auto-compare against design mocks (File 2's "Synchrony of Verbal and Visual").

**Action Item**: Modify the vision prompt to include: `"Focus assessment on the first 15 seconds of user experience. Weight visual completeness at 40% for above-fold content."`

### **8. Model-Agnostic Routing with Cost-Aware Fallback**
*Source: File 1 (Cost Optimization) | PRD Alignment: FR-RTR-01**

**Implementation Readiness:** 🚀 **Scale in v1.0, Enhance in v2.0**

Your routing is functional but lacks **cost-awareness** from File 1's "$242/month" target:

- **Dynamic Price Arbitrage**: Monitor OpenRouter's real-time pricing. If `claude-sonnet` cost spikes >2×, auto-route to `gemini-1.5-pro` for YELLOW/RED tasks.
- **Token Recycling**: For GREEN lane tasks, cache embeddings of successful tool calls. If a worker repeats a similar task within 24h, retrieve from cache instead of re-running.

**Horizon Metric**: Achieve the **98% cost reduction** by implementing a **cost-based router** that minimizes spend per task type, not just latency.

**Action Item**: Add `cost_per_1k_tokens` to routing rules and implement a `cost_optimizer` agent that auto-tunes rules weekly.

### **9. Cross-Project Memory Injection**
*Source: File 4 (Future Capability) | PRD Alignment: FR-MEM-06**

**Implementation Readiness:** 🧠 **v2.0 Infrastructure**

File 4 mentions "Knowledge Injection" as future capability. The horizon plan:

- **ReasoningBank Expansion**: Store not just successful tasks, but **failed council votes** and **termination rationales**. Use these as negative examples for future CEO agents.
- **Cross-Project Pattern Matching**: When Alex's `rust-migrator` agent solves a deadlock in Service A, auto-index the solution pattern. When Priya's team faces similar issue in Service B, proactively inject the resolution path.

**Why Horizon**: Requires stable AgentDB schema and 10k+ memory entries for pattern emergence. Build the ingestion pipeline in v1.0, activation in v2.0.

**Action Item**: Add `shared: true` flag to AgentDB schema and implement a `pattern-miner` agent that runs weekly to extract reusable solution templates.

---

## 📊 **Implementation Priority Framework**

I've mapped each concept to your PRD's implementation phases:

| **Immediate (Now-3mo)** | **Horizon (3-12mo)** | **Research (12mo+)** |
|-------------------------|----------------------|----------------------|
| CLI-first tool priming | Skills-based bundling (v2.0) | Degradation classifier |
| Script-based progressive disclosure | Automated doc degradation detection | Multi-accent voice synthesis |
| Color-coded routing | Multi-modal assessment (Figma) | Neural compiler (v3.0) |
| Council voting (GPG) | Cost-aware routing arbitrage | AI-to-AI marketplace |
| Pre/Post hooks (format enforcers) | Cross-project memory injection | Autonomous company (v3.0) |
| Voice scripting (UX) | ReasoningBank expansion | |

---

## 🎯 **Critical Path Recommendation**

**For v1.0 (Weeks 1-18):** Focus on **File 1 + File 4 synergy**:
1. Use CLI-first pattern to achieve the PRD's <2k token target
2. Implement Color-Coded Framework with environment-specific adaptations (Roo Code AST injection)
3. Enforce quality via hooks that prevent File 3's degradation patterns

**For v2.0 (Beyond):** Leverage **File 2 + File 3 intelligence**:
1. Build the degradation classifier from File 3 as an autonomous RED lane task
2. Enhance validation with File 2's "first 15-second" UX weighting
3. Accept skills-based lock-in *only after* establishing portability standards

This creates a **virtuous cycle**: Low-context agents (File 1) → effective orchestration (File 4) → preserved quality (File 3) → trusted automation (SwarmForge's core value).





















# Reassessment: Document-to-PRD Integration Mapping

You're correct—the PRD is the implementation plan, and the four documents are external research inputs. Re-analyzed from this perspective, here's where each document's ideas fit into your 18-week SwarmForge timeline.

---

## 📋 **Executive Summary: Integration vs. Deferral**

| Document | Key Idea | PRD Coverage | Recommendation |
|----------|----------|--------------|----------------|
| **File 1 (MCP Alternatives)** | Script-based progressive disclosure, CLI priming, toolbelt heuristic | ✅ **Well-covered** in FR-SCR, FR-CLI, FR-SKL | **Integrate tactical constraints** into Phase 0-1 |
| **File 2 (Voice/Accent)** | Voice-driven retention, A/B testing, accent perception | ❌ **Not covered** (UX layer) | **Defer to Phase 4** dashboard polish; low engineering priority |
| **File 3 (Doc Degradation)** | Structural degradation monitoring, quality metrics | ❌ **Not covered** (meta-concern) | **Add as Phase 5 gate**; low dev effort, high long-term value |
| **File 4 (AIME Architecture)** | Color-coded lanes, Actor Factory, Dynamic Planner | ✅ **Foundation of PRD** | **Align terminology**; PRD extends AIME with specifics |

---

## 🔧 **Immediate Integration (Phase 0-1): Missing Tactical Details from File 1**

Your PRD captures the *what* but lacks File 1's *how* constraints. Add these to Phase 0:

### **Phase 0 Enhancement: Script Executor Hard Constraints**
```rust
// Add to Execution Engine spec (Section 5.1)
fn execute_script(name: &str) -> Result<Output> {
    // ENFORCE: Script source never enters context
    let prime_prompt = format!(
        "Execute 'uv run scripts/{}.py --json'. \
         DO NOT read the script file. Rely only on --help output.",
        name
    );
    // ENFORCE: Help-on-failure retry
    if output.status != 0 {
        let help = Command::new("uv").args(&["run", &script, "--help"]).output()?;
        // Re-prompt agent with help text only
    }
}
```

**Why Critical**: Without this constraint, agents will read scripts, inflating context to 10k+ tokens. This is the single most important detail from File 1.

### **Phase 1 Enhancement: Two-Strike Termination Rule**
Update `FR-COU-05`:
- **Original**: Terminate on first consensus failure
- **File 1 Integration**: Require **two consecutive failures** before termination
- **Rationale**: Prevents false positives from transient errors; aligns with "last resort" philosophy

**Code Change**:
```yaml
# In council config
termination_policy:
  consecutive_failures: 2  # Add this field
  quorum_threshold: 0.8
```

---

## 🎨 **Near-Term Integration (Phase 4): Voice & Accent UX from File 2**

File 2 is about **human voice perception**—but your agents don't speak. However, its principles apply to **dashboard UX and agent communication style**.

### **Phase 4 Dashboard Enhancement: "Agent Voice & Tone Chart"**
Add to Section 4.6.1:
- **Agent Card Voice Persona**: Each agent displays 3 adjectives: "Authoritative, Precise, Fast" vs. "Empathetic, Thorough, Cautious"
- **First 15-Second Hook**: When user clicks an agent, the first log line must state value: *"I am performance-optimizer. I will reduce your API latency by analyzing 5 hotspots."*
- **Pattern Interrupt Visuals**: Agent status changes (waiting → working → completed) should use color/pacing variations to maintain attention (File 2's "vocal variety" principle)

**Implementation**: Add `voice: { adjectives: [...], tone: "authoritative" }` to agent YAML. Use in UI rendering.

### **Phase 4 A/B Testing: Agent Persona Optimization**
File 2's A/B protocol can test agent **communication style**:
- **Hypothesis**: For `security-auditor` agent, "authoritative" tone yields higher user trust (measured by approval rate) than "friendly" tone.
- **Method**: Sequential testing—Week 1 uses authoritative persona, Week 2 friendly, measure `/approve` vs. `/reject` commands.

**Why Defer**: Needs 100+ daily interactions for significance. Build infrastructure in Phase 4, activate when user base grows.

---

## 🔬 **Long-Term Integration (Phase 5): Documentation Quality from File 3**

File 3's degradation patterns threaten your `.claude/agents/*.md` files as you scale to 50+ agents.

### **Phase 5 Quality Gate: Agent Doc Linter**
Add to Section 4.8.1 (`PreToolUse` hooks):
```json
{
  "matcher": "Write(.claude/agents/**.md)",
  "hooks": [{
    "type": "command",
    "command": ".claude/hooks/agent-doc-linter.sh"
  }]
}
```

**Linter Script** (implements File 3's metrics):
- **Progressive Simplification**: Fail if average sentence length drops >30% in later sections
- **Format Momentum**: Fail if bullet list ratio exceeds 60% of content
- **Context Loss**: Fail if "concept-to-detail" ratio <0.5 (count `### Concept` vs `#### Detail` headings)

**Why Phase 5**: Low priority until you have 10+ complex agent definitions. But critical for maintainability at scale.

---

## 🏗️ **Foundation Alignment: File 4 vs. PRD**

File 4 is **theoretical**; your PRD is **concrete**. The PRD correctly extends AIME with specifics:

| AIME Concept (File 4) | SwarmForge Implementation (PRD) | Alignment Status |
|-----------------------|---------------------------------|------------------|
| Dynamic Planner | Orchestration Layer (Go) + Temporal | ✅ Extended with cost tracking |
| Actor Factory | Agent spawn via YAML + context isolation | ✅ Added resume capability (`agent-{id}.jsonl`) |
| Color-Coded Lanes | GREEN/YELLOW/RED/GRAY with ONNX routing | ✅ Added thresholds & fallback logic |
| Progress Management | `taskmaster-ai` module | ✅ Enhanced with memory DB |

**No changes needed**—your PRD is already a superset of AIME. Just **align terminology** in code comments for clarity.

---

## ⚠️ **Explicit Deferrals: Ideas to Reject or Postpone**

### **Reject: Multi-Accent Voice Synthesis (File 2)**
- **Why**: Agents don't speak audio. TTS for dashboard notifications adds complexity without ROI.
- **Decision**: Exclude from all phases. Revisit in v3.0 if you build a voice interface.

### **Postpone: Skills-Based Ecosystem Lock-in (File 1)**
- **Why**: PRD's FR-SKL adds value, but "Clawed ecosystem lock-in" is an anti-goal (Section 2.3).
- **Decision**: Implement FR-SKL as **portable directories** in Phase 0, but **do not** integrate with Claude Code's native skill system until v2.0. Maintain MCP import/export as escape hatch.

### **Postpone: Automated Degradation Recovery (File 3)**
- **Why**: Auto-rewriting agent docs is risky. Human review is safer until you have 1000+ examples of good vs. degraded docs.
- **Decision**: Implement linter (Phase 5) but **manual fix only**. Add `/agent-doc-fix` slash command in v2.0 that spawns a RED lane agent to rewrite, but require human approval.

---

## 📅 **Revised Phase Plan with Document Integration**

### **Phase 0 (Weeks 1-2): Foundation**
- **Add**: Script executor constraint (File 1)
- **Add**: `.claude/hooks/agent-doc-linter.sh` stub (File 3)
- **Keep**: All existing deliverables

### **Phase 1 (Weeks 3-5): Delegation**
- **Modify**: Subagent spawn to include two-strike termination (File 1)
- **Add**: `color_lane` field to agent YAML (File 4)
- **Keep**: Resume logic, CEO-worker pattern

### **Phase 4 (Weeks 12-14): Validation & UI**
- **Add**: Agent voice personas in UI (File 2)
- **Add**: Agent doc linter activation (File 3)
- **Keep**: Playwright validation, SvelteKit dashboard

### **Phase 5 (Weeks 15-18): Hardening**
- **Add**: A/B testing infrastructure for personas (File 2)
- **Keep**: RBAC, SAML, scaling

---

## 🎯 **Final Recommendation: Focus on File 1's Constraints**

The highest-impact integration is **File 1's "DO NOT READ SCRIPTS" constraint**. Without it, your script-based tool pattern (`FR-SCR-01`) will degrade into MCP-like context bloat. **Add this as a hard rule in Phase 0 execution engine—no exceptions.**

Everything else (voice, doc quality, accents) is optimization. **Ship v1.0 with rock-solid script isolation, then iterate.**














# Strategic Implementation Roadmap: SwarmForge Multi-Agent Platform

## Executive Summary of Core Concepts

The following concepts from external research provide proven patterns for reducing token overhead by 94%, preventing documentation decay, and optimizing human-agent interaction. These ideas are categorized by implementation readiness and integrated directly into your 18-week development timeline.

---

## 🚀 **Immediate Implementation (Phase 0-2): Core Patterns Ready for Deployment**

### **1. Script-Based Progressive Disclosure for Tool Integration**

**Concept**: Instead of loading full tool code into context, the agent reads only a high-level mapping file (`readme.md`) that connects user intents to specific scripts. The agent is explicitly forbidden from reading script source code and must execute them via `uv run scripts/{name}.py --json`, loading only the output into context. This achieves <2k token overhead per tool activation—a 94% reduction from traditional MCP servers.

**Implementation Details**:
- Create a single `readme.md` in `apps/3-file-system/` that maps conditions to scripts (e.g., "When user searches, use `search.py`")
- Prime prompt must contain the strict constraint: **"DO NOT read scripts themselves unless --help fails"**
- Scripts must be self-contained with dependencies in `pyproject.toml` and mandatory `--help` flags
- Agent queries `--help` on ambiguity, never reads source
- Versioning support: `scripts/v1/search.py`, `scripts/v2/search.py`

**SwarmForge Integration**:
- Add to Phase 0: Create `swarmforge prime-script` CLI that auto-generates the two-file structure
- Modify `FR-SCR-02` in PRD: Replace "explicitly forbids" with the exact phrasing:  **"DO NOT READ THE SCRIPTS THEMSELVES; rely only on --help output"**  —this is critical for context preservation
- Script failure handling: Non-zero exit triggers auto-retry with `--help` parse, no source code inspection

**Expected Impact**: Context overhead drops from 10k tokens (MCP) to <2k tokens per tool, enabling 50+ tools within 50k token budget.

---

### **2. CLI-First Tool Priming Pattern**

**Concept**: On-demand context loading via prime commands (e.g., `/prime-kshi-cli-tools`). The agent reads only two files: a `readme.md` explaining workflows and a `cli.py` defining commands. This reduces context waste from 10% to 5.6% while giving developers full control.

**Implementation Details**:
- User runs prime prompt (e.g., `/prime-kshi-cli-tools`)
- Agent reads: `apps/1-cli/readme.md` + `apps/1-cli/cli.py`
- Agent summarizes capabilities then accepts natural language commands
- Command translation: "market search trillionaire" → `market search "trillionaire"`
- Supports argument inference (synonyms: "find" → "search")

**SwarmForge Integration**:
- Add to Phase 0: `swarmforge prime-cli --tool={name}` command
- Create template `cli.py` with argparse/click definitions and auto-generated `readme.md`
- Include in `FR-CLI-04`: Agent must map synonyms to reduce user memorization
- Prime latency target: <2s for file read + summarize

**Expected Impact**: 44% context reduction, immediate usability improvement for custom CLIs.

---

### **3. Color-Coded Strategic Task Routing**

**Concept**: A four-lane classification system that guides task decomposition:
- **GREEN**: Direct execution (file manipulation, simple commands)
- **YELLOW**: Pattern-based development (find pattern → implement)
- **RED**: Deep dynamic planning (sub-planning, CEO-worker hierarchy)
- **GRAY**: Summarization & archival

**Implementation Details**:
- GREEN lane: Instantiate "File Agent" with `filesystem` tool only
- YELLOW lane: Use "Template Agent" with pattern-matching tools
- RED lane: "Lead Engineer Agent" with `mcp-sequentialthinking-tools` and delegation authority
- GRAY lane: "Librarian Agent" for memory archival

**SwarmForge Integration**:
- Add `color_lane` field to `.claude/agents/*.md` YAML frontmatter
- Phase 1: Implement GREEN and YELLOW lanes for majority of tasks
- Phase 2: RED lane for complex planning tasks requiring sub-agent spawning
- Environment adaptations:
  - **Roo Code**: Inject AST analysis as "Knowledge" component per File 4
  - **OpenCoder**: Favor shell-based actors (`uv run`, `cargo run`)
  - **OpenHands**: Use as orchestrator for existing micro-agents

**Expected Impact**: Clear task routing reduces planner cognitive load, enables environment-specific optimizations.

---

### **4. Council Voting with Byzantine Fault Tolerance**

**Concept**: Group of 5 agents votes on completion quality using structured JSON: `{"agent_id": "a1", "target_id": "a3", "score": 0.0/0.5/1.0, "rationale": "..."}`. Consensus threshold is 0.8; if not met, lowest-voted agent is terminated. Votes can be GPG-encrypted to prevent retaliation.

**Implementation Details**:
- Council size: 5 agents (configurable)
- Quorum: `ceil(n/2) + 1 = 3` votes required
- Vote aggregation: Excluding self-votes, identify lowest-scoring agent
- Termination: `pkill -f agent-{id}` with graceful state handoff to `agent-{id}.jsonl` transcript
- Two-strike rule: Require consecutive failures to prevent false positives
- Encrypted votes: GPG with council public key for hidden messages

**SwarmForge Integration**:
- Phase 2: Implement Temporal workflow for council rounds
- Add `FR-COU-06`: GPG encryption option for sensitive votes
- Modify termination logic: Two failed votes required
- Dashboard UI: Real-time vote timeline with red/yellow/green indicators

**Expected Impact**: Prevents production outages by catching flawed migrations before commit.

---

### **5. Pre/Post Tool Use Hooks for Quality Preservation**

**Concept**: Bash scripts or LLM prompts that execute before/after tool use for validation, logging, and auto-fix. Exit codes control flow: `0`=allow, `2`=block. Environment variables expose context: `$CLAUDE_PROJECT_DIR`, `$CLAUDE_TOOL_NAME`, `$CLAUDE_TOOL_INPUT`.

**Implementation Details**:
- Hook types: `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`
- Matcher patterns: `Write(src/**.rs)`, `Bash(cargo *)`
- Command hooks: `.claude/hooks/rust-fmt-check.sh` (latency <100ms)
- Prompt hooks: Haiku-evaluated context decisions (<500ms)
- JSON output: `{"decision": "allow|deny", "updatedInput": {...}}`
- Session hooks: Persist env vars via `$CLAUDE_ENV_FILE`

**SwarmForge Integration**:
- Phase 0: Ship with 5 default hooks: `rustfmt`, `black`, `ruff`, `prettier`, `context-preservation-guard`
- Add to `FR-HOOK-04`: JSON output for granular control
- SessionStart hook auto-primes tools using progressive disclosure pattern

**Expected Impact**: 84% reduction in permission prompts, automatic enforcement of code quality standards.

---

### **6. Agent Resume Capability with Transcript Storage**

**Concept**: Each agent writes its entire context to `agent-{id}.jsonl` on termination. On resume, the transcript is rehydrated from AgentDB, restoring state without context loss.

**Implementation Details**:
- Transcript format: JSONL with messages, tool calls, and reasoning
- Storage: Local SQLite for dev, PostgreSQL for production
- Resume trigger: `resume: {agentId}` in YAML or CLI
- Cross-session persistence: Weekend shutdown → Monday restart with full context
- Memory rehydration: Query AgentDB for related tasks, inject as "Known Patterns"

**SwarmForge Integration**:
- Phase 1: Implement `FR-DEL-04` transcript write/read
- Add to AgentDB schema: `agent_memory(agent_id, task_id, content, embedding, access_count)`
- Auto-summarization: When transcript >10k tokens, spawn summarizer agent to compress to 1k

**Expected Impact**: Zero context loss between sessions, enables long-running tasks.

---

## 🔭 **Horizon Plan (Phase 3-5): Future Capabilities Requiring Research or Scale**

### **7. Skills-Based Bundling with Lock-in Mitigation**

**Concept**: Self-contained directories (`skills/{name}/`) with `SKILL.md`, scripts, and resources. Uses three-tier loading: metadata (100 tokens) always loaded, instructions loaded on trigger, scripts loaded on-demand. This creates ecosystem lock-in but provides isolation.

**Why Deferred**: File 1 warns of **"Clawed ecosystem lock-in"**—a direct tradeoff with your PRD's portability goals. Implement in Phase 0 as portable directories, but **defer native Claude Code integration** until v2.0 when you have 50+ skills and can justify the lock-in cost.

**Implementation Path**:
- Phase 0: Build skills as portable directories with YAML frontmatter
- Phase 3: Add `skills/` directory auto-discovery and activation
- v2.0 Decision: Integrate with Claude Code's native skill system only if portability escape hatch (`swarmforge export-skill`) is maintained

**Expected Impact**: High portability for small skill libraries; strategic lock-in decision deferred until ecosystem maturity.

---

### **8. Automated Documentation Degradation Detection**

**Concept**: Train a classifier to detect the three degradation patterns from File 3:
1. **Progressive Simplification**: Sentence complexity drops >30% in later sections
2. **Format Degradation**: List density exceeds 60% of document
3. **Context Loss**: Concept-to-detail ratio falls below 0.5

**Why Deferred**: Requires 1000+ labeled examples of good vs. degraded agent docs. Build infrastructure in Phase 5 but activate auto-fix only after manual monitoring validates accuracy.

**Implementation Path**:
- Phase 5: Add `/audit-docs` slash command that runs linter and generates degradation report
- v2.0: Promote to auto-fix with human approval gate
- v3.0: Full autonomous rewriting of degraded sections by RED lane agents

**Expected Impact**: Prevents long-term maintainability collapse; reduces technical debt growth.

---

### **9. Multi-Modal Completion Assessment Enhancement**

**Concept**: Extend Playwright validation with File 2's UX principles: prioritize above-the-fold content (40% weight), test first 15-second user experience, and add audio descriptions for accessibility.

**Why Deferred**: Requires Figma API integration and accessibility tooling. Current Playwright + Claude Sonnet is sufficient for MVP.

**Implementation Path**:
- Phase 4: Basic screenshot + design doc comparison
- v2.0: Add Figma API integration for pixel-perfect mockup comparison
- v2.0: Add `audio_description` field to validation JSON for screen reader support

**Expected Impact**: Catches UI/UX regressions that pure visual diff misses; improves accessibility compliance.

---

### **10. Cost-Aware Model Routing with Token Recycling**

**Concept**: Monitor OpenRouter's real-time pricing and route to cheapest adequate model. Cache embeddings of successful tool calls to avoid re-execution on similar tasks.

**Why Deferred**: Requires pricing API integration and similarity detection infrastructure. Current static routing rules are sufficient for v1.0.

**Implementation Path**:
- Phase 3: Add `cost_per_1k_tokens` to routing rules
- Phase 3: Implement LRU cache for GREEN lane tool outputs
- v2.0: Add `cost_optimizer` agent that auto-tunes rules weekly based on spend analytics

**Expected Impact**: Achieves 98% cost reduction target by dynamic arbitrage rather than static rules.

---

### **11. Cross-Project Memory Injection**

**Concept**: Store failed council votes and termination rationales as negative examples. When similar task patterns emerge, proactively inject resolution paths into CEO agent's context.

**Why Deferred**: Requires 10k+ memory entries for pattern emergence and robust similarity search. Build ingestion in Phase 1, activation in v2.0.

**Implementation Path**:
- Phase 1: Add `shared: true` flag to AgentDB schema for cross-agent memories
- Phase 3: Build `pattern-miner` agent that extracts reusable templates weekly
- v2.0: CEO agents auto-query pattern DB before RED lane planning

**Expected Impact**: Reduces planning time by 30% through learned heuristics; prevents repeat failures.

---

## 📊 **Implementation Priority Matrix**

| **Concept** | **Effort** | **Impact** | **Risk** | **Phase** |
|-------------|------------|------------|----------|-----------|
| Script-based progressive disclosure | Low | Very High | Very Low | **Phase 0** |
| CLI-first priming | Low | High | Very Low | **Phase 0** |
| Color-coded routing (GREEN/YELLOW) | Medium | Very High | Low | **Phase 0-1** |
| Council voting (two-strike) | Medium | Very High | Medium | **Phase 2** |
| Pre/Post hooks (5 defaults) | Low | High | Low | **Phase 0** |
| Agent resume capability | Medium | High | Low | **Phase 1** |
| Skills-based bundling (portable) | Medium | Medium | Medium | **Phase 3** |
| Doc degradation linter | Low | Medium | Low | **Phase 5** |
| Multi-modal assessment (Figma) | Medium | Medium | Low | **v2.0** |
| Cost-aware routing | Medium | High | Medium | **v2.0** |
| Cross-project memory | High | Very High | Medium | **v2.0** |

---

## 🎯 **Critical Path Recommendation**

**Phase 0-2 Focus**: Implement **File 1's script isolation constraints** and **File 4's color-coded routing** simultaneously. This creates your core value proposition: low-context, high-control agents.

**Phase 3-5 Focus**: Build **File 3's degradation monitoring** as a passive audit tool. Activate auto-fix only after you have 50+ agents and 1000+ docs to train on.

**Post-v1.0**: Evaluate **File 2's UX principles** for dashboard polish and A/B testing agent personas. This is low engineering cost but high user impact.

**Reject**: Multi-accent voice synthesis—agents don't speak, and TTS adds complexity without solving core orchestration problems.

The roadmap now balances immediate tactical wins (context reduction, quality enforcement) with strategic bets (cost arbitrage, pattern learning) that mature as your agent ecosystem scales.

























# **Product Requirements Document: SwarmForge – Intelligent Multi-Agent Orchestration Platform**

**PRD Version:** 3.1 (Revised)  
**Date:** 2025-11-18  
**Authors:** Product & Engineering Team  
**Status:** Pre-Development – Ready for Implementation  
**Classification:** Internal – Engineering & Product Alignment

---

## 1. Executive Summary

SwarmForge is an enterprise-grade orchestration platform that transforms Claude Code from a single-agent assistant into a resilient, cost-efficient swarm of specialized AI agents. By replacing traditional MCP servers with progressive disclosure patterns and implementing council-based consensus protocols, SwarmForge achieves **10× faster task completion** at **98% lower cost** while scaling to 100+ concurrent tools.

This revision integrates three proven external patterns: **script-based progressive disclosure** (reducing context overhead to <2k tokens), **color-coded strategic routing** (adapting agent architecture to host environments), and **council-based Byzantine fault tolerance** (terminating underperforming agents via peer vote). The platform will leverage Claude Code as an external dependency while forking and heavily modifying two open-source projects: `apolopena/multi-agent-workflow` (for hooks and observability) and `aaaronmiller/claude-code-proxy` (for model-agnostic routing).

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

**Description**: Implements Byzantine fault tolerance via peer review. Agents vote on completion quality; lowest-voted agent terminated after two consecutive consensus failures to prevent false positives. Votes can be GPG-encrypted to prevent retaliation.

**Functional Requirements**:
- **FR-COU-01**: Council size configurable (default `n=5` agents)
- **FR-COU-02**: Vote casting via structured JSON: `{"agent_id": "a1", "target_id": "a3", "score": 0.0/0.5/1.0, "rationale": "..."}`
- **FR-COU-03**: Quorum threshold configurable (default `ceil(n/2) + 1 = 3`)
- **FR-COU-04**: Consensus threshold configurable (default `0.8`)
- **FR-COU-05**: Two-strike termination: Identify lowest-voted agent after second consecutive failure
- **FR-COU-06**: Encrypted votes via GPG gossip protocol to prevent retaliation while maintaining auditability
- **FR-COU-07**: Termination triggers graceful state handoff: agent writes `agent-{id}.jsonl` transcript, hub redistributes pending tasks
- **FR-COU-08**: Visual UI shows live vote timeline, scores, and termination events

**Non-Functional Requirements**:
- **NFR-COU-01**: Voting round latency <200ms end-to-end
- **NFR-COU-02**: Termination must be atomic: no partial task commits
- **NFR-COU-03**: Council token overhead ≤5× single-agent cost (acceptable for critical tasks)

**User Story**: Alex delegates a complex DB migration to a council. The `schema-migrator` agent proposes a flawed migration; peers vote it down twice (scores 0.3, 0.2). It is terminated, and the `rollback-expert` agent inherits its state, preventing a production outage.

---

#### 4.1.2 Agent Subagent Delegation

**Description**: Hierarchical task decomposition with isolated contexts and explicit trust graphs. Subagents resume from transcript files, enabling zero-loss state recovery.

**Functional Requirements**:
- **FR-DEL-01**: Subagent configuration via YAML frontmatter in `.claude/agents/*.md`
- **FR-DEL-02**: Support `delegatees: [agent-a, agent-b]` field defining explicit delegation graph
- **FR-DEL-03**: Subagent context isolation: each spawn receives clean slate, no parent context pollution
- **FR-DEL-04**: Resume capability: subagent transcripts stored as `agent-{id}.jsonl`, resumable via `resume: {agentId}`
- **FR-DEL-05**: PreToolUse/PostToolUse hooks can intercept delegation for audit/logging
- **FR-DEL-06**: Automatic delegation via semantic matching: agent `description` fields indexed in AgentDB, matched against task embeddings
- **FR-DEL-07**: Max delegation depth configurable (default `3`) to prevent infinite recursion

**Non-Functional Requirements**:
- **NFR-DEL-01**: Subagent spawn latency <500ms (including context priming)
- **NFR-DEL-02**: Independent tool access: subagent tools restricted to `tools` field; parent tools not inherited unless specified
- **NFR-DEL-03**: Memory overhead per subagent <50MB

**User Story**: Priya defines a `security-auditor` agent that automatically delegates static analysis to `bandit-agent`, dependency scanning to `snyk-agent`, and secret detection to `trufflehog-agent`. Each runs in parallel, returning JSON reports that the auditor synthesizes.

---

#### 4.1.3 Model-Agnostic Task Routing

**Description**: Proxy shim that intercepts model calls and routes based on task signature, cost, and latency. Integrates `aaaronmiller/claude-code-proxy` as a foundation, extending it with cost-aware fallback and local model prioritization.

**Functional Requirements**:
- **FR-RTR-01**: Claude Code proxy implements `ModelProvider` interface; transparent to agents
- **FR-RTR-02**: Task classification via ONNX model (DistilBERT, 50MB) with 92% accuracy
- **FR-RTR-03**: Routing rules configurable in `.claude/settings.json` with patterns, cost limits, and confidence thresholds
- **FR-RTR-04**: Fallback logic: If local model returns low confidence (`<0.7`), auto-retry with `claude-sonnet`
- **FR-RTR-05**: Provider abstraction: Support OpenRouter, local vLLM, Claude API, Gemini via unified interface
- **FR-RTR-06**: Cost tracking per agent per task; exposed via `/cost` slash command
- **FR-RTR-07**: Latency SLO enforcement: If local model exceeds 100ms, timeout and fallback
- **FR-RTR-08**: Dynamic price arbitrage: Monitor OpenRouter pricing, route to cheapest adequate model
- **FR-RTR-09**: Token recycling cache for GREEN lane tasks to avoid re-execution

**Non-Functional Requirements**:
- **NFR-RTR-01**: Routing latency <5ms per call
- **NFR-RTR-02**: No API calls during optimization (<5ms decision overhead)
- **NFR-RTR-03**: Support 27+ model providers

**User Story**: Alex runs a load test script. The proxy routes 1000 calls to `local-qwen2.5-3b` at $0.01 total cost. One call hits an edge case (low confidence); it auto-fallbacks to Claude Sonnet, spending $0.15 to ensure correctness. Total cost $0.16 vs. $200 with Claude-only.

---

### 4.2 Tool Integration & Progressive Disclosure

#### 4.2.1 Script-Based Tool Execution (Primary Pattern)

**Description**: Most advanced pattern; agent reads only intent→script mapping; script source never enters context. This achieves <2k token overhead per tool activation.

**Functional Requirements**:
- **FR-SCR-01**: Single `readme.md` maps conditions (user intents) to script files
- **FR-SCR-02**: Prime prompt explicitly forbids reading script source:  **"DO NOT READ THE SCRIPTS THEMSELVES unless --help fails"**  —this is the critical constraint
- **FR-SCR-03**: Agent calls scripts via `uv run scripts/{name}.py --json`; only output enters context
- **FR-SCR-04**: Scripts must be self-contained: dependencies in `pyproject.toml`, arg parsing via `argparse`/`click`
- **FR-SCR-05**: `--help` flag mandatory; agent queries it for usage on ambiguity
- **FR-SCR-06**: Support script versioning: `scripts/v1/search.py`, `scripts/v2/search.py`
- **FR-SCR-07**: Script registry: `scripts/index.json` with metadata for auto-discovery

**Non-Functional Requirements**:
- **NFR-SCR-01**: Context overhead <2k tokens per tool activation (94% reduction)
- **NFR-SCR-02**: Script execution overhead <100ms (excluding tool logic)
- **NFR-SCR-03**: Script failure triggers agent retry with `--help` parse, never source inspection

**User Story**: Alex’s agent needs 50 tools (GitHub, Slack, DB, deploy, monitor). Rather than loading 50k tokens of MCP schemas, it loads a <2k token `readme.md`. Each script is called on demand; context grows only with output, not code.

---

#### 4.2.2 CLI-First Priming Pattern (Secondary)

**Description**: Agent reads `readme.md` + `cli.py` on-demand; full control, moderate context cost (5.6% vs. 10% MCP baseline).

**Functional Requirements**:
- **FR-CLI-01**: Prime prompt command instructs agent to read two files (`readme.md` + `cli.py`)
- **FR-CLI-02**: Agent summarizes capabilities after reading; user can issue natural language commands
- **FR-CLI-03**: Agent translates commands to CLI calls: "market search trillionaire" → `market search "trillionaire"`
- **FR-CLI-04**: Support argument inference: agent maps synonyms (e.g., "find" → "search")

**Non-Functional Requirements**:
- **NFR-CLI-01**: Context reduction from 10% → 5.6% (44% savings)
- **NFR-CLI-02**: Priming latency <2s for 2-file read + summarize

**User Story**: Dan has a custom CLI for his startup's infra. He primes the agent; it learns 10 commands. He can now say "deploy staging" instead of memorizing `deploy.py --env staging --branch main`.

---

#### 4.2.3 Skills-Based Bundling (Tertiary)

**Description**: Self-contained directory with `SKILL.md`, scripts, resources; three-tier loading (metadata → instructions → resources) for minimal idle cost.

**Functional Requirements**:
- **FR-SKL-01**: Directory structure: `skills/{name}/SKILL.md`, `scripts/`, `resources/`
- **FR-SKL-02**: `SKILL.md` uses YAML frontmatter: `name`, `description`, `triggers`
- **FR-SKL-03**: Three-tier loading (Anthropic pattern):
  - Level 1: Metadata (100 tokens, always loaded)
  - Level 2: `SKILL.md` instructions loaded when triggered (<5k tokens)
  - Level 3: Scripts/resources loaded on-demand (zero token cost if unused)
- **FR-SKL-04**: Auto-discovery: Claude Code scans `~/.claude/skills/` and `./.claude/skills/` on startup
- **FR-SKL-05**: Hooks integration: `PostToolUse` can auto-activate skill if tool pattern matches

**Non-Functional Requirements**:
- **NFR-SKL-01**: Portable: `cp -r skills/kshi-markets .claude/skills/` activates instantly
- **NFR-SKL-02**: Isolated: skill dependencies contained within directory

**User Story**: Priya builds a "security-scan" skill with 5 scripts and 20MB of CVE databases. It costs 100 tokens at idle; when triggered, loads <5k tokens of instructions; CVE DB is queried via script, never loaded into context.

---

#### 4.2.4 MCP Server Support (Legacy)

**Description**: Standard MCP protocol for external tools; high context cost but maximum interoperability. Use only for external tools where modification is not needed.

**Functional Requirements**:
- **FR-MCP-01**: Config in `.claude/mcp.json` or `.claude/settings.json#mcpServers`
- **FR-MCP-02**: Support stdio, SSE, HTTP transports
- **FR-MCP-03**: Capability negotiation: agent requests tools, server grants subset
- **FR-MCP-04**: Permission management: granular allow/deny per tool per agent

**Non-Functional Requirements**:
- **NFR-MCP-01**: Context overhead 10k+ tokens per server (documented limitation)
- **NFR-MCP-02**: Use only for external tools where modification is not needed (80% heuristic)

**User Story**: Dan needs GitHub integration. He adds official MCP server; it "just works" but costs 10k tokens. He accepts this for 1-2 critical external tools.

---

### 4.3 Hooks & Extensibility

#### 4.3.1 Pre/Post Tool Use Hooks

**Description**: Execute bash scripts or LLM prompts before/after tool execution for validation, logging, auto-fix. Integrates `apolopena/multi-agent-workflow` as the foundation, extending it with agent-specific constraints and encrypted vote logging.

**Functional Requirements**:
- **FR-HOOK-01**: Config in `.claude/settings.json#hooks` with pattern matchers and hook chains
- **FR-HOOK-02**: Environment variables: `$CLAUDE_PROJECT_DIR`, `$CLAUDE_TOOL_NAME`, `$CLAUDE_TOOL_INPUT`
- **FR-HOOK-03**: Exit codes: `0` = success, `2` = block action, other = non-blocking error
- **FR-HOOK-04**: JSON output for granular control: `{"decision": "allow|deny|block", "updatedInput": {...}}`
- **FR-HOOK-05**: Prompt hooks: LLM evaluation of tool input/output for context-aware decisions (uses Haiku)
- **FR-HOOK-06**: SessionStart/End hooks: Initialize/cleanup, persist env vars via `$CLAUDE_ENV_FILE`
- **FR-HOOK-07**: Council logging hook: Encrypt vote transcripts for post-mortem analysis

**Non-Functional Requirements**:
- **NFR-HOOK-01**: Hook execution latency <100ms for command hooks, <500ms for prompt hooks
- **NFR-HOOK-02**: Timeout configurable (default 30s); abort tool if hook times out

**User Story**: Alex configures a `PreToolUse` hook on `Write(**.py)` that runs `ruff check --fix`. Every agent code edit is auto-linted; agent sees fix output and learns.

---

#### 4.3.2 Slash Commands

**Description**: Built-in commands for agent management, cost tracking, swarm control.

**Functional Requirements**:
- **FR-CMD-01**: `/agents` – list, create, edit, delete subagents; manage tool permissions
- **FR-CMD-02**: `/cost` – show per-agent token usage, cost breakdown by model
- **FR-CMD-03**: `/council spawn --size=5 --task="..."` – manually trigger council
- **FR-CMD-04**: `/mine` – manually trigger project mining from notes
- **FR-CMD-05**: `/clear` – clear context window (prevent pollution)
- **FR-CMD-06**: `/hooks` – list, enable/disable hooks mid-session
- **FR-CMD-07**: `/validate {url}` – manually trigger completion assessment
- **FR-CMD-08**: `/audit-docs` – run degradation linter on agent definitions

**Non-Functional Requirements**:
- **NFR-CMD-01**: Command response latency <200ms

**User Story**: Priya types `/cost` and sees that `security-auditor` spent $12 this session; she realizes it's using Sonnet for simple grep tasks and updates routing rules.

---

### 4.4 Autonomous Project Management

#### 4.4.1 Project Mining from Notes

**Description**: Parse Obsidian/Roam/Notion notes for `TODO: Project Idea:` blocks; auto-spawn projects with deduplication based on embedding similarity.

**Functional Requirements**:
- **FR-MINE-01**: Configurable notes directories: `.claude/config.json#notes_dirs: ["~/Obsidian", "~/Roam"]`
- **FR-MINE-02**: Regex pattern: `r'TODO: Project Idea: (.+)'` (customizable)
- **FR-MINE-03**: For each match, check if project repo exists (local or GitHub)
- **FR-MINE-04**: If not exists, spawn `project-starter` agent with context: source note path, idea text, related notes (link analysis)
- **FR-MINE-05**: `project-starter` agent: scaffold repo, create `CLAUDE.md`, open GitHub issue, assign to creator
- **FR-MINE-06**: Frequency: Run on `SessionStart` and via cron (daily at 09:00)
- **FR-MINE-07**: Deduplication: Don't spawn if similar project created in last 30 days (embed similarity >0.9)

**Non-Functional Requirements**:
- **NFR-MINE-01**: Mining latency <5s for 1000 notes
- **NFR-MINE-02**: False positive rate <5% (tune regex with user feedback)

**User Story**: Alex has 200 TODOs in Obsidian. SwarmForge mines them, finds "Build Rust CLI for log parsing," creates `~/projects/log-parser/`, opens issue #1, assigns to Alex. Alex reviews and approves.

---

#### 4.4.2 GitHub Issue Resolution

**Description**: Poll GitHub Issues, self-assign based on capability match, execute fixes, open PRs with completion assessment validation.

**Functional Requirements**:
- **FR-GH-01**: Config: `.claude/settings.json#github_integration`: `{token, repos: ["org/repo"]}`
- **FR-GH-02**: Poll interval: 5 minutes for assigned issues, 1 hour for unassigned
- **FR-GH-03**: Filter: `label:in-progress` or `label:good-first-issue` (customizable)
- **FR-GH-04**: Agent self-assigns if issue body embedding matches agent capabilities (similarity >0.85)
- **FR-GH-05**: Execution: spawn `issue-worker` agent with issue body as prompt
- **FR-GH-06**: Validation: For issues with `label:needs-validation`, run completion assessment before PR
- **FR-GH-07**: PR automation: create branch `swarmforge/issue-{id}`, commit, open PR with "Automated fix for #{id}"
- **FR-GH-08**: Human review gate: PR requires approval before merge (configurable)
- **FR-GH-09**: Success tracking: Log resolution rate and auto-merge rate

**Non-Functional Requirements**:
- **NFR-GH-01**: Issue-to-PR latency <10 minutes for simple fixes (typos, lint)
- **NFR-GH-02**: Success rate: 50% of assigned issues resolved without human intervention

**User Story**: Dan's repo has issue #42: "Fix typo in README." Swarmforge polls, `doc-writer` agent self-assigns, fixes, opens PR #43. Dan reviews and merges in 30 seconds.

---

### 4.5 Completion Assessment Pipeline

**Description**: Automated QA via Playwright browser automation + vision model analyzing screenshots against design docs. Catches UI/UX regressions before merge.

**Functional Requirements**:
- **FR-VAL-01**: Trigger: agent emits `<completion_assessment>` tag or manual `/validate {url}`
- **FR-VAL-02**: Orchestrator spawns `validation-subagent` (isolated context)
- **FR-VAL-03**: Playwright: launch headless browser, navigate to URL, capture screenshot, extract DOM
- **FR-VAL-04**: Design Docs: load `CLAUDE.md` or `design.md` from repo
- **FR-VAL-05**: Vision Model: prompt Claude Sonnet with screenshot + design docs, score functionality 0-1, list discrepancies
- **FR-VAL-06**: Output structured JSON: `{"score": 0.92, "discrepancies": ["Missing 'Export' button"], "pass": true/false}`
- **FR-VAL-07**: If `pass=false`, re-open issue or alert human
- **FR-VAL-08**: User Story Matching: Extract acceptance criteria from issue; validate each via Playwright script
- **FR-VAL-09**: First-15-second focus: Weight above-fold content 40% in scoring algorithm

**Non-Functional Requirements**:
- **NFR-VAL-01**: Assessment latency <1s (Playwright 500ms + LLM 300ms)
- **NFR-VAL-02**: Accuracy: 92% alignment with manual QA (benchmark target)
- **NFR-VAL-03**: Support responsive design: test at 1920×1080 and 375×667 (mobile)

**User Story**: Alex's agent claims "user profile page done." Validation spawns, loads `localhost:3000/profile`, captures screenshot, compares against Figma link in `CLAUDE.md`. Detects missing avatar upload. Reopens issue.

---

### 4.6 Visual Dashboard & Interface

#### 4.6.1 Agent Monitor

**Description**: Real-time Web UI showing agent states, message streams, costs, council votes. Built by heavily modifying `apolopena/multi-agent-workflow` (a fork of disler) to support council visualization and encrypted vote logging.

**Functional Requirements**:
- **FR-UI-01**: Layout: 3-column – Agents List (left), Agent Detail (center), System Log (right)
- **FR-UI-02**: Agent Card: name, status (working/waiting/completed/terminated), current task, token usage, cost
- **FR-UI-03**: Live Stream: WebSocket connection to `claude --debug` output; separate pane per agent (not interleaved)
- **FR-UI-04**: Council View: shows live vote progress, scores, termination countdown, GPG decryption status
- **FR-UI-05**: Cost Dashboard: bar chart of per-agent spend; alert if daily budget exceeded
- **FR-UI-06**: Task Timeline: Gantt chart of agent tasks, dependencies, parallel execution blocks
- **FR-UI-07**: Kill Switch: manual "Terminate Agent" button for rogue agents
- **FR-UI-08**: Mobile Friendly: responsive for monitoring on phone
- **FR-UI-09**: Agent Voice Persona: display 3 adjectives describing agent's communication style

**Non-Functional Requirements**:
- **NFR-UI-01**: Page load <100ms; WebSocket message latency <50ms
- **NFR-UI-02**: Support 100+ concurrent agents in dashboard without jank
- **NFR-UI-03**: Export logs as JSON for post-mortem analysis

**User Story**: Priya opens dashboard, sees 5 agents working on feature. `performance-optimizer` agent shows high token usage; she clicks it, sees it's stuck on a regex. She hits Terminate, council redistributes task.

---

#### 4.6.2 Slash Command Interface

**Description**: Terminal-style command bar in UI for rapid actions with autocomplete and history.

**Functional Requirements**:
- **FR-SUI-01**: Autocomplete for `/agents`, `/cost`, `/council`, `/mine`, `/validate`, `/audit-docs`
- **FR-SUI-02**: Command history (persisted in localStorage)
- **FR-SUI-03**: Keyboard shortcuts: `Ctrl+K` to focus, `Esc` to clear

**Non-Functional Requirements**:
- **NFR-SUI-01**: Command response <200ms

---

### 4.7 Memory & Knowledge Management

#### 4.7.1 AgentDB Integration

**Concept**: Persistent SQLite + pgvector for hybrid BM25 + semantic search. Stores agent memories, transcripts, and failure patterns for cross-project learning.

**Functional Requirements**:
- **FR-MEM-01**: Schema: `agent_memory(agent_id, task_id, content, embedding, access_count, created_at, shared)`
- **FR-MEM-02**: Storage: local SQLite for prototyping, PostgreSQL(pgvector) for production, Pinecone for scale
- **FR-MEM-03**: Search: Hybrid query combining BM25 keyword search and cosine similarity on embeddings
- **FR-MEM-04**: Auto-summarization: When memory length >10k tokens, spawn `summarizer` agent to compress to 1k
- **FR-MEM-05**: Eviction: LRU based on `access_count`; oldest summarized memories archived to cold storage (S3)
- **FR-MEM-06**: Cross-agent sharing: Workers query CEO's `ReasoningBank` for patterns; explicit opt-in via `shared: true` flag
- **FR-MEM-07**: Failure pattern storage: Index council termination rationales as negative examples

**Non-Functional Requirements**:
- **NFR-MEM-01**: Query latency 2-3ms (HNSW index)
- **NFR-MEM-02**: Search speed 96×-164× faster than naive vector scan (benchmark)
- **NFR-MEM-03**: Memory reduction 4-32× via quantization

**User Story**: Alex reopens session after weekend. `rust-executor` agent resumes from `agent-123.jsonl` transcript, reloads context from AgentDB, continues migration task. No context loss.

---

#### 4.7.2 Interleaved Thinking Storage

**Concept**: Parse `<thinking>` tags from model output; store separately in AgentDB to reduce context bloat by 6×. Thinking is visible in UI but not reinserted on resume.

**Functional Requirements**:
- **FR-THINK-01**: Regex parse `<thinking>(.*?)</thinking>` from model responses
- **FR-THINK-02**: Store parsed thinking in AgentDB linked to task ID
- **FR-THINK-03**: UI toggle: "Show Thinking" reveals chain-of-thought in agent detail pane
- **FR-THINK-04**: Thinking not re-inserted into context on resume; agent sees only final action

**Non-Functional Requirements**:
- **NFR-THINK-01**: Reduce context bloat by 6× on long chains (Kimi K2 benchmark)

**User Story**: Alex debugs agent failure. He opens UI, clicks "Show Thinking" for the task, sees 8-step reasoning that led to bad decision. He corrects the logic in the prompt.

---

### 4.8 Security & Isolation

#### 4.8.1 Permission & Tool Scoping

**Description**: Principle of least privilege; agents grant only necessary tools. Achieves 84% reduction in permission prompts vs. MCP.

**Functional Requirements**:
- **FR-PER-01**: Agent YAML: `tools: ["Read(src/**)", "Deny(Read(.env*))", "Bash(cargo *)", "Deny(Bash(rm -rf /))"]`
- **FR-PER-02**: Glob pattern matching for tool paths
- **FR-PER-03**: Permission inheritance: subagent inherits parent restrictions; cannot escalate
- **FR-PER-04**: Audit log: every tool call logged with agent ID, input, output, timestamp
- **FR-PER-05**: Hooks can enforce additional scoping at runtime

**Non-Functional Requirements**:
- **NFR-PER-01**: 84% reduction in permission prompts vs. MCP (Anthropic sandboxing benchmark)

**User Story**: Priya configures `security-auditor` agent with `Deny(Write(**))` to read-only mode. Agent cannot accidentally modify code; attempts are blocked and logged.

---

#### 4.8.2 Sandboxing

**Concept**: OS-level isolation for tool execution using Linux namespaces + seccomp-bpf.

**Functional Requirements**:
- **FR-SBX-01**: Rust-based sandbox using Linux namespaces + seccomp-bpf
- **FR-SBX-02**: Filesystem restriction: agent can only access `./.claude/` and project working directory
- **FR-SBX-03**: Network proxy: domain allowlist; block external calls unless whitelisted
- **FR-SBX-04**: Resource limits: CPU 1 core, RAM 2GB per agent cgroup

**Non-Functional Requirements**:
- **NFR-SBX-01**: Sandboxed execution overhead <10ms per tool call

---

## 5. Technical Architecture

### 5.1 System Components

**Integration Strategy**:
- **Claude Code**: External dependency, leveraged via API; host environment detection (Roo Code, OpenCoder, OpenHands) drives Actor Factory adaptations
- **apolopena/multi-agent-workflow**: Forked and heavily modified to support council voting UI, encrypted vote logging, and progressive disclosure hooks
- **aaaronmiller/claude-code-proxy**: Forked and extended to support color-coded routing, cost-aware fallback, and local model integration

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (Go)                        │
│  - REST: /api/tasks, /api/agents, /api/validate            │
│  - WebSocket: /ws/events (agent logs, votes)               │
│  - Integration: Modified from claude-code-proxy            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 Orchestration Layer (Go)                    │
│  - Temporal/Cadence workflows (council votes, mining)      │
│  - Task router (star topology, round-robin)                │
│  - Cost tracker (per-agent, per-task)                      │
│  - Extended from apolopena/multi-agent-workflow            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Execution Engine (Rust)                   │
│  - Tool executor (reqwest, tokio)                          │
│  - Playwright controller (thirtyfour)                      │
│  - Script invoker (uv, npx, cargo run)                     │
│  - Enforces "DO NOT READ SCRIPTS" constraint               │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Model Proxy (Rust)                      │
│  - ONNX classifier (task categorization)                   │
│  - OpenRouter client with price arbitrage                  │
│  - Local vLLM integration (Qwen2.5-3B)                     │
│  - Extended from aaaronmiller/claude-code-proxy            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                       Memory (AgentDB)                      │
│  - SQLite (dev) → PostgreSQL (prod) → Pinecone (scale)    │
│  - Embeddings (pgvector)                                   │
│  - Stores transcripts, votes, failure patterns             │
└─────────────────────────────────────────────────────────────┘
```

---

### 5.2 Technology Stack

| Layer | Technology | Rationale | Source Integration |
|-------|------------|-----------|--------------------|
| **API Gateway** | Go `fiber` + `gorilla/websocket` | 20k req/s, low latency | Extended from claude-code-proxy |
| **Orchestration** | Temporal/Cadence | Durable workflows, exactly-once execution | Extended from multi-agent-workflow |
| **Execution** | Rust `tokio` + `reqwest` | 20-60ms tool calls, memory safety | Enforces script isolation constraint |
| **Browser** | Playwright Rust (`thirtyfour`) | 100-300ms automation, 2-3× faster than Python | Basic validation in Phase 4 |
| **Sandbox** | Linux namespaces + seccomp-bpf | OS-level isolation, <10ms overhead | New implementation |
| **Model Proxy** | Rust `ort` (ONNX) + `hyper` | 5ms classification, 5ms routing | Extended from claude-code-proxy |
| **Memory** | SQLite → PostgreSQL(pgvector) → Pinecone | Progressive scaling, 2-3ms query | New AgentDB implementation |
| **UI** | SvelteKit + WebSocket | <100ms load, <50ms updates | Modified from multi-agent-workflow |
| **CLI** | Python `click` (prototype) → Rust `clap` (prod) | Rapid iteration → performance | New implementation |

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
5. First vote fails: consensus 0.4 < 0.8; `schema-migrator` receives warning.
6. Second vote: consensus 0.3; termination triggered.
7. Council identifies `schema-migrator` as lowest-voted across both rounds.
8. Termination signal sent: `pkill -f agent-schema-migrator`.
9. `rollback-expert` inherits state from transcript, runs `ROLLBACK`, restores index.
10. Alex receives alert: "Council terminated schema-migrator after 2 votes; rollback complete."

**Outcome**: Production incident prevented; Alex reviews logs, updates `schema-migrator` prompt with index-preservation rule.

---

### 6.2 Project Mining Spawns Revenue Feature

**Persona**: Indie Dev Dan

**Scenario**: Dan has Obsidian note "Startup Ideas" with line: "TODO: Project Idea: Build Stripe analytics dashboard for SaaS founders."

**Steps**:
1. SwarmForge `SessionStart` hook triggers project mining.
2. Parser extracts idea, checks GitHub: no `stripe-dashboard` repo exists.
3. Spawns `project-starter` agent with context: source note path, idea text, Dan's coding style from `CLAUDE.md`.
4. `project-starter` scaffolds repo, creates `CLAUDE.md` with spec derived from idea.
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
2. Validation agent spawns Playwright, loads `https://staging.myapp.com/onboarding `.
3. Captures screenshot, extracts DOM, prioritizes above-fold content (40% scoring weight).
4. Loads design doc from Figma (linked in `CLAUDE.md`).
5. Claude Sonnet vision prompt compares screenshot to design: detects "Next" button disabled, missing progress indicator.
6. Output JSON: `{"score": 0.6, "discrepancies": [...], "pass": false}`
7. Validation fails; issue reopened with screenshot diff.
8. `frontend-agent` fixes button state and progress bar.
9. Re-run validation: score 1.0; PR approved.

**Outcome**: UI bug caught before merge; manual QA would have taken 30 minutes.

---

### 6.4 Document Degradation Linting Prevents Quality Decay

**Persona**: Platform Priya

**Scenario**: Priya's team maintains 25 agent definitions in `.claude/agents/`. After adding 10 new agents, documentation quality degrades.

**Steps**:
1. Priya runs `/audit-docs` slash command in Phase 5.
2. Linter analyzes agent definitions using File 3's three metrics:
   - Progressive Simplification: 3 agents show 35% sentence complexity drop
   - Format Momentum: 5 agents exceed 60% list density
   - Context Loss: 2 agents have concept-to-detail ratio <0.5
3. Report highlights `security-auditor` agent as degraded.
4. Priya manually rewrites section with narrative context.
5. Adds `PreToolUse` hook to enforce quality on future edits.

**Outcome**: Prevents long-term maintainability collapse; documentation quality preserved at scale.

---

## 7. Competitive Analysis Matrix

| Feature | SwarmForge | wshobson/agents | openrouter-deep-research | claude-flow | ccswarm |
|---------|------------|-----------------|--------------------------|-------------|---------|
| **Council Voting** | ✅ Termination (2-strike) | ❌ | ❌ | ❌ | ❌ |
| **Project Mining** | ✅ Auto-spawn with dedup | ❌ | ❌ | ❌ | ❌ |
| **Completion Assessment** | ✅ Vision-based + UX weighting | ❌ | ❌ | ❌ | ❌ |
| **Model-Agnostic Routing** | ✅ Local + OpenRouter + cost arbitrage | ❌ (Claude only) | ✅ (OpenRouter only) | ❌ (Claude only) | ❌ |
| **Script-Based Tools** | ✅ <2k tokens + source isolation | ✅ | ❌ (MCP only) | ❌ | ❌ |
| **Rust/Go Backend** | ✅ 20-60ms | ❌ (TypeScript) | ❌ (Python) | ❌ (Ruby) | ❌ (Python) |
| **Visual Dashboard** | ✅ <50ms WS + council view | ❌ | ❌ | ⚠️ Basic | ✅ |
| **SWE-Bench Target** | 90%+ | 84.8% | N/A | 84.8% | N/A |
| **Cost at Scale** | $242/mo | $3,000+/mo | $450/mo | $2,000/mo | $1,500/mo |

**Differentiation**: SwarmForge is the only system combining **council fault tolerance**, **autonomous project lifecycle**, **polyglot performance**, and **script source isolation** in one platform.

---

## 8. Implementation Phases

### Phase 0: Foundation (Weeks 1–2)

**Goal**: Core infrastructure, hooks, script-based tools, and project integration.

**Deliverables**:
- **Repo Structure**: `swarmforge/` (Rust), `swarmforge-py/` (Python prototype), `.claude/` scaffold
- **CLI**: `swarmforge init`, `swarmforge agent list`, `swarmforge run`, `swarmforge prime-script`
- **Script Executor**: Rust binary enforcing  **"DO NOT READ SCRIPTS"**  constraint; runs `uv run scripts/{name}.py --json`
- **Hooks System**: PreToolUse, PostToolUse, SessionStart/End implemented in Go; integrated from `apolopena/multi-agent-workflow` fork
- **Prime Prompt Library**: 10 example primes for CLI-first and script-based patterns
- **Project Integration**: Fork `apolopena/multi-agent-workflow` and `aaaronmiller/claude-code-proxy`; establish modification workflow

**Success Criteria**: Can run a single task through script-based tool; latency <200ms; context overhead <2k tokens.

---

### Phase 1: Orchestration & Delegation (Weeks 3–5)

**Goal**: Subagent spawning, resume capability, CEO-worker pattern, color-coded routing.

**Deliverables**:
- **Subagent Manager**: Parse `.claude/agents/*.md`, spawn agents with isolated contexts; resume from `agent-{id}.jsonl`
- **Color-Coded Lanes**: Add `color_lane` field to agent YAML; implement GREEN and YELLOW lanes
- **CEO-Worker Protocol**: CEO agent (Sonnet) delegates to workers (Qwen2.5-3B) via explicit `delegatees` list
- **Hooks**: Add `OnAgentSpawn`, `OnAgentTerminate` events
- **Model Proxy Integration**: Begin extending `aaaronmiller/claude-code-proxy` with ONNX classifier

**Success Criteria**: Run 3-agent hierarchy (CEO → 2 workers) on sample refactoring task; sub-agent spawn <500ms.

---

### Phase 2: Council & Consensus (Weeks 6–8)

**Goal**: Council voting, two-strike termination, encrypted votes, dashboard UI.

**Deliverables**:
- **Council Workflow**: Temporal workflow for round-based voting
- **Vote Aggregator**: Collect votes, compute consensus, identify lowest-voted agent after two failures
- **Termination Executor**: Graceful shutdown + state handoff
- **GPG Integration**: `gpg --encrypt --recipient council@vote` for hidden messages
- **Dashboard UI**: Real-time vote progress bar, agent cards, termination log; modified from `apolopena/multi-agent-workflow` Vue components

**Success Criteria**: Simulate 5-agent council on 10 tasks; termination occurs on 2/10; consensus quality >0.85.

---

### Phase 3: Model Routing & Performance (Weeks 9–11)

**Goal**: Model-agnostic proxy, ONNX classifier, local model integration, cost-aware fallback.

**Deliverables**:
- **Model Proxy**: Rust service intercepting calls, classifying via ONNX, routing with cost arbitrage; extended from `aaaronmiller/claude-code-proxy`
- **ONNX Classifier**: DistilBERT fine-tuned on 10k task examples (tool call vs. reasoning)
- **Local Model Support**: vLLM integration for Qwen2.5-3B, Granite-4.0-Tiny
- **OpenRouter Client**: Fallback when local models unavailable; price monitoring for arbitrage
- **Cost Tracking**: Per-agent spend accumulator; exposed via `/cost` API
- **Token Recycling**: LRU cache for GREEN lane tool outputs

**Success Criteria**: 95% tasks route to local models; fallback <5%; classification accuracy >90%; average cost $0.16 per 1000 tasks vs. $200 Claude-only.

---

### Phase 4: Validation & Mining (Weeks 12–14)

**Goal**: Completion assessment with UX-weighted scoring, project mining, GitHub integration, dashboard polish.

**Deliverables**:
- **Playwright Executor**: Rust controller for headless browser automation
- **Vision Validation**: Claude Sonnet prompt with screenshot + design docs; weight above-fold content 40%
- **Project Miner**: Cron job + `SessionStart` hook; regex parsing; similarity dedup
- **GitHub MCP Server**: Enhanced version with self-assignment logic; integrated from fork
- **Dashboard**: SvelteKit UI with WebSocket; agent timeline, cost chart; voice personas displayed
- **A/B Testing Framework**: Infrastructure for testing agent communication styles (deferred activation)

**Success Criteria**: Validate 10 sample tasks; catch 2 UI bugs; mine 5 projects from notes; dashboard supports 100 concurrent agents.

---

### Phase 5: Enterprise Hardening (Weeks 15–18)

**Goal**: Scale to 10,000 agents, RBAC, SAML, audit logs, documentation quality gates.

**Deliverables**:
- **Temporal Cluster**: Multi-node orchestration for 1M+ workflows/day
- **AgentDB**: Migrate to PostgreSQL → Pinecone for 100M+ memories
- **RBAC**: Agent roles (viewer, executor, admin), team workspaces
- **SAML/SSO**: Okta, Azure AD integration
- **Audit Export**: SOC2-compliant logs to S3/GCS
- **Document Degradation Linter**: `/audit-docs` command; scans agent definitions for File 3's three patterns
- **Hook Enhancement**: Encrypted vote logging for council post-mortems

**Success Criteria**: Pass security review; scale test: 10,000 concurrent agents, 99.9% uptime; documentation quality maintained across 50+ agents.

---

## 9. Success Metrics & KPIs

| Metric | Baseline | Target v1.0 | Target v2.0 | Measurement |
|--------|----------|-------------|-------------|-------------|
| **Task Latency (p95)** | 8s (Python MCP) | 880ms | 500ms | Distributed tracing |
| **Cost per 1k tasks** | $45 (GPT-4) | $2.42 | $0.68 | OpenRouter + local + recycling |
| **SWE-Bench Score** | 84.8% (wshobson) | 90% | 95% | Automated benchmark |
| **Agent Uptime** | N/A | 99.5% | 99.9% | Temporal metrics |
| **Council Consensus Rate** | N/A | 80% | 90% | Vote log analysis |
| **Project Mining Yield** | 0/week | 5/week | 15/week | Issue creation log |
| **GitHub Resolution Rate** | 0% | 30% | 50% | PR merge log |
| **Context Overhead per Tool** | 10k tokens (MCP) | <2k tokens | <1k tokens | Token counter |
| **Documentation Quality Score** | N/A | >90% | >95% | Linter pass rate |
| **Developer NPS** | N/A | >50 | >70 | Quarterly survey |
| **Token Efficiency** | 1× (naïve) | 5× | 10× | Benchmark suite |

---

## 10. Open Questions & Risks

### 10.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Council terminates productive agent** | Medium | High | Two-strike rule; human override; encrypted vote review |
| **Model classifier misroutes complex task** | Medium | Medium | Confidence threshold + fallback; human review queue |
| **Script-based tools drift (no schema)** | High | Medium | Versioning; automated `--help` testing; migration warnings |
| **AgentDB query latency at scale** | Low | High | Shard by agent_id; add Redis cache for hot paths |
| **Encrypted votes cause deadlock** | Low | Medium | Timeout on GPG ops; fallback to public votes if delay >10s |
| **Multi-project fork divergence** | Medium | Medium | Maintain upstream sync schedule; isolate modifications |

### 10.2 Product Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Developers distrust agent termination** | High | High | Dashboard transparency; two-strike rule; opt-out mode |
| **Project mining creates noise (false positives)** | Medium | Medium | Tune regex with user feedback; similarity threshold >0.95 |
| **Cost tracking is inaccurate** | Medium | High | Reconcile with provider invoices monthly; real-time estimates |
| **Ecosystem lock-in (Claude skills)** | High | Medium | Support MCP import/export; maintain script-based parity |
| **Visual UI is slow at 100+ agents** | Medium | High | Virtualized lists; WebSocket binary framing; pagination |

### 10.3 Business Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Anthropic changes Claude Code API** | Medium | High | Abstract behind proxy; maintain feature flags |
| **OpenRouter pricing increases** | Medium | Medium | Local model fallback; multi-provider routing; arbitrage |
| **Enterprise security review blocks** | Medium | High | FedRAMP-compliant cloud; on-prem option in v2.0 |
| **Competitor copies features** | High | Medium | First-mover advantage; community moat (open source core) |
| **Fork maintenance burden** | Medium | Medium | Contribute non-proprietary enhancements upstream |

---

## 11. Assumptions & Constraints

### 11.1 Assumptions

- Target users are senior engineers comfortable with CLI, YAML config, and async concepts
- Claude Code remains actively developed; APIs stable for 12 months
- Local model inference (Qwen2.5-3B) is acceptable for 95% of tasks; edge cases escalate
- GitHub is primary code host; GitLab support in v2.0
- Observidian/Roam are primary note-taking tools; Notion integration in v2.0
- `apolopena/multi-agent-workflow` and `aaaronmiller/claude-code-proxy` can be forked and modified without upstream conflicts

### 11.2 Constraints

- **Context Window**: Claude Sonnet 4.5 limit 200k tokens; we target <50k tokens per council round
- **Rate Limits**: OpenRouter 1000 req/min; local models unlimited
- **Hardware**: Local model inference requires GPU (RTX 4090 or A10G) for <50ms latency
- **Budget**: Development budget $150k; cloud infra budget $500/month for v1.0
- **Timeline**: 18 weeks to v1.0; 12 weeks to v2.0
- **Fork Divergence**: Must maintain ability to merge upstream security fixes from `apolopena/multi-agent-workflow` and `aaaronmiller/claude-code-proxy`

---

## 12. Future Roadmap (v2.0 & Beyond)

### 12.1 v2.0 Features (Q2 2026)

- **Async Coordination**: NATS message queue for pub/sub agent communication; Raft consensus for distributed council
- **Memory Evolution**: Neo4j knowledge graph for relationship tracking; episodic memory for cross-project learning
- **Cross-Platform**: React Native mobile app; Siri shortcuts for task kickoff
- **Industry Skills**: Pre-built skills for finance, healthcare, legal
- **Voice Interface**: Whisper integration for voice commands; TTS for agent status updates
- **Document Auto-Fix**: Promote linter to autonomous rewriting with human approval gate

### 12.2 v3.0 Vision (Q4 2026)

- **Autonomous Company**: Mine Notion OKRs, spawn projects, hire agents (auto-scale based on budget), report KPIs to human CEO
- **AI-to-AI Market**: Agents can "hire" other agents from marketplace; pay per task in credits
- **Neural Compiler**: Train model to emit directly optimized LLVM IR, bypassing borrow checker limits

---

## 13. Glossary

- **Agent**: Specialized AI worker with YAML config, isolated context, tool restrictions
- **Council**: Group of agents voting on completion; lowest-voted terminated after two failures if consensus fails
- **MCP**: Model Context Protocol; standard but high-context tool integration
- **Prime Prompt**: Command that loads tool definitions into agent context on-demand
- **Progressive Disclosure**: Load only metadata → instructions → resources as needed; agent cannot read script source
- **Script-Based**: Agent reads intent→script map; script source never enters context
- **Star Topology**: Central hub broadcasts tasks to agents; agents pull based on capability
- **SWE-Bench**: Benchmark for software engineering task automation
- **Temporal**: Durable workflow orchestration (Go)
- **Two-Strike Termination**: Requires consecutive consensus failures before terminating agent

---

## 14. Appendices

### Appendix A: Example `.claude/agents/code-reviewer.md`

```yaml
---
name: code-reviewer
description: Expert code review specialist. Proactively review code immediately after changes.
tools: Read, Grep, Glob, Bash
model: claude-sonnet
color_lane: YELLOW
delegatees: [security-auditor, performance-checker, style-enforcer]
resume: agent-456
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

### Appendix B: Integration Points for Forked Projects

**`apolopena/multi-agent-workflow` Fork**:
- **Retain**: WebSocket message broadcasting, agent state management, Vue UI components
- **Modify**: Add council voting UI, GPG encryption support, progressive disclosure hook injection
- **Remove**: Hardcoded MCP server assumptions; replace with script-based tool calls
- **Upstream Sync**: Monthly merge of security patches; maintain custom features in feature branches

**`aaaronmiller/claude-code-proxy` Fork**:
- **Retain**: Proxy interface, request interception, response streaming
- **Modify**: Add ONNX classifier, cost arbitrage logic, local model fallback, color-coded routing metadata
- **Remove**: OpenRouter-only assumption; extend to support 27+ providers
- **Upstream Sync**: Quarterly merge of provider updates; maintain routing logic in isolated modules

---

**End of Revised PRD**


































creation prompt (prd):
```
<start>
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
2. Validation agent spawns Playwright, loads `https://staging.myapp.com/onboarding `.
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
<end>
<start summary of attachments>
# Strategic Analysis: Implementation Roadmap for Your Agent & Documentation Platform

Based on my analysis of the four provided documents, I'll map the insights to concrete implementation stages for your program. The papers converge around three critical themes: **intelligent agent architecture**, **content quality preservation**, and **audience engagement optimization**. Here's a phased implementation plan:

---

## 🚀 **Phase 1: Immediate Implementation (0-3 months)**

These ideas are battle-tested, have low technical risk, and deliver immediate ROI.

### **1. CLI-First Tool Pattern + Prime Prompt System**
*From: File 1 (MCP Alternatives)*

**Implementation:**
- Convert your existing MCP servers into lightweight CLI wrappers using the "Trifecta" approach
- Create a `/prime-[tool]-cli` prompt template that loads only `readme.md` + `cli.py` (reduces context waste from 10% to ~5%)
- Deploy this in your Roo Code environment for immediate context savings

**Why Now:** 
- No architectural changes needed—just wrapper scripts
- Cut token costs by 40-50% immediately while maintaining full control
- Works today in your existing agent environment (identified as Roo Code in File 4)

### **2. Progressive Disclosure Documentation System**
*From: File 1 (Scripts-Based) + File 3 (Context Loss Prevention)*

**Implementation:**
- Refactor your agent documentation to use a single `readme.md` as a condition-to-script router
- Add the explicit constraint:  **"DO NOT read script source code, only execute via `--help`**  "
- This achieves the <1% context usage reported in File 1 while preventing the "format degradation" problem from File 3

**Why Now:**
- Direct solution to both context window pressure AND documentation quality decay
- Can be implemented with simple file structure changes
- Aligns with the "real-time documentation" principle from File 3

### **3. Color-Coded Actor Factory for Task Routing**
*From: File 4 (AIME Architecture)*

**Implementation:**
- Implement the four-lane system (GREEN/YELLOW/RED/GRAY) in your existing agent framework
- Start with GREEN (direct file manipulation) and YELLOW (pattern-based) lanes
- Use your current `taskmaster-ai` as the Progress Management Module

**Why Now:**
- Immediately clarifies task complexity without full multi-agent orchestration
- Roo Code's semantic awareness (mentioned in File 4) can be leveraged for YELLOW lane pattern detection
- Low risk—just adds metadata tags to existing workflows

### **4. Voice Scripting & Pattern Interrupts for User Facing Content**
*From: File 2 (Audience Retention)*

**Implementation:**
- Create a "Voice & Tone Chart" for your agent's user-facing responses
- Script the first 15 seconds of every agent interaction to state value proposition clearly
- Mark scripts with vocal dynamics cues: `[PAUSE]`, `[EMPHASIS]`, `[TONE:Authoritative]`

**Why Now:**
- Immediately improves user trust and engagement with your agents
- Zero technical cost—pure prompt engineering
- Prevents the "monotonous delivery" problem that kills retention

---

## 🔭 **Phase 2: Near-Term Horizon (3-6 months)**

These require moderate integration effort but build directly on Phase 1 foundations.

### **5. Dynamic Actor Instantiation with Environment-Specific Adaptation**
*From: File 4 (Actor Factory)*

**Implementation:**
- Build the Actor Factory to spawn ephemeral agents per-task
- Configure environment-specific adaptations:
  - **Roo Code:** Inject AST analysis as "Knowledge" component
  - **OpenCoder:** Default to shell-based actors using `uv run` (from File 1)
  - **OpenHands:** Map color lanes to existing micro-agents

**Why Horizon:**
- Requires refactoring your monolithic agent into a factory pattern
- Need to implement `taskmaster.update_task` tooling for progress tracking
- Benefits compound after you have 5+ specialized tool sets

### **6. Documentation Degradation Monitoring Dashboard**
*From: File 3 (Structural Degradation)*

**Implementation:**
- Automate the six metrics from File 3's Phase 1:
  - Narrative flow score (transitional phrase density)
  - Format consistency score (heading hierarchy validation)
  - Context coverage ratio (concepts explained per technical detail)
- Build a pre-commit hook that fails if degradation exceeds 15% across document sections

**Why Horizon:**
- Requires building custom linters/parsers for your documentation format
- Need baseline metrics from your existing docs first
- High value once you have 10+ complex technical documents

### **7. A/B Testing Framework for Agent Personas**
*From: File 2 (A/B Testing Protocol)**

**Implementation:**
- Apply File 2's sequential testing method to agent voice/persona:
  - Test male vs. female voice personas for your agent
  - Test "Authoritative" vs. "Empathetic" tone lanes
  - Measure "Average Interaction Completion Rate" instead of retention
- Use controlled distribution (Method A from File 2) across user segments

**Why Horizon:**
- Requires building user segmentation and variant routing
- Need statistically significant user base (100+ daily interactions)
- But provides data-driven persona optimization that's impossible to guess

---

## 🧬 **Phase 3: Long-Term Horizon (6+ months)**

These are strategic bets that require research, infrastructure, or ecosystem maturity.

### **8. Skills-Based Ecosystem with Platform Lock-in**
*From: File 1 (Skills-Based) + File 4 (Clawed Ecosystem)**

**Implementation:**
- Create self-contained `skills/` directories bundling scripts + `skill.md` prime prompts
- Accept the "Clawed ecosystem lock-in" as a tradeoff for isolation
- Map to AIME's GRAY lane for automatic skill discovery

**Why Horizon:**
- Only valuable once you have 20+ specialized capabilities
- Requires committing to a single platform (Roo Code vs. OpenHands)
- High portability cost—wait until your agent architecture stabilizes

### **9. Automated Degradation Detection & Recovery**
*From: File 3 (Future Research) **

** Implementation: **
- Train a small LM to detect the three degradation patterns:
  - Progressive Simplification (sentence complexity drop)
  - Format Momentum (list density acceleration)
  - Context Loss (concept-to-detail ratio)
- Auto-trigger RED lane actors to "re-narrativize" degraded sections

** Why Horizon: **
- Requires labeled dataset of degraded docs (build during Phase 2 monitoring)
- Needs LM fine-tuning infrastructure
- High automation payoff only after manual monitoring proves value

### ** 10. Multi-Accent Voice Synthesis for Global Agents **
*From: File 2 (Accent Perception)**

**Implementation:**
- Integrate TTS APIs that can dynamically shift accent based on user geography
- Use British RP for European enterprise clients, GenAm for US/Asia
- Apply "Accent Prestige Theory" from File 2: high-status content = low-pitch, prestige accent

**Why Horizon:**
- Current AI voice quality still triggers "credibility penalty" for complex technical content (see File 2)
- Requires real-time accent detection and synthesis
- Wait for TTS models to improve (2025-2026 expected leap in quality)

### **11. Memory Injection & Knowledge Graph Integration**
*From: File 4 (Future Capability) **

** Implementation: **
- Connect `memory` MCP tool to a vector DB storing successful task executions
- Inject relevant past Actor blueprints into new Dynamic Actor prompts
- Build a knowledge graph mapping "task type" → "optimal actor config" → "success rate"

** Why Horizon: **
- Requires robust embedding and retrieval infrastructure
- Benefits only emerge after 1000+ task executions
- Strategic for scaling beyond 50+ specialized tools

---

## 📊 **Implementation Priority Matrix**

| Idea | Effort | Impact | Risk | Phase |
|------|--------|--------|------|-------|
| CLI-First Pattern | Low | High | Very Low | **Immediate** |
| Progressive Disclosure Docs | Low | High | Low | **Immediate** |
| Color-Coded Routing | Medium | High | Low | **Immediate** |
| Voice Scripting | Low | Medium | Very Low | **Immediate** |
| Actor Factory | High | Very High | Medium | **Horizon 3mo** |
| Degradation Dashboard | Medium | Medium | Low | **Horizon 3mo** |
| A/B Testing Personas | Medium | High | Medium | **Horizon 3mo** |
| Skills-Based Ecosystem | High | Medium | High | **Horizon 6mo+** |
| Auto-Detection AI | Very High | Very High | High | **Horizon 6mo+** |
| Multi-Accent Voices | High | Low | Medium | **Horizon 6mo+** |
| Memory Injection | Very High | Very High | Medium | **Horizon 6mo+** |

---

## 🎯 **Critical Path Recommendation**

**Start with the synergy between File 1 + File 4:**
1. Implement CLI-First pattern (File 1) as the foundation for your GREEN/YELLOW lane tools (File 4)
2. Use the `taskmaster-ai` module from File 4 to enforce the progressive disclosure rules from File 1
3. Apply File 3's degradation monitoring to ensure your agent documentation doesn't decay as you add tools

This creates a self-reinforcing system: **low-context agents** (File 1) → **color-coded orchestration** (File 4) → **quality preservation** (File 3) → **higher user retention** (File 2).
<end>
analyze these papers in the context of my program and suggest what ideas are ready for imnplkmeentatoin and what should be on our horizon plan for future improvements



```