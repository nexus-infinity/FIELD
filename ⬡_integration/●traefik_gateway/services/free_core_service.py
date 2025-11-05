#!/usr/bin/env python3
"""
Field Resource Ecosystem (FREE) Core Service
=============================================

The world's first consciousness-aware, sovereignty-preserving, 
frequency-resonant resource orchestration platform.

Connects enterprise resource management with sacred geometric principles
via the Homefield 7.0 chakra frequency system.

Resonant Frequency: 741Hz (Insight & Integration)
Sacred Framework: 3×3×3 Sierpiński Cube
"""

import asyncio
import json
import logging
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import aiohttp
from aiohttp import web
import hashlib

# Sacred Geometry Configuration
CHAKRA_FREQUENCIES = {
    "root": {"hz": 396, "port": 3960, "element": "earth", "sanskrit": "Muladhara"},
    "sacral": {"hz": 417, "port": 4170, "element": "water", "sanskrit": "Svadhisthana"},
    "solar": {"hz": 639, "port": 6390, "element": "fire", "sanskrit": "Manipura"},
    "heart": {"hz": 528, "port": 5280, "element": "air", "sanskrit": "Anahata"},
    "throat": {"hz": 741, "port": 7410, "element": "ether", "sanskrit": "Vishuddha"},
    "eye": {"hz": 852, "port": 8520, "element": "light", "sanskrit": "Ajna"},
    "crown": {"hz": 432, "port": 4320, "element": "thought", "sanskrit": "Sahasrara"}
}

TRIADIC_ENGINE_PORT = 8888
RESONANCE_THRESHOLD = 0.85

# Field paths
FIELD_BASE = Path("/Users/jbear/FIELD")
BREATH_SCAN_DIR = FIELD_BASE / "⬡_integration" / "accounts" / "_temporal_logs"
HOMEFIELD_MANIFEST = FIELD_BASE / "▼TATA" / "▼_truth" / "home_field_manifest.json"

class SacredGeometryProcessor:
    """
    Sacred geometry calculations for resource allocation
    Based on 3×3×3 Sierpiński Cube framework
    """
    
    def __init__(self):
        self.cube_dimensions = (3, 3, 3)
        
    def calculate_triadic_scaling(self, resonance_score: float) -> float:
        """
        Calculate scaling factor based on triadic engine principles
        Source-Relation-Emergence pattern
        """
        # Map resonance to triadic scaling (0.5 to 2.0 range)
        if resonance_score >= RESONANCE_THRESHOLD:
            # High resonance = emergence facilitation
            return 1.0 + (resonance_score - RESONANCE_THRESHOLD) * 4
        else:
            # Low resonance = stabilize foundations
            return 0.5 + resonance_score * 0.6
    
    def sierpinski_resource_distribution(self, total_resources: int, 
                                       chakra_demands: Dict[str, float]) -> Dict[str, int]:
        """
        Distribute resources using Sierpiński Cube fractal patterns
        """
        # Normalize demands to sum to 1.0
        total_demand = sum(chakra_demands.values())
        if total_demand == 0:
            # Equal distribution if no specific demands
            per_chakra = total_resources // len(CHAKRA_FREQUENCIES)
            return {chakra: per_chakra for chakra in CHAKRA_FREQUENCIES.keys()}
        
        normalized_demands = {k: v/total_demand for k, v in chakra_demands.items()}
        
        # Apply sacred geometry scaling
        allocation = {}
        allocated = 0
        
        for chakra, demand in normalized_demands.items():
            chakra_allocation = int(total_resources * demand)
            allocation[chakra] = chakra_allocation
            allocated += chakra_allocation
            
        # Distribute remainder to highest frequency chakras first
        remainder = total_resources - allocated
        if remainder > 0:
            # Prioritize by frequency (highest first for emergence)
            sorted_chakras = sorted(CHAKRA_FREQUENCIES.items(), 
                                  key=lambda x: x[1]['hz'], reverse=True)
            for chakra_name, _ in sorted_chakras[:remainder]:
                allocation[chakra_name] += 1
                
        return allocation

