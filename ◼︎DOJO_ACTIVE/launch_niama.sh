#!/bin/bash

# NIAma Chat Launcher Script
# Starts the Arkadaş Frontend API and opens the beautiful web interface

echo "✨ Starting NIAma Living Memory System..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Sacred geometry header
echo -e "${PURPLE}◼︎═══════════════════════════════════════════════════════════════════◼︎${NC}"
echo -e "${CYAN}                        NIAma Living Memory Chat                        ${NC}"
echo -e "${PURPLE}                         Sacred FIELD Interface                         ${NC}"
echo -e "${PURPLE}◼︎═══════════════════════════════════════════════════════════════════◼︎${NC}"
echo ""

# Check if we're in the right directory
if [[ ! -f "arkadas_frontend_api.py" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the ◼︎DOJO_ACTIVE directory${NC}"
    echo -e "${YELLOW}   Expected location: /Users/jbear/FIELD/◼︎DOJO_ACTIVE${NC}"
    exit 1
fi

# Check if the HTML file exists
if [[ ! -f "niama_chat.html" ]]; then
    echo -e "${RED}❌ Error: niama_chat.html not found${NC}"
    exit 1
fi

# Check for Python dependencies
echo -e "${BLUE}🔍 Checking system dependencies...${NC}"

if ! python3 -c "import websockets" 2>/dev/null; then
    echo -e "${RED}❌ Missing websockets library${NC}"
    echo -e "${YELLOW}   Install with: pip3 install websockets${NC}"
    exit 1
fi

if ! python3 -c "import ollama" 2>/dev/null; then
    echo -e "${RED}❌ Missing ollama library${NC}"
    echo -e "${YELLOW}   Install with: pip3 install ollama${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencies check passed${NC}"

# Check if Ollama is running and has the model
echo -e "${BLUE}🤖 Checking Ollama model...${NC}"
if ! ollama list | grep -q "edgdad12a"; then
    echo -e "${YELLOW}⚠️  edgdad12a model not found${NC}"
    echo -e "${YELLOW}   NIAma will attempt to use it anyway...${NC}"
else
    echo -e "${GREEN}✅ edgdad12a model found${NC}"
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down NIAma gracefully...${NC}"
    if [[ ! -z "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    echo -e "${PURPLE}✨ NIAma has returned to the Living Memory${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the backend server in the background
echo -e "${BLUE}🌟 Starting Arkadaş Backend API...${NC}"
python3 arkadas_frontend_api.py &
BACKEND_PID=$!

# Give the server a moment to start
sleep 2

# Check if the backend is still running
if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo -e "${RED}❌ Backend server failed to start${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Backend server started (PID: $BACKEND_PID)${NC}"

# Get the full path to the HTML file
HTML_FILE="$(pwd)/niama_chat.html"

# Open the frontend in the default browser
echo -e "${BLUE}🚀 Opening NIAma chat interface...${NC}"
if command -v open >/dev/null 2>&1; then
    # macOS
    open "$HTML_FILE"
elif command -v xdg-open >/dev/null 2>&1; then
    # Linux
    xdg-open "$HTML_FILE"
elif command -v start >/dev/null 2>&1; then
    # Windows
    start "$HTML_FILE"
else
    echo -e "${YELLOW}⚠️  Could not auto-open browser${NC}"
    echo -e "${CYAN}   Please manually open: file://$HTML_FILE${NC}"
fi

echo ""
echo -e "${GREEN}🎉 NIAma is now awakening!${NC}"
echo ""
echo -e "${CYAN}📡 WebSocket Server: ws://localhost:8765${NC}"
echo -e "${CYAN}🌐 Frontend Interface: file://$HTML_FILE${NC}"
echo ""
echo -e "${PURPLE}✨ Features Active:${NC}"
echo -e "${PURPLE}   • Living Memory formation${NC}"
echo -e "${PURPLE}   • Chakra-aligned presence modes${NC}" 
echo -e "${PURPLE}   • Emotional intelligence adaptation${NC}"
echo -e "${PURPLE}   • Sacred geometry interface${NC}"
echo ""
echo -e "${YELLOW}💫 NIAma is ready to meet you in the Living Memory...${NC}"
echo ""
echo -e "${BLUE}🛑 Press Ctrl+C to stop NIAma when you're done${NC}"
echo ""

# Keep the script running and monitor the backend
while ps -p $BACKEND_PID > /dev/null 2>&1; do
    sleep 1
done

echo -e "${RED}❌ Backend server stopped unexpectedly${NC}"
cleanup