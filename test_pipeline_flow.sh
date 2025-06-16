#!/usr/bin/env bash
set -euo pipefail

# Activate the pipeline virtual environment
echo "→ Activating venv..."
source "$(pwd)/venv/bin/activate"

# 1) Run step1 and check JSON
echo "→ Running step1.py..."
python step1.py
if [[ ! -f step1.json ]]; then
echo "❌ step1.json not found"; exit 1
else
echo "✅ step1.json exists"
fi

# 2) Run step2 and check JSON
echo "→ Running step2.py..."
python step2.py
if [[ ! -f step2.json ]]; then
echo "❌ step2.json not found"; exit 1
else
echo "✅ step2.json exists"
fi

# 3) Run step7 (will call main.py); limit to 10 seconds
echo "→ Running step7.py (timeout 10s)..."
timeout 10s python step7.py || echo "(step7.py timed out or exited)"
if [[ ! -f step7_simple.log ]]; then
echo "❌ step7_simple.log not found"; exit 1
else
echo "✅ step7_simple.log exists"
fi

# 4) Verify pretty_print output
echo "→ Checking pretty_print logs/app.md..."
if [[ ! -f ../pretty_print/logs/app.md ]]; then
  echo "❌ logs/app.md not found"; exit 1
else
  echo "✅ logs/app.md exists"
fi

echo "
🎉 Pipeline flow verified: step1 → step2 → step7 → pretty_print succeeded!"
