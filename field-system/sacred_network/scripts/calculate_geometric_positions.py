#!/usr/bin/env python3
"""Calculate sacred geometric positions from extracted patterns"""

import json
import numpy as np
from pathlib import Path

PHI = 1.618033988749  # Golden ratio

def calculate_geometric_positions():
    """Calculate 3D sacred geometric positions"""
    
    # Load all extracted patterns
    data_dir = Path("$DATA_DIR")
    all_contacts = set()
    
    # Collect all unique contacts
    for pattern_file in data_dir.glob("*.json"):
        with open(pattern_file) as f:
            data = json.load(f)
            
            # Extract contacts from different data structures
            if 'introduction_patterns' in data:
                for intro in data['introduction_patterns']:
                    all_contacts.add(intro.get('introducer', ''))
                    all_contacts.add(intro.get('introduced', ''))
            
            if 'collaboration_flows' in data:
                for flow in data['collaboration_flows']:
                    all_contacts.add(flow.get('from', ''))
                    all_contacts.add(flow.get('to', ''))
    
    # Calculate geometric positions
    positions = {}
    for i, contact in enumerate(all_contacts):
        if contact:  # Skip empty strings
            # Use golden ratio spiral
            angle = i * PHI * 2 * np.pi
            radius = PHI ** (i / 10)
            z = i / len(all_contacts) * 10 - 5
            
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            positions[contact] = {
                'x': float(x),
                'y': float(y),
                'z': float(z),
                'radius': float(radius),
                'angle': float(angle)
            }
    
    return positions

if __name__ == "__main__":
    positions = calculate_geometric_positions()
    output_path = Path("$DATA_DIR/geometric_positions.json")
    
    with open(output_path, 'w') as f:
        json.dump(positions, f, indent=2)
    
    print(f"✅ Geometric positions calculated for {len(positions)} contacts")
    print(f"   Positions follow golden ratio spiral in 3D sacred geometry")
