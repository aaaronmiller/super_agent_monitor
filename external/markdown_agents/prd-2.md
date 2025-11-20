# Product Requirements Document: Markdown Agent Auditor
## Autonomous Multi-Agent Document Analysis System

**Version:** 2.0
**Date:** 2025-11-19
**Status:** Implementation Ready
**Classification:** Production

---

## 1. Executive Summary

The Markdown Agent Auditor is a headless Claude Code orchestration system that autonomously analyzes folders containing markdown files, identifies PRD (Product Requirements Document) files, discovers related files, rates document quality, and compares projects against existing GitHub repositories to determine uniqueness and improvement opportunities.

### Core Value Propositions

1. **Autonomous Document Discovery**: Automatically finds PRDs and related project files
2. **Intelligent Tagging**: Uses content analysis to associate files with projects even without explicit mentions
3. **Quality Assessment**: Rates PRDs and provides actionable improvement suggestions
4. **Market Research**: Searches GitHub for similar projects and provides comparison analysis
5. **Iterative Analysis**: Two-pass system ensures comprehensive file association

---

## 2. System Architecture

### High-Level Workflow

```
┌─────────────────────────────────────────────────────────────┐
│         ORCHESTRATOR (CLAUDE.md in root .claude)            │
│   Coordinates all agents, manages workflow state            │
└────────────┬────────────────────────────────────────────────┘
             │
     ┌───────┴────────┬──────────────┬──────────────┐
     ↓                ↓              ↓              ↓
┌─────────┐    ┌──────────┐   ┌──────────┐   ┌──────────┐
│ PRD     │    │ File     │   │ Project  │   │ GitHub   │
│ Finder  │    │ Analyzer │   │ Tagger   │   │ Searcher │
└─────────┘    └──────────┘   └──────────┘   └──────────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                    ↓
          ┌─────────────────┐
          │   Scratchpad    │
          │  (analysis.md)  │
          └─────────────────┘
                    ↓
          ┌─────────────────┐
          │  Final Report   │
          │ (report.md)     │
          └─────────────────┘
```

### Two-Pass Analysis Strategy

**Pass 1: Project Identification**
1. Prioritize files with "PRD" in name/content
2. Analyze each file, creating summaries in scratchpad
3. Extract project names and key features
4. Build project registry

