#!/bin/bash
# Daily Maintenance Script

echo "Running Daily Maintenance Tasks..."

# Run Sacred Validation Demo
python3 /Users/jbear/FIELD/▲ATLAS/sacred_validation_demo.py

# Run Sacred CLI Tools Health Check
/Users/jbear/FIELD/▲ATLAS/sacred-cli-tools.js health

echo "Daily Maintenance Tasks Complete."
