---
date: 2025-11-10 12:28:02 PST 
ver: 4.1.1 
author: Indie Dev Dan 
model: Gemini 
tags: [agents, mcp, context-window, cli, skills, progressive-disclosure, prompt-engineering, claude]
---

```

```
# Beyond MCP- 3 Alternatives for Agent Tool Use

links: [[AI Agent Architecture]], [[Prompt Engineering]], [[Context Window Management]]

## 📜 Executive Summary

This analysis synthesizes the core methodologies presented by Indie Dev Dan for connecting AI agents to external tools as alternatives to "MCP servers." The primary problem addressed is **context window consumption**, where a standard MCP server can consume 5-20% of an agent's available context before any work begins.

The core theme is to **"use raw code as tools."** The transcript details three specific, proven alternatives—**CLI-First**, **Script-Based**, and **Skills-Based**—that trade off complexity for granular control and significant context preservation. The analysis extracts these patterns, the "prime prompts" used to enable them, and the decision-making heuristic for when to use each approach.


## 🧠 Phase 1: Visual Concept Map

This mind map outlines the core problem, the three alternative solutions, and the decision-making framework presented in the transcript.

Code snippet

```
mindmap
  Root((Beyond MCP: Agent Tooling Alternatives))
    ---
    Problem: MCP Server Context Waste
      * "just ate 10,000 tokens"
      * "5% of my agent's context window"
      * "bleeding 20% plus context"
    ---
    Core Theme
      * "Use raw code as tools"
      * Tradeoff: Complexity for Control
    ---
    Alternative 1: CLI-First Approach
      * Mechanism: "Prime Prompt"
      * Action: Agent reads `readme.md` + `cli.py`
      * Agent Call: `market search trillionaire`
      * Benefit: Full control, dynamic setup
      * Result: Reduced context (10% -> 5.6%)
    ---
    Alternative 2: Script-Based Approach
      * Mechanism: "Prime Prompt" + "Progressive Disclosure"
      * Action: Agent reads `readme.md` (maps conditions to files)
      * Agent Call: `uv run ... scripts/search.py --json ...`
      * Key Tactic: "Do not read scripts themselves"
      * Benefit: Massive context savings
      * Result: <1% context use (~2k tokens)
      * Tradeoff: Code duplication
    ---
    Alternative 3: Skills-Based Approach
      * Mechanism: `skill.md` acts as prime prompt
      * Action: Bundles scripts in a `skills` directory
      * Benefit: Progressive disclosure, self-contained, isolated
      * Tradeoff: "Clawed ecosystem lock-in"
    ---
    Key Concepts
      * Priming Prompts
        * `/prime-kshi-cli-tools`
        * `/file-system-scripts`
      * Progressive Disclosure
        * Source: Anthropic
        * "Activate or ignore context"
        * "just a little bit of information"
      * "Trifecta" Development
        * CLI serves: You, Your Team, Your Agents
    ---
    Decision Heuristic (Tool Belt)
      * External Tools
        * 80%: MCP (Simplicity)
        * 15%: CLI (Control/Modify)
        * 5%: Scripts (Context Preservation)
      * New Tools
        * 80%: CLI (Trifecta)
        * 10%: MCP (Wrap CLI for scale)
        * 10%: Scripts (Context Preservation)
    ---
    Cited Sources
      * Anthropic (Progressive Disclosure)
      * Mario (Engineer, advocates raw code)
      * Vitalic (Info Finance)
```

---

## 🧐 Phase 2: Methodology Justification

- **Wrapper Selection:** The analysis employs a **research-enhanced analysis** wrapper. The speaker, Indie Dev Dan, explicitly cites and builds upon the work of others, including a blog post from **Anthropic** (on progressive disclosure), an engineer named **Mario** (on using raw code), and **Vitalic** (on "info finance"). A simple extraction would miss this context; therefore, the analysis integrates these external concepts as central to the speaker's methodology.
    
