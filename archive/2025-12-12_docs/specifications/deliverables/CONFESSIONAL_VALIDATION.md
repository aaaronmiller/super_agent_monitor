# Confessional Validation: The "Last Mile" Gaps

**Objective**: Verify if "Trending Workflows" and "Context Injection" are *fully* implemented (Frontend + Backend).

## 🔍 Findings

### 1. Trending Workflows
*   **Backend**: ✅ Implemented (`workflows.ts` sorts by `usageCount`).
*   **Frontend**: ❌ **MISSING**. `Dashboard.vue` does not display a "Trending" section. It only shows "Recent Sessions".
*   **Verdict**: **PARTIAL FAILURE**. The user cannot *see* the trending workflows.

### 2. Context Injection
*   **Backend**: ✅ Implemented (`SessionLauncher.ts` handles `contextInjection` flag).
*   **Frontend**: ❌ **MISSING**. `WorkflowDetail.vue` (Start Modal) has no checkbox for "Context Injection" and no input for "Initial Prompt".
*   **Verdict**: **PARTIAL FAILURE**. The user cannot *use* the feature.

### 3. Help Page (Visuals)
*   **Docs**: ✅ Created (`docs/VISUALS.md`).
*   **Frontend**: ❌ **MISSING**. No `/help` route or view exists.
*   **Verdict**: **FAILURE**. The visuals are hidden in the repo, not in the app.

---

## 🛠️ Remediation Plan (The "Immediate Mandate")

### 1. Dashboard Upgrade
*   **Action**: Update `Dashboard.vue` to fetch workflows and display the top 3 sorted by `usageCount` in a new "🔥 Trending Workflows" card.

### 2. Session Start Upgrade
*   **Action**: Update `WorkflowDetail.vue` modal:
    *   Add `textarea` for "Initial Prompt" (User Task).
    *   Add `checkbox` for "Enable Context Injection (Auto-RAG)".
    *   Update `sessionsStore.createSession` to accept these new parameters.

### 3. Help Page Implementation
*   **Action**: Create `frontend/src/views/Help.vue`.
*   **Action**: Install `mermaid` (if possible) or render simplified diagrams.
*   **Action**: Add `/help` route in `router/index.ts`.
*   **Action**: Add "Help" link to the Sidebar/Navigation.

## 🗳️ Confessional Vote
*   **The Council**: Unanimously agrees that these are **CRITICAL GAPS** preventing the user from realizing the value of the backend work.
*   **Mandate**: **EXECUTE IMMEDIATELY**.
