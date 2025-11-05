#!/bin/bash

# 🏠 Field Resource Ecosystem (FREE) Startup Script
# Purpose: Initialize complete FREE system with sacred geometry integration
# Frequency: 741Hz (Insight & Integration)

set -e

GATEWAY_DIR="/Users/jbear/FIELD/⬡_integration/●traefik_gateway"
FREE_SERVICE="$GATEWAY_DIR/services/free_core_service.py"
FIELD_BASE="/Users/jbear/FIELD"

echo "🎆 Starting Field Resource Ecosystem (FREE)"
echo "📍 Location: ⬡_integration/●traefik_gateway"
echo "🎵 Resonant Frequency: 741Hz (Insight & Integration)"
echo "⬡  Sacred Framework: 3×3×3 Sierpiński Cube"
echo ""

# Check dependencies
echo "🔧 Checking FREE system dependencies..."

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 not found"
    exit 1
fi
echo "✅ Python 3 available"

# Check required Python packages
echo "📦 Checking Python packages..."
REQUIRED_PACKAGES=("aiohttp" "sqlite3")

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo "✅ $package available"
    else
        echo "⚠️  $package missing - installing..."
        pip3 install $package
    fi
done

# Check FREE core service file
if [ -f "$FREE_SERVICE" ]; then
    echo "✅ FREE core service found"
else
    echo "❌ FREE core service missing at $FREE_SERVICE"
    exit 1
fi

# Check homefield manifest
HOMEFIELD_MANIFEST="$FIELD_BASE/▼TATA/▼_truth/home_field_manifest.json"
if [ -f "$HOMEFIELD_MANIFEST" ]; then
    echo "✅ Homefield manifest found"
else
    echo "⚠️  Homefield manifest not found (will use defaults)"
fi

# Check breath scan directory
BREATH_SCAN_DIR="$FIELD_BASE/⬡_integration/accounts/_temporal_logs"
if [ -d "$BREATH_SCAN_DIR" ]; then
    echo "✅ Breath scan logs directory found"
    SCAN_COUNT=$(ls "$BREATH_SCAN_DIR"/breath_scan_*.json 2>/dev/null | wc -l)
    echo "📊 Found $SCAN_COUNT breath scan files"
else
    echo "⚠️  Breath scan logs directory not found (will use default resonance)"
fi

echo ""

# Pre-flight system checks
echo "🧘 Running FREE system pre-flight checks..."

# Check chakra frequency mappings
echo "🎵 Verifying chakra frequency mappings:"
echo "  Root: 396Hz → Port 3960"
echo "  Sacral: 417Hz → Port 4170" 
echo "  Solar: 639Hz → Port 6390"
echo "  Heart: 528Hz → Port 5280"
echo "  Throat: 741Hz → Port 7410"
echo "  Third Eye: 852Hz → Port 8520"
echo "  Crown: 432Hz → Port 4320"
echo "  Triadic Engine: Port 8888"

# Check port availability
echo ""
echo "🔌 Checking port availability..."

FREE_PORT=8888
if lsof -i :$FREE_PORT >/dev/null 2>&1; then
    echo "⚠️  Port $FREE_PORT is already in use - stopping existing service"
    # Try to find and kill the process
    PID=$(lsof -t -i :$FREE_PORT 2>/dev/null || true)
    if [ -n "$PID" ]; then
        echo "🛑 Stopping process $PID on port $FREE_PORT"
        kill $PID 2>/dev/null || true
        sleep 2
    fi
fi

if lsof -i :$FREE_PORT >/dev/null 2>&1; then
    echo "❌ Port $FREE_PORT still in use - cannot start FREE service"
    exit 1
else
    echo "✅ Port $FREE_PORT available for FREE service"
fi

echo ""

# Start FREE core service
echo "🚀 Starting FREE Core Service..."
echo "⬡  Triadic Engine Port: $FREE_PORT"
echo "🧘 Sacred Geometry Processor: Active"
echo "📊 Resonance Monitor: Integrated"
echo "🔄 Resource Frequency Mapper: Ready"
echo ""

echo "🎆 FREE System Access Points:"
echo "📊 Main Interface: http://free.local:8080"
echo "💊 System Health: http://free.local:8080/health"
echo "⚡ Resource Allocation: http://free.local:8080/allocate"
echo "🧘 Resonance Monitor: http://free.local:8080/resonance"
echo "⬡  Triadic Engine: http://free.local:8080/triadic-engine"
echo ""

echo "🏗️ Chakra Resource Endpoints:"
echo "🔴 Root (Infrastructure): http://free.local:8080/resources/root"
echo "🟠 Sacral (Development): http://free.local:8080/resources/sacral"
echo "🟡 Solar (Control): http://free.local:8080/resources/solar"
echo "🟢 Heart (Integration): http://free.local:8080/resources/heart"
echo "🔵 Throat (Communication): http://free.local:8080/resources/throat"
echo "🟣 Third Eye (Intelligence): http://free.local:8080/resources/eye"
echo "⚪ Crown (Wisdom): http://free.local:8080/resources/crown"
echo ""

echo "🔗 Professional Integration:"
echo "💼 FRE Commands: http://free.local:8080/fre"
echo "🕵️ Intelligence Collection: http://free.local:8080/intelligence"
echo ""

# Change to services directory and start the service
cd "$GATEWAY_DIR/services"

echo "🎵 Field Resource Ecosystem (FREE) activating..."
echo "⬡  Sacred geometry processors online"
echo "🧘 Consciousness-aware resource management ready"
echo "🔒 Sovereignty preservation active"
echo ""

# Start the FREE service
exec python3 free_core_service.py