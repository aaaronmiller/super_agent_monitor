# Agent-to-Agent Communication Patterns

## Overview

The OmniEdge system uses a **swarm orchestration model** where a central `orchestrator` spawns and coordinates specialized subagents. Communication happens through:

1. **Structured file outputs** (JSON, Markdown)
2. **Shared directory conventions**
3. **Explicit budget parameter passing**
4. **Mutagen memory system** for self-improvement

## Agent Hierarchy

```
orchestrator (central coordinator)
    ├── file-auditor (batch processing)
    ├── cluster-analyzer (grouping)
    ├── web-researcher (scouting)
    ├── master-consolidator (merging)
    ├── document-organizer (structuring)
    ├── publication-assessor (quality)
    ├── daily-submission (platform discovery)
    └── promotion-agent (marketing)
```

## Communication Mechanisms

### 1. Orchestrator → Subagents

**Pattern**: Explicit parameter passing via user prompt

**Required Parameters**:
```json
{
  "manager": "omniedge-orchestrator",
  "context_window_tokens": 150000,
  "payload_budget_tokens": 40000,
  "payload_utilization_target": 0.75,
  "model_hint": "sonnet|gpt5-high|local-lfm2",
  "batch_id": "batch_0001",
  "job": "file-audit|cluster-analyze|web-research|consolidate",
  "execution_history": [...], // from mutagen memory
  "prompt_version": "v1.2",
  "optimization_notes": "..."
}
```

**Agent-Specific Parameters**:

**File Auditor**:
- `batch_files`: list of file paths
- `skip_patterns`: patterns to ignore

**Cluster Analyzer**:
- `batch_outputs_dirs`: list of audit directories
- `similarity_threshold`: clustering threshold

**Web Researcher**:
- `research_topics`: list of topics
- `query_types`: search strategy types

**Publication Assessor**:
- `documents_to_assess`: list of document paths
- `assessment_criteria`: quality rubric parameters

### 2. File Auditor → Cluster Analyzer

**Pattern**: File-based handoff via structured audit data

**Input Path**: `batch/<batch_id>/file-audits/`

**Output Files**:

**`index.json`**:
```json
{
  "batch_id": "batch_0001",
  "file_count": 45,
  "total_tokens": 38000,
  "files": [
    {
      "path": "src/App.tsx",
      "hash": "abc123...",
      "size": 2400,
      "tokens": 1200,
      "type": "code"
    }
  ]
}
```

**Individual Audit Files**: `batch/<batch_id>/file-audits/<relative-path>.md`
```markdown
# File Audit: src/App.tsx

## Metadata
- **Path**: ./relative/path/to/file
- **SHA256**: <hash>
- **Size**: <bytes> bytes
- **Type**: [code|doc|config|binary|other]

## Summary
<3-sentence summary>

## Extracted Ideas
- [List of features/concepts]

## Flags
- [ ] is_doc
- [ ] is_src
- [ ] is_config

## Skill Analysis
<JSON from file-summarizer skill>
```

**Consumed By**:
- `cluster-analyzer` - uses audit data for similarity analysis

### 3. Cluster Analyzer → Master Consolidator

**Pattern**: Structured cluster data handoff

**Input Path**: `clusters/cluster_<id>/`

**Output Files**:

**`family_tree.md`**:
```markdown
# Cluster <id>: <descriptive name>

## Lineage
<founder> → <derived> → <variant>

## Members
- fileA.md (founder)
- fileB.md (derived v1)
- fileC.md (derived v2)

## Quality Score
<0-1 confidence>
```

**`members.md`**:
```markdown
# Cluster <id> Members

| File | Hash | Size | Tokens | Date |
|------|------|------|--------|------|
| fileA.md | abc123... | 5.2k | 1200 | 2024-01-15 |
```

**`clusters/index.json`**:
```json
{
  "clustering_timestamp": "2025-11-06T00:00:00Z",
  "clusters_created": 15,
  "total_files_clustered": 45,
  "clusters": [
    {
      "cluster_id": "cluster_001",
      "member_count": 15,
      "confidence": 0.87
    }
  ]
}
```

**Consumed By**:
- `master-consolidator` - for final synthesis

### 4. Web Researcher → Publication Assessor

**Pattern**: Research results in structured JSON

**Output Path**: `research/<batch_id>/`

**Output Files**:

