#!/bin/bash
# 🔮 IRONCLAD START HERE - Ice-ninja Edition
# Run this to see your complete Ironclad system in action

echo "🔮 Ironclad Hybrid Architecture"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Quick validation
services=$(ls backend/src/services/ 2>/dev/null | grep -E "(Bead|Archivist|Smart|Time|Collab)" | wc -l)
docs=$(ls *.md 2>/dev/null | grep -E "(QUICK|PHASE3|ACTION|ICE-NINJA)" | wc -l)
scripts=$(ls *.ts 2>/dev/null | grep -E "(bead|ironclad|phase3|test)" | wc -l)

echo "📊 System Status:"
echo "   Services: $services/9 ✅"
echo "   Docs:     $docs/8 ✅"
echo "   Scripts:  $scripts/4 ✅"
echo ""

if [ $services -lt 9 ] || [ $docs -lt 8 ] || [ $scripts -lt 4 ]; then
    echo "❌ Incomplete installation"
    echo "   Please ensure all Phase 3 files are present"
    exit 1
fi

echo "🚀 NEXT STEP: Choose Your Path"
echo ""
echo "1️⃣  DEMO MODE (30 seconds)"
echo "   bun run phase3-demo.ts"
echo "   → Shows: Bead creation, Git context, Time-travel, Review"
echo ""
echo "2️⃣  TEST MODE (1 minute)"
echo "   bun run test-ironclad.ts"
echo "   → Validates: All 6 systems"
echo ""
echo "3️⃣  SETUP MODE (2 minutes)"
echo "   bun run bead-init.ts"
echo "   → Creates: .beads/, types, gitignore"
echo ""
echo "4️⃣  INTEGRATION MODE"
echo "   Read: IRONCLAD_ACTION_PLAN.md"
echo "   → Step-by-step SAM integration"
echo ""
echo "5️⃣  DOCUMENTATION MODE"
echo "   Read: ICE-NINJA_FINAL_SUMMARY.md"
echo "   → Complete architecture overview"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 TIP: Start with #1 to see the magic!"
echo ""
read -p "Choose [1-5] or Enter to demo: " choice

case $choice in
    1|"" ) echo "Running demo..." && bun run phase3-demo.ts ;;
    2    ) echo "Running tests..." && bun run test-ironclad.ts ;;
    3    ) echo "Initializing..." && bun run bead-init.ts ;;
    4    ) echo "Opening action plan..." && cat IRONCLAD_ACTION_PLAN.md ;;
    5    ) echo "Opening summary..." && cat ICE-NINJA_FINAL_SUMMARY.md ;;
    *    ) echo "Invalid choice" ;;
esac