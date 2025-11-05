#!/usr/bin/env python3
"""
Test Script for Trident Flow
Tests complete data flow through OBI-WAN → TATA → ATLAS using real investigation data
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pprint import pprint

# Add FIELD paths
field_path = os.path.expanduser("~/FIELD")
sys.path.insert(0, field_path)  # Add main FIELD directory
sys.path.extend([
    os.path.join(field_path, "●OBI-WAN/_protocols"),
    os.path.join(field_path, "▼TATA"),
    os.path.join(field_path, "▲ATLAS")
])

# Ensure all required directories exist
for dir_path in [
    os.path.join(field_path, "●OBI-WAN/_protocols"),
    os.path.join(field_path, "▼TATA"),
    os.path.join(field_path, "▲ATLAS")
]:
    os.makedirs(dir_path, exist_ok=True)

# Import core components
try:
    from sacred_sphere_state_manager import SacredSphereManager
    from sacred_file_headers import TataValidator
    from geometric_cleanliness_validator import GeometricCleanlinessValidator
    from trident_flow_controller import TridentFlowController
    from resonance_validation_system import ResonanceValidator
except ImportError as e:
    print(f"\nERROR: Failed to import required components: {e}")
    print("Ensure all components are properly installed in the FIELD directory.")
    sys.exit(1)

async def test_trident_flow():
    """Test the complete Trident flow with real investigation data"""
    try:
    
    # Create test data from real investigation
        investigation_data = {
        "_geometric": {
            "origin": {"x": 0, "y": 0, "z": 0},
            "phi_ratio": 1.618033988749895,
            "state": "PROCESSING"
        },
        "_resonance": {
            "geometric_alignment": 0.95,
            "pattern_resonance": 0.90,
            "harmonic_coherence": 0.97,
            "quantum_stability": 0.85
        },
        "content": {
            "investigation_id": "investigation-1758032257",
            "timestamp": "2025-09-17T00:00:00Z",
            "entities": [
                {
                    "name": "CENTOSA SA",
                    "type": "company",
                    "jurisdiction": "BVI",
                    "status": "active",
                    "investigation_priority": "high"
                },
                {
                    "name": "PASCALI TRUST",
                    "type": "trust",
                    "jurisdiction": "unknown",
                    "status": "under_investigation",
                    "investigation_priority": "high"
                },
                {
                    "name": "Jacques Rich",
                    "type": "individual",
                    "accounts": ["BEKB 16 734.081.3.19"],
                    "investigation_priority": "high"
                }
            ],
            "financial_data": {
                "csv_files": 94,
                "pdf_documents": 1267,
                "high_priority_alerts": 12,
                "significant_transactions": [
                    {"amount": 137441.70, "currency": "USD"},
                    {"amount": 350000.00, "currency": "USD"}
                ]
            }
        },
        "metadata": {
            "source": "31-task investigation report",
            "system_status": "PARTIALLY_READY",
            "operational_percentage": 71.4,
            "timestamp": "2025-09-19T14:31:24Z"
        }
    }
    
        print("\n1. Initializing Trident Flow Controller...")
        controller = TridentFlowController()
        resonance_validator = ResonanceValidator()
    
        print("\n2. Beginning data flow process...")
        success, processed_data = await controller.process_data(investigation_data)
    
        if success:
            print("\n✅ Data successfully processed through Trident flow")
            print("\n3. Flow stages completed:")
            for stage in controller.flow_history:
                print(f"\n{stage.component} Stage:")
                print(f"  Status: {stage.status}")
                print(f"  Timestamp: {stage.timestamp}")
                if stage.validation_result:
                    print("  Validation Results:")
                    pprint(stage.validation_result, indent=4)
                
            print("\n4. Checking final resonance measurements...")
            valid, resonance_results = resonance_validator.validate_resonance(processed_data)
            print("\nResonance Results:")
            pprint(resonance_results, indent=4)
        
            print("\n5. Final processed data structure:")
            print("\nGeometric metadata:")
            pprint(processed_data.get('_geometric', {}), indent=4)
            print("\nTATA validation:")
            pprint(processed_data.get('_tata_validation', {}), indent=4)
            print("\nATLAS validation:")
            pprint(processed_data.get('_atlas_validation', {}), indent=4)
        
        else:
            print("\n❌ Data processing failed")
            print("\nFlow Status:")
            pprint(controller.get_flow_status(), indent=4)
    except Exception as e:
        print(f"\nERROR: Test execution failed: {e}")
        print("\nTraceback:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_trident_flow())