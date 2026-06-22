---
name: promotion-strategist
description: Develops multi-channel promotion strategies for articles. Optimizes content for different platforms and calculates promotion ROI.
---

# Promotion Strategist Skill

## INPUT
- Article metadata and content
```json
{
  "article_id": "doc-001",
  "title": "Article Title",
  "url": "https://publication.com/article",
  "content": "Full content",
  "category": "technology/ai",
  "tags": ["ai", "ml", "tutorial"],
  "target_audience": "data scientists",
  "published_date": "2025-11-06"
}
```

## OUTPUT
Machine-parsable JSON with promotion strategy:

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
        "content_adaptation": {
          "hook": "Struggling with [problem]? Here's what I discovered...",
          "body": "2-3 key insights in 140 chars",
          "cta": "Read the full guide 👇",
          "hashtags": ["#AI", "#MachineLearning", "#DataScience"]
        },
        "posting_schedule": {
          "first_post": "2025-11-06 09:00",
          "follow_up_1": "2025-11-07 14:00",
          "follow_up_2": "2025-11-10 10:00"
        },
        "expected_reach": 5000,
        "engagement_prediction": 3.2,
        "roi_score": 85
      }
    ],
    "secondary_channels": [
      {
        "platform": "linkedin",
        "priority": 2,
        "content_adaptation": {
          "hook": "Personal story + problem",
          "body": "3 key insights from article",
          "cta": "What's your experience?",
          "tone": "professional_thought_leadership"
        }
      }
    ]
  },
  "campaign_timeline": {
    "day_1": ["twitter_post", "linkedin_post"],
    "day_2": ["reddit_post", "community_engagement"],
    "day_3": ["follow_up_twitter", "youtube_comment"],
    "week_1": ["influencer_engagement", "medium_response"],
    "week_2": ["promotion_summary", "engagement_analysis"]
  },
  "engagement_plan": {
    "respond_to_comments": true,
    "engagement_time": "within_2_hours",
    "key_people_to_engage": [
      {"platform": "twitter", "user": "@influencer1"},
      {"platform": "linkedin", "user": "Jane Smith"}
    ],
    "community_participation": [
      "r/MachineLearning",
      "r/artificial",
      "discord.ai"
    ]
  },
  "success_metrics": {
    "kpis": {
      "reach": "target 10k people",
      "engagement": "target 3% engagement rate",
      "traffic": "target 500 clicks",
      "conversions": "target 50 newsletter signups"
    },
    "tracking_method": "utm_parameters + analytics"
  }
}
```

## PLATFORM-SPECIFIC STRATEGIES

### 1. Twitter/X Strategy
**Optimal Format:**
- Hook: Question, bold claim, or surprising stat
- Body: 1-2 key insights (140 chars total)
- CTA: "Full guide below" or "Thread 👇"
- Hashtags: 2-3 max, specific not generic

**Content Adaptation:**
- Turn insights into questions
- Use emojis sparingly (1-2 max)
- Create curiosity gaps
- Share unexpected findings

**Posting Schedule:**
- First post: Within 2 hours of publication
- Follow-up 1: Next day at different time
- Follow-up 2: 3-4 days later
- Ongoing: Respond to questions, engage

**Engagement Tactics:**
- Reply to influencers' tweets
- Quote tweet relevant discussions
- Create Twitter threads (carousels)
- Polls and questions

### 2. LinkedIn Strategy
**Optimal Format:**
- Story-driven opening
- Professional insights
- Actionable takeaways
- Discussion questions

**Content Adaptation:**
- Personal experience angle
- Industry insights
- Professional network value
- "Lessons learned" format

**Posting Schedule:**
- Within 24-48 hours
- Peak times: Weekday mornings
- Follow-up: Respond to comments

**Engagement Tactics:**
- Ask questions at end
- Share in relevant groups
- Comment on industry leader posts
- Create LinkedIn articles (longer form)

### 3. Reddit Strategy
**Community-First Approach:**
- Value before promotion
- Follow community rules strictly
- No direct linking initially
- Participate genuinely first

**Content Adaptation:**
- Remove marketing language
- Focus on technical details
- Ask for feedback/help
- Share process, not just results

**Community Targeting:**
- r/MachineLearning (2.5M)
- r/artificial (2M)
- r/compsci (1.5M)
- r/MachineLearning (technical)
- r/artificial (general AI)

**Posting Schedule:**
- Read rules thoroughly first
- Post during community peak hours
- Engage immediately after posting
- Respond to all comments

**Warning:** Reddit is strict about self-promotion. Follow "9:1 rule" - 9 value posts for every 1 promotional.

### 4. HackerNews Strategy
**Format:**
- Clear, benefit-focused title
- Technical merit emphasis
- No fluff or marketing

**Title Formulas:**
- "Show HN: [Project/Tool] - [Benefit]"
- "I built [X] to solve [Y] problem"
- "Lessons learned building [X]"

**Submission Strategy:**
- Submit at 7-8 AM PT for front page
- Only if genuinely high quality
- Monitor comments, engage thoughtfully
- Don't solicit upvotes

### 5. Dev.to Strategy
**Format:**
- Markdown-friendly
- Code examples welcome
- Community-focused
- Beginner-friendly approach

**Content Adaptation:**
- Include working code
- Step-by-step tutorials
- "I wish I knew" format
- Multiple parts/series

## CONTENT ADAPTATION RULES

### Hook Adaptation by Platform
**Twitter:** "Did you know [surprising fact]?"
**LinkedIn:** "Last week, I discovered..."
**Reddit:** "[Problem description] - seeking advice"
**HN:** "Show HN: [tool] helps with [problem]"

### Body Adaptation
**Twitter:** 1-2 key points max
**LinkedIn:** 3-5 insights, story-driven
**Reddit:** Technical details, process
**HN:** Technical approach, results

### CTA Adaptation
**Twitter:** "Full guide below 👇"
**LinkedIn:** "What's your experience?"
**Reddit:** "Happy to answer questions"
**HN:** No direct CTA, let content speak

## PROMOTION TIMELINE

### Day 1 (Publication Day)
- [ ] Twitter post (morning)
- [ ] LinkedIn post (afternoon)
- [ ] Share in relevant Slack/Discord
- [ ] Email to newsletter subscribers
- [ ] Post on personal website

### Day 2
- [ ] Reddit post (1 community)
- [ ] Twitter follow-up
- [ ] Engage with comments
- [ ] Share in industry Facebook groups

### Day 3
- [ ] HackerNews (if applicable)
- [ ] Another Reddit community
- [ ] Twitter thread version
- [ ] YouTube comments (related videos)

### Week 1
- [ ] Medium responses
- [ ] Influencer engagement
- [ ] Twitter quote tweets
- [ ] Additional communities

### Week 2
- [ ] Summary post
- [ ] Lessons learned
- [ ] Thank you to community
- [ ] Performance analysis

## ENGAGEMENT STRATEGY

### Comment Engagement
**Timing:**
- Respond within 2 hours
- Check every 2-3 hours
- Continue for 48-72 hours

**Quality:**
- Thoughtful, substantive replies
- Add value beyond the article
- Ask clarifying questions
- Thank for engagement

**Community Guidelines:**
- Follow each platform's rules
- Be helpful, not promotional
- Build relationships
- Share credit

### Influencer Engagement
**Target:**
- Industry thought leaders
- Related content creators
- Potential collaborators
- Community moderators

**Approach:**
- Engage with their content first
- Share their work
- Add value to discussions
- Build relationships over time

## ROI CALCULATION

### Reach Metrics
- Impressions/views
- Unique users reached
- Social shares
- Click-through rate

### Engagement Metrics
- Likes/reactions
- Comments
- Shares/retweets
- Discussion depth

### Conversion Metrics
- Article reads
- Newsletter signups
- Follow/subscribe
- inquiries/contacts

### ROI Formula
```
ROI = (Engagement + Traffic + Conversions) / Effort

