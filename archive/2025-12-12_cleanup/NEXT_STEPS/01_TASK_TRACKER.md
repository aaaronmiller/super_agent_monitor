# NEXT_STEPS: Sprint 3+ Task Tracker

## Current Phase: EXECUTION

---

## Main Objectives
1. [x] Migrate old build features to new build
2. [x] Integrate all `/docs/amalgam` content (core patterns)
3. [x] Upgrade TTS to Microsoft Vibe Voice
4. [x] Add STT with NVIDIA Parakeet v3
5. [x] Unify agent template format
6. [/] Process MACS extracts
7. [ ] Implement swarm-cli
8. [ ] Configure 3-layer proxy routing

---

## Task Breakdown

### Phase 1: Analysis & Inventory ✅ DONE
- [x] Create NEXT_STEPS directory
- [x] Build file inventory
- [x] Identify large files needing chunking
- [x] Complete prd.md reading
- [x] Read agent_definition.md
- [x] Analyze Generic Agent Monitoring Architecture
- [x] Process SwarmForge Roadmap
- [x] Read MACS notes (key deployment patterns)

### Phase 2: Gap Analysis ✅ DONE
- [x] Create DIFF: old PRD vs current implementation
- [x] List missing features
- [x] Identify conflicting patterns

### Phase 3: Voice System Integration ✅ DONE
- [x] Web search: Microsoft Vibe Voice
- [x] Web search: NVIDIA Parakeet v3
- [x] Document integration approach (02_VOICE_INTEGRATION.md)
- [x] Implement vibevoice_tts.py
- [x] Implement parakeet_stt.py
- [x] Create TTS/STT routers

### Phase 4: Agent Template Standardization ✅ DONE
- [x] Catalog all agent formats in amalgam
- [x] Analyze format trade-offs
- [x] Design optimal unified template
- [x] Create AGENT_TEMPLATE_SPEC.md
- [x] Migrate 33 agents with scripts/migrate_agents.py

### Phase 5: PRD Generation ✅ DONE
- [x] Draft MIGRATION_PRD.md (05_MIGRATION_PRD.md) - 857 lines
- [x] Expand with competitor analysis

### Phase 6: Migration Implementation ✅ DONE
- [x] Phase 1: Voice System (TTS/STT)
- [x] Phase 2: Agent Template Migration
- [x] Phase 3: Observability Hook Migration
- [x] Phase 4: Script-Based Progressive Disclosure
- [x] Phase 5: Council Voting Implementation
- [x] Phase 6: MACS Mission Launcher

### Phase 7: Amalgam Audit ✅ DONE
- [x] Categorize 340 files with 9-category schema
- [x] Create 07_AMALGAM_AUDIT.md
- [x] Create 08_INTEGRATION_PROTOCOL_TEMPLATE.md
- [x] Add large file chunking protocol

### Phase 8: Adversarial Validation ✅ DONE
- [x] 10-member, 2-round validation of deferred elements
- [x] Web search grounding (3 rounds)
- [x] Create 09_ADVERSARIAL_VALIDATION.md
- [x] Create 10_OPTIMIZED_INTEGRATION_PLAN.md

### Phase 9: Unprocessed Files ✅ DONE
- [x] Process docs/ subdirectory (7 files)
- [x] Extract CCPS pattern
- [x] Extract Claude folder architecture
- [x] Create 11_UNPROCESSED_EXTRACTION.md

### Phase 10: MACS Extract Integration ✅ DONE
- [x] Inventory MACS extract folders (21 files)
- [x] Process synthesis documents
- [x] Process arc lists
- [x] Process debates
- [x] Process embedded configs
- [x] Create 12_MACS_INTEGRATION_ASSESSMENT.md
- [x] Evaluate format quality

### Phase 11: PRD Feature Integration ✅ DONE
- [x] Build swarm-cli (`scripts/swarm_cli.py`) - 380 lines
- [x] Implement skill loader (`scripts/skill_loader.py`) - 320 lines
- [x] Create budget governor hook (`.claude/hooks/budget_governor.py`) - 280 lines
- [x] Port 5 priority skills to `components/skills/`
- [x] Create 7 slash commands in `.claude/commands/`
- [x] Create agent taxonomy directories (council/, swarm/)

### Phase 12: PRD Completion ✅ DONE
- [x] Add continuation/nudge support to mission_launcher
- [x] Categorize agents into council/ (5) vs swarm/ (9)
- [x] Create 3-layer proxy config template
- [x] Port remaining 12 skills from amalgam

---

## NEXT_STEPS Documents (12)
| # | File | Lines | Purpose |
|:--|:-----|:------|:--------|
| 00 | SCRATCH.md | ~125 | Working notes |
| 01 | TASK_TRACKER.md | ~90 | This file |
| 02 | VOICE_INTEGRATION.md | ~131 | TTS/STT research |
| 03 | FEATURE_GAP_ANALYSIS.md | ~118 | PRD vs implementation |
| 04 | AGENT_TEMPLATE_SPEC.md | ~233 | Optimal agent format |
| 05 | MIGRATION_PRD.md | ~857 | Comprehensive PRD |
| 06 | AMALGAM_INSIGHTS.md | ~400 | Extracted patterns |
| 07 | AMALGAM_AUDIT.md | ~200 | File categorization |
| 08 | INTEGRATION_PROTOCOL_TEMPLATE.md | ~300 | Universal parsing protocol |
| 09 | ADVERSARIAL_VALIDATION.md | ~350 | 10-member council validation |
| 10 | OPTIMIZED_INTEGRATION_PLAN.md | ~270 | Execution-ready plan |
| 11 | UNPROCESSED_EXTRACTION.md | ~200 | New patterns from docs/ |
| 12 | MACS_INTEGRATION_ASSESSMENT.md | ~350 | MACS extract analysis |

---

## Implementation Status
| Component | Status | Files |
|:----------|:-------|:------|
| Voice TTS | ✅ | `components/hooks/utils/tts/*.py` |
| Voice STT | ✅ | `components/hooks/utils/stt/*.py` |
| Council Voting | ✅ | `scripts/council.py` |
| Mission Launcher | ✅ | `scripts/mission_launcher.py` |
| Progressive Tools | ✅ | `scripts/tools/*.py` |
| Observability Hooks | ✅ | `.claude/hooks/*.py` |
| Swarm CLI | ⏳ | `scripts/swarm_cli.py` (pending) |
| Skill Loader | ⏳ | `scripts/skill_loader.py` (pending) |

