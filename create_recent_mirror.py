#!/usr/bin/env python3
"""
Create recent_fetches.json - A mirror of step1.json structure but only last 3 fetches
"""

import json
import os
from datetime import datetime
import pytz
from collections import deque

RECENT_FETCHES_FILE = "step1_mirror.json"
MAX_FETCHES = 3

def create_or_update_recent_fetches(new_data):
    """
    Create or update recent_fetches.json with the new fetch data
    Maintains only the last 3 fetches in the same structure as step1.json
    """
    
    # Load existing recent fetches or create new structure
    if os.path.exists(RECENT_FETCHES_FILE):
        try:
            with open(RECENT_FETCHES_FILE, 'r') as f:
                recent_data = json.load(f)
        except:
            recent_data = {"recent_fetches": [], "metadata": {}}
    else:
        recent_data = {"recent_fetches": [], "metadata": {}}
    
    # Get current NY time
    ny_tz = pytz.timezone("America/New_York")
    current_time = datetime.now(ny_tz)
    
    # Create fetch entry with same structure as step1.json
    fetch_entry = {
        "fetch_timestamp": new_data.get("timestamp", current_time.isoformat()),
        "ny_timestamp": new_data.get("ny_timestamp", current_time.strftime('%m/%d/%Y %I:%M:%S %p')),
        "live_matches": new_data.get("live_matches", {}),
        "team_info": new_data.get("team_info", {}),
        "competition_info": new_data.get("competition_info", {}),
        "countries": new_data.get("countries", {}),
        "unified_status_summary": new_data.get("unified_status_summary", {}),
        "detailed_status_mapping": new_data.get("detailed_status_mapping", {}),
        "comprehensive_match_breakdown": new_data.get("comprehensive_match_breakdown", {}),
        "step1_completion_summary": new_data.get("step1_completion_summary", {})
    }
    
    # Add to recent fetches (maintain only last 3)
    recent_data["recent_fetches"].append(fetch_entry)
    
    # Keep only last 3 fetches
    if len(recent_data["recent_fetches"]) > MAX_FETCHES:
        recent_data["recent_fetches"] = recent_data["recent_fetches"][-MAX_FETCHES:]
    
    # Update metadata
    recent_data["metadata"] = {
        "description": "Mirror of step1.json structure containing only the last 3 live fetches",
        "total_fetches_stored": len(recent_data["recent_fetches"]),
        "max_fetches": MAX_FETCHES,
        "last_updated": current_time.isoformat(),
        "last_updated_ny": current_time.strftime('%m/%d/%Y %I:%M:%S %p (NYT)'),
        "file_purpose": "Lightweight version for VS Code viewing without memory issues",
        "source": "Generated from step1.json data"
    }
    
    # Calculate summary stats across all recent fetches
    total_matches = 0
    total_teams = 0
    total_competitions = 0
    
    for fetch in recent_data["recent_fetches"]:
        if "live_matches" in fetch and "results" in fetch["live_matches"]:
            total_matches += len(fetch["live_matches"]["results"])
        total_teams += len(fetch.get("team_info", {}))
        total_competitions += len(fetch.get("competition_info", {}))
    
    recent_data["summary_across_fetches"] = {
        "total_matches_across_fetches": total_matches,
        "total_unique_teams": total_teams,
        "total_unique_competitions": total_competitions,
        "avg_matches_per_fetch": round(total_matches / len(recent_data["recent_fetches"]), 2) if recent_data["recent_fetches"] else 0
    }
    
    # Save updated recent fetches
    with open(RECENT_FETCHES_FILE, 'w') as f:
        json.dump(recent_data, f, indent=2)
    
    return len(recent_data["recent_fetches"])

def update_from_step1():
    """Update recent_fetches.json from current step1.json"""
    if not os.path.exists("step1.json"):
        print("❌ step1.json not found")
        return False
    
    try:
        print("📖 Reading step1.json...")
        with open("step1.json", 'r') as f:
            step1_data = json.load(f)
        
        print("🔄 Updating step1_mirror.json...")
        fetch_count = create_or_update_recent_fetches(step1_data)
        
        # Get file sizes for comparison
        step1_size = os.path.getsize("step1.json") / (1024*1024)  # MB
        recent_size = os.path.getsize(RECENT_FETCHES_FILE) / 1024  # KB
        
        print(f"✅ Updated step1_mirror.json")
        print(f"📊 Contains {fetch_count} recent fetches")
        print(f"📏 Size comparison:")
        print(f"   step1.json: {step1_size:.1f}MB")
        print(f"   step1_mirror.json: {recent_size:.1f}KB")
        print(f"🎯 Safe to open step1_mirror.json in VS Code!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating recent fetches: {e}")
        return False

if __name__ == "__main__":
    update_from_step1()