**Pass 2: File Association**
1. Re-scan all files with project registry in context
2. Tag files with relevant project hashtags (#project-name)
3. Associate files even without explicit project mentions
4. Update scratchpad with associations

---

## 3. Component Architecture

### 3.1 Directory Structure

```
markdown_agents/
├── orchestrator/                  # Main orchestration plugin
│   └── .claude/
│       ├── CLAUDE.md             # Orchestrator system prompt
│       ├── settings.json         # Model config
│       ├── agents/               # Subagent definitions
│       │   ├── prd-finder.md
│       │   ├── file-analyzer.md
│       │   ├── project-tagger.md
│       │   ├── prd-rater.md
│       │   └── github-searcher.md
│       ├── hooks/
│       │   ├── session-start.py  # Initialize scratchpad
│       │   └── progress-tracker.py
│       └── scripts/
│           ├── scan-files.py     # File discovery
│           ├── extract-tags.py   # Tag parser
│           └── github-api.py     # GitHub search
├── target/                        # User's markdown files (example)
│   ├── prd-example-1.md
│   ├── notes.md
│   └── ...
├── output/                        # Generated analysis (gitignored)
│   ├── scratchpad.md             # Working analysis
│   ├── projects.json             # Project registry
│   └── final-report.md           # Summary report
├── prd.md                         # Original PRD
├── prd-2.md                       # This document
└── README.md                      # User guide
```

### 3.2 Agent Definitions

#### 3.2.1 Orchestrator
- **Role**: Master coordinator
- **Responsibilities**:
  - Deploys subagents in correct sequence
  - Maintains project registry
  - Aggregates results
  - Generates final report
- **Model**: claude-sonnet-4
- **Tools**: Read, Write, Bash, Task, TodoWrite

#### 3.2.2 PRD Finder Agent
- **Role**: Document discovery specialist
- **Responsibilities**:
  - Scan target directory for markdown files
  - Prioritize files with "PRD" in name/content
  - Return sorted list for analysis
- **Model**: claude-haiku
- **Tools**: Glob, Grep, Read

#### 3.2.3 File Analyzer Agent
- **Role**: Content analysis specialist
- **Responsibilities**:
  - Read individual markdown files
  - Extract key information (project name, features, purpose)
  - Write concise summaries to scratchpad
  - Identify project associations
- **Model**: claude-sonnet-4
- **Tools**: Read, Write, Edit

#### 3.2.4 Project Tagger Agent
- **Role**: Association specialist
- **Responsibilities**:
  - Maintain project registry
  - Tag files with project hashtags
  - Identify implicit associations
  - Update scratchpad with tags
- **Model**: claude-sonnet-4
- **Tools**: Read, Write, Edit, Grep

#### 3.2.5 PRD Rater Agent
- **Role**: Quality assessment specialist
- **Responsibilities**:
  - Evaluate PRD completeness
  - Rate on 1-10 scale across dimensions
  - Provide specific improvement suggestions
  - Generate improvement checklist
- **Model**: claude-sonnet-4
- **Tools**: Read, Write

#### 3.2.6 GitHub Searcher Agent
- **Role**: Market research specialist
- **Responsibilities**:
  - Search GitHub for similar projects
  - Analyze feature overlap
  - Determine uniqueness
  - Recommend: link to existing OR enhance our approach
- **Model**: claude-sonnet-4
- **Tools**: WebSearch, WebFetch, Read, Write

---

## 4. Functional Requirements

### 4.1 Phase 1: File Discovery & Analysis

**FR-1.1**: Scan target directory recursively for all `.md` files
**FR-1.2**: Prioritize files containing "PRD" or "Product Requirements" in filename or first 500 chars
**FR-1.3**: Create `output/scratchpad.md` with file list
**FR-1.4**: Analyze each file, append summary to scratchpad with format:
```markdown
## File: path/to/file.md
**Project**: [Name if identified, "Unknown" otherwise]
**Type**: [PRD/Documentation/Notes/etc]
**Summary**: 1-3 sentence overview
**Key Features**: Bullet list
**Tags**: [Extracted hashtags]
---
```

**FR-1.5**: Build `output/projects.json`:
```json
{
  "projects": [
    {
      "name": "Project Name",
      "prd_file": "path/to/prd.md",
      "related_files": [],
      "tags": ["#project-name"],
      "status": "identified"
    }
  ]
}
```

### 4.2 Phase 2: Project Association

**FR-2.1**: Load `projects.json` into context
**FR-2.2**: Re-scan all files with project registry
**FR-2.3**: For each file, determine associations based on:
- Mentions of project names
- Shared technical concepts
- Similar feature descriptions
- Related problem domains

**FR-2.4**: Update scratchpad summaries with `**Associated Projects**: #tag1 #tag2`
**FR-2.5**: Update `projects.json` with `related_files` arrays

### 4.3 Phase 3: PRD Rating

**FR-3.1**: For each PRD file, evaluate on:
- Completeness (1-10): All sections present?
- Clarity (1-10): Unambiguous requirements?
- Technical Detail (1-10): Sufficient for implementation?
- User Focus (1-10): Clear value propositions?
- Feasibility (1-10): Realistic scope?

**FR-3.2**: Generate improvement suggestions:
- Missing sections
- Vague requirements needing clarification
- Technical gaps
- Recommended additions

**FR-3.3**: Append to scratchpad:
```markdown
### PRD Rating: path/to/prd.md
**Overall Score**: X/10
**Completeness**: X/10 - [Comments]
**Clarity**: X/10 - [Comments]
...
**Improvement Suggestions**:
1. [Specific actionable item]
2. ...
```

### 4.4 Phase 4: GitHub Comparison

**FR-4.1**: For each project, search GitHub for similar functionality
**FR-4.2**: Query construction: Use project name + key features
**FR-4.3**: Analyze top 5 results for:
- Feature overlap (%)
- Unique features in our PRD
- Unique features in existing projects
- Code quality indicators (stars, activity, docs)

**FR-4.4**: Generate recommendation:
- **Link Only**: If existing project is superior in every way (>95% overlap, better docs, active)
- **Enhance Ours**: If we have unique features (>20% unique) or novel approach
- **Build New**: If no similar project found

**FR-4.5**: Append to scratchpad:
```markdown
### GitHub Comparison: Project Name
**Similar Projects Found**: X
**Top Match**: [repo URL]
- Feature Overlap: X%
- Their Unique Features: [list]
- Our Unique Features: [list]
- **Recommendation**: [Link/Enhance/Build]
**Rationale**: [Explanation]
```

### 4.5 Phase 5: Final Report

**FR-5.1**: Generate `output/final-report.md` with:
- Executive summary
- Projects discovered (count)
- PRD ratings table
- Top-rated PRDs
- Bottom-rated PRDs needing work
- GitHub comparison summary
- Next steps recommendations

**FR-5.2**: Format for easy consumption:
```markdown
# Markdown Audit Report
**Date**: YYYY-MM-DD
**Files Analyzed**: X
**Projects Identified**: X

## PRD Quality Overview
| Project | File | Overall | Completeness | Clarity | Technical | User | Feasibility |
|---------|------|---------|--------------|---------|-----------|------|-------------|
| ...     | ...  | X/10    | X/10         | X/10    | X/10      | X/10 | X/10        |

## Top 3 PRDs
...

## PRDs Needing Improvement
...

## GitHub Comparison Summary
...

## Recommended Next Steps
...
```

---

## 5. Non-Functional Requirements

**NFR-1**: System must handle 100+ markdown files without manual intervention
**NFR-2**: Progress tracking via hooks (console output or log file)
**NFR-3**: Graceful error handling (skip unparseable files, log errors)
**NFR-4**: Idempotent operation (re-running produces same results)
**NFR-5**: Output files use consistent markdown formatting
**NFR-6**: No external dependencies beyond Claude Code and Python stdlib
**NFR-7**: Production-ready: No placeholders, no TODOs in code

---

## 6. Implementation Specifications

### 6.1 Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Orchestration | Claude Code CLAUDE.md | Native multi-agent support |
| Agents | Markdown prompts | Claude Code subagent format |
| Hooks | Python 3.8+ | Claude Code hook system |
| Scripts | Python 3.8+ stdlib only | No external deps |
| State | JSON + Markdown | Human-readable, versionable |

### 6.2 File Formats

#### projects.json Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "scan_date": "string (ISO 8601)",
    "target_directory": "string",
    "projects": [
      {
        "id": "string (slug)",
        "name": "string",
        "prd_file": "string (path)",
        "related_files": ["string (paths)"],
        "tags": ["string (#project-name)"],
        "status": "enum (identified/analyzed/rated/compared)",
        "rating": {
          "overall": "number (1-10)",
          "completeness": "number",
          "clarity": "number",
          "technical": "number",
          "user_focus": "number",
          "feasibility": "number"
        },
        "github_comparison": {
          "top_match": "string (URL)",
          "overlap_pct": "number",
          "recommendation": "enum (link/enhance/build)"
        }
      }
    ]
  }
}
```

### 6.3 Scratchpad Format

```markdown
# Markdown Audit Scratchpad
**Scan Date**: YYYY-MM-DD HH:MM:SS
**Target Directory**: /path/to/target
**Status**: [In Progress/Complete]

