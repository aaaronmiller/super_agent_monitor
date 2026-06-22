---
name: signature-patterns
description: User's prompting DNA and rhetorical devices for better results
category: meta
tags: [patterns, style, optimization]
priority: medium
---

# Signature Prompting Patterns

Core rhetorical devices that consistently produce better results.

## Pattern 1: "The PRD is Garbage"
**Purpose:** Force rebuild from scratch rather than relying on flawed docs.
**Usage:** Start by disparaging existing documentation.
```
This PRD is incomplete garbage. Rebuild it from first principles using 
only the source code as ground truth.
```

## Pattern 2: "Ground Via Internet Research"
**Purpose:** Never trust model's internal knowledge alone.
**Usage:** Force current lookups.
```
Before proceeding, perform 5 web searches on current best practices 
for [specific tech]. Do not rely on training data.
```

## Pattern 3: "Source of Truth Consolidation"
**Purpose:** Fight context window degradation.
**Usage:** Obsessively consolidate scattered info.
```
Create a single source-of-truth document consolidating all 
requirements from these 12 scattered files.
```

## Pattern 4: "YOLO Mode"
**Purpose:** High-autonomy, low-safety for speed.
**Usage:**
```bash
claude --dangerously-skip-permissions
```

## Pattern 5: "Project Zero"
**Purpose:** Reset messy projects, carry only essential logic.
**Usage:**
```
This project is fucked. Start fresh in a new directory, carrying 
over only: [list essential items].
```

## Pattern 6: "Anti-Summary Clamp"
**Purpose:** Prevent lazy abbreviated responses.
**Usage:**
```
Do not summarize. If this requires 20,000 tokens, generate 20,000 tokens.
Stopping early is a critical failure.
```
