# Document Integration Analysis Protocol

**Version:** 1.0.0
**Purpose:** Universal template for extracting concepts from source documents and integrating them into target projects.

---

## 1. Overview

This protocol provides a systematic approach to:
1. Inventory source documents
2. Classify content by integration status
3. Extract actionable patterns
4. Track integration progress

---

## 2. Classification Schema

The simple "Add / Don't Add / Add Later" trichotomy is **insufficient** for complex projects. 

### 2.1 Expanded Classification (Recommended)

| Code | Category | Description | Action Required |
|:-----|:---------|:------------|:----------------|
| **I** | **INTEGRATED** | Copied verbatim or adapted | None (complete) |
| **E** | **EXTRACTED** | Pattern/concept documented, not copied | Track in insights doc |
| **D** | **DEFERRED-BLOCKED** | Requires missing infrastructure | Create prerequisite ticket |
| **P** | **DEFERRED-PLANNED** | Scheduled for future phase | Add to roadmap |
| **R** | **REJECTED-REDUNDANT** | Duplicate of existing content | Document in audit |
| **O** | **REJECTED-OBSOLETE** | Outdated or superseded | Archive reference |
| **X** | **REJECTED-IRRELEVANT** | Not applicable to target | Explain in audit |
| **C** | **CONFIG/EXAMPLE** | Configuration or example file | Do not integrate |
| **?** | **UNPROCESSED** | Not yet analyzed | Queue for analysis |

### 2.2 Decision Tree

```
START: Examine source element
    │
    ├─► Is it configuration, example data, or test fixture?
    │   └─► YES → [C] CONFIG/EXAMPLE
    │
    ├─► Does identical content already exist in target?
    │   └─► YES → [R] REJECTED-REDUNDANT
    │
    ├─► Is it marked legacy/deprecated/obsolete?
    │   └─► YES → [O] REJECTED-OBSOLETE
    │
    ├─► Is it relevant to target project goals?
    │   └─► NO → [X] REJECTED-IRRELEVANT
    │
    ├─► Can it be integrated immediately?
    │   ├─► YES, verbatim copy works → [I] INTEGRATED
    │   └─► YES, but needs adaptation → [E] EXTRACTED
    │
    ├─► Why can't it be integrated now?
    │   ├─► Missing infrastructure → [D] DEFERRED-BLOCKED
    │   └─► Scheduled for later → [P] DEFERRED-PLANNED
    │
    └─► None of the above → [?] UNPROCESSED (needs more analysis)
```

---

## 3. Analysis Protocol (Step-by-Step)

### Phase 1: Inventory

```markdown
## Step 1.1: Generate File List
Command: `find {SOURCE_DIR} -type f \( -name "*.md" -o -name "*.py" ... \) | sort`

## Step 1.2: Count and Categorize
- Total files: ___
- By extension: .md: ___, .py: ___, .json: ___, etc.
- By directory: {subdir1}: ___, {subdir2}: ___, etc.

## Step 1.3: Identify Large Files
Files > 50KB require chunked processing:
| File | Size | Chunks Needed |
|:-----|:-----|:--------------|
| ... | ... | ... |
```

### Large File Chunking Protocol (MANDATORY)

> [!CAUTION]
> Files exceeding 100KB MUST be divided into ≤50KB chunks to prevent context collapse and model crash.

**Chunking Rules:**

| File Size | Action | Chunk Size |
|:----------|:-------|:-----------|
| <50KB | Process whole | N/A |
| 50-100KB | Process carefully | N/A |
| >100KB | **MANDATORY CHUNKING** | ≤50KB each |

**Chunking Procedure:**

```bash
# 1. Identify files >100KB
find {SOURCE_DIR} -type f -size +100k -exec ls -lh {} \;

# 2. Calculate chunks needed
# chunks = ceil(file_size / 50000)

# 3. Process in chunks
head -c 50000 large_file.md > chunk_1.md
tail -c +50001 large_file.md | head -c 50000 > chunk_2.md
# ... continue until complete

# 4. Alternative: Line-based chunking (preferred for markdown)
split -l 800 large_file.md chunk_  # ~800 lines per chunk
```

