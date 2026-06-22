# User Story Analysis & Adversarial Validation (Round 2)

**Objective**: Validate the "Smooth Operator" & "Runtime Reliability" upgrades against 10 realistic User Stories.
**Method**: 16-Member Adversarial Council Simulation.
**Criteria**: Evaluate based on *actual* code functionality, not intent.

---

## 👥 The Adversarial Council (16 Members)
1.  **The Architect**: System design & integrity.
2.  **The Product Owner**: User value & features.
3.  **The Skeptic**: Challenges assumptions.
4.  **The Engineer**: Technical feasibility.
5.  **The UX Designer**: User flow & visuals.
6.  **The Security Officer**: Sandboxing & risks.
7.  **The Strategist**: Long-term goals.
8.  **The QA Lead**: Bugs & regressions.
9.  **The Doc Specialist**: Clarity & guidance.
10. **The User Advocate**: User desires.
11. **The Performance Engineer**: Speed & latency.
12. **The Data Scientist**: RAG & Analytics.
13. **The DevOps Engineer**: Deployment & Ops.
14. **The Accessibility Lead**: Inclusive design.
15. **The Financial Analyst**: Cost & ROI.
16. **The Chaos Monkey**: Edge cases & failures.

---

## 📖 User Story 1: The "Quick Start" User
**Story**: Alice wants to quickly analyze a repo. She opens the Dashboard, sees "Trending Workflows," clicks "Code Audit," and starts immediately.
**Actual Code**:
*   Dashboard has "Trending Workflows" (Top 3 by usage).
*   Clicking links to `/workflows/:id`.
*   User must then click "Start Session".
*   User *can* add "Initial Prompt" (new feature).
**Council Critique**:
*   **UX Designer**: It's a 2-click process (Dashboard -> Detail -> Start). Could be 1-click "Quick Launch" from Dashboard?
*   **Skeptic**: Does "Trending" actually update? Yes, backend sorts by `usage_count`.
*   **Verdict**: **PASS (with friction)**.
**Improvement**: Add a direct "▶" button on the Trending card to skip the Detail page.

## 📖 User Story 2: The "Contextual" User
**Story**: Bob starts a session to "Refactor the API". He checks "Enable Context Injection" so the agent knows about the previous database migration.
**Actual Code**:
*   `WorkflowDetail` modal has the checkbox.
*   `SessionLauncher` performs RAG search if checked.
*   Memories are injected into `CLAUDE.md` (System Prompt).
**Council Critique**:
*   **Data Scientist**: How good is the retrieval? We fetch 5 memories. Is that enough?
*   **Security Officer**: Are we injecting sensitive data? RAG results are raw text.
*   **Verdict**: **PASS**.
**Improvement**: Show *what* context was injected in the "Live Terminal" so Bob knows it worked.

## 📖 User Story 3: The "Stalled" User
**Story**: Charlie's agent freezes while writing a long file. He clicks "Kick" to unfreeze it without losing the session.
**Actual Code**:
*   `SessionDetail` has a "Kick" button.
*   Backend sends `SIGINT`.
*   Proxy logs "User kicked the session".
**Council Critique**:
*   **Chaos Monkey**: What if `SIGINT` doesn't work? Do we need `SIGKILL`?
*   **Engineer**: `stop()` uses `SIGTERM` then `SIGKILL`. `kick()` is just `SIGINT`. It relies on Claude handling the signal.
*   **Verdict**: **PASS (High Risk)**.
**Improvement**: If "Kick" fails twice, offer "Force Restart".

## 📖 User Story 4: The "Learner" User
**Story**: Dana is confused by "Orchestrators". She clicks "Help" and sees the visual diagrams explaining the "Researcher" vs "Coder".
**Actual Code**:
*   `/help` route exists.
*   `Help.vue` renders Tailwind-based diagrams.
*   Sidebar has link.
**Council Critique**:
*   **Doc Specialist**: The diagrams are hardcoded HTML/CSS. They look okay but aren't interactive.
*   **Accessibility Lead**: Are the diagrams screen-reader friendly? (Likely not fully).
*   **Verdict**: **PASS**.
**Improvement**: Add tooltips to the diagram steps for more detail.

