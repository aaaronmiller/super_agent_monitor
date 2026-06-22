---
name: quality-rubric
description: Applies comprehensive quality evaluation rubric to assess publication worthiness. Provides detailed scoring and improvement recommendations.
---

# Quality Rubric Skill

## INPUT
- Document object with content
```json
{
  "path": "documents/article.md",
  "content": "Full text content",
  "metadata": {
    "title": "Title",
    "word_count": 2500,
    "author": "Name"
  }
}
```

## OUTPUT
Machine-parsable JSON with quality assessment:

```json
{
  "skill": "quality-rubric",
  "version": "1.0",
  "document_id": "doc-001",
  "overall_grade": "B",
  "overall_score": 85,
  "detailed_scores": {
    "originality_novelty": {
      "score": 21,
      "max": 25,
      "breakdown": {
        "unique_perspective": 9,
        "novel_insights": 7,
        "not_derivative": 5
      },
      "comments": "Good original insights, unique approach to problem"
    },
    "content_quality": {
      "score": 23,
      "max": 25,
      "breakdown": {
        "accuracy": 10,
        "depth": 8,
        "relevance": 5
      },
      "comments": "Accurate information, good depth, highly relevant"
    },
    "structure": {
      "score": 16,
      "max": 20,
      "breakdown": {
        "logical_flow": 8,
        "headers_sections": 6,
        "intro_conclusion": 2
      },
      "comments": "Good flow, clear sections, weak conclusion"
    },
    "writing_quality": {
      "score": 12,
      "max": 15,
      "breakdown": {
        "clarity": 8,
        "grammar": 4,
        "engagement": 0
      },
      "comments": "Clear writing, minor grammar issues, could be more engaging"
    },
    "technical_merit": {
      "score": 13,
      "max": 15,
      "breakdown": {
        "code_examples": 5,
        "citations": 3,
        "actionable": 5
      },
      "comments": "Good code examples, properly cited, actionable advice"
    }
  },
  "publication_readiness": {
    "verdict": "publishable_with_revisions",
    "target_grade": "A",
    "needed_improvements": [
      {
        "priority": "critical",
        "area": "structure",
        "issue": "Weak conclusion",
        "specific_fix": "Add 2-3 sentence conclusion summarizing key takeaways"
      },
      {
        "priority": "important",
        "area": "writing_quality",
        "issue": "Low engagement",
        "specific_fix": "Add more compelling examples and stories"
      }
    ],
    "estimated_effort": "2-3 hours"
  },
  "grade_distribution": {
    "A": 0,
    "B": 1,
    "C": 0,
    "D": 0,
    "F": 0
  }
}
```

## QUALITY RUBRIC (100 POINTS)

### 1. Originality & Novelty (25 points)

#### Unique Perspective (0-10 points)
- **9-10**: Fresh, innovative viewpoint that reframes the problem
- **7-8**: Distinct perspective with valuable insights
- **5-6**: Some originality, mostly follows conventional wisdom
- **3-4**: Limited originality, standard approach
- **0-2**: No unique perspective, purely derivative

**Evaluation Criteria:**
- Does it present a new way of thinking?
- Is the approach fresh or just recycling ideas?
- Does it challenge assumptions?

#### Novel Insights (0-10 points)
- **9-10**: Multiple original insights that advance understanding
- **7-8**: Several new insights or discoveries
- **5-6**: Some novel observations or connections
- **3-4**: Few original insights, mostly recaps
- **0-2**: No original insights

**Evaluation Criteria:**
- Are there "aha!" moments?
- Does it reveal something new?
- Do insights build on each other?

#### Not Derivative (0-5 points)
- **5**: Completely original work
- **4**: Minimally derivative, heavily transformed
- **3**: Some derivative elements, but transformed
- **2**: Noticeably derivative
- **0-1**: Heavily derivative or copy

### 2. Content Quality (25 points)

#### Accuracy (0-10 points)
- **9-10**: All information accurate, fact-checked
- **7-8**: Mostly accurate, minor inaccuracies
- **5-6**: Generally accurate, some errors
- **3-4**: Several inaccuracies
- **0-2**: Many factual errors

