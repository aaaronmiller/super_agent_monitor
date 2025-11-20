---
name: web-search-advanced
displayName: Advanced Web Search Techniques
description: Expert knowledge for effective web searching and information gathering
category: skill
tags: [web, search, research, information-gathering]
dependencies: []
version: 1.0.0
---

# Advanced Web Search Skill

This skill provides expert knowledge for conducting effective web searches and gathering high-quality information.

## Search Operators

### Google Search Operators
- `site:example.com` - Search within specific site
- `"exact phrase"` - Search for exact phrase
- `filetype:pdf` - Find specific file types
- `-exclude` - Exclude terms
- `intitle:keyword` - Search in page titles
- `inurl:keyword` - Search in URLs
- `related:example.com` - Find similar sites
- `cache:example.com` - View cached version

### Advanced Combinations
```
site:github.com "multi-agent" language:python
intitle:"API documentation" -site:stackoverflow.com
filetype:pdf "machine learning" site:arxiv.org
```

## Search Strategies

### 1. Start Broad, Then Narrow
```
Step 1: "AI agent orchestration"
Step 2: "AI agent orchestration" + "production"
Step 3: "AI agent orchestration" + "production" + "monitoring"
```

### 2. Use Multiple Sources
- Academic: Google Scholar, arXiv, ResearchGate
- Technical: GitHub, Stack Overflow, Documentation sites
- News: Google News, Hacker News, Reddit
- Social: Twitter, LinkedIn, Discord

### 3. Verify Information
- Cross-reference across 3+ independent sources
- Check publication dates for current info
- Evaluate source authority and bias
- Look for primary sources when possible

## Source Quality Assessment

### High-Quality Sources
✅ Academic papers (peer-reviewed)
✅ Official documentation
✅ Government/institutional sites (.gov, .edu)
✅ Reputable news organizations
✅ Industry expert blogs (verified)

### Questionable Sources
⚠️ Anonymous blogs
⚠️ Unverified social media posts
⚠️ Sites with excessive ads
⚠️ Outdated content (>3 years old for tech)
⚠️ Sites with no author information

## Boolean Search Techniques

### AND (narrow results)
```
"Claude Code" AND "multi-agent" AND "workflow"
```

### OR (broaden results)
```
"AI agent" OR "autonomous agent" OR "intelligent agent"
```

### NOT (exclude)
```
"machine learning" NOT "deep learning"
```

### Grouping
```
("AI agent" OR "autonomous agent") AND (orchestration OR coordination)
```

## Finding Recent Information

```
# Last 24 hours
Tools → Any time → Past 24 hours

# Specific date range
Tools → Custom range → 01/01/2025 - 01/31/2025

# Sort by date
Tools → Sort by date
```

## Domain-Specific Search Tips

### Technical Documentation
```
site:docs.anthropic.com OR site:docs.openai.com "API reference"
```

### Academic Research
```
site:arxiv.org OR site:scholar.google.com "multi-agent systems"
```

### Code Examples
```
site:github.com "agent orchestration" language:typescript
```

### Product Reviews
```
"Super Agent Monitor" (review OR comparison OR alternative)
```

## Handling No Results

If search returns nothing:
1. Remove quotes from phrases
2. Try synonyms
3. Broaden search terms
4. Check spelling
5. Try different search engines (DuckDuckGo, Bing)

## Ethical Considerations

- Respect robots.txt
- Don't overwhelm servers with requests
- Cite sources properly
- Respect paywalls (find legal alternatives)
- Verify facts before sharing

## Search Workflow Example

```markdown
Research Question: "What are the best practices for AI agent monitoring?"

Step 1: Broad search
→ "AI agent monitoring"
→ Results: 234,000 (too broad)

Step 2: Add context
→ "AI agent monitoring" + "production"
→ Results: 45,000 (better)

Step 3: Find authoritative sources
→ site:anthropic.com OR site:openai.com "agent monitoring"
→ Results: 12 (high quality)

Step 4: Find alternatives/discussions
→ site:reddit.com OR site:news.ycombinator.com "agent monitoring"
→ Results: 89 (community insights)

Step 5: Academic perspective
→ site:arxiv.org "agent" AND "observability"
→ Results: 23 (research papers)
```

## Tools & Resources

### Search Engines
- Google: General purpose
- Google Scholar: Academic papers
- GitHub: Code and repositories
- DuckDuckGo: Privacy-focused
- Perplexity: AI-powered search with citations

### Research Databases
- arXiv.org: Pre-print papers
- JSTOR: Academic journals
- IEEE Xplore: Engineering papers
- PubMed: Medical research

### Fact-Checking
- Snopes: General fact-checking
- FactCheck.org: Political claims
- PolitiFact: Political fact-checking
