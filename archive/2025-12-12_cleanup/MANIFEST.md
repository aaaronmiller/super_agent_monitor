# Archive Manifest - 2025-12-12

**Protocol:** Project Gardener v2.1
**Operator:** Antigravity (Gemini)
**Date:** 2025-12-12T04:15:00-08:00

---

## Files Moved

| Original Path | Archive Path | Lineage | Reason |
|:--------------|:-------------|:--------|:-------|
| `NEXT_STEPS/00_SCRATCH.md` | `NEXT_STEPS/00_SCRATCH.md` | LOG | Superseded by current system |
| `NEXT_STEPS/01_TASK_TRACKER.md` | `NEXT_STEPS/01_TASK_TRACKER.md` | LOG | Superseded |
| `NEXT_STEPS/02_VOICE_INTEGRATION.md` | `NEXT_STEPS/02_VOICE_INTEGRATION.md` | LOG | Deliverable exists (tts_service.py) |
| `NEXT_STEPS/03_FEATURE_GAP_ANALYSIS.md` | `NEXT_STEPS/03_FEATURE_GAP_ANALYSIS.md` | LOG | Superseded by reorganization |
| `NEXT_STEPS/04_AGENT_TEMPLATE_SPEC.md` | `NEXT_STEPS/04_AGENT_TEMPLATE_SPEC.md` | LOG | Integrated into .claude/agents/ |
| `NEXT_STEPS/05_MIGRATION_PRD.md` | `NEXT_STEPS/05_MIGRATION_PRD.md` | LOG | Completed |
| `NEXT_STEPS/06_AMALGAM_INSIGHTS.md` | `NEXT_STEPS/06_AMALGAM_INSIGHTS.md` | LOG | Integrated |
| `NEXT_STEPS/07_AMALGAM_AUDIT.md` | `NEXT_STEPS/07_AMALGAM_AUDIT.md` | LOG | Completed |
| `NEXT_STEPS/08_INTEGRATION_PROTOCOL_TEMPLATE.md` | `NEXT_STEPS/08_INTEGRATION_PROTOCOL_TEMPLATE.md` | LOG | Superseded |
| `NEXT_STEPS/09_ADVERSARIAL_VALIDATION.md` | `NEXT_STEPS/09_ADVERSARIAL_VALIDATION.md` | LOG | Completed |
| `NEXT_STEPS/10_OPTIMIZED_INTEGRATION_PLAN.md` | `NEXT_STEPS/10_OPTIMIZED_INTEGRATION_PLAN.md` | LOG | Completed |
| `NEXT_STEPS/11_UNPROCESSED_EXTRACTION.md` | `NEXT_STEPS/11_UNPROCESSED_EXTRACTION.md` | LOG | Superseded |
| `apply_patches.sh` | `root_orphans/apply_patches.sh` | ORPHAN | Duplicate of .claude/scripts/apply-patches.sh |
| `dev.sh` | `root_orphans/dev.sh` | ORPHAN | Unclear usage, no dependents |
| `shell-functions.sh` | `root_orphans/shell-functions.sh` | ORPHAN | Unclear usage, no dependents |
| `update_deps.sh` | `root_orphans/update_deps.sh` | ORPHAN | Unclear usage, no dependents |

---

## How to Restore

To restore any file, run:

```bash
# Example: restore 02_VOICE_INTEGRATION.md
mv archive/2025-12-12_cleanup/NEXT_STEPS/02_VOICE_INTEGRATION.md NEXT_STEPS/

# Example: restore dev.sh
mv archive/2025-12-12_cleanup/root_orphans/dev.sh ./

# Restore ALL files (full rollback)
mv archive/2025-12-12_cleanup/NEXT_STEPS/* NEXT_STEPS/
mv archive/2025-12-12_cleanup/root_orphans/* ./
```

---

## Verification

- `sam.py --status`: ✅ 49 skills, 78 agents, 12 swarms
- Entry points: ✅ start.sh, deploy.sh intact
- Active file: `NEXT_STEPS/12_MACS_INTEGRATION_ASSESSMENT.md` retained
