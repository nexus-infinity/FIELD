#!/bin/bash

#==============================================================================
# SDR Ingestion Canonicalization Script
#
# This script archives legacy SDR ingestion scripts and ensures the system
# uses the canonical SDR ingestion system, as defined by the
# `◎_sdr_symbol_mapping.yaml` file.
#
#==============================================================================

#--- Configuration ---#

# The directory where legacy scripts will be archived
ARCHIVE_DIR="/Users/jbear/FIELD_ARCHIVE/legacy_sdr_scripts/$(date +'%Y-%m-%d_%H-%M-%S')"

# A log file to record the archived scripts
ARCHIVE_LOG="$ARCHIVE_DIR/archive_log.txt"

# The root directory to search for legacy scripts
SEARCH_DIR="/Users/jbear/FIELD"

# The list of legacy script files to be archived
LEGACY_SCRIPTS=(
    "/Users/jbear/FIELD/sdr_flow.py"
    "/Users/jbear/FIELD/◼︎DOJO/test_sdr_connectors.py"
    "/Users/jbear/FIELD/◼︎DOJO/field_sdr_chakra_integration.py"
    "/Users/jbear/FIELD/◼︎DOJO/●sdr_ingestion_script.py"
    "/Users/jbear/FIELD/◼︎DOJO/notion_sdr_sync_engine.py"
    "/Users/jbear/FIELD/sdr_harmonic_pipeline.py"
    "/Users/jbear/FIELD-DEV/◼_dojo/implement_sdr_auth.sh"
    "/Users/jbear/FIELD-LIVING/●sdr_bridge.py"
)

#--- Functions ---#

# Log messages to the console and a log file
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" | tee -a "$ARCHIVE_LOG"
}

#--- Main ---#

log "Starting SDR ingestion canonicalization process..."

mkdir -p "$ARCHIVE_DIR"

log "Archiving legacy SDR scripts..."

for script in "${LEGACY_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        log "Archiving $script to $ARCHIVE_DIR"
        mv "$script" "$ARCHIVE_DIR/"
    else
        log "WARNING: Legacy script $script not found. It may have been previously archived or removed."
    fi
done

log "Updating references to legacy scripts (manual step required)."
log "Please review the project to ensure all references to the archived scripts have been updated to use the canonical SDR ingestion system."

log "SDR ingestion canonicalization process complete."

exit 0
