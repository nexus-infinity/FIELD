#!/usr/bin/env python3
"""
FIELD Intelligence Ingestion Engine
ISO-Compliant Live Data Collection & Validation
Sacred Geometric Intelligence Architecture
"""

import asyncio
import hashlib
import json
import logging
import sqlite3
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiohttp
import requests
from dataclasses import dataclass
from enum import Enum

class DataSourcePriority(Enum):
    """Priority levels for data sources"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH" 
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class ValidationStatus(Enum):
    """Validation status for ingested records"""
    VALID = "VALID"
    TIMESTAMP_UNCERTAIN = "TIMESTAMP_UNCERTAIN"
    GEO_INCOMPLETE = "GEO_INCOMPLETE"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    INTEGRITY_FAILED = "INTEGRITY_FAILED"

@dataclass
class IngestedRecord:
    """ISO-compliant data record"""
    observed_at: str          # ISO 8601 timestamp from source
    source_id: str           # publisher:endpoint format
    where: str               # ISO 3166 location code
    sha256: str              # Payload integrity hash
    payload: Dict[str, Any]  # Original data
    ingested_at: str         # FIELD processing timestamp
    geo_metadata: Optional[Dict[str, Any]] = None
    validation_status: ValidationStatus = ValidationStatus.VALID
    completeness_score: float = 1.0

class FIELDIntelligenceEngine:
    """
    FIELD Intelligence Ingestion Engine
    
    Collects, validates, and archives live data from government and public sources
    following ISO standards for temporal, spatial, and integrity compliance.
    """
    
    def __init__(self, config_path: str = "data_sources_watchlist.yaml"):
        self.base_path = Path("/Users/jbear/FIELD/◎_source_core")
        self.config_path = self.base_path / config_path
        self.db_path = self.base_path / "intelligence_data.db"
        
        # Load configuration
        self.config = self._load_config()
        self.sources = self.config.get('sources', {})
        
        # Setup logging
        self._setup_logging()
        
        # Initialize database
        self._init_database()
        
        # Active sessions for async operations
        self.session = None
        
        self.logger.info("FIELD Intelligence Engine initialized")
    
    def _setup_logging(self):
        """Setup logging for intelligence operations"""
        log_file = self.base_path / "intelligence_engine.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('FIELDIntelligence')
    
    def _load_config(self) -> Dict[str, Any]:
        """Load data sources configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}
    
    def _init_database(self):
        """Initialize intelligence database with ISO-compliant schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main intelligence records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intelligence_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observed_at TEXT NOT NULL,
                source_id TEXT NOT NULL,
                where_iso TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                payload TEXT NOT NULL,
                ingested_at TEXT NOT NULL,
                geo_metadata TEXT,
                validation_status TEXT DEFAULT 'VALID',
                completeness_score REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Source monitoring table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS source_monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL,
                last_successful_fetch TEXT,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 1.0,
                last_error TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Quality metrics table  
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quality_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_date DATE,
                total_records INTEGER,
                valid_records INTEGER,
                validation_rate REAL,
                avg_completeness_score REAL,
                integrity_failures INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self.logger.info("Intelligence database initialized")
    
    def validate_record(self, raw_data: Dict[str, Any], source_config: Dict[str, Any]) -> IngestedRecord:
        """Validate and normalize incoming data to ISO standards"""
        validation_status = ValidationStatus.VALID
        completeness_score = 1.0
        
        # Extract or generate required fields
        observed_at = raw_data.get('timestamp', datetime.utcnow().isoformat())
        source_id = source_config['source_id']
        where = source_config['location']
        
        # Calculate payload hash for integrity
        payload_str = json.dumps(raw_data, sort_keys=True)
        sha256_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        
        # Validate ISO 8601 timestamp
        try:
            datetime.fromisoformat(observed_at.replace('Z', '+00:00'))
        except ValueError:
            validation_status = ValidationStatus.TIMESTAMP_UNCERTAIN
            completeness_score *= 0.8
            self.logger.warning(f"Invalid timestamp format: {observed_at}")
        
        # Check geospatial metadata completeness
        geo_metadata = raw_data.get('geo_metadata')
        if source_config.get('iso_standard') == 'ISO 19115-1' and not geo_metadata:
            validation_status = ValidationStatus.GEO_INCOMPLETE
            completeness_score *= 0.9
        
        return IngestedRecord(
            observed_at=observed_at,
            source_id=source_id,
            where=where,
            sha256=sha256_hash,
            payload=raw_data,
            ingested_at=datetime.utcnow().isoformat(),
            geo_metadata=geo_metadata,
            validation_status=validation_status,
            completeness_score=completeness_score
        )
    
    def store_record(self, record: IngestedRecord) -> bool:
        """Store validated record in intelligence database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO intelligence_records 
                (observed_at, source_id, where_iso, sha256, payload, ingested_at, 
                 geo_metadata, validation_status, completeness_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record.observed_at,
                record.source_id,
                record.where,
                record.sha256,
                json.dumps(record.payload),
                record.ingested_at,
                json.dumps(record.geo_metadata) if record.geo_metadata else None,
                record.validation_status.value,
                record.completeness_score
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Stored record from {record.source_id} with validation {record.validation_status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store record: {e}")
            return False
    
    async def fetch_source_data(self, source_id: str, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch data from a configured source"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            base_url = source_config['base_url']
            timeout = self.config.get('pipeline', {}).get('timeout_seconds', 30)
            
            async with self.session.get(base_url, timeout=timeout) as response:
                if response.status == 200:
                    # For now, return a mock successful fetch
                    # In production, this would parse HTML/JSON/XML based on source
                    self.logger.info(f"Successfully fetched from {source_id}")
                    self._update_source_monitoring(source_id, success=True)
                    
                    return [{
                        'timestamp': datetime.utcnow().isoformat(),
                        'content': f"Mock data from {source_id}",
                        'url': base_url
                    }]
                else:
                    self.logger.warning(f"HTTP {response.status} from {source_id}")
                    self._update_source_monitoring(source_id, success=False, error=f"HTTP {response.status}")
                    return []
                    
        except Exception as e:
            self.logger.error(f"Failed to fetch from {source_id}: {e}")
            self._update_source_monitoring(source_id, success=False, error=str(e))
            return []
    
    def _update_source_monitoring(self, source_id: str, success: bool, error: str = None):
        """Update source monitoring metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get existing metrics
            cursor.execute('''
                SELECT success_count, failure_count FROM source_monitoring 
                WHERE source_id = ?
            ''', (source_id,))
            result = cursor.fetchone()
            
            if result:
                success_count, failure_count = result
                if success:
                    success_count += 1
                    last_successful_fetch = datetime.utcnow().isoformat()
                else:
                    failure_count += 1
                    last_successful_fetch = None
                
                success_rate = success_count / (success_count + failure_count)
                
                cursor.execute('''
                    UPDATE source_monitoring 
                    SET success_count = ?, failure_count = ?, success_rate = ?, 
                        last_successful_fetch = COALESCE(?, last_successful_fetch),
                        last_error = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE source_id = ?
                ''', (success_count, failure_count, success_rate, last_successful_fetch, error, source_id))
            else:
                # Insert new monitoring record
                success_count = 1 if success else 0
                failure_count = 0 if success else 1
                success_rate = 1.0 if success else 0.0
                last_successful_fetch = datetime.utcnow().isoformat() if success else None
                
                cursor.execute('''
                    INSERT INTO source_monitoring 
                    (source_id, success_count, failure_count, success_rate, 
                     last_successful_fetch, last_error)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (source_id, success_count, failure_count, success_rate, 
                      last_successful_fetch, error))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to update monitoring for {source_id}: {e}")
    
    async def run_collection_cycle(self):
        """Run a single collection cycle across all sources"""
        self.logger.info("Starting intelligence collection cycle")
        
        total_records = 0
        valid_records = 0
        
        for source_id, source_config in self.sources.items():
            priority = source_config.get('priority', 'MEDIUM')
            
            try:
                # Fetch raw data
                raw_data_list = await self.fetch_source_data(source_id, source_config)
                
                # Process each record
                for raw_data in raw_data_list:
                    total_records += 1
                    
                    # Validate and normalize
                    record = self.validate_record(raw_data, source_config)
                    
                    if record.validation_status in [ValidationStatus.VALID, ValidationStatus.TIMESTAMP_UNCERTAIN, ValidationStatus.GEO_INCOMPLETE]:
                        # Store valid/recoverable records
                        if self.store_record(record):
                            valid_records += 1
                    else:
                        self.logger.warning(f"Rejected record from {source_id}: {record.validation_status}")
                        
            except Exception as e:
                self.logger.error(f"Collection failed for {source_id}: {e}")
        
        # Update daily quality metrics
        self._update_quality_metrics(total_records, valid_records)
        
        self.logger.info(f"Collection cycle complete: {valid_records}/{total_records} records processed")
    
    def _update_quality_metrics(self, total_records: int, valid_records: int):
        """Update daily quality metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.utcnow().date().isoformat()
            validation_rate = valid_records / max(total_records, 1)
            
            # Get average completeness score for today
            cursor.execute('''
                SELECT AVG(completeness_score) FROM intelligence_records 
                WHERE DATE(ingested_at) = ?
            ''', (today,))
            avg_completeness = cursor.fetchone()[0] or 1.0
            
            # Get integrity failure count
            cursor.execute('''
                SELECT COUNT(*) FROM intelligence_records 
                WHERE validation_status = 'INTEGRITY_FAILED' AND DATE(ingested_at) = ?
            ''', (today,))
            integrity_failures = cursor.fetchone()[0] or 0
            
            # Insert or update quality metrics
            cursor.execute('''
                INSERT OR REPLACE INTO quality_metrics 
                (metric_date, total_records, valid_records, validation_rate, 
                 avg_completeness_score, integrity_failures)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (today, total_records, valid_records, validation_rate, 
                  avg_completeness, integrity_failures))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to update quality metrics: {e}")
    
    def get_intelligence_summary(self) -> Dict[str, Any]:
        """Get summary of intelligence collection status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total records
            cursor.execute("SELECT COUNT(*) FROM intelligence_records")
            total_records = cursor.fetchone()[0]
            
            # Records by validation status
            cursor.execute('''
                SELECT validation_status, COUNT(*) 
                FROM intelligence_records 
                GROUP BY validation_status
            ''')
            validation_breakdown = dict(cursor.fetchall())
            
            # Source performance
            cursor.execute('''
                SELECT source_id, success_rate, last_successful_fetch 
                FROM source_monitoring 
                ORDER BY success_rate DESC
            ''')
            source_performance = cursor.fetchall()
            
            # Recent quality metrics
            cursor.execute('''
                SELECT * FROM quality_metrics 
                ORDER BY metric_date DESC 
                LIMIT 7
            ''')
            recent_quality = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_records': total_records,
                'validation_breakdown': validation_breakdown,
                'source_performance': source_performance,
                'recent_quality_trends': recent_quality
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate summary: {e}")
            return {}
    
    async def close(self):
        """Clean shutdown"""
        if self.session:
            await self.session.close()
        self.logger.info("FIELD Intelligence Engine shut down")

async def main():
    """Test run of the intelligence engine"""
    engine = FIELDIntelligenceEngine()
    
    try:
        # Run a collection cycle
        await engine.run_collection_cycle()
        
        # Display summary
        summary = engine.get_intelligence_summary()
        print("\n" + "="*60)
        print("FIELD INTELLIGENCE SUMMARY")
        print("="*60)
        print(f"Total Records: {summary.get('total_records', 0)}")
        print(f"Validation Breakdown: {summary.get('validation_breakdown', {})}")
        print("\nSource Performance:")
        for source_id, success_rate, last_fetch in summary.get('source_performance', []):
            print(f"  {source_id}: {success_rate:.2%} success rate, last: {last_fetch}")
            
    finally:
        await engine.close()

if __name__ == "__main__":
    asyncio.run(main())