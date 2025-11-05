#!/usr/bin/env python3
"""
Notion-Documents Forensic Integration
Pulls verified corporate structure from Notion databases for document classification
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import hashlib

@dataclass
class CorporateEntity:
    """Verified corporate entity from Notion"""
    name: str
    entity_type: str  # "trust", "company", "partnership"
    abn: Optional[str] = None
    acn: Optional[str] = None
    trustees: List[str] = None
    directors: List[str] = None
    status: str = "active"  # active, dormant, deregistered
    verification_source: str = "notion"
    
class NotionForensicIntegrator:
    """Integrates Notion corporate database with document organization"""
    
    def __init__(self, notion_token: Optional[str] = None):
        self.notion_token = notion_token or os.getenv('NOTION_TOKEN')
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        self.verified_entities = {}
        self.forensic_flags = {
            'verified': '✅',
            'anomaly': '🚨',
            'unknown': '❓',
            'shadow': '👻'
        }
        
    def fetch_corporate_entities(self, database_id: str) -> List[CorporateEntity]:
        """Fetch verified corporate entities from Notion database"""
        try:
            response = requests.post(
                f"{self.base_url}/databases/{database_id}/query",
                headers=self.headers,
                json={"page_size": 100}
            )
            
            if response.status_code != 200:
                print(f"Notion API error: {response.status_code}")
                return []
                
            entities = []
            for page in response.json()['results']:
                props = page['properties']
                
                entity = CorporateEntity(
                    name=self._extract_title(props.get('Name', {})),
                    entity_type=self._extract_select(props.get('Type', {})),
                    abn=self._extract_text(props.get('ABN', {})),
                    acn=self._extract_text(props.get('ACN', {})),
                    trustees=self._extract_multi_select(props.get('Trustees', {})),
                    directors=self._extract_multi_select(props.get('Directors', {})),
                    status=self._extract_select(props.get('Status', {}))
                )
                entities.append(entity)
                
            return entities
            
        except Exception as e:
            print(f"Error fetching from Notion: {e}")
            return []
    
    def _extract_title(self, prop: Dict) -> str:
        """Extract title from Notion property"""
        try:
            return prop['title'][0]['text']['content'] if prop.get('title') else ""
        except (KeyError, IndexError):
            return ""
    
    def _extract_text(self, prop: Dict) -> str:
        """Extract rich text from Notion property"""
        try:
            return prop['rich_text'][0]['text']['content'] if prop.get('rich_text') else ""
        except (KeyError, IndexError):
            return ""
    
    def _extract_select(self, prop: Dict) -> str:
        """Extract select from Notion property"""
        try:
            return prop['select']['name'] if prop.get('select') else ""
        except (KeyError, TypeError):
            return ""
    
    def _extract_multi_select(self, prop: Dict) -> List[str]:
        """Extract multi-select from Notion property"""
        try:
            return [item['name'] for item in prop['multi_select']] if prop.get('multi_select') else []
        except (KeyError, TypeError):
            return []
    
    def build_forensic_schema(self, entities: List[CorporateEntity]) -> Dict:
        """Build document classification schema from verified entities"""
        schema = {
            'verified_entities': {},
            'entity_patterns': {},
            'forensic_rules': {}
        }
        
        for entity in entities:
            # Create entity record
            schema['verified_entities'][entity.name] = {
                'type': entity.entity_type,
                'abn': entity.abn,
                'acn': entity.acn,
                'trustees': entity.trustees,
                'directors': entity.directors,
                'status': entity.status,
                'document_keywords': self._generate_keywords(entity)
            }
            
            # Create search patterns for document classification
            patterns = []
            patterns.append(entity.name.lower())
            if entity.abn:
                patterns.append(entity.abn)
            if entity.acn:
                patterns.append(entity.acn)
            
            schema['entity_patterns'][entity.name] = patterns
        
        return schema
    
    def _generate_keywords(self, entity: CorporateEntity) -> List[str]:
        """Generate keywords for document classification"""
        keywords = [entity.name.lower()]
        
        # Add variations
        name_parts = entity.name.lower().split()
        keywords.extend(name_parts)
        
        # Add identifiers
        if entity.abn:
            keywords.append(entity.abn)
        if entity.acn:
            keywords.append(entity.acn)
            
        return list(set(keywords))
    
    def classify_document(self, filename: str, schema: Dict) -> Dict:
        """Classify document based on forensic schema"""
        filename_lower = filename.lower()
        
        classification = {
            'filename': filename,
            'matched_entities': [],
            'forensic_flag': self.forensic_flags['unknown'],
            'confidence': 0,
            'anomaly_indicators': []
        }
        
        # Check against verified entities
        for entity_name, patterns in schema['entity_patterns'].items():
            for pattern in patterns:
                if pattern and pattern in filename_lower:
                    classification['matched_entities'].append(entity_name)
                    classification['forensic_flag'] = self.forensic_flags['verified']
                    classification['confidence'] += 1
        
        # Check for potential anomalies
        company_indicators = ['pty ltd', 'trust', 'partnership', 'limited', 'corp']
        if any(indicator in filename_lower for indicator in company_indicators):
            if not classification['matched_entities']:
                classification['forensic_flag'] = self.forensic_flags['anomaly']
                classification['anomaly_indicators'].append('Unknown corporate entity')
        
        return classification
    
    def generate_folder_structure(self, schema: Dict) -> Dict:
        """Generate folder structure based on verified entities"""
        structure = {
            "📁PERSONAL": {},
            "💼VOCATION": {
                "VERIFIED_CORPORATE_STRUCTURE": {
                    "Trust_Structures": {},
                    "Operating_Companies": {}
                },
                "VERIFIED_BUSINESS_OPERATIONS": {},
                "🚨ANOMALY_DETECTION": {
                    "Unknown_Entities": {},
                    "Shadow_Structure_Indicators": {},
                    "Timeline_Discrepancies": {}
                }
            },
            "🌐COMMUNITY": {},
            "⟡_INTAKE": {}
        }
        
        # Add verified entities to structure
        for entity_name, entity_data in schema['verified_entities'].items():
            if entity_data['type'] == 'trust':
                structure["💼VOCATION"]["VERIFIED_CORPORATE_STRUCTURE"]["Trust_Structures"][entity_name] = {
                    "Trustee": {},
                    "Beneficiaries": {},
                    "Trust_Deeds": {},
                    "Financial_Records": {}
                }
            elif entity_data['type'] == 'company':
                structure["💼VOCATION"]["VERIFIED_CORPORATE_STRUCTURE"]["Operating_Companies"][entity_name] = {
                    "Directors_Shareholders": {},
                    "ABN_ACN_Records": {},
                    "Legal_Documents": {},
                    "Financial_Records": {}
                }
        
        return structure

def main():
    """Test integration with sample Notion database"""
    integrator = NotionForensicIntegrator()
    
    # For now, create sample entities for testing
    sample_entities = [
        CorporateEntity(
            name="ANSEVATA No 2 Trust",
            entity_type="trust",
            trustees=["Berjak Nominees (N.T.) Pty Ltd"],
            status="active"
        ),
        CorporateEntity(
            name="Berjak and Partners Unit Trust", 
            entity_type="trust",
            trustees=["TBD"],
            status="active"
        ),
        CorporateEntity(
            name="Berjak Metals Pty Ltd",
            entity_type="company",
            acn="123456789",
            directors=["Jeremy Rich"],
            status="active"
        )
    ]
    
    # Build forensic schema
    schema = integrator.build_forensic_schema(sample_entities)
    
    # Test document classification
    test_files = [
        "2023 Annual Company Statement - Berjak Metals Pty Ltd.pdf",
        "ANSEVATA No 2 Trust deed.pdf", 
        "Unknown Company Annual Report.pdf"
    ]
    
    print("🔍 Forensic Document Classification:")
    print("="*50)
    
    for filename in test_files:
        classification = integrator.classify_document(filename, schema)
        flag = classification['forensic_flag']
        entities = classification['matched_entities']
        
        print(f"{flag} {filename}")
        if entities:
            print(f"   Matched: {', '.join(entities)}")
        if classification['anomaly_indicators']:
            print(f"   ⚠️  Anomalies: {', '.join(classification['anomaly_indicators'])}")
    
    # Generate folder structure
    structure = integrator.generate_folder_structure(schema)
    print(f"\n📁 Generated {len(structure)} main folders with verified entity substructures")

if __name__ == "__main__":
    main()