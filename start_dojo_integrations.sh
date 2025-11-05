#!/bin/bash
# Dojo System Integration Startup Script

echo "🥋 Starting Dojo System Integrations..."

# Start API Gateway
echo "🚀 Starting API Gateway..."
cd /Users/jbear/FIELD/integrations/api_gateway
python3 server.py &
API_PID=$!
echo "API Gateway started (PID: $API_PID)"

# Start Monitoring
echo "📊 Starting System Monitor..."
cd /Users/jbear/FIELD/integrations/monitoring
python3 monitor.py &
MONITOR_PID=$!
echo "Monitor started (PID: $MONITOR_PID)"

# Wait for services to start
sleep 5

# Test API Gateway
echo "🧪 Testing API Gateway..."
curl -s http://localhost:8000/ | jq .

echo "✅ Dojo System Integrations are now running!"
echo "📋 Services:"
echo "  - API Gateway: http://localhost:8000"
echo "  - Datashare: http://localhost:9630"
echo "  - Monitoring: Active"

echo "🛑 To stop services:"
echo "  kill $API_PID $MONITOR_PID"

# Keep script running
wait
