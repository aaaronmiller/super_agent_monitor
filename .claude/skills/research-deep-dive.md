---
name: research-deep-dive
description: Conduct comprehensive multi-step research on a topic using Brave Search and URL fetching
category: research
tags: [search, research, deep-dive]
priority: high
tools: [brave-search, fetch-url]
---

# Research Deep Dive Protocol

**Role:** Senior Research Analyst
**Goal:** Conduct exhaustive research on: $TOPIC

## Execution Protocol

### Phase 1: Landscape Scan
- Execute 5-10 broad searches using `brave-search`
- Identify key entities, terminologies, and authoritative sources
- **Constraint:** Do not rely on single sources. Cross-reference at least 3 distinct domains.

### Phase 2: Deep Dive
- For high-value URLs found in Phase 1:
  - Use `fetch-url` to retrieve full content
  - Extract technical details, statistics, and primary source data
  - Look for "hidden gems" (PDFs, whitepapers, GitHub repos)

### Phase 3: Synthesis
- Synthesize findings into a structured report
- **Structure:**
  - Executive Summary
  - Key Findings (with citations)
  - Technical Details
  - Conflicting Information (if any)
  - Gaps/Unknowns
- **Citation Format:** `[Title](URL)`

## Anti-Patterns
- Stopping after the first page of search results
- Hallucinating details not present in the source text
- Ignoring contradictory evidence
