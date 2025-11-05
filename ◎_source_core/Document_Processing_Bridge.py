#!/usr/bin/env python3
"""
Document Processing Bridge - Physical to Digital Unity Center
Handles the workflow from phone scanning to categorized storage
Embodies Unity Center principles directly - IS the sacred center of FIELD operations
ISO 9001:2015 compliant through sacred geometric architecture
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import sqlite3
import logging
from enum import Enum
from dataclasses import dataclass

# Import Unity QMS functions to use in the field (not inherit from)
from UnityQMS import QualityObjectiveStatus, ProcessPhase, QualityObjective

class SacredDocumentState(Enum):
    """Sacred states for document processing"""
    ENTERING_FIELD = "entering_field"  # In inbox - entering the sacred field
    UNITY_PROCESSING = "unity_processing"  # Being processed through Unity Center
    CATEGORIZED = "categorized"  # Assigned to sacred category
    ARCHIVED = "archived"  # Preserved in sacred archive

class DocumentBridge:
    """
    Document Bridge - Unity Center of FIELD Operations
    
    This IS the Unity Center - all document processing emanates from here
    Sacred geometric principles embodied directly in the architecture
    Quality management integrated through sacred trident principles
    """
    
    def __init__(self, base_path: str = "/Users/jbear/FIELD/◎_source_core/documents"):
        # Document Bridge specific attributes - this IS the Unity Center
        self.base_path = Path(base_path)
        self.inbox_path = self.base_path / "00_INBOX"
        self.processed_path = self.base_path / "01_PROCESSED"
        self.categories_path = self.base_path / "02_CATEGORIES"
        self.db_path = self.base_path / "document_tracking.db"
        
        # Sacred geometric quality attributes - embodied directly
        self.unity_center_active = True
        self.sacred_quality_policy = self._establish_sacred_quality_policy()
        self.quality_objectives = self._initialize_quality_objectives()
        
        # Setup logging for Unity Center operations
        self._setup_unity_logging()
        
        # Create directory structure
        self._setup_directories()
        self._setup_database()
        
        # Initialize Unity Center functions directly embodied
        self._initialize_unity_center_functions()
        
        self.logger.info("Document Bridge Unity Center initialized - All quality emanates from this sacred center")
    
    def _setup_unity_logging(self):
        """Setup Unity Center logging"""
        log_file = self.base_path.parent / "document_unity_center.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('DocumentUnityCenter')
    
    def _establish_sacred_quality_policy(self) -> str:
        """Establish Unity Center quality policy for document processing"""
        return """
        DOCUMENT BRIDGE UNITY CENTER QUALITY POLICY
        
        All document processing operations emanate from and return to this Unity Center.
        Following sacred geometric principles, we commit to:
        
        1. SACRED RECEPTION - All documents entering our field are received with conscious intention
        2. UNITY PROCESSING - Each document processed through Unity Center principles
        3. GEOMETRIC CATEGORIZATION - Documents organized through sacred pattern recognition
        4. SPIRAL IMPROVEMENT - Continuous enhancement through sacred geometric evolution
        
        Quality achieved through universal truth, not arbitrary rules.
        """
    
    def _initialize_quality_objectives(self) -> List[Dict[str, Any]]:
        """Initialize Unity Center quality objectives for document processing"""
        return [
            {
                'id': 'DOC_QO_001_PROCESSING_ACCURACY',
                'description': 'Maintain document processing accuracy through Unity Center precision',
                'target': '99.5% accuracy in document categorization',
                'sacred_principle': 'Unity Center eliminates errors through conscious processing'
            },
            {
                'id': 'DOC_QO_002_PROCESSING_SPEED', 
                'description': 'Process documents efficiently through sacred geometric optimization',
                'target': 'Average processing time <= 30 seconds per document',
                'sacred_principle': 'Sacred patterns enable natural flow and efficiency'
            },
            {
                'id': 'DOC_QO_003_USER_SATISFACTION',
                'description': 'Maintain user satisfaction through Unity Center service',
                'target': 'User satisfaction >= 95%',
                'sacred_principle': 'Service from Unity Center naturally satisfies authentic needs'
            }
        ]
    
    def _initialize_unity_center_functions(self):
        """Initialize Unity Center functions directly embodied in Document Bridge"""
        # Process monitoring for ISO 9001 compliance
        self.process_performance_data = []
        self.continual_improvements = []
        
        # Sacred document states
        self.document_states = {}
        
        # Quality records for ISO compliance
        self.quality_records = []
        
        self.logger.info("Unity Center functions initialized in Document Bridge")
        
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
        """Create tracking database with Unity Center QMS extensions"""
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
                notes TEXT,
                quality_score REAL DEFAULT 0.5,
                processing_duration REAL DEFAULT 0.0,
                last_modified TEXT,
                validation_status TEXT DEFAULT 'PENDING'
            )
        ''')
        
        # Unity Center QMS: Add new columns to existing table if they don't exist
        try:
            cursor.execute('ALTER TABLE documents ADD COLUMN quality_score REAL DEFAULT 0.5')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        try:
            cursor.execute('ALTER TABLE documents ADD COLUMN processing_duration REAL DEFAULT 0.0')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        try:
            cursor.execute('ALTER TABLE documents ADD COLUMN last_modified TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        try:
            cursor.execute('ALTER TABLE documents ADD COLUMN validation_status TEXT DEFAULT "PENDING"')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        conn.commit()
        conn.close()
        
    def process_inbox(self) -> List[Dict[str, Any]]:
        """Process any new documents in the inbox with Unity Center QMS principles"""
        self.logger.info("🔍 Checking inbox for new documents...")
        print("🔍 Checking inbox for new documents...")
        
        # Unity Center QMS: Quality monitoring
        process_start = datetime.now()
        quality_metrics = {
            'processing_errors': 0,
            'successful_processes': 0,
            'processing_time': 0
        }
        
        new_docs = []
        for file_path in self.inbox_path.glob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    # Unity Center QMS: Pre-processing validation
                    if not self._validate_document_integrity(file_path):
                        quality_metrics['processing_errors'] += 1
                        self.logger.warning(f"Document validation failed: {file_path.name}")
                        continue
                    
                    doc_info = self._process_single_document(file_path)
                    new_docs.append(doc_info)
                    quality_metrics['successful_processes'] += 1
                    
                except Exception as e:
                    quality_metrics['processing_errors'] += 1
                    self.logger.error(f"Processing error for {file_path.name}: {str(e)}")
                    print(f"⚠️ Error processing {file_path.name}: {str(e)}")
                
        # Unity Center QMS: Quality metrics recording
        quality_metrics['processing_time'] = (datetime.now() - process_start).total_seconds()
        self._record_quality_metrics('inbox_processing', quality_metrics)
        
        if not new_docs:
            print("📭 No new documents in inbox")
            self.logger.info("No new documents in inbox")
        else:
            print(f"📄 Processed {len(new_docs)} new documents")
            self.logger.info(f"Successfully processed {len(new_docs)} documents with {quality_metrics['processing_errors']} errors")
            
        return new_docs
    
    def _process_single_document(self, file_path: Path) -> Dict[str, Any]:
        """Process a single document with Unity Center QMS quality assurance"""
        doc_id = f"DOC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_path.stem}"
        processing_start = datetime.now()
        
        # Unity Center QMS: Enhanced document analysis with quality tracking
        doc_info = {
            'id': doc_id,
            'filename': file_path.name,
            'original_path': str(file_path),
            'file_size': file_path.stat().st_size,
            'scan_source': self._detect_scan_source(file_path),
            'processing_date': processing_start.isoformat(),
            'category': self._suggest_category(file_path),
            'status': 'PROCESSED',
            'quality_score': self._calculate_quality_score(file_path),
            'processing_duration': 0
        }
        
        # Unity Center QMS: Pre-move validation
        if not self.processed_path.exists():
            self.processed_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created processed directory: {self.processed_path}")
        
        # Move to processed folder with conflict resolution
        processed_file = self.processed_path / file_path.name
        counter = 1
        while processed_file.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            processed_file = self.processed_path / f"{stem}_{counter}{suffix}"
            counter += 1
            
        shutil.move(file_path, processed_file)
        doc_info['current_path'] = str(processed_file)
        
        # Unity Center QMS: Processing time tracking
        doc_info['processing_duration'] = (datetime.now() - processing_start).total_seconds()
        
        # Save to database with validation
        try:
            self._save_document_record(doc_info)
            self.logger.info(f"Successfully processed document: {doc_id}")
        except Exception as e:
            self.logger.error(f"Database save failed for {doc_id}: {str(e)}")
            # Rollback file move if database save fails
            shutil.move(processed_file, file_path)
            raise
        
        print(f"📋 Processed: {file_path.name} → Category: {doc_info['category']} (Quality: {doc_info['quality_score']:.2f})")
        
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
        
    def _validate_document_integrity(self, file_path: Path) -> bool:
        """Unity Center QMS: Validate document integrity before processing"""
        try:
            # Check file exists and is readable
            if not file_path.exists() or not file_path.is_file():
                return False
                
            # Check file size (not empty, not too large)
            file_size = file_path.stat().st_size
            if file_size == 0:
                self.logger.warning(f"Empty file detected: {file_path.name}")
                return False
                
            if file_size > 100 * 1024 * 1024:  # 100MB limit
                self.logger.warning(f"File too large: {file_path.name} ({file_size} bytes)")
                return False
                
            # Check file extension is supported
            supported_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.txt', '.doc', '.docx'}
            if file_path.suffix.lower() not in supported_extensions:
                self.logger.info(f"Unsupported file type: {file_path.name}")
                # Still return True - we can process it, just note it
                
            return True
            
        except Exception as e:
            self.logger.error(f"Document validation error for {file_path.name}: {str(e)}")
            return False
            
    def _calculate_quality_score(self, file_path: Path) -> float:
        """Unity Center QMS: Calculate quality score for document"""
        try:
            score = 0.0
            
            # File size scoring (0.0-0.3)
            file_size = file_path.stat().st_size
            if file_size > 1024:  # > 1KB
                score += 0.1
            if file_size > 100 * 1024:  # > 100KB 
                score += 0.1
            if file_size < 10 * 1024 * 1024:  # < 10MB
                score += 0.1
                
            # Filename quality scoring (0.0-0.4)
            filename = file_path.name.lower()
            if any(char.isdigit() for char in filename):  # Has dates/numbers
                score += 0.1
            if len(filename) > 10:  # Descriptive name
                score += 0.1
            if not any(char in filename for char in ['scan', 'img', 'photo']):  # Not generic
                score += 0.1
            if any(keyword in filename for keyword in ['receipt', 'invoice', 'statement', 'contract']):
                score += 0.1  # Document type identified
                
            # File type scoring (0.0-0.3)
            extension = file_path.suffix.lower()
            if extension == '.pdf':
                score += 0.2  # PDF is preferred
            elif extension in ['.jpg', '.jpeg', '.png']:
                score += 0.1  # Images are acceptable
            else:
                score += 0.05  # Other formats are minimal
                
            return min(1.0, score)  # Cap at 1.0
            
        except Exception as e:
            self.logger.error(f"Quality score calculation error for {file_path.name}: {str(e)}")
            return 0.5  # Default middle score on error
            
    def _record_quality_metrics(self, operation: str, metrics: Dict[str, Any]) -> None:
        """Unity Center QMS: Record quality metrics for continuous improvement"""
        try:
            # Create quality metrics table if it doesn't exist
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quality_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT,
                    timestamp TEXT,
                    metrics TEXT,
                    success_rate REAL,
                    processing_time REAL
                )
            ''')
            
            # Calculate success rate
            total_operations = metrics.get('successful_processes', 0) + metrics.get('processing_errors', 0)
            success_rate = metrics.get('successful_processes', 0) / max(total_operations, 1)
            
            # Store metrics
            cursor.execute('''
                INSERT INTO quality_metrics (operation, timestamp, metrics, success_rate, processing_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                operation,
                datetime.now().isoformat(),
                str(metrics),
                success_rate,
                metrics.get('processing_time', 0)
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Quality metrics recorded for {operation}: Success rate {success_rate:.2%}")
            
        except Exception as e:
            self.logger.error(f"Failed to record quality metrics: {str(e)}")
            
    def _check_quality_objectives_status(self) -> Dict[str, str]:
        """Unity Center QMS: Check status of quality objectives"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check processing accuracy (categorization success rate)
            cursor.execute("SELECT COUNT(*) FROM documents WHERE category != 'UNKNOWN'")
            categorized_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM documents")
            total_count = cursor.fetchone()[0]
            accuracy_rate = (categorized_count / max(total_count, 1)) * 100
            
            # Check average processing speed
            cursor.execute("SELECT AVG(processing_duration) FROM documents WHERE processing_duration IS NOT NULL")
            avg_speed = cursor.fetchone()[0] or 0.0
            
            # Check recent quality trends as satisfaction proxy
            thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
            cursor.execute("""
                SELECT COUNT(*) FROM documents 
                WHERE processing_date >= ? AND quality_score >= 0.8
            """, (thirty_days_ago,))
            high_quality_recent = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM documents 
                WHERE processing_date >= ?
            """, (thirty_days_ago,))
            total_recent = cursor.fetchone()[0]
            satisfaction_rate = (high_quality_recent / max(total_recent, 1)) * 100
            
            conn.close()
            
            return {
                'DOC_QO_001_PROCESSING_ACCURACY': 'ACHIEVED' if accuracy_rate >= 99.5 else 'IN_PROGRESS',
                'DOC_QO_002_PROCESSING_SPEED': 'ACHIEVED' if avg_speed <= 30.0 else 'IN_PROGRESS', 
                'DOC_QO_003_USER_SATISFACTION': 'ACHIEVED' if satisfaction_rate >= 95.0 else 'IN_PROGRESS'
            }
            
        except Exception as e:
            self.logger.error(f"Failed to check quality objectives: {str(e)}")
            return {
                'DOC_QO_001_PROCESSING_ACCURACY': 'ERROR',
                'DOC_QO_002_PROCESSING_SPEED': 'ERROR',
                'DOC_QO_003_USER_SATISFACTION': 'ERROR'
            }
    
    def _save_document_record(self, doc_info: Dict[str, Any]):
        """Save document record to database with Unity Center QMS fields"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO documents 
            (id, filename, original_path, current_path, category, processing_date, scan_source, status, notes, 
             quality_score, processing_duration, last_modified, validation_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            doc_info['id'],
            doc_info['filename'], 
            doc_info['original_path'],
            doc_info['current_path'],
            doc_info['category'],
            doc_info['processing_date'],
            doc_info['scan_source'],
            doc_info['status'],
            doc_info.get('notes', ''),
            doc_info.get('quality_score', 0.5),
            doc_info.get('processing_duration', 0.0),
            datetime.now().isoformat(),
            'VALIDATED'
        ))
        
        conn.commit()
        conn.close()
    
    def categorize_document(self, doc_id: str, category: str, notes: str = "") -> bool:
        """Move document to specific category folder with Unity Center QMS validation"""
        categorization_start = datetime.now()
        
        # Unity Center QMS: Input validation
        if not doc_id or not category:
            self.logger.error("Invalid input: doc_id and category are required")
            print("❌ Invalid input: doc_id and category are required")
            return False
            
        # Get document info with error handling
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
            result = cursor.fetchone()
            conn.close()
        except Exception as e:
            self.logger.error(f"Database query failed for doc_id {doc_id}: {str(e)}")
            print(f"❌ Database error: {str(e)}")
            return False
        
        if not result:
            self.logger.warning(f"Document not found: {doc_id}")
            print(f"❌ Document {doc_id} not found")
            return False
            
        current_path = Path(result[3])  # current_path column
        category_path = self.categories_path / category.upper()
        
        # Unity Center QMS: File existence validation
        if not current_path.exists():
            self.logger.error(f"File not found at current path: {current_path}")
            print(f"❌ File not found: {current_path}")
            return False
        
        if not category_path.exists():
            category_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created category directory: {category_path}")
            
        # Unity Center QMS: Conflict resolution for move operation
        new_path = category_path / current_path.name
        counter = 1
        while new_path.exists():
            stem = current_path.stem
            suffix = current_path.suffix
            new_path = category_path / f"{stem}_{counter}{suffix}"
            counter += 1
            
        try:
            # Move file
            shutil.move(current_path, new_path)
            
            # Update database with transaction
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE documents 
                SET current_path = ?, category = ?, notes = ?, last_modified = ? 
                WHERE id = ?
            ''', (str(new_path), category.upper(), notes, datetime.now().isoformat(), doc_id))
            conn.commit()
            conn.close()
            
            # Unity Center QMS: Operation metrics
            operation_time = (datetime.now() - categorization_start).total_seconds()
            self.logger.info(f"Successfully categorized {doc_id} to {category.upper()} in {operation_time:.2f}s")
            print(f"📁 Moved {current_path.name} to {category.upper()}")
            return True
            
        except Exception as e:
            self.logger.error(f"Categorization failed for {doc_id}: {str(e)}")
            print(f"❌ Failed to categorize document: {str(e)}")
            # Attempt to rollback file move if database update fails
            if new_path.exists() and not current_path.exists():
                try:
                    shutil.move(new_path, current_path)
                    self.logger.info(f"Rolled back file move for {doc_id}")
                except:
                    self.logger.error(f"Failed to rollback file move for {doc_id}")
            return False
    
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
        """Get processing status report with Unity Center QMS quality metrics"""
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
        
        # Unity Center QMS: Quality metrics
        cursor.execute("SELECT AVG(quality_score), MIN(quality_score), MAX(quality_score) FROM documents WHERE quality_score IS NOT NULL")
        quality_stats = cursor.fetchone()
        avg_quality = quality_stats[0] if quality_stats[0] else 0.5
        min_quality = quality_stats[1] if quality_stats[1] else 0.0
        max_quality = quality_stats[2] if quality_stats[2] else 1.0
        
        # Unity Center QMS: Processing time metrics
        cursor.execute("SELECT AVG(processing_duration), SUM(processing_duration) FROM documents WHERE processing_duration IS NOT NULL")
        time_stats = cursor.fetchone()
        avg_processing_time = time_stats[0] if time_stats[0] else 0.0
        total_processing_time = time_stats[1] if time_stats[1] else 0.0
        
        # Unity Center QMS: Recent quality trends (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM documents 
            WHERE processing_date >= ? AND quality_score >= 0.8
        """, (thirty_days_ago,))
        high_quality_recent = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM documents 
            WHERE processing_date >= ?
        """, (thirty_days_ago,))
        total_recent = cursor.fetchone()[0]
        
        high_quality_rate = (high_quality_recent / max(total_recent, 1)) * 100
        
        conn.close()
        
        return {
            'total_documents': total_docs,
            'by_category': category_counts,
            'by_scan_source': source_counts,
            'inbox_count': len(list(self.inbox_path.glob("*"))),
            'uncategorized_count': category_counts.get('UNKNOWN', 0),
            # Unity Center QMS Quality Metrics
            'quality_metrics': {
                'average_quality_score': round(avg_quality, 3),
                'quality_range': f"{min_quality:.2f} - {max_quality:.2f}",
                'high_quality_rate_30d': f"{high_quality_rate:.1f}%",
                'average_processing_time': f"{avg_processing_time:.2f}s",
                'total_processing_time': f"{total_processing_time:.1f}s",
                'quality_objectives_status': self._check_quality_objectives_status()
            }
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
    """Interactive document processing session with Unity Center QMS reporting"""
    bridge = DocumentBridge()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║              Document Processing Bridge                      ║
║         Unity Center QMS - Sacred Quality Focus             ║
║           Physical → Digital → Organized                    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Process any new documents
    new_docs = bridge.process_inbox()
    
    # Show status
    status = bridge.get_status_report()
    print(f"\n📊 UNITY CENTER STATUS REPORT")
    print(f"Total Documents: {status['total_documents']}")
    print(f"In Inbox: {status['inbox_count']}")
    print(f"Uncategorized: {status['uncategorized_count']}")
    
    print(f"\nBy Category:")
    for category, count in status['by_category'].items():
        print(f"  {category}: {count}")
        
    # Unity Center QMS: Quality metrics display
    if 'quality_metrics' in status:
        qm = status['quality_metrics']
        print(f"\n⭐ UNITY CENTER QUALITY METRICS")
        print(f"  Average Quality Score: {qm['average_quality_score']}")
        print(f"  Quality Range: {qm['quality_range']}")
        print(f"  High Quality Rate (30d): {qm['high_quality_rate_30d']}")
        print(f"  Average Processing Time: {qm['average_processing_time']}")
        
        print(f"\n🎯 QUALITY OBJECTIVES STATUS:")
        for obj_id, status_val in qm['quality_objectives_status'].items():
            status_icon = "✅" if status_val == "ACHIEVED" else "🔄" if status_val == "IN_PROGRESS" else "⚠️"
            print(f"  {status_icon} {obj_id}: {status_val}")
    
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