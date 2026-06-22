---
name: document-lineage
description: Identifies document versions, evolution, and relationships. Maps how ideas change across versions and detects duplicates.
---

# Document Lineage Skill

## INPUT
- Array of categorized documents
```json
[
  {
    "path": "documents/v1.md",
    "content": "Version 1 content",
    "metadata": {"title": "Title", "date": "2024-01-15"},
    "topics": ["ai", "ml"],
    "hash": "abc123..."
  }
]
```

## OUTPUT
Machine-parsable JSON with lineage mapping:

```json
{
  "skill": "document-lineage",
  "version": "1.0",
  "total_documents": 25,
  "series_identified": [
    {
      "series_name": "AI Fundamentals Series",
      "confidence": 0.94,
      "founder_document": "documents/ai-intro.md",
      "members": [
        {
          "path": "documents/ai-intro.md",
          "version_label": "v1",
          "role": "founder",
          "date": "2024-01-15",
          "hash": "abc123...",
          "similarity_score": 1.0,
          "key_differences": []
        },
        {
          "path": "documents/ai-advanced.md",
          "version_label": "v2",
          "role": "derived",
          "date": "2024-03-20",
          "hash": "def456...",
          "similarity_score": 0.87,
          "key_differences": [
            {
              "type": "addition",
              "description": "Added deep learning section",
              "impact": "major"
            },
            {
              "type": "modification",
              "description": "Expanded neural network explanation",
              "impact": "medium"
            },
            {
              "type": "removal",
              "description": "Removed basic definitions section",
              "impact": "major",
              "discarded_idea": "Basic definition of AI that was too simplistic"
            }
          ]
        }
      ],
      "evolution_analysis": {
        "direction": "progressive",
        "quality_trend": "improving",
        "completeness_trend": "increasing",
        "abandoned_ideas": [
          {
            "idea": "Basic AI definition",
            "removal_reason": "Too simplistic for advanced audience",
            "reintegration_recommendation": "Modify for beginners, keep simplified version"
          }
        ]
      }
    }
  ],
  "duplicates": [
    {
      "file1": "documents/similar-a.md",
      "file2": "documents/similar-b.md",
      "similarity_score": 0.96,
      "duplicate_type": "exact|partial|near-duplicate",
      "recommendation": "merge|keep-separate|remove-older"
    }
  ],
  "orphan_documents": [
    {
      "path": "documents/unique-article.md",
      "reason": "low_similarity",
      "best_match_score": 0.34,
      "notes": "Completely unique content"
    }
  ]
}
```

## LINEAGE DETECTION HEURISTICS

### 1. Similarity Scoring
```
similarity = (
  content_overlap * 0.4 +
  title_similarity * 0.2 +
  topic_overlap * 0.2 +
  structural_similarity * 0.1 +
  temporal_proximity * 0.1
)

content_overlap = word_intersection / word_union
title_similarity = levenshtein_distance(title1, title2)
topic_overlap = common_topics / total_topics
structural_similarity = section_structure_match
temporal_proximity = time_decay(1 - abs(date1 - date2) / 365)
```

### 2. Version Indicators
**Strong Indicators:**
- Same base filename with v1, v2, v3
- "Part 1", "Part 2" in titles
- "Revised", "Updated", "Final" in titles
- Explicit version numbers

**Medium Indicators:**
- Similar titles with slight variations
- Sequential date patterns
- Shared core content + additions
- "Continued from" references

**Weak Indicators:**
- Same topics and themes
- Similar writing style
- Related but not explicitly connected

### 3. Evolution Analysis
**Track changes:**
- **Additions**: New sections, ideas, examples
- **Modifications**: Rewrites, expansions, clarifications
- **Removals**: Deleted content (flag for potential reintegration)

**Assess impact:**
- **Major**: Changes meaning, adds/removes core concepts
- **Medium**: Clarifies, expands, improves examples
- **Minor**: Grammar, formatting, wording

### 4. Quality Assessment
**Quality Indicators:**
- Length trend (growing/shrinking/refined)
- Depth trend (superficial → detailed)
- Clarity trend (unclear → clear)
- Completeness trend (gaps → filled)

**Quality Score by Version:**
- v1: 0.65 (foundational, rough)
- v2: 0.78 (improved, clearer)
- v3: 0.89 (polished, complete)

### 5. Discarded Ideas Analysis
**For each removed idea, assess:**
- **Why was it removed?**
  - Redundant/duplicative
  - Inaccurate/outdated
  - Off-topic/tangential
  - Too advanced/too basic
  - Experimental/unsupported