- **Methodology Justification:** The transcript's task geometry is a **comparative analysis of three distinct patterns** followed by a **decision-making heuristic**. The chosen article structure, with dedicated sections for each pattern, a comparative tradeoff table, and formalized appendices, provides the highest-fidelity representation of the speaker's logic. This structure directly mirrors the `deliverable_specification` by separating canonical definitions (Phase 3) from prompt examples (Phase 4) and evaluation (Phase 6).
    

---

## 🛠️ Phase 3: Extracted Patterns & Workflows

The transcript details three primary patterns for providing agent tool access, moving from a high-context MCP server to low-context raw code.

### 1. The CLI-First Tool Priming Pattern [Improves Context]

This pattern replaces the "all-or-nothing" context dump of an MCP server with a dynamic, just-in-time priming process.

- **Canonical Definition:** The agent is _not_ given MCP tools. Instead, the user executes a "prime prompt" (e.g., a slash command like `/prime-kshi-cli-tools`) that instructs the agent to read two specific files: a `readme.md` detailing the workflow and a `cli.py` file defining the available commands.
    
- **Workflow:**
    
    1. User starts a "clean" agent with no MCP server.
        
    2. User runs a prime prompt (e.g., `/prime-kshi-cli-tools`).
        
    3. The agent reads the specified `readme.md` and `cli.py` files into its context.
        
    4. The agent summarizes its new capabilities.
        
    5. The user can now issue commands (e.g., "market search trillionaire"), which the agent translates into the appropriate CLI calls (e.g., `market search "trillionaire"`).
        
- **Benefit:** This method cuts context window usage significantly (e.g., from 10% to 5.6%) by only loading the minimal code and instructions necessary. It also grants the developer full control over what the agent can and cannot do.
    

### 2. The Script-Based Progressive Disclosure Pattern [Improves Context]

This is the most advanced pattern, building on an idea from Anthropic to achieve maximum context preservation.

- **Canonical Definition:** The agent is primed with a _single `readme.md` file_. This file acts as a high-level router, mapping _conditions_ (user intents) to _specific, self-contained script files_ (e.g., `search.py`, `get_order_book.py`). The prime prompt _explicitly forbids_ the agent from reading the scripts themselves, instructing it to rely on `--help` flags or just execute them when a condition is met.
    
- **Workflow:**
    
    1. User runs a prime prompt (e.g., `/file-system-scripts`).
        
    2. The agent reads _only_ the `readme.md`, which lists available scripts and their "when to use" conditions.
        
    3. The agent's context usage is minimal (e.g., <1% or ~2k tokens).
        
    4. User issues a command (e.g., "search for government shutdown market").
        
    5. The agent identifies the correct script from its `readme.md` "map" (e.g., `search.py`) and executes it (e.g., `uv run apps/3-file-system/scripts/search.py --json "government shutdown"`).
        
    6. Context is only consumed for the _output_ of the script, not the script's code.
        
- **Benefit:** This is an "incremental context" approach that provides massive context savings, allowing an agent to scale to many tools without paying the upfront token cost.
    

### 3. The Skills-Based Bundling Pattern [Improves Context]

This pattern is functionally similar to the Script-Based approach but leverages the "Clawd ecosystem's" built-in "Skills" feature.

- **Canonical Definition:** A "skill" is a self-contained directory that bundles all necessary scripts. A `skill.md` file at the root of this directory acts as the prime prompt, which the agent reads automatically. This file, like the `readme.md` in Pattern 2, explains when to use each bundled script.
    
- **Workflow:**
    
    1. The agent (in the "Clawd" ecosystem) automatically discovers the `skill.md` file.
        
    2. It reads the high-level instructions, gaining knowledge of the skill (e.g., "Kshi Markets") and its sub-tools (the scripts).
        
    3. This process enables the same progressive disclosure as Pattern 2.
        
    4. User issues a command (e.g., "Kshi market search top LLM").
        
    5. The agent invokes the skill, which in turn runs the appropriate script.
        
