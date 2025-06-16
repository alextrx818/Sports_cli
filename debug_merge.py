#!/usr/bin/env python3

import json
import sys
sys.path.append('/root/6-4-2025')
import step2

# Load step1 data
with open('/root/6-4-2025/step1.json', 'r') as f:
    step1_data = json.load(f)

# Test full merge process
live_matches = step1_data.get("live_matches", {})
payload_data = {k: v for k, v in step1_data.items() if k != "live_matches"}

print("Testing merge_and_summarize function:")
print("Live matches count:", len(live_matches.get('results', [])))
print("Payload data keys:", list(payload_data.keys()))

# Test merge_and_summarize
merged_data = step2.merge_and_summarize(live_matches, payload_data)

print("Merged data structure:")
print("Total summaries:", len(merged_data.get('summaries', [])))

# Check first summary
summaries = merged_data.get('summaries', [])
if summaries:
    first_summary = summaries[0]
    print("First summary:")
    print("  Home:", first_summary.get('home'))
    print("  Away:", first_summary.get('away'))
    print("  Competition:", first_summary.get('competition'))
    print("  Odds:", bool(first_summary.get('odds')))
    print("  Environment:", first_summary.get('environment'))
