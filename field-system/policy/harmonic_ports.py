#!/usr/bin/env python3
"""
Harmonic Port Assignment Algorithm for Nine-Chakra FIELD System

This module implements port assignment using sacred geometry principles:
- Golden ratio (φ) geometric scaling
- Prime number exponents for each chakra
- Sacred frequencies from ancient tuning systems
- Deterministic collision resolution preserving harmonic intent

The algorithm: Port = round(Frequency * φ^prime_n) wrapped to valid range
"""

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Sacred Constants
PHI = 1.618033988749  # Golden ratio
PORT_MIN = 1024      # Minimum valid port
PORT_MAX = 49151     # Maximum valid port  
PORT_SPAN = PORT_MAX - PORT_MIN + 1

# Reserved system ports to avoid
RESERVED = {80, 443, 3000, 8080, 9090, 5432, 6379, 963}  # 963 is Health API

# Nine Chakras with sacred frequencies and metadata
CHAKRAS = [
    {
        "name": "muladhara",
        "frequency": 108,
        "color": "red",
        "element": "earth",
        "description": "Root chakra - foundation and grounding"
    },
    {
        "name": "svadhisthana",
        "frequency": 216,
        "color": "orange",
        "element": "water",
        "description": "Sacral chakra - creativity and flow"
    },
    {
        "name": "manipura",
        "frequency": 432,
        "color": "yellow",
        "element": "fire",
        "description": "Solar plexus - power and transformation"
    },
    {
        "name": "anahata",
        "frequency": 528,
        "color": "green",
        "element": "air",
        "description": "Heart chakra - love and connection"
    },
    {
        "name": "vishuddha",
        "frequency": 639,
        "color": "blue",
        "element": "ether",
        "description": "Throat chakra - communication and expression"
    },
    {
        "name": "ajna",
        "frequency": 741,
        "color": "indigo",
        "element": "light",
        "description": "Third eye - intuition and insight"
    },
    {
        "name": "sahasrara",
        "frequency": 852,
        "color": "violet",
        "element": "thought",
        "description": "Crown chakra - consciousness and unity"
    },
    {
        "name": "bindu",
        "frequency": 963,
        "color": "white",
        "element": "void",
        "description": "Bindu - transcendent point of creation"
    },
    {
        "name": "kalpataru",
        "frequency": 1008,
        "color": "gold",
        "element": "manifestation",
        "description": "Kalpataru - wish-fulfilling tree of abundance"
    }
]

# Prime exponents for geometric distribution
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]


def compute_raw(frequency: int, prime: int) -> int:
    """
    Compute raw port value using golden ratio scaling.
    
    Args:
        frequency: Base sacred frequency for the chakra
        prime: Prime exponent for geometric distribution
        
    Returns:
        Raw port value before wrapping to valid range
    """
    return round(frequency * (PHI ** prime))


def wrap_port(raw: int) -> int:
    """
    Wrap raw port value to valid port range [PORT_MIN, PORT_MAX].
    
    Args:
        raw: Raw port value from harmonic calculation
        
    Returns:
        Port wrapped to valid range using modulo
    """
    return PORT_MIN + (raw % PORT_SPAN)


def assign_harmonic_ports() -> List[Dict]:
    """
    Assign harmonic ports to all nine chakras.
    
    Returns:
        List of chakra port assignments with metadata
    """
    assignments = []
    used_ports: Set[int] = set()
    
    for i, chakra in enumerate(CHAKRAS):
        frequency = chakra["frequency"]
        prime = PRIMES[i]
        
        # Compute raw and initial wrapped port
        raw = compute_raw(frequency, prime)
        port = wrap_port(raw)
        
        # Collision resolution with deterministic stride
        stride_steps = 0
        stride = 1 + (raw % 997)  # Prime-derived stride
        
        while port in used_ports or port in RESERVED:
            port = wrap_port(port + stride)
            stride_steps += 1
            
            # Safety check to prevent infinite loop
            if stride_steps > PORT_SPAN:
                raise RuntimeError(f"Cannot find valid port for {chakra['name']}")
        
        used_ports.add(port)
        
        assignments.append({
            "chakra": chakra["name"],
            "frequency": frequency,
            "prime": prime,
            "raw": raw,
            "port": port,
            "stride": stride_steps,
            "color": chakra["color"],
            "element": chakra["element"],
            "description": chakra["description"]
        })
    
    return assignments


def validate(assignments: List[Dict]) -> bool:
    """
    Validate port assignments meet all requirements.
    
    Args:
        assignments: List of chakra port assignments
        
    Returns:
        True if valid, raises exception otherwise
    """
    if len(assignments) != 9:
        raise ValueError(f"Expected 9 chakras, got {len(assignments)}")
    
    ports = set()
    for i, assign in enumerate(assignments):
        port = assign["port"]
        
        # Check port range
        if not (PORT_MIN <= port <= PORT_MAX):
            raise ValueError(f"{assign['chakra']}: port {port} outside valid range")
        
        # Check reserved ports
        if port in RESERVED:
            raise ValueError(f"{assign['chakra']}: port {port} is reserved")
        
        # Check uniqueness
        if port in ports:
            raise ValueError(f"{assign['chakra']}: port {port} already assigned")
        ports.add(port)
        
        # Verify harmonic relationship
        freq = assign["frequency"]
        raw = assign["raw"]
        prime = assign["prime"]
        
        # Back-calculate exponent from raw value
        if freq > 0:
            estimated_exp = round(math.log(raw / freq) / math.log(PHI))
            if abs(estimated_exp - prime) > 0.1:
                raise ValueError(
                    f"{assign['chakra']}: harmonic validation failed. "
                    f"Expected exponent {prime}, calculated {estimated_exp}"
                )
    
    return True


