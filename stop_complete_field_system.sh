#!/bin/bash
echo "🛑 Stopping Complete FIELD System..."

# Kill all FIELD processes
pkill -f "server.py"
pkill -f "train_station.py" 
pkill -f "mcp_.*\.py"

# Clean up PID files
rm -f /tmp/field_*_pid
rm -f /tmp/mcp_*.py

echo "✅ FIELD System stopped"
