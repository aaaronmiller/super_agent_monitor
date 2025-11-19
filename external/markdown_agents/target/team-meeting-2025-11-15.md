# Team Meeting Notes - November 15, 2025

**Attendees**: Sarah (PM), Mike (Backend), Lisa (Frontend), Tom (DevOps)
**Time**: 2:00 PM - 3:15 PM

## Agenda
1. Sprint review
2. AI Assistant progress
3. Infrastructure concerns
4. Next sprint planning

---

## Sprint Review

### Completed
- Authentication system fully implemented ✅
- VS Code extension scaffold created ✅
- Backend API endpoints for suggestions ✅
- Redis caching layer added ✅

### In Progress
- Bug detection algorithm refinement 🔄
- Integration tests for auth flow 🔄
- UI polish for extension 🔄

### Blocked
- Claude API rate limits hitting us hard 🚫
  - Need to implement better caching strategy
  - Consider fallback to local models for simple cases
  - Mike to investigate batch processing

## AI Assistant Discussion

**Mike**: "The Claude API costs are higher than projected. We're at $2000/month already with just 50 beta users."

**Sarah**: "We budgeted $5000/month for 500 users, so that's way over. What's causing the spike?"

**Mike**: "A lot of duplicate requests. Users are triggering suggestions on every keystroke. We need smarter debouncing and better caching."

**Action Items**:
- Implement 300ms debounce on keystroke triggers (Lisa)
- Cache suggestions per file hash, not per request (Mike)
- Add telemetry to track actual usage patterns (Tom)
- Consider local fallback model for basic suggestions (Research needed)

## Infrastructure Concerns

**Tom**: "PostgreSQL is running hot during peak hours. Query performance degrading."

**Mike**: "We're not using indexes properly. Also, the OAuth token lookups are slow."

**Solutions**:
- Add composite index on (user_id, created_at) for refresh_tokens table
- Move OAuth tokens to Redis (faster lookups)
- Consider read replica for analytics queries
- Tom to set up monitoring dashboards

## UI/UX Feedback

**Lisa**: "Beta testers love the inline suggestions but hate the popup window for explanations. It's jarring."

**Sarah**: "Can we make it less intrusive? Maybe a sidebar panel?"

**Lisa**: "Yes, VS Code has a webview sidebar API. Would be much better UX. I'll prototype this week."

**Feedback from beta testers**:
- "Suggestions are usually good but sometimes way off base"
- "Love the bug detection, saved me twice this week"
- "Refactoring suggestions are too aggressive - scary to accept"
- "Need keyboard shortcuts, clicking is slow"

## Security Review

**Mike**: "Had a security researcher reach out about code privacy concerns."

**Sarah**: "What's the issue?"

**Mike**: "Users are worried their proprietary code is being sent to Anthropic's servers. We need to be more transparent."

**Actions**:
- Add clear disclosure in extension about data handling
- Provide option for on-premise deployment (enterprise feature)
- Write blog post about our security practices
- Consider adding "local mode" that uses smaller model without API

## Next Sprint Goals

### High Priority
1. Reduce API costs to <$30/user/month
2. Improve suggestion accuracy (get acceptance rate to 75%+)
3. Implement sidebar panel for explanations
4. Add keyboard shortcuts

### Medium Priority
1. Optimize database performance
2. Set up monitoring dashboards
3. Write security disclosure documentation
4. Research local model options

### Low Priority
1. Multi-language support exploration
2. Mobile IDE investigation (very early research)
3. Custom model fine-tuning experiments

## Parking Lot
- Code collaboration features (multiple devs, one session)
- Integration with GitHub Copilot (complement, not compete)
- Offline mode for airplane coding

## Action Items Summary

| Owner | Task | Due Date |
|-------|------|----------|
| Lisa | Implement 300ms debounce | Nov 22 |
| Mike | Add file hash caching | Nov 22 |
| Tom | Set up monitoring dashboards | Nov 25 |
| Mike | Add database indexes | Nov 18 |
| Lisa | Prototype sidebar panel | Nov 25 |
| Sarah | Write security blog post | Nov 30 |
| All | Research local model options | Dec 5 |

## Next Meeting
**Date**: November 22, 2025
**Time**: 2:00 PM
**Focus**: API cost reduction results + sidebar UX demo

---

**Notes compiled by**: Sarah
**Shared with**: Engineering team, Leadership
