#!/usr/bin/env python3
"""
JBR New Schema Integration with Database Stripper
Maps JBR hierarchical schema to tetrahedral FIELD geometry
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from akron_sovereign_integration import AkronSovereignRepository, DataPurity

class JBRSchemaMapper:
    """Maps JBR New schema to FIELD tetrahedral geometry"""
    
    def __init__(self):
        self.schema_mapping = {
            # Sacred FIELD (Above) Tetrahedron
            'TATA': [  # Truth/Temporal
                'Legal Documents', 'Trust Deeds', 'Financial Records', 
                'Meeting Minutes', 'Incorporation Documents', 'Trust Accounts'
            ],
            'ATLAS': [  # Intelligence/Mapping  
                'Asset Management', 'Site Plans', 'Investment Reports',
                'Property Records', 'Land Ownership Documents', 'Inventory Management'
            ],
            'OBI_WAN': [  # Observer/Memory
                'Correspondence', 'Gmail_Account_Emails', 'Google_Vault_Records',
                'Documents', 'Bank Statements', 'Transactions'
            ],
            'DOJO': [  # Manifestation/Action
                'Operations', 'Project A', 'Project B', 'Crop Management',
                'Walkerville Vineyard', 'Supplier Information'
            ],
            
            # FIELD-LIVING (Below) Mirror Tetrahedron  
            'AKRON': [  # Sovereignty
                'Personal Information', 'Personal Documents', 'Private Asset Management',
                'Switzerland Assets', 'Directors', 'Shareholders'
            ],
            'FIELD_DEV': [  # Development
                'MYOB_Files', 'Excel_Spreadsheets', 'Budgets and Financial Statements',
                'Accounting Records'
            ],
            'FIELD_OOWL': [  # Wisdom
                'Medical Records', 'Beneficiary Information', 'Art and Chattels',
                'POA for Centosa'
            ]
        }
        
    def classify_data(self, data_category: str) -> str:
        """Classify JBR data into tetrahedral position"""
        for position, categories in self.schema_mapping.items():
            if any(cat.lower() in data_category.lower() for cat in categories):
                return position
        return 'AKRON'  # Default to sovereign storage

class JBRDataProcessor:
    """Process actual JBR data through Database Stripper"""
    
    def __init__(self):
        self.repo = AkronSovereignRepository()
        self.mapper = JBRSchemaMapper() 
        self.documents_path = Path.home() / "Documents"
        
    def scan_documents_folder(self) -> List[Dict]:
        """Scan ~/Documents for JBR structured data"""
        documents = []
        
        for file_path in self.documents_path.glob("**/*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                # Extract temporal info from filename
                file_info = {
                    'path': str(file_path),
                    'name': file_path.name,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'category': self._classify_document(file_path.name),
                    'tetrahedral_position': None
                }
                
                # Map to tetrahedral geometry
                file_info['tetrahedral_position'] = self.mapper.classify_data(
                    file_info['category']
                )
                
                documents.append(file_info)
                
        return documents
    
    def _classify_document(self, filename: str) -> str:
        """Classify document based on filename patterns"""
        filename_lower = filename.lower()
        
        # Temporal classification from filename patterns
        if 'email' in filename_lower:
            return 'Correspondence'
        elif any(x in filename_lower for x in ['bank', 'statement', 'transaction']):
            return 'Bank Statements'  
        elif any(x in filename_lower for x in ['legal', 'contract', 'agreement']):
            return 'Legal Documents'
        elif any(x in filename_lower for x in ['financial', 'invoice', 'receipt']):
            return 'Financial Records'
        elif any(x in filename_lower for x in ['property', 'deed', 'title']):
            return 'Property Records'
        else:
            return 'Documents'
    
    def process_jbr_data(self):
        """Process JBR data through Database Stripper with geometric alignment"""
        print("🔺 Starting JBR New Schema Integration")
        print("="*50)
        
        # Scan documents
        documents = self.scan_documents_folder()
        print(f"📂 Found {len(documents)} documents for processing")
        
        # Group by tetrahedral position
        tetrahedral_groups = {}
        for doc in documents:
            position = doc['tetrahedral_position']
            if position not in tetrahedral_groups:
                tetrahedral_groups[position] = []
            tetrahedral_groups[position].append(doc)
        
        # Process through Database Stripper by tetrahedral position
        for position, docs in tetrahedral_groups.items():
            print(f"\n{self._get_position_symbol(position)} {position}: {len(docs)} documents")
            
            # Create transaction for each document group
            transaction = {
                'id': hashlib.md5(f"{position}_{datetime.now().isoformat()}".encode()).hexdigest(),
                'context': position.lower(),
                'data': {
                    'tetrahedral_position': position,
                    'document_count': len(docs),
                    'total_size': sum(doc['size'] for doc in docs),
                    'categories': list(set(doc['category'] for doc in docs)),
                    'documents': docs[:10]  # Sample of documents
                },
                'timestamp': datetime.now().isoformat(),
                'schema_version': 'JBR_NEW_v1.0'
            }
            
            # Add to blockchain processing queue
            self.repo.blockchain.add_transaction(transaction)
            
        # Process blockchain with strippers
        print("\n⛓️  Processing through Database Stripper blockchain...")
        processed_blocks = 0
        while not self.repo.blockchain.pending_transactions.empty():
            block = self.repo.blockchain.process_block()
            if block:
                processed_blocks += 1
                alignment = block.get('symbolic_alignment', '⟡')
                print(f"   Block {block['index']}: {alignment} ({len(block['transactions'])} transactions)")
                
                # Persist processed data to sovereign repository
                self._persist_block_data(block)
        
        print(f"\n✅ Processed {processed_blocks} blocks through double tetrahedron")
        
        # Show final metrics
        self.repo.print_metrics()
        
        # Validate data flow integrity
        self._validate_semantic_alignment()
        
    def _persist_block_data(self, block: Dict):
        """Persist processed block data to sovereign repository"""
        for transaction in block['transactions']:
            data = transaction['data']
            
            # Create sovereign data entry
            sovereign_entry = {
                'tetrahedral_position': data['tetrahedral_position'],
                'document_count': data['document_count'],
                'total_size': data['total_size'],
                'categories': data['categories'],
                'block_hash': block['hash'],
                'symbolic_alignment': block['symbolic_alignment'],
                'processing_timestamp': block['timestamp'],
                'schema_version': transaction.get('schema_version', 'JBR_NEW_v1.0')
            }
            
            # Store in repository with appropriate purity level
            purity = self._determine_data_purity(data['tetrahedral_position'])
            result = self.repo.ingest_data(
                sovereign_entry, 
                context=transaction['context'],
                purity=purity
            )
            
            if result:
                print(f"     💾 Persisted {data['document_count']} documents to {data['tetrahedral_position']}")
                
    def _determine_data_purity(self, position: str) -> DataPurity:
        """Determine data purity level based on tetrahedral position"""
        if position == 'AKRON':
            return DataPurity.IMMUTABLE  # Sovereign data is immutable
        elif position in ['TATA', 'ATLAS']:
            return DataPurity.SACRED  # Sacred FIELD manifestation
        elif position == 'OBI_WAN':
            return DataPurity.MIRROR_DECAY  # Living memory, temporary
        else:
            return DataPurity.EXPERIMENTAL  # Development/testing
            
    def _validate_semantic_alignment(self):
        """Validate OBI-WAN→TATA→ATLAS→DOJO semantic flow integrity"""
        print("\n🔍 Validating Semantic Alignment:")
        
        # Query processed data by tetrahedral position
        results = self.repo.query_sovereign_data({'access_level': 'archive_only'})
        
        position_counts = {}
        for record in results:
            content = json.loads(record['content']) if isinstance(record['content'], str) else record['content']
            pos = content.get('tetrahedral_position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1
            
        # Validate flow sequence
        flow_sequence = ['OBI_WAN', 'TATA', 'ATLAS', 'DOJO']
        print("   Sacred Flow Validation:")
        for pos in flow_sequence:
            count = position_counts.get(pos, 0)
            symbol = self._get_position_symbol(pos)
            status = "✅" if count > 0 else "⚠️"
            print(f"     {status} {symbol} {pos}: {count} records processed")
            
        # Test infinite potential extensibility
        total_records = len(results)
        print(f"\n🌟 Infinite Potential Test: {total_records} records maintain geometric integrity")
        
        return position_counts
        
    def _get_position_symbol(self, position: str) -> str:
        """Get sacred symbol for tetrahedral position"""
        symbols = {
            'TATA': '▼', 'ATLAS': '▲', 'OBI_WAN': '●', 'DOJO': '◼︎',
            'AKRON': '⟡', 'FIELD_DEV': '🔧', 'FIELD_OOWL': '🦉'
        }
        return symbols.get(position, '⚪')

def main():
    processor = JBRDataProcessor()
    processor.process_jbr_data()

if __name__ == "__main__":
    main()