**Evaluation:**
- Verify claims and statistics
- Check technical accuracy
- Confirm cited information

#### Depth (0-10 points)
- **9-10**: Deep dive, comprehensive coverage
- **7-8**: Good depth, covers most aspects
- **5-6**: Adequate depth, surface-level on some areas
- **3-4**: Shallow, misses key aspects
- **0-2**: Very shallow, superficial

**Evaluation:**
- Goes beyond surface level
- Explores implications
- Provides comprehensive view

#### Relevance (0-5 points)
- **5**: Highly relevant to target audience
- **4**: Mostly relevant
- **3**: Somewhat relevant
- **2**: Limited relevance
- **0-1**: Not relevant

### 3. Structure & Organization (20 points)

#### Logical Flow (0-8 points)
- **7-8**: Excellent flow, natural progression
- **5-6**: Good flow, minor hiccups
- **3-4**: Adequate flow, some jumps
- **1-2**: Poor flow, hard to follow
- **0**: No clear flow

**Check:**
- Does each section lead to the next?
- Are transitions smooth?
- Is the progression logical?

#### Headers & Sections (0-6 points)
- **5-6**: Clear, descriptive headers, well-organized
- **3-4**: Adequate headers, some organization issues
- **1-2**: Poor headers, disorganized
- **0**: No headers, chaotic

#### Introduction & Conclusion (0-6 points)
- **5-6**: Strong intro hooks reader, conclusion summarizes
- **3-4**: Decent intro/conclusion
- **1-2**: Weak intro or conclusion
- **0**: No intro or conclusion

### 4. Writing Quality (15 points)

#### Clarity (0-8 points)
- **7-8**: Exceptionally clear, easy to understand
- **5-6**: Generally clear, minor confusion
- **3-4**: Somewhat unclear, needs clarification
- **1-2**: Often unclear, hard to follow
- **0**: Very unclear

#### Grammar & Style (0-4 points)
- **4**: Perfect grammar, excellent style
- **3**: Minor grammar issues, good style
- **2**: Some grammar errors, acceptable style
- **1**: Grammar issues, poor style
- **0**: Many grammar errors, bad style

#### Engagement (0-3 points)
- **3**: Highly engaging, compelling read
- **2**: Somewhat engaging
- **1**: Slightly engaging
- **0**: Not engaging

### 5. Technical Merit (15 points)

#### Code/Examples (0-5 points)
- **5**: Working code, complete examples
- **4**: Mostly working, good examples
- **3**: Partial code, basic examples
- **2**: Minimal code, poor examples
- **0-1**: No code, no examples

#### Citations & References (0-5 points)
- **5**: Properly cited, comprehensive references
- **4**: Well cited, mostly complete
- **3**: Adequately cited
- **2**: Poorly cited
- **0-1**: No citations

#### Actionable Takeaways (0-5 points)
- **5**: Clear, actionable advice
- **4**: Mostly actionable
- **3**: Some actionable elements
- **2**: Limited actionability
- **0-1**: Not actionable

## GRADE MAPPING

### A (90-100 points)
**Verdict:** Publishable with minor edits
**Actions:** Polish, fix minor issues
**Timeline:** 1-2 days

### B (80-89 points)
**Verdict:** Publishable with moderate revisions
**Actions:** Improve weak areas, add depth
**Timeline:** 1 week

### C (70-79 points)
**Verdict:** Needs substantial work
**Actions:** Major revisions, restructure
**Timeline:** 2-3 weeks

### D (60-69 points)
**Verdict:** Major revisions required
**Actions:** Rewrite sections, add content
**Timeline:** 1-2 months

### F (0-59 points)
**Verdict:** Not publishable in current form
**Actions:** Complete rewrite, novel research
**Timeline:** 3+ months

## IMPROVEMENT RECOMMENDATIONS

### For Each Score < 3/5 (in max categories)

