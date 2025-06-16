#!/usr/bin/env python3

import json
import sys
sys.path.append('/root/6-4-2025')
import step2

# Load step1 data
with open('/root/6-4-2025/step1.json', 'r') as f:
    step1_data = json.load(f)

# Test extraction
live_matches = step1_data.get('live_matches', {})
payload_data = {k: v for k, v in step1_data.items() if k != 'live_matches'}

print('Live matches structure:', live_matches.get('code'), len(live_matches.get('results', [])))
print('Payload data keys:', list(payload_data.keys()))

# Test first match
matches = live_matches.get('results', [])
if matches:
    first_match = matches[0]
    match_id = first_match.get('id')
    print('First match ID:', match_id)
    
    # Check if match_details has this ID
    match_details = payload_data.get('match_details', {})
    print('Match details has this ID:', match_id in match_details)
    
    if match_id in match_details:
        detail = match_details[match_id]
        print('Match detail structure:', detail.get('code'), len(detail.get('results', [])))
        if detail.get('results'):
            match_detail = detail['results'][0]
            print('Home team ID:', match_detail.get('home_team_id'))
            print('Away team ID:', match_detail.get('away_team_id'))
            print('Competition ID:', match_detail.get('competition_id'))
    
    # Test the extraction function
    summary = step2.extract_summary_fields(first_match, match_details, payload_data.get('team_info', {}), payload_data.get('competition_info', {}))
    print('Extracted summary for first match:')
    print('  Home:', summary.get('home'))
    print('  Away:', summary.get('away'))
    print('  Competition:', summary.get('competition'))