- **Benefit:** High portability (copy the directory) and self-contained isolation.
    
- **Tradeoff:** The speaker explicitly notes this creates **"Clawed ecosystem lock-in,"** making it a platform-specific solution.
    

---

## 📊 Comparative Tradeoff Analysis

The speaker provides a clear breakdown of the tradeoffs between the approaches, which is synthesized into the table below.

|**Feature**|**MCP Server**|**CLI-First**|**Scripts-Based**|**Skills-Based**|
|---|---|---|---|---|
|**Invocation**|Automatic (on boot)|Manual (Prime Prompt)|Manual (Prime Prompt)|Automatic (on boot)|
|**Context Waste**|**Very High** (10k+ tokens)|**Medium** (~5.6k tokens)|**Very Low** (<2k tokens)|**Very Low** (<2k tokens)|
|**Customizability**|Low (if external)|**Full Control**|**Full Control**|**Full Control**|
|**Portability**|Low|High|**Very High** (single file)|**Very High** (single dir)|
|**Composability**|High (built-in)|Medium (needs local prompts)|Medium (needs local prompts)|High (within ecosystem)|
|**Simplicity**|**Very High**|Medium|Medium-High|High (within ecosystem)|
|**Eng. Investment**|Low (if external)|Medium|Medium-High|Medium|
|**Lock-In**|No (Open Standard)|None|None|**Yes (Clawed Ecosystem)**|

---

## 🧭 The Tool Belt Heuristic (Decision Framework)

Indie Dev Dan provides a two-part heuristic for deciding which pattern to use.

### 1. For **External Tools** (Tools you don't own):

- **80% of the time: Use the MCP Server.**
    
    - **Reason:** It's simple, standard, and fast. Don't reinvent the wheel.
        
- **15% of the time: Use the CLI-First Approach.**
    
    - **Reason:** Do this _only_ if you need to modify, extend, or specifically control the tools and context in a way the MCP server doesn't allow.
        
- **5% of the time: Use the Script-Based Approach.**
    
    - **Reason:** Do this as a last resort _only_ if context preservation is the absolute top priority and you're stacking many MCPs.
        

### 2. For **New Tools** (Tools you are building):

- **80% of the time: Use the CLI-First Approach.**
    
    - **Reason:** This hits the **"Trifecta"**: a single CLI works for **you** (the dev), **your team** (in CI/local), and **your agents**.
        
- **10% of the time: Wrap your CLI in an MCP Server.**
    
    - **Reason:** Do this _after_ building the CLI if you need to serve multiple agents at scale and want the convenience of the MCP standard. The speaker's MCP tools simply call his CLI, providing interoperability.
        
- **10% of the time: Use the Script-Based Approach.**
    
    - **Reason:** Again, only if you have many tools and context preservation is the paramount concern.
        

---

## 📋 Appendix A: Verbatim Prompts & Commands

The following prompts and commands were spoken verbatim by the user (Indie Dev Dan) during the transcript.

- `Kshi search markets OpenAI achieves AGI`
    
- `Get recent trades and get the order book for this market.`
    
- `Summarize bets and market sentiment in a concise table.`
    
- `/prime-kshi-cli-tools`
    
- `market search trillionaire`
    
- `Summarize bets and market sentiment for Elon and first trillionaire markets.`
    
- `Web search 2025, the net worth, uh, Jensen, Elon, and Sam, what market cap would their companies need to make them trillionaire?`
    
- `/file-system-scripts`
    
- `Koshi market search. I want to understand the government shutdown.`
    
- `Summarize bets. When can we expect the government shutdown to end?`
    
- `Kshi market search top LLM`
    

---

## 📝 Appendix B: Constructed Prompts

The following prompts are _constructed_ based on the speaker's detailed descriptions of the "prime prompts" used to enable the CLI and Script-based patterns.

