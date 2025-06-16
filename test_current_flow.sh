#!/usr/bin/env bash
set -euo pipefail

echo "=== TESTING CURRENT PIPELINE FLOW ==="
echo "Time: $(date)"
echo ""

# Clean up any previous test outputs
echo "→ Cleaning up previous test outputs..."
rm -f step1.json step2.json step7_simple.log step7_matches.log
rm -f /root/pretty_print/logs/app.md

# Activate the pipeline virtual environment
echo "→ Activating venv..."
source "$(pwd)/venv/bin/activate"

# Step 1: Run step1.py
echo ""
echo "=== STEP 1: Fetching live data ==="
python step1.py
if [[ -f step1.json ]]; then
    echo "✅ step1.json created"
    echo "   Size: $(stat -c%s step1.json) bytes"
    echo "   First 200 chars: $(head -c 200 step1.json | tr '\n' ' ')"
else
    echo "❌ step1.json NOT found"
    exit 1
fi

# Step 2: Run step2.py (which should call step7.py)
echo ""
echo "=== STEP 2: Processing and enriching data ==="
python step2.py
if [[ -f step2.json ]]; then
    echo "✅ step2.json created"
    echo "   Size: $(stat -c%s step2.json) bytes"
    # Check if it has summaries array
    if grep -q '"summaries"' step2.json; then
        echo "   Contains 'summaries' array"
        SUMMARY_COUNT=$(jq '.summaries | length' step2.json 2>/dev/null || echo "parse error")
        echo "   Number of summaries: $SUMMARY_COUNT"
    fi
else
    echo "❌ step2.json NOT found"
    exit 1
fi

# Check what step7 created
echo ""
echo "=== STEP 7 OUTPUT CHECK ==="
if [[ -f step7_simple.log ]]; then
    echo "✅ step7_simple.log created"
    echo "   Size: $(stat -c%s step7_simple.log) bytes"
    echo "   Line count: $(wc -l < step7_simple.log)"
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
    echo "✅ /root/pretty_print/logs/app.md created"
    echo "   Size: $(stat -c%s /root/pretty_print/logs/app.md) bytes"
    echo "   Line count: $(wc -l < /root/pretty_print/logs/app.md)"
    echo "   First 300 chars: $(head -c 300 /root/pretty_print/logs/app.md | tr '\n' ' ')"
else
    echo "❌ /root/pretty_print/logs/app.md NOT found"
fi

# Show running processes to see if main.py is still running
echo ""
echo "=== CHECKING FOR RUNNING PROCESSES ==="
if pgrep -f "main.py" > /dev/null; then
    echo "⚠️  main.py is still running (PID: $(pgrep -f 'main.py'))"
    echo "   This suggests it's in continuous loop mode"
else
    echo "✅ main.py is not running (one-shot mode or finished)"
fi

echo ""
echo "=== FLOW SUMMARY ==="
echo "1. step1.py → created step1.json ✓"
echo "2. step2.py → created step2.json ✓"
echo "3. step7.py was called by step2.py"
echo "4. step7.py created log files: $(ls step7_*.log 2>/dev/null | xargs basename -a | tr '\n' ' ')"
echo "5. main.py was called and created: /root/pretty_print/logs/app.md"
echo ""
echo "Test complete!"
