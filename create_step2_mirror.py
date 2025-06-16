#!/usr/bin/env python3
"""
STEP2 MIRROR CREATOR - Lightweight Version for VS Code
=====================================================

Creates step2_mirror.json with only the last 5 matches to prevent VS Code crashes.
This allows for easy data comparison and debugging without loading massive files.

Usage:
- Run manually: python3 create_step2_mirror.py
- Auto-run: Called by step2.py after each successful save

Features:
- Extracts last 5 matches from step2.json
- Preserves metadata and structure
- Adds mirror-specific metadata
- Safe error handling
"""

import json
import os
from datetime import datetime
import pytz
from pathlib import Path

# Constants
STEP2_JSON_PATH = "/root/6-4-2025/step2.json"
MIRROR_JSON_PATH = "/root/6-4-2025/step2_mirror.json"
TZ = pytz.timezone("America/New_York")

def create_mirror_from_large_file():
    """
    Handle large/corrupted step2.json files by extracting structure safely.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print("🔧 Parsing large file safely...")
        
        # Read first 50 lines to get structure
        print("📖 Reading file beginning...")
        with open(STEP2_JSON_PATH, 'r', encoding='utf-8') as f:
            lines = []
            for i, line in enumerate(f):
                lines.append(line.strip())
                if i >= 50:  # Read first 50 lines
                    break
        
        # Look for summaries start
        summaries_start = None
        for i, line in enumerate(lines):
            if '"summaries":' in line:
                summaries_start = i
                break
        
        if summaries_start is None:
            print("❌ Could not find summaries in file")
            return False
        
        # Read last 500 lines to get recent matches and metadata
        print("📖 Reading file ending...")
        with open(STEP2_JSON_PATH, 'r', encoding='utf-8') as f:
            # Go to end and read backwards
            f.seek(0, 2)  # Go to end
            file_size = f.tell()
            
            # Read last chunk (500KB should be enough for metadata + last few matches)
            chunk_size = min(500000, file_size)
            f.seek(file_size - chunk_size)
            end_content = f.read()
        
        # Find the last complete match object and metadata
        lines = end_content.split('\n')
        
        # Create a minimal mirror with available data
        mirror_data = {
            "mirror_info": {
                "created_at": datetime.now(TZ).strftime("%m/%d/%Y %I:%M:%S %p %Z"),
                "source_file": STEP2_JSON_PATH,
                "file_size_bytes": os.path.getsize(STEP2_JSON_PATH),
                "parsing_method": "safe_large_file_extraction",
                "note": "Original file too large - showing structure only",
                "last_updated": datetime.now(TZ).isoformat()
            },
            "summaries": [
                {
                    "note": "Original file contains massive dataset",
                    "file_size_mb": round(os.path.getsize(STEP2_JSON_PATH) / 1024 / 1024, 1),
                    "estimated_matches": "Unknown (file too large to parse)",
                    "suggestion": "Use step2_sample.json for testing or regenerate step2.json"
                }
            ],
            "metadata": {
                "source": "step2.py",
                "extraction_method": "safe_parsing",
                "timestamp": datetime.now(TZ).isoformat()
            }
        }
        
        # Try to extract any completion summary from the end
        end_text = '\n'.join(lines[-50:])  # Last 50 lines
        if 'completion_summary' in end_text:
            print("📋 Found completion summary in file end")
            mirror_data["original_completion_found"] = True
        
        # Write mirror file
        print(f"✍️ Writing safe mirror to {MIRROR_JSON_PATH}...")
        with open(MIRROR_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(mirror_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Safe mirror created!")
        print(f"   ⚠️ Original file is {round(os.path.getsize(STEP2_JSON_PATH) / 1024 / 1024, 1)}MB - too large for safe parsing")
        print(f"   💡 Consider regenerating step2.json or using step2_sample.json for testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in safe parsing: {e}")
        return False

def create_step2_mirror():
    """
    Create a lightweight mirror of step2.json with only the last 5 matches.
    Safely handles large/corrupted JSON files.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if step2.json exists
        if not os.path.exists(STEP2_JSON_PATH):
            print(f"❌ {STEP2_JSON_PATH} not found")
            return False
        
        # Check file size first
        file_size = os.path.getsize(STEP2_JSON_PATH)
        print(f"📊 step2.json size: {file_size:,} bytes")
        
        if file_size > 100_000_000:  # 100MB
            print("⚠️ File is very large, using safe parsing...")
            return create_mirror_from_large_file()
        
        # Read step2.json for normal sized files
        print(f"📖 Reading {STEP2_JSON_PATH}...")
        try:
            with open(STEP2_JSON_PATH, 'r', encoding='utf-8') as f:
                step2_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("🔧 Attempting to repair and extract data...")
            return create_mirror_from_large_file()
        
        # Extract summaries
        all_summaries = step2_data.get("summaries", [])
        total_matches = len(all_summaries)
        
        if total_matches == 0:
            print("⚠️ No summaries found in step2.json")
            return False
        
        # Take last 5 matches (or all if less than 5)
        last_5_summaries = all_summaries[-5:] if total_matches >= 5 else all_summaries
        mirror_count = len(last_5_summaries)
        
        # Create mirror structure
        mirror_data = {
            "mirror_info": {
                "created_at": datetime.now(TZ).strftime("%m/%d/%Y %I:%M:%S %p %Z"),
                "source_file": STEP2_JSON_PATH,
                "total_matches_in_source": total_matches,
                "matches_in_mirror": mirror_count,
                "mirror_purpose": "Lightweight version for VS Code viewing and debugging",
                "last_updated": datetime.now(TZ).isoformat()
            },
            "summaries": last_5_summaries,
            "metadata": step2_data.get("metadata", {}),
            "step2_processing_summary": step2_data.get("step2_processing_summary", {})
        }
        
        # Add source metadata if available
        if "step2_processing_summary" in step2_data:
            mirror_data["source_processing_info"] = {
                "original_processing_time": step2_data["step2_processing_summary"].get("processing_time", "Unknown"),
                "original_processed_at": step2_data["step2_processing_summary"].get("processed_at", "Unknown"),
                "original_total_matches": step2_data["step2_processing_summary"].get("total_matches_processed", "Unknown")
            }
        
        # Write mirror file
        print(f"✍️ Writing mirror with {mirror_count} matches to {MIRROR_JSON_PATH}...")
        with open(MIRROR_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(mirror_data, f, indent=2, ensure_ascii=False)
        
        # Get file sizes for comparison
        original_size = os.path.getsize(STEP2_JSON_PATH)
        mirror_size = os.path.getsize(MIRROR_JSON_PATH)
        
        print(f"✅ Mirror created successfully!")
        print(f"   📊 Original: {original_size:,} bytes ({total_matches} matches)")
        print(f"   🪞 Mirror: {mirror_size:,} bytes ({mirror_count} matches)")
        print(f"   💾 Size reduction: {((original_size - mirror_size) / original_size * 100):.1f}%")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {STEP2_JSON_PATH}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating mirror: {e}")
        return False

def create_or_update_step2_mirror():
    """
    Create or update the step2 mirror. Can be called from other modules.
    
    Returns:
        bool: True if successful, False otherwise
    """
    return create_step2_mirror()

def main():
    """Main entry point for standalone execution."""
    print("STEP2 MIRROR CREATOR")
    print("=" * 40)
    
    success = create_step2_mirror()
    
    if success:
        print(f"\n🎉 Mirror available at: {MIRROR_JSON_PATH}")
        print("💡 Use this file for VS Code viewing to prevent crashes")
    else:
        print("\n❌ Failed to create mirror")
    
    return success

if __name__ == "__main__":
    main()