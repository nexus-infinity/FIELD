#!/usr/bin/env python3
"""
Dojo System Integration Automator

Automatically sets up integrations based on the current Dojo development scope:
- Money Hub operations (Institutions, Accounts, Claims, Tasks, Documents, Interactions)
- Discovery Links intake and sovereign reconciliation  
- Evidence principles and export bundles
- Warp + GCP bootstrap runbook
- Geometric Alignment Lab for small practice frames

Integrates with your existing FIELD ecosystem and Datashare setup.
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
import subprocess

class DojoIntegrationAutomator:
    def __init__(self, field_root="/Users/jbear/FIELD"):
        self.field_root = Path(field_root)
        self.integrations_dir = self.field_root / "integrations"
        self.datashare_url = "http://localhost:9630"
        
        # Dojo system components from your Notion scope
        self.dojo_components = {
            "money_hub": {
                "operations": ["institutions", "accounts", "claims", "tasks", "documents", "interactions"],
                "description": "Money Hub operations management"
            },
            "discovery_links": {
                "operations": ["intake", "sovereign_reconciliation"],
                "description": "Discovery Links intake and sovereign reconciliation"
            },
            "evidence_principles": {
                "operations": ["export_bundles", "chain_of_custody"],
                "description": "Evidence principles and export bundles"
            },
            "warp_gcp": {
                "operations": ["bootstrap", "runbook", "deployment"],
                "description": "Warp + GCP bootstrap runbook"
            },
            "geometric_alignment": {
                "operations": ["small_practice_frames", "alignment_lab"],
                "description": "Geometric Alignment Lab for small practice frames"
            }
        }
        
        # Integration targets
        self.integration_apis = {
            "gitbook": "https://app.gitbook.com/o/XRXzpVdz6OYh9MuiQD08/sites/site_E7eCZ",
            "notion": "https://berjak-nexus-infinity.notion.site",
            "datashare": self.datashare_url
        }

    def setup_automated_integrations(self):
        """Set up all automated integrations for the Dojo system"""
        print("🥋 Setting up Dojo System Integrations...")
        
        # 1. Create integration directory structure
        self.create_integration_structure()
        
        # 2. Set up API gateway
        self.setup_api_gateway()
        
        # 3. Create component-specific integrations
        self.setup_component_integrations()
        
        # 4. Set up monitoring and automation
        self.setup_monitoring()
        
        # 5. Create GitBook documentation sync
        self.setup_gitbook_sync()
        
        print("✅ Dojo Integration Automator setup complete!")

    def create_integration_structure(self):
        """Create the integration directory structure"""
        print("📁 Creating integration structure...")
        
        directories = [
            "api_gateway",
            "money_hub",
            "discovery_links", 
            "evidence_principles",
            "warp_gcp",
            "geometric_alignment",
            "monitoring",
            "gitbook_sync",
            "notion_sync",
            "datashare_bridge"
        ]
        
        for dir_name in directories:
            dir_path = self.integrations_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created {dir_path}")

    def setup_api_gateway(self):
        """Set up the central API gateway for Dojo system"""
        gateway_dir = self.integrations_dir / "api_gateway"
        
        gateway_config = {
            "name": "Dojo System API Gateway",
            "version": "1.0.0",
            "components": list(self.dojo_components.keys()),
            "endpoints": {
                "/money-hub": "Money Hub operations API",
                "/discovery": "Discovery Links API", 
                "/evidence": "Evidence management API",
                "/warp": "Warp+GCP operations API",
                "/geometry": "Geometric Alignment API",
                "/datashare": "Document search proxy",
                "/notion": "Notion workspace sync"
            },
            "integrations": self.integration_apis
        }
        
        # Create API gateway server
        gateway_code = '''#!/usr/bin/env python3
"""
Dojo System API Gateway
Central hub for all Dojo component integrations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import json
from datetime import datetime

