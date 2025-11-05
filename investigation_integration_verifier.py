#!/usr/bin/env python3
"""
Investigation Integration Verifier
Ensures 31-task investigation process has access to all FIELD system tools
"""

import requests
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class InvestigationIntegrationVerifier:
    def __init__(self):
        self.dojo_api = "http://localhost:8000"
        self.datashare_api = "http://localhost:9630"
        self.field_root = Path("/Users/jbear/FIELD")
        self.verification_results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "PENDING",
            "component_status": {},
            "data_access": {},
            "integration_health": {},
            "recommendations": []
        }
    
    def verify_api_gateway(self):
        """Verify DOJO API Gateway is operational"""
        try:
            response = requests.get(f"{self.dojo_api}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.verification_results["component_status"]["dojo_gateway"] = {
                    "status": "OPERATIONAL",
                    "components": data.get("components", []),
                    "version": data.get("version", "unknown")
                }
                print("✅ DOJO API Gateway: OPERATIONAL")
                return True
            else:
                self.verification_results["component_status"]["dojo_gateway"] = {
                    "status": "ERROR",
                    "error": f"HTTP {response.status_code}"
                }
                print(f"❌ DOJO API Gateway: ERROR (HTTP {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            self.verification_results["component_status"]["dojo_gateway"] = {
                "status": "UNREACHABLE",
                "error": str(e)
            }
            print(f"❌ DOJO API Gateway: UNREACHABLE ({e})")
            return False
    
    def verify_datashare(self):
        """Verify Datashare document search is operational"""
        try:
            # Test basic connectivity
            test_query = {"query": "test", "size": 1}
            response = requests.post(f"{self.datashare_api}/search", 
                                   json=test_query, timeout=10)
            if response.status_code == 200:
                self.verification_results["component_status"]["datashare"] = {
                    "status": "OPERATIONAL",
                    "search_capability": "CONFIRMED"
                }
                print("✅ Datashare Document Search: OPERATIONAL")
                return True
            else:
                self.verification_results["component_status"]["datashare"] = {
                    "status": "ERROR",
                    "error": f"HTTP {response.status_code}"
                }
                print(f"❌ Datashare: ERROR (HTTP {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            self.verification_results["component_status"]["datashare"] = {
                "status": "UNREACHABLE",
                "error": str(e)
            }
            print(f"❌ Datashare: UNREACHABLE ({e})")
            return False
    
    def verify_financial_data(self):
        """Verify access to comprehensive financial data"""
        tata_path = self.field_root / "▼TATA"
        financial_manifest = tata_path / "comprehensive_financial_manifest.json"
        account_list = tata_path / "R11_master_account_list_20250421.json"
        
        data_status = {
            "tata_directory": tata_path.exists(),
            "financial_manifest": financial_manifest.exists(),
            "master_account_list": account_list.exists(),
            "csv_files": 0,
            "pdf_files": 0
        }
        
        if tata_path.exists():
            csv_files = list(tata_path.rglob("*.csv"))
            pdf_files = list(tata_path.rglob("*.pdf"))
            data_status["csv_files"] = len(csv_files)
            data_status["pdf_files"] = len(pdf_files)
        
        self.verification_results["data_access"]["financial_data"] = data_status
        
        if data_status["tata_directory"] and data_status["financial_manifest"]:
            print(f"✅ Financial Data: ACCESSIBLE ({data_status['csv_files']} CSV, {data_status['pdf_files']} PDF files)")
            return True
        else:
            print("❌ Financial Data: NOT ACCESSIBLE")
            return False
    
    def verify_investigation_results(self):
        """Verify access to investigation results"""
        investigation_path = self.field_root / "investigation_results"
        
        investigation_status = {
            "directory_exists": investigation_path.exists(),
            "session_directories": [],
            "latest_session": None
        }
        
        if investigation_path.exists():
            session_dirs = [d for d in investigation_path.iterdir() if d.is_dir()]
            investigation_status["session_directories"] = [d.name for d in session_dirs]
            if session_dirs:
                latest_session = max(session_dirs, key=lambda d: d.stat().st_mtime)
                investigation_status["latest_session"] = latest_session.name
        
        self.verification_results["data_access"]["investigation_results"] = investigation_status
        
        if investigation_status["directory_exists"] and investigation_status["session_directories"]:
            print(f"✅ Investigation Results: ACCESSIBLE (Latest: {investigation_status['latest_session']})")
            return True
        else:
            print("❌ Investigation Results: NOT ACCESSIBLE")
            return False
    
    def verify_money_hub(self):
        """Verify Money Hub integration"""
        try:
            response = requests.get(f"{self.dojo_api}/money-hub/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.verification_results["integration_health"]["money_hub"] = {
                    "status": "OPERATIONAL",
                    "operations": data.get("operations", [])
                }
                print(f"✅ Money Hub: OPERATIONAL (Operations: {', '.join(data.get('operations', []))})")
                return True
            else:
                print(f"❌ Money Hub: ERROR (HTTP {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Money Hub: UNREACHABLE ({e})")
            return False
    
    def verify_evidence_bundle(self):
        """Verify Evidence Bundle capability"""
        try:
            response = requests.get(f"{self.dojo_api}/evidence/bundles", timeout=5)
            if response.status_code == 200:
                self.verification_results["integration_health"]["evidence_bundles"] = {
                    "status": "OPERATIONAL"
                }
                print("✅ Evidence Bundle Export: OPERATIONAL")
                return True
            else:
                print(f"❌ Evidence Bundle: ERROR (HTTP {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Evidence Bundle: UNREACHABLE ({e})")
            return False
    
    def test_investigation_searches(self):
        """Test critical investigation entity searches"""
        test_entities = ["CENTOSA SA", "PASCALI TRUST", "Jacques Rich"]
        search_results = {}
        
        for entity in test_entities:
            try:
                response = requests.post(f"{self.datashare_api}/search", 
                                       json={"query": entity, "size": 5}, 
                                       timeout=10)
                if response.status_code == 200:
                    results = response.json()
                    search_results[entity] = {
                        "status": "SUCCESS",
                        "hits": results.get("hits", {}).get("total", 0)
                    }
                    print(f"✅ Search '{entity}': {search_results[entity]['hits']} results")
                else:
                    search_results[entity] = {
                        "status": "ERROR",
                        "error": f"HTTP {response.status_code}"
                    }
                    print(f"❌ Search '{entity}': ERROR")
            except requests.exceptions.RequestException as e:
                search_results[entity] = {
                    "status": "FAILED",
                    "error": str(e)
                }
                print(f"❌ Search '{entity}': FAILED")
        
        self.verification_results["integration_health"]["search_tests"] = search_results
        return all(result.get("status") == "SUCCESS" for result in search_results.values())
    
    def generate_recommendations(self):
        """Generate recommendations based on verification results"""
        recommendations = []
        
        # Check component statuses
        dojo_status = self.verification_results["component_status"].get("dojo_gateway", {}).get("status")
        datashare_status = self.verification_results["component_status"].get("datashare", {}).get("status")
        
        if dojo_status != "OPERATIONAL":
            recommendations.append("🔧 Start DOJO API Gateway: Navigate to /Users/jbear/FIELD/integrations/api_gateway/ and run server.py")
        
        if datashare_status != "OPERATIONAL":
            recommendations.append("🔍 Start Datashare: Ensure Datashare is running on port 9630 with indexed documents")
        
        # Check data access
        financial_data = self.verification_results["data_access"].get("financial_data", {})
        if not financial_data.get("financial_manifest"):
            recommendations.append("📊 Financial Data: Verify access to TATA directory and financial manifest files")
        
        # Integration health
        money_hub = self.verification_results["integration_health"].get("money_hub")
        if not money_hub or money_hub.get("status") != "OPERATIONAL":
            recommendations.append("💰 Money Hub: Activate Money Hub integration for financial operations")
        
        evidence_bundle = self.verification_results["integration_health"].get("evidence_bundles")
        if not evidence_bundle or evidence_bundle.get("status") != "OPERATIONAL":
            recommendations.append("📋 Evidence Bundle: Ensure evidence export capability is functional")
        
        search_tests = self.verification_results["integration_health"].get("search_tests", {})
        failed_searches = [entity for entity, result in search_tests.items() 
                         if result.get("status") != "SUCCESS"]
        if failed_searches:
            recommendations.append(f"🔍 Search Issues: Review search capability for entities: {', '.join(failed_searches)}")
        
        # Add essential integration recommendations
        recommendations.extend([
            "🎯 31-Task Integration: Ensure investigation process uses API endpoints for entity searches",
            "📈 Real-time Monitoring: Use http://localhost:8000/ for system status monitoring",
            "🔗 Cross-Reference: Leverage both Dojo discovery and Datashare search for complete coverage",
            "⚖️ Evidence Export: Prepare legal-ready bundles using /evidence/bundles endpoint"
        ])
        
        self.verification_results["recommendations"] = recommendations
    
    def run_complete_verification(self):
        """Run complete verification suite"""
        print("🔍 INVESTIGATION INTEGRATION VERIFICATION")
        print("=" * 50)
        print(f"Verification Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        verification_checks = [
            ("API Gateway", self.verify_api_gateway),
            ("Datashare", self.verify_datashare),
            ("Financial Data", self.verify_financial_data),
            ("Investigation Results", self.verify_investigation_results),
            ("Money Hub", self.verify_money_hub),
            ("Evidence Bundle", self.verify_evidence_bundle),
            ("Search Tests", self.test_investigation_searches)
        ]
        
        passed_checks = 0
        total_checks = len(verification_checks)
        
        for check_name, check_function in verification_checks:
            print(f"\n🔍 Verifying {check_name}...")
            if check_function():
                passed_checks += 1
        
        # Generate overall status
        success_rate = passed_checks / total_checks
        if success_rate >= 0.8:
            self.verification_results["overall_status"] = "READY"
            status_emoji = "✅"
        elif success_rate >= 0.6:
            self.verification_results["overall_status"] = "PARTIALLY_READY"
            status_emoji = "⚠️"
        else:
            self.verification_results["overall_status"] = "NOT_READY"
            status_emoji = "❌"
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Display summary
        print("\n" + "=" * 50)
        print(f"{status_emoji} VERIFICATION SUMMARY")
        print("=" * 50)
        print(f"Overall Status: {self.verification_results['overall_status']}")
        print(f"Checks Passed: {passed_checks}/{total_checks} ({success_rate:.1%})")
        print()
        
        print("📋 RECOMMENDATIONS:")
        for i, recommendation in enumerate(self.verification_results["recommendations"], 1):
            print(f"{i}. {recommendation}")
        
        return self.verification_results
    
    def save_verification_report(self):
        """Save detailed verification report"""
        report_path = self.field_root / "investigation_verification_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.verification_results, f, indent=2)
        print(f"\n📄 Detailed report saved: {report_path}")

def main():
    """Main verification execution"""
    verifier = InvestigationIntegrationVerifier()
    results = verifier.run_complete_verification()
    verifier.save_verification_report()
    
    # Exit with appropriate code
    if results["overall_status"] == "READY":
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Issues found

if __name__ == "__main__":
    main()