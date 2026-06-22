# 🔮 Ironclad Installation Checklist

Ice-ninja, your Ironclad Hybrid Architecture is complete. Follow this checklist to deploy.

## ✅ **Phase 1: Setup (5 minutes)**

### 1. Initialize System
```bash
cd /Users/macuser/git/0MY_PROJECTS/super_agent_monitor
bun run bead-init.ts
```
- ✅ Creates `.beads/` directory
- ✅ Adds to `.gitignore`
- ✅ Creates type definitions

### 2. Apply SessionLauncher Patch
**File:** `backend/src/services/SessionLauncher.ts`

**Add import:**
```typescript
import { BeadIntegration } from './BeadIntegration'
```

**Add to `handleOutput()` (after line 348):**
```typescript
const config = this.sessionConfigs.get(sessionId)
if (config) {
  BeadIntegration.logBead(sessionId, sessionEvent, config.workflowId)
}
```

**Add to `handleExit()` (after line 454):**
```typescript
const config = this.sessionConfigs.get(sessionId)
if (config) {
  BeadIntegration.logBead(sessionId, sessionEvent, config.workflowId)
}
```

**See `BeadLauncherPatch.ts` for complete integration points.**

## ✅ **Phase 2: Integration (3 minutes)**

### 3. Add Archivist to Main Server
**File:** `backend/src/server.ts`

```typescript
import { archivist } from './services/Archivist'
import { smartNudge } from './services/SmartNudge'

// After webSocketService.initialize(server):
archivist.start(webSocketService)

// Add to SessionMonitor stall detection:
sessionMonitor.on('session:stalled', async (data) => {
  if (data.stallDuration > 45000) {
    const nudge = await smartNudge.generateApiPayload(data.sessionId)
    webSocketService.broadcast(nudge)
  }
})
```

## ✅ **Phase 3: Validation (2 minutes)**

### 4. Run System Tests
```bash
bun run test-ironclad.ts
```
Expected: All 6 tests pass

### 5. Start Demo Mode
```bash
bun run ironclad-start.ts --demo
```
Expected: Creates test beads, shows smart nudge, broadcasts via WebSocket

## ✅ **Phase 4: Production (2 minutes)**

### 6. Start Full System
**Terminal 1:** Your normal SAM backend
```bash
cd backend && bun run server.ts
```

**Terminal 2:** Ironclad Archivist
```bash
bun run ironclad-start.ts --integrated
```

### 7. Test with Real Agent
```bash
# Launch any agent session through your normal interface
# Watch .beads/ directory populate:
watch -n 1 'find .beads -name "*.json" | wc -l'
```

---

## 📋 **Expected Results**

### **File System**
```
.beads/
├── a3/
│   └── 8b2b7e.json (Bead 1)
├── 4f/
│   └── 9d1c2a.json (Bead 2)
└── index.json (Session mapping)
```

### **Database**
```sql
SELECT COUNT(*) FROM memory_entries WHERE metadata->>'bead_id' IS NOT NULL;
-- Should increase as beads get indexed
```

### **WebSocket Messages**
```json
{
  "type": "ARCHIVIST_UPDATE",
  "beadId": "8b2b7e...",
  "action": "indexed",
  "significance": 0.85,
  "session": "session-uuid"
}
```

### **Console Output**
```
📚 Indexed bead 8b2b7e... [tool_use] [0.85]
🧠 Smart Nudge ready for session: "You are stalled on npm error. Try rm -rf node_modules"
```

---

## 🎯 **Quick Commands**

### **Development**
```bash
# Run demo
bun run ironclad-start.ts --demo

# Run tests
bun run test-ironclad.ts

# Initialize only
bun run bead-init.ts
```

### **Production**
```bash
# Integrated mode (connects to existing SAM)
bun run ironclad-start.ts --integrated

# Standalone mode (separate service)
bun run ironclad-start.ts
```

### **Maintenance**
```bash
# Check bead count
find .beads -name "*.json" | wc -l

# Check indexed count
psql -c "SELECT COUNT(*) FROM memory_entries WHERE metadata->>'vector_status' = 'indexed'"

# Reset (dev only)
rm -rf .beads/*
```

---

## 🔧 **Troubleshooting**

### **"No beads created"**
- Check SessionLauncher patch was applied
- Verify `.beads/` directory exists
- Run: `bun run bead-init.ts`

### **"Archivist not indexing"**
- Check significance threshold (default 0.5)
- Lower in Archivist constructor if needed
- Verify PostgreSQL connection

### **"WebSocket not connecting"**
- Ensure port matches: `export IRONCLAD_PORT=3000`
- Check `ws://localhost:3000/ws` connects

### **"Smart nudge empty"**
- This is normal for new sessions
- Run agent for a while to create history
- Check `backend/src/services/SmartNudge.ts` for logic

---

## 📊 **Monitoring Commands**

### **Live Bead Creation**
```bash
watch -n 1 'ls -la .beads/*/*.json 2>/dev/null | wc -l'
```

### **Live Indexing Rate**
```bash
watch -n 1 'psql -c "SELECT COUNT(*) FROM memory_entries WHERE created_at > NOW() - INTERVAL '\''5 minutes'\''" -t'
```

### **WebSocket Activity**
```bash
wscat -c ws://localhost:3000/ws
```

---

## 🚨 **Security Notes**

1. **Beads contain sensitive data** - add `.beads/` to `.gitignore` ✓ (auto-done)
2. **Vector DB may store prompts** - consider encryption at rest
3. **WebSocket needs auth** - implement session tokens
4. **File watcher permissions** - ensure read/write access to `.beads/`

---

## 🎉 **Verification Complete**

When you see this sequence, you're live:

1. ✅ `bun run bead-init.ts` → "Ironclad Bead System Initialized"
2. ✅ `bun run test-ironclad.ts` → "ALL TESTS PASSED"
3. ✅ `bun run ironclad-start.ts --demo` → "Beads: 2, Nudge: [message]"
4. ✅ Real agent session → `.beads/` fills with JSON files
5. ✅ Archivist logs → "Indexed bead [hash]..."

**Ice-ninja, your Ironclad Hybrid Architecture is now operational!** 🚀

*The Factory is writing, the Archivist is indexing, and the Library is learning.*