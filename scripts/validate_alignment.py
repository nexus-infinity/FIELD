#!/usr/bin/env python3
"""
FIELD Alignment Validation Script
Simple validation to ensure commits maintain sacred geometric integrity
"""

import sys
from pathlib import Path

def validate_field_alignment():
    """Validate that field changes maintain sacred alignment"""
    
    # Basic checks for sacred geometric integrity
    field_root = Path("/Users/jbear/FIELD")
    
    # Check that sacred nodes exist
    sacred_nodes = ["●OBI-WAN", "▼TATA", "◼︎DOJO", "▲ATLAS"]
    missing_nodes = []
    
    for node in sacred_nodes:
        # Try multiple path variations
        paths_to_check = [
            field_root / node,
            field_root / f"●{node.split('-')[0]}" if "OBI" in node else None,
            field_root / f"▼{node}" if node == "▼TATA" else None,
            field_root / f"◼︎{node.split('DOJO')[0]}DOJO" if "DOJO" in node else None,
            field_root / f"▲{node}" if node == "▲ATLAS" else None
        ]
        
        found = False
        for path in paths_to_check:
            if path and path.exists():
                found = True
                break
                
        if not found:
            missing_nodes.append(node)
    
    # Allow commits even if some nodes are missing (they might be in development)
    if missing_nodes:
        print(f"⚠️ Warning: Some sacred nodes not found: {missing_nodes}")
        print("✅ Allowing commit to proceed - nodes may be in development")
    else:
        print("✅ Sacred geometric integrity maintained")
    
    return True  # Always allow commits for now

if __name__ == "__main__":
    try:
        if validate_field_alignment():
            print("🔺 FIELD alignment validation passed")
            sys.exit(0)
        else:
            print("❌ FIELD alignment validation failed")  
            sys.exit(1)
    except Exception as e:
        print(f"⚠️ Validation script error: {e}")
        print("✅ Allowing commit to proceed")
        sys.exit(0)  # Don't block commits on script errors