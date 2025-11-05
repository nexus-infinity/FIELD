#!/bin/zsh
# ═══════════════════════════════════════════════════════════════════════════════
# FIELD RESOURCE ECOSYSTEM (FRE) - Professional Shell Integration
# ═══════════════════════════════════════════════════════════════════════════════
# 
# Professional unified front-end for all FIELD system modules and business operations.
# This file should be sourced in your .zshrc to enable FRE commands and functionality.
#
# Integration with:
# - Universal Data Processor
# - Berjak CRM System
# - Sacred Geometry Orchestration
# - FIELD Navigation Systems
# - Business Intelligence Tools
# ═══════════════════════════════════════════════════════════════════════════════

# FRE System Paths
export FRE_ROOT="$HOME/FIELD/◎_source_core"
export FRE_MAIN="$FRE_ROOT/field_resource_ecosystem.py"
export FRE_DATA_PROCESSOR="$FRE_ROOT/universal_data_processor.py"
export FRE_DASHBOARD="$FRE_ROOT/dashboard.py"
export BERJAK_CRM_ROOT="$HOME/.berjak_crm"

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN FRE COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

# Main FRE Interface
alias fre="python3 '$FRE_MAIN'"
alias field-resource-ecosystem="python3 '$FRE_MAIN'"

# Quick FRE Commands
alias fre-status="python3 '$FRE_MAIN' status"
alias fre-dashboard="python3 '$FRE_MAIN' dashboard"
alias fre-process="python3 '$FRE_MAIN' process"
alias fre-report="python3 '$FRE_MAIN' report"
alias fre-help="python3 '$FRE_MAIN' help"

# ═══════════════════════════════════════════════════════════════════════════════
# DATA PROCESSING COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

# Universal Data Processor
alias data-process="cd '$FRE_ROOT' && python3 universal_data_processor.py"
alias data-scan="cd '$FRE_ROOT' && python3 universal_data_processor.py --scan-only"
alias data-setup="cd '$FRE_ROOT' && python3 universal_data_processor.py --setup"
alias data-dashboard="cd '$FRE_ROOT' && python3 dashboard.py"

# Data Source Quick Access
alias goto-czur="cd '$HOME/CZURImages' && ls -la"
alias goto-data="cd '$HOME/DATA' && ls -la"  
alias goto-downloads="cd '$HOME/Downloads' && ls -la"
alias goto-quarantine="cd '$HOME/FIELD-QUARANTINE' && ls -la"

# ═══════════════════════════════════════════════════════════════════════════════
# BERJAK CRM INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

# CRM System Access
alias crm="python3 '$FRE_MAIN' 3"  # Launch CRM interface
alias crm-status="python3 '$FRE_MAIN' status | grep -i crm"
alias crm-web="open '$FRE_ROOT/berjak_crm_interface.html'"  # Beautiful web interface
alias berjak="cd '$BERJAK_CRM_ROOT' && ls -la"

# Google Cloud Integration (Berjak)
alias gcloud-berjak="gcloud config set account jeremy.rich@berjak.com.au"
alias gcloud-project="gcloud config set project berjak-development-project"

# ═══════════════════════════════════════════════════════════════════════════════
# FIELD SYSTEM NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════

# Enhanced FIELD Navigation (keeping existing but improving)
alias field="cd '$HOME/FIELD' && ls -la"
alias field-core="cd '$FRE_ROOT' && ls -la"
alias field-atlas="cd '$HOME/FIELD/▲ATLAS' && ls -la"
alias field-dev="cd '$HOME/FIELD-DEV' && ls -la"
alias field-living="cd '$HOME/FIELD-LIVING' && ls -la"
alias field-reports="cd '$HOME/FIELD-REPORTS' && ls -la"

# Professional FIELD Management
alias field-overview="fre-status && echo '\n🎯 Quick Navigation:' && echo '  field-core    - Core system' && echo '  field-atlas   - Knowledge base' && echo '  field-dev     - Development' && echo '  field-living  - Production'"

# ═══════════════════════════════════════════════════════════════════════════════
# BUSINESS INTELLIGENCE & ANALYTICS  
# ═══════════════════════════════════════════════════════════════════════════════

# Business Dashboard
alias bi="python3 '$FRE_MAIN' dashboard"
alias business-dashboard="python3 '$FRE_MAIN' dashboard"
alias analytics="fre-dashboard && fre-report"

