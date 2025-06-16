#!/usr/bin/env python3

import json
import sys
sys.path.append('/root/6-4-2025')
import step2

print("=== TRACING STEP2 EXECUTION ===")

# Load step1 data exactly like step2.py does
step1_data = {}
with open('/root/6-4-2025/step1.json', 'r') as f:
    step1_data = json.load(f)

# Extract data exactly like step2.py does  
live_matches = step1_data.get("live_matches", {})
payload_data = {k: v for k, v in step1_data.items() if k != "live_matches"}

print(f"Live matches: {len(live_matches.get('results', []))}")
print(f"Payload keys: {list(payload_data.keys())}")

# Call merge_and_summarize exactly like step2.py does
merged_data = step2.merge_and_summarize(live_matches, payload_data)

print(f"Merged summaries count: {len(merged_data.get('summaries', []))}")

# Check first summary
summaries = merged_data.get("summaries", [])
if summaries:
    first = summaries[0]
    print(f"\nFirst summary:")
    print(f"  ID: {first.get('match_id')}")
    print(f"  Home: {first.get('home')}")
    print(f"  Away: {first.get('away')}")
    print(f"  Competition: {first.get('competition')}")
    print(f"  Odds: {len(first.get('odds', {}))}")
    print(f"  Environment: {first.get('environment')}")

# Now try to save it and see what happens
print(f"\nSaving to test_step2.json...")
test_output = "/root/6-4-2025/test_step2.json"
success = step2.save_match_summaries(merged_data, test_output)
print(f"Save success: {success}")

# Read back what was saved
if success:
    with open(test_output, 'r') as f:
        saved_data = json.load(f)
    
    saved_summaries = saved_data.get("summaries", [])
    if saved_summaries:
        saved_first = saved_summaries[0]
        print(f"\nSaved first summary:")
        print(f"  ID: {saved_first.get('match_id')}")
        print(f"  Home: {saved_first.get('home')}")
        print(f"  Away: {saved_first.get('away')}")
        print(f"  Competition: {saved_first.get('competition')}")
        print(f"  Odds: {len(saved_first.get('odds', {}))}")
        print(f"  Environment: {saved_first.get('environment')}")