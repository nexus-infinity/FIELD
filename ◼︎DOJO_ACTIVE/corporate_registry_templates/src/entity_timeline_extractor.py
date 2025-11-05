#!/usr/bin/env python3
"""
BERJAK | NEXUS | INFINITY FRE Entity Timeline Extractor
Automatically scans files and extracts comprehensive timeline of corporate entities
"""

import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

class EntityTimelineExtractor:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.entities = set()
        self.timelines = {}
        self.file_registry = {}
        
        # Entity name patterns
        self.entity_patterns = {
            'berjak': [
                r'Berjak.*Pty.*Ltd',
                r'Berjak.*Nominees',
                r'Berjak.*\(VIC\)',
                r'Berjak.*\(NT\)',
                r'Berjak.*Metals'
            ],
            'ansevata': [
                r'Ansevata.*Nominees',
                r'Ansevata.*Investments',
                r'Ansevata.*Trust'
            ],
            'other': [
                r'Next.*Vintage',
                r'J.*Rich.*Partners'
            ]
        }
        
    def scan_files(self):
        """Scan all files in base directory and build registry"""
        for file_path in self.base_dir.rglob('*'):
            if file_path.is_file() and self._is_relevant_file(file_path):
                self._process_file(file_path)
                
    def _is_relevant_file(self, file_path: Path) -> bool:
        """Check if file is likely to contain relevant corporate information"""
        relevant_extensions = {'.pdf', '.doc', '.docx', '.txt', '.csv', '.xlsx'}
        if file_path.suffix.lower() not in relevant_extensions:
            return False
            
        # Look for key terms in filename
        key_terms = ['asic', 'company', 'corporate', 'trust', 'deed', 
                    'minutes', 'resolution', 'director', 'shareholder',
                    'berjak', 'ansevata']
                    
        return any(term in file_path.name.lower() for term in key_terms)
        
    def _process_file(self, file_path: Path):
        """Process a single file and extract corporate entity information"""
        try:
            file_date = self._extract_date_from_filename(file_path)
            content = self._extract_file_content(file_path)
            
            # Extract entities mentioned
            entities = self._extract_entities(content)
            
            if entities:
                self.file_registry[str(file_path)] = {
                    'date': file_date,
                    'entities': list(entities),
                    'type': self._determine_document_type(file_path, content)
                }
                
                # Update entity timelines
                for entity in entities:
                    if entity not in self.timelines:
                        self.timelines[entity] = []
                    
                    self.timelines[entity].append({
                        'date': file_date,
                        'file': str(file_path),
                        'type': self.file_registry[str(file_path)]['type']
                    })
                    
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            
    def _extract_date_from_filename(self, file_path: Path) -> str:
        """Extract date from filename or use file modification time"""
        # Try to find YYYYMMDD or YYYY_MM_DD pattern
        date_patterns = [
            r'(\d{4})[\s_-]?(\d{2})[\s_-]?(\d{2})',
            r'(\d{2})[\s_-]?(\d{2})[\s_-]?(\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, file_path.name)
            if match:
                groups = match.groups()
                if len(groups[0]) == 4:  # YYYY-MM-DD
                    return f"{groups[0]}-{groups[1]}-{groups[2]}"
                else:  # DD-MM-YYYY
                    return f"{groups[2]}-{groups[1]}-{groups[0]}"
                    
        # Fallback to file modification time
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        return mtime.strftime('%Y-%m-%d')
        
    def _extract_file_content(self, file_path: Path) -> str:
        """Extract text content from file"""
        # Implementation would handle different file types
        # This is a placeholder that returns filename
        return file_path.name
        
    def _extract_entities(self, content: str) -> Set[str]:
        """Extract mentioned corporate entities from content"""
        entities = set()
        
        for category, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                entities.update(match.group(0) for match in matches)
                
        return entities
        
    def _determine_document_type(self, file_path: Path, content: str) -> str:
        """Determine document type based on filename and content"""
        filename = file_path.name.lower()
        
        if 'asic' in filename:
            return 'ASIC_DOCUMENT'
        elif any(term in filename for term in ['minutes', 'resolution']):
            return 'CORPORATE_RESOLUTION'
        elif 'trust' in filename and 'deed' in filename:
            return 'TRUST_DEED'
        elif any(term in filename for term in ['financial', 'statement', 'report']):
            return 'FINANCIAL_DOCUMENT'
        else:
            return 'OTHER'
            
    def generate_entity_timelines(self):
        """Generate comprehensive timelines for each entity"""
        for entity in self.timelines:
            # Sort timeline by date
            self.timelines[entity].sort(key=lambda x: x['date'])
            
            # Group by year
            timeline_by_year = {}
            for event in self.timelines[entity]:
                year = event['date'].split('-')[0]
                if year not in timeline_by_year:
                    timeline_by_year[year] = []
                timeline_by_year[year].append(event)
                
            self.timelines[entity] = timeline_by_year
            
    def export_timelines(self):
        """Export timelines to JSON"""
        output = {
            'generated_at': datetime.now().isoformat(),
            'entities': list(self.timelines.keys()),
            'timelines': self.timelines,
            'file_registry': self.file_registry
        }
        
        output_file = self.base_dir / 'corporate_registry_templates/output/entity_timelines.json'
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
            
def main():
    base_dir = Path('/Users/jbear/FIELD/◼︎DOJO_ACTIVE')
    extractor = EntityTimelineExtractor(base_dir)
    
    print("Scanning files...")
    extractor.scan_files()
    
    print("Generating timelines...")
    extractor.generate_entity_timelines()
    
    print("Exporting results...")
    extractor.export_timelines()
    
if __name__ == '__main__':
    main()