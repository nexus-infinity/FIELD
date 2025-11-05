#!/usr/bin/env python3
"""
External Data Integration Dashboard
Complete external data validation system for FIELD investigations
"""

import asyncio
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add integrations directory to path
sys.path.append('/Users/jbear/FIELD/integrations')

try:
    from external_data_manager import ExternalDataManager
except ImportError:
    print("⚠️  External Data Manager not available - creating basic implementation")
    class ExternalDataManager:
        def __init__(self):
            self.field_root = Path("/Users/jbear/FIELD")
        
        def get_data_sources_status(self):
            return {"status": "basic_mode", "sources": {}}

class ExternalDataDashboard:
    def __init__(self):
        self.field_root = Path("/Users/jbear/FIELD")
        self.manager = ExternalDataManager()
        self.services_status = {}
        
    def display_banner(self):
        """Display dashboard banner"""
        print("🌐" + "="*80 + "🌐")
        print("    FIELD EXTERNAL DATA INTEGRATION DASHBOARD")
        print("    Comprehensive External Data Validation System")
        print("    For 31-Task Investigation Process")
        print("🌐" + "="*80 + "🌐")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def check_system_status(self):
        """Check status of all integrated systems"""
        print("📊 SYSTEM STATUS CHECK")
        print("-" * 50)
        
        # Check DOJO API Gateway
        try:
            import requests
            response = requests.get("http://localhost:8000/", timeout=3)
            if response.status_code == 200:
                print("✅ DOJO API Gateway: OPERATIONAL (Port 8000)")
                self.services_status['dojo'] = True
            else:
                print(f"⚠️  DOJO API Gateway: HTTP {response.status_code}")
                self.services_status['dojo'] = False
        except Exception:
            print("❌ DOJO API Gateway: NOT ACCESSIBLE")
            self.services_status['dojo'] = False

        # Check External Data API
        try:
            response = requests.get("http://localhost:8001/", timeout=3)
            if response.status_code == 200:
                print("✅ External Data API: OPERATIONAL (Port 8001)")
                self.services_status['external_api'] = True
            else:
                print(f"⚠️  External Data API: HTTP {response.status_code}")
                self.services_status['external_api'] = False
        except Exception:
            print("❌ External Data API: NOT RUNNING")
            self.services_status['external_api'] = False

        # Check Datashare
        try:
            response = requests.get("http://localhost:9630/", timeout=3)
            if response.status_code in [200, 302]:
                print("✅ Datashare: OPERATIONAL (Port 9630)")
                self.services_status['datashare'] = True
            else:
                print(f"⚠️  Datashare: HTTP {response.status_code}")
                self.services_status['datashare'] = False
        except Exception:
            print("❌ Datashare: NOT ACCESSIBLE")
            self.services_status['datashare'] = False

        print()

    def display_external_sources_status(self):
        """Display external data sources status"""
        print("🌍 EXTERNAL DATA SOURCES STATUS")
        print("-" * 50)
        
        try:
            status = self.manager.get_data_sources_status()
            
            for source_id, source_info in status.get("sources", {}).items():
                name = source_info.get("name", source_id)
                source_status = source_info.get("status", "unknown")
                api_key_required = source_info.get("api_key_required", False)
                api_key_configured = source_info.get("api_key_configured", False)
                
                if source_status == "active":
                    if api_key_required and not api_key_configured:
                        print(f"⚠️  {name}: ACTIVE (API key needed)")
                    else:
                        print(f"✅ {name}: READY")
                elif source_status == "ready":
                    print(f"🔄 {name}: READY FOR ACTIVATION")
                else:
                    print(f"📋 {name}: {source_status.upper()}")
            
            print()
            print(f"📈 Ready Sources: {len(status.get('ready_sources', []))}")
            print(f"🔑 API Keys Needed: {len(status.get('configuration_needed', []))}")
            
        except Exception as e:
            print(f"❌ Error checking external sources: {e}")
        
        print()

    def display_investigation_entities(self):
        """Display key investigation entities"""
        print("🔍 KEY INVESTIGATION ENTITIES")
        print("-" * 50)
        
        entities = {
            "Primary Targets": ["CENTOSA SA", "PASCALI TRUST", "Jacques Rich"],
            "Associated Entities": ["Adam Rich", "David Rich", "BERJAK NOMINEES"],
            "Financial Institutions": ["Rothschild Bank", "NAB", "BEKB Swiss"]
        }
        
        for category, entity_list in entities.items():
            print(f"📂 {category}:")
            for entity in entity_list:
                print(f"   • {entity}")
            print()

    def display_available_endpoints(self):
        """Display available API endpoints"""
        print("🔗 AVAILABLE API ENDPOINTS")
        print("-" * 50)
        
        endpoints = {
            "DOJO System (Port 8000)": [
                "GET  /                      - System status",
                "GET  /money-hub/status      - Financial operations",
                "GET  /discovery/links       - Entity discovery",
                "GET  /evidence/bundles      - Evidence export",
                "POST /datashare/search      - Document search"
            ],
            "External Data API (Port 8001)": [
                "GET  /                      - External API status",
                "GET  /validate/{entity}     - Single entity validation",
                "POST /batch-validate        - Multiple entity validation",
                "GET  /investigation/validate - Key entities validation",
                "GET  /sources/status        - Data sources status",
                "GET  /reports/compliance    - Compliance report"
            ]
        }
        
        for service, endpoint_list in endpoints.items():
            print(f"🌐 {service}:")
            for endpoint in endpoint_list:
                print(f"   {endpoint}")
            print()

    def run_quick_validation_test(self):
        """Run quick validation test"""
        print("🧪 QUICK VALIDATION TEST")
        print("-" * 50)
        
        if not self.services_status.get('external_api'):
            print("❌ External Data API not running - starting it...")
            self.start_external_data_api()
            time.sleep(3)
        
        try:
            import requests
            
            # Test external data sources status
            print("Testing external data sources...")
            response = requests.get("http://localhost:8001/sources/status", timeout=10)
            if response.status_code == 200:
                print("✅ External data sources: ACCESSIBLE")
            else:
                print(f"⚠️  External data sources: HTTP {response.status_code}")
            
            # Test single entity validation
            print("Testing entity validation...")
            response = requests.get("http://localhost:8001/validate/test", timeout=15)
            if response.status_code == 200:
                print("✅ Entity validation: FUNCTIONAL")
            else:
                print(f"⚠️  Entity validation: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Validation test failed: {e}")
        
        print()

    def start_external_data_api(self):
        """Start the external data API"""
        print("🚀 STARTING EXTERNAL DATA API")
        print("-" * 50)
        
        try:
            # Start external data API in background
            api_script = self.field_root / "integrations" / "external_data_api.py"
            if api_script.exists():
                print("Starting External Data API on port 8001...")
                subprocess.Popen([
                    sys.executable, str(api_script)
                ], cwd=str(api_script.parent))
                print("✅ External Data API started")
            else:
                print("❌ External Data API script not found")
        except Exception as e:
            print(f"❌ Failed to start External Data API: {e}")
        
        print()

    def display_31_task_integration_guide(self):
        """Display integration guide for 31-task process"""
        print("🎯 31-TASK INVESTIGATION INTEGRATION GUIDE")
        print("-" * 50)
        
        print("📋 TASK CATEGORIES & EXTERNAL DATA USAGE:")
        print()
        
        categories = {
            "Tasks 1-10: Entity Identification & Verification": [
                "Use: /validate/{entity_name} for each primary entity",
                "Sources: ICIJ, OpenCorporates, Sanctions lists",
                "Focus: CENTOSA SA, PASCALI TRUST, Jacques Rich"
            ],
            "Tasks 11-20: Financial Pattern Analysis": [
                "Use: /investigation/validate for comprehensive analysis",
                "Sources: World Bank, LEI Registry, Sanctions",
                "Compare: Internal financial data vs external records"
            ],
            "Tasks 21-30: Cross-Reference & Risk Assessment": [
                "Use: /reports/compliance for detailed risk assessment",
                "Sources: All external sources + internal comparison",
                "Output: Legal-ready compliance report"
            ],
            "Task 31: Final Evidence Package": [
                "Use: /evidence/bundles (DOJO) + compliance report",
                "Sources: Complete external validation results",
                "Deliver: Comprehensive evidence package"
            ]
        }
        
        for category, instructions in categories.items():
            print(f"🔥 {category}")
            for instruction in instructions:
                print(f"   {instruction}")
            print()

    def display_command_examples(self):
        """Display practical command examples"""
        print("💻 PRACTICAL COMMAND EXAMPLES")
        print("-" * 50)
        
        examples = [
            {
                "Task": "Validate CENTOSA SA",
                "Command": "curl http://localhost:8001/validate/\"CENTOSA SA\""
            },
            {
                "Task": "Validate all investigation entities",
                "Command": "curl http://localhost:8001/investigation/validate"
            },
            {
                "Task": "Generate compliance report",
                "Command": "curl http://localhost:8001/reports/compliance"
            },
            {
                "Task": "Check external data sources status",
                "Command": "curl http://localhost:8001/sources/status"
            },
            {
                "Task": "Get system health",
                "Command": "curl http://localhost:8000/"
            },
            {
                "Task": "Export evidence bundle",
                "Command": "curl http://localhost:8000/evidence/bundles"
            }
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example['Task']}:")
            print(f"   {example['Command']}")
            print()

    def display_data_comparison_benefits(self):
        """Display benefits of external data comparison"""
        print("📊 EXTERNAL DATA COMPARISON BENEFITS")
        print("-" * 50)
        
        benefits = [
            "✅ VALIDATION: Verify internal investigation findings against global databases",
            "✅ DISCOVERY: Find additional connections not visible in internal data",
            "✅ COMPLIANCE: Ensure entities are not on sanctions or debarment lists",
            "✅ RISK ASSESSMENT: Generate comprehensive risk scores based on multiple sources",
            "✅ LEGAL DEFENSIBILITY: Create audit trails with external data references",
            "✅ COMPLETENESS: Ensure no critical information is missed",
            "✅ CREDIBILITY: Strengthen investigation with independent data sources",
            "✅ AUTOMATION: Reduce manual research time through API integration"
        ]
        
        for benefit in benefits:
            print(f"   {benefit}")
        
        print()

    def display_next_steps(self):
        """Display recommended next steps"""
        print("🚀 RECOMMENDED NEXT STEPS")
        print("-" * 50)
        
        steps = [
            "1. 🔧 START SERVICES: Ensure DOJO API (8000) and External Data API (8001) are running",
            "2. 🧪 RUN TEST: Execute validation test to confirm external data sources are accessible",
            "3. 🎯 VALIDATE ENTITIES: Start with primary investigation entities (CENTOSA SA, PASCALI TRUST)",
            "4. 📊 COMPARE DATA: Use comparison endpoints to validate internal vs external data",
            "5. 📋 GENERATE REPORTS: Create compliance and risk assessment reports",
            "6. 🔗 INTEGRATE 31-TASKS: Use API endpoints within your investigation workflow",
            "7. 📄 EXPORT EVIDENCE: Generate comprehensive evidence packages for legal use"
        ]
        
        for step in steps:
            print(f"   {step}")
        
        print()

    def interactive_menu(self):
        """Interactive menu system"""
        while True:
            print("\n" + "="*60)
            print("🎛️  EXTERNAL DATA INTEGRATION CONTROL PANEL")
            print("="*60)
            print("1. 📊 Check System Status")
            print("2. 🌍 View External Sources Status") 
            print("3. 🧪 Run Validation Test")
            print("4. 🚀 Start External Data API")
            print("5. 🔍 View Investigation Entities")
            print("6. 🔗 View API Endpoints")
            print("7. 🎯 View 31-Task Integration Guide")
            print("8. 💻 View Command Examples")
            print("9. 📊 View Data Comparison Benefits")
            print("10. 🚀 View Next Steps")
            print("0. ❌ Exit")
            print()
            
            choice = input("Select option (0-10): ").strip()
            print()
            
            if choice == "1":
                self.check_system_status()
            elif choice == "2":
                self.display_external_sources_status()
            elif choice == "3":
                self.run_quick_validation_test()
            elif choice == "4":
                self.start_external_data_api()
            elif choice == "5":
                self.display_investigation_entities()
            elif choice == "6":
                self.display_available_endpoints()
            elif choice == "7":
                self.display_31_task_integration_guide()
            elif choice == "8":
                self.display_command_examples()
            elif choice == "9":
                self.display_data_comparison_benefits()
            elif choice == "10":
                self.display_next_steps()
            elif choice == "0":
                print("👋 Exiting External Data Integration Dashboard")
                break
            else:
                print("❌ Invalid option. Please select 0-10.")
            
            input("\nPress Enter to continue...")

    def run_full_dashboard(self):
        """Run complete dashboard display"""
        self.display_banner()
        self.check_system_status()
        self.display_external_sources_status()
        self.display_investigation_entities()
        self.display_available_endpoints()
        self.display_31_task_integration_guide()
        self.display_command_examples()
        self.display_data_comparison_benefits()
        self.display_next_steps()
        
        print("🎛️  For interactive control panel, run with --interactive")

def main():
    """Main dashboard execution"""
    dashboard = ExternalDataDashboard()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        dashboard.interactive_menu()
    else:
        dashboard.run_full_dashboard()

if __name__ == "__main__":
    main()