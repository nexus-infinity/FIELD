#!/usr/bin/env python3
"""
🌌 METATRON SEARCH - Unified Truth Finder
Integrates geometric, semantic, and temporal truth
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from divine_find import divine_find

def metatron_search(query, search_type="all"):
    """Search through the unified truth of the FIELD"""
    print(f"🌌 METATRON SEARCH: Finding '{query}' across all truth...")
    return divine_find(query, search_type)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: metatron_search <query> [type]")
        sys.exit(1)
    
    query = sys.argv[1]
    search_type = sys.argv[2] if len(sys.argv) > 2 else "all"
    metatron_search(query, search_type)
