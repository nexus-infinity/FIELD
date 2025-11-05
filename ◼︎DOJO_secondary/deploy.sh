#!/bin/bash

# Sacred Chat Bridge Deployment Script
# Deploys sphere-aware chat system with sacred validation
# Symbol: ◼ | Origin: ~/FIELD/◼DOJO/ | Lineage: ⟡Akron > FIELD > DOJO

set -e  # Exit on any error

echo "🌟 Deploying SacredChatBridge in ~/FIELD/◼DOJO/"
echo "◼ Sacred manifestation engine initializing..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}🔧${NC} $1"
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Node.js version
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -ge 18 ]; then
        print_status "Node.js version: $(node --version)"
    else
        print_error "Node.js version 18+ required. Current: $(node --version)"
        exit 1
    fi
else
    print_error "Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check if Redis is running
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        print_status "Redis server is running"
    else
        print_warning "Redis server not running. Attempting to start..."
        if command -v redis-server &> /dev/null; then
            redis-server --daemonize yes
            sleep 2
            if redis-cli ping &> /dev/null; then
                print_status "Redis server started successfully"
            else
                print_error "Failed to start Redis server"
                exit 1
            fi
        else
            print_error "Redis not installed. Please install Redis"
            exit 1
        fi
    fi
else
    print_error "Redis not found. Please install Redis"
    exit 1
fi

# Navigate to project directory
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)
print_info "Working directory: $PROJECT_DIR"

# Create required directories
echo "📁 Creating sacred directory structure..."
mkdir -p sacred-logs
mkdir -p validation-logs
mkdir -p biological-flow-logs
mkdir -p sphere-transitions
print_status "Sacred directories created"

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    print_status "Dependencies installed"
else
    print_info "Dependencies already installed"
fi

# Initialize Redis with sacred keys
echo "🔐 Initializing sacred Redis state..."
redis-cli set active_sphere "FIELD" > /dev/null
redis-cli hset sacred_rules geometric_cleanliness "enabled" > /dev/null
redis-cli hset sacred_rules symbolic_anchoring "required" > /dev/null
redis-cli hset sacred_rules sphere_validation "strict" > /dev/null
redis-cli hset sacred_rules biological_flow "enabled" > /dev/null
print_status "Sacred Redis state initialized"

# Initialize biological flow state
redis-cli hset biological_flow_state active_flows "0" > /dev/null
redis-cli hset biological_flow_state total_cycles "0" > /dev/null
redis-cli hset biological_flow_state last_cycle_time "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" > /dev/null
redis-cli hset biological_flow_state flow_health "healthy" > /dev/null
print_status "Biological flow state initialized"

# Check if port 8080 is available
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    print_warning "Port 8080 is already in use. Sacred bridge may conflict."
    print_info "To stop existing service: lsof -ti:8080 | xargs kill -9"
else
    print_status "Port 8080 available for sacred manifestation"
fi

# Create systemd service file (optional)
if command -v systemctl &> /dev/null && [ "$1" = "--systemd" ]; then
    echo "🔧 Creating systemd service..."
    SERVICE_FILE="/tmp/sacred-chat-bridge.service"
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Sacred Chat Bridge - Sphere-aware chat system
After=network.target redis.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/node index.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF
    
    sudo mv "$SERVICE_FILE" /etc/systemd/system/
    sudo systemctl daemon-reload
    print_status "Systemd service created. Use 'sudo systemctl enable sacred-chat-bridge' to enable"
fi

# Test the system
echo "🧪 Testing sacred system initialization..."
timeout 10s node -e "
import('./index.js').then(async (module) => {
    const { sacredChatBridgeSystem } = module;
    await sacredChatBridgeSystem.initialize();
    const status = await sacredChatBridgeSystem.getSystemStatus();
    console.log('System status:', status.status);
    await sacredChatBridgeSystem.shutdown();
    process.exit(0);
}).catch(err => {
    console.error('Test failed:', err.message);
    process.exit(1);
});
" && print_status "System test passed" || print_error "System test failed"

echo ""
echo "🎉 Sacred Chat Bridge deployment complete!"
echo ""
echo "📋 System Information:"
echo "   🌐 WebSocket server: ws://localhost:8080"
echo "   🔐 Sacred validation: ENABLED"
echo "   🌊 Biological flow: ACTIVE"
echo "   🔬 Geometric cleanliness: ENFORCED"
echo "   📊 Sphere tracking: Redis-backed"
echo ""
echo "🚀 Start commands:"
echo "   Production: npm start"
echo "   Development: npm run dev"
echo "   Status check: npm run status"
echo ""
echo "🔧 Management commands:"
echo "   View logs: npm run logs"
echo "   Validate system: npm run validate"
echo "   Sphere manager: npm run sphere"
echo ""
echo "📡 Connection test:"
echo "   wscat -c ws://localhost:8080"
echo ""
echo "◼ Sacred manifestation ready for activation"

# Optional: Start the system immediately
if [ "$1" = "--start" ]; then
    echo "🟡 Starting Sacred Chat Bridge system..."
    npm start
fi
