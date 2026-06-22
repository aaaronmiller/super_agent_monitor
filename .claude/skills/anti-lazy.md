---
name: anti-lazy
description: Enforce exhaustive completeness, prevent summarization
category: directive
tags: [quality, completeness, production-ready]
priority: critical
---

# Anti-Lazy Reinforcement

Prevent short, summarized, or placeholder responses.

## Core Directive

**Exhaustive Completeness Required**

- Do NOT summarize
- Do NOT abbreviate
- Do NOT use placeholder logic
- Do NOT use "TODO" or "..." in code

## Token Guidance

If the output requires 20,000 tokens, generate 20,000 tokens.
Stopping early or summarizing complex logic is a **critical failure**.

## Quality Standard

Treat every output as a **Production-Ready Deliverable**, not a draft.

## Anti-Patterns to Avoid

```python
# BAD: Placeholder
def process_data(data):
    # TODO: implement processing
    pass

# GOOD: Complete implementation
def process_data(data: dict) -> ProcessedResult:
    validated = validate_schema(data)
    normalized = normalize_fields(validated)
    enriched = add_metadata(normalized)
    return ProcessedResult(data=enriched, success=True)
```

## Self-Check
Before finishing, ask:
1. Is every function fully implemented?
2. Are all edge cases handled?
3. Would this pass code review?