# System Health & Monitoring
alias health-check="python3 '$FRE_MAIN' status"
alias system-status="fre-status"
alias field-health="health-check"

# ═══════════════════════════════════════════════════════════════════════════════
# AUTOMATION & WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════════

# Automation Management
alias automation-setup="python3 '$FRE_DATA_PROCESSOR' --setup"
alias automation-status="launchctl list | grep field"
alias automation-logs="tail -f '$FRE_ROOT/logs/data_processor.log'"

# Quick Workflow Commands
alias morning-routine="fre-status && data-scan && echo '\n☀️ Morning FRE check complete!'"
alias evening-report="fre-report && echo '\n🌙 Evening report generated!'"

# ═══════════════════════════════════════════════════════════════════════════════
# SCANNER & INPUT INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

# Scanner Workflow
alias scan-process="echo '🔄 Processing scanned documents...' && data-process"
alias scan-status="ls -la '$HOME/CZURImages' && echo '\n📊 Scanner files ready for processing'"

# Phone & Mobile Integration  
alias phone-sync="echo '📱 Checking Downloads for mobile files...' && ls -la '$HOME/Downloads' | grep -E '(Genius|Scanner|IMG_|Photo)'"

# ═══════════════════════════════════════════════════════════════════════════════
# PROFESSIONAL UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

# System Information
fre-info() {
    echo "═══════════════════════════════════════════════════════════════════"
    echo "🔮 FIELD RESOURCE ECOSYSTEM (FRE) - System Information"
    echo "═══════════════════════════════════════════════════════════════════"
    echo "📍 FRE Root: $FRE_ROOT"
    echo "💼 Berjak CRM: $BERJAK_CRM_ROOT"
    echo "⚙️  Main Interface: fre"
    echo "📊 Quick Dashboard: fre-dashboard"
    echo "🔄 Data Processing: data-process"
    echo "💼 CRM Access: crm"
    echo "🏥 Health Check: health-check"
    echo "═══════════════════════════════════════════════════════════════════"
}

# Professional Environment Check
fre-env-check() {
    echo "🔍 FRE ENVIRONMENT CHECK"
    echo "────────────────────────"
    
    # Check core components
    [[ -d "$FRE_ROOT" ]] && echo "✅ FRE Core: Ready" || echo "❌ FRE Core: Missing"
    [[ -f "$FRE_MAIN" ]] && echo "✅ Main Interface: Ready" || echo "❌ Main Interface: Missing"
    [[ -f "$FRE_DATA_PROCESSOR" ]] && echo "✅ Data Processor: Ready" || echo "❌ Data Processor: Missing"
    [[ -d "$BERJAK_CRM_ROOT" ]] && echo "✅ Berjak CRM: Connected" || echo "⚠️ Berjak CRM: Not found"
    
    # Check Python environment
    which python3 > /dev/null && echo "✅ Python3: Available" || echo "❌ Python3: Missing"
    
    # Check FIELD directories
    [[ -d "$HOME/FIELD" ]] && echo "✅ FIELD System: Active" || echo "❌ FIELD System: Missing"
}

# Professional File Search within FRE
fre-find() {
    local search_term="$1"
    if [[ -z "$search_term" ]]; then
        echo "Usage: fre-find <search-term>"
        echo "Searches across all FIELD directories for files/folders matching the term"
        return 1
    fi
    
    echo "🔍 Searching FIELD system for: $search_term"
    echo "────────────────────────────────────────────"
    
    for field_dir in FIELD FIELD-DEV FIELD-LIVING FIELD-QUARANTINE FIELD-REPORTS; do
        if [[ -d "$HOME/$field_dir" ]]; then
            echo "\n📁 Searching $field_dir:"
            find "$HOME/$field_dir" -name "*$search_term*" -type f 2>/dev/null | head -5
        fi
    done
}

# Quick Business Context
fre-context() {
    echo "💼 BUSINESS CONTEXT - $(date '+%Y-%m-%d %H:%M')"
    echo "══════════════════════════════════════════════"
    
    # System status
    python3 "$FRE_MAIN" status 2>/dev/null | head -10
    
    # Recent activity
    if [[ -f "$FRE_ROOT/logs/data_processor.log" ]]; then
        echo "\n📊 Recent Activity:"
        tail -3 "$FRE_ROOT/logs/data_processor.log" 2>/dev/null
    fi
    
    # Quick metrics
    echo "\n📈 Quick Metrics:"
    [[ -d "$HOME/CZURImages" ]] && echo "  Scanner Files: $(find "$HOME/CZURImages" -type f | wc -l | tr -d ' ')"
    [[ -d "$HOME/DATA" ]] && echo "  DATA Files: $(find "$HOME/DATA" -type f | wc -l | tr -d ' ')"
}

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED PROMPT INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