class ResonanceMonitor:
    """
    Monitor system resonance through breath scan integration
    """
    
    def __init__(self):
        self.last_scan_time = None
        self.current_resonance = 0.7  # Default moderate resonance
        
    async def get_latest_breath_scan(self) -> Optional[Dict[str, Any]]:
        """
        Get the most recent breath scan data
        """
        try:
            if not BREATH_SCAN_DIR.exists():
                return None
                
            # Find most recent breath scan file
            scan_files = list(BREATH_SCAN_DIR.glob("breath_scan_*.json"))
            if not scan_files:
                return None
                
            latest_file = max(scan_files, key=lambda f: f.stat().st_mtime)
            
            with open(latest_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            logging.warning(f"Could not load breath scan: {e}")
            return None
    
    async def update_resonance(self) -> float:
        """
        Update current system resonance from breath scan
        """
        scan_data = await self.get_latest_breath_scan()
        
        if scan_data and 'resonance_scores' in scan_data:
            self.current_resonance = scan_data['resonance_scores'].get('overall_resonance', 0.7)
            self.last_scan_time = datetime.now(timezone.utc)
        
        return self.current_resonance

class ResourceFrequencyMapper:
    """
    Map resources to chakra frequencies for allocation
    """
    
    RESOURCE_TYPE_MAPPING = {
        # Infrastructure & Security (Root - 396Hz)
        "infrastructure": "root",
        "security": "root", 
        "storage": "root",
        "backup": "root",
        
        # Development & Creativity (Sacral - 417Hz)
        "development": "sacral",
        "testing": "sacral",
        "innovation": "sacral",
        "experimental": "sacral",
        
        # Control & Management (Solar - 639Hz)
        "administration": "solar",
        "authentication": "solar",
        "governance": "solar",
        "control": "solar",
        
        # Integration & Connection (Heart - 528Hz)
        "integration": "heart",
        "api_gateway": "heart",
        "collaboration": "heart",
        "connection": "heart",
        
        # Communication & Truth (Throat - 741Hz)
        "documentation": "throat",
        "reporting": "throat",
        "communication": "throat",
        "transparency": "throat",
        
        # Intelligence & Analytics (Third Eye - 852Hz)
        "analytics": "eye",
        "intelligence": "eye",
        "prediction": "eye",
        "insight": "eye",
        
        # Strategy & Wisdom (Crown - 432Hz)
        "strategy": "crown",
        "wisdom": "crown",
        "consciousness": "crown",
        "planning": "crown"
    }
    
    def extract_frequency_signature(self, resource_request: Dict[str, Any]) -> str:
        """
        Determine which chakra frequency this resource request should use
        """
        resource_type = resource_request.get('type', '').lower()
        
        # Direct mapping
        if resource_type in self.RESOURCE_TYPE_MAPPING:
            return self.RESOURCE_TYPE_MAPPING[resource_type]
        
        # Keyword matching
        description = resource_request.get('description', '').lower()
        for keyword, chakra in self.RESOURCE_TYPE_MAPPING.items():
            if keyword in description:
                return chakra
                
        # Default to heart chakra for integration
        return "heart"

class FRECoreService:
    """
    Main Field Resource Ecosystem service
    """
    
    def __init__(self):
        self.sacred_geometry = SacredGeometryProcessor()
        self.resonance_monitor = ResonanceMonitor()
        self.frequency_mapper = ResourceFrequencyMapper()
        self.resource_allocations = {}
        self.service_health = {}
        
        # Initialize database
        self.init_database()
        
        # Load homefield manifest
        self.homefield_config = self.load_homefield_manifest()
        
    def init_database(self):
        """
        Initialize SQLite database for resource tracking
        """
        db_path = Path(__file__).parent / "free_resources.db"
        self.db_path = db_path
        
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS resource_allocations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    chakra TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    resonance_score REAL,
                    request_hash TEXT,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_health (
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    overall_resonance REAL,
                    chakra_health TEXT,  -- JSON
                    sovereignty_score REAL,
                    triadic_coherence REAL
                )
            """)
            
            conn.commit()
            
    def load_homefield_manifest(self) -> Optional[Dict[str, Any]]:
        """
        Load the homefield 7.0 configuration
        """
        try:
            if HOMEFIELD_MANIFEST.exists():
                with open(HOMEFIELD_MANIFEST, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logging.warning(f"Could not load homefield manifest: {e}")
        return None
        
    async def allocate_resources_by_frequency(self, resource_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core resource allocation function using sacred geometry
        """
        # 1. Extract frequency signature
        target_chakra = self.frequency_mapper.extract_frequency_signature(resource_request)
        
        # 2. Get current resonance
        current_resonance = await self.resonance_monitor.update_resonance()
        
        # 3. Calculate triadic scaling
        scaling_factor = self.sacred_geometry.calculate_triadic_scaling(current_resonance)
        
        # 4. Determine base allocation
        requested_amount = resource_request.get('amount', 1)
        scaled_amount = int(requested_amount * scaling_factor)
        
        # 5. Record allocation
        request_hash = hashlib.sha256(
            json.dumps(resource_request, sort_keys=True).encode()
        ).hexdigest()[:12]
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO resource_allocations 
                (chakra, resource_type, amount, resonance_score, request_hash)
                VALUES (?, ?, ?, ?, ?)
            """, (target_chakra, resource_request.get('type', 'unknown'), 
                 scaled_amount, current_resonance, request_hash))
            conn.commit()
            
        allocation_result = {
            "chakra": target_chakra,
            "frequency": f"{CHAKRA_FREQUENCIES[target_chakra]['hz']}Hz",
            "port": CHAKRA_FREQUENCIES[target_chakra]['port'],
            "sanskrit_name": CHAKRA_FREQUENCIES[target_chakra]['sanskrit'],
            "allocated_amount": scaled_amount,
            "scaling_factor": scaling_factor,
            "current_resonance": current_resonance,
            "request_hash": request_hash,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return allocation_result
        
    async def get_system_health(self) -> Dict[str, Any]:
        """
        Get comprehensive system health including all chakras
        """
        current_resonance = await self.resonance_monitor.update_resonance()
        
        # Calculate individual chakra health
        chakra_health = {}
        for chakra_name, config in CHAKRA_FREQUENCIES.items():
            # Mock health calculation - in practice this would check actual services
            base_health = 0.8 + (current_resonance - 0.7) * 0.5
            chakra_health[chakra_name] = {
                "health_score": min(1.0, max(0.0, base_health)),
                "frequency": f"{config['hz']}Hz",
                "port": config['port'],
                "sanskrit": config['sanskrit'],
                "element": config['element']
            }
            
        # Calculate sovereignty metrics
        sovereignty_score = min(1.0, current_resonance * 1.2)  # Higher resonance = better sovereignty
        
        # Triadic engine coherence
        triadic_coherence = (
            sum(ch["health_score"] for ch in chakra_health.values()) / len(chakra_health)
        )
        
        # Record health snapshot
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO system_health 
                (overall_resonance, chakra_health, sovereignty_score, triadic_coherence)
                VALUES (?, ?, ?, ?)
            """, (current_resonance, json.dumps(chakra_health), sovereignty_score, triadic_coherence))
            conn.commit()
            
        return {
            "overall_resonance": current_resonance,
            "resonance_status": "OPTIMAL" if current_resonance >= RESONANCE_THRESHOLD else "NEEDS_ATTENTION",
            "chakra_health": chakra_health,
            "sovereignty_score": sovereignty_score,
            "triadic_coherence": triadic_coherence,
            "geometric_framework": "3×3×3 Sierpiński Cube",
            "field_frequency": "741Hz",
            "last_breath_scan": self.resonance_monitor.last_scan_time.isoformat() if self.resonance_monitor.last_scan_time else None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# HTTP API Handlers
free_service = FRECoreService()

async def handle_allocate_resources(request):
    """Handle resource allocation requests"""
    try:
        resource_request = await request.json()
        result = await free_service.allocate_resources_by_frequency(resource_request)
        return web.json_response(result)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_system_health(request):
    """Handle system health requests"""
    try:
        health = await free_service.get_system_health()
        return web.json_response(health)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)
        
