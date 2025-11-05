#!/usr/bin/env python3
"""
Manual External Data Validation
Direct integration with external data sources for comprehensive validation
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class ManualExternalValidation:
    def __init__(self):
        self.field_root = Path("/Users/jbear/FIELD")
        self.results_dir = self.field_root / "external_validation_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Investigation entities
        self.investigation_entities = [
            "CENTOSA SA",
            "PASCALI TRUST", 
            "Jacques Rich",
            "Adam Rich",
            "David Rich",
            "BERJAK NOMINEES"
        ]
        
        self.session = requests.Session()
        self.session.timeout = 15

    def display_banner(self):
        """Display validation banner"""
        print("🌐" + "="*80 + "🌐")
        print("    MANUAL EXTERNAL DATA VALIDATION")
        print("    Direct External Source Integration")
        print("    Investigation Entity Validation")
        print("🌐" + "="*80 + "🌐")
        print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Entities to Validate: {len(self.investigation_entities)}")
        print()

    def validate_sanctions_ofac(self, entity_name: str) -> Dict[str, Any]:
        """Validate entity against OFAC sanctions list"""
        print(f"🔍 Checking OFAC Sanctions: {entity_name}")
        
        result = {
            "source": "OFAC Consolidated Screening List",
            "entity": entity_name,
            "status": "checked",
            "matches": 0,
            "results": [],
            "error": None
        }
        
        try:
            params = {
                "q": entity_name,
                "sources": "SDN,FSE,UVL,ISN,DTC,SSI,PART561,CAP,DPL,EL,UNNT"
            }
            
            response = self.session.get(
                "https://api.trade.gov/consolidated_screening_list/search",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get("total", 0)
                result["matches"] = matches
                result["results"] = data.get("results", [])[:3]  # First 3 matches
                
                if matches > 0:
                    print(f"   ⚠️  SANCTIONS FOUND: {matches} matches")
                    for match in result["results"]:
                        print(f"      • {match.get('name', 'Unknown')} - {match.get('source', 'Unknown source')}")
                else:
                    print(f"   ✅ CLEAR: No sanctions matches")
            else:
                result["error"] = f"HTTP {response.status_code}"
                print(f"   ❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            result["error"] = str(e)
            print(f"   ❌ ERROR: {e}")
        
        return result

    def validate_world_bank_debarment(self, entity_name: str) -> Dict[str, Any]:
        """Check World Bank debarment list"""
        print(f"🏛️ Checking World Bank Debarment: {entity_name}")
        
        result = {
            "source": "World Bank Debarred Firms",
            "entity": entity_name,
            "status": "checked",
            "matches": 0,
            "results": [],
            "error": None
        }
        
        try:
            params = {
                "format": "json",
                "os": 0,
                "size": 10,
                "qterm": entity_name
            }
            
            response = self.session.get(
                "https://apigwext.worldbank.org/dvsvc/v1.0/json/APPLICATION/ADOBE_EXPRNCE_MGR/FIRM/SANCTIONED_FIRM",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                firms = data.get("response", {}).get("FIRM", [])
                result["matches"] = len(firms)
                result["results"] = firms[:3]  # First 3 matches
                
                if result["matches"] > 0:
                    print(f"   ⚠️  DEBARMENT FOUND: {result['matches']} matches")
                    for firm in result["results"]:
                        print(f"      • {firm.get('FIRM_NAME', 'Unknown')} - {firm.get('COUNTRY', 'Unknown country')}")
                else:
                    print(f"   ✅ CLEAR: No debarment matches")
            else:
                result["error"] = f"HTTP {response.status_code}"
                print(f"   ❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            result["error"] = str(e)
            print(f"   ❌ ERROR: {e}")
        
        return result

    def validate_lei_registry(self, entity_name: str) -> Dict[str, Any]:
        """Check Legal Entity Identifier registry"""
        print(f"🏢 Checking LEI Registry: {entity_name}")
        
        result = {
            "source": "LEI Registry",
            "entity": entity_name,
            "status": "checked",
            "matches": 0,
            "results": [],
            "error": None
        }
        
        try:
            params = {"name": entity_name}
            
            response = self.session.get(
                "https://api.lei-lookup.com/api/v2/lei/search",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                entities = data.get("data", [])
                result["matches"] = len(entities)
                result["results"] = entities[:3]  # First 3 matches
                
                if result["matches"] > 0:
                    print(f"   ✅ LEI FOUND: {result['matches']} matches")
                    for entity in result["results"]:
                        lei_code = entity.get("lei", "Unknown LEI")
                        entity_name = entity.get("entity_name", "Unknown entity")
                        print(f"      • {entity_name} - LEI: {lei_code}")
                else:
                    print(f"   ➖ NOT FOUND: No LEI registry matches")
            else:
                result["error"] = f"HTTP {response.status_code}"
                print(f"   ❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            result["error"] = str(e)
            print(f"   ❌ ERROR: {e}")
        
        return result

    def validate_opencorporates_basic(self, entity_name: str) -> Dict[str, Any]:
        """Basic OpenCorporates validation (no API key required)"""
        print(f"🏢 Checking OpenCorporates: {entity_name}")
        
        result = {
            "source": "OpenCorporates Basic",
            "entity": entity_name,
            "status": "checked",
            "matches": 0,
            "results": [],
            "error": None
        }
        
        try:
            params = {"q": entity_name}
            
            response = self.session.get(
                "https://api.opencorporates.com/v0.4/companies/search",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                companies = data.get("results", {}).get("companies", [])
                result["matches"] = len(companies)
                result["results"] = companies[:3]  # First 3 matches
                
                if result["matches"] > 0:
                    print(f"   ✅ CORPORATE RECORDS: {result['matches']} matches")
                    for company in result["results"]:
                        comp_data = company.get("company", {})
                        name = comp_data.get("name", "Unknown")
                        jurisdiction = comp_data.get("jurisdiction_code", "Unknown")
                        print(f"      • {name} - {jurisdiction}")
                else:
                    print(f"   ➖ NOT FOUND: No corporate registry matches")
            elif response.status_code == 429:
                result["error"] = "Rate limited - try again later"
                print(f"   ⚠️  RATE LIMITED: Try again later")
            else:
                result["error"] = f"HTTP {response.status_code}"
                print(f"   ❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            result["error"] = str(e)
            print(f"   ❌ ERROR: {e}")
        
        return result

    def search_internal_data(self, entity_name: str) -> Dict[str, Any]:
        """Search internal FIELD data for entity"""
        print(f"📊 Checking Internal FIELD Data: {entity_name}")
        
        result = {
            "source": "FIELD Internal Data",
            "entity": entity_name,
            "status": "checked",
            "findings": [],
            "error": None
        }
        
        try:
            # Check comprehensive financial manifest
            financial_manifest_path = self.field_root / "▼TATA" / "comprehensive_financial_manifest.json"
            if financial_manifest_path.exists():
                with open(financial_manifest_path, 'r') as f:
                    financial_data = json.load(f)
                    
                # Search for entity in financial data
                financial_text = json.dumps(financial_data, default=str).upper()
                if entity_name.upper() in financial_text:
                    result["findings"].append("Found in comprehensive financial manifest")
            
            # Check investigation results
            investigation_path = self.field_root / "investigation_results"
            if investigation_path.exists():
                for investigation_dir in investigation_path.iterdir():
                    if investigation_dir.is_dir():
                        results_file = investigation_dir / "investigation_results.json"
                        if results_file.exists():
                            with open(results_file, 'r') as f:
                                investigation_data = json.load(f)
                                entities_analyzed = investigation_data.get("entities_analyzed", [])
                                if entity_name in entities_analyzed:
                                    result["findings"].append(f"Found in investigation results: {investigation_dir.name}")
            
            # Check master account list
            account_list_path = self.field_root / "▼TATA" / "R11_master_account_list_20250421.json"
            if account_list_path.exists():
                with open(account_list_path, 'r') as f:
                    account_data = json.load(f)
                    account_text = json.dumps(account_data, default=str).upper()
                    if entity_name.upper() in account_text:
                        result["findings"].append("Found in master account list")
            
            if result["findings"]:
                print(f"   ✅ INTERNAL DATA: Found in {len(result['findings'])} sources")
                for finding in result["findings"]:
                    print(f"      • {finding}")
            else:
                print(f"   ➖ NOT FOUND: No internal data matches")
                
        except Exception as e:
            result["error"] = str(e)
            print(f"   ❌ ERROR: {e}")
        
        return result

    def comprehensive_entity_validation(self, entity_name: str) -> Dict[str, Any]:
        """Perform comprehensive validation for single entity"""
        print(f"\n{'='*60}")
        print(f"🎯 VALIDATING: {entity_name}")
        print(f"{'='*60}")
        
        entity_result = {
            "entity": entity_name,
            "timestamp": datetime.now().isoformat(),
            "external_sources": {},
            "internal_data": {},
            "risk_assessment": {
                "sanctions_risk": "CLEAR",
                "debarment_risk": "CLEAR",
                "overall_risk": "LOW",
                "risk_factors": []
            }
        }
        
        # External source validations
        entity_result["external_sources"]["ofac_sanctions"] = self.validate_sanctions_ofac(entity_name)
        time.sleep(1)  # Rate limiting
        
        entity_result["external_sources"]["world_bank"] = self.validate_world_bank_debarment(entity_name)
        time.sleep(1)
        
        entity_result["external_sources"]["lei_registry"] = self.validate_lei_registry(entity_name)
        time.sleep(1)
        
        entity_result["external_sources"]["opencorporates"] = self.validate_opencorporates_basic(entity_name)
        time.sleep(2)  # Longer delay for rate limiting
        
        # Internal data search
        entity_result["internal_data"] = self.search_internal_data(entity_name)
        
        # Risk assessment
        risk_factors = []
        
        # Check sanctions
        sanctions_matches = entity_result["external_sources"]["ofac_sanctions"].get("matches", 0)
        if sanctions_matches > 0:
            entity_result["risk_assessment"]["sanctions_risk"] = "HIGH"
            entity_result["risk_assessment"]["overall_risk"] = "HIGH"
            risk_factors.append(f"SANCTIONS_MATCH ({sanctions_matches} matches)")
        
        # Check debarment
        debarment_matches = entity_result["external_sources"]["world_bank"].get("matches", 0)
        if debarment_matches > 0:
            entity_result["risk_assessment"]["debarment_risk"] = "MEDIUM"
            if entity_result["risk_assessment"]["overall_risk"] != "HIGH":
                entity_result["risk_assessment"]["overall_risk"] = "MEDIUM"
            risk_factors.append(f"DEBARMENT_RISK ({debarment_matches} matches)")
        
        # Check corporate presence
        corporate_matches = entity_result["external_sources"]["opencorporates"].get("matches", 0)
        lei_matches = entity_result["external_sources"]["lei_registry"].get("matches", 0)
        
        if corporate_matches > 0 or lei_matches > 0:
            risk_factors.append("CORPORATE_PRESENCE")
        
        # Check internal data presence
        internal_findings = len(entity_result["internal_data"].get("findings", []))
        if internal_findings > 0:
            risk_factors.append(f"INTERNAL_DATA_PRESENCE ({internal_findings} sources)")
        
        entity_result["risk_assessment"]["risk_factors"] = risk_factors
        
        # Display risk assessment
        print(f"\n🚨 RISK ASSESSMENT:")
        print(f"   Overall Risk: {entity_result['risk_assessment']['overall_risk']}")
        print(f"   Sanctions Risk: {entity_result['risk_assessment']['sanctions_risk']}")
        print(f"   Debarment Risk: {entity_result['risk_assessment']['debarment_risk']}")
        if risk_factors:
            print(f"   Risk Factors: {', '.join(risk_factors)}")
        
        return entity_result

    def execute_full_validation(self) -> Dict[str, Any]:
        """Execute validation for all investigation entities"""
        self.display_banner()
        
        validation_results = {
            "execution_timestamp": datetime.now().isoformat(),
            "total_entities": len(self.investigation_entities),
            "entity_results": {},
            "summary": {
                "high_risk": [],
                "medium_risk": [],
                "low_risk": [],
                "sanctions_found": [],
                "debarment_found": [],
                "corporate_presence": [],
                "internal_data_matches": []
            }
        }
        
        for i, entity in enumerate(self.investigation_entities, 1):
            print(f"\n[{i}/{len(self.investigation_entities)}] Processing {entity}...")
            
            # Validate entity
            entity_result = self.comprehensive_entity_validation(entity)
            validation_results["entity_results"][entity] = entity_result
            
            # Update summary
            overall_risk = entity_result["risk_assessment"]["overall_risk"]
            if overall_risk == "HIGH":
                validation_results["summary"]["high_risk"].append(entity)
            elif overall_risk == "MEDIUM":
                validation_results["summary"]["medium_risk"].append(entity)
            else:
                validation_results["summary"]["low_risk"].append(entity)
            
            # Track specific findings
            if entity_result["external_sources"]["ofac_sanctions"].get("matches", 0) > 0:
                validation_results["summary"]["sanctions_found"].append(entity)
                
            if entity_result["external_sources"]["world_bank"].get("matches", 0) > 0:
                validation_results["summary"]["debarment_found"].append(entity)
                
            if (entity_result["external_sources"]["opencorporates"].get("matches", 0) > 0 or
                entity_result["external_sources"]["lei_registry"].get("matches", 0) > 0):
                validation_results["summary"]["corporate_presence"].append(entity)
                
            if entity_result["internal_data"].get("findings"):
                validation_results["summary"]["internal_data_matches"].append(entity)
        
        return validation_results

    def display_summary(self, results: Dict[str, Any]):
        """Display validation summary"""
        print("\n" + "="*80)
        print("📊 EXTERNAL VALIDATION SUMMARY")
        print("="*80)
        
        summary = results["summary"]
        
        print(f"🎯 TOTAL ENTITIES PROCESSED: {results['total_entities']}")
        print()
        
        print("🚨 RISK CATEGORIZATION:")
        if summary["high_risk"]:
            print(f"   🔴 HIGH RISK: {', '.join(summary['high_risk'])}")
        if summary["medium_risk"]:
            print(f"   🟡 MEDIUM RISK: {', '.join(summary['medium_risk'])}")
        if summary["low_risk"]:
            print(f"   🟢 LOW RISK: {', '.join(summary['low_risk'])}")
        print()
        
        print("🎯 SPECIFIC FINDINGS:")
        if summary["sanctions_found"]:
            print(f"   ⚠️  SANCTIONS MATCHES: {', '.join(summary['sanctions_found'])}")
        else:
            print(f"   ✅ SANCTIONS: All entities clear")
            
        if summary["debarment_found"]:
            print(f"   ⚠️  DEBARMENT MATCHES: {', '.join(summary['debarment_found'])}")
        else:
            print(f"   ✅ DEBARMENT: All entities clear")
            
        if summary["corporate_presence"]:
            print(f"   🏢 CORPORATE PRESENCE: {', '.join(summary['corporate_presence'])}")
            
        if summary["internal_data_matches"]:
            print(f"   📊 INTERNAL DATA MATCHES: {', '.join(summary['internal_data_matches'])}")
        print()

    def save_results(self, results: Dict[str, Any]) -> Path:
        """Save validation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.results_dir / f"manual_external_validation_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        return results_file

    def run_validation(self):
        """Run complete validation process"""
        # Execute validation
        results = self.execute_full_validation()
        
        # Display summary
        self.display_summary(results)
        
        # Save results
        results_file = self.save_results(results)
        
        print("💾 RESULTS SAVED:")
        print(f"   📄 File: {results_file}")
        print(f"   📊 Directory: {self.results_dir}")
        print()
        
        print("🔗 31-TASK INTEGRATION:")
        print("   • Tasks 1-10: Use risk assessments for entity verification")
        print("   • Tasks 11-20: Apply external findings to pattern analysis")
        print("   • Tasks 21-30: Leverage compliance data for risk assessment")
        print("   • Task 31: Include external validation in final evidence package")
        print()
        
        print("✅ MANUAL EXTERNAL VALIDATION COMPLETED")

def main():
    """Main execution"""
    validator = ManualExternalValidation()
    validator.run_validation()

if __name__ == "__main__":
    main()