#!/bin/bash

#==============================================================================
# MCP Environment Manager
#
# This script centralizes the configuration and management of MCP server
# environments. It provides functions to start, stop, and check the status of
# individual or all chakra servers.
#
# Each chakra's configuration is defined in a dedicated .plist file within
# ~/Library/LaunchAgents/. These files contain the necessary environment
# variables (FIELD_SYMBOL, DOJO_GATE, PORT, etc.) and the path to the
# server's Python script.
#
# This script is designed to be the canonical way to manage MCP environments,
# deprecating any previous, disparate methods.
#
#==============================================================================

#--- Configuration ---#

# Directory containing the LaunchAgent plist files
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

# Base name for the chakra server plist files
PLIST_BASE_NAME="ai.field.chakra"

# Log file for this script's operations
LOG_FILE="$HOME/Library/Logs/mcp_env_manager.log"

#--- Functions ---#

# Log messages to the console and a log file
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Start a specific chakra server
start_chakra() {
    local chakra_name="$1"
    local plist_file="$LAUNCH_AGENTS_DIR/${PLIST_BASE_NAME}.${chakra_name}.plist"

    if [ -f "$plist_file" ]; then
        log "Starting ${chakra_name} server..."
        launchctl load -w "$plist_file"
        log "${chakra_name} server started."
    else
        log "ERROR: Plist file for ${chakra_name} not found at ${plist_file}"
    fi
}

# Stop a specific chakra server
stop_chakra() {
    local chakra_name="$1"
    local plist_file="$LAUNCH_AGENTS_DIR/${PLIST_BASE_NAME}.${chakra_name}.plist"

    if [ -f "$plist_file" ]; then
        log "Stopping ${chakra_name} server..."
        launchctl unload -w "$plist_file"
        log "${chakra_name} server stopped."
    else
        log "ERROR: Plist file for ${chakra_name} not found at ${plist_file}"
    fi
}

# Check the status of a specific chakra server
status_chakra() {
    local chakra_name="$1"
    local label="${PLIST_BASE_NAME}.${chakra_name}"
    
    log "Checking status of ${chakra_name} server..."
    launchctl list | grep "$label" || echo "${chakra_name} server is not running."
}

# Start all chakra servers
start_all() {
    log "Starting all chakra servers..."
    for plist_file in "$LAUNCH_AGENTS_DIR/${PLIST_BASE_NAME}"*.plist; do
        local chakra_name=$(basename "$plist_file" .plist | sed "s/${PLIST_BASE_NAME}.//")
        start_chakra "$chakra_name"
    done
    log "All chakra servers started."
}

# Stop all chakra servers
stop_all() {
    log "Stopping all chakra servers..."
    for plist_file in "$LAUNCH_AGENTS_DIR/${PLIST_BASE_NAME}"*.plist; do
        local chakra_name=$(basename "$plist_file" .plist | sed "s/${PLIST_BASE_NAME}.//")
        stop_chakra "$chakra_name"
    done
    log "All chakra servers stopped."
}

#--- Main ---#

# Display usage information
usage() {
    echo "Usage: $0 {start|stop|status|start_all|stop_all} [chakra_name]"
    echo "  - start [chakra_name]: Start the specified chakra server."
    echo "  - stop [chakra_name]: Stop the specified chakra server."
    echo "  - status [chakra_name]: Check the status of the specified chakra server."
    echo "  - start_all: Start all chakra servers."
    echo "  - stop_all: Stop all chakra servers."
}

# Parse command-line arguments
case "$1" in
    start)
        [ -z "$2" ] && usage && exit 1
        start_chakra "$2"
        ;;
    stop)
        [ -z "$2" ] && usage && exit 1
        stop_chakra "$2"
        ;;
    status)
        [ -z "$2" ] && usage && exit 1
        status_chakra "$2"
        ;;
    start_all)
        start_all
        ;;
    stop_all)
        stop_all
        ;;
    *)
        usage
        exit 1
        ;;
esac

exit 0
