#!/bin/bash

# =============================================================================
# FIELD Structure Test Suite - Field-Awareness and Visual Indicators
# =============================================================================
# Tests starship prompt indicators and glyph display across FIELD structure
# Step 6: Test Field-Awareness and Visual Indicators

echo "🧪 FIELD Structure Test Suite - Field-Awareness and Visual Indicators"
echo "========================================================================"
echo "Testing prompt indicators and glyph display across FIELD structure"
echo "Date: $(date)"
echo ""

# Test configuration
TEST_LOG="/tmp/field_test_$(date +%Y%m%d_%H%M%S).log"
TEST_RESULTS=()
FAILED_TESTS=()

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to test directory and capture prompt
test_directory() {
    local dir="$1"
    local expected_indicator="$2"
    local expected_glyph="$3"
    local test_name="$4"
    
    echo -e "${CYAN}Testing: ${test_name}${NC}"
    echo "  Directory: $dir"
    
    if [[ ! -d "$dir" ]]; then
        echo -e "  ${RED}❌ SKIP${NC} - Directory does not exist"
        FAILED_TESTS+=("$test_name - Directory missing")
        return 1
    fi
    
    # Change to directory and capture prompt
    cd "$dir" 2>/dev/null || {
        echo -e "  ${RED}❌ FAIL${NC} - Cannot access directory"
        FAILED_TESTS+=("$test_name - Access denied")
        return 1
    }
    
    # Generate prompt using starship and clean up escape sequences
    local prompt_output
    prompt_output=$(starship prompt 2>/dev/null | sed 's/%{[^}]*}//g')
    local prompt_exit_code=$?
    
    if [[ $prompt_exit_code -ne 0 ]]; then
        echo -e "  ${RED}❌ FAIL${NC} - Starship prompt generation failed"
        FAILED_TESTS+=("$test_name - Prompt generation failed")
        return 1
    fi
    
    # Test field indicator
    local indicator_found=false
    if [[ -n "$expected_indicator" ]]; then
        if echo "$prompt_output" | grep -q "$expected_indicator"; then
            echo -e "  ${GREEN}✅ PASS${NC} - Field indicator '$expected_indicator' found"
            indicator_found=true
        else
            echo -e "  ${RED}❌ FAIL${NC} - Field indicator '$expected_indicator' NOT found"
            echo "    Debug: Raw output snippet: $(echo "$prompt_output" | head -c 100)..."
            FAILED_TESTS+=("$test_name - Missing field indicator")
        fi
    else
        echo -e "  ${YELLOW}⚠️  INFO${NC} - No field indicator expected"
        indicator_found=true
    fi
    
    # Test glyph indicator
    local glyph_found=false
    if [[ -n "$expected_glyph" ]]; then
        if echo "$prompt_output" | grep -q "$expected_glyph"; then
            echo -e "  ${GREEN}✅ PASS${NC} - Glyph '$expected_glyph' found"
            glyph_found=true
        else
            echo -e "  ${RED}❌ FAIL${NC} - Glyph '$expected_glyph' NOT found"
            echo "    Debug: Raw output snippet: $(echo "$prompt_output" | head -c 100)..."
            FAILED_TESTS+=("$test_name - Missing glyph")
        fi
    else
        echo -e "  ${YELLOW}⚠️  INFO${NC} - No glyph expected"
        glyph_found=true
    fi
    
    # Log full prompt for debugging
    echo "  Prompt Output: $prompt_output" >> "$TEST_LOG"
    
    if [[ "$indicator_found" == "true" && "$glyph_found" == "true" ]]; then
        TEST_RESULTS+=("$test_name - PASS")
        echo -e "  ${GREEN}🎯 OVERALL: PASS${NC}"
    else
        TEST_RESULTS+=("$test_name - FAIL")
        echo -e "  ${RED}🚨 OVERALL: FAIL${NC}"
    fi
    
    echo ""
}

