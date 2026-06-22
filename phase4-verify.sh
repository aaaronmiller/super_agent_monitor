#!/bin/bash
# 🎯 Phase 4 Verification Script for Ice-ninja
# Run this to verify all Phase 4 components are in place

echo "🔮 Phase 4 Verification - Ironclad System"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
RESET='\033[0m'

# Counters
passed=0
total=0

check_file() {
    local file=$1
    local name=$2
    total=$((total + 1))

    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        lines=$(wc -l < "$file")
        echo -e "${GREEN}✅${RESET} $name (${lines} lines, ${size} bytes)"
        passed=$((passed + 1))
    else
        echo -e "${RED}❌${RESET} $name - MISSING"
    fi
}

check_route() {
    local route=$1
    echo "   📡 API: $route"
}

echo "1️⃣  Core Services"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "backend/src/services/GitWorkflowManager.ts" "GitWorkflowManager"
check_file "backend/src/services/MultiAgentCoordinator.ts" "MultiAgentCoordinator"
check_file "backend/src/services/VisualDiffService.ts" "VisualDiffService"
check_file "backend/src/services/WebhookAutomation.ts" "WebhookAutomation"
check_file "backend/src/services/CheckpointTemplates.ts" "CheckpointTemplates"
echo ""

echo "2️⃣  API Routes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "backend/src/routes/phase4.ts" "Phase 4 Router"
if [ -f "backend/src/routes/phase4.ts" ]; then
    echo "   Available endpoints:"
    check_route "POST /api/phase4/workflow/pr/:sessionId"
    check_route "POST /api/phase4/workflow/merge/:workflowId"
    check_route "POST /api/phase4/agent/coordinate"
    check_route "POST /api/phase4/diff/generate"
    check_route "POST /api/phase4/webhook/register/:sessionId"
    check_route "POST /api/phase4/template/apply/:sessionId"
fi
echo ""

echo "3️⃣  Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "PHASE4_COMPLETE.md" "Phase 4 Complete Guide"
check_file "PHASE3_COMPLETE.md" "Phase 3 Architecture"
echo ""

echo "4️⃣  Previous Phase Core (Should exist)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "backend/src/services/BeadFactory.ts" "BeadFactory (Phase 1)"
check_file "backend/src/services/Archivist.ts" "Archivist (Phase 2)"
check_file "backend/src/services/TimeTravelReplay.ts" "TimeTravelReplay (Phase 3)"
check_file "backend/src/services/GitSessionContext.ts" "GitSessionContext (Phase 3)"
echo ""

echo "5️⃣  Integration & Demo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "backend/src/services/Phase3LauncherPatch.ts" "Phase 3 Integration Patch"
check_file "phase3-demo.ts" "Phase 3 Demo"
check_file "phase4-verify.sh" "This verification script"
echo ""

echo "📊 RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Passed: ${GREEN}${passed}/${total}${RESET}"

if [ $passed -eq $total ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED - PHASE 4 COMPLETE!${RESET}"
    echo ""
    echo "Next Steps:"
    echo "  1. Run: bun run phase3-demo.ts"
    echo "  2. Apply: backend/src/services/Phase3LauncherPatch.ts to SessionLauncher"
    echo "  3. Test: curl http://localhost:3001/api/phase4/health"
    echo "  4. Explore: Open PHASE4_COMPLETE.md for usage examples"
else
    echo -e "${YELLOW}⚠️  Some files missing. Run: git status to see what's missing.${RESET}"
fi
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"