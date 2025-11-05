#!/bin/bash

# 🔷 Field Integration Gateway Startup
# Resonant Location: ⬡_integration/●traefik_gateway
# Purpose: Initialize unified API gateway for DOJO ↔ Walkerville integration

set -e

GATEWAY_DIR="/Users/jbear/FIELD/⬡_integration/●traefik_gateway"
CONFIG_FILE="$GATEWAY_DIR/config/traefik.yml"
LOG_FILE="$GATEWAY_DIR/logs/gateway.log"

# Create logs directory if it doesn't exist
mkdir -p "$GATEWAY_DIR/logs"

echo "🔷 Initializing Field Integration Gateway..."
echo "📍 Location: ⬡_integration/●traefik_gateway"
echo "🎵 Frequency: 741Hz (Insight & Integration)"
echo ""

# Add local hostnames to /etc/hosts if not present
echo "🔧 Configuring local DNS entries..."

HOSTS_ENTRIES=(
    "127.0.0.1 walkerville.local"
    "127.0.0.1 dojo.local" 
    "127.0.0.1 api.local"
    "127.0.0.1 gateway.local"
    "127.0.0.1 homefield.local"
    "127.0.0.1 free.local"
)

for entry in "${HOSTS_ENTRIES[@]}"; do
    if ! grep -q "$entry" /etc/hosts 2>/dev/null; then
        echo "Adding: $entry"
        echo "$entry" | sudo tee -a /etc/hosts > /dev/null
    else
        echo "✅ Already configured: $entry"
    fi
done

echo ""
echo "🚀 Starting Traefik Gateway..."
echo "📊 Dashboard: http://localhost:9090"
echo "🌐 Walkerville: http://walkerville.local:8080"
echo "🧘 DOJO: http://dojo.local:8080"
echo "🏠 Homefield 7.0: http://homefield.local:8080"
echo "🎆 FREE System: http://free.local:8080"
echo "🔗 Unified API: http://api.local:8080"
echo "❤️  Health Monitor: http://gateway.local:8080/health"
echo ""

# Start Traefik
exec traefik \
    --configfile="$CONFIG_FILE" \
    --log.filePath="$LOG_FILE" \
    --log.level=INFO