# FRE Status in Prompt (enhances existing field_prompt)
fre_prompt_status() {
    local status=""
    
    # Check if we're in a FIELD directory
    case "$PWD" in
        *FIELD*)
            # Check FRE system health
            if [[ -f "$FRE_MAIN" ]] && [[ -d "$BERJAK_CRM_ROOT" ]]; then
                status="🔮💼"  # FRE + CRM active
            elif [[ -f "$FRE_MAIN" ]]; then
                status="🔮"     # FRE active
            else
                status="⚠️"     # FIELD but no FRE
            fi
            ;;
        *)
            # Check if automation is running
            if launchctl list 2>/dev/null | grep -q "field"; then
                status="🤖"     # Automation active
            fi
            ;;
    esac
    
    echo "$status"
}

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZATION & STARTUP
# ═══════════════════════════════════════════════════════════════════════════════

# FRE System Initialization Check
fre_init_check() {
    # Only run if in interactive shell
    if [[ $- == *i* ]] && [[ -f "$FRE_MAIN" ]]; then
        # Quick silent health check on startup
        local health_score=$(python3 "$FRE_MAIN" status 2>/dev/null | grep -o "[0-9]\+\.[0-9]\+%" | head -1)
        
        if [[ -n "$health_score" ]]; then
            local score_num=$(echo "$health_score" | cut -d'%' -f1)
            if (( $(echo "$score_num < 70" | bc -l) 2>/dev/null )); then
                echo "⚠️  FRE System needs attention. Run 'health-check' for details."
            fi
        fi
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# HELP & DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

# Comprehensive FRE Help
fre-commands() {
    echo "🔮 FIELD RESOURCE ECOSYSTEM - Command Reference"
    echo "════════════════════════════════════════════════"
    echo ""
    echo "🎯 MAIN COMMANDS:"
    echo "  fre                 - Launch FRE main interface"
    echo "  fre-status          - System status overview"
    echo "  fre-dashboard       - Business intelligence dashboard"
    echo "  fre-process         - Process new data files"
    echo "  fre-report          - Generate system reports"
    echo ""
    echo "🔄 DATA PROCESSING:"
    echo "  data-process        - Run universal data processor"
    echo "  data-scan           - Scan for new files only"
    echo "  data-setup          - Setup automation"
    echo "  data-dashboard      - View processing dashboard"
    echo ""
    echo "💼 BUSINESS & CRM:"
    echo "  crm                 - Access Berjak CRM interface"
    echo "  crm-web             - Launch beautiful web interface"
    echo "  business-dashboard  - Launch business metrics"
    echo "  analytics           - View analytics summary"
    echo ""
    echo "🏗  FIELD NAVIGATION:"
    echo "  field-core          - Navigate to core system"
    echo "  field-atlas         - Navigate to knowledge base"
    echo "  field-dev           - Navigate to development"
    echo "  field-living        - Navigate to production"
    echo ""
    echo "🔧 UTILITIES:"
    echo "  health-check        - Comprehensive system health"
    echo "  fre-env-check       - Environment validation"
    echo "  fre-find <term>     - Search across FIELD system"
    echo "  fre-context         - Current business context"
    echo ""
    echo "⚡ QUICK WORKFLOWS:"
    echo "  morning-routine     - Morning system check"
    echo "  evening-report      - Evening report generation"
    echo "  scan-process        - Process scanned documents"
    echo ""
    echo "Type any command above or 'fre' for the main interface"
}

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT AND FINALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

# Make key functions available globally
export -f fre-info
export -f fre-env-check
export -f fre-find
export -f fre-context
export -f fre_prompt_status
export -f fre-commands

# Integration complete message (only show once per session)
if [[ -z "$FRE_INTEGRATION_LOADED" ]]; then
    export FRE_INTEGRATION_LOADED=1
    
    # Show integration success (only in interactive shells)
    if [[ $- == *i* ]] && [[ -f "$FRE_MAIN" ]]; then
        echo "✅ Field Resource Ecosystem (FRE) integration loaded"
        echo "   Type 'fre-commands' to see all available commands"
        echo "   Type 'fre' to launch the main interface"
        
        # Run initialization check
        fre_init_check
    fi
fi