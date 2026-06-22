# Improvement Proposal: Round 2 (The "Polish" Phase)

**Objective**: Implement the top 5 improvements identified by the Adversarial Council to reduce friction and increase trust.

## 🏆 Top 5 Improvements

### 1. 🚀 Quick Launch Button
*   **Problem**: Starting a trending workflow takes 2 clicks (Dashboard -> Detail -> Start).
*   **Solution**: Add a "▶" button directly on the "Trending Workflows" card in `Dashboard.vue`.
*   **Implementation**:
    *   Add button to card.
    *   On click, open a "Quick Start" modal (simplified version of `WorkflowDetail` modal).
    *   Or, just redirect to `WorkflowDetail` with the modal *already open* via query param (`?start=true`).

### 2. 🧐 Context Inspector
*   **Problem**: Users don't know if "Context Injection" actually worked or what it found.
*   **Solution**: Add a collapsible "Injected Context" block to the `SessionDetail.vue` log.
*   **Implementation**:
    *   Backend: When injecting context, log a special event `type: 'system_context'`.
    *   Frontend: Render this event as a collapsible JSON/Text block.

### 3. ⏩ Skip Animation
*   **Problem**: The "Typewriter" effect is cool but slow for long outputs.
*   **Solution**: Click the terminal area to instantly drain the buffer.
*   **Implementation**:
    *   Update `Typewriter.ts` to add a `flush()` method.
    *   Bind `click` event on `SessionDetail.vue` terminal to call `flush()`.

### 4. 🔍 Memory Search
*   **Problem**: The Memory page is a static list.
*   **Solution**: Add a client-side search bar.
*   **Implementation**:
    *   Add `<input v-model="searchQuery">` to `Memory.vue`.
    *   Filter the `memories` array based on the query.

### 5. 🏥 Proxy Health Indicator
*   **Problem**: "System Status" doesn't explicitly show the Proxy port status.
*   **Solution**: Add a specific check for the Proxy.
*   **Implementation**:
    *   Update `SystemCheckService.ts` to ping the proxy port.
    *   Update `SystemStatus.vue` to show "Proxy: Online".

---

## 📅 Implementation Plan

1.  **Phase 1: Low Hanging Fruit** (Memory Search, Proxy Health)
2.  **Phase 2: UX Friction** (Quick Launch, Skip Animation)
3.  **Phase 3: Trust** (Context Inspector)

## 🗳️ Council Recommendation
**EXECUTE ALL**. These are low-effort, high-impact changes that significantly polish the user experience.
