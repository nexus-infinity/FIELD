#!/usr/bin/env python3
"""
File Access Pattern Analyzer
Analyzes file access patterns to determine optimal storage placement
"""

import os
import time
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import mmap
import struct

class AccessPatternAnalyzer:
    def __init__(self, base_dirs: List[str]):
        self.base_dirs = base_dirs
        self.db_path = "/Users/jbear/FIELD/storage_optimization.db"
        self.index_path = "/Users/jbear/FIELD/file_index.mmap"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for file metadata"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_metadata (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE,
                size INTEGER,
                last_access REAL,
                last_modified REAL,
                access_count INTEGER DEFAULT 0,
                file_type TEXT,
                content_hash TEXT,
                storage_location TEXT,
                performance_score REAL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS access_patterns (
                id INTEGER PRIMARY KEY,
                file_path TEXT,
                access_time REAL,
                operation_type TEXT,
                FOREIGN KEY (file_path) REFERENCES file_metadata (path)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def analyze_directory(self, directory: str) -> Dict:
        """Analyze access patterns for a directory"""
        results = {
            'total_files': 0,
            'total_size': 0,
            'by_type': {},
            'by_size': {'small': 0, 'medium': 0, 'large': 0},
            'by_age': {'recent': 0, 'old': 0, 'ancient': 0},
            'recommendations': []
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = time.time()
        week_ago = now - (7 * 24 * 3600)
        month_ago = now - (30 * 24 * 3600)
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    stat = os.stat(file_path)
                    file_size = stat.st_size
                    last_access = stat.st_atime
                    last_modified = stat.st_mtime
                    
                    # File type analysis
                    file_ext = Path(file_path).suffix.lower()
                    if file_ext not in results['by_type']:
                        results['by_type'][file_ext] = {'count': 0, 'size': 0}
                    results['by_type'][file_ext]['count'] += 1
                    results['by_type'][file_ext]['size'] += file_size
                    
                    # Size categorization
                    if file_size < 1024 * 1024:  # < 1MB
                        results['by_size']['small'] += 1
                    elif file_size < 100 * 1024 * 1024:  # < 100MB
                        results['by_size']['medium'] += 1
                    else:
                        results['by_size']['large'] += 1
                    
                    # Age analysis
                    if last_access > week_ago:
                        results['by_age']['recent'] += 1
                    elif last_access > month_ago:
                        results['by_age']['old'] += 1
                    else:
                        results['by_age']['ancient'] += 1
                    
                    # Calculate performance score
                    access_frequency = max(1, (now - last_access) / 86400)  # Days since access
                    size_factor = min(1.0, file_size / (10 * 1024 * 1024))  # Size impact
                    performance_score = (1 / access_frequency) * (1 - size_factor)
                    
                    # Store in database
                    cursor.execute("""
                        INSERT OR REPLACE INTO file_metadata 
                        (path, size, last_access, last_modified, file_type, performance_score, storage_location)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (file_path, file_size, last_access, last_modified, file_ext, performance_score, directory))
                    
                    results['total_files'] += 1
                    results['total_size'] += file_size
                    
                except (OSError, IOError):
                    continue
        
        conn.commit()
        conn.close()
        
        # Generate recommendations
        results['recommendations'] = self.generate_recommendations(directory, results)
        
        return results
    
    def generate_recommendations(self, directory: str, analysis: Dict) -> List[str]:
        """Generate storage optimization recommendations"""
        recommendations = []
        
        # High-frequency access optimization
        if 'FIELD' in directory and directory.endswith('FIELD'):
            if analysis['by_age']['ancient'] > analysis['by_age']['recent']:
                recommendations.append("Consider moving ancient files to FIELD-DEV for archival")
            
            if analysis['by_size']['large'] > 100:
                recommendations.append("Large files should be symlinked from FIELD-DEV")
            
            if analysis['total_size'] > 15 * 1024 * 1024 * 1024:  # > 15GB
                recommendations.append("Directory size exceeds optimal threshold - implement archival")
        
        # Archive optimization
        if 'FIELD-DEV' in directory:
            if analysis['by_age']['recent'] > analysis['by_age']['old']:
                recommendations.append("Consider creating symlinks to frequently accessed files")
            
            recommendations.append("Implement compression for old files")
        
        return recommendations
    
    def create_memory_mapped_index(self):
        """Create memory-mapped file index for rapid lookups"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT path, size, last_access, file_type, performance_score 
            FROM file_metadata 
            ORDER BY performance_score DESC
        """)
        
        records = cursor.fetchall()
        conn.close()
        
        # Create memory-mapped index
        with open(self.index_path, 'wb') as f:
            # Header: number of records
            f.write(struct.pack('I', len(records)))
            
            # Records: path_len, path, size, last_access, type_len, type, score
            for record in records:
                path, size, last_access, file_type, score = record
                path_bytes = path.encode('utf-8')
                type_bytes = file_type.encode('utf-8')
                
                f.write(struct.pack('I', len(path_bytes)))
                f.write(path_bytes)
                f.write(struct.pack('Q', size))
                f.write(struct.pack('d', last_access))
                f.write(struct.pack('I', len(type_bytes)))
                f.write(type_bytes)
                f.write(struct.pack('d', score))
    
    def get_migration_candidates(self, source_dir: str, target_dir: str) -> List[Tuple[str, str]]:
        """Get list of files to migrate from source to target directory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Files that should be moved to archive (low performance score, large size)
        cursor.execute("""
            SELECT path, size FROM file_metadata 
            WHERE storage_location = ? 
            AND performance_score < 0.1 
            AND size > 10485760  -- 10MB
            ORDER BY size DESC
            LIMIT 1000
        """, (source_dir,))
        
        candidates = []
        for path, size in cursor.fetchall():
            # Generate target path
            rel_path = os.path.relpath(path, source_dir)
            target_path = os.path.join(target_dir, rel_path)
            candidates.append((path, target_path))
        
        conn.close()
        return candidates

def main():
    """Main execution function"""
    analyzer = AccessPatternAnalyzer([
        "/Users/jbear/FIELD",
        "/Users/jbear/FIELD-DEV",
        "/Users/jbear/FIELD-LIVING"
    ])
    
    print("Analyzing file access patterns...")
    
    # Analyze each directory
    for directory in analyzer.base_dirs:
        if os.path.exists(directory):
            print(f"\nAnalyzing {directory}...")
            results = analyzer.analyze_directory(directory)
            
            print(f"Total files: {results['total_files']}")
            print(f"Total size: {results['total_size'] / (1024**3):.2f} GB")
            print(f"File age distribution: {results['by_age']}")
            print(f"Recommendations: {results['recommendations']}")
    
    # Create memory-mapped index
    print("\nCreating memory-mapped index...")
    analyzer.create_memory_mapped_index()
    
    # Get migration candidates
    candidates = analyzer.get_migration_candidates("/Users/jbear/FIELD", "/Users/jbear/FIELD-DEV")
    print(f"\nFound {len(candidates)} migration candidates")
    
    # Save results
    with open("/Users/jbear/FIELD/access_analysis_results.json", 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'migration_candidates': candidates[:50],  # Top 50 candidates
            'analysis_complete': True
        }, f, indent=2)
    
    print("Analysis complete! Results saved to access_analysis_results.json")

if __name__ == "__main__":
    main()
