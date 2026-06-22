# Archive Manifest - 2025-12-12

**Date:** 2025-12-12T05:00:00-08:00
**Operation:** Project Consolidation & PRD v3.0 Creation

---

## Files Archived

### Documentation (from docs/)
| Original Path | New Path | Reason |
|:--------------|:---------|:-------|
| `docs/amalgam/` | `archive/2025-12-12_docs/amalgam/` | Research material, concepts extracted to skills |

### Specifications (from specifications/)
| Original Path | New Path | Reason |
|:--------------|:---------|:-------|
| `specifications/archive/` | `archive/2025-12-12_docs/specifications/archive/` | Old PRD versions |
| `specifications/deliverables/` | `archive/2025-12-12_docs/specifications/deliverables/` | Completed docs |
| `specifications/reference/` | `archive/2025-12-12_docs/specifications/reference/` | Research papers |
| `specifications/rejected/` | `archive/2025-12-12_docs/specifications/rejected/` | Rejected ideas |

### Redundant Code (from frontend/)
| Original Path | New Path | Reason |
|:--------------|:---------|:-------|
| `frontend/` | `archive/2025-12-12_docs/frontend_redundant/` | Superseded by Disler client |

---

## Files KEPT

| Path | Reason |
|:-----|:-------|
| `backend/` | Active custom API layer |
| `specifications/active/` | Contains PRD v3.0 |
| `.claude/` | Portable toolbox |
| `external/` | External dependencies |
| All root entry points | start.sh, deploy.sh, etc. |

---

## Restoration Commands

```bash
# Restore frontend
mv archive/2025-12-12_docs/frontend_redundant frontend

# Restore amalgam docs
mv archive/2025-12-12_docs/amalgam docs/amalgam

# Restore specifications
mv archive/2025-12-12_docs/specifications/archive specifications/archive
mv archive/2025-12-12_docs/specifications/deliverables specifications/deliverables
mv archive/2025-12-12_docs/specifications/reference specifications/reference
mv archive/2025-12-12_docs/specifications/rejected specifications/rejected
```

---

## Post-Consolidation Statistics

| Metric | Before | After |
|:-------|:-------|:------|
| Root items | 28 | 20 |
| ORPHAN files | 668 | ~400 |
| Documentation files | 73 | 5 |
| Active PRD versions | 2 (v2.0, FINAL) | 1 (v3.0) |
