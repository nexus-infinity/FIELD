#!/bin/bash
# Weekly Maintenance Script

echo "Running Weekly Maintenance Tasks..."

# Run Sacred Validation Demo with Full Scan
python3 /Users/jbear/FIELD/▲ATLAS/sacred_validation_demo.py --full-scan

# Run Sacred CLI Tools Metrics
/Users/jbear/FIELD/▲ATLAS/sacred-cli-tools.js metrics --json

echo "Weekly Maintenance Tasks Complete."
