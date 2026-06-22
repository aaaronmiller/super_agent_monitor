# Optimal Agentic Template Specification

## Purpose
Define a unified, context-efficient agent template format that balances comprehensive capability definition with minimal context overhead.

---

## Current Template Formats Found

### Format 1: YAML Frontmatter + Markdown Body (Most Common)
**Used in**: `components/agents/*.md`, PRD examples

```markdown
---
name: researcher-primary
displayName: Primary Research Agent
description: Lead researcher coordinating information gathering
category: agent
tags: [research, coordination, autonomous]
dependencies: []
incompatibilities: [researcher-solo]
model: claude-sonnet-4
tools: [Read, Write, Bash, WebSearch]
version: 1.0.0
---

# Primary Research Agent

You are the lead research coordinator responsible for:
1. **Task Decomposition**: Break complex research questions into subtasks
2. **Delegation**: Assign subtasks to specialist agents
...
```

**Pros**: Human-readable, parseable, standard markdown
**Cons**: Verbose frontmatter can bloat context

---

### Format 2: Pure YAML (Agent Toolkit)
**Used in**: `agent-toolkit/templates/`

```yaml
name: code-analyzer
model: sonnet
thinking_budget: 8000
tools: [filesystem, github]
skills: [code-review]
complexity: high
```

**Pros**: Minimal, machine-parseable
**Cons**: No room for behavioral guidance

---

### Format 3: CIO Pattern (Context-Injected Orchestration)
**Used in**: `agent_definition.md` examples

```
<swarm-name>/
├── CLAUDE.md              # Identity + orchestration logic
└── .claude/
    ├── settings.json      # Capabilities
    ├── agents/            # Sub-agent definitions
    └── plugins/           # Strategy configs
```

**Identity** (`CLAUDE.md`):
```markdown
# [Swarm Name] - Orchestrator

You are the **[Role]**, managing [responsibilities].

## Agent Toolkit Integration
## Model Sizing Strategy
## Workflow
## Quality Standards
```

**Capabilities** (`settings.json`):
```json
{
  "model": "claude-sonnet-4-20250514",
  "thinking_budget": 12000,
  "agents": {
    "code-analyzer": { "complexity": "high" },
    "refactoring-executor": { "complexity": "low" }
  }
}
```

---

## Recommended Optimal Template

### Design Principles

1. **Context Efficiency First**: ~500-1500 tokens per agent definition
2. **Progressive Disclosure**: Load detailed skills on-demand, not upfront
3. **Machine Parseable**: YAML frontmatter for tooling
4. **Human Readable**: Clear markdown body for agent behavior
5. **Dynamic Assembly Support**: Reference skills/tools by name, inject at runtime

---

### Optimal Agent Template Format

```markdown
---
# METADATA (Required)
name: agent-name             # Unique identifier, kebab-case
version: 1.0.0               # Semantic version

# CLASSIFICATION (Required)
category: agent              # agent|skill|hook|script|orchestrator
model: sonnet                # haiku|sonnet|opus (for model sizing)
complexity: medium           # low|medium|high (thinking budget hint)

# CAPABILITIES (Optional - loaded dynamically)
tools: [Read, Write, Bash]   # Tool permissions
skills: [code-review]        # Skill packages (loaded on-demand)
dependencies: []             # Required components
incompatibilities: []        # Conflicting components

# UI DISPLAY (Optional)
displayName: Code Analyzer
description: Analyzes code structure and identifies improvement opportunities
tags: [analysis, code-quality]
icon: 🔍                     # Emoji icon for UI
---

# Agent Name

Brief identity statement (1-2 sentences).

## Mission
Core responsibilities (3-5 bullet points max).

## Workflow
Step-by-step execution pattern (numbered list).

## Constraints
Hard limits and boundaries (bullet list).

## Output Format
Expected output structure.
```

---

### Token Budget Guidelines

| Section | Target Tokens | Purpose |
|:--------|:--------------|:--------|
| YAML Frontmatter | 50-100 | Machine parsing |
| Identity Statement | 20-50 | Quick context |
| Mission | 50-100 | Core purpose |
| Workflow | 100-200 | Execution pattern |
| Constraints | 50-100 | Boundaries |
| Output Format | 50-100 | Structure |
| **Total** | **320-650** | Context-efficient |

---

### Model Sizing Matrix

| Complexity | Model | Thinking Budget | Use Cases |
|:-----------|:------|:----------------|:----------|
| low | haiku | 2000-5000 | File ops, scanning, formatting |
| medium | sonnet | 8000-12000 | Analysis, refactoring, testing |
| high | opus | 15000-20000 | Architecture, research, synthesis |

---

### Skill Reference Pattern

Instead of embedding full skill content, reference by path:

```markdown
## Skills Integration

Load when needed (progressive disclosure):
- `cat skills/code-review/SKILL.md` - Code quality patterns
- `cat skills/testing-strategies/SKILL.md` - Test generation

DO NOT load all skills at session start.
```

---

### Tool Declaration Pattern

Minimal tool list, expand at runtime:

```yaml
tools: [Read, Write, Bash]  # Core permissions
```

Rather than:
```yaml
tools:
  - name: filesystem
    type: script
    path: scripts/filesystem.py
    permissions: [read, write, list]
  # ... verbose
```

---

## Example: Optimized Agent Template

```markdown
---
name: code-analyzer
version: 1.0.0
category: agent
model: sonnet
complexity: medium
tools: [Read, Bash, Grep]
skills: [code-review]
tags: [analysis, quality]
displayName: Code Analyzer
description: Analyzes code structure and complexity
icon: 🔍
---

# Code Analyzer

You analyze code structure, identify patterns, and assess quality.

## Mission
- Scan codebase for complexity hotspots
- Identify code smells and anti-patterns
- Generate actionable improvement recommendations
- Track quality metrics over time

## Workflow
1. Receive target files/directories
2. Load code-review skill: `cat skills/code-review/SKILL.md`
3. Analyze structure using AST/grep patterns
4. Score complexity (cyclomatic, lines, coupling)
5. Generate markdown report

## Constraints
- NEVER modify source files
- Report only verified findings
- Include line numbers for all issues

## Output Format
```markdown
## Code Analysis Report
### Summary: [X files, Y issues, Z score]
### Findings: [severity, location, description]
### Recommendations: [priority, action, impact]
```
```

**Token count**: ~450 tokens (efficient)

---

## Migration Checklist

1. [ ] Audit existing agents in `components/agents/`
2. [ ] Identify agents exceeding 1500 tokens
3. [ ] Extract embedded skill content to `skills/` directories
4. [ ] Standardize frontmatter fields
5. [ ] Add `complexity` and `model` fields
6. [ ] Validate against schema
7. [ ] Test with agent assembly script

---

## Schema Validation

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "version", "category", "model", "complexity"],
  "properties": {
    "name": { "type": "string", "pattern": "^[a-z][a-z0-9-]*$" },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "category": { "enum": ["agent", "skill", "hook", "script", "orchestrator"] },
    "model": { "enum": ["haiku", "sonnet", "opus"] },
    "complexity": { "enum": ["low", "medium", "high"] },
    "tools": { "type": "array", "items": { "type": "string" } },
    "skills": { "type": "array", "items": { "type": "string" } },
    "dependencies": { "type": "array", "items": { "type": "string" } },
    "incompatibilities": { "type": "array", "items": { "type": "string" } },
    "displayName": { "type": "string" },
    "description": { "type": "string", "maxLength": 200 },
    "tags": { "type": "array", "items": { "type": "string" } },
    "icon": { "type": "string", "maxLength": 2 }
  }
}
```
