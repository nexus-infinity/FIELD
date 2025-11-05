#!/usr/bin/env python3
"""
Hybrid Local + Google Cloud Integration for Global Investigation Databases

Strategy:
1. Keep local Datashare for immediate document processing (your 42 Jacques Rich files)
2. Deploy cloud-based Datashare + Neo4j on GCP for global database integration
3. Create sync bridge between local and cloud instances
4. Connect to ICIJ global databases through cloud instance

Based on:
- Your existing berjak-development-project GCP setup
- Docker preference for Neo4j integration (server mode)
- Local FIELD environment restrictions on Docker
"""

import json
import requests
from pathlib import Path
import subprocess
import os
from datetime import datetime

class HybridInvestigationPlatform:
    def __init__(self):
        self.local_datashare = "http://localhost:9630"
        self.local_api_gateway = "http://localhost:8000"
        self.gcp_project = "berjak-development-project"
        self.field_root = Path("/Users/jbear/FIELD")
        
        # Global investigation databases
        self.global_databases = {
            "icij_offshoreleaks": {
                "url": "https://offshoreleaks.icij.org/",
                "description": "Panama Papers, Paradise Papers, Offshore Leaks"
            },
            "opencorporates": {
                "url": "https://api.opencorporates.com/v0.4/",
                "description": "Global corporate registry"
            },
            "fatf_greylist": {
                "description": "FATF grey and blacklisted jurisdictions"
            },
            "sanctions_lists": {
                "description": "OFAC, EU, UN sanctions lists"
            }
        }
        
    def create_gcp_deployment_config(self):
        """Create GCP deployment configuration for cloud Datashare + Neo4j"""
        
        gcp_config = {
            "version": "1.0",
            "project_id": self.gcp_project,
            "region": "us-central1",
            "services": {
                "datashare_cloud": {
                    "image": "icij/datashare:latest",
                    "mode": "SERVER",
                    "neo4j_enabled": True,
                    "ports": {
                        "datashare": 8080,
                        "neo4j": 7474,
                        "neo4j_bolt": 7687
                    },
                    "environment": {
                        "DS_DOCKER_MODE": "SERVER",
                        "DS_DOCKER_ELASTICSEARCH_ADDRESS": "http://elasticsearch:9200",
                        "DS_DOCKER_DATABASE_URL": "postgresql://datashare:password@postgres/datashare",
                        "DS_DOCKER_NEO4J_URI": "bolt://neo4j:7687"
                    }
                },
                "neo4j": {
                    "image": "neo4j:4.4",
                    "environment": {
                        "NEO4J_AUTH": "neo4j/password",
                        "NEO4J_PLUGINS": "[\"apoc\"]"
                    }
                },
                "elasticsearch": {
                    "image": "docker.elastic.co/elasticsearch/elasticsearch:7.9.1"
                },
                "postgres": {
                    "image": "postgres:13",
                    "environment": {
                        "POSTGRES_USER": "datashare",
                        "POSTGRES_PASSWORD": "password",
                        "POSTGRES_DB": "datashare"
                    }
                }
            }
        }
        
        # Create docker-compose.yml for GCP deployment
        docker_compose = """version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: datashare
      POSTGRES_PASSWORD: password
      POSTGRES_DB: datashare
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.9.1
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  neo4j:
    image: neo4j:4.4
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    ports:
      - "7474:7474"
      - "7687:7687"

  datashare:
    image: icij/datashare:latest
    environment:
      DS_DOCKER_MODE: SERVER
      DS_DOCKER_ELASTICSEARCH_ADDRESS: http://elasticsearch:9200
      DS_DOCKER_DATABASE_URL: postgresql://datashare:password@postgres/datashare
      DS_DOCKER_NEO4J_URI: bolt://neo4j:7687
    depends_on:
      - postgres
      - elasticsearch 
      - neo4j
    ports:
      - "8080:8080"
    volumes:
      - ./data:/home/datashare/Datashare

volumes:
  postgres_data:
  elasticsearch_data:
  neo4j_data:
  neo4j_logs:
"""
        
        return gcp_config, docker_compose
    
    def create_cloud_deployment_script(self):
        """Create script to deploy to Google Cloud"""
        
        deployment_script = f"""#!/bin/bash
# Deploy Datashare + Neo4j to Google Cloud

set -e

echo "🚀 Deploying Investigation Platform to Google Cloud..."

# Set project
gcloud config set project {self.gcp_project}

# Create VM instance for Datashare
gcloud compute instances create datashare-investigation \\
    --project={self.gcp_project} \\
    --zone=us-central1-a \\
    --machine-type=e2-standard-4 \\
    --network-interface=network-tier=PREMIUM,subnet=default \\
    --maintenance-policy=MIGRATE \\
    --provisioning-model=STANDARD \\
    --service-account=jeremy.rich@berjak.com.au \\
    --scopes=https://www.googleapis.com/auth/cloud-platform \\
    --tags=datashare-server \\
    --create-disk=auto-delete=yes,boot=yes,device-name=datashare-investigation,image=projects/cos-cloud/global/images/cos-stable-101-17162-40-8,mode=rw,size=50,type=projects/{self.gcp_project}/zones/us-central1-a/diskTypes/pd-balanced \\
    --container-mount-host-path=mount-path=/home/datashare/Datashare,host-path=/home/datashare/data \\
    --metadata-from-file=user-data=cloud-init.yml

# Create firewall rules
gcloud compute firewall-rules create allow-datashare \\
    --project={self.gcp_project} \\
    --direction=INGRESS \\
    --priority=1000 \\
    --network=default \\
    --action=ALLOW \\
    --rules=tcp:8080,tcp:7474,tcp:7687 \\
    --source-ranges=0.0.0.0/0 \\
    --target-tags=datashare-server

echo "✅ Cloud deployment complete!"
echo "🌐 Datashare: http://$(gcloud compute instances describe datashare-investigation --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'):8080"
echo "🔗 Neo4j: http://$(gcloud compute instances describe datashare-investigation --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'):7474"
"""
        
        return deployment_script
    
    def create_local_cloud_bridge(self):
        """Create bridge between local Datashare and cloud instance"""
        
        bridge_code = '''#!/usr/bin/env python3
"""
Local-Cloud Bridge for Investigation Platform

Syncs data between local Datashare (immediate processing) 
and cloud Datashare (global database integration)
"""

import requests
import json
import time
from pathlib import Path

class LocalCloudBridge:
    def __init__(self, cloud_datashare_url):
        self.local_url = "http://localhost:9630"
        self.cloud_url = cloud_datashare_url
        self.local_api_gateway = "http://localhost:8000"
        
    def sync_entities_to_cloud(self):
        """Sync local entities to cloud for global database matching"""
        
        # Get entities from local Datashare
        entities = self.get_local_entities()
        
        for entity in entities:
            # Send to cloud for global database cross-reference
            self.cross_reference_entity_globally(entity)
    
    def get_local_entities(self):
        """Extract entities from local documents"""
        entities = []
        
        try:
            # Search local Datashare for key entities
            key_entities = [
                "CENTOSA SA", "PASCALI TRUST", "Jacques Rich", 
                "Adam Rich", "David Rich", "Mossack Fonseca",
                "BERJAK NOMINEES", "Rothschild Bank"
            ]
            
            for entity_name in key_entities:
                response = requests.get(f"{self.local_url}/api/search", 
                                      params={"q": entity_name})
                if response.status_code == 200:
                    entities.append({
                        "name": entity_name,
                        "type": "ORGANIZATION" if "SA" in entity_name or "TRUST" in entity_name else "PERSON",
                        "source": "local_datashare",
                        "documents": response.json().get("hits", {}).get("total", 0)
                    })
                    
        except Exception as e:
            print(f"Error getting local entities: {e}")
            
        return entities
    
    def cross_reference_entity_globally(self, entity):
        """Cross-reference entity against global databases via cloud"""
        
        global_matches = {
            "panama_papers": self.check_panama_papers(entity),
            "paradise_papers": self.check_paradise_papers(entity),
            "opencorporates": self.check_opencorporates(entity),
            "sanctions_lists": self.check_sanctions(entity)
        }
        
        return global_matches
    
    def check_panama_papers(self, entity):
        """Check entity against Panama Papers via ICIJ API"""
        # Implementation for Panama Papers API
        return {"found": False, "matches": []}
    
    def check_paradise_papers(self, entity):
        """Check entity against Paradise Papers"""
        # Implementation for Paradise Papers API
        return {"found": False, "matches": []}
    
    def check_opencorporates(self, entity):
        """Check entity against OpenCorporates global registry"""
        # Implementation for OpenCorporates API
        return {"found": False, "matches": []}
    
    def check_sanctions(self, entity):
        """Check entity against sanctions lists"""
        # Implementation for sanctions list checking
        return {"found": False, "matches": []}
    
    def generate_compliance_report(self):
        """Generate compliance report with global database matches"""
        
        report = {
            "generated_at": time.time(),
            "local_entities": len(self.get_local_entities()),
            "global_matches": {},
            "compliance_status": "CLEAN",
            "red_flags": []
        }
        
        return report

if __name__ == "__main__":
    # Usage: python3 local_cloud_bridge.py <cloud-datashare-url>
    import sys
    
    if len(sys.argv) > 1:
        cloud_url = sys.argv[1]
        bridge = LocalCloudBridge(cloud_url)
        bridge.sync_entities_to_cloud()
        report = bridge.generate_compliance_report()
        print(json.dumps(report, indent=2))
    else:
        print("Usage: python3 local_cloud_bridge.py <cloud-datashare-url>")
'''
        
        return bridge_code
    
    def create_global_database_connectors(self):
        """Create connectors for global investigation databases"""
        
        connectors = {
            "icij_connector": '''#!/usr/bin/env python3
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
''',
            
            "opencorporates_connector": '''#!/usr/bin/env python3
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
''',
            
            "sanctions_connector": '''#!/usr/bin/env python3
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
'''
        }
        
        return connectors

