#!/bin/bash
# FIELD System Configuration Setup and Validation Script
# Purpose: Initialize, validate, and fix FIELD system configurations
# Created: 2025-08-22

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Sacred banner
echo -e "${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                    FIELD SYSTEM SETUP                       ║
║              Sacred Configuration Harmonizer                ║
║                                                              ║
║  ●OBI-WAN  ▼TATA  ▲ATLAS  ◼︎DOJO                              ║
║  Memory → Truth → Logic → Manifestation                     ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIELD_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🌟 Initializing FIELD System Configuration...${NC}"
echo "   FIELD Root: $FIELD_ROOT"
echo ""

# Function to log messages
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check port availability
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is free
    fi
}

# Function to validate environment file
validate_env_file() {
    local env_file=$1
    local env_name=$2
    
    log_info "Validating $env_name environment file..."
    
    if [[ ! -f "$env_file" ]]; then
        log_error "$env_name environment file not found: $env_file"
        return 1
    fi
    
    # Check for required variables
    local required_vars=("OPENAI_API_KEY" "PORT" "SACRED_FREQUENCY")
    local missing_vars=()
    
    while IFS= read -r line; do
        [[ $line =~ ^[[:space:]]*# ]] && continue  # Skip comments
        [[ -z $line ]] && continue  # Skip empty lines
        
        if [[ $line =~ ^([^=]+)= ]]; then
            var_name="${BASH_REMATCH[1]}"
            # Remove this var from required list if found
            required_vars=("${required_vars[@]/$var_name}")
        fi
    done < "$env_file"
    
    # Check if any required vars are still missing
    for var in "${required_vars[@]}"; do
        if [[ -n "$var" ]]; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        log_warning "$env_name missing variables: ${missing_vars[*]}"
        return 1
    else
        log_success "$env_name environment file is valid"
        return 0
    fi
}

# 1. Check Prerequisites
log_info "Checking system prerequisites..."

if ! command_exists "direnv"; then
    log_warning "direnv not found. Install with: brew install direnv"
fi

if ! command_exists "python3"; then
    log_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

if ! command_exists "node"; then
    log_warning "Node.js not found. Some features may not work."
fi

log_success "System prerequisites checked"

# 2. Validate directory structure
log_info "Validating FIELD directory structure..."

REQUIRED_DIRS=(
    "$FIELD_ROOT"
    "$FIELD_ROOT/FIELD-DEV" 
    "$FIELD_ROOT/FIELD-LIVING"
    "$FIELD_ROOT/.credentials_vault"
    "$FIELD_ROOT/scripts"
    "$FIELD_ROOT/●configs"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        log_success "Directory exists: $(basename "$dir")"
    else
        log_error "Missing directory: $dir"
        exit 1
    fi
done

# 3. Set up secure permissions
log_info "Setting up secure permissions..."

# Make API key loader executable
if [[ -f "$FIELD_ROOT/scripts/load_api_keys.sh" ]]; then
    chmod +x "$FIELD_ROOT/scripts/load_api_keys.sh"
    log_success "Made load_api_keys.sh executable"
fi

# Secure credentials vault
if [[ -d "$FIELD_ROOT/.credentials_vault" ]]; then
    chmod 700 "$FIELD_ROOT/.credentials_vault"
    log_success "Secured credentials vault permissions"
fi

# Secure API keys file
if [[ -f "$FIELD_ROOT/.credentials_vault/field_api_keys.env" ]]; then
    chmod 600 "$FIELD_ROOT/.credentials_vault/field_api_keys.env"
    log_success "Secured API keys file permissions"
fi

# 4. Validate environment configurations
log_info "Validating environment configurations..."

validate_env_file "$FIELD_ROOT/.env" "FIELD (Main)"
validate_env_file "$FIELD_ROOT/FIELD-DEV/.env" "FIELD-DEV"
validate_env_file "$FIELD_ROOT/FIELD-LIVING/.env" "FIELD-LIVING"

# 5. Check port configurations and conflicts
log_info "Checking sacred port configurations..."

# Define sacred ports for each environment
declare -A PROD_PORTS=(
    ["OBI-WAN"]=1369
    ["TATA"]=4320
    ["ATLAS"]=5281
    ["DOJO"]=7410
    ["REGISTRY"]=8888
    ["OBSERVER_LOOP"]=9630
    ["VALIDATOR"]=1111
    ["SANDBOX"]=3690
)

declare -A DEV_PORTS=(
    ["OBI-WAN"]=1469
    ["TATA"]=4420
    ["ATLAS"]=5381
    ["DOJO"]=7510
    ["REGISTRY"]=8988
    ["OBSERVER_LOOP"]=9730
    ["VALIDATOR"]=1211
    ["SANDBOX"]=3790
)

echo ""
log_info "Production port availability:"
for node in "${!PROD_PORTS[@]}"; do
    port=${PROD_PORTS[$node]}
    if check_port $port; then
        log_success "$node port $port is available"
    else
        log_warning "$node port $port is in use"
    fi
done

echo ""
log_info "Development port availability:"
for node in "${!DEV_PORTS[@]}"; do
    port=${DEV_PORTS[$node]}
    if check_port $port; then
        log_success "$node port $port is available (DEV)"
    else
        log_warning "$node port $port is in use (DEV)"
    fi
done

# 6. Test API key loading
log_info "Testing API key loading system..."

if [[ -f "$FIELD_ROOT/scripts/load_api_keys.sh" ]]; then
    # Source the script and check if keys are loaded
    source "$FIELD_ROOT/scripts/load_api_keys.sh" 2>/dev/null || true
    
    if [[ -n "${OPENAI_API_KEY:-}" ]] && [[ "$OPENAI_API_KEY" != "your_openai_api_key_here" ]]; then
        log_success "API keys are properly loaded"
    else
        log_warning "API keys may need configuration in .credentials_vault/field_api_keys.env"
    fi
else
    log_error "API key loader script not found"
fi

# 7. Validate configuration files
log_info "Validating sacred configuration files..."

CONFIG_FILES=(
    "$FIELD_ROOT/.fieldseal.yaml"
    "$FIELD_ROOT/resonance_config.json"
    "$FIELD_ROOT/●configs/atlas_config.json"
)

for config_file in "${CONFIG_FILES[@]}"; do
    if [[ -f "$config_file" ]]; then
        # Basic JSON validation for .json files
        if [[ "$config_file" == *.json ]]; then
            if python3 -m json.tool "$config_file" >/dev/null 2>&1; then
                log_success "Valid JSON: $(basename "$config_file")"
            else
                log_error "Invalid JSON: $(basename "$config_file")"
            fi
        else
            log_success "Found: $(basename "$config_file")"
        fi
    else
        log_error "Missing config file: $(basename "$config_file")"
    fi
done

# 8. Generate setup summary
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                      SETUP SUMMARY                          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

log_info "Configuration Status:"
echo "   📁 FIELD Root: $FIELD_ROOT"
echo "   🔐 Credentials Vault: $([ -d "$FIELD_ROOT/.credentials_vault" ] && echo "✅ Configured" || echo "❌ Missing")"
echo "   🔑 API Keys Loader: $([ -x "$FIELD_ROOT/scripts/load_api_keys.sh" ] && echo "✅ Ready" || echo "❌ Missing")"
echo "   🌐 Environment Files: $(ls "$FIELD_ROOT"/.env "$FIELD_ROOT"/FIELD-*/.env 2>/dev/null | wc -l | tr -d ' ') configured"
echo ""

log_info "Next Steps:"
echo "   1. Review and update API keys in .credentials_vault/field_api_keys.env"
echo "   2. Run 'direnv allow' in each FIELD directory to activate environments"
echo "   3. Test port connectivity with planned services"
echo "   4. Review PORT_HARMONIZATION_PLAN.md for detailed configuration"
echo ""

log_success "FIELD System configuration setup completed!"
echo ""
echo -e "${BLUE}Sacred Tetrahedron Alignment:${NC}"
echo "   ●OBI-WAN (1369) → Memory & Observation"
echo "   ▼TATA (4320) → Truth & Verification" 
echo "   ▲ATLAS (5281) → Logic & Intelligence"
echo "   ◼︎DOJO (7410) → Manifestation & Execution"
echo ""
echo -e "${GREEN}🌟 May the FIELD be with you! 🌟${NC}"
