#!/usr/bin/env python3
"""
Document Processing Bridge - Physical to Digital
Handles the workflow from phone scanning to categorized storage
Built on FIELD system principles with grounded, incremental approach
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import sqlite3

class DocumentBridge:
    """Bridge between physical documents and digital organization"""
    
    def __init__(self, base_path: str = "/Users/jbear/FIELD/◎_source_core/documents"):
        self.base_path = Path(base_path)
        self.inbox_path = self.base_path / "00_INBOX"
        self.processed_path = self.base_path / "01_PROCESSED"
        self.categories_path = self.base_path / "02_CATEGORIES"
        self.db_path = self.base_path / "document_tracking.db"
        
        # Create directory structure
        self._setup_directories()
        self._setup_database()
        
    def _setup_directories(self):
        """Create the basic directory structure"""
        directories = [
            self.inbox_path,
            self.processed_path,
            self.categories_path / "FINANCIAL",
            self.categories_path / "MEDICAL",
            self.categories_path / "LEGAL",
            self.categories_path / "PERSONAL", 
            self.categories_path / "HOUSEHOLD",
            self.categories_path / "UNKNOWN"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
        print(f"✅ Document structure ready at: {self.base_path}")
        
    def _setup_database(self):
        """Create simple tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT,
                original_path TEXT,
                current_path TEXT,
                category TEXT,
                processing_date TEXT,
                scan_source TEXT,
                status TEXT,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def process_inbox(self) -> List[Dict[str, Any]]:
        """Process any new documents in the inbox"""
        print("🔍 Checking inbox for new documents...")
        
        new_docs = []
        for file_path in self.inbox_path.glob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                doc_info = self._process_single_document(file_path)
                new_docs.append(doc_info)
                
        if not new_docs:
            print("📭 No new documents in inbox")
        else:
            print(f"📄 Processed {len(new_docs)} new documents")
            
        return new_docs
    
    def _process_single_document(self, file_path: Path) -> Dict[str, Any]:
        """Process a single document from inbox"""
        doc_id = f"DOC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_path.stem}"
        
        # Basic document analysis
        doc_info = {
            'id': doc_id,
            'filename': file_path.name,
            'original_path': str(file_path),
            'file_size': file_path.stat().st_size,
            'scan_source': self._detect_scan_source(file_path),
            'processing_date': datetime.now().isoformat(),
            'category': self._suggest_category(file_path),
            'status': 'PROCESSED'
        }
        
        # Move to processed folder
        processed_file = self.processed_path / file_path.name
        shutil.move(file_path, processed_file)
        doc_info['current_path'] = str(processed_file)
        
        # Save to database
        self._save_document_record(doc_info)
        
        print(f"📋 Processed: {file_path.name} → Category: {doc_info['category']}")
        
        return doc_info
    
    def _detect_scan_source(self, file_path: Path) -> str:
        """Detect which scanning app/device was used"""
        filename = file_path.name.lower()
        
        if 'genius' in filename or 'scan' in filename:
            return 'GENIUS_SCAN'
        elif 'cam' in filename:
            return 'CAMERA_APP'
        elif 'bizhub' in filename:
            return 'BIZHUB_PRINTER'
        elif 'epson' in filename:
            return 'EPSON_PRINTER'
        else:
            return 'UNKNOWN'
    
    def _suggest_category(self, file_path: Path) -> str:
        """Simple category suggestion based on filename patterns"""
        filename = file_path.name.lower()
        
        # Financial keywords
        financial_keywords = ['bank', 'statement', 'receipt', 'invoice', 'tax', 'bill', 'payment']
        if any(keyword in filename for keyword in financial_keywords):
            return 'FINANCIAL'
            
        # Medical keywords
        medical_keywords = ['medical', 'doctor', 'health', 'prescription', 'medicare']
        if any(keyword in filename for keyword in medical_keywords):
            return 'MEDICAL'
            
        # Legal keywords  
        legal_keywords = ['legal', 'contract', 'agreement', 'court', 'notice']
        if any(keyword in filename for keyword in legal_keywords):
            return 'LEGAL'
            
        # Household keywords
        household_keywords = ['utility', 'insurance', 'warranty', 'manual']
        if any(keyword in filename for keyword in household_keywords):
            return 'HOUSEHOLD'
            
        return 'UNKNOWN'
    
    def _save_document_record(self, doc_info: Dict[str, Any]):
        """Save document record to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO documents 
            (id, filename, original_path, current_path, category, processing_date, scan_source, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            doc_info['id'],
            doc_info['filename'], 
            doc_info['original_path'],
            doc_info['current_path'],
            doc_info['category'],
            doc_info['processing_date'],
            doc_info['scan_source'],
            doc_info['status'],
            ''  # notes
        ))
        
        conn.commit()
        conn.close()
    
    def categorize_document(self, doc_id: str, category: str, notes: str = "") -> bool:
        """Move document to specific category folder"""
        # Get document info
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            print(f"❌ Document {doc_id} not found")
            return False
            
        current_path = Path(result[3])  # current_path column
        category_path = self.categories_path / category.upper()
        
        if not category_path.exists():
            category_path.mkdir(parents=True)
            
        # Move file
        new_path = category_path / current_path.name
        shutil.move(current_path, new_path)
        
        # Update database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE documents 
            SET current_path = ?, category = ?, notes = ? 
            WHERE id = ?
        ''', (str(new_path), category.upper(), notes, doc_id))
        conn.commit()
        conn.close()
        
        print(f"📁 Moved {current_path.name} to {category.upper()}")
        return True
    
    def list_uncategorized(self) -> List[Dict[str, Any]]:
        """List documents needing categorization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE category = 'UNKNOWN' OR category IS NULL")
        results = cursor.fetchall()
        conn.close()
        
        uncategorized = []
        for row in results:
            uncategorized.append({
                'id': row[0],
                'filename': row[1],
                'current_path': row[3],
                'processing_date': row[5],
                'scan_source': row[6]
            })
            
        return uncategorized
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get processing status report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count by category
        cursor.execute("SELECT category, COUNT(*) FROM documents GROUP BY category")
        category_counts = dict(cursor.fetchall())
        
        # Count by scan source
        cursor.execute("SELECT scan_source, COUNT(*) FROM documents GROUP BY scan_source")
        source_counts = dict(cursor.fetchall())
        
        # Total documents
        cursor.execute("SELECT COUNT(*) FROM documents")
        total_docs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_documents': total_docs,
            'by_category': category_counts,
            'by_scan_source': source_counts,
            'inbox_count': len(list(self.inbox_path.glob("*"))),
            'uncategorized_count': category_counts.get('UNKNOWN', 0)
        }
    
    def suggest_next_actions(self) -> List[str]:
        """Suggest what Jeremy should do next"""
        suggestions = []
        
        # Check inbox
        inbox_files = list(self.inbox_path.glob("*"))
        if inbox_files:
            suggestions.append(f"📥 Process {len(inbox_files)} files in inbox")
            
        # Check uncategorized
        uncategorized = self.list_uncategorized()
        if uncategorized:
            suggestions.append(f"📋 Categorize {len(uncategorized)} documents")
            
        if not suggestions:
            suggestions.append("✅ All caught up! Ready for more documents from phone.")
            
        return suggestions

def main():
    """Interactive document processing session"""
    bridge = DocumentBridge()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║              Document Processing Bridge                      ║
║           Physical → Digital → Organized                    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Process any new documents
    new_docs = bridge.process_inbox()
    
    # Show status
    status = bridge.get_status_report()
    print(f"\n📊 STATUS REPORT")
    print(f"Total Documents: {status['total_documents']}")
    print(f"In Inbox: {status['inbox_count']}")
    print(f"Uncategorized: {status['uncategorized_count']}")
    
    print(f"\nBy Category:")
    for category, count in status['by_category'].items():
        print(f"  {category}: {count}")
    
    # Suggest next actions
    suggestions = bridge.suggest_next_actions()
    print(f"\n🎯 NEXT ACTIONS:")
    for suggestion in suggestions:
        print(f"  {suggestion}")
    
    # Show uncategorized for manual review
    uncategorized = bridge.list_uncategorized()
    if uncategorized:
        print(f"\n📋 UNCATEGORIZED DOCUMENTS:")
        for doc in uncategorized[:5]:  # Show first 5
            print(f"  {doc['id']}: {doc['filename']}")
        if len(uncategorized) > 5:
            print(f"  ... and {len(uncategorized) - 5} more")

if __name__ == "__main__":
    main()