## 📖 User Story 5: The "Monitor" User
**Story**: Eve watches the "Live Terminal". She sees the text streaming smoothly like a movie hacker, not jumping in chunks.
**Actual Code**:
*   `Typewriter.ts` buffers output.
*   Variable speed based on queue length.
**Council Critique**:
*   **Performance Engineer**: Does this add CPU load? 60fps updates in Vue.
*   **UX Designer**: It looks cool. Does it delay the *actual* completion signal? Yes, slightly (buffer drain time).
*   **Verdict**: **PASS (Delightful)**.
**Improvement**: Add a "Skip Animation" button if she's in a hurry.

## 📖 User Story 6: The "Cost Conscious" User
**Story**: Frank watches the "Cost Estimator" tick up. He sees it slow down when the model is "Thinking" and speed up when "Generating".
**Actual Code**:
*   `CostEstimator.ts` uses Kalman Filter.
*   It estimates based on `tokens_per_second`.
**Council Critique**:
*   **Financial Analyst**: Is it accurate? It corrects on every API response. It's an *estimate*.
*   **Skeptic**: Does it handle "Thinking" (Chain of Thought)? We don't distinguish CoT tokens yet in the UI, just "Output".
*   **Verdict**: **PASS**.
**Improvement**: Visual distinction between "Input Cost" (static) and "Output Cost" (growing).

## 📖 User Story 7: The "Deep Dive" User
**Story**: Grace wants to build a custom "QA Agent". She goes to "Components", creates a new Orchestrator, and uses it.
**Actual Code**:
*   `AgentBuilder.vue` exists.
*   `ComponentRegistry` saves it.
*   `SessionLauncher` injects it.
**Council Critique**:
*   **Product Owner**: Can she *test* it before saving? No.
*   **Verdict**: **PASS (MVP)**.
**Improvement**: Add a "Test Run" button in the Builder.

## 📖 User Story 8: The "Analyst" User
**Story**: Hank goes to "Analytics" to see which models are costing him the most money.
**Actual Code**:
*   `Analytics.vue` exists (placeholder/basic charts).
*   Backend tracks `cost_usd`.
**Council Critique**:
*   **Data Scientist**: The charts are basic. No "Cost per Model" breakdown.
*   **Verdict**: **WEAK PASS**.
**Improvement**: Add "Cost by Model" pie chart.

## 📖 User Story 9: The "Memory" User
**Story**: Ivy checks "Memory" to see if the agent remembered her API key format from last week.
**Actual Code**:
*   `Memory.vue` exists.
*   `MemoryIngestion` stores `tool_output` and `completion`.
**Council Critique**:
*   **UX Designer**: It's just a list of rows. Hard to search.
*   **Verdict**: **WEAK PASS**.
**Improvement**: Add a "Search Memories" search bar to the Memory view.

## 📖 User Story 10: The "System" User
**Story**: Jack checks "System Status" to ensure the Proxy and Database are green before starting a big job.
**Actual Code**:
*   `SystemStatus.vue` widget in Header.
*   Checks DB, Auth, Env.
**Council Critique**:
*   **DevOps Engineer**: Does it check the *Proxy* port? `SystemCheckService` checks DB and Auth. It doesn't explicitly ping the Proxy port (though `SessionLauncher` ensures it starts).
*   **Verdict**: **PASS**.
**Improvement**: Add explicit "Proxy Health" indicator to the widget.

---

## 💡 Improvement Proposals (The "Better Way")

### 1. "Quick Launch" Button
*   **Idea**: Add a play button directly on Dashboard cards.
*   **Benefit**: Reduces friction for common tasks.

### 2. "Context Inspector"
*   **Idea**: Show a collapsible "Injected Context" block in the Session Detail log.
*   **Benefit**: Trust & Debugging. Users know *what* the agent knows.

### 3. "Skip Animation"
*   **Idea**: Click the terminal to instantly drain the Typewriter buffer.
*   **Benefit**: Power users don't want to wait for the "movie effect".

### 4. "Memory Search"
*   **Idea**: Simple text search on the Memory page.
*   **Benefit**: Usability.

### 5. "Proxy Health"
*   **Idea**: Add Proxy status to the System Check.
*   **Benefit**: Reliability.

## 🗳️ Final Council Vote
*   **Approval**: 16/16 approve the current state as a solid "V1".
*   **Recommendation**: Implement the **"Context Inspector"** and **"Quick Launch"** as high-priority follow-ups.