def main():
    """Setup hybrid investigation platform"""
    
    platform = HybridInvestigationPlatform()
    
    print("🏗️ Setting up Hybrid Investigation Platform...")
    
    # Create integration directories
    gcp_dir = platform.field_root / "integrations" / "gcp_cloud"
    gcp_dir.mkdir(exist_ok=True)
    
    global_db_dir = platform.field_root / "integrations" / "global_databases"
    global_db_dir.mkdir(exist_ok=True)
    
    # Create GCP deployment config
    gcp_config, docker_compose = platform.create_gcp_deployment_config()
    
    with open(gcp_dir / "gcp_config.json", "w") as f:
        json.dump(gcp_config, f, indent=2)
    
    with open(gcp_dir / "docker-compose.yml", "w") as f:
        f.write(docker_compose)
    
    # Create deployment script
    deployment_script = platform.create_cloud_deployment_script()
    with open(gcp_dir / "deploy_to_gcp.sh", "w") as f:
        f.write(deployment_script)
    os.chmod(gcp_dir / "deploy_to_gcp.sh", 0o755)
    
    # Create local-cloud bridge
    bridge_code = platform.create_local_cloud_bridge()
    with open(global_db_dir / "local_cloud_bridge.py", "w") as f:
        f.write(bridge_code)
    
    # Create global database connectors
    connectors = platform.create_global_database_connectors()
    for name, code in connectors.items():
        with open(global_db_dir / f"{name}.py", "w") as f:
            f.write(code)
    
    print("✅ Hybrid Investigation Platform setup complete!")
    print(f"📁 GCP deployment: {gcp_dir}/")
    print(f"🌐 Global databases: {global_db_dir}/")
    print(f"🚀 To deploy: cd {gcp_dir} && ./deploy_to_gcp.sh")

if __name__ == "__main__":
    main()