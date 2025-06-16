#!/usr/bin/env python3
"""
Examples of different Python table formatting libraries
for displaying sports match data with odds
"""

from tabulate import tabulate
from prettytable import PrettyTable
from rich.console import Console
from rich.table import Table
from texttable import Texttable

# Sample match data
match_info = {
    "home": "Marin FC (W)",
    "away": "Stockton Cargo(w)",
    "score": "0-0",
    "ht_score": "0-0",
    "status": "Second Half",
    "status_id": 4
}

odds_data = [
    ["Money Line", "+650", "+400", "-333"],
    ["Spread", "+100", "Point: -0.5", "-125"],
    ["O/U", "Over: -118", "Line: 4.0", "Under: -105"]
]

print("=" * 80)
print("COMPARISON OF PYTHON TABLE FORMATTING LIBRARIES")
print("=" * 80)
print()

# 1. TABULATE Examples
print("1. TABULATE LIBRARY")
print("-" * 40)
print("\nTabulate with 'grid' format:")
print(tabulate(odds_data, headers=["MARKET", "HOME", "DRAW", "AWAY"], tablefmt="grid"))

print("\nTabulate with 'simple' format:")
print(tabulate(odds_data, headers=["MARKET", "HOME", "DRAW", "AWAY"], tablefmt="simple"))

print("\nTabulate with 'pipe' format (Markdown compatible):")
print(tabulate(odds_data, headers=["MARKET", "HOME", "DRAW", "AWAY"], tablefmt="pipe"))

print("\nTabulate with 'pretty' format:")
print(tabulate(odds_data, headers=["MARKET", "HOME", "DRAW", "AWAY"], tablefmt="pretty"))

# 2. PRETTYTABLE Example
print("\n\n2. PRETTYTABLE LIBRARY")
print("-" * 40)
table = PrettyTable()
table.field_names = ["MARKET", "HOME", "DRAW", "AWAY"]
for row in odds_data:
    table.add_row(row)

print("\nPrettyTable default:")
print(table)

# Customize PrettyTable
table.align = "c"  # Center align
table.border = True
table.header = True
table.junction_char = "+"
table.horizontal_char = "-"
table.vertical_char = "|"

print("\nPrettyTable customized:")
print(table)

# 3. RICH Example
print("\n\n3. RICH LIBRARY")
print("-" * 40)
console = Console()

# Basic Rich table
rich_table = Table(title=f"{match_info['home']} vs. {match_info['away']}")
rich_table.add_column("MARKET", style="cyan", no_wrap=True)
rich_table.add_column("HOME", style="green")
rich_table.add_column("DRAW", style="yellow")
rich_table.add_column("AWAY", style="red")

for row in odds_data:
    rich_table.add_row(*row)

print("\nRich table (with colors in terminal):")
console.print(rich_table)

# Rich table without colors for log files
rich_table_plain = Table(
    title=f"{match_info['home']} vs. {match_info['away']}",
    show_header=True,
    header_style="bold"
)
rich_table_plain.add_column("MARKET", width=14)
rich_table_plain.add_column("HOME", width=14)
rich_table_plain.add_column("DRAW", width=14)
rich_table_plain.add_column("AWAY", width=14)

for row in odds_data:
    rich_table_plain.add_row(*row)

print("\nRich table (plain style):")
console_plain = Console(force_terminal=False, width=80)
console_plain.print(rich_table_plain)

# 4. TEXTTABLE Example
print("\n\n4. TEXTTABLE LIBRARY")
print("-" * 40)

# Basic Texttable
t = Texttable()
t.add_rows([["MARKET", "HOME", "DRAW", "AWAY"]] + odds_data)
print("\nTexttable default:")
print(t.draw())

# Customized Texttable
t2 = Texttable()
t2.set_deco(Texttable.HEADER | Texttable.BORDER | Texttable.HLINES | Texttable.VLINES)
t2.set_cols_align(["l", "c", "c", "c"])
t2.set_cols_width([14, 14, 14, 14])
t2.add_rows([["MARKET", "HOME", "DRAW", "AWAY"]] + odds_data)
print("\nTexttable customized:")
print(t2.draw())

# Complete match display example using tabulate
print("\n\n" + "=" * 80)
print("COMPLETE MATCH DISPLAY EXAMPLE (using tabulate)")
print("=" * 80)

# Match header
match_header = [
    [f"{match_info['home']} vs. {match_info['away']}"],
    [f"Score: {match_info['score']} (HT:{match_info['ht_score']})"],
    [f"Status: {match_info['status']} (ID:{match_info['status_id']})"]
]

print("\nMatch Information:")
print("+" + "-" * 78 + "+")
for row in match_header:
    print(f"| {row[0]:<76} |")
print("+" + "-" * 78 + "+")

print("\nOdds Table:")
print(tabulate(odds_data, headers=["MARKET", "HOME", "DRAW", "AWAY"], 
               tablefmt="grid", colalign=("left", "center", "center", "center")))

print("\nWeather: Sunny  ·  Temp: 60.8°F  ·  Wind: 6.5mph")
