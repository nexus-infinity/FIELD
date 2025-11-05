#!/usr/bin/env python3
"""
ICIJ Global Database Connector
Connects to Panama Papers, Paradise Papers, Offshore Leaks databases
"""

import requests
import json

class ICIJConnector:
    def __init__(self):
        self.base_url = "https://offshoreleaks.icij.org/search"
        self.databases = ["panama_papers", "paradise_papers", "offshore_leaks", "pandora_papers"]
    
    def search_entity(self, entity_name, database="all"):
        """Search for entity across ICIJ databases"""
        
        params = {
            "q": entity_name,
            "c": database if database != "all" else "all",
            "e": 1,  # Entities
            "a": 1,  # Addresses
            "o": 1   # Officers
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error searching ICIJ: {e}")
            return None
    
    def get_entity_details(self, entity_id):
        """Get detailed information about a specific entity"""
        # Implementation for detailed entity lookup
        pass
