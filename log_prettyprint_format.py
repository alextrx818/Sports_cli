"""
Configuration for Step 7 pretty-print logging format.
"""

# Default display width for banners and tables
DEFAULT_WIDTH = 80

# Status filtering and display names
STATUS_FILTER = [2, 3, 4, 5, 6, 7]
STATUS_NAMES = {
    2: "First Half",
    3: "Half-time",
    4: "Second Half",
    5: "Overtime",
    6: "Overtime",
    7: "Penalty Shootout",
    8: "Finished",
    9: "Cancelled",
    10: "Postponed",
}

# Table column widths for odds display
COLUMN_WIDTHS = {
    'market': 14,
    'home': 14,
    'draw': 14,
    'away': 14,
}

# Character definitions
HORIZONTAL_BORDER = '-'  # used for drawing boxes
VERTICAL_BORDER = '|'    # used for drawing boxes
# Full inner width for tables (excluding border chars)
INNER_WIDTH = DEFAULT_WIDTH - 2

import json, logging, time, pytz
from datetime import datetime
from pathlib import Path

# Path placeholders will be provided by caller
STEP2_FILE = Path("step2.json")
DAILY_COUNTER_FILE = Path("daily_match_counter.json")
LOG_FILE = Path("step7_simple.log")
TZ = pytz.timezone("America/New_York")

# Function to setup logger writing to LOG_FILE
def setup_logger(log_file: Path = LOG_FILE) -> logging.Logger:
    logger = logging.getLogger("prettyprint")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(message)s")
    fh = logging.FileHandler(str(log_file), mode="w", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger

# Move et_now, format_american_odds, centred, write_competition_header,
# write_status_header, write_match_body, write_global_header, write_summary_footer here

# Central entrypoint

def pretty_print(summaries: list, daily_count: int, log_file: Path = LOG_FILE):
    logger = setup_logger(log_file)
    in_play = [m for m in summaries if m.get("status_id") in STATUS_FILTER]
    write_global_header(logger, daily_count, len(in_play))
    # Group by competition and print
    # ...existing code to iterate comp_groups and call write_competition_header, write_status_header, write_match_body...
    write_summary_footer(logger, in_play, comp_groups, start_time)
