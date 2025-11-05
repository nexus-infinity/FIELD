#!/usr/bin/env python3
"""
Datashare Project Setup for Jacques Rich Investigation
Creates projects and initiates indexing for all entity categories
"""

import requests
import json
import time
from pathlib import Path

DATASHARE_URL = "http://localhost:9630"
DATA_DIR = "/Users/jbear/Datashare"

# Project definitions with key entities for each
PROJECTS = {
    "jacques-rich-estate-documents": {
        "description": "Main estate documents, wills, trusts",
        "entities": ["Jacques Rich", "Adam Rich", "David Rich", "PASCALI TRUST"]
    },
    "jacques-rich-corporate-structure": {
        "description": "Offshore companies and corporate entities", 
        "entities": ["CENTOSA SA", "FREELER ASSOCIATES SA", "FRELIA SA", "BERJAK NOMINEES NT"]
    },
    "jacques-rich-banking-records": {
        "description": "Banking relationships and transactions",
        "entities": ["Rothschild Bank", "NAB", "CENTOSA280211", "David Rich"]
    },
    "jacques-rich-panama-papers": {
        "description": "Mossack Fonseca and Panama Papers connections",
        "entities": ["Mossack Fonseca", "bearer shares", "Cumberland Building Company", "Adam Rich"]
    },
    "jacques-rich-regulatory-matters": {
        "description": "ASIC, ATO, and regulatory investigations",
        "entities": ["Verdeck Nominees NT", "ASIC", "ATO", "regulatory"]
    }
}

def create_project(project_name):
    """Create a project in Datashare"""
    url = f"{DATASHARE_URL}/api/project/{project_name}"
    
    # Try PUT method first
    response = requests.put(url, headers={'Content-Type': 'application/json'})
    if response.status_code not in [200, 201, 409]:  # 409 = already exists
        # Try POST method
        response = requests.post(f"{DATASHARE_URL}/api/project", 
                               json={"name": project_name},
                               headers={'Content-Type': 'application/json'})
    
    print(f"Project {project_name}: {response.status_code} - {response.text}")
    return response.status_code in [200, 201, 409]

def start_indexing(project_name):
    """Start indexing for a project"""
    data_path = Path(DATA_DIR) / project_name
    if not data_path.exists():
        print(f"Warning: Data directory {data_path} does not exist")
        return False
        
    url = f"{DATASHARE_URL}/api/project/{project_name}/index"
    payload = {
        "path": str(data_path),
        "options": {
            "resume": True,
            "filter": True
        }
    }
    
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    print(f"Indexing {project_name}: {response.status_code} - {response.text}")
    return response.status_code in [200, 201]

def get_project_stats(project_name):
    """Get statistics for a project"""
    url = f"{DATASHARE_URL}/api/project/{project_name}/statistics"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def main():
    print("Setting up Datashare projects for Jacques Rich investigation...")
    
    # Check if Datashare is running
    try:
        response = requests.get(f"{DATASHARE_URL}/api/status")
        if response.status_code != 200:
            print("ERROR: Datashare is not running or not accessible")
            return
        print("✓ Datashare is running")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Datashare on localhost:9630")
        return
    
    # Create projects
    for project_name, config in PROJECTS.items():
        print(f"\n--- Setting up {project_name} ---")
        print(f"Description: {config['description']}")
        print(f"Key entities: {', '.join(config['entities'])}")
        
        if create_project(project_name):
            print(f"✓ Project {project_name} created/exists")
            
            # Start indexing
            if start_indexing(project_name):
                print(f"✓ Indexing started for {project_name}")
            else:
                print(f"⚠ Failed to start indexing for {project_name}")
        else:
            print(f"✗ Failed to create project {project_name}")
    
    # Wait a moment and check stats
    print("\n--- Waiting for initial indexing ---")
    time.sleep(5)
    
    for project_name in PROJECTS.keys():
        stats = get_project_stats(project_name)
        if stats:
            print(f"{project_name}: {stats}")
        else:
            print(f"{project_name}: Stats not available yet")

if __name__ == "__main__":
    main()