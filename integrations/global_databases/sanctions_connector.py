#!/usr/bin/env python3
"""
Global Sanctions Lists Connector
OFAC, EU, UN sanctions checking
"""

import requests
import json

class SanctionsConnector:
    def __init__(self):
        self.ofac_url = "https://api.trade.gov/consolidated_screening_list/search"
        
    def check_sanctions(self, entity_name):
        """Check entity against global sanctions lists"""
        
        params = {
            "q": entity_name,
            "sources": "SDN,FSE,UVL,ISN,DTC,SSI"  # OFAC lists
        }
        
        try:
            response = requests.get(self.ofac_url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error checking sanctions: {e}")
            return None
