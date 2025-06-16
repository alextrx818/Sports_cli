#!/usr/bin/env python3
"""
Examples of Rich tables with fully connected grid lines like Excel
"""

from rich.console import Console
from rich.table import Table
from rich.box import Box, ASCII, SQUARE, MINIMAL_DOUBLE_HEAD, DOUBLE, HEAVY, ROUNDED
from rich import box
import json

# Load actual data
with open('step2.json', 'r') as f:
    data = json.load(f)

# Get a sample match
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

# Create console for output
console = Console()

print("=" * 80)
print("RICH TABLES WITH CONNECTED GRID LINES")
print("=" * 80)
print()

# Example 1: Default Rich table with box.SQUARE (fully connected)
print("1. RICH WITH box.SQUARE (Fully Connected Grid)")
print("-" * 50)

table1 = Table(title=f"{home} vs. {away}", box=box.SQUARE)
table1.add_column("MARKET", style="cyan", width=12)
table1.add_column("HOME", style="green", justify="center", width=14)
table1.add_column("DRAW", style="yellow", justify="center", width=14)
table1.add_column("AWAY", style="red", justify="center", width=14)

# Add odds data
money_line = sample_match.get("money_line_american", [])
if money_line:
    latest = money_line[-1]
    if len(latest) >= 5:
        table1.add_row(
            "Money Line",
            format_american_odds(latest[2]),
            format_american_odds(latest[3]),
            format_american_odds(latest[4])
        )

spread = sample_match.get("spread_american", [])
if spread:
    latest = spread[-1]
    if len(latest) >= 5:
        table1.add_row(
            "Spread",
            format_american_odds(latest[2]),
            f"Point: {latest[3]:+.2g}".rstrip('0').rstrip('.'),
            format_american_odds(latest[4])
        )

over_under = sample_match.get("over_under_american", [])
if over_under:
    latest = over_under[-1]
    if len(latest) >= 5:
        table1.add_row(
            "O/U",
            f"Over: {format_american_odds(latest[2])}",
            f"Line: {latest[3]:.1f}",
            f"Under: {format_american_odds(latest[4])}"
        )

console.print(table1)
print()

# Example 2: ASCII box (pure ASCII, no Unicode)
print("\n2. RICH WITH box.ASCII (Pure ASCII Grid)")
print("-" * 50)

table2 = Table(title=f"{home} vs. {away}", box=box.ASCII)
table2.add_column("MARKET", width=12)
table2.add_column("HOME", justify="center", width=14)
table2.add_column("DRAW", justify="center", width=14)
table2.add_column("AWAY", justify="center", width=14)

# Add same data
if money_line:
    latest = money_line[-1]
    if len(latest) >= 5:
        table2.add_row(
            "Money Line",
            format_american_odds(latest[2]),
            format_american_odds(latest[3]),
            format_american_odds(latest[4])
        )

if spread:
    latest = spread[-1]
    if len(latest) >= 5:
        table2.add_row(
            "Spread",
            format_american_odds(latest[2]),
            f"Point: {latest[3]:+.2g}".rstrip('0').rstrip('.'),
            format_american_odds(latest[4])
        )

if over_under:
    latest = over_under[-1]
    if len(latest) >= 5:
        table2.add_row(
            "O/U",
            f"Over: {format_american_odds(latest[2])}",
            f"Line: {latest[3]:.1f}",
            f"Under: {format_american_odds(latest[4])}"
        )

console.print(table2)
print()

# Example 3: Custom Box Style (Excel-like)
print("\n3. HEAVY BOX STYLE (Thick Connected Grid)")
print("-" * 50)

table3 = Table(title=f"{home} vs. {away}", box=box.HEAVY)
table3.add_column("MARKET", width=12)
table3.add_column("HOME", justify="center", width=14)
table3.add_column("DRAW", justify="center", width=14)
table3.add_column("AWAY", justify="center", width=14)

# Add data
if money_line:
    latest = money_line[-1]
    if len(latest) >= 5:
        table3.add_row(
            "Money Line",
            format_american_odds(latest[2]),
            format_american_odds(latest[3]),
            format_american_odds(latest[4])
        )

if spread:
    latest = spread[-1]
    if len(latest) >= 5:
        table3.add_row(
            "Spread",
            format_american_odds(latest[2]),
            f"Point: {latest[3]:+.2g}".rstrip('0').rstrip('.'),
            format_american_odds(latest[4])
        )

