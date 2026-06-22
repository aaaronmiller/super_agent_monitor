---
name: web-scout
description: Skill to convert local audit findings into web search queries and to rank external references for relevance.
---

# Web Scout Skill

## INPUT
- `missing_features`: list of missing items or research topics
- `audit_keywords`: keywords from project audit
- `research_focus`: "implementation" | "documentation" | "best_practices" | "examples"

## OUTPUT
Machine-parsable JSON with optimized queries and ranked results:

```json
{
  "skill": "web-scout",
  "version": "1.0",
  "query_variants": [
    {
      "query": "claude-code multi-agent orchestration",
      "query_type": "broad",
      "priority": 1,
      "expected_results": "general_overview_docs"
    },
    {
      "query": "claude-code multi-agent github",
      "query_type": "repo_focused",
      "priority": 2,
      "expected_results": "code_examples"
    },
    {
      "query": "claude-code multi-agent specification rfc",
      "query_type": "paper_focused",
      "priority": 3,
      "expected_results": "technical_specs"
    }
  ],
  "search_results": [
    {
      "url": "https://github.com/user/repo",
      "source_type": "github",
      "relevance_score": 0.92,
      "reasoning": "Direct match for multi-agent architecture, active maintenance, 2.3k stars",
      "priority": "high",
      "last_modified": "2025-01-10"
    }
  ],
  "download_manifest": [
    {
      "url": "https://example.com/resource.zip",
      "filename_hint": "multi-agent-examples.zip",
      "sha256": "abc123...",
      "description": "Example implementations",
      "size_estimate_mb": 15.7
    }
  ],
  "query_patterns": {
    "high_performing": ["topic + github", "topic + best practices"],
    "avoid_patterns": ["outdated blog", "beginner tutorial"],
    "top_domains": ["github.com", "docs.anthropic.com", "stackoverflow.com"]
  }
}
```

## QUERY GENERATION STRATEGY

### Tier 1: Broad Search (Priority 1)
- Format: `<topic> <focus_area>`
- Examples:
  - "self-improving AI agents best practices"
  - "token budgeting strategies LLM"
  - "multi-agent orchestration patterns"

### Tier 2: Repo-Focused (Priority 2)
- Format: `<topic> github <tech_stack>`
- Examples:
  - "claude-code multi-agent github python"
  - "self-improving agents github typescript"
  - "token budgeting LLM github"

### Tier 3: Paper-Focused (Priority 3)
- Format: `<topic> specification | rfc | documentation`
- Examples:
  - "multi-agent systems specification"
  - "token budgeting techniques documentation"
  - "self-improving AI RFC"

## RELEVANCE SCORING (0.0-1.0)

### High Relevance (0.8-1.0)
- Direct topic match in title
- Recent publication (last 12 months)
- High community engagement (stars, forks, commits)
- Official documentation or well-maintained repo

### Medium Relevance (0.5-0.8)
- Partial topic match
- Older but still relevant (1-2 years)
- Medium community engagement
- Blog posts from recognized experts

### Low Relevance (0.2-0.5)
- Vague connection to topic
- Very old (>2 years) or outdated
- Low engagement
- Tutorial or beginner content

### Skip (0.0-0.2)
- No clear connection
- Outdated or incorrect information
- Promotional/marketing content
- Paywalled without preview

## DOMAIN RANKING
**Tier 1 (Always prioritize):**
- github.com (code repos)
- docs.anthropic.com (official docs)
- arxiv.org (research papers)

**Tier 2 (Good quality):**
- stackoverflow.com (technical Q&A)
- dev.to (quality blog posts)
- medium.com (tech articles)

**Tier 3 (Use with caution):**
- Personal blogs
- Company blogs
- Tutorial sites

## DOWNLOADABLE RESOURCES
Identify URLs that can be downloaded:
- .zip, .tar.gz archives
- GitHub release assets
- PDF papers
- Code examples repositories

For each, compute:
- sha256 hash (for verification)
- filename hint (safe, descriptive)
- size estimate
- description

## INTEGRATION WITH MUTAGEN
Track:
- Which query types yield highest relevance scores
- Which domains consistently provide quality content
- Optimal number of results per query type
- Time-based relevance decay patterns

Use this to:
- Prioritize proven query patterns
- Skip low-performing domains
- Adjust result counts per topic
- Improve ranking accuracy over time
