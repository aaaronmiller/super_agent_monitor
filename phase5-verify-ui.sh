#!/bin/bash
# 🎯 Phase 5 UI Verification Script
# Verify all Phase 5 frontend components are in place

echo "🔮 Phase 5 UI Verification - Production Interface"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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
        echo -e "${GREEN}✅${RESET} $name (${lines} lines, ${size} bytes)"
        passed=$((passed + 1))
    else
        echo -e "${RED}❌${RESET} $name - MISSING"
    fi
}

echo "1️⃣  Core Layout & Routing"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "frontend/src/routes/phase5/+page.svelte" "Main Dashboard"
check_file "frontend/src/routes/phase5/+layout.svelte" "Layout Wrapper"
check_file "frontend/src/routes/phase5/Navigation.svelte" "Navigation Sidebar"
echo ""

echo "2️⃣  Individual Page Routes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "frontend/src/routes/phase5/dashboard/+page.svelte" "Dashboard Route"
check_file "frontend/src/routes/phase5/agents/+page.svelte" "Multi-Agent Route"
check_file "frontend/src/routes/phase5/diff/+page.svelte" "Diff Viewer Route"
check_file "frontend/src/routes/phase5/workflows/+page.svelte" "Workflows Route"
check_file "frontend/src/routes/phase5/templates/+page.svelte" "Templates Route"
check_file "frontend/src/routes/phase5/analytics/+page.svelte" "Analytics Route"
check_file "frontend/src/routes/phase5/deployment/+page.svelte" "Deployment Route"
check_file "frontend/src/routes/phase5/settings/+page.svelte" "Settings Route"
check_file "frontend/src/routes/phase5/help/+page.svelte" "Help Route"
echo ""

echo "3️⃣  Reusable Components"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "frontend/src/routes/phase5/DiffViewer.svelte" "Diff Viewer Component"
check_file "frontend/src/routes/phase5/AnalyticsDashboard.svelte" "Analytics Component"
check_file "frontend/src/routes/phase5/TemplateManager.svelte" "Template Manager"
check_file "frontend/src/routes/phase5/DeploymentTools.svelte" "Deployment Tools"
echo ""

echo "4️⃣  Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "PHASE5_COMPLETE.md" "Phase 5 Complete Guide"
echo ""

echo "📊 RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Passed: ${GREEN}${passed}/${total}${RESET}"

if [ $passed -eq $total ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED - PHASE 5 UI COMPLETE!${RESET}"
    echo ""
    echo "Next Steps:"
    echo "  1. Start development server:"
    echo "     cd frontend && bun run dev"
    echo ""
    echo "  2. Visit http://localhost:5173/phase5"
    echo ""
    echo "  3. Test all routes:"
    echo "     - /phase5/dashboard (overview)"
    echo "     - /phase5/analytics (metrics)"
    echo "     - /phase5/agents (coordination)"
    echo "     - /phase5/diff (visual comparison)"
    echo "     - /phase5/workflows (git PRs)"
    echo "     - /phase5/templates (patterns)"
    echo "     - /phase5/deployment (production tools)"
    echo "     - /phase5/settings (configuration)"
    echo "     - /phase5/help (documentation)"
    echo ""
    echo "  4. Connect to backend:"
    echo "     Update API_BASE in components to point to your backend"
    echo ""
    echo "  5. Deploy to production"
else
    echo -e "${YELLOW}⚠️  Some files missing. Check the output above.${RESET}"
fi
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"