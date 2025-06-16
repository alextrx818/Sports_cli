#!/usr/bin/env python3
"""
TEST PIPELINE WORKFLOW
======================
Simulates step2 -> step7 -> logging workflow
"""

import os
import sys
import json
import time
from pathlib import Path
import subprocess

# Configuration
STEP2_JSON = "/root/6-4-2025/step2.json"
PRETTY_PRINT_DIR = "/root/pretty_print"

# Simulate step2 writing data
def simulate_step2():
    print("🔧 Simulating step2 data creation...")
    data = {
        "summaries": [
            {
                "match_id": "test123",
                "home": "Test Team A",
                "away": "Test Team B",
                "score": "2-1",
                "status": "Completed",
                "competition": "Test League"
            }
        ]
    }
    
    with open(STEP2_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Test data written to {STEP2_JSON}")

# Simulate step7 execution
def run_step7():
    print("🔧 Running step7...")
    try:
        # Run step7.py
        result = subprocess.run(
            [sys.executable, "/root/6-4-2025/step7.py"],
            capture_output=True,
            text=True
        )
        print(f"🚀 step7 output:\n{result.stdout}")
        if result.stderr:
            print(f"⚠️ step7 errors:\n{result.stderr}")
        return True
    except Exception as e:
        print(f"❌ Error running step7: {e}")
        return False

# Check log file
def check_logs():
    log_path = Path("/root/pretty_print/logs/app.md")
    print(f"🔍 Checking log file: {log_path}")
    
    if not log_path.exists():
        print("❌ Log file not found!")
        return
        
    content = log_path.read_text(encoding="utf-8")
    print(f"📝 Log content:\n{content}")
    
    if "Test Team A" in content and "Test Team B" in content:
        print("✅ Test data found in logs!")
    else:
        print("❌ Test data not found in logs")

if __name__ == "__main__":
    # Clean previous test data
    if Path(STEP2_JSON).exists():
        Path(STEP2_JSON).unlink()
    
    # Run test workflow
    simulate_step2()
    time.sleep(1)  # Brief pause
    
    if run_step7():
        time.sleep(2)  # Allow time for processing
        check_logs()
    else:
        print("❌ Pipeline test failed at step7")
    
    print("\nTest completed!")