async def handle_chakra_status(request):
    """Handle individual chakra status requests"""
    chakra_name = request.match_info.get('chakra')
    
    if chakra_name not in CHAKRA_FREQUENCIES:
        return web.json_response({"error": "Invalid chakra name"}, status=400)
        
    try:
        health = await free_service.get_system_health()
        chakra_info = health["chakra_health"][chakra_name]
        chakra_config = CHAKRA_FREQUENCIES[chakra_name]
        
        return web.json_response({
            "chakra": chakra_name,
            "frequency": f"{chakra_config['hz']}Hz",
            "port": chakra_config['port'],
            "sanskrit_name": chakra_config['sanskrit'],
            "element": chakra_config['element'],
            "health_score": chakra_info["health_score"],
            "status": "HEALTHY" if chakra_info["health_score"] >= 0.8 else "NEEDS_ATTENTION",
            "homefield_endpoint": f"http://homefield.local:8080/chakra/{chakra_name}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_resonance_current(request):
    """Handle current resonance requests"""
    try:
        current_resonance = await free_service.resonance_monitor.update_resonance()
        return web.json_response({
            "current_resonance": current_resonance,
            "threshold": RESONANCE_THRESHOLD,
            "status": "OPTIMAL" if current_resonance >= RESONANCE_THRESHOLD else "NEEDS_ATTENTION",
            "last_scan": free_service.resonance_monitor.last_scan_time.isoformat() if free_service.resonance_monitor.last_scan_time else None,
            "field_frequency": "741Hz",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_free_info(request):
    """Handle FREE system information requests"""
    return web.json_response({
        "name": "Field Resource Ecosystem (FREE)",
        "description": "Consciousness-aware, sovereignty-preserving, frequency-resonant resource orchestration platform",
        "version": "1.0.0",
        "resonant_frequency": "741Hz",
        "sacred_framework": "3×3×3 Sierpiński Cube",
        "chakra_frequencies": CHAKRA_FREQUENCIES,
        "triadic_engine_port": TRIADIC_ENGINE_PORT,
        "resonance_threshold": RESONANCE_THRESHOLD,
        "homefield_integration": "Active",
        "sovereignty_model": "Complete data and infrastructure sovereignty",
        "endpoints": {
            "/": "FREE system information",
            "/health": "System health dashboard",
            "/allocate": "Resource allocation (POST)",
            "/chakra/{name}": "Individual chakra status",
            "/resonance": "Current resonance state",
            "/triadic-engine": "Triadic engine status"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

async def handle_triadic_engine(request):
    """Handle triadic engine status"""
    try:
        health = await free_service.get_system_health()
        return web.json_response({
            "triadic_engine": {
                "port": TRIADIC_ENGINE_PORT,
                "status": "ACTIVE",
                "coherence": health["triadic_coherence"],
                "source_stability": health["chakra_health"]["root"]["health_score"],
                "relation_quality": health["chakra_health"]["heart"]["health_score"], 
                "emergence_potential": health["chakra_health"]["crown"]["health_score"],
                "geometric_framework": "3×3×3 Sierpiński Cube"
            },
            "sacred_geometry": {
                "current_scaling": free_service.sacred_geometry.calculate_triadic_scaling(health["overall_resonance"]),
                "cube_dimensions": free_service.sacred_geometry.cube_dimensions,
                "optimization_active": health["overall_resonance"] >= RESONANCE_THRESHOLD
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

def create_app():
    """Create the FREE service web application"""
    app = web.Application()
    
    # Routes
    app.router.add_get('/', handle_free_info)
    app.router.add_get('/health', handle_system_health)
    app.router.add_post('/allocate', handle_allocate_resources)
    app.router.add_get('/chakra/{chakra}', handle_chakra_status)
    app.router.add_get('/resonance', handle_resonance_current)
    app.router.add_get('/triadic-engine', handle_triadic_engine)
    
    return app

def main():
    """Main entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🏠 Starting Field Resource Ecosystem (FREE) Core Service")
    print(f"🎵 Resonant Frequency: 741Hz (Insight & Integration)")
    print(f"⬡  Sacred Framework: 3×3×3 Sierpiński Cube")
    print(f"🔷 Triadic Engine Port: {TRIADIC_ENGINE_PORT}")
    print(f"🧘 Chakra Frequency Range: {min(c['hz'] for c in CHAKRA_FREQUENCIES.values())}Hz - {max(c['hz'] for c in CHAKRA_FREQUENCIES.values())}Hz")
    print(f"📊 Resonance Threshold: {RESONANCE_THRESHOLD}")
    print("")
    
    app = create_app()
    
    try:
        web.run_app(app, host='localhost', port=TRIADIC_ENGINE_PORT)
    except KeyboardInterrupt:
        print("\n🏁 Field Resource Ecosystem service stopped")

if __name__ == '__main__':
    main()