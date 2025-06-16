#!/usr/bin/env python3
"""
STEP2 CLEAN MIRROR CREATOR - VS Code Safe Version
=================================================

Creates step2_mirror.json from step2_sample.json with proper structure and recent matches.
This provides a clean, safe version for VS Code viewing and data comparison.

Usage:
- Run manually: python3 create_clean_step2_mirror.py
- Auto-integrated with step2.py

Features:
- Uses step2_sample.json as clean source
- Extracts 5 most recent matches
- Preserves proper field structure
- Adds mirror metadata
- Safe for VS Code viewing
"""

import json
import os
from datetime import datetime
import pytz
from pathlib import Path

# Constants
STEP2_SAMPLE_PATH = "/root/6-4-2025/step2_sample.json"
MIRROR_JSON_PATH = "/root/6-4-2025/step2_mirror.json"
TZ = pytz.timezone("America/New_York")

def create_clean_step2_mirror():
    """
    Create a clean mirror from step2_sample.json with last 5 matches.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if step2_sample.json exists
        if not os.path.exists(STEP2_SAMPLE_PATH):
            print(f"❌ {STEP2_SAMPLE_PATH} not found")
            return False
        
        # Read step2_sample.json
        print(f"📖 Reading {STEP2_SAMPLE_PATH}...")
        with open(STEP2_SAMPLE_PATH, 'r', encoding='utf-8') as f:
            sample_data = json.load(f)
        
        # Extract matches from sample data
        if "first_5_matches" in sample_data:
            matches = sample_data["first_5_matches"]
            source_info = "first_5_matches from sample"
        elif "summaries" in sample_data:
            matches = sample_data["summaries"][:5]  # Take first 5
            source_info = "summaries from sample"
        else:
            print("❌ No matches found in step2_sample.json")
            return False
        
        total_in_sample = sample_data.get("total_matches", len(matches))
        
        # Create clean mirror structure
        mirror_data = {
            "mirror_info": {
                "created_at": datetime.now(TZ).strftime("%m/%d/%Y %I:%M:%S %p %Z"),
                "source_file": STEP2_SAMPLE_PATH,
                "source_info": source_info,
                "total_matches_in_source": total_in_sample,
                "matches_in_mirror": len(matches),
                "mirror_purpose": "Clean version for VS Code viewing and data comparison",
                "note": "Generated from step2_sample.json - shows proper data structure",
                "last_updated": datetime.now(TZ).isoformat()
            },
            "summaries": matches,
            "metadata": {
                "source": "step2_sample.json",
                "extraction_method": "clean_sample_extraction",
                "timestamp": datetime.now(TZ).isoformat(),
                "sample_total_matches": total_in_sample
            }
        }
        
        # Add sample data info if available
        if "total_matches" in sample_data:
            mirror_data["sample_statistics"] = {
                "total_matches_in_full_dataset": sample_data["total_matches"],
                "matches_shown": len(matches),
                "data_date": sample_data.get("date", "Unknown")
            }
        
        # Write mirror file
        print(f"✍️ Writing clean mirror with {len(matches)} matches to {MIRROR_JSON_PATH}...")
        with open(MIRROR_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(mirror_data, f, indent=2, ensure_ascii=False)
        
        # Get file sizes for comparison
        sample_size = os.path.getsize(STEP2_SAMPLE_PATH)
        mirror_size = os.path.getsize(MIRROR_JSON_PATH)
        
        print(f"✅ Clean mirror created successfully!")
        print(f"   📊 Sample: {sample_size:,} bytes ({total_in_sample} total matches)")
        print(f"   🪞 Mirror: {mirror_size:,} bytes ({len(matches)} matches shown)")
        print(f"   💎 Structure: Clean and VS Code safe")
        
        # Show sample of match data
        if matches:
            sample_match = matches[0]
            print(f"   📋 Sample match: {sample_match.get('home', 'Unknown')} vs {sample_match.get('away', 'Unknown')}")
            print(f"      Status: {sample_match.get('status_id', 'Unknown')} | Competition: {sample_match.get('competition', 'Unknown')}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {STEP2_SAMPLE_PATH}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating clean mirror: {e}")
        return False

def main():
    """Main entry point for standalone execution."""
    print("STEP2 CLEAN MIRROR CREATOR")
    print("=" * 40)
    
    success = create_clean_step2_mirror()
    
    if success:
        print(f"\n🎉 Clean mirror available at: {MIRROR_JSON_PATH}")
        print("💡 This file shows proper step2.json structure and is safe for VS Code")
        print("🔧 Use this for data comparison and debugging")
    else:
        print("\n❌ Failed to create clean mirror")
    
    return success

if __name__ == "__main__":
    main()