### Constructed Prompt 1: CLI-First Priming Prompt

> **[Synthesized from the 25-line prompt description for `/prime-kshi-cli-tools`]**
> 
> **Task:** You are an AI agent that will interact with the Kshi prediction markets. Your tools are _not_ provided by an MCP server.
> 
> **Core Workflow:**
> 
> 1. **Read ONLY these two files** to understand your capabilities:
>     
>     - `apps/1-cli/readme.md` (This explains the overall workflow)
>         
>     - `apps/1-cli/cli.py` (This file defines the exact CLI commands, options, and arguments you can use)
>         
> 2. **DO NOT read any other Python files.** All functionality is exposed via the CLI.
>     
> 3. **Summarize** your understanding of the tools and common workflows from those two files.
>     
> 4. As you work with the user, **call the right CLI tools** to get the data you need.
>     

- **Genre:** Agent Priming, Tool-Loading
    
- **Difficulty:** Easy
    
- **Capabilities:** File Read, Command Execution, Summarization
    

### Constructed Prompt 2: Script-Based Progressive Disclosure Priming Prompt

> **[Synthesized from the description for `/file-system-scripts`]**
> 
> **Task:** You are an AI agent with access to a set of file-system scripts for the Kshi prediction markets.
> 
> **Critical Instruction: Context Preservation**
> 
> - You must **read ONLY the `apps/3-file-system/readme.md` file.**
>     
> - This file contains a list of available scripts and, crucially, the _conditions_ under which you should use each one.
>     
> - **DO NOT READ THE SCRIPTS THEMSELVES** to save context. Trust the `readme.md` map.
>     
> 
> **Workflow:**
> 
> 1. Read `apps/3-file-system/readme.md`.
>     
> 2. Summarize the mapping of conditions to scripts (e.g., "When user wants to search, I will use `search.py`").
>     
> 3. When a condition is met, execute the appropriate script using `uv run ...`.
>     
> 4. If you are unsure how a script works, you may use its `--help` flag, but _still do not read the file's source code_.
>     
> 5. State: "I will not read the scripts themselves unless --help doesn't provide the information needed."
>     

- **Genre:** Agent Priming, Progressive Disclosure, Context Management
    
- **Difficulty:** Medium
    
- **Capabilities:** File Read, Constrained Logic, Command Execution
    

### Constructed Prompt 3: "Lazy" 5-Line CLI Priming Prompt

