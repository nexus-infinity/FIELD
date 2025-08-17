# Sacred Geometry Development Justfile
# Command runner for FIELD development

# Default recipe - show help
default:
    @just --list

# Sacred port configuration
obiwan_port := "9630"
tata_port := "5280"
atlas_port := "4320"
dojo_port := "3960"

# === Sacred Geometry Commands ===

# Start the sacred geometry orchestrator
start-orchestrator:
    python3 ●OBI-WAN/sacred_geometry_orchestrator.py

# Check status of all sacred nodes
status:
    python3 ●OBI-WAN/sacred_geometry_orchestrator.py status

# Start individual nodes
start-obiwan:
    FIELD_SYMBOL="●" FIELD_NAME="OBI-WAN" SACRED_PORT={{obiwan_port}} python3 ●OBI-WAN/observer_server.py

start-tata:
    FIELD_SYMBOL="▼" FIELD_NAME="TATA" SACRED_PORT={{tata_port}} python3 ▼TATA/integrity_server.py

start-atlas:
    FIELD_SYMBOL="▲" FIELD_NAME="ATLAS" SACRED_PORT={{atlas_port}} python3 ▲ATLAS/intelligence_server.py

start-dojo:
    FIELD_SYMBOL="◼" FIELD_NAME="DOJO" SACRED_PORT={{dojo_port}} python3 ◼DOJO/manifestation_server.py

# === Development Workflow ===

# Interactive exploration mode
explore:
    #!/usr/bin/env bash
    intent=$(gum input --placeholder "What's your intention?")
    slug=$(echo "$intent" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | head -c 20)
    branch="exp/$(date +%Y%m%d)-$slug"
    git checkout -b "$branch"
    echo "🔍 Exploration branch created: $branch"
    echo "Intention: $intent" > .exploration_intent.md
    git add .exploration_intent.md
    git commit -m "🔍 explore: $intent"

# Ship current work
ship:
    #!/usr/bin/env bash
    current_branch=$(git branch --show-current)
    if [[ "$current_branch" == "main" ]]; then
        echo "❌ Cannot ship from main branch"
        exit 1
    fi
    git add -A
    gum input --placeholder "Describe your changes" | xargs -I {} git commit -m "✨ {}"
    gh pr create --fill

# === Testing & Quality ===

# Run tests
test:
    python3 -m pytest tests/ -v

# Run linting
lint:
    python3 -m ruff check .

# Check alignment (fractal observer toolbox)
align:
    python3 scripts/alignment_gate.py exploration

# Verify all systems
verify:
    @echo "🔍 Verifying sacred geometry..."
    @curl -s localhost:{{obiwan_port}}/health || echo "OBI-WAN not responding"
    @curl -s localhost:{{tata_port}}/health || echo "TATA not responding"
    @curl -s localhost:{{atlas_port}}/health || echo "ATLAS not responding"
    @curl -s localhost:{{dojo_port}}/health || echo "DOJO not responding"
    @lsof -n -i:{{obiwan_port}},{{tata_port}},{{atlas_port}},{{dojo_port}} | head -5

# === Progress & Monitoring ===

# Show progress HUD
hud:
    #!/usr/bin/env bash
    if [ -f PROGRESS.md ]; then
        glow PROGRESS.md
    else
        echo "# FIELD Development Progress" > PROGRESS.md
        echo "" >> PROGRESS.md
        echo "## Current State" >> PROGRESS.md
        echo "- Sacred Nodes: Active" >> PROGRESS.md
        echo "- Observer State: ●" >> PROGRESS.md
        echo "" >> PROGRESS.md
        glow PROGRESS.md
    fi

# Monitor system with btop
monitor:
    btop

# === Utility Commands ===

# Clean Python cache files
clean:
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete

# Setup development environment
bootstrap:
    @echo "🔧 Bootstrapping development environment..."
    @which python3 || echo "⚠️  Python3 not found"
    @which node || echo "⚠️  Node not found"
    @which git || echo "⚠️  Git not found"
    @echo "✅ Bootstrap check complete"

# Git status with sacred symbols
gs:
    @git status --short | sed 's/^M /● /' | sed 's/^A /▲ /' | sed 's/^D /▼ /' | sed 's/^?? /◼ /'

# === MCP Integration ===

# Start MCP servers
mcp-start:
    @echo "🌐 Starting MCP servers..."
    cd mcp && npm start

# === Disk Management ===

# Check disk space
disk-check:
    @df -h | grep -E "/$|/System/Volumes/Data|/Volumes/Akron"

# === AI Partner Management ===

# Configure AI partners
ai-config:
    python3 scripts/ai_partners_config.py

# Show AI partner matrix
ai-matrix:
    @python3 -c "from scripts.ai_partners_config import AIPartnerConfig; c = AIPartnerConfig(); c.display_partnership_matrix()"

# Test AI API keys
ai-test:
    @echo "Testing AI API connections..."
    @[ -n "${OPENAI_API_KEY:-}" ] && echo "✅ OpenAI configured" || echo "⚠️  OpenAI missing"
    @[ -n "${GEMINI_API_KEY:-}" ] && echo "✅ Gemini configured" || echo "⚠️  Gemini missing"
    @[ -n "${ANTHROPIC_API_KEY:-}" ] && echo "✅ Claude configured" || echo "⚠️  Claude missing"

# === Sacred State Management ===

# Save current state to iCloud
save-state:
    #!/usr/bin/env bash
    state_file="$HOME/Library/Mobile Documents/com~apple~CloudDocs/FIELD-DEV/state/sacred_state.json"
    echo '{' > "$state_file"
    echo '  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",' >> "$state_file"
    echo '  "observer_state": "●",' >> "$state_file"
    echo '  "nodes": {' >> "$state_file"
    echo '    "obiwan": '$(lsof -n -i:{{obiwan_port}} > /dev/null 2>&1 && echo "true" || echo "false")',' >> "$state_file"
    echo '    "tata": '$(lsof -n -i:{{tata_port}} > /dev/null 2>&1 && echo "true" || echo "false")',' >> "$state_file"
    echo '    "atlas": '$(lsof -n -i:{{atlas_port}} > /dev/null 2>&1 && echo "true" || echo "false")',' >> "$state_file"
    echo '    "dojo": '$(lsof -n -i:{{dojo_port}} > /dev/null 2>&1 && echo "true" || echo "false") >> "$state_file"
    echo '  }' >> "$state_file"
    echo '}' >> "$state_file"
    echo "💾 State saved to iCloud"