**`search-results.json`**:
```json
{
  "skill": "web-scout",
  "version": "1.0",
  "query_type": "documentation",
  "results": [
    {
      "url": "https://example.com",
      "title": "Page Title",
      "relevance_score": 0.92,
      "content_preview": "...",
      "domain_authority": 85
    }
  ],
  "search_strategy": {
    "queries_used": ["query1", "query2"],
    "total_results": 25
  }
}
```

**Consumed By**:
- `publication-assessor` - for quality assessment
- `master-consolidator` - for synthesis

### 5. Publication Assessor → Daily Submission

**Pattern**: Quality-scored documents

**Output Path**: `assessments/<batch_id>/`

**Output Files**:

**`quality-report.json`**:
```json
{
  "skill": "quality-rubric",
  "version": "1.0",
  "document_id": "doc-001",
  "overall_grade": "B",
  "overall_score": 85,
  "detailed_scores": {
    "originality_novelty": {"score": 21, "max": 25},
    "content_quality": {"score": 23, "max": 25}
  },
  "publication_readiness": {
    "verdict": "publishable_with_revisions",
    "target_grade": "A"
  }
}
```

**`originality-report.json`**:
```json
{
  "skill": "originality-checker",
  "version": "1.0",
  "document_id": "doc-001",
  "originality_analysis": {
    "classification": "original|derivative|summary|compilation|copy",
    "originality_score": 85,
    "confidence": 0.92
  }
}
```

**Consumed By**:
- `daily-submission` - for platform matching
- `master-consolidator` - for final assessment

### 6. Daily Submission → Promotion Agent

**Pattern**: Platform opportunities with match scores

**Output Path**: `submissions/<batch_id>/`

**Output Files**:

**`opportunities.json`**:
```json
{
  "skill": "submission-finder",
  "version": "1.0",
  "opportunities_found": [
    {
      "platform": "Towards Data Science",
      "match_score": 92,
      "difficulty": "medium",
      "submission_requirements": {
        "format": "markdown",
        "max_words": 5000
      },
      "audience": {
        "size": "600k+ followers",
        "engagement": "high"
      }
    }
  ]
}
```

**Consumed By**:
- `promotion-agent` - for multi-channel strategy

### 7. Promotion Agent → (End of Pipeline)

**Output Path**: `promotion/<batch_id>/`

**Output Files**:

**`campaign-plan.json`**:
```json
{
  "skill": "promotion-strategist",
  "version": "1.0",
  "article_id": "doc-001",
  "promotion_strategy": {
    "primary_channels": [
      {
        "platform": "twitter",
        "priority": 1,
        "expected_reach": 5000,
        "roi_score": 85
      }
    ]
  },
  "campaign_timeline": {
    "day_1": ["twitter_post", "linkedin_post"],
    "week_1": ["influencer_engagement"]
  }
}
```

## Shared Directory Structure

```
.claude/
├── batch/              # Orchestrator-managed batches
│   ├── batch_0001/
│   │   ├── file-audits/       # File auditor outputs
│   │   ├── clusters/          # Cluster analyzer outputs
│   │   └── index.json         # Batch metadata
├── clusters/           # Consolidated cluster data
│   ├── cluster_001/
│   ├── cluster_002/
│   └── index.json
├── research/           # Web research results
│   ├── batch_0001/
│   └── search-results.json
├── assessments/        # Quality & originality reports
│   ├── quality-report.json
│   └── originality-report.json
├── submissions/        # Platform opportunities
│   └── opportunities.json
├── promotion/          # Campaign plans
│   └── campaign-plan.json
└── memory/             # Mutagen self-improvement
    ├── agent_performance.json
    └── prompt_archive/
```

## Data Flow Patterns

### Pattern 1: Sequential Pipeline
```
File Audit → Cluster Analysis → Quality Assessment → Submission → Promotion
```

**Use Case**: End-to-end document publication workflow

**Example**:
1. `file-auditor` processes 50 files
2. `cluster-analyzer` groups them into 8 clusters
3. `publication-assessor` evaluates quality of cluster representatives
4. `daily-submission` finds platforms for high-quality content
5. `promotion-agent` creates multi-channel campaign

### Pattern 2: Parallel Processing
```
Orchestrator
    ├── file-auditor-1 → batch_1
    ├── file-auditor-2 → batch_2
    ├── file-auditor-3 → batch_3
    ↓
    master-consolidator merges all batches
```

**Use Case**: Large codebase processing

**Example**: Process 1,000 files by spawning 10 file-auditor instances, each handling 100 files