> **[Synthesized from the speaker's "even simpler version" description]**
> 
> **Task:** Learn to use the Kshi CLI.
> 
> 1. Read these files:
>     
>     - `readme.md`
>         
>     - `cli.py`
>         
> 2. Summarize these tools.
>     
> 3. Now, you are ready to work.
>     

- **Genre:** Agent Priming (Minimal)
    
- **Difficulty:** Easy
    
- **Capabilities:** File Read, Summarization
    

---

## 🕵️‍♂️ Phase 5: Methodological Defense

- **Deviation Justification:** No deviations from the `analysis_protocol` were necessary. The transcript was well-structured, a fact which lent itself directly to the phased extraction process. The speaker's explicit signposting ("So the first version...", "For our next approach...", "There's one more way...") made identification of the three core patterns trivial.
    
- **Gap Analysis:** The primary ambiguity is the term **"MCP server."** The speaker uses it as a proper noun, but its exact definition (e.g., "Modular Co-Processor"?) is never given. It appears to be a term of art within the "Clawed" ecosystem, analogous to a generic plugin or tool server in other agentic systems. The analysis proceeds by accepting the speaker's terminology, as its function (a high-context, all-in-one tool provider) is made clear, even if its name is not.
    

---

## ✅ Phase 6: Quality Evaluation

### Coverage Checklist

- [x] Core Problem: MCP server context waste (10k tokens)
    
- [x] Alternative 1: CLI-First Approach
    
- [x] Alternative 2: Script-Based Approach (Progressive Disclosure)
    
- [x] Alternative 3: Skills-Based Approach (Clawed lock-in)
    
- [x] Key Concept: Prime Prompts
    
- [x] Key Concept: Progressive Disclosure (from Anthropic)
    
- [x] Key Concept: "Trifecta" (You, Team, Agents)
    
- [x] Tradeoff Table (Simplicity vs. Control vs. Context)
    
- [x] Decision Heuristic (External Tools vs. New Tools)
    
- [x] Cited Sources (Mario, Vitalic, Anthropic)
    

### Validation Framework

1. **Question:** What is the primary problem with traditional MCP servers identified in the transcript?
    
    - **Expected Answer:** They consume a large, static amount of the agent's context window (e.g., 5-20%) before any work is done.
        
2. **Question:** Explain the "Progressive Disclosure" pattern. How does it save context?
    
    - **Expected Answer:** The agent is given a `readme.md` that maps _intents_ to _scripts_. The agent is forbidden from reading the scripts' code, only executing them when the intent is matched. This saves context because the tool's code is never loaded, only its output.
        
3. **Question:** According to the speaker's heuristic, when should you build a CLI for a _new_ tool, and why?
    
    - **Expected Answer:** 80% of the time. The reason is the "Trifecta": a single CLI serves the developer, their team, and their agents, making it the most versatile and efficient starting point.
        
4. **Task:** A developer is using 3 external MCP servers, and their agent is "bleeding 20% context." They only use one or two tools from each server per session. What alternative pattern should they use and why?
    
    - **Expected Answer:** The Script-Based (or CLI-First) approach. This is the 5% "context preservation" case for external tools. They should write scripts/CLI wrappers that call _only_ the specific tools they need, then use a prime prompt to teach the agent to use those scripts instead of the full MCP servers.
        

### Benchmark Rubric

|**Criterion**|**1 (Novice)**|**2 (Competent)**|**3 (Proficient)**|**4 (Expert)**|
|---|---|---|---|---|
|**Accuracy**|Misrepresents the problem; thinks MCPs are "bad" without an exact reason.|Accurately describes the CLI, Script, and Skills alternatives.|Correctly explains _how_ the CLI and Script approaches save context (loading code vs. not).|Articulates the nuances of "progressive disclosure" and the "Trifecta" benefit of CLI-first development.|
|**Completeness**|Only mentions "use a CLI."|Describes the 3 alternatives but omits the decision-making framework.|Covers all 3 alternatives and the specific context savings (10% vs 5.6% vs <1%).|Covers all artifacts (MCP, CLI, Scripts, Skills) _and_ the 2-part decision heuristic (External vs. New tools).|
|**Transferability**|Cannot explain when to use each method.|Can repeat the speaker's heuristic (80% CLI, etc.) but cannot apply it.|Can correctly apply the heuristic to a new, hypothetical "new tool" vs. "external tool" scenario.|Can strategically reason about the tradeoffs, including "ecosystem lock-in" vs. portability, and justify _when_ to deviate from the heuristic.|
|**Instruction-Following**|Output does not follow the requested article structure.|Output is structured but misses key sections like appendices or the rubric.|Output includes all requested sections but with minimal detail.|Output provides a comprehensive, well-structured article that fulfills all requirements of the prompt.|

---

## 💡 Phase 7: Meta-Learning Note

The extraction of distinct, hierarchical patterns was significantly simplified by the speaker's strong pedagogical structure. The use of explicit signposting ("So the first version...", "For our next approach...", "There's one more way...") and a clear summary ("So, how am I using all of these...") provided a perfect skeleton for the analysis.

For future extractions, this transcript serves as a model: when a speaker explicitly references external sources (Anthropic, Mario), these should be treated as foundational to the speaker's own methodology and given a prominent place in the analysis (as done in Phase 2), rather than being relegated to a simple citation.