# How to Pick an Orchestrator

This directory contains a library of **Orchestration Templates** designed to optimize agent performance for specific types of tasks. These patterns are based on adversarial validation research.

## The Catalog

### 1. Adaptive Router (`templates/adaptive-router.md`)
*   **Use When**: You are unsure which pattern to use.
*   **Function**: Acts as a "Meta-Agent" that analyzes the request and selects the best specific orchestrator.
*   **Best For**: General purpose entry point.

### 2. CEO Council (`templates/ceo-council.md`)
*   **Use When**: You need deep reasoning, strategy, or creative problem solving.
*   **Mechanism**: Simulates a council of experts. Rounds 1-4 are for debate and critique; Round 5 is for synthesis.
*   **Best For**: Complex architectural decisions, strategic planning, nuanced writing.

### 3. Playoff Debate (`templates/playoff-debate.md`)
*   **Use When**: You need to choose the "best" option from several alternatives.
*   **Mechanism**: Tournament style elimination (8 -> 4 -> 2 -> 1). Agents aggressively critique and debunk each other.
*   **Best For**: Selecting a tech stack, comparing products, making binary decisions.

### 4. RCR Protocol (`templates/rcr-critique.md`)
*   **Use When**: You need to improve an existing draft or code snippet.
*   **Mechanism**: **R**eflect (self-correction), **C**ritique (hostile review), **R**efine (improvement).
*   **Best For**: Code review, debugging, editing, polishing content.

### 5. Research Deep Dive (`templates/research-deep-dive.md`)
*   **Use When**: You need comprehensive information on a topic.
*   **Mechanism**: Decomposes the topic -> Runs parallel exhaustive searches -> Cross-validates findings -> Synthesizes report.
*   **Best For**: "Tell me everything about X", finding obscure information ("Needle in a Haystack").

## Usage

To use an orchestrator, copy the content of the desired template into your active `CLAUDE.md` or system prompt configuration.

```

## 📊 Visual Comparison

### 1. CEO Council (Deep Reasoning)
*Sequential refinement with expert critique.*

```mermaid
graph LR
    Start((Start)) --> R1[Round 1: Analyze]
    R1 --> Search1[Tool: Search]
    Search1 --> R2[Round 2: Critique]
    R2 --> R3[Round 3: Refine]
    R3 --> R5[Round 5: Synthesize]
    R5 --> Search2[Tool: Verify]
    Search2 --> End((End))
    
    style Start fill:#fff,stroke:#333
    style End fill:#000,stroke:#333,color:#fff
    style Search1 fill:#f9f,stroke:#333
    style Search2 fill:#f9f,stroke:#333
```

### 2. Playoff Debate (Decision Making)
*Tournament-style elimination of weaker options.*

```mermaid
graph TD
    Start((Start)) --> QF[8 Agents: Argue]
    QF --> Search1[Tool: Search All]
    Search1 --> Elim1{Eliminate 4}
    Elim1 --> SF[4 Agents: Rebut]
    SF --> Search2[Tool: Search All]
    Search2 --> Elim2{Eliminate 2}
    Elim2 --> Final[2 Agents: Duel]
    Final --> Winner((Winner))
    
    style Start fill:#fff,stroke:#333
    style Winner fill:#000,stroke:#333,color:#fff
    style Search1 fill:#f9f,stroke:#333
    style Search2 fill:#f9f,stroke:#333
    style Elim1 fill:#faa,stroke:#333
    style Elim2 fill:#faa,stroke:#333
```

### 3. RCR Protocol (Quality Assurance)
*Circular loop for continuous improvement.*

```mermaid
graph LR
    Start((Start)) --> Reflect[Reflect]
    Reflect --> Critique[Critique]
    Critique --> Search[Tool: Verify]
    Search --> Refine[Refine]
    Refine --> Check{Good Enough?}
    Check -- No --> Reflect
    Check -- Yes --> End((End))
    
    style Start fill:#fff,stroke:#333
    style End fill:#000,stroke:#333,color:#fff
    style Search fill:#f9f,stroke:#333
    style Check fill:#faa,stroke:#333
```

### 4. Research Deep Dive (Information Gathering)
*Parallel execution for maximum coverage.*

```mermaid
graph TD
    Start((Start)) --> Decompose[Decompose Topic]
    Decompose --> B1[Sub-topic 1]
    Decompose --> B2[Sub-topic 2]
    Decompose --> B3[Sub-topic 3]
    
    B1 --> S1[Tool: Search]
    B2 --> S2[Tool: Search]
    B3 --> S3[Tool: Search]
    
    S1 --> Validate[Cross-Validate]
    S2 --> Validate
    S3 --> Validate
    
    Validate --> Synthesize[Synthesize Report]
    Synthesize --> End((End))
    
    style Start fill:#fff,stroke:#333
    style End fill:#000,stroke:#333,color:#fff
    style S1 fill:#f9f,stroke:#333
    style S2 fill:#f9f,stroke:#333
    style S3 fill:#f9f,stroke:#333
```
