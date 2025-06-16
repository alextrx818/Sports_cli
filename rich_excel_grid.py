#!/usr/bin/env python3
"""
Rich tables with Excel-like connected grid formatting for step7.py
"""

from rich.console import Console
from rich.table import Table
from rich import box
import json

# Load actual data
with open('step2.json', 'r') as f:
    data = json.load(f)

# Get a sample match with odds
sample_match = None
for match in data['summaries']:
    if match.get('money_line_american') or match.get('money_line'):
        sample_match = match
        break

# Helper function
def format_american_odds(value):
    if value is None:
        return "N/A"
    try:
        odds_int = int(value)
        return f"+{odds_int}" if odds_int > 0 else str(odds_int)
    except (ValueError, TypeError):
        return str(value)

# Extract match data
home = sample_match['home']
away = sample_match['away']
score = sample_match.get('score', 'N/A')
ht_score = sample_match.get('ht_score', '')
status_name = sample_match.get('status_name', 'Unknown')
status_id = sample_match.get('status_id', 0)

print("=" * 80)
print("RICH TABLES WITH EXCEL-LIKE CONNECTED GRIDS")
print("=" * 80)
print()

# Create different console configurations
color_console = Console()  # For terminal with colors
plain_console = Console(force_terminal=False, width=80)  # For log files

# Example 1: ASCII Box (Best for Log Files)
print("1. ASCII BOX - Perfect for Log Files")
print("-" * 50)
print(f"\nMatch: {home} vs. {away}")
print(f"Score: {score}" + (f" (HT:{ht_score})" if ht_score else ""))
print(f"Status: {status_name} (ID:{status_id})\n")

ascii_table = Table(box=box.ASCII, show_header=True, padding=(0, 1))
ascii_table.add_column("MARKET", width=12)
ascii_table.add_column("HOME", justify="center", width=14)
ascii_table.add_column("DRAW", justify="center", width=14)
ascii_table.add_column("AWAY", justify="center", width=14)

# Add odds data
money_line = sample_match.get("money_line_american") or sample_match.get("money_line", [])
spread = sample_match.get("spread_american") or sample_match.get("spread", [])
over_under = sample_match.get("over_under_american") or sample_match.get("over_under", [])

if money_line and len(money_line) > 0:
    latest = money_line[-1]
    if len(latest) >= 5:
        ascii_table.add_row(
            "Money Line",
            format_american_odds(latest[2]),
            format_american_odds(latest[3]),
            format_american_odds(latest[4])
        )

if spread and len(spread) > 0:
    latest = spread[-1]
    if len(latest) >= 5:
        ascii_table.add_row(
            "Spread",
            format_american_odds(latest[2]),
            f"Point: {latest[3]:+.2g}".rstrip('0').rstrip('.'),
            format_american_odds(latest[4])
        )

if over_under and len(over_under) > 0:
    latest = over_under[-1]
    if len(latest) >= 5:
        ascii_table.add_row(
            "O/U",
            f"Over: {format_american_odds(latest[2])}",
            f"Line: {latest[3]:.1f}",
            f"Under: {format_american_odds(latest[4])}"
        )

plain_console.print(ascii_table)

# Example 2: Square Box (Unicode Grid)
print("\n\n2. SQUARE BOX - Unicode Connected Grid")
print("-" * 50)

square_table = Table(
    title=f"{home} vs. {away}",
    box=box.SQUARE,
    show_header=True,
    padding=(0, 1)
)
square_table.add_column("MARKET", style="cyan", width=12)
square_table.add_column("HOME", style="green", justify="center", width=14)
square_table.add_column("DRAW", style="yellow", justify="center", width=14)
square_table.add_column("AWAY", style="red", justify="center", width=14)

# Add same data
if money_line and len(money_line) > 0:
    latest = money_line[-1]
    if len(latest) >= 5:
        square_table.add_row(
            "Money Line",
            format_american_odds(latest[2]),
            format_american_odds(latest[3]),
            format_american_odds(latest[4])
        )

if spread and len(spread) > 0:
    latest = spread[-1]
    if len(latest) >= 5:
        square_table.add_row(
            "Spread",
            format_american_odds(latest[2]),
            f"Point: {latest[3]:+.2g}".rstrip('0').rstrip('.'),
            format_american_odds(latest[4])
        )

