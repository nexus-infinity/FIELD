#!/usr/bin/env python3
"""
FIELD Sovereign Sync Configuration System
Automatically configures Google Apps Script using FIELD credentials vault

This system:
1. Extracts Notion credentials from FIELD vault
2. Creates Data_Lake database if needed
3. Generates complete Google Apps Script configuration
4. Provides setup instructions and validation
"""

import json
import os
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Any

class FIELDSyncConfigurator:
    """Configures sovereign sync system using FIELD credentials"""
    
    def __init__(self):
        self.field_root = Path("/Users/jbear/FIELD")
        self.dojo_active = self.field_root / "◼︎DOJO_ACTIVE"
        self.credentials_vault = self.field_root / ".credentials_vault"
        
        # Load credentials
        self.notion_token = self.load_notion_credentials()
        self.drive_folder_id = "1HcjrZXlHi7yszRJCeYzg8wxzdFnTW3RQ"
        
        # Notion databases
        self.data_lake_db_id = None
        self.databases = {}
        
        print("🔧 FIELD Sovereign Sync Configurator initialized")
        print(f"📁 Credentials vault: {self.credentials_vault}")
        
    def load_notion_credentials(self):
        """Load Notion token from FIELD credentials vault"""
        env_file = self.credentials_vault / "field_api_keys.env"
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('export NOTION_TOKEN='):
                        token = line.split('=', 1)[1].strip().strip('"')
                        print(f"✅ Found Notion token: {token[:20]}...")
                        return token
        
        print("❌ Notion token not found in credentials vault")
        return None
    
    def create_notion_headers(self):
        """Create Notion API headers"""
        return {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    def find_or_create_data_lake_database(self):
        """Find existing Data_Lake database or create new one"""
        if not self.notion_token:
            print("❌ Cannot access Notion - no token available")
            return None
        
        headers = self.create_notion_headers()
        
        # Search for existing Data_Lake database
        print("🔍 Searching for existing Data_Lake database...")
        
        # List all databases (Note: This requires the integration to be added to databases)
        response = requests.post(
            "https://api.notion.com/v1/search",
            headers=headers,
            json={
                "query": "Data_Lake",
                "filter": {"property": "object", "value": "database"}
            }
        )
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            
            for result in results:
                if result.get('object') == 'database':
                    title_parts = result.get('title', [])
                    if title_parts and any('data_lake' in part.get('plain_text', '').lower() for part in title_parts):
                        db_id = result['id']
                        print(f"✅ Found existing Data_Lake database: {db_id}")
                        return db_id
        
        # If not found, create new database
        print("📊 Creating new Data_Lake database...")
        return self.create_data_lake_database()
    
    def create_data_lake_database(self):
        """Create new Data_Lake database in Notion"""
        headers = self.create_notion_headers()
        
        # Need a parent page to create database
        # First, try to find a suitable parent or create one
        parent_page_id = self.find_or_create_parent_page()
        
        if not parent_page_id:
            print("❌ Could not find or create parent page for Data_Lake database")
            return None
        
        # Create database schema
        database_schema = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": "Data_Lake"}}],
            "properties": {
                "File Name": {"title": {}},
                "Source Link": {"url": {}},
                "Date": {"date": {}},
                "Entity": {"multi_select": {"options": [
                    {"name": "Rich Family", "color": "red"},
                    {"name": "Trust Structure", "color": "orange"},
                    {"name": "Corporate Entity", "color": "yellow"},
                    {"name": "Financial Institution", "color": "green"},
                    {"name": "Legal Entity", "color": "blue"},
                    {"name": "Government Authority", "color": "purple"},
                    {"name": "Offshore Structure", "color": "pink"},
                    {"name": "Property", "color": "brown"},
                    {"name": "Unclassified", "color": "gray"}
                ]}},
                "Topic": {"multi_select": {"options": [
                    {"name": "Financial Records", "color": "green"},
                    {"name": "Legal Documents", "color": "blue"},
                    {"name": "Communications", "color": "yellow"},
                    {"name": "Tax Documents", "color": "orange"},
                    {"name": "Property Finance", "color": "red"},
                    {"name": "Property Rights", "color": "purple"},
                    {"name": "Planning Documents", "color": "pink"},
                    {"name": "Law Enforcement", "color": "red"},
                    {"name": "Digital Security", "color": "blue"},
                    {"name": "Investigation", "color": "red"},
                    {"name": "Document", "color": "gray"},
                    {"name": "Evidence", "color": "red"},
                    {"name": "Intake", "color": "gray"}
                ]}},
                "File Size (KB)": {"number": {}},
                "File Type": {"select": {"options": [
                    {"name": "PDF Document", "color": "red"},
                    {"name": "Word Document", "color": "blue"},
                    {"name": "Image", "color": "green"},
                    {"name": "Spreadsheet", "color": "yellow"},
                    {"name": "Text File", "color": "gray"},
                    {"name": "Other", "color": "default"}
                ]}},
                "Last Modified": {"date": {}},
                "Investigation Priority": {"select": {"options": [
                    {"name": "Critical", "color": "red"},
                    {"name": "High", "color": "orange"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Standard", "color": "green"}
                ]}}
            }
        }
        
        response = requests.post(
            "https://api.notion.com/v1/databases",
            headers=headers,
            json=database_schema
        )
        
        if response.status_code == 200:
            db_data = response.json()
            db_id = db_data['id']
            print(f"✅ Created Data_Lake database: {db_id}")
            return db_id
        else:
            print(f"❌ Failed to create database: {response.status_code} - {response.text}")
            return None
    
    def find_or_create_parent_page(self):
        """Find or create a parent page for the database"""
        headers = self.create_notion_headers()
        
        # Search for existing FIELD workspace page
        response = requests.post(
            "https://api.notion.com/v1/search",
            headers=headers,
            json={
                "query": "FIELD",
                "filter": {"property": "object", "value": "page"}
            }
        )
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                # Use first found page as parent
                page_id = results[0]['id']
                print(f"✅ Found parent page for database: {page_id}")
                return page_id
        
        print("ℹ️  No suitable parent page found. Please create Data_Lake database manually in Notion.")
        return None
    
    def generate_google_apps_script_config(self):
        """Generate complete Google Apps Script configuration"""
        
        # Find or create Data_Lake database
        self.data_lake_db_id = self.find_or_create_data_lake_database()
        
        if not self.data_lake_db_id:
            # Use placeholder for manual setup
            self.data_lake_db_id = "YOUR_DATA_LAKE_DATABASE_ID_HERE"
            print("⚠️  Using placeholder database ID - manual configuration required")
        
        # Generate configuration
        config = {
            "NOTION_TOKEN": self.notion_token,
            "NOTION_DATABASE_ID": self.data_lake_db_id,
            "FOLDER_ID": self.drive_folder_id,
            "setup_complete": self.data_lake_db_id != "YOUR_DATA_LAKE_DATABASE_ID_HERE"
        }
        
        # Save configuration
        config_file = self.dojo_active / "google_apps_script_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"📝 Google Apps Script configuration saved: {config_file}")
        return config
    
    def create_setup_instructions(self, config):
        """Create detailed setup instructions for Google Apps Script"""
        
        instructions = f"""# Google Apps Script Setup Instructions

## 🚀 Automated Configuration Ready

Your FIELD credentials have been loaded and configuration is ready:

### **Configuration Values**
```
NOTION_TOKEN: {config['NOTION_TOKEN'][:20]}...
NOTION_DATABASE_ID: {config['NOTION_DATABASE_ID']}
FOLDER_ID: {config['FOLDER_ID']}
```

### **Setup Steps (5 minutes)**

1. **Open Google Apps Script**
   - Go to: https://script.google.com
   - Click "New Project"
   - Delete default code

2. **Paste Production Script**
   - Copy entire contents of: `notion_drive_sync_production.js`
   - Paste into Google Apps Script editor
   - Save project as: "FIELD Data_Lake Sync"

3. **Configure Script Properties**
   - Click gear icon (Project Settings)
   - Scroll to "Script Properties"
   - Add these properties:

   | Property Name | Value |
   |---------------|-------|
   | `NOTION_TOKEN` | `{config['NOTION_TOKEN']}` |
   | `NOTION_DATABASE_ID` | `{config['NOTION_DATABASE_ID']}` |
   | `FOLDER_ID` | `{config['FOLDER_ID']}` |

4. **Test Setup**
   - Select function: `setupFieldSync`
   - Click "Run" button
   - Grant permissions when prompted
   - Check logs for success messages

5. **Create Daily Trigger**
   - Select function: `createDailyTrigger`
   - Click "Run" button
   - Verify trigger in "Triggers" sidebar

### **Verification**
Run `testFieldSync()` to test with sample files before full sync.

### **Ready for Operation**
Once setup, your system will:
- ✅ Sync Drive folder daily at 6 AM Melbourne time
- ✅ Intelligent entity/topic classification
- ✅ De-duplication and priority assignment
- ✅ Full integration with FIELD sovereign systems

{"✅ **SETUP COMPLETE** - Database created automatically" if config['setup_complete'] else "⚠️  **MANUAL DATABASE SETUP REQUIRED**"}
"""
        
        # Save instructions
        instructions_file = self.dojo_active / "GOOGLE_APPS_SCRIPT_SETUP.md"
        with open(instructions_file, 'w') as f:
            f.write(instructions)
        
        print(f"📋 Setup instructions saved: {instructions_file}")
        return instructions
    
    def validate_configuration(self):
        """Validate the complete configuration"""
        print("\n🔍 CONFIGURATION VALIDATION")
        print("=" * 50)
        
        validation_results = {
            "notion_token": bool(self.notion_token),
            "drive_folder_access": True,  # Assume accessible since URL provided
            "data_lake_database": False,
            "google_apps_script_ready": False
        }
        
        # Test Notion connection
        if self.notion_token:
            try:
                headers = self.create_notion_headers()
                response = requests.get("https://api.notion.com/v1/users/me", headers=headers)
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"✅ Notion connection successful: {user_data.get('name', 'Unknown user')}")
                    validation_results["notion_connection"] = True
                else:
                    print(f"❌ Notion connection failed: {response.status_code}")
                    validation_results["notion_connection"] = False
            except Exception as e:
                print(f"❌ Notion connection error: {e}")
                validation_results["notion_connection"] = False
        
        # Check database
        if self.data_lake_db_id and self.data_lake_db_id != "YOUR_DATA_LAKE_DATABASE_ID_HERE":
            validation_results["data_lake_database"] = True
            print(f"✅ Data_Lake database configured: {self.data_lake_db_id}")
        else:
            print("⚠️  Data_Lake database needs manual setup")
        
        # Check Google Apps Script file
        gas_file = self.dojo_active / "notion_drive_sync_production.js"
        if gas_file.exists():
            validation_results["google_apps_script_ready"] = True
            print(f"✅ Google Apps Script file ready: {gas_file}")
        else:
            print("❌ Google Apps Script file not found")
        
        return validation_results
    
    def run_complete_configuration(self):
        """Run complete configuration process"""
        print("🔧 FIELD SOVEREIGN SYNC - COMPLETE CONFIGURATION")
        print("=" * 60)
        
        # Step 1: Generate configuration
        print("\n📋 STEP 1: Generating Google Apps Script configuration...")
        config = self.generate_google_apps_script_config()
        
        # Step 2: Create setup instructions
        print("\n📝 STEP 2: Creating setup instructions...")
        instructions = self.create_setup_instructions(config)
        
        # Step 3: Validate configuration
        print("\n🔍 STEP 3: Validating configuration...")
        validation = self.validate_configuration()
        
        # Step 4: Update sovereign system with configuration
        print("\n🏛️  STEP 4: Updating sovereign system...")
        self.update_sovereign_config(config)
        
        # Final summary
        print("\n✅ CONFIGURATION COMPLETE")
        print("=" * 40)
        print(f"📝 Setup instructions: GOOGLE_APPS_SCRIPT_SETUP.md")
        print(f"🔧 Configuration file: google_apps_script_config.json")
        
        if config['setup_complete']:
            print("🚀 **READY FOR IMMEDIATE USE** - Database created automatically")
            print("📋 Follow setup instructions to activate Google Apps Script")
        else:
            print("⚠️  **MANUAL DATABASE SETUP REQUIRED** - See instructions for details")
        
        return {
            'config': config,
            'instructions': instructions,
            'validation': validation
        }
    
    def update_sovereign_config(self, config):
        """Update sovereign system with new configuration"""
        sovereign_config = {
            'notion_token': config['NOTION_TOKEN'],
            'data_lake_db_id': config['NOTION_DATABASE_ID'],
            'drive_folder_id': config['FOLDER_ID'],
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'auto_configured': config['setup_complete']
        }
        
        # Save to FIELD credentials for sovereign system
        sovereign_config_file = self.dojo_active / "data_lake_config.json"
        with open(sovereign_config_file, 'w') as f:
            json.dump(sovereign_config, f, indent=2)
        
        print(f"🏛️  Sovereign configuration updated: {sovereign_config_file}")


def main():
    """Main configuration function"""
    configurator = FIELDSyncConfigurator()
    return configurator.run_complete_configuration()


if __name__ == "__main__":
    main()