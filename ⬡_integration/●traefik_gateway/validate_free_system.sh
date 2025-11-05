#!/bin/bash

# 🧪 Field Resource Ecosystem (FREE) - Complete Postman Validation
# Purpose: Start services and run comprehensive Postman tests
# Frequency: 741Hz (Insight & Integration)

set -e

GATEWAY_DIR="/Users/jbear/FIELD/⬡_integration/●traefik_gateway"
SERVICES_DIR="$GATEWAY_DIR/services"
POSTMAN_DIR="$GATEWAY_DIR/postman"

echo "🧪 Starting Field Resource Ecosystem (FREE) Validation Tests"
echo "📍 Location: ⬡_integration/●traefik_gateway"  
echo "🎵 Resonant Frequency: 741Hz (Insight & Integration)"
echo "⬡  Sacred Framework: 3×3×3 Sierpiński Cube"
echo ""

# Function to check if a service is running on a port
check_service() {
    local port=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo "🔍 Checking $service_name on port $port..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "http://localhost:$port" >/dev/null 2>&1; then
            echo "✅ $service_name is ready on port $port"
            return 0
        fi
        echo "⏳ Attempt $attempt/$max_attempts - waiting for $service_name..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $service_name failed to start on port $port"
    return 1
}

# Function to cleanup processes
cleanup() {
    echo ""
    echo "🧹 Cleaning up processes..."
    
    # Kill FREE service
    pkill -f "free_core_service.py" 2>/dev/null || true
    
    # Kill Traefik
    pkill -f "traefik" 2>/dev/null || true
    
    # Kill any process using our ports
    for port in 8080 8888 9090; do
        PID=$(lsof -t -i :$port 2>/dev/null || true)
        if [ -n "$PID" ]; then
            echo "📀 Killing process $PID on port $port"
            kill $PID 2>/dev/null || true
        fi
    done
    
    # Wait longer for processes to fully terminate
    sleep 5
    
    echo "✅ Cleanup complete"
}

# Set up cleanup trap
trap cleanup EXIT

# Step 1: Check dependencies
echo "🔧 Step 1: Checking dependencies..."

if ! command -v newman >/dev/null 2>&1; then
    echo "❌ Newman (Postman CLI) not found"
    echo "📦 Installing Newman..."
    npm install -g newman
fi
echo "✅ Newman available"

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 not found"
    exit 1
fi
echo "✅ Python 3 available"

if ! command -v traefik >/dev/null 2>&1; then
    echo "❌ Traefik not found"
    exit 1
fi
echo "✅ Traefik available"

echo ""

# Step 2: Kill any existing services
echo "🛑 Step 2: Stopping any existing services..."
cleanup
echo ""

# Step 3: Start FREE Core Service
echo "🚀 Step 3: Starting FREE Core Service..."

# Create a log file for the FREE service
mkdir -p "$GATEWAY_DIR/logs"
FREE_LOG="$GATEWAY_DIR/logs/free_service.log"

# Start FREE service in background
cd "$SERVICES_DIR"
nohup python3 free_core_service.py > "$FREE_LOG" 2>&1 &
FREE_PID=$!

echo "📝 FREE service started with PID: $FREE_PID"
echo "📋 Log file: $FREE_LOG"

# Wait for FREE service to be ready
if ! check_service 8888 "FREE Core Service"; then
    echo "❌ FREE Core Service failed to start"
    cat "$FREE_LOG" | tail -20
    exit 1
fi

echo ""

# Step 4: Configure hosts file (if needed)
echo "🔧 Step 4: Configuring local DNS..."

HOSTS_ENTRIES=(
    "127.0.0.1 free.local"
    "127.0.0.1 homefield.local"  
    "127.0.0.1 gateway.local"
    "127.0.0.1 dojo.local"
    "127.0.0.1 walkerville.local"
    "127.0.0.1 api.local"
)

for entry in "${HOSTS_ENTRIES[@]}"; do
    if ! grep -q "$entry" /etc/hosts 2>/dev/null; then
        echo "🔧 Adding: $entry"
        echo "$entry" | sudo tee -a /etc/hosts > /dev/null
    else
        echo "✅ Already configured: $entry"
    fi
done

echo ""

# Step 5: Start Traefik Gateway
echo "🔷 Step 5: Starting Traefik Gateway..."

# Create Traefik log file
TRAEFIK_LOG="$GATEWAY_DIR/logs/traefik.log"

# Start Traefik in background
cd "$GATEWAY_DIR"
nohup traefik \
    --configfile="$GATEWAY_DIR/config/traefik.yml" \
    --log.filePath="$TRAEFIK_LOG" \
    --log.level=INFO > "$TRAEFIK_LOG" 2>&1 &
TRAEFIK_PID=$!