# Function to test performance
test_performance() {
    local dir="$1"
    local test_name="$2"
    
    echo -e "${CYAN}Performance Test: ${test_name}${NC}"
    
    if [[ ! -d "$dir" ]]; then
        echo -e "  ${RED}❌ SKIP${NC} - Directory does not exist"
        return 1
    fi
    
    cd "$dir" 2>/dev/null || return 1
    
    # Time the prompt generation (use gdate if available for nanoseconds)
    if command -v gdate >/dev/null; then
        local start_time=$(gdate +%s%N)
        starship prompt >/dev/null 2>&1
        local end_time=$(gdate +%s%N)
        local duration=$(((end_time - start_time) / 1000000))
    else
        # Fallback to millisecond precision
        local start_time=$(python3 -c "import time; print(int(time.time() * 1000))")
        starship prompt >/dev/null 2>&1
        local end_time=$(python3 -c "import time; print(int(time.time() * 1000))")
        local duration=$((end_time - start_time))
    fi
    
    echo "  Render time: ${duration}ms"
    
    if [[ $duration -lt 200 ]]; then
        echo -e "  ${GREEN}✅ EXCELLENT${NC} - Render time under 200ms"
    elif [[ $duration -lt 500 ]]; then
        echo -e "  ${YELLOW}⚠️  GOOD${NC} - Render time under 500ms"
    else
        echo -e "  ${RED}❌ SLOW${NC} - Render time over 500ms"
        FAILED_TESTS+=("$test_name - Performance issue")
    fi
    echo ""
}

echo "🏁 Starting Field Structure Tests..."
echo ""

# =============================================================================
# Test 1: Field Indicators (Red, Green, Blue, Purple circles)
# =============================================================================
echo -e "${WHITE}📋 TEST SUITE 1: Field Indicators${NC}"
echo "Testing field-specific indicators across main field directories"
echo ""

test_directory "/Users/jbear/FIELD/▼TATA" "🔴" "" "TATA Field Indicator"
test_directory "/Users/jbear/FIELD/●▼TATA" "🔴" "" "TATA Unified Field Indicator"
test_directory "/Users/jbear/FIELD/▼TATA/_core" "🔴" "" "TATA Core Subdirectory"

test_directory "/Users/jbear/FIELD/▲ATLAS" "🟢" "▲" "ATLAS Field Indicator"
test_directory "/Users/jbear/FIELD/▲ATLAS/_core" "🟢" "" "ATLAS Core Subdirectory"
test_directory "/Users/jbear/FIELD/▲ATLAS/compass" "🟢" "" "ATLAS Compass Subdirectory"

test_directory "/Users/jbear/FIELD/■DOJO" "🔵" "■" "DOJO Field Indicator (square)"
test_directory "/Users/jbear/FIELD/◼︎DOJO" "🔵" "◼︎" "DOJO Field Indicator (filled square)"
test_directory "/Users/jbear/FIELD/Dojo" "🔵" "" "DOJO Basic Directory"

test_directory "/Users/jbear/FIELD/●OBI-WAN" "🟣" "" "OBI-WAN Field Indicator"

# =============================================================================
# Test 2: Prime Petal Glyph Indicators
# =============================================================================
echo -e "${WHITE}📋 TEST SUITE 2: Prime Petal Glyphs${NC}"
echo "Testing prime petal glyph detection and display"
echo ""

test_directory "/Users/jbear/FIELD/●◎_FIELD_TRAIN_STATION" "" "◎" "P1 Unity Glyph"
test_directory "/Users/jbear/FIELD/●◎_sandbox" "" "◎" "P1 Sandbox Glyph"

# Test for ▲ glyph (P3)
test_directory "/Users/jbear/FIELD/▲ATLAS" "" "▲" "P3 Identity Glyph"

# Test for ⬢ glyph (P7)
test_directory "/Users/jbear/FIELD/▲ATLAS/⬢_crystallized_patterns" "" "⬢" "P7 Life Pattern Glyph"
test_directory "/Users/jbear/FIELD/▲ATLAS/⬢_models" "" "⬢" "P7 Models Glyph"

# Test for ✦ glyph (P9)
test_directory "/Users/jbear/FIELD/▲ATLAS/✦_metatron_translator_core" "" "✦" "P9 Cognition Glyph"
test_directory "/Users/jbear/FIELD/▼TATA/✦_sovereign_wisdom" "" "✦" "P9 Sovereign Wisdom Glyph"

# Test for ⭣ glyph (P11)
test_directory "/Users/jbear/FIELD/●⭣_registry" "" "⭣" "P11 Registry Glyph"
test_directory "/Users/jbear/FIELD/▼TATA/⭣_registry" "" "⭣" "P11 TATA Registry Glyph"

# =============================================================================
# Test 3: Combined Indicators and Glyphs
# =============================================================================
echo -e "${WHITE}📋 TEST SUITE 3: Combined Indicators and Glyphs${NC}"
echo "Testing directories that should display both field indicators and glyphs"
echo ""

