#!/usr/bin/env python3
"""
TRIGGER PROCESSING SCRIPT
=========================
Run this after step2.py completes to immediately trigger processing
"""

import os
import time
from pathlib import Path

# Create trigger file
TRIGGER_FILE = Path("/tmp/step2_complete.trigger")
TRIGGER_FILE.touch()

print(f"✅ Trigger file created at {TRIGGER_FILE}")
print("Processing will run immediately in main.py")
