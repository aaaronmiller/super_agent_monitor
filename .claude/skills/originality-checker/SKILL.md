---
name: originality-checker
description: Assesses document originality, detects plagiarism, and identifies potential source materials. Distinguishes original work from summaries or derivatives.
---

# Originality Checker Skill

## INPUT
- Document object with content
```json
{
  "path": "documents/article.md",
  "content": "Full text content",
  "metadata": {
    "title": "Title",
    "author": "Name",
    "word_count": 2500
  }
}
```

## OUTPUT
Machine-parsable JSON with originality assessment:

```json
{
  "skill": "originality-checker",
  "version": "1.0",
  "document_id": "doc-001",
  "originality_analysis": {
    "classification": "original|derivative|summary|compilation|copy",
    "confidence": 0.92,
    "originality_score": 85,
    "uniqueness_indicators": [
      "First-person experience",
      "Original data/experiments",
      "Novel perspective"
    ],
    "derivative_indicators": [
      "Matches known content",
      "Summary language detected"
    ]
  },
  "source_detection": {
    "potential_sources": [
      {
        "source_type": "youtube_video",
        "url": "https://youtube.com/watch?v=...",
        "title": "Video Title",
        "similarity_score": 0.78,
        "match_type": "summary",
        "evidence": "Language patterns match video transcript"
      },
      {
        "source_type": "article",
        "url": "https://medium.com/...",
        "title": "Original Article",
        "similarity_score": 0.34,
        "match_type": "inspiration",
        "evidence": "Similar concepts, different execution"
      }
    ],
    "direct_quotes": 0,
    "paraphrased_sections": 2,
    "common_phrases": 5
  },
  "content_analysis": {
    "first_person_usage": "high|medium|low|none",
    "original_data": true,
    "unique_insights": [
      "Author's own experience",
      "Novel interpretation"
    ],
    "referenced_materials": [
      {
        "type": "citation",
        "content": "Reference to paper X",
        "properly_cited": true
      }
    ],
    "summary_sections": [
      {
        "start_line": 45,
        "length": 200,
        "summary_of": "Previous work on topic Y"
      }
    ]
  },
  "recommendations": {
    "verdict": "publishable_as_original",
    "actions_needed": [
      "Add more original insights",
      "Remove summary sections",
      "Include more personal experience"
    ],
    "attribution_required": false
  }
}
```

## CLASSIFICATION CATEGORIES

### 1. Original (Score: 80-100)
**Characteristics:**
- Majority original content and insights
- Personal experience, experiments, data
- Novel perspective on known topics
- Minimal copying from sources
- Properly cites references

**Acceptable:**
- Building on others' work
- Original analysis of existing data
- Personal stories and experiences
- Novel combinations of ideas

### 2. Derivative (Score: 50-79)
**Characteristics:**
- Heavily inspired by existing work
- Similar structure and content
- Adds limited original value
- May be transformable with edits

**Common Issues:**
- Recreates another's tutorial with minor changes
- Summarizes existing research without adding analysis
- Uses same examples and explanations

### 3. Summary (Score: 20-49)
**Characteristics:**
- Primarily summarizes existing content
- Little to no original analysis
- Often accompanies YouTube videos, books
- No new insights or perspectives

**Examples:**
- "This video explains X, here's what it covers..."
- "I read book Y, here are the main points..."
- "In this post, we learn about X"

### 4. Compilation (Score: 10-39)
**Characteristics:**
- Aggregates multiple sources
- Minimal original input
- Paraphrases without synthesis
- No clear value addition

**Examples:**
- List posts with no analysis
- "Top 10 X" without experience
- Aggregate of other people's work

### 5. Copy (Score: 0-9)
**Characteristics:**
- Substantial reproduction
- Minimal changes
- No attribution
- Potentially plagiarized

**Red Flags:**
- Identical wording
- No transformations
- Missing citations
- Same examples and structure

## PLAGIARISM DETECTION

### Search Query Generation
For each document, generate queries:

1. **Exact Title Match**
   - `"[EXACT_TITLE]" [AUTHOR]`
   - `"[EXACT_TITLE]" filetype:pdf`

2. **Key Phrase Search**
   - `"[UNIQUE_PHRASE]"` + site:medium.com
   - `"[UNIQUE_PHRASE]"` + site:dev.to
   - `"[UNIQUE_PHRASE]"` + site:reddit.com

3. **Conceptual Search**
   - `[TOPIC] + [RELATED_TERM]` + "tutorial" OR "guide"
   - `[TECHNIQUE] + [APPLICATION]` + "implementation"

4. **Author Search**
   - `[AUTHOR_NAME]` + publication history
   - `[AUTHOR_NAME]` + "[TOPIC]"

### Similarity Analysis
**Content Overlap:**
- Direct quotes (verbatim matches)
- Paraphrased sections (similar structure, different words)
- Common phrases (idomatic expressions)
- Structural similarity (same sections, organization)

**Acceptable Similarities:**
- Common knowledge
- Standard definitions
- Generic phrases
- Widely known facts
- Properly cited references

**Problematic Similarities:**
- Unique phrases
- Specific examples
- Original explanations
- Personal anecdotes
- Proprietary information

## ORIGINALITY INDICATORS

