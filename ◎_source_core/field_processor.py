#!/usr/bin/env python3

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

class FieldProcessor:
    # Sacred Geometry Symbols
    SYMBOLS = {
        'DOJO_ACTIVE': '◼︎',
        'SOURCE_CORE': '◎',
        'OBSERVER': '●',
        'LIVING_MEMORY': '◆',
        'INTEGRATION': '⬡',
        'CHAKRA': '⬢',
        'TATA': '◉',
        'OBI_WAN': '◯'
    }
    
    def __init__(self, field_root="/Users/jbear/FIELD"):
        self.field_root = field_root
        self.sacred_paths = self._initialize_sacred_paths()
        
    def _initialize_sacred_paths(self):
        """Initialize paths using sacred geometry symbols"""
        return {
            'active': os.path.join(self.field_root, f"{self.SYMBOLS['DOJO_ACTIVE']}DOJO_ACTIVE"),
            'source': os.path.join(self.field_root, f"{self.SYMBOLS['SOURCE_CORE']}_source_core"),
            'memory': os.path.join(self.field_root, f"{self.SYMBOLS['LIVING_MEMORY']}_living_memory"),
            'observer': os.path.join(self.field_root, f"{self.SYMBOLS['OBSERVER']}_observer_core"),
            'integration': os.path.join(self.field_root, f"{self.SYMBOLS['INTEGRATION']}_integration"),
            'chakra': os.path.join(self.field_root, f"{self.SYMBOLS['CHAKRA']}_CHAKRA_SYSTEM")
        }
    
    def process_document(self, source_path, context=None):
        """Process a document maintaining sacred geometry alignment"""
        if not os.path.exists(source_path):
            return False, f"Source path does not exist: {source_path}"
            
        # Determine document type and sacred alignment
        doc_type = self._determine_document_type(source_path)
        sacred_path = self._get_sacred_path(doc_type, context)
        
        # Create sacred timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate sacred-aligned filename
        filename = os.path.basename(source_path)
        sacred_filename = f"{timestamp}_{self._sanctify_filename(filename)}"
        
        # Create target path with sacred geometry
        target_path = os.path.join(sacred_path, sacred_filename)
        
        # Ensure target directory exists
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Copy with sacred intention
        try:
            if os.path.isdir(source_path):
                shutil.copytree(source_path, target_path)
            else:
                shutil.copy2(source_path, target_path)
            return True, target_path
        except Exception as e:
            return False, str(e)
    
    def _determine_document_type(self, path):
        """Determine document type based on path and content"""
        path_lower = path.lower()
        if "workcover" in path_lower or "legal" in path_lower:
            return "legal"
        elif "medical" in path_lower:
            return "health"
        elif "fraud" in path_lower or "investigation" in path_lower:
            return "investigation"
        else:
            return "document"
    
    def _get_sacred_path(self, doc_type, context=None):
        """Get sacred-aligned path based on document type"""
        if doc_type == "legal":
            return os.path.join(self.sacred_paths['active'], "legal_intelligence")
        elif doc_type == "health":
            return os.path.join(self.sacred_paths['memory'], "health_records")
        elif doc_type == "investigation":
            return os.path.join(self.sacred_paths['observer'], "investigations")
        else:
            return os.path.join(self.sacred_paths['source'], "documents")
    
    def _sanctify_filename(self, filename):
        """Transform filename to maintain sacred alignment"""
        # Remove special characters while preserving sacred symbols
        clean_name = ""
        for char in filename:
            if char in "".join(self.SYMBOLS.values()):
                clean_name += char
            elif char.isalnum() or char in ".-_":
                clean_name += char
            else:
                clean_name += "_"
        return clean_name

    def process_directory(self, source_dir, context=None):
        """Process entire directory maintaining sacred geometry"""
        results = []
        for root, dirs, files in os.walk(source_dir):
            for item in dirs + files:
                source_path = os.path.join(root, item)
                success, result = self.process_document(source_path, context)
                results.append({
                    'source': source_path,
                    'success': success,
                    'result': result
                })
        return results

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <source_path> [context_json]")
        sys.exit(1)
        
    source_path = sys.argv[1]
    context = None
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            context = json.load(f)
            
    processor = FieldProcessor()
    
    if os.path.isdir(source_path):
        results = processor.process_directory(source_path, context)
    else:
        success, result = processor.process_document(source_path, context)
        results = [{
            'source': source_path,
            'success': success,
            'result': result
        }]
        
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()