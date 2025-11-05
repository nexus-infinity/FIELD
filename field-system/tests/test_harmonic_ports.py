#!/usr/bin/env python3
"""
Unit tests for harmonic port assignment algorithm.
Tests sacred geometry principles and collision avoidance.
"""

import sys
import json
import math
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from policy.harmonic_ports import (
    PHI, PORT_MIN, PORT_MAX, RESERVED, CHAKRAS, PRIMES,
    compute_raw, wrap_port, assign_harmonic_ports, validate,
    generate_json, generate_nix
)


def test_range_and_uniqueness():
    """Test that all ports are in valid range and unique."""
    assignments = assign_harmonic_ports()
    
    # Check we have 9 chakras
    assert len(assignments) == 9, f"Expected 9 chakras, got {len(assignments)}"
    
    ports = set()
    for assign in assignments:
        port = assign["port"]
        
        # Check range
        assert PORT_MIN <= port <= PORT_MAX, \
            f"Port {port} for {assign['chakra']} outside valid range"
        
        # Check not reserved
        assert port not in RESERVED, \
            f"Port {port} for {assign['chakra']} is reserved"
        
        # Check uniqueness
        assert port not in ports, \
            f"Port {port} for {assign['chakra']} already assigned"
        ports.add(port)
    
    print("✅ test_range_and_uniqueness passed")


def test_harmonic_exponents_match_primes():
    """Test that harmonic relationships match prime exponents."""
    assignments = assign_harmonic_ports()
    
    for i, assign in enumerate(assignments):
        freq = assign["frequency"]
        raw = assign["raw"]
        prime = assign["prime"]
        
        # Back-calculate exponent
        if freq > 0:
            estimated_exp = round(math.log(raw / freq) / math.log(PHI))
            assert estimated_exp == prime, \
                f"{assign['chakra']}: Expected prime {prime}, calculated {estimated_exp}"
    
    print("✅ test_harmonic_exponents_match_primes passed")


def test_reserved_avoidance():
    """Test that reserved ports are avoided."""
    assignments = assign_harmonic_ports()
    
    for assign in assignments:
        port = assign["port"]
        assert port not in RESERVED, \
            f"Port {port} for {assign['chakra']} is in reserved list"
    
    print("✅ test_reserved_avoidance passed")


def test_stability_same_inputs_same_outputs():
    """Test that same inputs always produce same outputs."""
    # Run multiple times
    results = []
    for _ in range(5):
        assignments = assign_harmonic_ports()
        # Convert to comparable format
        port_map = {a["chakra"]: a["port"] for a in assignments}
        results.append(port_map)
    
    # Check all results are identical
    first = results[0]
    for result in results[1:]:
        assert result == first, "Port assignments not stable across runs"
    
    print("✅ test_stability_same_inputs_same_outputs passed")


def test_nix_snippet_roundtrip_parses_ports():
    """Test that Nix snippet contains valid port assignments."""
    assignments = assign_harmonic_ports()
    nix_content = generate_nix(assignments)
    
    # Check each chakra appears in Nix output
    for assign in assignments:
        name = assign["chakra"]
        port = assign["port"]
        color = assign["color"]
        element = assign["element"]
        
        # Check port assignment in Nix
        expected = f'{name} = {{ port = {port}; color = "{color}"; element = "{element}"; }};'
        assert expected in nix_content, \
            f"Expected Nix line not found: {expected}"
    
    print("✅ test_nix_snippet_roundtrip_parses_ports passed")


def test_validation_function():
    """Test the validation function works correctly."""
    assignments = assign_harmonic_ports()
    
    # Should pass validation
    assert validate(assignments) == True
    
    # Test validation catches bad data
    bad_assignments = assignments.copy()
    
    # Test port out of range
    import copy
    bad = copy.deepcopy(assignments)
    bad[0]["port"] = 100  # Too low
    try:
        validate(bad)
        assert False, "Should have caught port out of range"
    except ValueError as e:
        assert "outside valid range" in str(e)
    
    # Test duplicate port
    bad = copy.deepcopy(assignments)
    bad[1]["port"] = bad[0]["port"]  # Duplicate
    try:
        validate(bad)
        assert False, "Should have caught duplicate port"
    except ValueError as e:
        assert "already assigned" in str(e)
    
    print("✅ test_validation_function passed")


def test_golden_ratio_scaling():
    """Test that raw values follow golden ratio scaling."""
    assignments = assign_harmonic_ports()
    
    for i in range(len(assignments) - 1):
        curr = assignments[i]
        next = assignments[i + 1]
        
        # Calculate ratio between consecutive raw values
        if curr["frequency"] > 0 and next["frequency"] > 0:
            # Account for frequency difference
            freq_ratio = next["frequency"] / curr["frequency"]
            raw_ratio = next["raw"] / curr["raw"]
            prime_diff = next["prime"] - curr["prime"]
            
            # The raw ratio should approximately equal
            # freq_ratio * PHI^(prime_diff)
            expected_ratio = freq_ratio * (PHI ** prime_diff)
            
            # Allow some tolerance for rounding
            tolerance = 0.01
            relative_diff = abs(raw_ratio - expected_ratio) / expected_ratio
            
            assert relative_diff < tolerance, \
                f"Golden ratio scaling off between {curr['chakra']} and {next['chakra']}: " \
                f"expected {expected_ratio:.4f}, got {raw_ratio:.4f}"
    
    print("✅ test_golden_ratio_scaling passed")


def test_chakra_metadata_preserved():
    """Test that chakra metadata (colors, elements) is preserved."""
    assignments = assign_harmonic_ports()
    
    for i, assign in enumerate(assignments):
        original = CHAKRAS[i]
        
        assert assign["chakra"] == original["name"]
        assert assign["frequency"] == original["frequency"]
        assert assign["color"] == original["color"]
        assert assign["element"] == original["element"]
        assert assign["description"] == original["description"]
    
    print("✅ test_chakra_metadata_preserved passed")


def main():
    """Run all tests."""
    print("🧪 Running harmonic port assignment tests...\n")
    
    test_range_and_uniqueness()
    test_harmonic_exponents_match_primes()
    test_reserved_avoidance()
    test_stability_same_inputs_same_outputs()
    test_nix_snippet_roundtrip_parses_ports()
    test_validation_function()
    test_golden_ratio_scaling()
    test_chakra_metadata_preserved()
    
    print("\n✨ All tests passed! Harmonic alignment achieved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
