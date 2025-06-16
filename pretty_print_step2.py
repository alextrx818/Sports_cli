#!/usr/bin/env python3
"""
PRETTY PRINT STEP2.JSON
=======================
Convert step2.json into human-readable format
"""

import json
from datetime import datetime

def pretty_print_step2():
    """Pretty print step2.json in human readable format"""
    
    try:
        with open('/root/6-4-2025/step2.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading step2.json: {e}")
        return

    summaries = data.get('summaries', [])
    
    print("=" * 80)
    print("📋 STEP2.JSON PRETTY PRINT")
    print("=" * 80)
    print(f"📊 Total Matches: {len(summaries)}")
    print(f"🕒 Data Source: step2.json")
    print("=" * 80)
    
    for i, match in enumerate(summaries, 1):
        print(f"\n🏆 MATCH #{i}")
        print("-" * 50)
        
        # Basic match info
        home = match.get('home', 'Unknown')
        away = match.get('away', 'Unknown')
        competition = match.get('competition', 'Unknown')
        country = match.get('country', 'Unknown')
        score = match.get('score', '0-0')
        status_id = match.get('status_id', 0)
        
        print(f"🏠 HOME: {home}")
        print(f"✈️  AWAY: {away}")
        print(f"⚽ SCORE: {score}")
        print(f"🏆 COMPETITION: {competition}")
        print(f"🌍 COUNTRY: {country}")
        print(f"📊 STATUS ID: {status_id}")
        
        # Betting odds summary
        ml_american = match.get('money_line_american', [])
        spread_american = match.get('spread_american', [])
        ou_american = match.get('over_under_american', [])
        corners_american = match.get('corners_american', [])
        
        print(f"\n💰 BETTING ODDS:")
        print(f"   Money Line: {len(ml_american)} entries")
        print(f"   Spread: {len(spread_american)} entries") 
        print(f"   Over/Under: {len(ou_american)} entries")
        print(f"   🎯 Corners: {len(corners_american)} entries")
        
        # Show latest corners if available
        if corners_american:
            latest = corners_american[-1]
            if len(latest) >= 5:
                time_minute = latest[1]
                over_odds = latest[2]
                line = latest[3]
                under_odds = latest[4]
                print(f"   📍 Latest Corners: Over {over_odds} | Line {line} | Under {under_odds} (@{time_minute}')")
        
        # Environment data
        env = match.get('environment', {})
        if env:
            temp = env.get('temperature', '')
            weather = env.get('weather', '')
            wind = env.get('wind_speed', '')
            
            if temp or weather or wind:
                print(f"\n🌤️  ENVIRONMENT:")
                if weather:
                    print(f"   Weather: {weather}")
                if temp:
                    print(f"   Temperature: {temp}")
                if wind:
                    print(f"   Wind: {wind}")
        
        # Separator for readability
        if i < len(summaries):
            print("\n" + "="*80)
        
        # Limit output to first 10 matches for readability
        if i >= 10:
            remaining = len(summaries) - 10
            if remaining > 0:
                print(f"\n... and {remaining} more matches")
            break

def main():
    """Main function"""
    pretty_print_step2()
    
    print(f"\n🔍 For full JSON structure, use:")
    print(f"   python3 -m json.tool /root/6-4-2025/step2.json | head -100")

if __name__ == "__main__":
    main()