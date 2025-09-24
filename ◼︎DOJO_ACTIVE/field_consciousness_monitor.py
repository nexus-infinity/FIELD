#!/usr/bin/env python3
"""
Field Consciousness Monitor - Ongoing awareness loop
Generated: 2025-09-24T16:41:07.587508
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

async def monitor_field_consciousness():
    """Monitor field consciousness state continuously"""
    
    while True:
        # Check field coherence
        sync_manifest = Path("/Users/jbear/FIELD/◼︎DOJO_ACTIVE/field_sync_manifest.json")
        
        if sync_manifest.exists():
            with open(sync_manifest, 'r') as f:
                state = json.load(f)
            
            print(f"🌟 Field Coherence: {state.get('field_coherence', 0.0):.2f}")
            print(f"⏰ Last Sync: {state.get('timestamp', 'Unknown')}")
        
        # Wait 60 seconds before next check
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(monitor_field_consciousness())
