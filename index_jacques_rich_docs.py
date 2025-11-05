#!/usr/bin/env python3
"""
Corrected Datashare API client for Jacques Rich Investigation
Uses proper API endpoints discovered from the JavaScript bundle
"""

import requests
import json
import time
import os
from pathlib import Path

DATASHARE_URL = "http://localhost:9630"
DATA_DIR = "/Users/jbear/Datashare"
DEFAULT_PROJECT = "local-datashare"

def check_datashare_status():
    """Check if Datashare is running"""
    try:
        response = requests.get(f"{DATASHARE_URL}/api/status")
        print(f"Status: {response.json()}")
        return True
    except Exception as e:
        print(f"Error checking status: {e}")
        return False

def create_project(project_name):
    """Create a project using the correct API"""
    try:
        # First method: PUT to create project  
        url = f"{DATASHARE_URL}/api/project/{project_name}"
        response = requests.put(url, json={}, headers={'Content-Type': 'application/json'})
        print(f"Create project {project_name}: {response.status_code} - {response.text}")
        return response.status_code in [200, 201, 409]  # 409 = already exists
    except Exception as e:
        print(f"Error creating project {project_name}: {e}")
        return False

def start_indexing_task(project_name, data_path):
    """Start indexing task using the task API"""
    try:
        # Based on the JS, indexing uses task/batchUpdate/index
        url = f"{DATASHARE_URL}/api/task/batchUpdate/index/{project_name}"
        
        # Try the payload structure from the JS
        payload = {
            "path": str(data_path),
            "resume": True,
            "filter": True
        }
        
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        print(f"Start indexing {project_name} at {data_path}: {response.status_code} - {response.text}")
        
        if response.status_code in [200, 201, 202]:
            return True
            
        # Try alternative: direct index API
        url = f"{DATASHARE_URL}/api/index/{project_name}"
        response = requests.put(url, json=payload, headers={'Content-Type': 'application/json'})
        print(f"Alternative indexing {project_name}: {response.status_code} - {response.text}")
        
        return response.status_code in [200, 201, 202]
        
    except Exception as e:
        print(f"Error starting indexing for {project_name}: {e}")
        return False

def search_entities(entity_name, project=DEFAULT_PROJECT):
    """Search for specific entity using the correct API endpoint"""
    try:
        # Based on JS: /api/index/search/{project}
        url = f"{DATASHARE_URL}/api/index/search/{project}"
        
        params = {
            "q": entity_name,
            "from": 0,
            "size": 10,
            "sort": "_score"
        }
        
        response = requests.get(url, params=params, headers={'Accept': 'application/json'})
        print(f"Search '{entity_name}' in {project}: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            total_hits = results.get('hits', {}).get('total', {}).get('value', 0) if isinstance(results.get('hits', {}).get('total'), dict) else results.get('hits', {}).get('total', 0)
            print(f"  Found {total_hits} documents")
            
            if total_hits > 0:
                hits = results.get('hits', {}).get('hits', [])
                for hit in hits[:3]:  # Show first 3 results
                    source = hit.get('_source', {})
                    print(f"    - {source.get('path', 'Unknown')} (score: {hit.get('_score', 0)})")
            
            return results
        else:
            print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"Search error: {e}")
    
    return None

def get_tasks_status():
    """Get all running tasks status"""
    try:
        url = f"{DATASHARE_URL}/api/task/all"
        response = requests.get(url)
        print(f"Tasks status: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"Active tasks: {len(tasks)}")
            for task in tasks:
                print(f"  - {task.get('name', 'Unknown')}: {task.get('state', 'Unknown')}")
            return tasks
        else:
            print(f"  Error getting tasks: {response.text}")
            
    except Exception as e:
        print(f"Error getting task status: {e}")
    
    return []

def main():
    print("=== Jacques Rich Investigation - Datashare Corrected Setup ===")
    
    # Check data directory contents
    print(f"\nData directory contents ({DATA_DIR}):")
    project_dirs = []
    for item in Path(DATA_DIR).iterdir():
        if item.is_dir() and item.name.startswith('jacques-rich-'):
            file_count = len(list(item.glob("**/*"))) if item.exists() else 0
            print(f"  {item.name}: {file_count} files")
            project_dirs.append((item.name, item))
    
    # Check Datashare status
    print("\n--- Checking Datashare Status ---")
    if not check_datashare_status():
        print("Cannot connect to Datashare")
        return
    
    # Get current task status
    print("\n--- Current Task Status ---")
    get_tasks_status()
    
    # Create projects and start indexing
    print("\n--- Setting up Projects and Indexing ---")
    successful_projects = []
    
    for project_name, project_path in project_dirs:
        print(f"\n📁 Processing {project_name}...")
        
        # Create project
        if create_project(project_name):
            print(f"✓ Project {project_name} ready")
            
            # Start indexing
            if start_indexing_task(project_name, project_path):
                print(f"✓ Indexing started for {project_name}")
                successful_projects.append(project_name)
            else:
                print(f"⚠ Failed to start indexing for {project_name}")
        else:
            print(f"✗ Failed to create project {project_name}")
    
    if not successful_projects:
        print("\n⚠ No projects were successfully set up. Trying default project...")
        
        # Try to index everything in the default project
        print(f"\n--- Using Default Project ({DEFAULT_PROJECT}) ---")
        if create_project(DEFAULT_PROJECT):
            if start_indexing_task(DEFAULT_PROJECT, DATA_DIR):
                successful_projects.append(DEFAULT_PROJECT)
                print(f"✓ Default project indexing started")
    
    if successful_projects:
        # Wait for initial indexing
        print("\n--- Waiting for indexing to process (60 seconds) ---")
        for i in range(6):
            time.sleep(10)
            print(f"  {(i+1)*10}s elapsed...")
            get_tasks_status()
        
        # Search for key entities
        key_entities = [
            "CENTOSA SA",
            "PASCALI TRUST", 
            "Jacques Rich",
            "Adam Rich",
            "Mossack Fonseca",
            "bearer shares",
            "BERJAK NOMINEES",
            "David Rich"
        ]
        
        print("\n--- Searching for Key Entities ---")
        
        # Try searching in each successful project
        for project in successful_projects:
            print(f"\n📊 Searching in project: {project}")
            
            for entity in key_entities:
                print(f"\n🔍 Searching for: {entity}")
                results = search_entities(entity, project)
                
                if results:
                    total_hits = results.get('hits', {}).get('total', {}).get('value', 0) if isinstance(results.get('hits', {}).get('total'), dict) else results.get('hits', {}).get('total', 0)
                    if total_hits > 0:
                        print(f"  ✓ Found {total_hits} documents mentioning '{entity}' in {project}")
                    else:
                        print(f"  - No documents found for '{entity}' in {project}")
                else:
                    print(f"  ✗ Search failed for '{entity}' in {project}")
                
                time.sleep(0.5)  # Rate limit
    
    else:
        print("\n❌ No projects were successfully indexed. Manual intervention needed.")
        print("\nNext steps:")
        print("1. Open Datashare web interface at http://localhost:9630")
        print("2. Manually create projects and upload documents")
        print("3. Or check Datashare logs for errors")

if __name__ == "__main__":
    main()