### Pattern 3: Research-and-Validate
```
Web Research → Quality Assessment → Consolidation
```

**Use Case**: Research validation and synthesis

**Example**:
1. `web-researcher` finds 50 sources on topic
2. `publication-assessor` validates originality
3. `master-consolidator` synthesizes into final report

## Mutagen Memory System

### Self-Improvement Flow

**Step 1: Performance Tracking**
```json
// .claude/memory/agent_performance.json
{
  "agent_type": "file-auditor",
  "execution_id": "exec_001",
  "timestamp": "2025-11-06T00:00:00Z",
  "metrics": {
    "context_tokens_used": 45000,
    "payload_tokens_used": 38000,
    "quality_score": 0.87,
    "success": true,
    "files_processed": 45
  },
  "lessons_learned": "Large files need earlier chunking",
  "next_run_adjustments": {
    "suggested_chunk_size_reduction": 0.15
  }
}
```

**Step 2: Analysis (every 10 executions)**
- If quality_score < 0.7 → adjust prompts
- If payload overflow → reduce batch sizes
- Track successful strategies

**Step 3: Prompt Evolution**
- Generate new prompt versions (v1.3, v1.4)
- Archive in `.claude/prompts_archive/`
- Auto-increment to highest-performing version

### Inter-Agent Learning

**File Auditor Lessons**:
- "Skip node_modules/* patterns"
- "Large files (>8k tokens) need chunking at 6k"
- "PDFs require text extraction before processing"

**Cluster Analyzer Lessons**:
- "Increase threshold for code files (0.75 vs 0.65)"
- "Documentation clusters need structural similarity boost"
- "Hash prefix matching works for versioned files"

**Web Researcher Lessons**:
- "Documentation queries get 40% better results"
- "StackOverflow.com has highest relevance for technical topics"
- "Limit to 15 results per query type for optimal quality"

**Communication of Lessons**:
Lessons flow UP the hierarchy to the orchestrator, which distributes them to ALL subagents via `execution_history` parameter.

## Error Handling & Recovery

### Pattern: Graceful Degradation

**Token Budget Overflow**:
1. Subagent detects approaching limit (75% of payload budget)
2. Subagent stops processing current file
3. Saves partial results to output directory
4. Returns to orchestrator with:
   - `success: partial`
   - `files_processed: X`
   - `remaining_files: Y`
   - `recommendation: "continue_with_smaller_batch"`

**Orchestrator Response**:
- Reduce batch size for next iteration
- Spawn additional subagent to handle remaining files
- Merge partial results automatically

### Pattern: Retry with Backoff

**For Failed Operations**:
```json
{
  "status": "failed",
  "error": "web_search_timeout",
  "retry_count": 2,
  "next_retry_delay": "exponential_backoff",
  "fallback_strategy": "reduce_query_complexity"
}
```

## Quality Control

### File Auditor → Cluster Analyzer Handoff

**Validation Checklist**:
- [ ] All audit files have required metadata fields
- [ ] Hash values present for deduping
- [ ] Summary lengths within 500 words
- [ ] Extracted ideas lists are non-empty
- [ ] File type classifications are accurate

**Quality Score**: Check `batch/<id>/index.json` for completeness

### Cluster Analyzer → Consolidator Handoff

**Validation Checklist**:
- [ ] Each cluster has minimum 2 members (unless explicitly singleton)
- [ ] Confidence scores > 0.5 for all clusters
- [ ] No file appears in multiple clusters
- [ ] Family tree represents clear evolution
- [ ] Index.json accurately reflects cluster count

**Quality Score**: Check `clusters/index.json` for coverage

## Agent-Specific Communication Details

### File Auditor

**Inputs**:
- List of file paths
- Skip patterns
- Budget constraints

**Outputs**:
- `batch/<id>/file-audits/` (individual markdown files)
- `batch/<id>/index.json` (batch metadata)

**Uses Skill**:
- `file-summarizer` - for content analysis

**Consumed By**:
- `cluster-analyzer`

### Cluster Analyzer

**Inputs**:
- `batch/<id>/file-audits/` directories
- Similarity thresholds
- Previous clustering attempts

**Outputs**:
- `clusters/cluster_<id>/family_tree.md`
- `clusters/cluster_<id>/members.md`
- `clusters/index.json`

**Uses Skill**:
- `similarity-cluster` - for grouping logic

**Consumed By**:
- `master-consolidator`

### Web Researcher

