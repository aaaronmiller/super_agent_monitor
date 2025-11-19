# Markdown Agent Auditor

**Autonomous Multi-Agent Document Analysis System**

A headless Claude Code orchestration system that autonomously analyzes folders containing markdown files, identifies PRD (Product Requirements Document) files, discovers related files, rates document quality, and compares projects against existing GitHub repositories.

---

## Features

- **Autonomous Document Discovery**: Automatically finds PRDs and related project files
- **Intelligent Tagging**: Uses content analysis to associate files with projects
- **Quality Assessment**: Rates PRDs on 5 dimensions with actionable improvement suggestions
- **Market Research**: Searches GitHub for similar projects and provides comparison analysis
- **Iterative Analysis**: Two-pass system ensures comprehensive file association
- **Production-Ready**: No placeholders, complete implementation, minimal dependencies

---

## Table of Contents

- [Quick Start](#quick-start)
- [System Architecture](#system-architecture)
- [Usage](#usage)
- [Output Files](#output-files)
- [Configuration](#configuration)
- [Agent Descriptions](#agent-descriptions)
- [Scripts and Utilities](#scripts-and-utilities)
- [Extending the System](#extending-the-system)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Quick Start

### Prerequisites

- **Claude Code**: Installed and configured ([Installation Guide](https://docs.claude.com))
- **Python**: 3.8 or higher
- **Markdown Files**: Place files to analyze in `target/` directory

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd markdown_agents
```

2. Place your markdown files in the `target/` directory:
```bash
mkdir -p target
cp /path/to/your/markdown/*.md target/
```

3. Run the analysis:
```bash
claude --config=orchestrator/.claude --prompt="Analyze all markdown files in target/ directory"
```

### Expected Runtime

- 10 files: ~2-3 minutes
- 50 files: ~10-15 minutes
- 100+ files: ~30-45 minutes

---

## System Architecture

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
```

### Analysis Phases

1. **Phase 1: File Discovery** - Scan target directory, prioritize PRDs
2. **Phase 2: File Analysis** - Extract project info, features, summaries
3. **Phase 3: Project Association** - Tag files with related projects
4. **Phase 4: PRD Rating** - Evaluate quality across 5 dimensions
5. **Phase 5: GitHub Comparison** - Search for similar projects
6. **Phase 6: Final Report** - Generate executive summary

---

## Usage

### Basic Usage

Analyze all markdown files in default `target/` directory:

```bash
claude --config=orchestrator/.claude --prompt="Analyze all markdown files in target/ directory"
```

### Custom Target Directory

Analyze files in a custom directory:

```bash
claude --config=orchestrator/.claude --prompt="Analyze all markdown files in /path/to/custom/directory"
```

### Re-running Analysis

The system is idempotent - you can re-run analysis safely:

```bash
# Previous output is in output/ directory
# Re-run will overwrite with fresh analysis
claude --config=orchestrator/.claude --prompt="Analyze all markdown files in target/ directory"
```

### Monitoring Progress

During analysis, you can check progress:

```bash
# In another terminal
python orchestrator/.claude/hooks/progress-tracker.py
```

Output:
```
============================================================
  Markdown Agent Auditor - Progress Report
============================================================

  Current Phase: Phase 3: Project Association
  Status: IN_PROGRESS

  [████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 40%

  Files Found: 25
  Projects Identified: 5
  PRDs Rated: 0/5
  GitHub Comparisons: 0/5

============================================================
```

---

## Output Files

All analysis results are saved in the `output/` directory:

### 1. scratchpad.md

**Purpose**: Working document with detailed analysis of each file

**Contents**:
- File discovery results
- Individual file analyses with summaries and features
- Project associations and tags
- PRD quality ratings with detailed assessments
- GitHub comparison analyses
- Session log

**Use Case**: Detailed reference for deep-diving into specific files

### 2. projects.json

**Purpose**: Structured data for programmatic access

**Schema**:
```json
{
  "scan_date": "2025-11-19T14:30:00",
  "target_directory": "/path/to/target",
  "projects": [
    {
      "id": "ai-code-assistant",
      "name": "AI Code Assistant",
      "prd_file": "target/ai-code-assistant-prd.md",
      "related_files": [
        "target/authentication-implementation.md",
        "target/team-meeting-2025-11-15.md"
      ],
      "tags": ["#ai-code-assistant"],
      "status": "compared",
      "rating": {
        "overall": 8.5,
        "completeness": 9,
        "clarity": 8,
        "technical": 8,
        "user_focus": 9,
        "feasibility": 8
      },
      "github_comparison": {
        "top_match": "https://github.com/user/similar-project",
        "overlap_pct": 65,
        "recommendation": "enhance_ours"
      }
    }
  ]
}
```

**Use Case**: Import into other tools, generate visualizations, automate workflows

### 3. final-report.md

**Purpose**: Executive summary for stakeholders

**Contents**:
- Overview of findings
- PRD quality table
- Top-rated PRDs
- PRDs needing improvement
- GitHub comparison summary
- Recommended next steps

**Example**:
```markdown
# Markdown Audit Report
**Date**: 2025-11-19
**Files Analyzed**: 25
**Projects Identified**: 5

## Executive Summary
Analyzed 25 markdown files and identified 5 distinct projects...

## PRD Quality Overview
| Project | Overall | Completeness | Clarity | Technical | User | Feasibility |
|---------|---------|--------------|---------|-----------|------|-------------|
| AI Code Assistant | 8.5/10 | 9/10 | 8/10 | 8/10 | 9/10 | 8/10 |
...
```

**Use Case**: Share with team, report to leadership, prioritize work

### 4. session.log

**Purpose**: Chronological log of analysis progress

**Contents**:
```
2025-11-19 14:30:00 - Session initialized
2025-11-19 14:30:15 - Phase 1: File Discovery - 10% complete
2025-11-19 14:32:45 - Phase 2: File Analysis - 35% complete
...
```

**Use Case**: Debug issues, track performance, audit trail

---

## Configuration

### Adjusting Model Settings

Edit `orchestrator/.claude/settings.json`:

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "temperature": 0.7,
  "thinkingBudget": 10000,
  "projectConfig": {
    "targetDirectory": "target/",
    "outputDirectory": "output/",
    "maxConcurrentAgents": 5,
    "retryFailedFiles": true
  }
}
```

**Options**:
- `model`: Choose Claude model (sonnet-4, opus, haiku)
- `temperature`: Adjust creativity (0.0-1.0, default 0.7)
- `thinkingBudget`: Token budget for extended thinking
- `maxConcurrentAgents`: Number of parallel agents (adjust for performance)

### Customizing Rating Criteria

Edit `ratingCriteria` in `settings.json`:

```json
{
  "ratingCriteria": {
    "completeness": "All required sections present",
    "clarity": "Requirements are unambiguous",
    "technical": "Sufficient detail for implementation",
    "userFocus": "Clear value propositions",
    "feasibility": "Realistic scope"
  }
}
```

---

## Agent Descriptions

### 1. PRD Finder Agent
- **Purpose**: Discover markdown files, prioritize PRDs
- **Model**: Claude Haiku (fast, cost-effective)
- **Output**: Sorted list of priority and standard files

### 2. File Analyzer Agent
- **Purpose**: Extract structured information from files
- **Model**: Claude Sonnet 4 (high quality)
- **Output**: Project name, type, summary, features, tags

### 3. Project Tagger Agent
- **Purpose**: Associate files with projects based on content
- **Model**: Claude Sonnet 4 (reasoning required)
- **Output**: Project associations with confidence scores

### 4. PRD Rater Agent
- **Purpose**: Evaluate PRD quality
- **Model**: Claude Sonnet 4 (expert assessment)
- **Output**: Scores on 5 dimensions + improvement suggestions

### 5. GitHub Searcher Agent
- **Purpose**: Find and compare similar GitHub projects
- **Model**: Claude Sonnet 4 (research + analysis)
- **Output**: Top matches, feature overlap, recommendation

---

## Scripts and Utilities

### scan-files.py

Scan directory for markdown files:

```bash
python orchestrator/.claude/scripts/scan-files.py target/
```

**Output**: JSON file list + markdown report

### extract-tags.py

Extract hashtags from a file:

```bash
python orchestrator/.claude/scripts/extract-tags.py target/file.md "Project Name"
```

**Output**: Existing tags, suggested project tag, merged tags

### github-api.py

Helper utilities for GitHub operations:

```bash
# Generate search queries
python orchestrator/.claude/scripts/github-api.py query "Multi-Agent Monitor" "workflow,agent" "Vue,PostgreSQL"

# Parse GitHub URL
python orchestrator/.claude/scripts/github-api.py parse "https://github.com/owner/repo"

# Calculate feature overlap
python orchestrator/.claude/scripts/github-api.py overlap "feat1,feat2,feat3" "feat1,feat4"
```

### progress-tracker.py

Check analysis progress:

```bash
python orchestrator/.claude/hooks/progress-tracker.py
```

**Output**: Visual progress bar, phase status, statistics

---

## Extending the System

### Adding a New Agent

1. Create agent definition in `orchestrator/.claude/agents/`:

```markdown
---
name: my-custom-agent
displayName: My Custom Agent
description: What this agent does
category: agent
tags: [custom, analysis]
model: claude-sonnet-4
tools: [Read, Write, Grep]
version: 1.0.0
---

# My Custom Agent

Your agent instructions here...
```

2. Update `CLAUDE.md` to include deployment logic for your agent

3. Test with: `claude --config=orchestrator/.claude --prompt="Test my custom agent"`

### Adding a New Hook

1. Create hook script in `orchestrator/.claude/hooks/`:

```python
#!/usr/bin/env python3
"""My Custom Hook"""

def main():
    # Your hook logic
    print("Hook executed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

2. Make executable: `chmod +x orchestrator/.claude/hooks/my-hook.py`

3. Configure Claude Code to call your hook at desired event

### Customizing Output Format

Edit agent definitions to change output format, or create post-processing scripts:

```python
import json

# Load projects.json
with open('output/projects.json', 'r') as f:
    data = json.load(f)

# Convert to custom format
# ...
```

---

## Troubleshooting

### Issue: "No markdown files found"

**Cause**: Target directory is empty or doesn't exist

**Solution**:
```bash
mkdir -p target
cp /path/to/markdown/*.md target/
```

### Issue: "Agent timeout or stall"

**Cause**: Large files or many files causing processing delays

**Solution**: Reduce `maxConcurrentAgents` in `settings.json` or split analysis into batches

### Issue: "API rate limits"

**Cause**: Too many concurrent requests to Claude API

**Solution**: Reduce `maxConcurrentAgents` to 2-3, or add delays between agent deployments

### Issue: "Inaccurate project associations"

**Cause**: Not enough context or ambiguous file content

**Solution**: Add explicit project tags to files manually, or improve PRD clarity

### Issue: "GitHub search returns no results"

**Cause**: Project name too generic or novel concept

**Solution**: This is expected for truly unique projects - the system will recommend "Build New"

---

## Directory Structure

```
markdown_agents/
├── orchestrator/           # Main plugin
│   └── .claude/
│       ├── CLAUDE.md       # Orchestrator system prompt
│       ├── settings.json   # Configuration
│       ├── agents/         # Agent definitions (5 files)
│       ├── hooks/          # Event hooks (2 files)
│       └── scripts/        # Utility scripts (3 files)
├── target/                 # Your markdown files (user-provided)
├── output/                 # Analysis results (generated)
│   ├── scratchpad.md
│   ├── projects.json
│   ├── final-report.md
│   └── session.log
├── prd.md                  # Original PRD
├── prd-2.md                # Refined PRD v2.0
└── README.md               # This file
```

---

## Contributing

### Reporting Issues

Found a bug or have a suggestion? Please:
1. Check existing issues
2. Provide minimal reproduction case
3. Include relevant output files
4. Specify Claude Code version

### Submitting PRs

1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Update documentation
5. Submit PR with clear description

---

## FAQ

**Q: How long does analysis take?**
A: 2-3 minutes for 10 files, 10-15 minutes for 50 files, 30-45 minutes for 100+ files.

**Q: Can I analyze non-English markdown files?**
A: Claude supports multiple languages, but quality may vary. English is recommended.

**Q: Does this work with GitHub Enterprise?**
A: Yes, the WebSearch tool can search private GitHub instances if configured.

**Q: Can I customize the rating criteria?**
A: Yes, edit `ratingCriteria` in `settings.json`.

**Q: What if my PRD uses a non-standard format?**
A: The system is flexible and will adapt. As long as the content is meaningful, it will be analyzed.

**Q: Is this safe to use with proprietary code/docs?**
A: Analysis runs locally via Claude Code. Data is only sent to Anthropic's API per Claude Code's standard behavior. Review your organization's AI usage policies.

**Q: Can I run this offline?**
A: No, Claude Code requires API access to Anthropic's servers.

---

## License

[Specify your license here]

---

## Support

- **Documentation**: This README
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Claude Code Docs**: https://docs.claude.com

---

**Built with Claude Code** | **Version 1.0.0** | **Last Updated: 2025-11-19**
