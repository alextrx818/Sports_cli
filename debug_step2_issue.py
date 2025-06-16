#!/usr/bin/env python3

import json

# Load current step1.json
with open('/root/6-4-2025/step1.json', 'r') as f:
    step1_data = json.load(f)

print("=== DEBUGGING STEP2 ISSUE ===")
print()

# Check the structure
live_matches = step1_data.get("live_matches", {})
matches = live_matches.get("results", [])
match_details = step1_data.get("match_details", {})
team_info = step1_data.get("team_info", {})
competition_info = step1_data.get("competition_info", {})

print(f"Live matches count: {len(matches)}")
print(f"Match details count: {len(match_details)}")
print(f"Team info count: {len(team_info)}")
print(f"Competition info count: {len(competition_info)}")
print()

# Check first match in detail
if matches and len(matches) > 0:
    first_match = matches[0]
    match_id = first_match.get("id")
    print(f"First match ID: {match_id}")
    print()
    
    # Check if this match ID exists in match_details
    if match_id in match_details:
        print("✅ Match ID found in match_details")
        detail = match_details[match_id]
        if detail.get("code") == 0 and "results" in detail:
            print("✅ Match detail has valid results")
            result = detail["results"][0]
            home_team_id = result.get("home_team_id")
            away_team_id = result.get("away_team_id")
            competition_id = result.get("competition_id")
            
            print(f"Home team ID: {home_team_id}")
            print(f"Away team ID: {away_team_id}")
            print(f"Competition ID: {competition_id}")
            print()
            
            # Check team info lookup
            if home_team_id in team_info:
                print("✅ Home team ID found in team_info")
                home_info = team_info[home_team_id]
                if home_info.get("code") == 0 and "results" in home_info:
                    home_name = home_info["results"][0].get("name")
                    print(f"Home team name: {home_name}")
                else:
                    print("❌ Home team info has invalid structure")
            else:
                print("❌ Home team ID NOT found in team_info")
                print(f"Available team IDs (first 5): {list(team_info.keys())[:5]}")
            
            if away_team_id in team_info:
                print("✅ Away team ID found in team_info")
                away_info = team_info[away_team_id]
                if away_info.get("code") == 0 and "results" in away_info:
                    away_name = away_info["results"][0].get("name")
                    print(f"Away team name: {away_name}")
                else:
                    print("❌ Away team info has invalid structure")
            else:
                print("❌ Away team ID NOT found in team_info")
            
            # Check competition info
            if competition_id in competition_info:
                print("✅ Competition ID found in competition_info")
                comp_info = competition_info[competition_id]
                if comp_info.get("code") == 0 and "results" in comp_info:
                    comp_name = comp_info["results"][0].get("name")
                    print(f"Competition name: {comp_name}")
                else:
                    print("❌ Competition info has invalid structure")
            else:
                print("❌ Competition ID NOT found in competition_info")
                print(f"Available competition IDs (first 5): {list(competition_info.keys())[:5]}")
        else:
            print("❌ Match detail has invalid structure")
    else:
        print("❌ Match ID NOT found in match_details")
        print(f"Available match detail IDs (first 5): {list(match_details.keys())[:5]}")
else:
    print("❌ No matches found in live_matches")