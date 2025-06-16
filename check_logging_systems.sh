#!/usr/bin/env bash
set -euo pipefail

echo "=== ANALYZING DIFFERENT LOGGING SYSTEMS ==="
echo ""

# Check step2.py logging
echo "=== STEP2.PY LOGGING ==="
echo "1. Uses Python's logging module:"
grep -n "import logging\|logging\." /root/6-4-2025/step2.py | head -5

echo ""
echo "2. Logs to files:"
grep -n "logging\.FileHandler\|\.log" /root/6-4-2025/step2.py | head -5 || echo "No file handlers found in step2.py"

# Check step7.py logging
echo ""
echo "=== STEP7.PY LOGGING ==="
echo "1. Log files created:"
grep -n "\.log" /root/6-4-2025/step7.py | grep -v "logger" | head -5

echo ""
echo "2. Direct file writes:"
grep -n "open.*log.*w" /root/6-4-2025/step7.py | head -5

# Check main.py logging
echo ""
echo "=== MAIN.PY (PRETTY PRINT) LOGGING ==="
echo "1. Custom logger:"
grep -n "get_md_logger\|MdLogger" /root/pretty_print/src/main.py | head -5

echo ""
echo "2. Markdown log files:"
grep -n "\.md\|markdown" /root/pretty_print/src/main.py | head -5

echo ""
echo "=== SUMMARY OF LOGGING RESPONSIBILITIES ==="
echo "- step2.py: Standard Python logging for processing steps (console output)"
echo "- step7.py: Creates step7_simple.log and step7_matches.log with formatted match data"
echo "- main.py: Creates markdown reports in logs/*.md for pretty-printed output"
echo ""
echo "Each component has its OWN logging system for different purposes!"