**Processing Protocol for Chunked Files:**

1. Process Chunk 1 → Extract patterns → Document findings
2. Process Chunk 2 → Extract NEW patterns only → Append to findings
3. Continue until all chunks processed
4. Deduplicate extracted patterns
5. Mark file as fully processed

**Chunk Processing Template:**

```markdown
## File: {filename}
## Chunk: {N} of {total}
## Bytes: {start_byte}-{end_byte}

### Patterns Found in This Chunk:
- Pattern 1: ...
- Pattern 2: ...

### Requires Next Chunk: YES/NO
### Reason: {why more chunks needed or not}
```

### Phase 2: First-Pass Classification

```markdown
## Step 2.1: Quick Scan Each Directory

For each subdirectory, answer:
1. What is the apparent purpose?
2. Does target project have equivalent?
3. Initial classification (bulk assign where possible)

## Step 2.2: Create Classification Table

| Path | Size | Category | Rationale | Prerequisite |
|:-----|:-----|:---------|:----------|:-------------|
| `/source/file1.md` | 5KB | I | Core docs | None |
| `/source/legacy/old.md` | 2KB | O | Deprecated | None |
| `/source/feature/x.py` | 10KB | D | Needs DB | Database setup |
```

### Phase 3: Deep Analysis

```markdown
## Step 3.1: Process Each INTEGRATED/EXTRACTED Item

For each I or E item:
1. Read content (first 800 lines for files)
2. Extract key patterns/concepts
3. Identify target location
4. Note any adaptations needed

## Step 3.2: Document Patterns

Create an insights document:
| Pattern Name | Source File | Description | Target Implementation |
|:-------------|:------------|:------------|:----------------------|
| Hub-Spoke | /docs/arch.md | Central coordinator | mission_launcher.py |
```

### Phase 4: Validate Classification

```markdown
## Step 4.1: Review REJECTED Items

For each R, O, X item:
- Confirm rejection rationale is valid
- Check for hidden value that was missed
- Document rejection reason

## Step 4.2: Review DEFERRED Items

For each D, P item:
- Confirm prerequisite is correctly identified
- Estimate when prerequisite will be ready
- Add to future phase planning
```

### Phase 5: Generate Report

```markdown
## Step 5.1: Summary Statistics

| Category | Count | % of Total |
|:---------|:------|:-----------|
| INTEGRATED | ___ | ___% |
| EXTRACTED | ___ | ___% |
| DEFERRED-BLOCKED | ___ | ___% |
| DEFERRED-PLANNED | ___ | ___% |
| REJECTED-* | ___ | ___% |
| UNPROCESSED | ___ | ___% |

## Step 5.2: Gap Analysis

What's missing that SHOULD have been in source?
What's in source that target already has better versions of?

## Step 5.3: Next Steps

1. Process remaining UNPROCESSED items
2. Build infrastructure for DEFERRED-BLOCKED items
3. Schedule DEFERRED-PLANNED items
```

---

## 4. Templates

### 4.1 Classification Record Template

```yaml
# Use this for each source element

source_path: "/path/to/source/file.md"
source_size: "10KB"
classification: "D"  # I, E, D, P, R, O, X, C, ?
rationale: "Requires skill activation framework"
prerequisite: "Implement skill-loader.py"
target_path: "/path/to/target/location/"  # null if rejected
patterns_extracted:
  - name: "Pattern Name"
    description: "Brief description"
    implementation_notes: "How to implement"
reviewed_by: "agent/human"
reviewed_date: "2025-12-08"
```

### 4.2 Insights Document Template

