#!/usr/bin/env bash
set -euo pipefail

echo "=== TESTING NO RELATIONSHIP BETWEEN STEP2 AND MAIN.PY ==="
echo "Time: $(date)"
echo ""

# Test 1: Check if step2.py imports main
echo "=== TEST 1: Checking if step2.py imports main ==="
echo "Searching for 'import main' or 'from main' in step2.py..."
if grep -E "(import main|from main)" /root/6-4-2025/step2.py; then
    echo "❌ FOUND: step2.py imports main"
else
    echo "✅ PASS: step2.py does NOT import main"
fi

# Test 2: Check if step2.py references main.py in any way
echo ""
echo "=== TEST 2: Checking if step2.py references main.py ==="
echo "Searching for 'main.py' string in step2.py..."
if grep -n "main\.py" /root/6-4-2025/step2.py; then
    echo "❌ FOUND: step2.py references main.py"
else
    echo "✅ PASS: step2.py does NOT reference main.py"
fi

# Test 3: Check if main.py imports step2
echo ""
echo "=== TEST 3: Checking if main.py imports step2 ==="
echo "Searching for 'import step2' or 'from step2' in main.py..."
if grep -E "^[[:space:]]*(import step2|from step2)" /root/pretty_print/src/main.py; then
    echo "❌ FOUND: main.py imports step2"
else
    echo "✅ PASS: main.py does NOT import step2"
fi

# Test 4: Check if main.py references step2.py (the module)
echo ""
echo "=== TEST 4: Checking if main.py references step2.py module ==="
echo "Searching for 'step2' (excluding step2.json) in main.py..."
if grep -v "step2\.json" /root/pretty_print/src/main.py | grep -n "step2\.py"; then
    echo "❌ FOUND: main.py references step2.py module"
else
    echo "✅ PASS: main.py does NOT reference step2.py module"
fi

# Test 5: Verify main.py only reads step2.json (the data file)
echo ""
echo "=== TEST 5: Verifying main.py only reads step2.json ==="
echo "Searching for 'step2.json' references in main.py..."
grep -n "step2\.json" /root/pretty_print/src/main.py | head -5 || echo "No step2.json references found"

# Test 6: Check the actual pipeline flow
echo ""
echo "=== TEST 6: Verifying Pipeline Flow ==="
echo "Step 2 → Step 7 relationship:"
if grep -n "step7" /root/6-4-2025/step2.py | head -3; then
    echo "✅ Confirmed: step2.py calls step7"
else
    echo "❌ WARNING: step2.py doesn't seem to call step7"
fi

echo ""
echo "Step 7 → main.py relationship:"
if grep -n "main\.py" /root/6-4-2025/step7.py | head -3; then
    echo "✅ Confirmed: step7.py calls main.py"
else
    echo "❌ WARNING: step7.py doesn't seem to call main.py"
fi

# Summary
echo ""
echo "=== SUMMARY ==="
echo "Expected flow: step2.py → step7.py → main.py"
echo "Data flow: step2.py writes step2.json → main.py reads step2.json"
echo ""
echo "Relationship test results:"
echo "- step2.py ↔ main.py: Should have NO direct relationship (only via step7.py)"
echo "- main.py reads step2.json: OK (data file, not module import)"
echo ""
echo "Test complete!"
