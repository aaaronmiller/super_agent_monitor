# Skill: memory-ingest
## Purpose
Push key outcomes into the internal memory systems.

## Implementation
- Append:
  - Findings, decisions, outcomes
- To:
  - `.delobotomize/memory/snapshots/*.json`
  - And, if configured, call MCP "delobotomize-memory" server
- No behavioral claims beyond storing/querying this project

## Input
- `phase` (scan|triage|remediate|verify|iterate)
- `results` (structured data)
- `metadata` (timestamp, run_id, etc.)

## Output
- Success confirmation
- Snapshot path
- Query endpoint info (if MCP enabled)

## Safety
- Additive writes only
- No deletions or overwrites
- Atomic snapshot creation
