#!/usr/bin/env python3
"""
Full Investigation External Validation Execution
Comprehensive external data validation for all investigation entities
"""

import requests
import json
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class FullExternalValidation:
    def __init__(self):
        self.field_root = Path("/Users/jbear/FIELD")
        self.external_api = "http://localhost:8001"
        self.dojo_api = "http://localhost:8000"
        self.results_dir = self.field_root / "external_validation_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Investigation entities for validation
        self.investigation_entities = [
            "CENTOSA SA",
            "PASCALI TRUST", 
            "Jacques Rich",
            "Adam Rich",
            "David Rich",
            "BERJAK NOMINEES"
        ]
        
        self.validation_results = {}
        self.session = requests.Session()
        self.session.timeout = 30

    def display_banner(self):
        """Display execution banner"""
        print("🌐" + "="*80 + "🌐")
        print("    FULL EXTERNAL VALIDATION EXECUTION")
        print("    Comprehensive Investigation Entity Validation")
        print("    External Data Comparison & Risk Assessment")
        print("🌐" + "="*80 + "🌐")
        print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Entities to Validate: {len(self.investigation_entities)}")
        print()

    def check_system_readiness(self) -> bool:
        """Check if all systems are ready for validation"""
        print("🔍 CHECKING SYSTEM READINESS")
        print("-" * 50)
        
        systems_ready = True
        
        # Check External Data API
        try:
            response = self.session.get(f"{self.external_api}/")
            if response.status_code == 200:
                print("✅ External Data API: READY")
            else:
                print(f"❌ External Data API: HTTP {response.status_code}")
                systems_ready = False
        except Exception as e:
            print(f"❌ External Data API: NOT ACCESSIBLE ({e})")
            systems_ready = False
        
        # Check DOJO API
        try:
            response = self.session.get(f"{self.dojo_api}/")
            if response.status_code == 200:
                print("✅ DOJO API: READY")
            else:
                print(f"❌ DOJO API: HTTP {response.status_code}")
                systems_ready = False
        except Exception as e:
            print(f"❌ DOJO API: NOT ACCESSIBLE ({e})")
            systems_ready = False
            
        # Check External Data Sources
        try:
            response = self.session.get(f"{self.external_api}/sources/status")
            if response.status_code == 200:
                sources_data = response.json()
                ready_sources = len(sources_data.get('ready_sources', []))
                print(f"✅ External Data Sources: {ready_sources} READY")
            else:
                print(f"❌ External Data Sources: HTTP {response.status_code}")
                systems_ready = False
        except Exception as e:
            print(f"❌ External Data Sources: ERROR ({e})")
            systems_ready = False
        
        print()
        return systems_ready

    def validate_single_entity(self, entity_name: str) -> Dict[str, Any]:
        """Validate single entity against external sources"""
        print(f"🔍 Validating: {entity_name}")
        
        validation_result = {
            "entity": entity_name,
            "timestamp": datetime.now().isoformat(),
            "validation_status": "PENDING",
            "external_validation": None,
            "internal_comparison": None,
            "risk_assessment": None,
            "error": None
        }
        
        try:
            # Step 1: External validation
            print(f"   📊 Running external validation...")
            response = self.session.get(f"{self.external_api}/validate/{entity_name}")
            
            if response.status_code == 200:
                external_data = response.json()
                validation_result["external_validation"] = external_data.get("validation_results")
                validation_result["internal_comparison"] = external_data.get("comparison_results")
                print(f"   ✅ External validation completed")
                
                # Extract key information
                if validation_result["external_validation"]:
                    compliance_status = validation_result["external_validation"].get("compliance_status", "UNKNOWN")
                    risk_indicators = validation_result["external_validation"].get("risk_indicators", [])
                    sources_checked = validation_result["external_validation"].get("sources_checked", [])
                    
                    validation_result["risk_assessment"] = {
                        "compliance_status": compliance_status,
                        "risk_indicators": risk_indicators,
                        "sources_checked": sources_checked,
                        "external_matches": self._count_external_matches(validation_result["external_validation"])
                    }
                    
                    print(f"   📋 Compliance Status: {compliance_status}")
                    print(f"   🎯 Risk Indicators: {len(risk_indicators)}")
                    print(f"   🌐 Sources Checked: {len(sources_checked)}")
                    
                validation_result["validation_status"] = "COMPLETED"
                
            else:
                error_msg = f"External validation failed: HTTP {response.status_code}"
                validation_result["error"] = error_msg
                validation_result["validation_status"] = "FAILED"
                print(f"   ❌ {error_msg}")
                
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            validation_result["error"] = error_msg
            validation_result["validation_status"] = "ERROR"
            print(f"   ❌ {error_msg}")
        
        print()
        return validation_result

    def _count_external_matches(self, external_validation: Dict[str, Any]) -> Dict[str, int]:
        """Count matches across external sources"""
        matches = {}
        
        if not external_validation or "matches" not in external_validation:
            return matches
            
        for source, data in external_validation["matches"].items():
            if isinstance(data, dict):
                if source == "icij":
                    matches[source] = data.get("total_matches", 0)
                elif source == "opencorporates":
                    matches[source] = data.get("matches", 0)
                elif source == "sanctions":
                    matches[source] = data.get("total_matches", 0)
                elif source == "lei":
                    matches[source] = data.get("matches", 0)
                elif source == "world_bank":
                    matches[source] = data.get("matches", 0)
                else:
                    matches[source] = 1 if not data.get("error") else 0
        
        return matches

    def execute_comprehensive_validation(self) -> Dict[str, Any]:
        """Execute validation for all investigation entities"""
        print("🚀 EXECUTING COMPREHENSIVE VALIDATION")
        print("-" * 50)
        
        comprehensive_results = {
            "execution_timestamp": datetime.now().isoformat(),
            "total_entities": len(self.investigation_entities),
            "entity_results": {},
            "summary": {
                "completed": 0,
                "failed": 0,
                "high_risk": [],
                "medium_risk": [],
                "low_risk": [],
                "clear": [],
                "external_matches_found": {}
            }
        }
        
        for i, entity in enumerate(self.investigation_entities, 1):
            print(f"[{i}/{len(self.investigation_entities)}] Processing {entity}...")
            
            # Validate entity
            entity_result = self.validate_single_entity(entity)
            comprehensive_results["entity_results"][entity] = entity_result
            
            # Update summary
            if entity_result["validation_status"] == "COMPLETED":
                comprehensive_results["summary"]["completed"] += 1
                
                # Categorize by risk
                if entity_result["risk_assessment"]:
                    compliance_status = entity_result["risk_assessment"]["compliance_status"]
                    if compliance_status == "HIGH_RISK":
                        comprehensive_results["summary"]["high_risk"].append(entity)
                    elif compliance_status == "MEDIUM_RISK":
                        comprehensive_results["summary"]["medium_risk"].append(entity)
                    elif compliance_status == "LOW_RISK":
                        comprehensive_results["summary"]["low_risk"].append(entity)
                    elif compliance_status == "CLEAR":
                        comprehensive_results["summary"]["clear"].append(entity)
                    
                    # Track external matches
                    external_matches = entity_result["risk_assessment"].get("external_matches", {})
                    for source, count in external_matches.items():
                        if count > 0:
                            if source not in comprehensive_results["summary"]["external_matches_found"]:
                                comprehensive_results["summary"]["external_matches_found"][source] = []
                            comprehensive_results["summary"]["external_matches_found"][source].append({
                                "entity": entity,
                                "matches": count
                            })
            else:
                comprehensive_results["summary"]["failed"] += 1
            
            # Brief pause between validations to avoid rate limiting
            time.sleep(2)
        
        return comprehensive_results

    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        print("📋 GENERATING COMPLIANCE REPORT")
        print("-" * 50)
        
        try:
            response = self.session.get(f"{self.external_api}/reports/compliance", timeout=60)
            
            if response.status_code == 200:
                compliance_data = response.json()
                print("✅ Compliance report generated successfully")
                return compliance_data.get("compliance_report", {})
            else:
                print(f"❌ Failed to generate compliance report: HTTP {response.status_code}")
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Compliance report error: {e}")
            return {"error": str(e)}

    def save_results(self, validation_results: Dict[str, Any], compliance_report: Dict[str, Any]):
        """Save validation results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save validation results
        validation_file = self.results_dir / f"full_validation_results_{timestamp}.json"
        with open(validation_file, 'w') as f:
            json.dump(validation_results, f, indent=2, ensure_ascii=False)
        
        # Save compliance report
        compliance_file = self.results_dir / f"compliance_report_{timestamp}.json"
        with open(compliance_file, 'w') as f:
            json.dump(compliance_report, f, indent=2, ensure_ascii=False)
        
        return validation_file, compliance_file

    def display_results_summary(self, results: Dict[str, Any]):
        """Display summary of validation results"""
        print("📊 VALIDATION RESULTS SUMMARY")
        print("=" * 60)
        
        summary = results["summary"]
        
        print(f"🎯 ENTITIES PROCESSED: {results['total_entities']}")
        print(f"✅ COMPLETED: {summary['completed']}")
        print(f"❌ FAILED: {summary['failed']}")
        print()
        
        print("🚨 RISK CATEGORIZATION:")
        if summary["high_risk"]:
            print(f"   🔴 HIGH RISK: {', '.join(summary['high_risk'])}")
        if summary["medium_risk"]:
            print(f"   🟡 MEDIUM RISK: {', '.join(summary['medium_risk'])}")
        if summary["low_risk"]:
            print(f"   🟢 LOW RISK: {', '.join(summary['low_risk'])}")
        if summary["clear"]:
            print(f"   ⚪ CLEAR: {', '.join(summary['clear'])}")
        print()
        
        print("🌐 EXTERNAL MATCHES FOUND:")
        for source, matches in summary.get("external_matches_found", {}).items():
            print(f"   📊 {source.upper()}: {len(matches)} entities with matches")
            for match in matches:
                print(f"      • {match['entity']}: {match['matches']} matches")
        print()

    def display_detailed_findings(self, results: Dict[str, Any]):
        """Display detailed findings for each entity"""
        print("🔍 DETAILED ENTITY FINDINGS")
        print("=" * 60)
        
        for entity, entity_result in results["entity_results"].items():
            print(f"📂 {entity}")
            print("-" * 40)
            
            if entity_result["validation_status"] == "COMPLETED":
                if entity_result["risk_assessment"]:
                    risk_data = entity_result["risk_assessment"]
                    print(f"   Status: {risk_data['compliance_status']}")
                    print(f"   Risk Indicators: {len(risk_data['risk_indicators'])}")
                    print(f"   Sources Checked: {len(risk_data['sources_checked'])}")
                    
                    if risk_data["risk_indicators"]:
                        print(f"   ⚠️  Risk Factors: {', '.join(risk_data['risk_indicators'])}")
                    
                    external_matches = risk_data.get("external_matches", {})
                    if external_matches:
                        print("   🌐 External Matches:")
                        for source, count in external_matches.items():
                            if count > 0:
                                print(f"      • {source}: {count} matches")
                else:
                    print("   Status: Validation completed (no risk data)")
            else:
                print(f"   Status: {entity_result['validation_status']}")
                if entity_result["error"]:
                    print(f"   Error: {entity_result['error']}")
            
            print()

    def run_full_validation(self):
        """Execute complete validation workflow"""
        self.display_banner()
        
        # Check system readiness
        if not self.check_system_readiness():
            print("❌ System not ready for validation. Please check system status.")
            return
        
        print("🚀 STARTING FULL EXTERNAL VALIDATION...")
        print()
        
        # Execute comprehensive validation
        validation_results = self.execute_comprehensive_validation()
        
        # Generate compliance report
        compliance_report = self.generate_compliance_report()
        
        # Save results
        print("\n💾 SAVING RESULTS...")
        validation_file, compliance_file = self.save_results(validation_results, compliance_report)
        print(f"✅ Validation results saved: {validation_file}")
        print(f"✅ Compliance report saved: {compliance_file}")
        print()
        
        # Display results
        self.display_results_summary(validation_results)
        self.display_detailed_findings(validation_results)
        
        # Final status
        print("🎉 FULL EXTERNAL VALIDATION COMPLETED")
        print("=" * 60)
        print(f"📄 Results Directory: {self.results_dir}")
        print(f"📊 Validation File: {validation_file.name}")
        print(f"📋 Compliance Report: {compliance_file.name}")
        print()
        print("🔗 Integration with 31-Task Process:")
        print("   • Use validation results for Tasks 1-10 (Entity Verification)")
        print("   • Apply risk assessments for Tasks 11-20 (Pattern Analysis)")
        print("   • Leverage compliance report for Tasks 21-30 (Risk Assessment)")
        print("   • Combine with evidence bundles for Task 31 (Final Package)")

def main():
    """Main execution"""
    validator = FullExternalValidation()
    validator.run_full_validation()

if __name__ == "__main__":
    main()