Where:
- Engagement: (likes + comments + shares) * engagement_value
- Traffic: clicks * avg_value
- Conversions: signups/follows * value
- Effort: time + resource cost
```

### Expected ROI by Platform
**Twitter:** High reach, medium engagement, medium conversions
**LinkedIn:** Medium reach, high engagement, high conversions
**Reddit:** Medium reach, high engagement (if valuable), low conversions
**HN:** Low reach, high engagement (quality), high conversions
**Dev.to:** Medium reach, high engagement (devs), medium conversions

## CRISIS MANAGEMENT

### Negative Feedback
1. **Listen** - Don't defend immediately
2. **Acknowledge** - Thank for feedback
3. **Clarify** - Ask questions to understand
4. **Respond** - Address concerns professionally
5. **Learn** - Apply to future content

### Platform-Specific Issues
**Reddit:** If downvoted/removed, learn from it
**Twitter:** If ratioed, adjust approach
**LinkedIn:** Professional tone always
**HN:** Technical merit is everything

## INTEGRATION WITH MUTAGEN
Track:
- Platform performance over time
- Content adaptation success
- Engagement patterns
- ROI by channel type

Optimize:
- Content hooks that work
- Best posting times
- Platform-specific strategies
- Community engagement approaches

## REFERENCE FILES

### Core Documentation
- **Agent Integration**: `.claude/agents/promotion-agent.md` - Uses this skill for campaign planning
- **Campaign Tracking**: `.claude/agents/promotion-agent.md` - Monitors engagement metrics
- **Promotion Script**: `scripts/promote_articles.py` - Campaign execution logic
- **ROI Calculator**: `scripts/calculate_roi.py` - Return on investment analysis

### Related Skills
- **submission-finder.md** - Finds platforms to promote on
- **quality-rubric.md** - Quality scores influence promotion strategy
- **originality-checker.md** - Ensures content is original before promotion

### Interactive Notebooks
**Jupyter Notebook**: `notebooks/promotion-strategist-demo.ipynb`
- Demo: Create multi-platform promotion campaigns
- Interactive: Test different strategies
- Visualization: ROI by platform
- Practice: Optimize engagement

**Google Colab**: https://colab.research.google.com/promotion-strategist-demo
- Plan promotion campaigns
- Analyze engagement metrics
- Calculate ROI

### External References
1. **Social Media Marketing**
   - Paper: "The Effects of Social Media on Content Distribution"
   - URL: https://doi.org/10.1016/j.chb.2019.106156
   - Key concepts: Engagement strategies, platform algorithms

2. **Multi-Channel Marketing**
   - Guide: "Integrated Marketing Communications"
   - URL: https://www.smartinsights.com
   - Focus: Channel coordination, campaign optimization

3. **Content Marketing**
   - Article: "The Complete Guide to Content Promotion"
   - URL: https://neilpatel.com
   - Application: Organic and paid promotion tactics

### Implementation Examples
**Python Reference**: `examples/promotion-strategist-example.py`
```python
from promotion_strategist import PromotionStrategist

strategist = PromotionStrategist()
campaign = strategist.create_campaign("Article content...", "Publication date...")
print(campaign)
```

**Campaign Planning**: `examples/plan-promotion.py`
- Design multi-platform campaigns
- Calculate expected ROI
- Schedule posts across channels

### Testing & Validation
**Test Suite**: `tests/test_promotion_strategist.py`
- Unit tests for ROI calculation
- Campaign planning accuracy
- Engagement prediction tests
- Platform adaptation validation

### Best Practices Guide
**Documentation**: `docs/promotion-strategist-best-practices.md`
- When to use promotion strategist
- Platform-specific strategies
- Campaign optimization tips
- Measuring success

### Version History
- **v1.0** (2025-11-06): Initial release with ROI calculation
- Future: AI-powered campaign optimization
