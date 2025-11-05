#!/bin/bash

# Sacred DOJO MCP Server Startup Script
# Optimized for Mac Studio M2 → iPhone 14 → Apple Watch Ultra

echo "🔥 Initializing Sacred DOJO Ecosystem..."

# Set base directory
FIELD_BASE="/Users/jbear/FIELD"
MCP_BASE="$FIELD_BASE/_MCP"
DOJO_BASE="$FIELD_BASE/◼︎DOJO"

# Create MCP directory structure
mkdir -p "$MCP_BASE/servers"
mkdir -p "$MCP_BASE/logs"
mkdir -p ~/.config/mcp

echo "◎ Setting up Sacred Memory Bus..."

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "Installing Redis via Homebrew..."
    brew install redis
fi

# Start Redis for unified memory bus
echo "◎ Starting Sacred Core Memory Bus..."
redis-server --port 6379 --daemonize yes

# Wait for Redis to be ready
sleep 2

# Test Redis connection
if redis-cli ping | grep -q "PONG"; then
    echo "✅ Sacred Memory Bus Connected"
else
    echo "❌ Redis connection failed"
    exit 1
fi

# Create MCP config for Xcode Copilot
echo "📝 Creating MCP config for Xcode Copilot..."
cat > ~/.config/mcp/xcode-copilot.json << 'EOF'
{
  "servers": {
    "sacred-dojo-system": {
      "type": "stdio",
      "command": "python3",
      "args": ["/Users/jbear/FIELD/_MCP/dojo_bridge_server.py"],
      "env": {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "FIELD_BASE": "/Users/jbear/FIELD",
        "DOJO_BASE": "/Users/jbear/FIELD/◼︎DOJO",
        "PYTHONPATH": "/Users/jbear/FIELD/_MCP"
      }
    }
  }
}
EOF

echo ""
echo "🌟 Sacred DOJO Ecosystem Status:"
echo "   ◼︎ DOJO Project: Ready"
echo "   📱 iPhone 14: Awaiting Deployment"
echo "   ⌚ Apple Watch Ultra: Companion Ready"
echo "   💻 Mac Studio M2: Core Processing Active"
echo ""
echo "✅ Setup Complete! Next: Configure Xcode Copilot"
echo "🔄 Restart Xcode to load MCP connection"
