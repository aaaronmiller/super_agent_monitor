# Upstream Modifications Log

> **Purpose:** This document tracks changes made to code ported from upstream projects to ensure smooth future upgrades and avoid merge conflicts.

---

## Source Projects

| Project | Repository | Purpose |
|---------|------------|---------|
| Primary | `disler/claude-code-hooks-multi-agent-observability` | Real-time observability components |
| Fork | `apolopena` fork | Additional patches |

---

## General Changes

| Change | From | To | Reason |
|--------|------|-----|--------|
| API Port | `4000` | `3001` | Match local backend configuration |

---

## Component Modifications

### `SettingsPanel.vue`

| Endpoint | Original | Modified |
|----------|----------|----------|
| Settings | `http://localhost:4000/settings` | `http://localhost:3001/settings` |

### `FilterPanel.vue`

| Endpoint | Original | Modified |
|----------|----------|----------|
| Filter Options | `http://localhost:4000/events/filter-options` | `http://localhost:3001/events/filter-options` |
| Save Summary Prompt | `http://localhost:4000/events/save-summary-prompt` | `http://localhost:3001/events/save-summary-prompt` |
| Batch Summaries | `http://localhost:4000/events/batch-summaries` | `http://localhost:3001/events/batch-summaries` |

### `EventRow.vue`

| Endpoint | Original | Modified |
|----------|----------|----------|
| Respond | `http://localhost:4000/events/${id}/respond` | `http://localhost:3001/events/${id}/respond` |

---

## Composable Modifications

### `useThemes.ts`

| Endpoint | Original | Modified |
|----------|----------|----------|
| Themes | `http://localhost:4000/api/themes` | `http://localhost:3001/api/themes` |

### `useSettings.ts`

| Endpoint | Original | Modified |
|----------|----------|----------|
| Settings | `http://localhost:4000/settings` | `http://localhost:3001/settings` |

### `useWebSocket.ts`

| Endpoint | Original | Modified |
|----------|----------|----------|
| WebSocket | `ws://localhost:4000` | `ws://localhost:3001` (or relative path) |

---

## Upgrade Guide

When upgrading from upstream:

1. **Pull upstream changes** into a separate branch
2. **Review this log** to identify modified files
3. **Re-apply port changes** (`4000` → `3001`) to any new/changed endpoints
4. **Test locally** before merging

### Files Likely to Conflict

```
frontend/src/components/SettingsPanel.vue
frontend/src/components/FilterPanel.vue
frontend/src/components/EventRow.vue
frontend/src/composables/useThemes.ts
frontend/src/composables/useSettings.ts
frontend/src/composables/useWebSocket.ts
```

---

## Version History

| Date | Upstream Commit | Notes |
|------|-----------------|-------|
| 2025-12-05 | Initial port | Full component port with port changes |