**Inputs**:
- Research topics
- Query types (documentation, tutorial, blog, paper, video)
- Target domains

**Outputs**:
- `research/<id>/search-results.json`
- `research/<id>/content-summaries/`

**Uses Skill**:
- `web-scout` - for search and ranking

**Consumed By**:
- `publication-assessor`
- `master-consolidator`

### Document Organizer

**Inputs**:
- Consolidated cluster data
- Taxonomy categories
- Organization rules

**Outputs**:
- `organized/structure.json`
- `organized/readme.md`
- `organized/category_indexes/`

**Uses Skill**:
- `document-taxon` - for categorization
- `document-lineage` - for version tracking

**Consumed By**:
- `publication-assessor`
- End users

### Publication Assessor

**Inputs**:
- Document paths
- Quality criteria
- Originality requirements

**Outputs**:
- `assessments/<id>/quality-report.json`
- `assessments/<id>/originality-report.json`

**Uses Skills**:
- `quality-rubric` - for quality scoring
- `originality-checker` - for plagiarism detection

**Consumed By**:
- `daily-submission`
- `master-consolidator`

### Daily Submission

**Inputs**:
- Quality-scored documents
- Platform requirements
- Target categories

**Outputs**:
- `submissions/<id>/opportunities.json`
- `submissions/<id>/submission-queue.json`

**Uses Skill**:
- `submission-finder` - for platform discovery

**Consumed By**:
- `promotion-agent`
- End users

### Promotion Agent

**Inputs**:
- Publication opportunities
- Target audience
- Campaign goals

**Outputs**:
- `promotion/<id>/campaign-plan.json`
- `promotion/<id>/social-posts/`

**Uses Skill**:
- `promotion-strategist` - for multi-channel planning

**Consumed By**:
- End users (marketing teams)

### Master Consolidator

**Inputs**:
- All subagent outputs from pipeline
- Previously consolidated batches
- Merge rules

**Outputs**:
- `consolidated/final-report.md`
- `consolidated/executive-summary.md`
- `consolidated/recommendations.json`

**Special Role**:
- Final synthesis of all agent outputs
- Cross-validation of results
- Quality assurance checkpoint

**Consumed By**:
- End users (project stakeholders)

## Performance Optimization

### Batch Sizing Guidelines

**File Auditor**:
- Ideal: 30-50 files per batch
- Token limit: 30,000 tokens (75% of 40k budget)
- Large files (>8k tokens): chunk separately

**Cluster Analyzer**:
- Ideal: 200-500 files per clustering run
- Similarity calculations: O(n²) - avoid >1000 files
- Use incremental clustering for larger sets

**Web Researcher**:
- Ideal: 5-10 research topics per batch
- Queries per topic: 3-5
- Results per query: 10-20

**Publication Assessor**:
- Ideal: 10-20 documents per batch
- Quality + originality checks: ~2,000 tokens each
- Total per batch: <40,000 tokens

### Concurrency Limits

**Recommended**:
- Max concurrent subagents: 12
- File auditors: 5 (parallel)
- Cluster analyzers: 2 (sequential after audits)
- Web researchers: 3 (parallel)
- Consolidators: 1 (final step)

**Hardware Scaling**:
- Add 1 file-auditor per 100 CPU cores
- 1 cluster-analyzer per 500 files
- 1 web-researcher per 10 concurrent research topics

## Testing & Validation

### Communication Test Suite

**Test File**: `tests/test_agent_communication.py`

**Test Cases**:
1. **File Auditor → Cluster Analyzer Handoff**
   - Create sample audit files
   - Verify cluster analyzer can consume them
   - Check data completeness

2. **Cluster Analyzer → Consolidator Flow**
   - Generate sample clusters
   - Verify consolidator can merge them
   - Check for duplicates/missing files

3. **End-to-End Pipeline**
   - Run full pipeline: audit → cluster → assess → submit
   - Verify each agent receives valid inputs
   - Check final outputs are coherent

4. **Error Recovery**
   - Simulate token overflow
   - Verify graceful degradation
   - Check retry logic

5. **Mutagen Memory**
   - Create performance records
   - Verify lessons flow to next iteration
   - Check prompt evolution

### Test Data

**Sample Batch**: `tests/data/sample_batch/`
- 10 diverse file types
- Pre-generated audit files
- Mock cluster data
- Sample research results

**Expected Outputs**: `tests/expected/`
- Golden outputs for each agent
- Quality benchmarks
- Performance baselines
