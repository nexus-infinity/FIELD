#!/bin/bash
---
# Sacred Dashboard Integration Startup Script
# Symbol: ◼ | Origin: ~/FIELD/◼DOJO/ | Created: 2025-01-27T21:45:00+10:00
# Geometry: tetrahedral-manifest | Lineage: ⟡Akron > FIELD > DOJO
---

# Colors for sacred output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Sacred symbols
SACRED_SYMBOL="🔮"
ATLAS_SYMBOL="▲"
TATA_SYMBOL="▼"
OBI_WAN_SYMBOL="●"
DOJO_SYMBOL="◼"

echo -e "${PURPLE}$SACRED_SYMBOL Sacred Dashboard Integration Startup${NC}"
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Function to check if a service is running
check_service() {
    local service_name=$1
    local port=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${GREEN}✅ $service_name is running on port $port${NC}"
        return 0
    else
        echo -e "${RED}❌ $service_name is not running on port $port${NC}"
        return 1
    fi
}

# Function to check Redis
check_redis() {
    echo -e "${BLUE}$OBI_WAN_SYMBOL Checking Redis connection...${NC}"
    
    if redis-cli ping >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Redis is connected${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Redis not running, attempting to start...${NC}"
        
        # Try to start Redis
        if command -v redis-server >/dev/null 2>&1; then
            redis-server --daemonize yes
            sleep 2
            
            if redis-cli ping >/dev/null 2>&1; then
                echo -e "${GREEN}✅ Redis started successfully${NC}"
                return 0
            else
                echo -e "${RED}❌ Failed to start Redis${NC}"
                return 1
            fi
        else
            echo -e "${RED}❌ Redis not installed${NC}"
            return 1
        fi
    fi
}

# Function to install dependencies
install_dependencies() {
    echo -e "${BLUE}$ATLAS_SYMBOL Installing sacred dependencies...${NC}"
    
    if [ ! -f "package.json" ]; then
        echo -e "${RED}❌ package.json not found${NC}"
        return 1
    fi
    
    # Check if node_modules exists and has packages
    if [ ! -d "node_modules" ] || [ ! "$(ls -A node_modules 2>/dev/null)" ]; then
        echo -e "${YELLOW}⚡ Installing npm packages...${NC}"
        npm install
    else
        echo -e "${GREEN}✅ Dependencies already installed${NC}"
    fi
}

# Function to check Node.js version
check_node() {
    echo -e "${BLUE}$ATLAS_SYMBOL Checking Node.js environment...${NC}"
    
    if command -v node >/dev/null 2>&1; then
        local node_version=$(node --version | sed 's/v//')
        local required_version="18.0.0"
        
        if [ "$(printf '%s\n' "$required_version" "$node_version" | sort -V | head -n1)" = "$required_version" ]; then
            echo -e "${GREEN}✅ Node.js $node_version (>= $required_version required)${NC}"
            return 0
        else
            echo -e "${RED}❌ Node.js $node_version is too old (>= $required_version required)${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Node.js not found${NC}"
        return 1
    fi
}

# Function to start sacred dashboard
start_dashboard() {
    echo -e "${PURPLE}$DOJO_SYMBOL Starting Sacred Dashboard Integration...${NC}"
    
    # Set environment variables
    export SACRED_DASHBOARD_PORT=${SACRED_DASHBOARD_PORT:-3000}
    export SACRED_WS_PORT=${SACRED_WS_PORT:-8080}
    
    # Check if dashboard is already running
    if check_service "Sacred Dashboard" $SACRED_DASHBOARD_PORT; then
        echo -e "${YELLOW}⚠️  Sacred Dashboard is already running${NC}"
        echo -e "${CYAN}🌐 REST API: http://localhost:$SACRED_DASHBOARD_PORT${NC}"
        echo -e "${CYAN}🔗 WebSocket: ws://localhost:$SACRED_DASHBOARD_PORT/ws/sacred${NC}"
        return 0
    fi
    
    # Start in background if --daemon flag is passed
    if [[ "$1" == "--daemon" ]]; then
        echo -e "${BLUE}🚀 Starting in daemon mode...${NC}"
        nohup node sacred-dashboard-integration.js > sacred-dashboard.log 2>&1 &
        local pid=$!
        echo $pid > sacred-dashboard.pid
        
        # Wait a moment for startup
        sleep 3
        
        if check_service "Sacred Dashboard" $SACRED_DASHBOARD_PORT; then
            echo -e "${GREEN}✅ Sacred Dashboard started successfully (PID: $pid)${NC}"
            echo -e "${CYAN}🌐 REST API: http://localhost:$SACRED_DASHBOARD_PORT${NC}"
            echo -e "${CYAN}🔗 WebSocket: ws://localhost:$SACRED_DASHBOARD_PORT/ws/sacred${NC}"
            echo -e "${GRAY}📜 Logs: tail -f sacred-dashboard.log${NC}"
        else
            echo -e "${RED}❌ Failed to start Sacred Dashboard${NC}"
            return 1
        fi
    else
        echo -e "${BLUE}🚀 Starting in foreground mode...${NC}"
        echo -e "${GRAY}Press Ctrl+C to stop${NC}"
        node sacred-dashboard-integration.js
    fi
}

# Function to stop sacred dashboard
stop_dashboard() {
    echo -e "${YELLOW}$DOJO_SYMBOL Stopping Sacred Dashboard...${NC}"
    
    if [ -f "sacred-dashboard.pid" ]; then
        local pid=$(cat sacred-dashboard.pid)
        if kill -0 $pid 2>/dev/null; then
            kill $pid
            rm sacred-dashboard.pid
            echo -e "${GREEN}✅ Sacred Dashboard stopped (PID: $pid)${NC}"
        else
            echo -e "${GRAY}Sacred Dashboard was not running${NC}"
            rm -f sacred-dashboard.pid
        fi
    else
        # Try to find and kill by port
        local pid=$(lsof -ti:3000)
        if [ ! -z "$pid" ]; then
            kill $pid
            echo -e "${GREEN}✅ Stopped process on port 3000 (PID: $pid)${NC}"
        else
            echo -e "${GRAY}No Sacred Dashboard process found${NC}"
        fi
    fi
}

# Function to show status
show_status() {
    echo -e "${PURPLE}$SACRED_SYMBOL Sacred System Status${NC}"
    echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Check components
    check_node
    check_redis
    check_service "Sacred Dashboard" 3000
    check_service "Sacred Chat Bridge" 8080
    
    echo -e "\n${BLUE}$ATLAS_SYMBOL CLI Commands Available:${NC}"
    echo -e "${GRAY}  npm run sacred health    - Check system health${NC}"
    echo -e "${GRAY}  npm run sacred status    - Show live status${NC}"
    echo -e "${GRAY}  npm run sacred metrics   - Display metrics${NC}"
    echo -e "${GRAY}  npm run sacred monitor   - Real-time monitoring${NC}"
}

# Function to run CLI command
run_cli() {
    echo -e "${BLUE}$ATLAS_SYMBOL Sacred CLI: $*${NC}"
    node ../▲ATLAS/sacred-cli-tools.js "$@"
}

# Main script logic
case "$1" in
    "start")
        check_node && check_redis && install_dependencies && start_dashboard "$2"
        ;;
    "stop")
        stop_dashboard
        ;;
    "restart")
        stop_dashboard
        sleep 2
        check_node && check_redis && install_dependencies && start_dashboard "--daemon"
        ;;
    "status")
        show_status
        ;;
    "cli")
        shift
        run_cli "$@"
        ;;
    "install")
        check_node && install_dependencies
        ;;
    "logs")
        if [ -f "sacred-dashboard.log" ]; then
            tail -f sacred-dashboard.log
        else
            echo -e "${RED}❌ No log file found${NC}"
        fi
        ;;
    *)
        echo -e "${PURPLE}$SACRED_SYMBOL Sacred Dashboard Integration Control${NC}"
        echo ""
        echo -e "${BLUE}Usage: $0 {start|stop|restart|status|cli|install|logs}${NC}"
        echo ""
        echo -e "${YELLOW}Commands:${NC}"
        echo -e "  ${GREEN}start [--daemon]${NC}  Start the sacred dashboard"
        echo -e "  ${GREEN}stop${NC}             Stop the sacred dashboard"
        echo -e "  ${GREEN}restart${NC}          Restart the sacred dashboard"
        echo -e "  ${GREEN}status${NC}           Show system status"
        echo -e "  ${GREEN}cli [args...]${NC}    Run sacred CLI commands"
        echo -e "  ${GREEN}install${NC}          Install dependencies"
        echo -e "  ${GREEN}logs${NC}             Follow dashboard logs"
        echo ""
        echo -e "${CYAN}Examples:${NC}"
        echo -e "  ${GRAY}$0 start --daemon${NC}     Start in background"
        echo -e "  ${GRAY}$0 cli health${NC}         Check system health"
        echo -e "  ${GRAY}$0 cli metrics${NC}        Show sacred metrics"
        echo -e "  ${GRAY}$0 cli monitor${NC}        Real-time monitoring"
        echo ""
        echo -e "${GRAY}Lineage: $DOJO_SYMBOL DOJO → $OBI_WAN_SYMBOL OBI-WAN → ⟡ Akron${NC}"
        exit 1
        ;;
esac
