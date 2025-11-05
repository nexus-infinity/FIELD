#!/usr/bin/env python3
"""
OpenCorporates Global Registry Connector
"""

import requests
import json

class OpenCorporatesConnector:
    def __init__(self, api_key=None):
        self.base_url = "https://api.opencorporates.com/v0.4"
        self.api_key = api_key
    
    def search_company(self, company_name, jurisdiction=None):
        """Search for company in global registry"""
        
        params = {"q": company_name}
        if jurisdiction:
            params["jurisdiction_code"] = jurisdiction
        if self.api_key:
            params["api_token"] = self.api_key
            
        try:
            response = requests.get(f"{self.base_url}/companies/search", params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error searching OpenCorporates: {e}")
            return None
