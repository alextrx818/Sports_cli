#!/bin/bash
"""
Pipeline Monitoring Script
==========================

Automated monitoring and maintenance for the football data pipeline.
Runs resource checks, performs maintenance, and sends alerts.

Usage:
  ./monitor_pipeline.sh check     - One-time resource check
  ./monitor_pipeline.sh watch     - Continuous monitoring (5 min intervals)
  ./monitor_pipeline.sh maintain  - Perform maintenance operations
  ./monitor_pipeline.sh alert     - Check for alert conditions only
"""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
RESOURCE_MONITOR="$SCRIPT_DIR/resource_monitor.py"
LOG_FILE="$SCRIPT_DIR/monitor_pipeline.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Function to check if pipeline is running
check_pipeline_running() {
    if pgrep -f "step1.py.*continuous" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to perform resource check
resource_check() {
    print_status "Performing resource check..."
    
    if [ ! -f "$PYTHON_BIN" ]; then
        print_error "Python virtual environment not found: $PYTHON_BIN"
        return 1
    fi
    
    if [ ! -f "$RESOURCE_MONITOR" ]; then
        print_error "Resource monitor script not found: $RESOURCE_MONITOR"
        return 1
    fi
    
    # Generate resource report
    "$PYTHON_BIN" "$RESOURCE_MONITOR" --report
    
    # Check for critical alerts
    alert_output=$("$PYTHON_BIN" "$RESOURCE_MONITOR" --report --json | jq -r '.summary.overall_status')
    
    case "$alert_output" in
        "CRITICAL")
            print_error "CRITICAL alerts detected! Immediate attention required."
            return 2
            ;;
        "WARNING")
            print_warning "Warning conditions detected. Monitor closely."
            return 1
            ;;
        "OK")
            print_success "All systems operating normally."
            return 0
            ;;
        *)
            print_error "Unable to determine system status."
            return 1
            ;;
    esac
}

# Function to perform maintenance
perform_maintenance() {
    print_status "Starting automated maintenance..."
    
    if ! check_pipeline_running; then
        print_warning "Pipeline is not running. Maintenance may be safer but data won't be current."
    fi
    
    # Check available disk space first
    free_space=$(df "$SCRIPT_DIR" | awk 'NR==2 {print $4}')
    free_gb=$((free_space / 1024 / 1024))
    
    if [ "$free_gb" -lt 5 ]; then
        print_warning "Low disk space detected ($free_gb GB). Performing aggressive cleanup..."
        
        # Compress old files
        print_status "Compressing old files..."
        "$PYTHON_BIN" "$RESOURCE_MONITOR" --compress
        
        # If still low, cleanup very old files
        if [ "$free_gb" -lt 2 ]; then
            print_warning "Still critically low on space. Deleting old files..."
            "$PYTHON_BIN" "$RESOURCE_MONITOR" --cleanup
        fi
    else
        print_status "Disk space adequate ($free_gb GB). Performing routine compression..."
        "$PYTHON_BIN" "$RESOURCE_MONITOR" --compress
    fi
    
    print_success "Maintenance completed."
}

# Function to check alerts only
check_alerts() {
    print_status "Checking for alert conditions..."
    
    # Get just the alerts from resource monitor
    alerts_json=$("$PYTHON_BIN" "$RESOURCE_MONITOR" --report --json | jq '.alerts')
    alert_count=$(echo "$alerts_json" | jq 'length')
    
    if [ "$alert_count" -gt 0 ]; then
        print_warning "Found $alert_count alert(s):"
        echo "$alerts_json" | jq -r '.[] | "  \(.level): \(.message)"'
        return 1
    else
        print_success "No alerts detected."
        return 0
    fi
}

# Function to watch continuously
watch_continuously() {
    print_status "Starting continuous monitoring (5-minute intervals)..."
    print_status "Press Ctrl+C to stop monitoring"
    
    # Log monitoring start
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Monitoring started" >> "$LOG_FILE"
    
    while true; do
        {
            echo "=== Monitor Check: $(date) ==="
            
            # Check if pipeline is still running
            if check_pipeline_running; then
                echo "✓ Pipeline is running"
            else
                echo "✗ Pipeline is NOT running!"
                print_error "Pipeline appears to have stopped!"
            fi
            
            # Perform resource check
            resource_check
            
            # Check for alerts
            check_alerts
            
            echo "=== End Check ==="
            echo ""
            
        } >> "$LOG_FILE" 2>&1
        
        # Wait 5 minutes
        sleep 300
    done
}

# Function to get pipeline status
get_pipeline_status() {
    echo "=================================="
    echo "    PIPELINE STATUS SUMMARY"
    echo "=================================="
    
    # Pipeline process status
    if check_pipeline_running; then
        PID=$(pgrep -f "step1.py.*continuous")
        echo "Pipeline Status: ✓ RUNNING (PID: $PID)"
        
        # Show process details
        echo ""
        echo "Process Details:"
        ps -p "$PID" -o pid,ppid,pcpu,pmem,etime,cmd --no-headers
        
        # Show recent activity
        echo ""
        echo "Recent Activity:"
        if [ -f "$SCRIPT_DIR/step1.log" ]; then
            tail -n 3 "$SCRIPT_DIR/step1.log" | sed 's/^/  /'
        fi
        
    else
        echo "Pipeline Status: ✗ NOT RUNNING"
    fi
    
    # Resource summary
    echo ""
    echo "Resource Summary:"
    "$PYTHON_BIN" "$RESOURCE_MONITOR" --report --json | jq -r '
        "  Disk Free: \(.disk_usage.free_gb)GB (\(.disk_usage.status))",
        "  Memory Used: \(.memory_usage.system.used_percent)%",
        "  Pipeline Data: \(.file_usage.total_size_gb)GB",
        "  Alerts: \(.summary.total_alerts) (\(.summary.overall_status))"
    '
    
    echo "=================================="
}

# Main script logic
case "${1:-status}" in
    check)
        resource_check
        ;;
    watch)
        watch_continuously
        ;;
    maintain)
        perform_maintenance
        ;;
    alert)
        check_alerts
        ;;
    status)
        get_pipeline_status
        ;;
    help|--help|-h)
        echo "Pipeline Monitoring Script"
        echo "========================="
        echo ""
        echo "Usage: $0 {check|watch|maintain|alert|status|help}"
        echo ""
        echo "Commands:"
        echo "  check    - Perform one-time resource check and report"
        echo "  watch    - Continuous monitoring every 5 minutes"
        echo "  maintain - Perform maintenance (compress/cleanup old files)"
        echo "  alert    - Check for alert conditions only"
        echo "  status   - Show current pipeline and resource status"
        echo "  help     - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 check                    # Quick resource check"
        echo "  $0 watch                    # Start continuous monitoring"
        echo "  $0 maintain                 # Clean up old files"
        echo "  $0 status                   # Show current status"
        echo ""
        echo "Files:"
        echo "  Monitor log: $LOG_FILE"
        echo "  Resource monitor: $RESOURCE_MONITOR"
        echo "  Alert log: $SCRIPT_DIR/resource_alerts.log"
        ;;
    *)
        echo "Usage: $0 {check|watch|maintain|alert|status|help}"
        echo "Use '$0 help' for detailed information."
        exit 1
        ;;
esac

exit $?