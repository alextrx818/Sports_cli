#!/bin/bash
"""
Simple Disk Space Alert Script
==============================

Quick disk space check with immediate alerts.
Can be run frequently without overhead.
"""

THRESHOLD_WARNING=85  # Warn at 85% disk usage
THRESHOLD_CRITICAL=95  # Critical at 95% disk usage
PIPELINE_DIR="/root/6-4-2025"

# Get disk usage percentage
USAGE=$(df "$PIPELINE_DIR" | awk 'NR==2 {print $5}' | sed 's/%//')
FREE_GB=$(df -BG "$PIPELINE_DIR" | awk 'NR==2 {print $4}' | sed 's/G//')

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Check thresholds and alert
if [ "$USAGE" -ge "$THRESHOLD_CRITICAL" ]; then
    echo -e "${RED}CRITICAL: Disk usage at ${USAGE}% (${FREE_GB}GB free)${NC}"
    echo "$(date): CRITICAL - Disk usage ${USAGE}% (${FREE_GB}GB free)" >> "$PIPELINE_DIR/disk_alerts.log"
    
    # Emergency cleanup
    echo "Performing emergency cleanup..."
    cd "$PIPELINE_DIR"
    
    # Compress largest files immediately
    find . -name "step1_20*.json" -size +10M -exec gzip {} \; 2>/dev/null
    
    # Remove oldest log rotations
    find logs/ -name "*.md.*" -mtime +7 -delete 2>/dev/null
    
    exit 2
    
elif [ "$USAGE" -ge "$THRESHOLD_WARNING" ]; then
    echo -e "${YELLOW}WARNING: Disk usage at ${USAGE}% (${FREE_GB}GB free)${NC}"
    echo "$(date): WARNING - Disk usage ${USAGE}% (${FREE_GB}GB free)" >> "$PIPELINE_DIR/disk_alerts.log"
    exit 1
    
else
    echo -e "${GREEN}OK: Disk usage at ${USAGE}% (${FREE_GB}GB free)${NC}"
    exit 0
fi