- **Should it be reintegrated?**
  - Yes, with modifications
  - Yes, as appendix material
  - No, removal was correct
  - No, actively harmful

- **Where does it fit?**
  - In main text (modified)
  - In appendices
  - As footnotes
  - As "evolution notes"

## SERIES PATTERNS

### Pattern 1: Progressive Enhancement
- Each version adds depth
- Quality steadily improves
- Removes simplistic content
- **Strategy**: Create authoritative version with best of all

### Pattern 2: Divergent Branches
- v1, v2a, v2b (different approaches)
- Different audiences or goals
- **Strategy**: Keep separate, document differences

### Pattern 3: Refinement
- v1: Broad overview
- v2: Narrowed focus
- v3: Deep dive
- **Strategy**: Consolidate into single authoritative version

### Pattern 4: Pivot
- v1: Topic A
- v2: Topic B (different direction)
- **Strategy**: Mark as separate documents

## DUPLICATE DETECTION

### Duplicate Types
- **Exact**: Same hash, identical content
- **Near-exact**: 95%+ similarity, minor differences
- **Partial**: One document contains most of another
- **Conceptual**: Same ideas, different execution

### Recommendations
- **exact**: Keep one, remove others (mark removed)
- **near-exact**: Keep most recent, archive older
- **partial**: Merge or choose better version
- **conceptual**: Keep separate (different approaches)

## QUALITY METRICS
Track for each series:
- **Improvement Score**: (vN_quality - v1_quality) / v1_quality
- **Completeness**: % of planned content actually covered
- **Consistency**: How well versions align on core concepts
- **Value Additions**: New insights added in later versions

## INTEGRATION WITH MUTAGEN
Track:
- Which series detection heuristics work best
- Accuracy of similarity scoring
- Quality of evolution analysis
- Success of reintegration recommendations

Optimize:
- Similarity thresholds
- Version label detection
- Impact assessment accuracy
- Discarded idea evaluation

## REFERENCE FILES

### Core Documentation
- **Agent Integration**: `.claude/agents/document-organizer.md` - Uses this skill for version tracking
- **Quality Assessment**: `.claude/agents/publication-assessor.md` - Leverages for quality evaluation
- **Document Organization**: `scripts/organize_documents.py` - Helper for categorization
- **Similarity Analysis**: `scripts/analyze_similarity.py` - Token estimation and comparison

### Related Skills
- **document-taxon.md** - Categorizes documents by topic, used before lineage analysis
- **file-summarizer.md** - Extracts ideas that are tracked across versions
- **quality-rubric.md** - Used to assess version quality scores

### Interactive Notebooks
**Jupyter Notebook**: `notebooks/document-lineage-demo.ipynb`
- Demo: Track document evolution across versions
- Interactive: Adjust similarity thresholds
- Visualization: Lineage tree diagrams
- Practice: Authoritative version creation

**Google Colab**: https://colab.research.google.com/document-lineage-demo
- Track version relationships
- Create lineage visualizations
- Test similarity algorithms

### External References
1. **Version Control Systems**
   - Paper: "Understanding Version Control Systems"
   - URL: https://git-scm.com/book/en/v2
   - Key concepts: Git branching models, merge strategies

2. **Document Similarity**
   - Paper: "Similarity Measures for Text Document Clustering"
   - URL: https://doi.org/10.1142/9789812772467_0003
   - Focus: Cosine similarity, Jaccard index, Levenshtein distance

3. **Information Evolution**
   - Paper: "Tracking Changes in Evolving Documents"
   - URL: https://arxiv.org/abs/1901.03729
   - Application: Change tracking and evolution analysis

### Implementation Examples
**Python Reference**: `examples/document-lineage-example.py`
```python
from document_lineage import DocumentLineage

lineage = DocumentLineage()
result = lineage.analyze_versions([
    {"path": "v1.md", "content": "Version 1", "date": "2024-01-01"},
    {"path": "v2.md", "content": "Version 2", "date": "2024-02-01"}
])
print(result)
```

**Version Tracking Example**: `examples/track-evolution.py`
- Track multiple versions
- Identify series patterns
- Create authoritative documents

### Testing & Validation
**Test Suite**: `tests/test_document_lineage.py`
- Unit tests for similarity calculation
- Series detection accuracy tests
- Evolution pattern recognition
- Reintegration recommendation validation

### Best Practices Guide
**Documentation**: `docs/document-lineage-best-practices.md`
- When to use lineage analysis
- Similarity threshold guidelines
- Handling divergent branches
- Authoritative version creation

### Version History
- **v1.0** (2025-11-06): Initial release
- Future: Version tracking in `.claude/memory/`
