# NEXT_STEPS: Migration & Integration PRD

## Purpose
This document tracks the iterative assessment of `/docs/amalgam` content for migration to the Super Agent Monitor production system.

---

## File Inventory

### Large Files (>100k - Require Chunking)
| File | Size | Status | Notes |
|:-----|:-----|:-------|:------|
| `MACS/Chat with gemini 3 - MACS.md` | 247k | ⏳ Pending | Chat transcript - extract key architecture notes |
| `MACS/Chat with gemini 3 - MACS - part II.md` | 142k | ⏳ Pending | Chat transcript - extract key notes |
| `Strategic Analysis SwarmForge Implementation Roadmap.md` | 140k | ⏳ Pending | Strategic analysis - distill to actionable items |

### Core PRDs (Found)
| File | Purpose | Integration Status |
|:-----|:--------|:-------------------|
| `markdown_agents/prd.md` | Super Agent Monitor PRD (main) | 🔵 Read - needs DIFF analysis |
| `markdown_agents/prd-2.md` | Markdown Agent Auditor | 🔵 Read - specialized auditor |
| `markdown_agents/agent_definition.md` | Agent definition format | ⏳ Pending |

### Migration/Upgrade Docs
| File/Dir | Purpose | Integration Status |
|:---------|:--------|:-------------------|
| `markdown_agents/agent-toolkit/UPGRADE_GUIDE.md` | Agent Toolkit → Script-based MCP | ✅ Read |
| `markdown_agents/agent-toolkit-swarms/migration-swarm-v2/` | Migration swarm V2 | ⏳ Pending |
| `markdown_agents/legacy-swarms-v1/migration-swarm/` | Legacy migration | ⏳ Pending |

### Agent Definitions by Location
| Location | Count | Description |
|:---------|:------|:------------|
| `dot-claude/agents/` | 13 | Active agent definitions |
| `claude-code/agents/` | 5 | Claude Code agent templates |
| `markdown_agents/agent-toolkit/` | 23 items | Agent toolkit library |
| `markdown_agents/evolutionary-swarms/` | 4 | Evolutionary swarm patterns |
| `markdown_agents/orchestration-examples/` | 6 | Orchestration examples |

### Skills by Location
| Location | Count |
|:---------|:------|
| `dot-claude/skills/` | 22 |
| `claude-code/skills/` | 7 |

### Hooks by Location
| Location | Count |
|:---------|:------|
| `dot-claude/hooks/` | 7 |
| `claude-code/hooks/` | 9 |
| `observability/` | 25 items (includes hooks + utils) |

### Observability System (Critical)
| File | Purpose |
|:-----|:--------|
| `observability/session_start.py` | Session start hook |
| `observability/send_event.py` | Event sender |
| `observability/utils/tts/` | TTS implementations (ElevenLabs, OpenAI, pyttsx3) |

### Architecture Docs
| File | Purpose |
|:-----|:--------|
| `Generic Agent Monitoring & Deployment Architecture.md` | 91k - comprehensive architecture |
| `ORCHESTRATOR_METHODOLOGY.md` | Core orchestrator methodology |
| `omniedge-orchestrator.md` | Omniedge swarm orchestrator (legacy/experimental) |
| `ADVERSARIAL_VALIDATION_RESEARCH.md` | Council formation patterns |

### MACS (Multi-Agent Coordination System) - Specialized
| File | Purpose |
|:-----|:--------|
| `MACS/Item_1_MACS_Deployment_Definition.md` | 57k - Deployment definition |
| `MACS/Item_2_Biomimetic_Architecture_Definition.md` | 61k - Biomimetic arch |
| `MACS/Item_3_Research_Paper_Biomimetic_Multi_Agent_Architecture.md` | 57k - Research paper |
| `MACS/NOTES_*.md` | Notes on each item |
| `MACS/PROCESS_ASSESSMENT_AND_IMPROVEMENTS.md` | Process improvements |
| `MACS/REFINEMENT_TODO.md` | Refinement TODOs |

### Voice/Speech Integration
| Component | Current State | Target State |
|:----------|:--------------|:-------------|
| **TTS** | ElevenLabs, OpenAI, pyttsx3 | Microsoft Vibe Voice |
| **STT** | Whisper (mentioned) | NVIDIA Parakeet v3 |

> **Note**: No Vibe Voice or Parakeet documentation found in amalgam. Web search required.

---

## Integration Strategy

### Phase 1: Old Build → New Build Migration
1. **Diff Analysis**: Compare `markdown_agents/prd.md` against current implementation
2. **Feature Extraction**: List all features from old PRD not yet implemented
3. **Gap Identification**: Document missing components

### Phase 2: Amalgam Integration
1. **Agent Unification**: Merge agent definitions from all locations into unified format
2. **Skill Consolidation**: Deduplicate and organize skills
3. **Hook Integration**: Port observability hooks to current system
4. **Template Standardization**: Define optimal agentic template format

### Phase 3: Voice System Upgrade
1. **Research**: Web search for Vibe Voice and Parakeet documentation
2. **TTS Replacement**: Replace current Whisper/ElevenLabs with Vibe Voice
3. **STT Addition**: Integrate NVIDIA Parakeet for speech-to-text

---

## Optimal Agentic Template (To Be Determined)

### Current Template Formats Found:
1. **Markdown YAML frontmatter + body** (most common)
2. **Pure YAML** (agent-toolkit)
3. **JSON** (settings files)

### Template Considerations:
- Context window efficiency (avoid overburden)
- Clear role/skill/tool specifications
- Dynamic assembly support
- Model sizing hints
- Thinking budget allocation

---

## Processing Log

| Timestamp | File/Action | Notes |
|:----------|:------------|:------|
| 2025-12-08 14:50 | Created scratch file | Initial inventory |
| 2025-12-08 14:55 | `prd.md` (full 751 lines) | Extracted feature matrix, 6-phase roadmap |
| 2025-12-08 14:57 | Web search: VibeVoice | Replicate/Fal.ai APIs available, GitHub disabled |
| 2025-12-08 14:57 | Web search: Parakeet v3 | NVIDIA NeMo, HuggingFace integration |
| 2025-12-08 15:00 | `agent_definition.md` (800 lines) | CIO Pattern, deployment scripts |
| 2025-12-08 15:05 | Created `02_VOICE_INTEGRATION.md` | Full integration research |
| 2025-12-08 15:07 | Created `03_FEATURE_GAP_ANALYSIS.md` | PRD feature matrix |
| 2025-12-08 15:10 | Created `04_AGENT_TEMPLATE_SPEC.md` | Optimal 450-token template |

---

## Next Actions
1. [x] Read `markdown_agents/prd.md` (full 751 lines) - feature matrix complete
2. [x] Web search: Microsoft Vibe Voice integration - DONE (Replicate API)
3. [x] Web search: NVIDIA Parakeet v3 STT - DONE (NeMo framework)
4. [ ] Chunk & analyze large MACS files (3 files, 530k total)
5. [x] Determine optimal agent template format - DONE (04_AGENT_TEMPLATE_SPEC.md)
6. [ ] Read `Generic Agent Monitoring & Deployment Architecture.md` (91k)
7. [ ] Process `Strategic Analysis SwarmForge Implementation Roadmap.md` (140k - chunk)
8. [ ] Create comprehensive MIGRATION_PRD.md