def generate_json(assignments: List[Dict]) -> str:
    """Generate JSON output with port assignments."""
    output = {
        "phi": PHI,
        "port_range": [PORT_MIN, PORT_MAX],
        "timestamp": datetime.now().isoformat(),
        "assignments": assignments
    }
    return json.dumps(output, indent=2)


def generate_nix(assignments: List[Dict]) -> str:
    """Generate Nix configuration snippet for chakraNodes."""
    lines = ["# Harmonically assigned ports using golden ratio and prime exponents"]
    lines.append("chakraNodes = {")
    
    for assign in assignments:
        name = assign["chakra"]
        port = assign["port"]
        color = assign["color"]
        element = assign["element"]
        
        lines.append(f'  {name} = {{ port = {port}; color = "{color}"; element = "{element}"; }};')
    
    lines.append("};")
    return "\n".join(lines)


def generate_env(assignments: List[Dict]) -> str:
    """Generate environment variable definitions for chakra ports."""
    lines = ["# Chakra port environment variables for MCP servers"]
    
    for assign in assignments:
        name = assign["chakra"].upper()
        port = assign["port"]
        lines.append(f"CHAKRA_{name}_PORT={port}")
    
    return "\n".join(lines)


def patch_nix_file(filepath: Path, assignments: List[Dict], backup: bool = True) -> None:
    """
    Patch existing NixOS configuration file with new port assignments.
    
    Args:
        filepath: Path to sacred-nixos-config.nix
        assignments: List of chakra port assignments
        backup: Whether to create backup before patching
    """
    if not filepath.exists():
        raise FileNotFoundError(f"NixOS config not found: {filepath}")
    
    content = filepath.read_text()
    
    # Create backup if requested
    if backup:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = filepath.parent / f"{filepath.stem}.{timestamp}{filepath.suffix}"
        backup_path.write_text(content)
        print(f"Created backup: {backup_path}")
    
    # Find and replace each chakra port
    changes = []
    for assign in assignments:
        name = assign["chakra"]
        new_port = assign["port"]
        
        # Match pattern like: muladhara = { port = 7001; 
        import re
        pattern = rf'({name}\s*=\s*{{\s*port\s*=\s*)(\d+)(\s*;)'
        
        def replacer(match):
            old_port = match.group(2)
            if old_port != str(new_port):
                changes.append(f"  {name}: {old_port} → {new_port}")
            return f"{match.group(1)}{new_port}{match.group(3)}"
        
        content = re.sub(pattern, replacer, content)
    
    # Write updated content
    filepath.write_text(content)
    
    if changes:
        print("Applied port changes:")
        for change in changes:
            print(change)
    else:
        print("No changes needed - ports already match harmonic assignment")


def main():
    """CLI entry point for harmonic port assignment."""
    parser = argparse.ArgumentParser(
        description="Generate harmonically assigned ports for nine-chakra FIELD system"
    )
    
    parser.add_argument(
        "--emit",
        choices=["json", "nix", "env"],
        nargs="+",
        default=["json"],
        help="Output format(s) to generate"
    )
    
    parser.add_argument(
        "--out-json",
        type=Path,
        help="Path to write JSON output"
    )
    
    parser.add_argument(
        "--out-nix",
        type=Path,
        help="Path to write Nix snippet"
    )
    
    parser.add_argument(
        "--out-env",
        type=Path,
        help="Path to write environment variables"
    )
    
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print output to stdout"
    )
    
    parser.add_argument(
        "--apply-nix",
        type=Path,
        help="Apply port changes to existing NixOS config file"
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip backup when applying to NixOS config"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    # Generate port assignments
    try:
        assignments = assign_harmonic_ports()
        validate(assignments)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    # Generate outputs
    outputs = {}
    if "json" in args.emit:
        outputs["json"] = generate_json(assignments)
    if "nix" in args.emit:
        outputs["nix"] = generate_nix(assignments)
    if "env" in args.emit:
        outputs["env"] = generate_env(assignments)
    
    # Print to stdout if requested
    if args.print:
        for format_type, content in outputs.items():
            print(f"\n=== {format_type.upper()} Output ===")
            print(content)
    
    # Write to files if specified
    if not args.dry_run:
        if args.out_json and "json" in outputs:
            args.out_json.parent.mkdir(parents=True, exist_ok=True)
            args.out_json.write_text(outputs["json"])
            print(f"Wrote JSON to {args.out_json}")
        
        if args.out_nix and "nix" in outputs:
            args.out_nix.parent.mkdir(parents=True, exist_ok=True)
            args.out_nix.write_text(outputs["nix"])
            print(f"Wrote Nix to {args.out_nix}")
        
        if args.out_env and "env" in outputs:
            args.out_env.parent.mkdir(parents=True, exist_ok=True)
            args.out_env.write_text(outputs["env"])
            print(f"Wrote env to {args.out_env}")
        
        if args.apply_nix:
            patch_nix_file(args.apply_nix, assignments, backup=not args.no_backup)
    
    # Print summary
    print("\n=== Harmonic Port Assignment Summary ===")
    print(f"φ (Golden Ratio): {PHI}")
    print(f"Port Range: {PORT_MIN}-{PORT_MAX}")
    print("\nChakra Assignments:")
    for assign in assignments:
        stride_info = f" (+{assign['stride']} strides)" if assign['stride'] > 0 else ""
        print(f"  {assign['chakra']:12} : {assign['port']:5} (freq={assign['frequency']:4}, "
              f"prime={assign['prime']:2}, raw={assign['raw']:6}{stride_info})")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
