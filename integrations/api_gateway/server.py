#!/usr/bin/env python3
"""
Dojo System API Gateway
Central hub for all Dojo component integrations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import json
from datetime import datetime

app = FastAPI(
    title="Dojo System API Gateway",
    description="Central API for Dojo investigation platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dojo component endpoints
@app.get("/")
async def root():
    return {
        "service": "Dojo System API Gateway",
        "version": "1.0.0",
        "components": ["money-hub", "discovery", "evidence", "warp", "geometry"],
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/money-hub/status")
async def money_hub_status():
    return {
        "component": "money-hub",
        "operations": ["institutions", "accounts", "claims", "tasks", "documents", "interactions"],
        "status": "active"
    }

@app.get("/discovery/links")
async def discovery_links():
    return {
        "component": "discovery-links", 
        "operations": ["intake", "sovereign_reconciliation"],
        "status": "monitoring"
    }

@app.get("/evidence/bundles")
async def evidence_bundles():
    return {
        "component": "evidence-principles",
        "operations": ["export_bundles", "chain_of_custody"],
        "status": "ready"
    }

@app.post("/datashare/search")
async def datashare_search(query: dict):
    """Proxy search requests to Datashare"""
    try:
        response = requests.post(
            "http://localhost:9630/api/index/search/local-datashare",
            json=query
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