```markdown
# {Project Name} Integration Insights

## 1. Architectural Patterns

### Pattern: {Name}
- **Source:** {file path}
- **Description:** {what it does}
- **Implementation:** {how to implement}
- **Priority:** HIGH/MEDIUM/LOW

## 2. Code Patterns

### Pattern: {Name}
- **Source:** {file path}
- **Code Example:**
```{language}
// key code snippet
```
- **Adaptation Notes:** {how to adapt for target}

## 3. Configuration Patterns

{Similar structure}

## 4. Rejected Patterns (and why)

| Pattern | Source | Rejection Reason |
|:--------|:-------|:-----------------|
| ... | ... | ... |
```

### 4.3 Audit Report Template

```markdown
# {Source Name} Integration Audit

**Date:** {YYYY-MM-DD}
**Total Elements:** {count}

## Summary

| Category | Count | % |
|:---------|:------|:---|
| INTEGRATED | | |
| EXTRACTED | | |
| DEFERRED-BLOCKED | | |
| DEFERRED-PLANNED | | |
| REJECTED-REDUNDANT | | |
| REJECTED-OBSOLETE | | |
| REJECTED-IRRELEVANT | | |
| CONFIG/EXAMPLE | | |
| UNPROCESSED | | |

## By Directory

### {Directory 1}
{Table of files and classifications}

### {Directory 2}
{Table of files and classifications}

## Blocking Dependencies

| Prerequisite | Blocks | Priority |
|:-------------|:-------|:---------|
| ... | ... | ... |

## Recommendations

1. ...
2. ...
```

---

## 5. Quality Checklist

Before marking integration complete:

- [ ] All source files classified (no UNPROCESSED remaining)
- [ ] All INTEGRATED items verified working in target
- [ ] All EXTRACTED patterns documented with examples
- [ ] All DEFERRED items have clear prerequisites
- [ ] All REJECTED items have documented rationale
- [ ] Insights document captures all valuable patterns
- [ ] Audit report is complete and accurate
- [ ] Gap analysis identifies any missing coverage

---

## 6. Common Pitfalls

| Pitfall | Symptom | Solution |
|:--------|:--------|:---------|
| Over-integration | Copying redundant code | Check for existing equivalents first |
| Under-extraction | Missing valuable patterns | Read files, not just filenames |
| Premature rejection | Dismissing unclear content | Mark as ? and revisit |
| Deferred drift | Items stuck in deferred forever | Set concrete prerequisite milestones |
| Missing context | Patterns extracted without understanding | Read surrounding files for context |

---

## 7. Automation Opportunities

### 7.1 File Classification Script Template

```python
#!/usr/bin/env python3
"""
Automated classification helper.
Suggests classifications based on patterns.
"""

PATTERNS = {
    'CONFIG': [r'settings\.json$', r'\.env\.', r'config\.yaml$'],
    'OBSOLETE': [r'/legacy/', r'/deprecated/', r'/old/'],
    'EXAMPLE': [r'/examples/', r'/target/', r'/fixtures/'],
}

def suggest_classification(path: str) -> str:
    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, path):
                return category
    return '?'  # Needs manual review
```

### 7.2 Progress Tracking

```bash
# Count classifications in audit file
grep -c "| I |" audit.md   # Integrated
grep -c "| D |" audit.md   # Deferred
grep -c "| ? |" audit.md   # Unprocessed
```

---

## 8. Schema Comparison

| Simple Schema | Expanded Schema | Why Expanded is Better |
|:--------------|:----------------|:----------------------|
| Add | INTEGRATED, EXTRACTED | Distinguishes verbatim copy vs pattern extraction |
| Don't Add | REJECTED-* (3 types) | Explains WHY rejected (redundant vs obsolete vs irrelevant) |
| Add Later | DEFERRED-* (2 types) | Distinguishes blocked vs planned deferral |
| (missing) | CONFIG/EXAMPLE | Handles non-integrable content |
| (missing) | UNPROCESSED | Tracks analysis progress |

**Verdict:** The 9-category schema is more robust because:
1. It separates "rejected because bad" from "rejected because duplicate"
2. It distinguishes "can't do now" from "won't do now"
3. It tracks analysis completeness
4. It handles edge cases (config files, examples)
