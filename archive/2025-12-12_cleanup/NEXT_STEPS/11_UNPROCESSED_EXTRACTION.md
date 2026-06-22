# Amalgam Unprocessed Files: Extracted Patterns

**Date:** 2025-12-08
**Protocol:** Integration Protocol v1.0 with Chunking
**Files Processed This Session:** 7

---

## Summary of New Patterns

| Pattern | Source | Priority | Status |
|:--------|:-------|:---------|:-------|
| Context Collapse Prevention System | Context Collapse.md | HIGH | E - EXTRACTED |
| Multi-LLM Debugging Chains | Context Collapse.md | MEDIUM | E - EXTRACTED |
| Claude Folder Architecture | Claude commands.md | HIGH | E - EXTRACTED |
| CLI-First Tool Pattern | Beyond MCP.md | HIGH | E - EXTRACTED |
| Script-Based Progressive Disclosure | Beyond MCP.md | HIGH | E - EXTRACTED |
| Skills-Based Bundling | Beyond MCP.md | HIGH | I - INTEGRATED |
| Decision Heuristic (80/15/5) | Beyond MCP.md | MEDIUM | E - EXTRACTED |

---

## Pattern 1: Code Context Preservation System (CCPS)

**Source:** `docs/🎯 THE CORE PROBLEM Context Collapse During Debugging.md`

### Problem Addressed
When models fix bugs, they "go blind" and make changes like:
- Fixing one bug but breaking three others
- Adding features that contradict existing architecture
- Creating internal inconsistencies

### Solution Architecture

```
┌─────────────────────────────────────────────────────────┐
│  PHASE 0: Initial Code Audit (ONE-TIME PER PROJECT)    │
│  Creates: codebase-map.md                               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  PHASE 1: Bug Discovery                                 │
│  Creates: bug-report.md                                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  PHASE 2: Context-Aware Fix Request                     │
│  Uses: codebase-map.md + bug-report.md + fix-task.md   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  PHASE 3: Validation & Update                           │
│  Updates: codebase-map.md with changes                  │
└─────────────────────────────────────────────────────────┘
```

### Key Documents

1. **`codebase-map.md`** - Persistent context document with:
   - SYSTEM ARCHITECTURE MAP
   - CRITICAL COMPONENTS INVENTORY
   - WORKING CODE REGISTRY (marked ⚠️ DO NOT MODIFY)
   - PROBLEMATIC CODE REGISTRY (marked 🔍 NEEDS FIXING)
   - API VERIFICATION CHECKLIST
   - ENVIRONMENTAL REQUIREMENTS
   - RECENT CHANGES LOG

2. **`bug-report.md`** - Standard format:
   - OBSERVED BEHAVIOR
   - REPRODUCTION STEPS
   - AFFECTED COMPONENTS (references codebase-map.md)
   - INITIAL HYPOTHESIS

3. **`fix-request-template.md`** - Context-aware fixing:
   - STEP 1: Context verification (check WORKING registry)
   - STEP 2: Dependency impact analysis
   - STEP 3: API verification
   - STEP 4: Surgical fix planning
   - CRITICAL RULES (never modify WORKING components)

### Action Items
- [ ] Create `scripts/audit_codebase.py` implementing this pattern
- [ ] Add `docs/templates/codebase-map-template.md`
- [ ] Integrate with observability hooks

---

## Pattern 2: Multi-LLM Debugging Chains

**Source:** `docs/🎯 THE CORE PROBLEM Context Collapse During Debugging.md`

### Workflow
1. **Model A** (Claude): Analyze bug report and context
2. **Model B** (GPT-4): Propose fix strategies  
3. **Model C** (Gemini): Validate fix doesn't break architecture

### Related Patterns
- Self-Debugging with Rubber Duck Method
- Context Compression with State Summaries
- Agent Memory Systems (RepoAudit)
- Layered Context Input with Validation Hooks (O1 framework)

### Integration Point
This pattern aligns with existing council voting (scripts/council.py) - can be extended to use multiple LLMs.

---

## Pattern 3: Claude Folder Architecture

**Source:** `docs/Claude commands.md`

### Canonical Project Structure

```bash
project-root/
├── CLAUDE.md                    # PROJECT MEMORY (team-shared)
├── .claude/
│   ├── settings.json            # PROJECT CONFIG (team-shared)
│   ├── settings.local.json      # PERSONAL OVERRIDES (gitignored)
│   ├── commands/                # SLASH COMMANDS
│   │   ├── orchestrate.md       # Multi-agent orchestrator
│   │   └── custom-workflow.md   # Custom commands
│   ├── agents/                  # SUB-AGENT DEFINITIONS
│   │   ├── backend-expert.md
│   │   └── frontend-expert.md
│   ├── skills/                  # SPECIALIZED KNOWLEDGE
│   │   └── api-patterns/
│   │       └── SKILL.md
│   └── hooks/                   # PRE/POST OPERATION SCRIPTS
│       ├── pre-write.sh
│       └── post-bash.sh
└── .mcp.json                    # MCP SERVERS (optional)
```

