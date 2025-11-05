#!/usr/bin/env python3
"""
External Data Sources Integration Manager
Comprehensive external data validation and comparison system for FIELD investigations
"""

import requests
import json
import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path
import os
from typing import Dict, List, Optional, Any

class ExternalDataManager:
    def __init__(self):
        self.field_root = Path("/Users/jbear/FIELD")
        self.results_cache = {}
        self.api_keys = self._load_api_keys()
        
        # External data sources configuration
        self.data_sources = {
            "icij": {
                "name": "ICIJ Offshore Leaks",
                "base_url": "https://offshoreleaks.icij.org/search",
                "databases": ["panama_papers", "paradise_papers", "offshore_leaks", "pandora_papers"],
                "status": "active"
            },
            "opencorporates": {
                "name": "OpenCorporates Global Registry",
                "base_url": "https://api.opencorporates.com/v0.4",
                "api_key_required": True,
                "status": "active"
            },
            "sanctions": {
                "name": "Global Sanctions Lists",
                "sources": {
                    "ofac": "https://api.trade.gov/consolidated_screening_list/search",
                    "eu": "https://webgate.ec.europa.eu/fsd/fsf/public/files/xmlFullSanctionsList/content",
                    "un": "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
                },
                "status": "active"
            },
            "lei": {
                "name": "Legal Entity Identifier (LEI) Registry",
                "base_url": "https://api.lei-lookup.com/api/v2",
                "status": "active"
            },
            "world_bank": {
                "name": "World Bank Debarred Firms",
                "base_url": "https://apigwext.worldbank.org/dvsvc/v1.0",
                "status": "active"
            },
            "company_house": {
                "name": "Companies House (UK)",
                "base_url": "https://api.company-information.service.gov.uk",
                "api_key_required": True,
                "status": "ready"
            },
            "sec_edgar": {
                "name": "SEC EDGAR Database",
                "base_url": "https://data.sec.gov/submissions/CIK",
                "status": "ready"
            },
            "fatf": {
                "name": "FATF High-Risk Jurisdictions",
                "url": "http://www.fatf-gafi.org/countries/",
                "status": "manual"
            }
        }

    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from secure storage"""
        api_keys = {}
        
        # Load from environment variables
        api_keys['opencorporates'] = os.getenv('OPENCORPORATES_API_KEY')
        api_keys['companies_house'] = os.getenv('COMPANIES_HOUSE_API_KEY')
        
        # Load from FIELD credentials vault if available
        creds_path = self.field_root / ".credentials_vault" / "field_api_keys.env"
        if creds_path.exists():
            try:
                with open(creds_path, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            api_keys[key.lower()] = value.strip('"\'')
            except Exception as e:
                print(f"Warning: Could not load API keys from {creds_path}: {e}")
        
        return api_keys

    async def comprehensive_entity_search(self, entity_name: str) -> Dict[str, Any]:
        """Comprehensive search across all external data sources"""
        results = {
            "entity": entity_name,
            "timestamp": datetime.now().isoformat(),
            "sources_checked": [],
            "matches": {},
            "risk_indicators": [],
            "compliance_status": "UNKNOWN",
            "confidence_score": 0.0
        }

        # Define search tasks
        search_tasks = [
            self.search_icij_databases(entity_name),
            self.search_opencorporates(entity_name),
            self.check_global_sanctions(entity_name),
            self.search_lei_registry(entity_name),
            self.check_world_bank_debarment(entity_name)
        ]

        # Execute searches concurrently
        search_results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(search_results):
            source_name = ["icij", "opencorporates", "sanctions", "lei", "world_bank"][i]
            results["sources_checked"].append(source_name)
            
            if isinstance(result, Exception):
                results["matches"][source_name] = {"error": str(result)}
            else:
                results["matches"][source_name] = result

        # Calculate risk and compliance
        results = self._assess_risk_and_compliance(results)
        
        return results

    async def search_icij_databases(self, entity_name: str) -> Dict[str, Any]:
        """Search ICIJ offshore databases"""
        results = {
            "source": "ICIJ Offshore Leaks",
            "databases": {},
            "total_matches": 0,
            "status": "checked"
        }

        databases = ["panama_papers", "paradise_papers", "offshore_leaks", "pandora_papers"]
        
        async with aiohttp.ClientSession() as session:
            for db in databases:
                try:
                    params = {
                        "q": entity_name,
                        "c": db,
                        "e": 1, "a": 1, "o": 1,  # entities, addresses, officers
                        "j": 1  # jurisdictions
                    }
                    
                    async with session.get(
                        "https://offshoreleaks.icij.org/search", 
                        params=params
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            matches = len(data.get("results", []))
                            results["databases"][db] = {
                                "matches": matches,
                                "data": data.get("results", [])[:5]  # First 5 results
                            }
                            results["total_matches"] += matches
                        else:
                            results["databases"][db] = {"error": f"HTTP {response.status}"}
                            
                except Exception as e:
                    results["databases"][db] = {"error": str(e)}

        return results

    async def search_opencorporates(self, entity_name: str) -> Dict[str, Any]:
        """Search OpenCorporates global registry"""
        results = {
            "source": "OpenCorporates Global Registry",
            "matches": 0,
            "companies": [],
            "status": "checked"
        }

        params = {"q": entity_name}
        if self.api_keys.get('opencorporates'):
            params["api_token"] = self.api_keys['opencorporates']

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    "https://api.opencorporates.com/v0.4/companies/search",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        companies = data.get("results", {}).get("companies", [])
                        results["matches"] = len(companies)
                        results["companies"] = companies[:10]  # First 10 results
                    else:
                        results["error"] = f"HTTP {response.status}"
                        
            except Exception as e:
                results["error"] = str(e)

        return results

    async def check_global_sanctions(self, entity_name: str) -> Dict[str, Any]:
        """Check entity against global sanctions lists"""
        results = {
            "source": "Global Sanctions Lists",
            "sanctions_found": False,
            "lists_checked": {},
            "total_matches": 0,
            "status": "checked"
        }

        # OFAC Consolidated Screening List
        async with aiohttp.ClientSession() as session:
            try:
                params = {
                    "q": entity_name,
                    "sources": "SDN,FSE,UVL,ISN,DTC,SSI,PART561,CAP,DPL,EL,UNNT"
                }
                
                async with session.get(
                    "https://api.trade.gov/consolidated_screening_list/search",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        matches = data.get("total", 0)
                        results["lists_checked"]["ofac"] = {
                            "matches": matches,
                            "results": data.get("results", [])[:5]
                        }
                        results["total_matches"] += matches
                        if matches > 0:
                            results["sanctions_found"] = True
                    else:
                        results["lists_checked"]["ofac"] = {"error": f"HTTP {response.status}"}
                        
            except Exception as e:
                results["lists_checked"]["ofac"] = {"error": str(e)}

        return results

    async def search_lei_registry(self, entity_name: str) -> Dict[str, Any]:
        """Search Legal Entity Identifier registry"""
        results = {
            "source": "LEI Registry",
            "matches": 0,
            "entities": [],
            "status": "checked"
        }

        async with aiohttp.ClientSession() as session:
            try:
                params = {"name": entity_name}
                async with session.get(
                    "https://api.lei-lookup.com/api/v2/lei/search",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        entities = data.get("data", [])
                        results["matches"] = len(entities)
                        results["entities"] = entities[:5]
                    else:
                        results["error"] = f"HTTP {response.status}"
                        
            except Exception as e:
                results["error"] = str(e)

        return results

    async def check_world_bank_debarment(self, entity_name: str) -> Dict[str, Any]:
        """Check World Bank debarment list"""
        results = {
            "source": "World Bank Debarred Firms",
            "matches": 0,
            "entities": [],
            "status": "checked"
        }

        async with aiohttp.ClientSession() as session:
            try:
                params = {"format": "json", "os": 0, "size": 50, "qterm": entity_name}
                async with session.get(
                    "https://apigwext.worldbank.org/dvsvc/v1.0/json/APPLICATION/ADOBE_EXPRNCE_MGR/FIRM/SANCTIONED_FIRM",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        firms = data.get("response", {}).get("FIRM", [])
                        results["matches"] = len(firms)
                        results["entities"] = firms[:5]
                    else:
                        results["error"] = f"HTTP {response.status}"
                        
            except Exception as e:
                results["error"] = str(e)

        return results

    def _assess_risk_and_compliance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk level and compliance status based on search results"""
        risk_score = 0.0
        risk_factors = []
        
        # Check sanctions matches
        sanctions_data = results["matches"].get("sanctions", {})
        if sanctions_data.get("sanctions_found"):
            risk_score += 10.0
            risk_factors.append("SANCTIONS_MATCH")
            results["compliance_status"] = "HIGH_RISK"

        # Check ICIJ offshore matches
        icij_data = results["matches"].get("icij", {})
        if icij_data.get("total_matches", 0) > 0:
            risk_score += 5.0
            risk_factors.append("OFFSHORE_PRESENCE")

        # Check debarment
        wb_data = results["matches"].get("world_bank", {})
        if wb_data.get("matches", 0) > 0:
            risk_score += 7.0
            risk_factors.append("WORLD_BANK_DEBARMENT")

        # Set compliance status
        if risk_score >= 10:
            results["compliance_status"] = "HIGH_RISK"
        elif risk_score >= 5:
            results["compliance_status"] = "MEDIUM_RISK"
        elif risk_score > 0:
            results["compliance_status"] = "LOW_RISK"
        else:
            results["compliance_status"] = "CLEAR"

        results["risk_indicators"] = risk_factors
        results["confidence_score"] = min(risk_score / 10.0, 1.0)

        return results

    def compare_with_internal_data(self, entity_name: str, external_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare external data with internal FIELD data"""
        comparison_results = {
            "entity": entity_name,
            "timestamp": datetime.now().isoformat(),
            "internal_data": {},
            "external_data": external_results,
            "correlations": [],
            "discrepancies": [],
            "validation_status": "PENDING"
        }

        # Load internal data
        try:
            # Check comprehensive financial manifest
            financial_manifest_path = self.field_root / "▼TATA" / "comprehensive_financial_manifest.json"
            if financial_manifest_path.exists():
                with open(financial_manifest_path, 'r') as f:
                    financial_data = json.load(f)
                    comparison_results["internal_data"]["financial_manifest"] = financial_data

            # Check investigation results
            investigation_path = self.field_root / "investigation_results"
            if investigation_path.exists():
                for investigation_dir in investigation_path.iterdir():
                    if investigation_dir.is_dir():
                        results_file = investigation_dir / "investigation_results.json"
                        if results_file.exists():
                            with open(results_file, 'r') as f:
                                investigation_data = json.load(f)
                                if entity_name.upper() in str(investigation_data).upper():
                                    comparison_results["internal_data"]["investigation_results"] = investigation_data

            # Perform correlation analysis
            comparison_results = self._analyze_correlations(comparison_results)

        except Exception as e:
            comparison_results["error"] = f"Error loading internal data: {e}"

        return comparison_results

    def _analyze_correlations(self, comparison_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze correlations between internal and external data"""
        correlations = []
        discrepancies = []

        internal_data = comparison_results.get("internal_data", {})
        external_data = comparison_results.get("external_data", {})

        # Check if entity exists in both internal and external data
        if internal_data and external_data.get("matches"):
            correlations.append("ENTITY_FOUND_BOTH_INTERNAL_EXTERNAL")

        # Check risk assessment correlation
        internal_risk = internal_data.get("investigation_results", {}).get("risk_score", {}).get("overall", "UNKNOWN")
        external_risk = external_data.get("compliance_status", "UNKNOWN")
        
        if internal_risk != "UNKNOWN" and external_risk != "UNKNOWN":
            if internal_risk == external_risk:
                correlations.append("RISK_ASSESSMENT_ALIGNED")
            else:
                discrepancies.append(f"RISK_MISMATCH: Internal({internal_risk}) vs External({external_risk})")

        comparison_results["correlations"] = correlations
        comparison_results["discrepancies"] = discrepancies

        # Set validation status
        if discrepancies:
            comparison_results["validation_status"] = "DISCREPANCIES_FOUND"
        elif correlations:
            comparison_results["validation_status"] = "VALIDATED"
        else:
            comparison_results["validation_status"] = "INSUFFICIENT_DATA"

        return comparison_results

    async def batch_entity_validation(self, entities: List[str]) -> Dict[str, Any]:
        """Validate multiple entities against external data sources"""
        batch_results = {
            "timestamp": datetime.now().isoformat(),
            "entities_processed": len(entities),
            "results": {},
            "summary": {
                "high_risk": [],
                "medium_risk": [],
                "low_risk": [],
                "clear": [],
                "errors": []
            }
        }

        # Process entities in batches to avoid rate limiting
        batch_size = 5
        for i in range(0, len(entities), batch_size):
            batch = entities[i:i+batch_size]
            batch_tasks = [self.comprehensive_entity_search(entity) for entity in batch]
            batch_entity_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            for j, result in enumerate(batch_entity_results):
                entity = batch[j]
                if isinstance(result, Exception):
                    batch_results["results"][entity] = {"error": str(result)}
                    batch_results["summary"]["errors"].append(entity)
                else:
                    batch_results["results"][entity] = result
                    
                    # Categorize by risk level
                    compliance_status = result.get("compliance_status", "UNKNOWN")
                    if compliance_status == "HIGH_RISK":
                        batch_results["summary"]["high_risk"].append(entity)
                    elif compliance_status == "MEDIUM_RISK":
                        batch_results["summary"]["medium_risk"].append(entity)
                    elif compliance_status == "LOW_RISK":
                        batch_results["summary"]["low_risk"].append(entity)
                    elif compliance_status == "CLEAR":
                        batch_results["summary"]["clear"].append(entity)

            # Rate limiting delay between batches
            await asyncio.sleep(2)

        return batch_results

    def save_validation_results(self, results: Dict[str, Any], filename: str = None) -> Path:
        """Save validation results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"external_validation_results_{timestamp}.json"

        results_path = self.field_root / "external_validation_results" / filename
        results_path.parent.mkdir(parents=True, exist_ok=True)

        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return results_path

    def get_data_sources_status(self) -> Dict[str, Any]:
        """Get status of all configured external data sources"""
        status_report = {
            "timestamp": datetime.now().isoformat(),
            "sources": {},
            "api_keys_configured": [],
            "ready_sources": [],
            "configuration_needed": []
        }

        for source_id, config in self.data_sources.items():
            status_info = {
                "name": config["name"],
                "status": config["status"],
                "api_key_required": config.get("api_key_required", False),
                "api_key_configured": False
            }

            if config.get("api_key_required"):
                if self.api_keys.get(source_id):
                    status_info["api_key_configured"] = True
                    status_report["api_keys_configured"].append(source_id)
                else:
                    status_report["configuration_needed"].append(source_id)

            if config["status"] == "active":
                status_report["ready_sources"].append(source_id)

            status_report["sources"][source_id] = status_info

        return status_report

# Async wrapper functions for CLI usage
async def validate_entity(entity_name: str) -> Dict[str, Any]:
    """Standalone entity validation function"""
    manager = ExternalDataManager()
    return await manager.comprehensive_entity_search(entity_name)

async def validate_investigation_entities() -> Dict[str, Any]:
    """Validate key investigation entities"""
    entities = ["CENTOSA SA", "PASCALI TRUST", "Jacques Rich", "Adam Rich", "David Rich", "BERJAK NOMINEES"]
    manager = ExternalDataManager()
    return await manager.batch_entity_validation(entities)

def main():
    """CLI interface for external data validation"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python external_data_manager.py <entity_name>")
        print("   or: python external_data_manager.py --validate-investigation")
        print("   or: python external_data_manager.py --status")
        return

    manager = ExternalDataManager()

    if sys.argv[1] == "--status":
        status = manager.get_data_sources_status()
        print(json.dumps(status, indent=2))
    elif sys.argv[1] == "--validate-investigation":
        results = asyncio.run(validate_investigation_entities())
        print(json.dumps(results, indent=2))
        manager.save_validation_results(results)
    else:
        entity_name = " ".join(sys.argv[1:])
        results = asyncio.run(validate_entity(entity_name))
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()