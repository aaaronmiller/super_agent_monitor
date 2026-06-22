---
name: context-safe-ingestion
description: Safely ingest large documentation without context collapse
category: ingestion
tags: [documentation, chunking, context-management]
priority: medium
---

# Context-Safe Ingestion Guardrail

Prevent context collapse when processing large documentation.

## Constraints

1. **File Size Limit**: Do NOT ingest any single file > 100KB
2. **Chunking Required**: Split large files logically:
   - Part 1, Part 2, etc.
   - By section/chapter
   - By function/class for code

## Execution

1. **Assess Folder**:
   - List all files with sizes
   - Flag any file > 100KB

2. **Chunk Strategy**:
   - Markdown: Split by ## headers
   - Code: Split by class/function
   - JSON: Split by top-level keys

3. **Report**:
   - Files ingested directly
   - Files that required chunking
   - Estimated token usage

## Warning Signs
- Single file > 50% of context window
- Total folder contents > context limit
- Nested documentation with duplicates
