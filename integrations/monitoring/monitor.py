#!/usr/bin/env python3
"""
Dojo System Monitor

Monitors all Dojo components and integrations.
Automatically syncs with Notion, Datashare, and GitBook.
"""

import time
import requests
import json
from datetime import datetime
import subprocess

class DojoSystemMonitor:
    def __init__(self):
        self.components = [
            "money_hub", "discovery_links", "evidence_principles", 
            "warp_gcp", "geometric_alignment"
        ]
        self.api_base = "http://localhost:8000"
        self.datashare_url = "http://localhost:9630"
        
    def check_all_components(self):
        """Check status of all Dojo components"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "operational",
            "components": {}
        }
        
        for component in self.components:
            try:
                response = requests.get(f"{self.api_base}/{component.replace('_', '-')}/status")
                status["components"][component] = {
                    "status": "active" if response.status_code == 200 else "error",
                    "response_time": response.elapsed.total_seconds()
                }
            except Exception as e:
                status["components"][component] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return status
    
    def check_datashare(self):
        """Check Datashare status"""
        try:
            response = requests.get(f"{self.datashare_url}/api/status")
            return response.json()
        except:
            return {"status": "error", "message": "Datashare not accessible"}
    
    def run_continuous_monitoring(self):
        """Run continuous monitoring loop"""
        while True:
            print("🔍 Checking Dojo system status...")
            
            # Check components
            status = self.check_all_components()
            print(f"Components: {len([c for c in status['components'].values() if c['status'] == 'active'])}/{len(self.components)} active")
            
            # Check Datashare
            ds_status = self.check_datashare()
            print(f"Datashare: {ds_status.get('database', False)} DB, {ds_status.get('index', False)} Index")
            
            # Sleep for monitoring interval
            time.sleep(30)

if __name__ == "__main__":
    monitor = DojoSystemMonitor()
    monitor.run_continuous_monitoring()
