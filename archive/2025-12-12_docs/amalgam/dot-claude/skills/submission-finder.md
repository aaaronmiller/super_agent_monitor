---
name: submission-finder
description: Discovers and evaluates publication submission opportunities. Maintains database of platforms and assesses suitability.
---

# Submission Finder Skill

## INPUT
- Article metadata and target category
```json
{
  "article_id": "doc-001",
  "title": "Article Title",
  "category": "technology/ai",
  "tags": ["ai", "machine-learning", "tutorial"],
  "grade": "B",
  "word_count": 2500
}
```

## OUTPUT
Machine-parsable JSON with submission opportunities:

```json
{
  "skill": "submission-finder",
  "version": "1.0",
  "search_timestamp": "2025-11-06T00:00:00Z",
  "opportunities_found": [
    {
      "platform": "Towards Data Science",
      "url": "https://towardsdatascience.com",
      "category": "medium",
      "match_score": 92,
      "difficulty": "medium",
      "submission_requirements": {
        "format": "markdown",
        "max_words": 5000,
        "min_words": 500,
        "bio_required": true,
        "links_allowed": true,
        "images_allowed": true,
        "code_required": false
      },
      "submission_process": {
        "method": "medium_publication",
        "url": "https://medium.com/towards-data-science/submit",
        "response_time": "1-3 days",
        "review_process": "editorial_review"
      },
      "audience": {
        "size": "600k+ followers",
        "engagement": "high",
        "demographic": "data scientists, ML engineers"
      },
      "past_performance": {
        "times_submitted": 3,
        "times_accepted": 2,
        "acceptance_rate": 67,
        "avg_views": 5000,
        "avg_likes": 150
      },
      "recommendation": "highly_recommended",
      "priority": 1,
      "notes": "Best fit for AI/ML content, high visibility"
    }
  ],
  "search_summary": {
    "total_platforms_checked": 25,
    "suitable_platforms": 8,
    "high_priority": 3,
    "medium_priority": 3,
    "low_priority": 2
  }
}
```

## PLATFORM CATEGORIES

### 1. Large Platforms (High Reach, High Competition)
**Medium Publications**
- Towards Data Science
- Better Programming
- The Startup
- HackerNoon
- Dev.to

**Characteristics:**
- Large audience
- High visibility
- More competition
- Faster response

**Best for:**
- High-quality content
- Technical tutorials
- Industry analysis

### 2. Niche Platforms (Medium Reach, Focused Audience)
**Developer Communities**
- Dev.to
- CSS-Tricks
- Smashing Magazine
- A List Apart

**AI/ML Specific**
- Distill.pub
- Papers With Code
- Machine Learning Mastery
- AI.JSX

**Best for:**
- Specialized content
- Technical depth
- Community engagement

### 3. Personal Blogs (Low Reach, High Control)
**Author Blogs**
- Ghost
- WordPress
- Substack

**Characteristics:**
- Full control
- Direct relationship with audience
- Lower traffic
- Build long-term

**Best for:**
- Building personal brand
- Direct audience connection
- Newsletter integration

## MATCH SCORING ALGORITHM

### Scoring Factors (100 points)

**1. Content Relevance (30 points)**
- Topic match (0-15)
- Tag overlap (0-10)
- Category fit (0-5)

**2. Platform Suitability (25 points)**
- Quality standards match (0-10)
- Editorial style fit (0-10)
- Audience expectation (0-5)

**3. Past Performance (20 points)**
- Historical acceptance rate (0-10)
- Engagement on similar content (0-5)
- Views/traffic potential (0-5)

**4. Practical Factors (15 points)**
- Submission requirements fit (0-5)
- Word count compatibility (0-5)
- Timeline urgency (0-5)

**5. Strategic Value (10 points)**
- Brand building (0-5)
- Relationship building (0-5)

### Match Score Calculation
```
match_score = (
  content_relevance * 0.3 +
  platform_suitability * 0.25 +
  past_performance * 0.2 +
  practical_factors * 0.15 +
  strategic_value * 0.1
)
```

### Score Ranges
- **90-100**: Excellent match, top priority
- **80-89**: Good match, high priority
- **70-79**: Decent fit, medium priority
- **60-69**: Weak match, low priority
- **<60**: Poor fit, avoid

## PLATFORM EVALUATION CRITERIA

### Difficulty Assessment
**Easy (High Acceptance Rate)**
- Open submissions
- Minimal requirements
- High acceptance rate (>70%)
- Fast response (<3 days)

**Medium (Moderate Competition)**
- Some requirements
- Moderate acceptance rate (40-70%)
- Standard response (3-7 days)

**Hard (Selective)**
- Strict requirements
- Low acceptance rate (<40%)
- Long response (1-2 weeks)
- Editorial review

### Audience Analysis
**Size Metrics:**
- Followers/subscribers
- Monthly visitors
- Social media reach

**Engagement Metrics:**
- Comments per post
- Social shares
- Time on page
- Return visitors

**Quality Metrics:**
- Audience expertise level
- Engagement quality
- Discussion depth

## SUBMISSION REQUIREMENTS CHECK

### Common Requirements
- [ ] Word count limits
- [ ] Format (Markdown, HTML, etc.)
- [ ] Author bio
- [ ] Social media links
- [ ] Headline/title guidelines
- [ ] Image guidelines
- [ ] Code formatting
- [ ] Citation style

### Optional Enhancements
- [ ] Include images/diagrams
- [ ] Add social media preview
- [ ] Create custom thumbnail
- [ ] Prepare video version
- [ ] Write Twitter thread version

