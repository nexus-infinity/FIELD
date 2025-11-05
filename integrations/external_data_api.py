#!/usr/bin/env python3
"""
External Data Sources API Integration
FastAPI integration for external data validation within DOJO system
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
from datetime import datetime
from pathlib import Path

from external_data_manager import ExternalDataManager

app = FastAPI(
    title="External Data Sources API",
    description="Comprehensive external data validation and comparison API",
    version="1.0.0"
)

# Pydantic models for request/response
class EntityValidationRequest(BaseModel):
    entity_name: str
    sources: Optional[List[str]] = None
    compare_internal: bool = True

class BatchValidationRequest(BaseModel):
    entities: List[str]
    sources: Optional[List[str]] = None
    compare_internal: bool = True

class ValidationResponse(BaseModel):
    entity: str
    timestamp: str
    sources_checked: List[str]
    compliance_status: str
    risk_indicators: List[str]
    confidence_score: float

# Global manager instance
data_manager = ExternalDataManager()

@app.get("/")
async def root():
    """API status and information"""
    return {
        "service": "External Data Sources API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "available_sources": list(data_manager.data_sources.keys()),
        "endpoints": [
            "/validate/{entity_name}",
            "/batch-validate",
            "/sources/status",
            "/investigation/validate",
            "/compare/{entity_name}"
        ]
    }

@app.get("/sources/status")
async def get_sources_status():
    """Get status of all external data sources"""
    return data_manager.get_data_sources_status()

@app.get("/validate/{entity_name}")
async def validate_entity(entity_name: str, compare_internal: bool = True):
    """Validate single entity against external data sources"""
    try:
        # Perform external validation
        external_results = await data_manager.comprehensive_entity_search(entity_name)
        
        if compare_internal:
            # Compare with internal data
            comparison_results = data_manager.compare_with_internal_data(
                entity_name, external_results
            )
            return {
                "validation_results": external_results,
                "comparison_results": comparison_results,
                "status": "success"
            }
        else:
            return {
                "validation_results": external_results,
                "status": "success"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")

@app.post("/batch-validate")
async def batch_validate_entities(request: BatchValidationRequest):
    """Validate multiple entities in batch"""
    try:
        batch_results = await data_manager.batch_entity_validation(request.entities)
        
        if request.compare_internal:
            # Add internal data comparison for each entity
            for entity_name, entity_results in batch_results["results"].items():
                if "error" not in entity_results:
                    comparison = data_manager.compare_with_internal_data(
                        entity_name, entity_results
                    )
                    batch_results["results"][entity_name]["comparison"] = comparison
        
        return {
            "batch_results": batch_results,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch validation error: {str(e)}")

@app.get("/investigation/validate")
async def validate_investigation_entities():
    """Validate all key investigation entities"""
    try:
        entities = ["CENTOSA SA", "PASCALI TRUST", "Jacques Rich", "Adam Rich", "David Rich", "BERJAK NOMINEES"]
        batch_results = await data_manager.batch_entity_validation(entities)
        
        # Add internal data comparison for each entity
        for entity_name, entity_results in batch_results["results"].items():
            if "error" not in entity_results:
                comparison = data_manager.compare_with_internal_data(
                    entity_name, entity_results
                )
                batch_results["results"][entity_name]["comparison"] = comparison
        
        # Save results for investigation
        results_path = data_manager.save_validation_results(
            batch_results, 
            f"investigation_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        return {
            "investigation_results": batch_results,
            "results_saved_to": str(results_path),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Investigation validation error: {str(e)}")

@app.get("/compare/{entity_name}")
async def compare_internal_external(entity_name: str):
    """Compare entity data between internal and external sources"""
    try:
        # First get external data
        external_results = await data_manager.comprehensive_entity_search(entity_name)
        
        # Then compare with internal data
        comparison_results = data_manager.compare_with_internal_data(
            entity_name, external_results
        )
        
        return {
            "comparison_results": comparison_results,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")

@app.get("/sources/{source_name}/test")
async def test_data_source(source_name: str):
    """Test connectivity to specific external data source"""
    if source_name not in data_manager.data_sources:
        raise HTTPException(status_code=404, detail=f"Data source '{source_name}' not found")
    
    try:
        # Test with a simple query
        test_entity = "test"
        
        if source_name == "icij":
            result = await data_manager.search_icij_databases(test_entity)
        elif source_name == "opencorporates":
            result = await data_manager.search_opencorporates(test_entity)
        elif source_name == "sanctions":
            result = await data_manager.check_global_sanctions(test_entity)
        elif source_name == "lei":
            result = await data_manager.search_lei_registry(test_entity)
        elif source_name == "world_bank":
            result = await data_manager.check_world_bank_debarment(test_entity)
        else:
            raise HTTPException(status_code=400, detail=f"Test not implemented for '{source_name}'")
        
        return {
            "source": source_name,
            "test_results": result,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test error for {source_name}: {str(e)}")

@app.get("/analysis/risk-summary")
async def get_risk_summary():
    """Get risk summary across all known entities"""
    try:
        # Get entities from internal data
        field_root = Path("/Users/jbear/FIELD")
        entities = []
        
        # Extract entities from investigation results
        investigation_path = field_root / "investigation_results"
        if investigation_path.exists():
            for investigation_dir in investigation_path.iterdir():
                if investigation_dir.is_dir():
                    results_file = investigation_dir / "investigation_results.json"
                    if results_file.exists():
                        with open(results_file, 'r') as f:
                            investigation_data = json.load(f)
                            entities.extend(investigation_data.get("entities_analyzed", []))
        
        # Remove duplicates
        entities = list(set(entities))
        
        if not entities:
            entities = ["CENTOSA SA", "PASCALI TRUST", "Jacques Rich", "Adam Rich", "David Rich", "BERJAK NOMINEES"]
        
        # Validate all entities
        batch_results = await data_manager.batch_entity_validation(entities)
        
        # Create risk summary
        risk_summary = {
            "timestamp": datetime.now().isoformat(),
            "total_entities": len(entities),
            "risk_breakdown": batch_results["summary"],
            "high_risk_details": [],
            "recommendations": []
        }
        
        # Add details for high-risk entities
        for entity in batch_results["summary"]["high_risk"]:
            entity_data = batch_results["results"][entity]
            risk_summary["high_risk_details"].append({
                "entity": entity,
                "risk_indicators": entity_data.get("risk_indicators", []),
                "compliance_status": entity_data.get("compliance_status", "UNKNOWN")
            })
        
        # Generate recommendations
        if batch_results["summary"]["high_risk"]:
            risk_summary["recommendations"].append("IMMEDIATE_REVIEW_REQUIRED: High-risk entities found")
        
        if batch_results["summary"]["medium_risk"]:
            risk_summary["recommendations"].append("ENHANCED_MONITORING: Medium-risk entities require attention")
        
        return {
            "risk_summary": risk_summary,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk summary error: {str(e)}")

@app.get("/reports/compliance")
async def generate_compliance_report():
    """Generate comprehensive compliance report"""
    try:
        entities = ["CENTOSA SA", "PASCALI TRUST", "Jacques Rich", "Adam Rich", "David Rich", "BERJAK NOMINEES"]
        batch_results = await data_manager.batch_entity_validation(entities)
        
        # Generate compliance report
        compliance_report = {
            "report_date": datetime.now().isoformat(),
            "entities_reviewed": len(entities),
            "compliance_overview": {
                "clear": len(batch_results["summary"]["clear"]),
                "low_risk": len(batch_results["summary"]["low_risk"]),
                "medium_risk": len(batch_results["summary"]["medium_risk"]),
                "high_risk": len(batch_results["summary"]["high_risk"])
            },
            "detailed_findings": {},
            "recommendations": [],
            "next_review_date": None
        }
        
        # Add detailed findings
        for entity, results in batch_results["results"].items():
            compliance_report["detailed_findings"][entity] = {
                "compliance_status": results.get("compliance_status", "UNKNOWN"),
                "risk_indicators": results.get("risk_indicators", []),
                "sources_checked": results.get("sources_checked", []),
                "confidence_score": results.get("confidence_score", 0.0)
            }
        
        # Generate recommendations
        if compliance_report["compliance_overview"]["high_risk"] > 0:
            compliance_report["recommendations"].append("Immediate compliance review required for high-risk entities")
        
        if compliance_report["compliance_overview"]["medium_risk"] > 0:
            compliance_report["recommendations"].append("Enhanced due diligence recommended for medium-risk entities")
        
        # Save report
        report_path = data_manager.save_validation_results(
            compliance_report,
            f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        return {
            "compliance_report": compliance_report,
            "report_saved_to": str(report_path),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance report error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🌐 Starting External Data Sources API on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)