if over_under:
    latest = over_under[-1]
    if len(latest) >= 5:
        table3.add_row(
            "O/U",
            f"Over: {format_american_odds(latest[2])}",
            f"Line: {latest[3]:.1f}",
            f"Under: {format_american_odds(latest[4])}"
        )

console.print(table3)
print()

# Example 4: Complete match display with Rich
print("\n4. COMPLETE MATCH DISPLAY WITH RICH")
print("-" * 50)

# Match info table (no box for clean look)
info_table = Table(show_header=False, box=None, padding=0)
info_table.add_column("Info", style="bold")
info_table.add_row(f"{home} vs. {away}")
info_table.add_row(f"Score: {score}" + (f" (HT:{ht_score})" if ht_score else ""))
info_table.add_row(f"Status: {status_name} (ID:{status_id})")

# Create a panel-like border
console.print("+" + "-" * 78 + "+")
for row in info_table.rows:
    text = row[0]
    console.print(f"| {text:<76} |")

# Odds table with connected grid
odds_table = Table(show_header=True, box=box.SQUARE, padding=(0, 1))
odds_table.add_column("MARKET", width=12)
odds_table.add_column("HOME", justify="center", width=14)
odds_table.add_column("DRAW", justify="center", width=14)
odds_table.add_column("AWAY", justify="center", width=14)

if money_line:
    latest = money_line[-1]
    if len(latest) >= 5:
        odds_table.add_row(
            "Money Line",
            format_american_odds(latest[2]),
            format_american_odds(latest[3]),
            format_american_odds(latest[4])
        )

if spread:
    latest = spread[-1]
    if len(latest) >= 5:
        odds_table.add_row(
            "Spread",
            format_american_odds(latest[2]),
            f"Point: {latest[3]:+.2g}".rstrip('0').rstrip('.'),
            format_american_odds(latest[4])
        )

if over_under:
    latest = over_under[-1]
    if len(latest) >= 5:
        odds_table.add_row(
            "O/U",
            f"Over: {format_american_odds(latest[2])}",
            f"Line: {latest[3]:.1f}",
            f"Under: {format_american_odds(latest[4])}"
        )

console.print(odds_table)

# Weather info
env = sample_match.get("environment", {})
weather = env.get("weather", "N/A")
temp = env.get("temperature", "N/A")
wind = env.get("wind_speed", "N/A")
print(f"\nWeather: {weather}  ·  Temp: {temp}  ·  Wind: {wind}")

# Example 5: Different box styles comparison
print("\n\n5. COMPARISON OF RICH BOX STYLES")
print("-" * 50)

box_styles = [
    ("SQUARE", box.SQUARE),
    ("DOUBLE", box.DOUBLE),
    ("HEAVY", box.HEAVY),
    ("ROUNDED", box.ROUNDED),
    ("ASCII", box.ASCII),
    ("MINIMAL_DOUBLE_HEAD", box.MINIMAL_DOUBLE_HEAD),
]

for name, style in box_styles:
    print(f"\n{name} Style:")
    demo_table = Table(box=style, show_header=True)
    demo_table.add_column("TYPE", width=10)
    demo_table.add_column("HOME", width=10)
    demo_table.add_column("AWAY", width=10)
    demo_table.add_row("ML", "+150", "-120")
    demo_table.add_row("Spread", "+2.5", "-2.5")
    console.print(demo_table)

# Example 6: For log files - no colors
print("\n\n6. RICH TABLE FOR LOG FILES (No Colors)")
print("-" * 50)

# Create a console that doesn't use colors
plain_console = Console(force_terminal=False, width=80, legacy_windows=True)

log_table = Table(
    title=f"{home} vs. {away}",
    box=box.ASCII,  # ASCII for maximum compatibility
    show_header=True,
    header_style=None,  # No styling
    title_style=None,   # No styling
    border_style=None,  # No styling
    row_styles=None,    # No styling
    padding=(0, 1)
)

log_table.add_column("MARKET", width=12)
log_table.add_column("HOME", justify="center", width=14)
log_table.add_column("DRAW", justify="center", width=14)
log_table.add_column("AWAY", justify="center", width=14)

if money_line:
    latest = money_line[-1]
    if len(latest) >= 5:
        log_table.add_row(
            "Money Line",
            format_american_odds(latest[2]),
            format_american_odds(latest[3]),
            format_american_odds(latest[4])
        )

if spread:
    latest = spread[-1]
    if len(latest) >= 5:
        log_table.add_row(
            "Spread",
            format_american_odds(latest[2]),
            f"Point: {latest[3]:+.2g}".rstrip('0').rstrip('.'),
            format_american_odds(latest[4])
        )

plain_console.print(log_table)