## DISCOVERY STRATEGIES

### Search Queries
1. **General Discovery**
   - "best [topic] publications 2025"
   - "[topic] blogs accept guest posts"
   - "[technology] writing opportunities"

2. **Platform-Specific**
   - "write for us" + [topic] + 2025
   - "[publication] submission guidelines"
   - "[category] publications list"

3. **Community-Driven**
   - Reddit: r/publishin, r/writing, r/Medium
   - Twitter: "write for us" + [topic]
   - Discord: writing communities

### Research Methods
1. **Direct Platform Search**
   - Visit submission pages
   - Read guidelines thoroughly
   - Check recent posts
   - Analyze acceptance patterns

2. **Community Research**
   - Ask in writing communities
   - Check writer forums
   - Look for submission roundups
   - Follow other successful authors

3. **Competitor Analysis**
   - See where similar articles published
   - Analyze publication patterns
   - Study successful posts
   - Learn from rejections

## DATABASE STRUCTURE

### Platform Information
```json
{
  "platforms": {
    "platform-id": {
      "basic_info": {...},
      "requirements": {...},
      "process": {...},
      "audience": {...},
      "performance": {...},
      "last_updated": "date",
      "status": "active|inactive|test|blocked"
    }
  }
}
```

### Performance Tracking
- Submission attempts
- Acceptance rate
- Response times
- Engagement metrics
- Revenue (if applicable)

## NEW PLATFORM EVALUATION

### Evaluation Checklist
1. **Research Phase**
   - [ ] Visit platform
   - [ ] Read submission guidelines
   - [ ] Check recent posts
   - [ ] Analyze audience

2. **Test Phase**
   - [ ] Submit test article
   - [ ] Monitor response
   - [ ] Track engagement
   - [ ] Document experience

3. **Integration Phase**
   - [ ] Add to database
   - [ ] Set priority level
   - [ ] Update requirements
   - [ ] Schedule regular checks

### Risk Assessment
**Low Risk:**
- Established platforms
- Clear guidelines
- Responsive editors

**Medium Risk:**
- Newer platforms
- Changing requirements
- Unclear processes

**High Risk:**
- Unverified platforms
- No clear ownership
- Spam-like characteristics
- Unrealistic promises

## RECOMMENDATION ENGINE

### High Priority Recommendations (Score 90+)
- Best fit for content
- High success probability
- Strong strategic value
- Execute immediately

### Medium Priority (Score 70-89)
- Good fit
- Moderate success rate
- Consider if high priority not available
- Submit within 1 week

### Low Priority (Score 60-69)
- Decent fit
- Lower success rate
- Use for practice or backup
- Submit if no other options

### Avoid (Score <60)
- Poor fit
- Low success rate
- May harm reputation
- Do not submit

## INTEGRATION WITH MUTAGEN
Track:
- Which platforms yield best ROI
- Accuracy of match scoring
- Success rate predictions
- Response time patterns

Optimize:
- Scoring algorithm weights
- Discovery strategies
- Platform categorization
- Priority recommendations

## REFERENCE FILES

### Core Documentation
- **Agent Integration**: `.claude/agents/daily-submission.md` - Uses this skill for platform discovery
- **Submission Tracking**: `.claude/agents/daily-submission.md` - Monitors success rates
- **Platform Finder**: `scripts/find_submissions.py` - Platform discovery logic
- **Match Scorer**: `scripts/calculate_match.py` - Platform matching algorithm

### Related Skills
- **quality-rubric.md** - Quality scores used for platform matching
- **promotion-strategist.md** - Promotion planning after successful submission
- **originality-checker.md** - Ensures content is ready for submission

### Interactive Notebooks
**Jupyter Notebook**: `notebooks/submission-finder-demo.ipynb`
- Demo: Find platforms for sample articles
- Interactive: Adjust match criteria
- Visualization: Platform comparison charts
- Practice: Track submission performance

**Google Colab**: https://colab.research.google.com/submission-finder-demo
- Test platform matching
- Analyze submission opportunities
- Track success rates

### External References
1. **Content Distribution**
   - Paper: "Multi-Platform Content Distribution Strategies"
   - URL: https://doi.org/10.1016/j.chb.2019.106156
   - Key concepts: Platform selection, audience targeting

2. **Publishing Platforms**
   - Guide: "The Complete Guide to Content Publishing"
   - URL: https://www.contentmarketinginstitute.com
   - Focus: Platform requirements, best practices

3. **Submission Strategies**
   - Article: "How to Successfully Pitch Publications"
   - URL: https://www.writersdigest.com
   - Application: Query writing, platform research

### Implementation Examples
**Python Reference**: `examples/submission-finder-example.py`
```python
from submission_finder import SubmissionFinder

finder = SubmissionFinder()
result = finder.find_platforms("Article content...")
print(result)
```

**Batch Processing**: `examples/find-opportunities.py`
- Scan multiple articles
- Generate platform recommendations
- Track submission queue

### Testing & Validation
**Test Suite**: `tests/test_submission_finder.py`
- Unit tests for matching algorithm
- Success rate prediction accuracy
- Platform database validation
- Priority scoring tests

### Best Practices Guide
**Documentation**: `docs/submission-finder-best-practices.md`
- When to use platform finder
- Interpreting match scores
- Building submission strategies
- Tracking performance metrics

### Version History
- **v1.0** (2025-11-06): Initial release with 100-point match scoring
- Future: Machine learning for platform recommendation
