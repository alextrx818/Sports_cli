#!/bin/bash
"""
Setup Automated Pipeline Monitoring
===================================

Sets up cron jobs and monitoring for the football data pipeline.
"""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_FILE="/tmp/pipeline_monitoring_cron"

echo "Setting up automated pipeline monitoring..."

# Create cron jobs file
cat > "$CRON_FILE" << 'EOF'
# Pipeline Resource Monitoring
# Check resources every 15 minutes
*/15 * * * * cd /root/6-4-2025 && ./monitor_pipeline.sh check >> /root/6-4-2025/monitor_pipeline.log 2>&1

# Maintenance every 6 hours
0 */6 * * * cd /root/6-4-2025 && ./monitor_pipeline.sh maintain >> /root/6-4-2025/monitor_pipeline.log 2>&1

# Daily status report at 9 AM
0 9 * * * cd /root/6-4-2025 && ./monitor_pipeline.sh status | mail -s "Pipeline Daily Status" root@localhost

# Weekly cleanup on Sundays at 2 AM
0 2 * * 0 cd /root/6-4-2025 && python3 resource_monitor.py --cleanup >> /root/6-4-2025/monitor_pipeline.log 2>&1
EOF

# Install cron jobs
echo "Installing cron jobs..."
crontab "$CRON_FILE"

# Verify installation
echo ""
echo "Installed cron jobs:"
crontab -l | grep -E "monitor_pipeline|resource_monitor"

# Clean up
rm "$CRON_FILE"

echo ""
echo "✅ Monitoring setup complete!"
echo ""
echo "Monitoring features:"
echo "  • Resource checks every 15 minutes"
echo "  • Automatic maintenance every 6 hours"
echo "  • Daily status reports"
echo "  • Weekly cleanup"
echo ""
echo "Manual commands:"
echo "  ./monitor_pipeline.sh status   - Current status"
echo "  ./monitor_pipeline.sh check    - Resource check"
echo "  ./monitor_pipeline.sh maintain - Maintenance"
echo "  ./monitor_pipeline.sh watch    - Continuous monitoring"
echo ""
echo "Log files:"
echo "  monitor_pipeline.log     - Monitoring activity"
echo "  resource_monitor.log     - Resource monitor details"
echo "  resource_alerts.log      - Alert notifications"