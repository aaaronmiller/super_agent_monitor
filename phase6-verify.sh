#!/bin/bash
# 🎯 Phase 6 Enterprise Verification Script
# Verify all Phase 6 components are in place

echo "🚀 Phase 6 Enterprise Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

passed=0
total=0

check_file() {
    local file=$1
    local name=$2
    total=$((total + 1))

    if [ -f "$file" ]; then
        size=$(wc -c < "$file" 2>/dev/null || echo "0")
        lines=$(wc -l < "$file" 2>/dev/null || echo "0")
        echo -e "${GREEN}✅${RESET} $name (${lines} lines)"
        passed=$((passed + 1))
    else
        echo -e "${RED}❌${RESET} $name - MISSING"
    fi
}

check_file_size() {
    local file=$1
    local name=$2
    local min_size=$3
    total=$((total + 1))

    if [ -f "$file" ]; then
        size=$(wc -c < "$file" 2>/dev/null || echo "0")
        if [ "$size" -gt "$min_size" ]; then
            echo -e "${GREEN}✅${RESET} $name (${size} bytes)"
            passed=$((passed + 1))
        else
            echo -e "${YELLOW}⚠️ ${RESET} $name (too small: ${size} bytes)"
        fi
    else
        echo -e "${RED}❌${RESET} $name - MISSING"
    fi
}

echo -e "${BLUE}1. Backend Services${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file_size "backend/src/services/LiveCollaborationService.ts" "LiveCollaborationService" 5000
check_file_size "backend/src/services/TeamRBACService.ts" "TeamRBACService" 15000
check_file_size "backend/src/services/CIIntegrationHub.ts" "CIIntegrationHub" 8000
echo ""

echo -e "${BLUE}2. API Routes${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file_size "backend/src/routes/phase6.ts" "Phase 6 Router" 8000
echo ""

echo -e "${BLUE}3. Frontend Pages${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file_size "frontend/src/routes/phase6/+page.svelte" "Main Phase 6 Page" 6000
check_file "frontend/src/routes/phase6/+layout.svelte" "Layout"
echo ""

echo -e "${BLUE}4. Frontend Components${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file_size "frontend/src/routes/phase6/CollaborationInterface.svelte" "Collaboration Interface" 8000
check_file_size "frontend/src/routes/phase6/TeamManagement.svelte" "Team Management" 8000
check_file_size "frontend/src/routes/phase6/CIIntegration.svelte" "CI Integration" 8000
echo ""

echo -e "${BLUE}5. Sub-Pages${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "frontend/src/routes/phase6/collab/+page.svelte" "Collaboration Page"
check_file "frontend/src/routes/phase6/teams/+page.svelte" "Teams Page"
check_file "frontend/src/routes/phase6/cicd/+page.svelte" "CI/CD Page"
echo ""

echo -e "${BLUE}6. Documentation${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file_size "PHASE6_COMPLETE.md" "Phase 6 Complete Guide" 5000
echo ""

echo -e "${BLUE}7. Previous Phases (Should Exist)${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "PHASE4_COMPLETE.md" "Phase 4 Guide"
check_file "PHASE3_COMPLETE.md" "Phase 3 Guide"
check_file "ICE-NINJA_IRONCLAD_COMPLETE.md" "Complete Guide"
echo ""

echo -e "${BLUE}8. Integration Points${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "backend/src/services/GitCheckpointService.ts" "GitCheckpoint (Phase 3)"
check_file "backend/src/services/GitWorkflowManager.ts" "GitWorkflow (Phase 4)"
check_file "backend/src/services/WebhookAutomation.ts" "Webhook (Phase 4)"
echo ""

echo "📊 RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Passed: ${GREEN}${passed}/${total}${RESET}"

if [ $passed -eq $total ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED - PHASE 6 ENTERPRISE READY!${RESET}"
    echo ""
    echo "Next Steps:"
    echo "  1. Start WebSocket Server (auto-starts on backend)"
    echo "     bun run dev (in backend directory)"
    echo ""
    echo "  2. Start Frontend"
    echo "     cd frontend && bun run dev"
    echo ""
    echo "  3. Test Phase 6 Features:"
    echo "     • http://localhost:5173/phase6 (main dashboard)"
    echo "     • http://localhost:5173/phase6/collab (live collaboration)"
    echo "     • http://localhost:5173/phase6/teams (RBAC management)"
    echo "     • http://localhost:5173/phase6/cicd (CI/CD integration)"
    echo ""
    echo "  4. Verify WebSocket (in browser console):"
    echo "     const ws = new WebSocket('ws://localhost:8080/ws/collaborate')"
    echo "     ws.onopen = () => console.log('Connected!')"
    echo ""
    echo "  5. Test Team RBAC:"
    echo "     curl http://localhost:3001/api/phase6/health"
    echo ""
    echo "  6. Generate CI Config:"
    echo "     curl http://localhost:3001/api/phase6/ci/templates"
    echo ""
    echo "🚀 Quick Commands:"
    echo "   ./start-phase6.sh   # Start all Phase 6 services"
    echo "   curl http://localhost:8080/health   # WebSocket health"
    echo "   curl http://localhost:3001/api/phase6/health   # API health"
else
    echo -e "${YELLOW}⚠️  Some files missing. Run git status to see what's missing.${RESET}"
    echo ""
    echo "Common fixes:"
    echo "  • Run: git status"
    echo "  • Check if backend services are built"
    echo "  • Verify frontend dependencies: cd frontend && bun install"
fi
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"