# Adversarial Validation & Council Reasoning Methodologies

> **Research Date:** December 2025  
> **Purpose:** Reference documentation for advanced reasoning patterns, council formations, and interspersed tool-use protocols.

---

## Council Formation Patterns

### CEO (Critique-Enhanced Orchestration)
- **Rounds:** 3-5 sequential with all agents participating
- **Best for:** Complex multi-dimensional problems
- **Tool-use:** Search allowed Round 1 and Round 5 only
- **Advantage:** Collective intelligence compounds across rounds

### Playoff/Tournament
- **Rounds:** log₂(n) rounds (8→4→2→1 for 8 agents)
- **Best for:** Clear-cut solutions, decision tasks
- **Tool-use:** Search every round (8+4+2 = 14 total vs 8×5 = 40 for CEO)
- **Advantage:** Faster convergence, reduces lazy-agent collapse

### RCR (Reflect-Critique-Refine)
1. **Reflect** - state why current answer could be wrong
2. **Critique** - analyze exactly two peer rationales with specific flaws
3. **Refine** - update answer with new reasoning steps
- **Result:** +2-10% accuracy gains over base debate

---

## Task-to-Pattern Mapping

| Task Type | Pattern | Tool Protocol | Rationale |
|-----------|---------|---------------|-----------|
| Factual research | Single agent | Multi-search + synthesis | No debate needed |
| Technical decisions | Playoff (3 rounds) | Search every round | Clear winner emerges |
| Creative/strategic | CEO (5 rounds) | Search R1 + R5 | Needs iteration |
| Code review | RCR debate | Search for stdlib/docs | Structured critique |
| Multi-domain | Adaptive | Dynamic allocation | Task-dependent |

---

## Interspersed Tool-Use Protocol

### Optimal Search Timing
- **Round 1:** Each council member gets search - grounds initial positions
- **Last round:** Validation phase - catches consensus errors
- **Playoff exception:** Every round searches (12 total vs 40 for CEO)

### Non-Council Research Assistant Pattern
```
Round structure:
1. Gimpy Helper performs multi-search on topic/last-round-statements
2. Presents findings to all council members
3. Council deliberates with grounded context
4. Cycle repeats
```

**Benefits:**
- Prevents search result bias (agents cherry-picking)
- Eliminates redundant searches
- Avoids context pollution (different search results)

---

## Frontier Training Paradigms (Nov 2025)

### 1. OpenAI: Deliberative Alignment
- Embeds safety specs directly into reasoning chains
- Model "conjures up" relevant policy excerpts mid-reasoning
- Uses test-time compute scaling (hundreds of candidate paths)
- **Extends** verifier training by internalizing evaluation criteria

### 2. Anthropic: Constitutional AI (RLAIF)
- Self-critique and revision loops
- Model critiques OWN response against constitutional principles
- Chain-of-thought improves transparency
- **Alternative** to verifier - reduces human labeling needs

### 3. Google Gemini: Iterative User Feedback
- Gemini training Gemini on feedback patterns
- Extended post-training iteration from deployment
- Self-verification during inference
- **Orthogonal** to verifier - continuous improvement focus

### 4. DeepSeek/VibeThinker: Process Supervision
- Step-level verification with process rewards
- GRPO (Group Relative Policy Optimization)
- MaxEnt focus on high-uncertainty problems
- **Core** verifier approach - most open/reproducible

---

## Model Comparison (Nov 2025)

| Model | Thinking Budget | Visible Output | Total | Release |
|-------|-----------------|----------------|-------|---------|
| GPT-5.1 Codex-Max | 32M tokens | 196k | 32M+ | Nov 2025 |
| Claude Opus 4.5 | 128k | 200k | 328k | Nov 2025 |
| Gemini 3 | Variable | 256k | 2M ctx | Nov 2025 |
| DeepSeekMath-V2 | Transparent | ~200k | ~200k | Nov 27-28, 2025 |
| VibeThinker-1.5B | Transparent | 128k+ | 128k+ | Nov 3, 2025 |

### Reasoning Model Equivalency
| Reasoning Model | Dense Equivalent | Multiplier |
|-----------------|------------------|------------|
| VibeThinker-1.5B | ~300-600B | 200-400x |
| Dr. Tulu-8B | ~100-200B | 12-25x |
| DeepSeek R1-14B | ~70B | 5x |

---

## Bootstrapping Multi-Trace Reasoning

### Triple-Chain Protocol
```
TRACE 1: RAPID ANALYSIS (3k tokens)
- Pattern matching, heuristic shortcuts
- Confidence: Medium

TRACE 2: METHODICAL VERIFICATION (8k tokens)  
- Systematic validation of Trace 1
- Identify contradictions
- Confidence: High

TRACE 3: ADVERSARIAL REVIEW (8k tokens)
- Challenge both previous traces
- If attacks succeed → spawn TRACE 4
- Confidence: Very High

TRACE 4: RECONCILIATION (if needed)
- Meta-analysis of reasoning strategies
- Hybrid solution
```

### Visible Output Exploitation
- Hidden thinking has separate budgets (can't bypass with prompts)
- Visible output CAN be hijacked for reasoning traces
- DeepSeek R1, VibeThinker use transparent reasoning
- Claude 3.7: 128k hidden + 128k visible = **256k total**

---

## Local Model Setups (M3 Max 36GB)

### Recommended Configuration
```
Target: Qwen3-32B-Instruct-MLX-4bit (~20GB)
Draft: Qwen3-0.5B-Instruct-MLX-4bit (~0.5GB)
Speculative Decoding: Enabled (2.4x speedup)
Output: 131k tokens
```

### 4-Model Council Setup
```
Member 1: VibeThinker-1.5B (math) @ 1.2GB
Member 2: Dr. Tulu-8B (research) @ 5GB  
Member 3: Qwen3-14B (general) @ 9GB
Member 4: DeepSeek-R1 14B (transparent) @ 9GB
Total: ~24GB RAM
```

---

## Sources
- arxiv.org/html/2505.15734v1 (Multi-agent debate)
- arxiv.org/html/2511.02303v1 (Dr. MAMR research)
- arxiv.org/html/2511.06221v1 (VibeThinker)
- platform.claude.com/docs (Extended Thinking)
- openai.com/index/deliberative-alignment/
- anthropic.com/research/constitutional-ai