if over_under and len(over_under) > 0:
    latest = over_under[-1]
    if len(latest) >= 5:
        square_table.add_row(
            "O/U",
            f"Over: {format_american_odds(latest[2])}",
            f"Line: {latest[3]:.1f}",
            f"Under: {format_american_odds(latest[4])}"
        )

color_console.print(square_table)

# Example 3: Complete Match Display for step7.py
print("\n\n3. COMPLETE MATCH DISPLAY (step7.py style)")
print("-" * 50)

# Match header (manual formatting)
print("\n+" + "-" * 78 + "+")
print(f"| {home} vs. {away:<{76 - len(home) - 5}} |")
print(f"| Score: {score}" + (f" (HT:{ht_score})" if ht_score else "") + " " * (68 - len(f"Score: {score}" + (f" (HT:{ht_score})" if ht_score else ""))) + " |")
print(f"| Status: {status_name} (ID:{status_id})" + " " * (68 - len(f"Status: {status_name} (ID:{status_id})")) + " |")

# Odds table using Rich
step7_table = Table(box=box.ASCII, show_header=True, padding=(0, 1), width=80)
step7_table.add_column("MARKET", width=14)
step7_table.add_column("HOME", justify="center", width=14)
step7_table.add_column("DRAW", justify="center", width=14)
step7_table.add_column("AWAY", justify="center", width=14)

if money_line and len(money_line) > 0:
    latest = money_line[-1]
    if len(latest) >= 5:
        step7_table.add_row(
            "Money Line",
            format_american_odds(latest[2]),
            format_american_odds(latest[3]),
            format_american_odds(latest[4])
        )

if spread and len(spread) > 0:
    latest = spread[-1]
    if len(latest) >= 5:
        step7_table.add_row(
            "Spread",
            format_american_odds(latest[2]),
            f"Point: {latest[3]:+.2g}".rstrip('0').rstrip('.'),
            format_american_odds(latest[4])
        )

if over_under and len(over_under) > 0:
    latest = over_under[-1]
    if len(latest) >= 5:
        step7_table.add_row(
            "O/U",
            f"Over: {format_american_odds(latest[2])}",
            f"Line: {latest[3]:.1f}",
            f"Under: {format_american_odds(latest[4])}"
        )

plain_console.print(step7_table)

# Weather info
env = sample_match.get("environment", {})
weather = env.get("weather", "N/A")
temp = env.get("temperature", "N/A")
wind = env.get("wind_speed", "N/A")
print(f"Weather: {weather}  ·  Temp: {temp}  ·  Wind: {wind}")

# Example 4: Comparison of Box Styles
print("\n\n4. BOX STYLE COMPARISON")
print("-" * 50)

styles = [
    ("ASCII (Best for logs)", box.ASCII),
    ("SQUARE (Clean Unicode)", box.SQUARE),
    ("HEAVY (Bold Unicode)", box.HEAVY),
    ("DOUBLE (Double lines)", box.DOUBLE),
]

for name, style in styles:
    print(f"\n{name}:")
    demo = Table(box=style, show_header=True, padding=(0, 1))
    demo.add_column("TYPE", width=10)
    demo.add_column("HOME", width=10, justify="center")
    demo.add_column("AWAY", width=10, justify="center")
    demo.add_row("ML", "+150", "-120")
    demo.add_row("Spread", "+2.5", "-2.5")
    plain_console.print(demo)

# Example 5: How to integrate into step7.py
print("\n\n5. INTEGRATION CODE FOR STEP7.PY")
print("-" * 50)
print("""
To integrate Rich into step7.py:

1. Import Rich:
   from rich.console import Console
   from rich.table import Table
   from rich import box

2. Create a plain console for log output:
   console = Console(force_terminal=False, width=80)

3. Replace the manual odds table formatting with:
   
   odds_table = Table(box=box.ASCII, show_header=True, padding=(0, 1))
   odds_table.add_column("MARKET", width=14)
   odds_table.add_column("HOME", justify="center", width=14)
   odds_table.add_column("DRAW", justify="center", width=14)
   odds_table.add_column("AWAY", justify="center", width=14)
   
   # Add rows...
   odds_table.add_row("Money Line", home_odds, draw_odds, away_odds)
   
   # Print to logger
   for line in console.capture().splitlines():
       logger.info(line)

Benefits:
- Automatic column width calculation
- Consistent formatting
- Easy to maintain
- Handles long text gracefully
""")
