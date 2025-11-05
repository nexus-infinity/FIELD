#!/bin/bash
# Monthly Maintenance Script

echo "Running Monthly Maintenance Tasks..."

# Run Sacred Protocol Review
python3 /Users/jbear/FIELD/scripts/sacred_incremental_deployment.py --review

# Run Sacred Dashboard Monitor System Status
python3 /Users/jbear/FIELD/scripts/sacred_dashboard_monitor.py --system-status

echo "Monthly Maintenance Tasks Complete."