---

## Phase 1: File Discovery

### Files Found: X

## Phase 2: File Analysis

## File: path/to/file1.md
**Project**: Project Name
**Type**: PRD
**Summary**: Brief overview
**Key Features**:
- Feature 1
- Feature 2
**Tags**: #project-name
**Associated Projects**: #related-project
---

[... more files ...]

## Phase 3: PRD Ratings

### PRD Rating: path/to/prd.md
[Rating details]

## Phase 4: GitHub Comparisons

### GitHub Comparison: Project Name
[Comparison details]

---

## Summary
[Quick stats]
```

---

## 7. Usage Instructions

### 7.1 Setup

1. Clone repository
2. Place target markdown files in `target/` directory (or specify custom path)
3. Run orchestrator: `claude --config=orchestrator/.claude --prompt="Analyze all markdown files in target/ directory"`

### 7.2 Configuration

Edit `orchestrator/.claude/settings.json` to adjust:
- Model selection (default: claude-sonnet-4)
- Temperature
- Thinking budget
- Target directory path

### 7.3 Output

Check `output/` directory for:
- `scratchpad.md`: Full working analysis
- `projects.json`: Structured project data
- `final-report.md`: Executive summary

---

## 8. Future Enhancements

**Not in MVP:**
- Web UI for file selection (Phase 2, integrate with Super Agent Monitor)
- Real-time progress meter (Phase 2)
- Multiple target directories (Phase 2)
- Custom rating criteria (Phase 2)
- Export formats (PDF, HTML) (Phase 3)

**Focus**: Build production-ready orchestrator + agents, defer UI to integration phase

---

## 9. Success Criteria

- ✅ Analyzes 100+ markdown files autonomously
- ✅ Correctly identifies 90%+ of PRD files
- ✅ Associates related files with 80%+ accuracy
- ✅ Generates actionable PRD improvement suggestions
- ✅ Provides GitHub comparison for all projects
- ✅ Produces human-readable final report
- ✅ Zero manual intervention required after launch
- ✅ No placeholders or incomplete code
- ✅ Production-ready for immediate use

---

## 10. Terminology Clarification

**"Plugin" in Claude Code context**: A complete `.claude/` folder containing:
- `CLAUDE.md` (system prompt)
- `settings.json` (configuration)
- `agents/` (subagent definitions)
- `skills/` (domain knowledge packages)
- `hooks/` (event-driven scripts)
- `scripts/` (utility functions)

This project delivers one plugin: **Markdown Agent Auditor** in `orchestrator/.claude/`

---

**End of PRD v2.0**
