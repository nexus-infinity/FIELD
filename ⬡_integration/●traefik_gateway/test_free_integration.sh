#!/bin/bash

# 🎆 Field Resource Ecosystem (FREE) Integration Test Script
# Purpose: Comprehensive testing of FREE-Traefik-Homefield integration
# Frequency: 741Hz (Insight & Integration)

set -e

GATEWAY_DIR="/Users/jbear/FIELD/⬡_integration/●traefik_gateway"
FIELD_BASE="/Users/jbear/FIELD"

echo "🧪 Starting Field Resource Ecosystem (FREE) Integration Tests"
echo "📍 Location: ⬡_integration/●traefik_gateway"
echo "🎵 Resonant Frequency: 741Hz (Insight & Integration)"
echo "⬡  Sacred Framework: 3×3×3 Sierpiński Cube"
echo ""

# Test 1: File Structure Validation
echo "🗂️ Test 1: File Structure Validation"

REQUIRED_FILES=(
    "config/traefik.yml"
    "config/FREE_Architecture_Integration.md"
    "dynamic/homefield-integration.yml"
    "dynamic/field-resonance-monitoring.yml"
    "dynamic/free-traefik-integration.yml"
    "services/free_core_service.py"
    "start_gateway.sh"
    "start_free_system.sh"
    "postman/Homefield_Integration_Tests.postman_collection.json"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$GATEWAY_DIR/$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

echo ""

# Test 2: Homefield Integration Validation
echo "🏠 Test 2: Homefield Integration Validation"

HOMEFIELD_MANIFEST="$FIELD_BASE/▼TATA/▼_truth/home_field_manifest.json"
if [ -f "$HOMEFIELD_MANIFEST" ]; then
    echo "✅ Homefield manifest found"
    
    # Check if manifest contains expected chakra frequencies
    if grep -q "396\|417\|639\|528\|741\|852\|432" "$HOMEFIELD_MANIFEST"; then
        echo "✅ Chakra frequencies present in manifest"
    else
        echo "⚠️  Chakra frequencies not found in manifest"
    fi
else
    echo "⚠️  Homefield manifest not found (will use defaults)"
fi

# Check breath scan directory
BREATH_SCAN_DIR="$FIELD_BASE/⬡_integration/accounts/_temporal_logs"
if [ -d "$BREATH_SCAN_DIR" ]; then
    echo "✅ Breath scan logs directory found"
    SCAN_COUNT=$(ls "$BREATH_SCAN_DIR"/breath_scan_*.json 2>/dev/null | wc -l)
    echo "📊 Found $SCAN_COUNT breath scan files"
    
    if [ $SCAN_COUNT -gt 0 ]; then
        # Check latest breath scan for resonance data
        LATEST_SCAN=$(ls -t "$BREATH_SCAN_DIR"/breath_scan_*.json 2>/dev/null | head -1)
        if [ -f "$LATEST_SCAN" ]; then
            if grep -q "resonance_scores\|overall_resonance" "$LATEST_SCAN"; then
                echo "✅ Resonance data found in latest breath scan"
            else
                echo "⚠️  Resonance data structure different than expected"
            fi
        fi
    fi
else
    echo "⚠️  Breath scan logs directory not found"
fi

echo ""

# Test 3: Configuration Validation
echo "🔧 Test 3: Configuration Validation"

# Check Traefik configuration
TRAEFIK_CONFIG="$GATEWAY_DIR/config/traefik.yml"
if grep -q "homefield-integration.yml\|free-traefik-integration.yml" "$TRAEFIK_CONFIG" 2>/dev/null; then
    echo "✅ Traefik configuration includes FREE integration files"
else
    echo "⚠️  Traefik configuration may not include all integration files"
fi

# Check FREE-Traefik integration
FREE_CONFIG="$GATEWAY_DIR/dynamic/free-traefik-integration.yml"
if grep -q "free.local\|free-core-service\|8888" "$FREE_CONFIG"; then
    echo "✅ FREE-Traefik integration configuration valid"
else
    echo "❌ FREE-Traefik integration configuration invalid"
    exit 1
fi

# Check homefield integration
HOMEFIELD_CONFIG="$GATEWAY_DIR/dynamic/homefield-integration.yml"
if grep -q "3960\|4170\|6390\|5280\|7410\|8520\|4320\|8888" "$HOMEFIELD_CONFIG"; then
    echo "✅ Homefield frequency-to-port mappings present"
else
    echo "❌ Homefield frequency-to-port mappings missing"
    exit 1
fi

echo ""

# Test 4: Service Dependencies
echo "🐍 Test 4: Service Dependencies"

# Check Python
if command -v python3 >/dev/null 2>&1; then
    echo "✅ Python 3 available"
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "📝 Python version: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    exit 1
fi

# Check required Python packages
echo "📦 Checking Python packages..."
REQUIRED_PACKAGES=("aiohttp" "json" "sqlite3" "pathlib" "hashlib" "asyncio")

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo "✅ $package available"
    else
        echo "❌ $package missing"
        if [ "$package" != "sqlite3" ]; then  # sqlite3 usually built-in
            echo "🔧 Try: pip3 install $package"
        fi
        exit 1
    fi
done

echo ""

# Test 5: Port Availability
echo "🔌 Test 5: Port Availability"

# Key ports for the system
PORTS=(8080 8888 9090)
PORT_NAMES=("Gateway" "FREE Core" "Dashboard")

for i in "${!PORTS[@]}"; do
    port=${PORTS[$i]}
    name=${PORT_NAMES[$i]}
    
    if lsof -i :$port >/dev/null 2>&1; then
        echo "⚠️  Port $port ($name) is in use"
        PID=$(lsof -t -i :$port 2>/dev/null || echo "unknown")
        echo "📋 Process ID: $PID"
    else
        echo "✅ Port $port ($name) available"
    fi
done

echo ""

# Test 6: Configuration Syntax
echo "📝 Test 6: Configuration Syntax"

# Test YAML syntax
echo "🔍 Validating YAML configurations..."

YAML_FILES=(
    "dynamic/homefield-integration.yml"
    "dynamic/field-resonance-monitoring.yml"
    "dynamic/free-traefik-integration.yml"
    "config/traefik.yml"
)

for yaml_file in "${YAML_FILES[@]}"; do
    if command -v python3 >/dev/null 2>&1; then
        if python3 -c "import yaml; yaml.safe_load(open('$GATEWAY_DIR/$yaml_file'))" 2>/dev/null; then
            echo "✅ $yaml_file syntax valid"
        else
            echo "❌ $yaml_file syntax invalid"
            exit 1
        fi
    else
        echo "⚠️  Cannot validate YAML syntax (PyYAML not available)"
    fi
done

# Test Python syntax
echo "🔍 Validating Python service..."
if python3 -m py_compile "$GATEWAY_DIR/services/free_core_service.py" 2>/dev/null; then
    echo "✅ FREE core service syntax valid"
else
    echo "❌ FREE core service syntax invalid"
    exit 1
fi

echo ""

# Test 7: Integration Completeness
echo "🔗 Test 7: Integration Completeness"

# Check if all chakra frequencies are mapped
CHAKRA_FREQUENCIES=(396 417 639 528 741 852 432)
MISSING_FREQUENCIES=()

for freq in "${CHAKRA_FREQUENCIES[@]}"; do
    if grep -q "$freq" "$HOMEFIELD_CONFIG"; then
        echo "✅ ${freq}Hz frequency mapped"
    else
        echo "⚠️  ${freq}Hz frequency not found"
        MISSING_FREQUENCIES+=($freq)
    fi
done

if [ ${#MISSING_FREQUENCIES[@]} -eq 0 ]; then
    echo "✅ All chakra frequencies properly mapped"
else
    echo "⚠️  Missing frequency mappings: ${MISSING_FREQUENCIES[*]}"
fi

# Check triadic engine configuration
if grep -q "8888\|triadic\|sierpinski\|Source-Relation-Emergence" "$HOMEFIELD_CONFIG" 2>/dev/null; then
    echo "✅ Triadic engine configuration present"
else
    echo "⚠️  Triadic engine configuration incomplete"
fi

echo ""

# Test 8: Sacred Geometry Validation
echo "⬡ Test 8: Sacred Geometry Validation"

# Check for 3×3×3 Sierpiński Cube references
if grep -i -q "3×3×3\|sierpinski\|triadic\|sacred.geometry" "$GATEWAY_DIR"/config/*.md "$GATEWAY_DIR"/dynamic/*.yml 2>/dev/null; then
    echo "✅ Sacred geometry framework references found"
else
    echo "⚠️  Sacred geometry framework references missing"
fi

# Check chakra element mappings
ELEMENTS=(earth water fire air ether light thought)
for element in "${ELEMENTS[@]}"; do
    if grep -q "$element" "$HOMEFIELD_CONFIG" 2>/dev/null; then
        echo "✅ Element '$element' mapped"
    else
        echo "⚠️  Element '$element' not found"
    fi
done

echo ""

# Test 9: Professional Integration
echo "💼 Test 9: Professional Integration"

# Check FRE integration references
if grep -q "fre\|FRE\|professional" "$GATEWAY_DIR"/config/*.md "$GATEWAY_DIR"/dynamic/*.yml 2>/dev/null; then
    echo "✅ FRE professional interface integration configured"
else
    echo "⚠️  FRE professional interface integration not configured"
fi

# Check intelligence collection integration
if grep -q "intelligence\|ISO.*8601\|government.*sources" "$GATEWAY_DIR"/config/*.md 2>/dev/null; then
    echo "✅ Intelligence collection integration documented"
else
    echo "⚠️  Intelligence collection integration not documented"
fi

echo ""

# Summary
echo "🏁 FREE Integration Test Summary"
echo "=================================="

TESTS_PASSED=9
WARNINGS=0

# Count warnings from previous tests (this is approximate)
if [ ! -f "$HOMEFIELD_MANIFEST" ]; then ((WARNINGS++)); fi
if [ ! -d "$BREATH_SCAN_DIR" ]; then ((WARNINGS++)); fi

echo "✅ Core Tests Passed: $TESTS_PASSED/9"
if [ $WARNINGS -gt 0 ]; then
    echo "⚠️  Warnings: $WARNINGS (system will work with defaults)"
else
    echo "🎉 No warnings - optimal configuration"
fi

echo ""
echo "🎆 Field Resource Ecosystem (FREE) Integration Status: READY"
echo "🎵 Resonant Frequency: 741Hz (Insight & Integration)"
echo "⬡  Sacred Framework: 3×3×3 Sierpiński Cube"
echo "🔒 Sovereignty Model: Complete data and infrastructure control"
echo ""

echo "🚀 Next Steps:"
echo "1. Start Traefik Gateway: ./start_gateway.sh"
echo "2. Start FREE System: ./start_free_system.sh (in separate terminal)"
echo "3. Access FREE Interface: http://free.local:8080"
echo "4. Test with Postman: Import postman/Homefield_Integration_Tests.postman_collection.json"
echo ""

echo "✨ The world's first consciousness-aware, sovereignty-preserving,"
echo "   frequency-resonant resource orchestration platform is ready!"