### Key Technical Details

**Subagent Configuration:**
```yaml
---
name: unique-agent-name
description: When and why to invoke this agent
tools: Read, Grep, Bash  # Optional - comma-separated
model: sonnet  # Optional - 'sonnet', 'opus', 'haiku', 'inherit'
---
System prompt defining the agent's role.
```

**Priority Order:**
1. Project subagents: `.claude/agents/`
2. CLI-defined: `--agents` flag
3. User subagents: `~/.claude/agents/`
4. Plugin subagents

**Hook Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [{"matcher": "ToolPattern", "hooks": [...]}],
    "PostToolUse": [...],
    "UserPromptSubmit": [...],
    "Stop": [...],
    "SessionStart": [...],
    "SessionEnd": [...],
    "Notification": [...]
  }
}
```

### Action Items
- [ ] Validate current `.claude/` structure matches this
- [ ] Create missing `commands/` directory
- [ ] Add `orchestrate.md` command

---

## Pattern 4: CLI-First Tool Pattern

**Source:** `docs/Beyond MCP- 3 Alternatives for Agent Tool Use.md`

### Problem
MCP servers consume 5-20% of agent context window before any work.

### Solution
Use "prime prompt" to tell agent to read `readme.md` + `cli.py` only.

**Workflow:**
1. User runs prime prompt (e.g., `/prime-kshi-cli-tools`)
2. Agent reads `readme.md` and `cli.py`
3. Agent summarizes capabilities
4. User issues commands → Agent translates to CLI calls

**Context Savings:** 10% → 5.6%

### Integration Point
Aligns with existing `scripts/tools/readme.md` pattern.

---

## Pattern 5: Script-Based Progressive Disclosure

**Source:** `docs/Beyond MCP- 3 Alternatives for Agent Tool Use.md`

### Core Principle
"DO NOT READ THE SCRIPTS THEMSELVES" - Trust the readme map.

**Workflow:**
1. Agent reads ONLY `readme.md` (maps conditions to scripts)
2. Context usage: <1% (~2k tokens)
3. Agent identifies correct script from map
4. Executes: `uv run scripts/search.py --json "query"`
5. Context consumed only for OUTPUT, not code

**Context Savings:** <1% (vs 10-20% for MCP)

### This Pattern Already Implemented
- `scripts/tools/readme.md` - Tool registry (DO NOT read source)
- `scripts/tools/*.py` - Executable tools with `--json` and `--help`

---

## Pattern 6: Decision Heuristic (80/15/5)

**Source:** `docs/Beyond MCP- 3 Alternatives for Agent Tool Use.md`

### For External Tools:
| % | Approach | Reason |
|:--|:---------|:-------|
| 80% | MCP | Simple, standard, fast |
| 15% | CLI-First | Need to modify/control |
| 5% | Scripts | Context preservation critical |

### For New Tools:
| % | Approach | Reason |
|:--|:---------|:-------|
| 80% | CLI-First | "Trifecta": You, Team, Agents |
| 10% | Wrap in MCP | Scale after CLI works |
| 10% | Scripts | Many tools, context critical |

---

## Files Categorized This Session

### INTEGRATED (I):
- Skills-based bundling → Already in `components/hooks/utils/tts/`, `scripts/tools/`

### EXTRACTED (E):
- CCPS (Code Context Preservation System)
- Multi-LLM debugging chains
- Claude folder architecture
- CLI-First tool pattern
- Progressive disclosure refinements
- Decision heuristics

### REMAINING UNPROCESSED:
| File | Size | Status |
|:-----|:-----|:-------|
| Strategic Analysis SwarmForge...md | 140KB | ? (needs chunking) |
| Generic Agent Monitoring...md | 91KB | ? (partial, needs more) |
| Item_1_MACS_Deployment_Definition.md | 57KB | ⏳ (MACS - user providing) |
| Item_2_Biomimetic_Architecture.md | 61KB | ⏳ (MACS - user providing) |
| Item_3_Research_Paper_Biomimetic.md | 57KB | ⏳ (MACS - user providing) |
| Research Paper High-Performance...md | 41KB | ? |
| The agentic swarm revolution...md | 36KB | ? |
| Swarm AI coding IDE comparison.md | 27KB | ? |
| Orchestrating Intelligence...md | 22KB | ? |
| PROCESS_ASSESSMENT_AND_IMPROVEMENTS.md | 19KB | ⏳ (MACS - user providing) |

---

## Next Steps

1. **Request MACS extracts** from user (5 files, ~213KB total)
2. **Chunk and process** remaining large files:
   - Strategic Analysis SwarmForge (140KB) → 3 chunks
   - Generic Agent Monitoring (91KB) → 2 chunks
3. **Process remaining medium files** (~8 files, <50KB each)
4. **Create audit scripts** implementing CCPS pattern
5. **Validate folder structure** against Claude architecture