### Strong Indicators
- **First-person narrative**: "I tried...", "My experience...", "In my project..."
- **Original data**: Charts, graphs, experiments
- **Novel perspective**: "What others miss is..."
- **Personal insights**: "The key insight is..."
- **Unique examples**: Own projects, custom implementations

### Medium Indicators
- **New combinations**: Known concepts in new contexts
- **Extended analysis**: Building on others' work
- **Personal reflection**: "I found that..."
- **Practical application**: Real-world use cases

### Weak/No Indicators
- **Neutral tone**: No personal voice
- **Standard explanations**: Generic descriptions
- **Summary language**: "This covers...", "In this article..."
- **Generic examples**: Common, unremarkable cases

## QUALITY SCORING

### Originality Score Calculation (100 points)
```
Base Score: 50

Add points for:
+ First-person narrative (0-15)
+ Original data/examples (0-15)
+ Novel insights (0-10)
+ Personal experience (0-10)

Deduct points for:
- Direct copying (-50 to -100)
- Heavy paraphrasing (-20 to -50)
- Summary sections (-10 to -30)
- Missing citations (-5 to -20)
```

### Confidence Scoring
- **0.9-1.0**: Very confident in classification
- **0.7-0.9**: Confident, some uncertainty
- **0.5-0.7**: Moderate confidence
- **0.3-0.5**: Low confidence, needs review
- **0.0-0.3**: Very uncertain

## CONTENT TYPE DETECTION

### YouTube Video Summary
**Indicators:**
- "In this video...", "This video covers..."
- Time stamps mentioned
- "As the speaker says..."
- Summary of someone else's points

### Existing Article Copy
**Indicators:**
- Identical structure
- Same examples
- Paraphrased explanations
- Missing proper attribution

### Academic Paper Summary
**Indicators:**
- Formal language
- "The paper presents..."
- Summarizes findings
- No original analysis

### Original Tutorial
**Indicators:**
- Step-by-step with own examples
- Screenshots from own work
- Original code snippets
- Personal tips and tricks

## RECOMMENDATIONS

### For Original Work
- "Ready for publication"
- "Add more personal experience"
- "Include original examples"

### For Derivative Work
- "Transform with original insights"
- "Add personal experience section"
- "Use your own examples"
- "Include novel perspective"

### For Summary Work
- "Not suitable for publication as-is"
- "Transform into analysis, not summary"
- "Add your own research/experience"
- "Make it uniquely yours"

### For Copy Work
- "Cannot be published"
- "Remove copied content"
- "Add substantial original content"
- "Properly attribute all sources"

## INTEGRATION WITH MUTAGEN
Track:
- Which queries detect plagiarism most effectively
- Accuracy of classification categories
- Success of transformation recommendations
- Rate of false positives/negatives

Optimize:
- Query generation strategies
- Similarity threshold tuning
- Classification heuristics
- Recommendation effectiveness

## REFERENCE FILES

### Core Documentation
- **Agent Integration**: `.claude/agents/publication-assessor.md` - Uses this skill for originality assessment
- **Plagiarism Check**: `.claude/agents/publication-assessor.md` - Combined with quality rubric
- **Originality Script**: `scripts/check_originality.py` - Main originality detection logic
- **Similarity Analyzer**: `scripts/analyze_similarity.py` - Token comparison and matching

### Related Skills
- **quality-rubric.md** - Combined for publication decision making
- **document-lineage.md** - Tracks originality across document versions
- **file-summarizer.md** - Extracts content for originality checking

### Interactive Notebooks
**Jupyter Notebook**: `notebooks/originality-checker-demo.ipynb`
- Demo: Detect plagiarism in sample documents
- Interactive: Adjust similarity thresholds
- Visualization: Similarity heatmaps
- Practice: Generate verification queries

**Google Colab**: https://colab.research.google.com/originality-checker-demo
- Test originality detection
- Verify source citations
- Visualize similarity scores

### External References
1. **Plagiarism Detection**
   - Paper: "Plagiarism Detection: A Marker-Based Approach"
   - URL: https://doi.org/10.1007/978-3-540-74045-0_7
   - Key concepts: N-gram analysis, semantic matching

2. **Text Similarity**
   - Survey: "A Survey of Text Similarity Approaches"
   - URL: https://doi.org/10.1109/ICECT.2010.5477472
   - Focus: Cosine similarity, semantic analysis

3. **Academic Integrity**
   - Guide: "Plagiarism in Academic Writing"
   - URL: https://www.ithenticate.com/plagiarism-detection
   - Application: Best practices for attribution

### Implementation Examples
**Python Reference**: `examples/originality-checker-example.py`
```python
from originality_checker import OriginalityChecker

checker = OriginalityChecker()
result = checker.assess_originality("Document content here...")
print(f"Classification: {result['classification']}")
```

**Batch Checking**: `examples/check-collection.py`
- Check multiple documents
- Generate similarity reports
- Track originality scores

### Testing & Validation
**Test Suite**: `tests/test_originality_checker.py`
- Unit tests for similarity calculation
- Classification accuracy tests
- False positive detection
- Query generation validation

### Best Practices Guide
**Documentation**: `docs/originality-checker-best-practices.md`
- When to run originality checks
- Interpreting classification results
- Handling borderline cases
- Citation best practices

### Version History
- **v1.0** (2025-11-06): Initial release with 4-category classification
- Future: AI-powered semantic similarity
