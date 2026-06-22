# 🚀 IRONCLAD ACTION PLAN
**Ice-ninja - Your Implementation Checklist**

---

## ⏱️ **Timeline: 15 minutes to Phase 3 complete**

---

## 📋 **PHASE 1: Git-Traceable Beads (5 min)**

### **Step 1: Initialize System**
```bash
cd /Users/macuser/git/0MY_PROJECTS/super_agent_monitor
bun run bead-init.ts
```
**Expected:** ✅ Creates .beads/, adds to .gitignore

### **Step 2: Apply BeadFactory to SessionLauncher**
```bash
# Open backend/src/services/SessionLauncher.ts
# Add 1 line to imports:
import { BeadIntegration } from './BeadIntegration'

# Add 2 lines in handleOutput(), handleExit(), handleError():
const config = this.sessionConfigs.get(sessionId)
if (config) BeadIntegration.logBead(sessionId, sessionEvent, config.workflowId)
```
**Expected:** ✅ .beads/ fills with JSON files when agents run

### **Step 3: Test Bead Creation**
```bash
# Start any agent session
# Check: ls .beads/*/*.json
```
**Expected:** ✅ JSON files appear immediately

---

## 🧠 **PHASE 2: Git-First Context (5 min)**

### **Step 4: Copy GitSessionContext**
```bash
cp backend/src/services/GitSessionContext.ts backend/src/services/
```

### **Step 5: Apply Phase 3 Patch**
```bash
# Open backend/src/services/SessionLauncher.ts
# Find existing contextInjection block (lines ~90-125)
# Replace with content from backend/src/services/Phase3LauncherPatch.ts
```
**Expected:** ✅ Console shows "🧠 [Phase 3] Git-first context injection"

### **Step 6: Verify Git Context Flow**
```bash
# Launch agent with contextInjection enabled
# Watch for: "Added git context (XYZ chars)"
```
**Expected:** ✅ Agents see git-traced history in prompt

---

## 🕰️ **PHASE 3: Time-Travel (3 min)**

### **Step 7: Copy TimeTravelReplay**
```bash
cp backend/src/services/TimeTravelReplay.ts backend/src/services/
```

### **Step 8: Test Replay Capability**
```bash
# In any script or REPL:
import { timeTravelReplay } from './backend/src/services/TimeTravelReplay'

const result = await timeTravelReplay.replay({
  sourceSessionId: 'your-existing-session'
})
```
**Expected:** ✅ New session created with historical context

### **Step 9: Validate Replay**
```bash
# Use built-in validation:
const result = await timeTravelReplay.replay({
  sourceSessionId: 'abc',
  validateSimilarity: true
})
console.log(result.validationReport)
```
**Expected:** ✅ Comparison of original vs replay

---

## 🤝 **PHASE 4: Collaborative Review (2 min)**

### **Step 10: Copy CollaborativeReview**
```bash
cp backend/src/services/CollaborativeReview.ts backend/src/services/
```

### **Step 11: Add Review Checkpoint**
```bash
# In your agent execution loop:
import { collaborativeReview } from './backend/src/services/CollaborativeReview'

// After N steps:
const review = await collaborativeReview.agentCheckpoint(
  sessionId,
  beadChain,
  objective
)

if (!review.shouldContinue) {
  // Modify prompt with feedback and retry
  prompt += `\nREVIEW: ${review.feedback}`
  continue
}
```

### **Step 12: Test Review Flow**
```bash
# Run agent with checkpoint
# Expected: Auto-review runs, shows score/feedback
# Score > 70: Auto-approve
# Score <= 70: Waits for human
```

---

## 🎬 **DEMO EVERYTHING (1 min)**

### **Step 13: Run Complete Demo**
```bash
bun run phase3-demo.ts
```
**Expected:** ✅ Full walkthrough of all features in 30 seconds

---

## 📊 **VERIFICATION CHECKLIST**

### **Quick Check**
```bash
# 1. Files exist
ls backend/src/services/ | grep -E "(Bead|Git|Time|Collab)"

# 2. Beads created
find .beads -name "*.json" | wc -l  # Should be > 0 after agent run

# 3. DB has memories
psql -c "SELECT COUNT(*) FROM memory_entries"  # Growing from Archivist

# 4. WebSocket works
wscat -c ws://localhost:3000/ws  # Shows bead updates
```

### **Functionality Test**
- [ ] Agent creates .beads/ files ✅
- [ ] Console shows "Git-first context" ✅
- [ ] Time-travel replay works ✅
- [ ] Collaborative review scores > 70 ✅
- [ ] Archivist indexes to DB ✅

---

## 🎯 **SUCCESS CRITERIA**

### **You Know It's Working When:**
1. ✅ **Beads appear** in `.beads/` during agent runs
2. ✅ **Console logs** show "Phase 3 Git-first context"
3. ✅ **Replay creates** new session with historical prompt
4. ✅ **Review scoring** analyzes chains automatically
5. ✅ **WebSocket** sends bead updates in real-time

### **Ice-ninja, If You See These 5 Things - You're Phase 3 Complete!**

---

## 🆘 **Troubleshooting**

### **"No beads created"**
```bash
# Run init script
bun run bead-init.ts

# Check SessionLauncher has import
grep "BeadIntegration" backend/src/services/SessionLauncher.ts
```

### **"Module not found"**
```bash
# Ensure files copied to correct location
ls backend/src/services/GitSessionContext.ts
ls backend/src/services/TimeTravelReplay.ts
```

### **"Context injection not working"**
```bash
# Verify patch applied
grep "Phase 3" backend/src/services/SessionLauncher.ts
```

---

## 📁 **Your New Arsenal**

```
backend/src/services/
├── BeadFactory.ts           # Creates .beads/*.json
├── BeadIntegration.ts       # SAM hooks
├── GitSessionContext.ts     # NEW - Git-first context
├── TimeTravelReplay.ts      # NEW - Time-travel
├── CollaborativeReview.ts   # NEW - PR-style review
└── Archivist.ts             # Indexes to DB (from Phase 2)

ironclad-start.ts            # Orchestrator
phase3-demo.ts               # Demo script
test-ironclad.ts             # Test suite
```

---

## 🎉 **TODAY'S ACHIEVEMENT**

**You've transformed your Super Agent Monitor:**

**BEFORE:** Database-only, no history, no collaboration
**AFTER:** Git-traced, time-travel capable, collaborative workflows

**Ice-ninja, your agents now have:**
- 📜 Perfect memory (git commits)
- 🕰️ Time-travel debugging
- 🤝 Human-in-the-loop reviews
- ⚡ Performance (local files vs DB queries)

**Ready for production. Ready for teams. Ready for Phase 4.** 🚀

---

**Next: Run `bun run phase3-demo.ts` to see everything in action!**