**Structure Issues:**
- Add clear section headers
- Reorganize for better flow
- Write stronger conclusion
- Add smooth transitions

**Content Issues:**
- Add more depth
- Include original examples
- Provide more context
- Expand on key points

**Writing Issues:**
- Improve clarity
- Fix grammar errors
- Add engaging elements
- Use more active voice

**Technical Issues:**
- Add working code
- Include proper citations
- Provide actionable steps
- Add references

## DOCUMENT TYPE ADJUSTMENTS

### For Tutorials
- Weight "Code/Examples" higher (20 points)
- Weight "Actionable Takeaways" higher (10 points)
- Require working examples
- Check step-by-step clarity

### For Opinion Pieces
- Weight "Unique Perspective" higher (15 points)
- Weight "Engagement" higher (10 points)
- Require personal voice
- Check argument strength

### For Research
- Weight "Citations" higher (10 points)
- Weight "Depth" higher (15 points)
- Require methodology
- Check accuracy rigorously

### For Guides
- Weight "Actionable Takeaways" higher (15 points)
- Weight "Structure" higher (10 points)
- Check completeness
- Ensure practical value

## INTEGRATION WITH MUTAGEN
Track:
- Which criteria correlate with actual acceptances
- Distribution of scores across categories
- Common weak areas
- Improvement rates

Optimize:
- Rubric weights based on success
- Thresholds for publication
- Recommendation effectiveness
- Scoring consistency

## REFERENCE FILES

### Core Documentation
- **Agent Integration**: `.claude/agents/publication-assessor.md` - Uses this skill for evaluation
- **Quality Tracking**: `.claude/agents/publication-assessor.md` - Monitors improvement
- **Assessment Script**: `scripts/assess_quality.py` - Quality evaluation logic
- **Rubric Calculator**: `scripts/calculate_rubric.py` - Scoring algorithms

### Related Skills
- **originality-checker.md** - Combined with quality rubric for publication decisions
- **document-lineage.md** - Used to assess quality improvements across versions
- **submission-finder.md** - Platform matching based on quality scores

### Interactive Notebooks
**Jupyter Notebook**: `notebooks/quality-rubric-demo.ipynb`
- Demo: Apply 100-point rubric to sample documents
- Interactive: Adjust scoring criteria
- Visualization: Quality score breakdowns
- Practice: Generate improvement recommendations

**Google Colab**: https://colab.research.google.com/quality-rubric-demo
- Score your own documents
- Visualize quality metrics
- Compare document quality

### External References
1. **Academic Assessment**
   - Paper: "Rubric-Referenced Self-Assessment"
   - URL: https://doi.org/10.3102/0013173X030010029
   - Key concepts: Self-assessment validity, rubric design

2. **Content Quality Metrics**
   - Article: "Measuring Content Quality in Digital Media"
   - URL: https://ijoc.org/index.php/ijoc/article/view/1879
   - Focus: Quality indicators, measurement frameworks

3. **Writing Assessment**
   - Guide: "Automated Writing Evaluation"
   - URL: https://www.cte.edu/assessment/autowriting
   - Application: Rubric-based scoring systems

### Implementation Examples
**Python Reference**: `examples/quality-rubric-example.py`
```python
from quality_rubric import QualityRubric

rubric = QualityRubric()
result = rubric.assess_document("Document content here...")
print(f"Grade: {result['grade']} ({result['total_score']}/100)")
```

**Batch Assessment**: `examples/batch-evaluate.py`
- Assess multiple documents
- Generate quality reports
- Track improvement over time

### Testing & Validation
**Test Suite**: `tests/test_quality_rubric.py`
- Unit tests for scoring functions
- Grade calculation accuracy
- Recommendation generation tests
- Consistency validation

### Best Practices Guide
**Documentation**: `docs/quality-rubric-best-practices.md`
- When to use quality assessment
- Score interpretation guidelines
- Improvement recommendation tips
- Customizing rubric for content types

### Version History
- **v1.0** (2025-11-06): Initial release with 100-point rubric
- Future: Machine learning quality prediction
