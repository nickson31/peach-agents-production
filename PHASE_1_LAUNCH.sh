#!/bin/bash

echo "════════════════════════════════════════════════════════════════"
echo "🚀 PHASE 1 LAUNCH - TEST MODE ACTIVATED"
echo "════════════════════════════════════════════════════════════════"
date
echo ""

# Start ORDER_ANALYZER in background (every 60 seconds)
echo "🔍 Activating ORDER_ANALYZER (every 60 sec)..."
nohup python3 ORDER_ANALYZER_LIVE.py > ORDER_ANALYZER_PHASE1.log 2>&1 &
ANALYZER_PID=$!
echo "✓ ORDER_ANALYZER started (PID: $ANALYZER_PID)"
echo ""

# Store PIDs for tracking
echo "$ANALYZER_PID" > PHASE_1_ANALYZER.pid

# Create Phase 1 deployment report
cat > PHASE_1_REPORT.md <<'REPORT'
# PHASE 1 DEPLOYMENT REPORT - TEST MODE

**Start**: 2026-03-20 10:33 UTC
**Phase**: 1 (Initial test with 2-5 orders)
**Goal**: Measure fill rate, BP efficiency, stuck order management

## Summary (updates every 30 min)

| Time | Deployed | Filled | %Fill | Stuck | Avg Time | BP Blocked | BP Remain | Status |
|------|----------|--------|-------|-------|----------|-----------|----------|--------|
| 10:33 | STARTING | - | - | - | - | - | - | ⏳ |

REPORT

echo "✓ Phase 1 report created"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo "🟢 PHASE 1 LIVE - TEST MODE ACTIVE"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "What's running:"
echo "  ✓ ORDER_ANALYZER - Monitoring stuck orders every 60 sec"
echo "  ✓ First batch - 2-5 orders deploying"
echo "  ✓ Reporting - Every 30 min with metrics"
echo ""
echo "Critical monitoring:"
echo "  - Watch fill rate (target: >85%)"
echo "  - Watch for stuck orders (should be canceled at 10 min)"
echo "  - Watch BP remaining"
echo ""
echo "Next decision point: After 2 hours of test data"
echo ""
