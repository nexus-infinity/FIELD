#!/usr/bin/env python3
"""
Universal Data Processing Module for FIELD System
================================================

This module provides a comprehensive solution for automatically ingesting,
categorizing, and organizing data from multiple sources into the FIELD system.

Data Sources Supported:
- CZUR Scanner (CZURImages/)
- Phone/Genius Scanner
- Printers (network and local)
- Manual uploads
- Cloud services (Drive, iCloud, OneDrive)
- Database exports

File Formats Handled:
- Documents: PDF, DOCX, DOC, TXT, MD
- Images: PNG, JPG, JPEG, TIFF, HEIC
- Data: JSON, CSV, XML, XLSX, XLS
- Archives: ZIP, TAR, RAR
- Code: PY, JS, TS, GO, etc.

Organizational Structure:
- FIELD-DEV: Development and active projects
- FIELD-LIVING: Production and live systems
- FIELD: Core system and knowledge base
- FIELD-QUARANTINE: Unprocessed/suspicious files
- FIELD-ARCHIVE: Historical data
"""

import os
import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import mimetypes
import logging

class UniversalDataProcessor:
    """
    Universal data processing and organization system for FIELD architecture.
    """
    
    def __init__(self, base_path: str = "/Users/jbear"):
        self.base_path = Path(base_path)
        self.field_paths = {
            'dev': self.base_path / 'FIELD-DEV',
            'living': self.base_path / 'FIELD-LIVING', 
            'core': self.base_path / 'FIELD',
            'quarantine': self.base_path / 'FIELD-QUARANTINE',
            'truth': self.base_path / 'FIELD-TRUTH',
            'backup': self.base_path / 'FIELD-BACKUPS'
        }
        
        # Data source paths
        self.source_paths = {
            'czur': self.base_path / 'CZURImages',
            'data': self.base_path / 'DATA',
            'downloads': self.base_path / 'Downloads',
            'desktop': self.base_path / 'Desktop',
            'documents': self.base_path / 'Documents'
        }
        
        # Initialize logging
        self.setup_logging()
        
        # File type mappings
        self.type_mappings = {
            'documents': ['.pdf', '.docx', '.doc', '.txt', '.md', '.rtf'],
            'images': ['.png', '.jpg', '.jpeg', '.tiff', '.heic', '.gif', '.bmp'],
            'data': ['.json', '.csv', '.xml', '.xlsx', '.xls', '.db', '.sqlite'],
            'code': ['.py', '.js', '.ts', '.go', '.rs', '.java', '.cpp', '.h'],
            'archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
            'media': ['.mp4', '.mov', '.avi', '.mp3', '.wav', '.m4a']
        }
        
        # Processing rules
        self.processing_rules = self.load_processing_rules()
    
    def setup_logging(self):
        """Initialize logging system."""
        log_dir = self.base_path / 'FIELD' / '◎_source_core' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'data_processor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_processing_rules(self) -> Dict:
        """Load processing rules from configuration."""
        rules_file = self.base_path / 'FIELD' / '◎_source_core' / 'config' / 'processing_rules.json'
        
        default_rules = {
            "auto_process": True,
            "quarantine_unknown": True,
            "duplicate_handling": "link",
            "metadata_extraction": True,
            "content_analysis": True,
            "classification_threshold": 0.7,
            "auto_categorization": True,
            "backup_originals": True
        }
        
        if rules_file.exists():
            with open(rules_file, 'r') as f:
                return {**default_rules, **json.load(f)}
        return default_rules
    
    def scan_sources(self) -> List[Path]:
        """Scan all data sources for new files."""
        new_files = []
        
        for source_name, source_path in self.source_paths.items():
            if source_path.exists():
                self.logger.info(f"Scanning {source_name}: {source_path}")
                
                for file_path in source_path.rglob('*'):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        if self.is_new_file(file_path):
                            new_files.append(file_path)
                            self.logger.info(f"Found new file: {file_path}")
        
        return new_files
    
    def is_new_file(self, file_path: Path) -> bool:
        """Check if file is new and hasn't been processed."""
        # Check against processing log
        processed_files_log = self.base_path / 'FIELD' / '◎_source_core' / 'logs' / 'processed_files.json'
        
        if not processed_files_log.exists():
            return True
            
        with open(processed_files_log, 'r') as f:
            processed = json.load(f)
            
        file_hash = self.calculate_file_hash(file_path)
        return file_hash not in processed
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file."""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def classify_file(self, file_path: Path) -> Tuple[str, str, float]:
        """Classify file type and determine destination."""
        file_ext = file_path.suffix.lower()
        mime_type, _ = mimetypes.guess_type(str(file_path))
        
        # Basic classification by extension
        for category, extensions in self.type_mappings.items():
            if file_ext in extensions:
                confidence = 0.9
                destination = self.determine_destination(file_path, category)
                return category, destination, confidence
        
        # If unknown, send to quarantine
        return 'unknown', 'quarantine', 0.0
    
    def determine_destination(self, file_path: Path, category: str) -> str:
        """Determine the appropriate FIELD destination."""
        file_name = file_path.name.lower()
        
        # Development files
        if any(keyword in file_name for keyword in ['dev', 'test', 'proto', 'experiment']):
            return 'dev'
        
        # Living/Production files
        elif any(keyword in file_name for keyword in ['prod', 'live', 'deploy', 'release']):
            return 'living'
        
        # Core system files
        elif any(keyword in file_name for keyword in ['core', 'system', 'config', 'atlas']):
            return 'core'
        
        # Scanner/Document processing
        elif file_path.parent.name == 'CZURImages' or category == 'documents':
            return 'core'  # Documents go to core for processing
        
        # Data files
        elif category == 'data':
            return 'living'  # Data goes to living for analysis
        
        # Default to development
        else:
            return 'dev'
    
    def process_file(self, file_path: Path) -> Dict:
        """Process a single file through the pipeline."""
        self.logger.info(f"Processing file: {file_path}")
        
        try:
            # Calculate file metadata
            file_hash = self.calculate_file_hash(file_path)
            file_size = file_path.stat().st_size
            created_time = datetime.fromtimestamp(file_path.stat().st_ctime)
            
            # Classify file
            category, destination, confidence = self.classify_file(file_path)
            
            # Create processing record
            processing_record = {
                'source_path': str(file_path),
                'hash': file_hash,
                'size': file_size,
                'created': created_time.isoformat(),
                'processed': datetime.now().isoformat(),
                'category': category,
                'destination': destination,
                'confidence': confidence
            }
            
            # Handle file based on destination
            if destination == 'quarantine' or confidence < self.processing_rules['classification_threshold']:
                new_path = self.move_to_quarantine(file_path, processing_record)
            else:
                new_path = self.organize_file(file_path, destination, category)
            
            processing_record['new_path'] = str(new_path)
            
            # Log processing
            self.log_processed_file(processing_record)
            
            return processing_record
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return {'error': str(e), 'source_path': str(file_path)}
    
    def move_to_quarantine(self, file_path: Path, record: Dict) -> Path:
        """Move file to quarantine for manual review."""
        quarantine_path = self.field_paths['quarantine']
        quarantine_path.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped folder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        quarantine_folder = quarantine_path / f"quarantine_{timestamp}"
        quarantine_folder.mkdir(exist_ok=True)
        
        # Move file
        new_path = quarantine_folder / file_path.name
        shutil.move(str(file_path), str(new_path))
        
        # Create metadata file
        metadata_file = quarantine_folder / f"{file_path.stem}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(record, f, indent=2)
        
        self.logger.info(f"Moved to quarantine: {new_path}")
        return new_path
    
    def organize_file(self, file_path: Path, destination: str, category: str) -> Path:
        """Organize file into appropriate FIELD structure."""
        dest_path = self.field_paths[destination]
        
        # Create category-based subfolder
        if destination == 'core':
            # Core files go into ATLAS knowledge structure
            category_path = dest_path / '▲ATLAS' / '▲⬟◯_knowledge_banks' / category
        elif destination == 'dev':
            # Dev files go into active development
            category_path = dest_path / f'●_{category}_intake'
        elif destination == 'living':
            # Living files go into production structure
            category_path = dest_path / f'●◆_living_{category}'
        else:
            category_path = dest_path / category
        
        category_path.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped subfolder
        timestamp = datetime.now().strftime('%Y%m%d')
        daily_folder = category_path / timestamp
        daily_folder.mkdir(exist_ok=True)
        
        # Move file
        new_path = daily_folder / file_path.name
        shutil.move(str(file_path), str(new_path))
        
        self.logger.info(f"Organized to: {new_path}")
        return new_path
    
    def log_processed_file(self, record: Dict):
        """Log processed file to tracking system."""
        processed_log = self.base_path / 'FIELD' / '◎_source_core' / 'logs' / 'processed_files.json'
        
        if processed_log.exists():
            with open(processed_log, 'r') as f:
                processed_files = json.load(f)
        else:
            processed_files = {}
        
        processed_files[record['hash']] = record
        
        with open(processed_log, 'w') as f:
            json.dump(processed_files, f, indent=2)
    
    def run_processing_cycle(self) -> Dict:
        """Run a complete processing cycle."""
        self.logger.info("Starting processing cycle")
        
        # Scan for new files
        new_files = self.scan_sources()
        
        if not new_files:
            self.logger.info("No new files found")
            return {'status': 'complete', 'processed': 0, 'errors': 0}
        
        # Process each file
        results = []
        errors = 0
        
        for file_path in new_files:
            result = self.process_file(file_path)
            results.append(result)
            
            if 'error' in result:
                errors += 1
        
        # Generate summary report
        summary = {
            'status': 'complete',
            'processed': len(results),
            'errors': errors,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        # Save processing report
        report_path = self.base_path / 'FIELD-REPORTS' / f"processing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.logger.info(f"Processing cycle complete. Processed: {len(results)}, Errors: {errors}")
        return summary
    
    def setup_automation(self):
        """Setup automated processing using system tools."""
        # Create launchd plist for macOS automation
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.field.dataprocessor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{self.base_path}/FIELD/◎_source_core/universal_data_processor.py</string>
        <string>--auto</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>'''
        
        plist_path = Path.home() / 'Library' / 'LaunchAgents' / 'com.field.dataprocessor.plist'
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        
        self.logger.info(f"Created automation plist: {plist_path}")


def main():
    """Main entry point for the universal data processor."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal Data Processor for FIELD System')
    parser.add_argument('--auto', action='store_true', help='Run in automatic mode')
    parser.add_argument('--scan-only', action='store_true', help='Only scan for files, don\'t process')
    parser.add_argument('--setup', action='store_true', help='Setup automation')
    
    args = parser.parse_args()
    
    processor = UniversalDataProcessor()
    
    if args.setup:
        processor.setup_automation()
        print("✓ Automation setup complete")
    elif args.scan_only:
        files = processor.scan_sources()
        print(f"Found {len(files)} new files to process")
    else:
        result = processor.run_processing_cycle()
        print(f"Processing complete: {result['processed']} files processed, {result['errors']} errors")


if __name__ == '__main__':
    main()