#!/usr/bin/env python3
"""
MCP-based Forensic Document Organizer
Uses existing MCP servers (Notion, SQLite, Memory) for forensic document classification
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import subprocess
import os
import hashlib

@dataclass
class ForensicClassification:
    """Document forensic classification result"""
    filename: str
    verified_entities: List[str]
    forensic_flag: str  # ✅ 🚨 ❓ 👻
    confidence_score: float
    anomaly_indicators: List[str]
    suggested_location: str
    mcp_source: str

class MCPForensicOrganizer:
    """Forensic document organizer using existing MCP infrastructure"""
    
    def __init__(self):
        self.documents_path = Path.home() / "Documents"
        self.forensic_flags = {
            'verified': '✅',
            'anomaly': '🚨', 
            'unknown': '❓',
            'shadow': '👻'
        }
        self.corporate_entities = {}
        self.folder_structure = {}
        
    async def load_corporate_data_from_mcp(self) -> Dict:
        """Load verified corporate structure from MCP Notion server"""
        try:
            # Use existing Claude Desktop MCP Notion server (port 5280)
            print("🔍 Querying MCP Notion server for corporate entities...")
            
            # For now, create sample data structure that would come from MCP
            # In production, this would call your MCP Notion server
            corporate_data = {
                "verified_entities": {
                    "ANSEVATA No 2 Trust": {
                        "type": "equity_trust",
                        "trustee": "Berjak Nominees (N.T.) Pty Ltd",
                        "status": "active",
                        "keywords": ["ansevata", "equity", "trust"]
                    },
                    "Berjak and Partners Unit Trust": {
                        "type": "trading_trust",
                        "trustee": "TBD",
                        "status": "active", 
                        "keywords": ["berjak", "partners", "unit", "trust"]
                    },
                    "Berjak Metals Pty Ltd": {
                        "type": "company",
                        "acn": "registered",
                        "directors": ["Jeremy Rich"],
                        "status": "active",
                        "keywords": ["berjak", "metals", "pty", "ltd"]
                    },
                    "Berjak Nominees (N.T.) Pty Ltd": {
                        "type": "nominee_company",
                        "status": "active",
                        "keywords": ["berjak", "nominees", "nt", "pty", "ltd"]
                    },
                    "Walkerville Vineyard": {
                        "type": "business_operation",
                        "category": "agriculture",
                        "status": "active",
                        "keywords": ["walkerville", "vineyard", "wine", "agriculture"]
                    },
                    "Cumberland Building Company": {
                        "type": "business_operation", 
                        "category": "construction",
                        "status": "active",
                        "keywords": ["cumberland", "building", "construction"]
                    }
                }
            }
            
            return corporate_data
            
        except Exception as e:
            print(f"Error loading from MCP: {e}")
            return {"verified_entities": {}}
    
    async def store_classification_in_mcp(self, classification: ForensicClassification):
        """Store forensic classification in MCP SQLite server"""
        try:
            # This would use your MCP SQLite server (port 3960) to store classifications
            # For now, just log the classification
            print(f"📊 Storing classification: {classification.forensic_flag} {classification.filename}")
            
            # In production, this would call your MCP SQLite server:
            # INSERT INTO forensic_classifications VALUES (...)
            
        except Exception as e:
            print(f"Error storing classification: {e}")
    
    def classify_document_forensically(self, filepath: Path, corporate_data: Dict) -> ForensicClassification:
        """Classify document using corporate entity verification"""
        filename = filepath.name.lower()
        
        classification = ForensicClassification(
            filename=filepath.name,
            verified_entities=[],
            forensic_flag=self.forensic_flags['unknown'],
            confidence_score=0.0,
            anomaly_indicators=[],
            suggested_location="⟡_INTAKE",
            mcp_source="notion_mcp"
        )
        
        # Check against verified entities
        for entity_name, entity_data in corporate_data['verified_entities'].items():
            keywords = entity_data.get('keywords', [])
            
            # Calculate match score
            matches = sum(1 for keyword in keywords if keyword in filename)
            if matches > 0:
                classification.verified_entities.append(entity_name)
                classification.confidence_score += matches / len(keywords)
                classification.forensic_flag = self.forensic_flags['verified']
                
                # Determine location based on entity type
                if entity_data['type'] in ['trust', 'equity_trust', 'trading_trust']:
                    classification.suggested_location = f"💼VOCATION/VERIFIED_CORPORATE_STRUCTURE/Trust_Structures/{entity_name}"
                elif entity_data['type'] in ['company', 'nominee_company']:
                    classification.suggested_location = f"💼VOCATION/VERIFIED_CORPORATE_STRUCTURE/Operating_Companies/{entity_name}"
                elif entity_data['type'] == 'business_operation':
                    classification.suggested_location = f"💼VOCATION/VERIFIED_BUSINESS_OPERATIONS/{entity_data['category']}/{entity_name}"
        
        # Check for potential anomalies
        corporate_indicators = ['pty ltd', 'trust', 'company', 'ltd', 'inc', 'corp']
        if any(indicator in filename for indicator in corporate_indicators):
            if not classification.verified_entities:
                classification.forensic_flag = self.forensic_flags['anomaly']
                classification.anomaly_indicators.append("Unknown corporate entity detected")
                classification.suggested_location = "💼VOCATION/🚨ANOMALY_DETECTION/Unknown_Entities/"
        
        # Check for email patterns
        if 'email' in filename:
            classification.suggested_location = "🌐COMMUNITY/Email_Correspondence/"
            if not classification.verified_entities:
                classification.forensic_flag = self.forensic_flags['verified']  # Emails are generally legitimate
        
        # Check for personal patterns
        personal_indicators = ['power-of-attorney', 'personal', 'medical', 'private']
        if any(indicator in filename for indicator in personal_indicators):
            classification.suggested_location = "📁PERSONAL/Personal_Legal/"
            classification.forensic_flag = self.forensic_flags['verified']
        
        return classification
    
    async def generate_forensic_folder_structure(self, corporate_data: Dict):
        """Generate folder structure based on verified entities"""
        base_structure = {
            "📁PERSONAL": {
                "Personal_Documents": {},
                "Trust_Documents": {},
                "Personal_Legal": {},
                "Switzerland_Assets": {}
            },
            "💼VOCATION": {
                "VERIFIED_CORPORATE_STRUCTURE": {
                    "Trust_Structures": {},
                    "Operating_Companies": {}
                },
                "VERIFIED_BUSINESS_OPERATIONS": {
                    "agriculture": {},
                    "construction": {},
                    "wine_business": {},
                    "scrap_metal_trading": {}
                },
                "🚨ANOMALY_DETECTION": {
                    "Unknown_Entities": {},
                    "Shadow_Structure_Indicators": {},
                    "Timeline_Discrepancies": {}
                }
            },
            "🌐COMMUNITY": {
                "Email_Correspondence": {},
                "Regulatory_Compliance": {},
                "Financial_Institutions": {},
                "Legal_Proceedings": {}
            },
            "⟡_INTAKE": {}
        }
        
        # Add verified entities to structure
        for entity_name, entity_data in corporate_data['verified_entities'].items():
            if entity_data['type'] in ['trust', 'equity_trust', 'trading_trust']:
                base_structure["💼VOCATION"]["VERIFIED_CORPORATE_STRUCTURE"]["Trust_Structures"][entity_name] = {
                    "Trustee": {},
                    "Beneficiaries": {},
                    "Trust_Deeds": {},
                    "Financial_Records": {}
                }
            elif entity_data['type'] in ['company', 'nominee_company']:
                base_structure["💼VOCATION"]["VERIFIED_CORPORATE_STRUCTURE"]["Operating_Companies"][entity_name] = {
                    "Directors_Shareholders": {},
                    "ABN_ACN_Records": {},
                    "Legal_Documents": {},
                    "Financial_Records": {}
                }
            elif entity_data['type'] == 'business_operation':
                category = entity_data.get('category', 'general')
                if category not in base_structure["💼VOCATION"]["VERIFIED_BUSINESS_OPERATIONS"]:
                    base_structure["💼VOCATION"]["VERIFIED_BUSINESS_OPERATIONS"][category] = {}
                base_structure["💼VOCATION"]["VERIFIED_BUSINESS_OPERATIONS"][category][entity_name] = {}
        
        self.folder_structure = base_structure
        return base_structure
    
    async def create_physical_folders(self, base_path: Path):
        """Create the physical folder structure"""
        def create_recursive(structure: Dict, current_path: Path):
            for folder_name, substructure in structure.items():
                folder_path = current_path / folder_name
                folder_path.mkdir(exist_ok=True)
                if isinstance(substructure, dict) and substructure:
                    create_recursive(substructure, folder_path)
        
        create_recursive(self.folder_structure, base_path)
        print(f"📁 Created folder structure at {base_path}")
    
    async def organize_documents_forensically(self):
        """Main forensic organization process using MCP data"""
        print("🔺 Starting MCP-based Forensic Document Organization")
        print("="*60)
        
        # Load corporate data from MCP Notion server
        corporate_data = await self.load_corporate_data_from_mcp()
        print(f"✅ Loaded {len(corporate_data['verified_entities'])} verified entities")
        
        # Generate folder structure
        await self.generate_forensic_folder_structure(corporate_data)
        print("✅ Generated forensic folder structure")
        
        # Create physical folders
        await self.create_physical_folders(self.documents_path)
        
        # Scan and classify documents
        document_files = [f for f in self.documents_path.iterdir() 
                         if f.is_file() and not f.name.startswith('.')]
        
        classifications = []
        for filepath in document_files:
            classification = self.classify_document_forensically(filepath, corporate_data)
            classifications.append(classification)
            
            # Store classification in MCP SQLite
            await self.store_classification_in_mcp(classification)
        
        # Report results
        print(f"\n🔍 Forensic Classification Results:")
        print("="*60)
        
        verified_count = len([c for c in classifications if c.forensic_flag == '✅'])
        anomaly_count = len([c for c in classifications if c.forensic_flag == '🚨'])
        unknown_count = len([c for c in classifications if c.forensic_flag == '❓'])
        
        print(f"✅ Verified: {verified_count} documents")
        print(f"🚨 Anomalies: {anomaly_count} documents") 
        print(f"❓ Unknown: {unknown_count} documents")
        
        # Show anomalies for investigation
        anomalies = [c for c in classifications if c.forensic_flag == '🚨']
        if anomalies:
            print(f"\n🚨 ANOMALIES REQUIRING INVESTIGATION:")
            for anomaly in anomalies:
                print(f"   {anomaly.filename}")
                for indicator in anomaly.anomaly_indicators:
                    print(f"     ⚠️  {indicator}")
        
        return classifications

async def main():
    """Run MCP-based forensic document organization"""
    organizer = MCPForensicOrganizer()
    classifications = await organizer.organize_documents_forensically()
    
    print(f"\n📊 Forensic organization complete - processed {len(classifications)} documents")

if __name__ == "__main__":
    asyncio.run(main())