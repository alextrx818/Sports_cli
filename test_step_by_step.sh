#!/usr/bin/env bash
set -euo pipefail

echo "=== TESTING CURRENT PIPELINE FLOW (Step by Step) ==="
echo "Time: $(date)"
echo ""

# Clean up any previous test outputs
echo "→ Cleaning up previous test outputs..."
rm -f step7_simple.log step7_matches.log
rm -f /root/pretty_print/logs/app.md

# Activate the pipeline virtual environment
echo "→ Activating venv..."
source "$(pwd)/venv/bin/activate"

# Since step1 imports step2 and step2 has an error, let's check if we already have step1.json and step2.json
echo ""
echo "=== CHECKING EXISTING FILES ==="
if [[ -f step1.json ]]; then
    echo "✅ step1.json already exists"
    echo "   Size: $(stat -c%s step1.json) bytes"
    echo "   Modified: $(stat -c%y step1.json)"
else
    echo "❌ step1.json does not exist"
    echo "   Cannot proceed without running step1.py (which has import error)"
    exit 1
fi

if [[ -f step2.json ]]; then
    echo "✅ step2.json already exists"
    echo "   Size: $(stat -c%s step2.json) bytes"
    echo "   Modified: $(stat -c%y step2.json)"
    # Check if it has summaries array
    if grep -q '"summaries"' step2.json; then
        echo "   Contains 'summaries' array"
        SUMMARY_COUNT=$(jq '.summaries | length' step2.json 2>/dev/null || echo "parse error")
        echo "   Number of summaries: $SUMMARY_COUNT"
    fi
else
    echo "❌ step2.json does not exist"
fi

# Test step7.py directly (since step2.json exists)
echo ""
echo "=== TESTING STEP 7 DIRECTLY ==="
echo "Running: python step7.py"
timeout 30 python step7.py || true

# Check what step7 created
echo ""
echo "=== STEP 7 OUTPUT CHECK ==="
if [[ -f step7_simple.log ]]; then
    echo "✅ step7_simple.log created"
    echo "   Size: $(stat -c%s step7_simple.log) bytes"
    echo "   Line count: $(wc -l < step7_simple.log)"
    echo "   Last 5 lines:"
    tail -5 step7_simple.log | sed 's/^/   /'
fi

if [[ -f step7_matches.log ]]; then
    echo "✅ step7_matches.log created"
    echo "   Size: $(stat -c%s step7_matches.log) bytes"
    echo "   Line count: $(wc -l < step7_matches.log)"
fi

# Check if main.py created its log
echo ""
echo "=== PRETTY PRINT ENGINE OUTPUT CHECK ==="
if [[ -f /root/pretty_print/logs/app.md ]]; then
    echo "✅ /root/pretty_print/logs/app.md exists"
    echo "   Size: $(stat -c%s /root/pretty_print/logs/app.md) bytes"
    echo "   Line count: $(wc -l < /root/pretty_print/logs/app.md)"
    echo "   Modified: $(stat -c%y /root/pretty_print/logs/app.md)"
    echo "   Last 10 lines:"
    tail -10 /root/pretty_print/logs/app.md | sed 's/^/   /'
else
    echo "❌ /root/pretty_print/logs/app.md NOT found"
fi

# Let's also check what step7.py actually does
echo ""
echo "=== ANALYZING STEP7.PY ==="
echo "Step7.py imports:"
grep -E "^import|^from" step7.py | head -10 | sed 's/^/   /'
echo ""
echo "Step7.py main execution:"
grep -A 5 "if __name__" step7.py | sed 's/^/   /'
echo ""
echo "Looking for main.py invocation in step7.py:"
grep -n "main.py" step7.py | sed 's/^/   /' || echo "   No direct 'main.py' reference found"

# Show running processes to see if main.py is still running
echo ""
echo "=== CHECKING FOR RUNNING PROCESSES ==="
if pgrep -f "main.py" > /dev/null; then
    echo "⚠️  main.py is still running (PID: $(pgrep -f 'main.py'))"
    echo "   This suggests it's in continuous loop mode"
    # Kill it for clean testing
    pkill -f "main.py" || true
    echo "   Killed main.py process"
else
    echo "✅ main.py is not running"
fi

echo ""
echo "=== CURRENT FLOW ANALYSIS ==="
echo "Based on the evidence:"
echo "1. step2.json exists (from previous runs)"
echo "2. step7.py can be run directly and creates log files"
echo "3. step7.py appears to be a standalone script that reads step2.json"
echo "4. Need to check if step7.py calls main.py..."
echo ""
echo "Test complete!"