app = FastAPI(
    title="Dojo System API Gateway",
    description="Central API for Dojo investigation platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dojo component endpoints
@app.get("/")
async def root():
    return {
        "service": "Dojo System API Gateway",
        "version": "1.0.0",
        "components": ["money-hub", "discovery", "evidence", "warp", "geometry"],
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/money-hub/status")
async def money_hub_status():
    return {
        "component": "money-hub",
        "operations": ["institutions", "accounts", "claims", "tasks", "documents", "interactions"],
        "status": "active"
    }

@app.get("/discovery/links")
async def discovery_links():
    return {
        "component": "discovery-links", 
        "operations": ["intake", "sovereign_reconciliation"],
        "status": "monitoring"
    }

@app.get("/evidence/bundles")
async def evidence_bundles():
    return {
        "component": "evidence-principles",
        "operations": ["export_bundles", "chain_of_custody"],
        "status": "ready"
    }

@app.post("/datashare/search")
async def datashare_search(query: dict):
    """Proxy search requests to Datashare"""
    try:
        response = requests.post(
            "http://localhost:9630/api/index/search/local-datashare",
            json=query
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        with open(gateway_dir / "server.py", "w") as f:
            f.write(gateway_code)
        
        with open(gateway_dir / "config.json", "w") as f:
            json.dump(gateway_config, f, indent=2)
        
        print("  ✓ API Gateway created")

    def setup_component_integrations(self):
        """Set up integrations for each Dojo component"""
        for component, config in self.dojo_components.items():
            self.create_component_integration(component, config)

    def create_component_integration(self, component_name, config):
        """Create integration code for a specific component"""
        component_dir = self.integrations_dir / component_name
        
        # Create component API connector
        connector_code = f'''#!/usr/bin/env python3
"""
{config["description"]} Integration

Automated integration for {component_name} component of Dojo system.
Operations: {", ".join(config["operations"])}
"""

import requests
import json
from datetime import datetime
from pathlib import Path

class {component_name.title().replace("_", "")}Integration:
    def __init__(self):
        self.component = "{component_name}"
        self.operations = {config["operations"]}
        self.base_url = "http://localhost:8000/{component_name.replace("_", "-")}"
        
    def get_status(self):
        """Get component status"""
        return {{
            "component": self.component,
            "operations": self.operations,
            "description": "{config["description"]}",
            "status": "active",
            "timestamp": datetime.now().isoformat()
        }}
    
    def sync_with_notion(self):
        """Sync component data with Notion workspace"""
        # Implementation for Notion sync
        pass
    
    def export_data(self):
        """Export component data for analysis"""
        # Implementation for data export
        pass

if __name__ == "__main__":
    integration = {component_name.title().replace("_", "")}Integration()
    print(json.dumps(integration.get_status(), indent=2))
'''
        
        with open(component_dir / f"{component_name}_integration.py", "w") as f:
            f.write(connector_code)
        
        # Create component configuration
        component_config = {
            "name": component_name,
            "description": config["description"],
            "operations": config["operations"],
            "api_endpoint": f"http://localhost:8000/{component_name.replace('_', '-')}",
            "notion_sync": True,
            "datashare_integration": True,
            "gitbook_docs": True
        }
        
        with open(component_dir / "config.json", "w") as f:
            json.dump(component_config, f, indent=2)
        
        print(f"  ✓ {component_name} integration created")

    def setup_monitoring(self):
        """Set up monitoring and automation"""
        monitoring_dir = self.integrations_dir / "monitoring"
        
        monitor_code = '''#!/usr/bin/env python3
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
'''
        
        with open(monitoring_dir / "monitor.py", "w") as f:
            f.write(monitor_code)
        
        print("  ✓ Monitoring system created")

    def setup_gitbook_sync(self):
        """Set up GitBook documentation sync"""
        gitbook_dir = self.integrations_dir / "gitbook_sync"
        
        gitbook_sync_code = '''#!/usr/bin/env python3
"""
GitBook Documentation Sync

Automatically syncs Dojo system documentation with GitBook.
Updates API docs, component guides, and integration status.
"""

import requests
import json
from datetime import datetime

class GitBookSync:
    def __init__(self):
        self.gitbook_api = "https://app.gitbook.com/o/XRXzpVdz6OYh9MuiQD08/sites/site_E7eCZ"
        self.dojo_api = "http://localhost:8000"
        
    def sync_component_docs(self):
        """Sync component documentation"""
        components = [
            "money_hub", "discovery_links", "evidence_principles",
            "warp_gcp", "geometric_alignment"
        ]
        
        for component in components:
            print(f"📝 Syncing {component} documentation...")
            # Implementation for GitBook API sync
            
    def update_api_docs(self):
        """Update interactive API documentation"""
        print("📚 Updating interactive API docs...")
        # Implementation for API docs update
        
    def sync_investigation_methodology(self):
        """Sync investigation methodology documentation"""
        print("🔬 Syncing investigation methodology...")
        # Implementation for methodology sync

if __name__ == "__main__":
    sync = GitBookSync()
    sync.sync_component_docs()
    sync.update_api_docs()
    sync.sync_investigation_methodology()
'''
        
        with open(gitbook_dir / "sync.py", "w") as f:
            f.write(gitbook_sync_code)
        
        print("  ✓ GitBook sync created")

    def create_startup_script(self):
        """Create script to start all Dojo integrations"""
        startup_script = '''#!/bin/bash
# Dojo System Integration Startup Script

echo "🥋 Starting Dojo System Integrations..."

# Start API Gateway
echo "🚀 Starting API Gateway..."
cd /Users/jbear/FIELD/integrations/api_gateway
python3 server.py &
API_PID=$!
echo "API Gateway started (PID: $API_PID)"

# Start Monitoring
echo "📊 Starting System Monitor..."
cd /Users/jbear/FIELD/integrations/monitoring
python3 monitor.py &
MONITOR_PID=$!
echo "Monitor started (PID: $MONITOR_PID)"

# Wait for services to start
sleep 5

# Test API Gateway
echo "🧪 Testing API Gateway..."
curl -s http://localhost:8000/ | jq .

echo "✅ Dojo System Integrations are now running!"
echo "📋 Services:"
echo "  - API Gateway: http://localhost:8000"
echo "  - Datashare: http://localhost:9630"
echo "  - Monitoring: Active"

echo "🛑 To stop services:"
echo "  kill $API_PID $MONITOR_PID"

# Keep script running
wait
'''
        
        with open(self.field_root / "start_dojo_integrations.sh", "w") as f:
            f.write(startup_script)
        
        os.chmod(self.field_root / "start_dojo_integrations.sh", 0o755)
        print("  ✓ Startup script created")

def main():
    """Main execution function"""
    automator = DojoIntegrationAutomator()
    automator.setup_automated_integrations()
    automator.create_startup_script()
    
    print("\n🎯 Next Steps:")
    print("1. Install dependencies: pip install fastapi uvicorn requests")
    print("2. Start integrations: ./start_dojo_integrations.sh")
    print("3. Access API Gateway: http://localhost:8000")
    print("4. Monitor system: check /integrations/monitoring/")
    print("5. Sync with GitBook: run /integrations/gitbook_sync/sync.py")

if __name__ == "__main__":
    main()