test_directory "/Users/jbear/FIELD/▲ATLAS/⬢_crystallized_patterns" "🟢" "⬢" "ATLAS + Crystallized Patterns"
test_directory "/Users/jbear/FIELD/▲ATLAS/✦_metatron_translator_core" "🟢" "✦" "ATLAS + Metatron Core"
test_directory "/Users/jbear/FIELD/▼TATA/✦_sovereign_wisdom" "🔴" "✦" "TATA + Sovereign Wisdom"
test_directory "/Users/jbear/FIELD/▼TATA/⭣_registry" "🔴" "⭣" "TATA + Registry"

# =============================================================================
# Test 4: Negative Tests (no indicators expected)
# =============================================================================
echo -e "${WHITE}📋 TEST SUITE 4: Negative Tests${NC}"
echo "Testing directories that should NOT display field indicators"
echo ""

test_directory "/Users/jbear/FIELD" "" "" "Root FIELD Directory"
test_directory "/Users/jbear/FIELD/●_core" "" "" "Core Directory"
test_directory "/Users/jbear/FIELD/_meta" "" "" "Meta Directory"
test_directory "/Users/jbear/FIELD/.git" "" "" "Git Directory"

# =============================================================================
# Test 5: Performance Tests
# =============================================================================
echo -e "${WHITE}📋 TEST SUITE 5: Performance Tests${NC}"
echo "Testing prompt rendering performance across key directories"
echo ""

test_performance "/Users/jbear/FIELD" "Root Directory Performance"
test_performance "/Users/jbear/FIELD/▲ATLAS" "ATLAS Performance"
test_performance "/Users/jbear/FIELD/▼TATA" "TATA Performance"
test_performance "/Users/jbear/FIELD/■DOJO" "DOJO Performance"
test_performance "/Users/jbear/FIELD/●OBI-WAN" "OBI-WAN Performance"

# =============================================================================
# Test 6: Stability Test
# =============================================================================
echo -e "${WHITE}📋 TEST SUITE 6: Stability Tests${NC}"
echo "Testing prompt stability with rapid directory changes"
echo ""

echo -e "${CYAN}Rapid Directory Change Test${NC}"
dirs=("/Users/jbear/FIELD/▲ATLAS" "/Users/jbear/FIELD/▼TATA" "/Users/jbear/FIELD/■DOJO" "/Users/jbear/FIELD/●OBI-WAN")
stable_count=0

for i in {1..10}; do
    for dir in "${dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            cd "$dir" 2>/dev/null
            if starship prompt >/dev/null 2>&1; then
                ((stable_count++))
            fi
        fi
    done
done

echo "Stability test: $stable_count successful prompt generations"
if [[ $stable_count -ge 35 ]]; then
    echo -e "${GREEN}✅ STABLE${NC} - High success rate"
else
    echo -e "${RED}❌ UNSTABLE${NC} - Low success rate"
    FAILED_TESTS+=("Stability Test - High failure rate")
fi
echo ""

# =============================================================================
# Results Summary
# =============================================================================
echo -e "${WHITE}📊 TEST RESULTS SUMMARY${NC}"
echo "========================================================================"

total_tests=${#TEST_RESULTS[@]}
passed_tests=$(printf '%s\n' "${TEST_RESULTS[@]}" | grep -c "PASS")
failed_tests=$(printf '%s\n' "${TEST_RESULTS[@]}" | grep -c "FAIL")

echo "Total Tests: $total_tests"
echo -e "Passed: ${GREEN}$passed_tests${NC}"
echo -e "Failed: ${RED}$failed_tests${NC}"
echo ""

if [[ $failed_tests -gt 0 ]]; then
    echo -e "${RED}❌ FAILED TESTS:${NC}"
    for failure in "${FAILED_TESTS[@]}"; do
        echo "  - $failure"
    done
    echo ""
fi

# Configuration verification
echo -e "${WHITE}⚙️  CONFIGURATION STATUS${NC}"
echo "========================================================================"
starship_config_status=$(starship print-config 2>&1 | grep -c "WARN\|ERROR")
if [[ $starship_config_status -eq 0 ]]; then
    echo -e "${GREEN}✅ Configuration Clean${NC} - No warnings or errors"
else
    echo -e "${YELLOW}⚠️  Configuration Issues${NC} - $starship_config_status warnings/errors found"
fi

# Return to original directory
cd "/Users/jbear/FIELD"

echo ""
echo "Test log saved to: $TEST_LOG"
echo "Test completed at: $(date)"

if [[ $failed_tests -eq 0 && $starship_config_status -eq 0 ]]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED - Field awareness and visual indicators working correctly!${NC}"
    exit 0
else
    echo -e "${RED}🚨 SOME TESTS FAILED - Review results above${NC}"
    exit 1
fi