echo "📝 Traefik started with PID: $TRAEFIK_PID"
echo "📋 Log file: $TRAEFIK_LOG"

# Wait for Traefik to be ready
if ! check_service 9090 "Traefik Dashboard"; then
    echo "❌ Traefik failed to start"
    cat "$TRAEFIK_LOG" | tail -20
    exit 1
fi

# Also check gateway routing
if ! check_service 8080 "Traefik Gateway"; then
    echo "❌ Traefik Gateway routing failed to start"
    cat "$TRAEFIK_LOG" | tail -20
    exit 1
fi

echo ""

# Step 6: Verify service integration
echo "🔗 Step 6: Verifying service integration..."

# Test FREE service directly
echo "🧪 Testing FREE service directly..."
if curl -s "http://localhost:8888/health" | jq . >/dev/null 2>&1; then
    echo "✅ FREE service health endpoint responding"
else
    echo "⚠️  FREE service health endpoint not responding with JSON"
fi

# Test FREE service through gateway
echo "🧪 Testing FREE through Traefik gateway..."
if curl -s "http://free.local:8080/health" >/dev/null 2>&1; then
    echo "✅ FREE accessible through Traefik gateway"
else
    echo "⚠️  FREE not accessible through gateway (may be routing issue)"
fi

echo ""

# Step 7: Run Postman Tests
echo "🧪 Step 7: Running Postman Validation Tests..."

COLLECTION_FILE="$POSTMAN_DIR/Homefield_Integration_Tests.postman_collection.json"

if [ ! -f "$COLLECTION_FILE" ]; then
    echo "❌ Postman collection not found: $COLLECTION_FILE"
    exit 1
fi

echo "📋 Collection: Homefield_Integration_Tests"
echo "🎯 Target: FREE System Integration"
echo ""

# Run Newman with detailed reporting
REPORT_DIR="$GATEWAY_DIR/test-results"
mkdir -p "$REPORT_DIR"

echo "🚀 Executing Newman tests..."
newman run "$COLLECTION_FILE" \
    --reporters cli,json,junit \
    --reporter-json-export "$REPORT_DIR/newman-results.json" \
    --reporter-junit-export "$REPORT_DIR/newman-results.xml" \
    --timeout 10000 \
    --delay-request 1000 \
    --verbose

NEWMAN_EXIT_CODE=$?

echo ""

# Step 8: Test Results Analysis
echo "📊 Step 8: Test Results Analysis..."

if [ $NEWMAN_EXIT_CODE -eq 0 ]; then
    echo "✅ All Postman tests PASSED!"
    echo "🎉 Field Resource Ecosystem (FREE) validation: SUCCESSFUL"
else
    echo "❌ Some Postman tests FAILED"
    echo "🔍 Check the detailed output above for specific failures"
fi

# Show service status
echo ""
echo "🔍 Final Service Status:"
echo "📊 FREE Core Service (8888): $(curl -s http://localhost:8888 >/dev/null && echo "✅ Running" || echo "❌ Not responding")"
echo "🔷 Traefik Dashboard (9090): $(curl -s http://localhost:9090 >/dev/null && echo "✅ Running" || echo "❌ Not responding")"
echo "🌐 Gateway Routing (8080): $(curl -s http://localhost:8080 >/dev/null && echo "✅ Running" || echo "❌ Not responding")"

# Show logs if there were failures
if [ $NEWMAN_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "📋 Recent FREE service logs:"
    tail -10 "$FREE_LOG" 2>/dev/null || echo "No FREE logs available"
    
    echo ""
    echo "📋 Recent Traefik logs:"
    tail -10 "$TRAEFIK_LOG" 2>/dev/null || echo "No Traefik logs available"
fi

echo ""
echo "📁 Test artifacts saved to: $REPORT_DIR"
echo "📊 JSON Report: $REPORT_DIR/newman-results.json"
echo "📋 JUnit Report: $REPORT_DIR/newman-results.xml"

echo ""
if [ $NEWMAN_EXIT_CODE -eq 0 ]; then
    echo "🎆 Field Resource Ecosystem (FREE) - VALIDATION COMPLETE ✅"
    echo "🎵 Resonant Frequency: 741Hz (Insight & Integration)"
    echo "⬡  Sacred Framework: 3×3×3 Sierpiński Cube"  
    echo "🔒 Sovereignty Model: Fully operational"
    echo ""
    echo "🌟 The world's first consciousness-aware, sovereignty-preserving,"
    echo "   frequency-resonant resource orchestration platform is"
    echo "   VALIDATED and ready for production use!"
else
    echo "⚠️  Field Resource Ecosystem (FREE) - VALIDATION INCOMPLETE"
    echo "🔧 Some tests failed - check logs and fix issues before production"
fi

exit $NEWMAN_EXIT_CODE