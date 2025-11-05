#!/usr/bin/env python3
"""
Akron Sovereign Repository - Real-Time Monitor
Shows concurrent blockchain processing with database strippers
"""

import time
import random
import threading
from datetime import datetime
from pathlib import Path
import json
from akron_sovereign_integration import (
    AkronSovereignRepository, 
    DataPurity,
    SACRED_SYMBOLS
)

class AkronMonitor:
    """Real-time monitor for Akron Sovereign Repository"""
    
    def __init__(self):
        self.repo = AkronSovereignRepository()
        self.running = False
        self.data_generators = []
        self.monitor_thread = None
        
    def generate_contact_data(self):
        """Generate sample contact data with duplicates and noise"""
        names = ["John", "Jane", "Bob", "Alice", "Charlie", "Eve"]
        domains = ["example.com", "test.org", "mail.net"]
        
        name = random.choice(names) + " " + random.choice(["Smith", "Doe", "Johnson"])
        
        # Randomly add duplicate markers and noise
        if random.random() > 0.7:
            name += " (duplicate)"
        
        data = {
            'name': name,
            'phone': f"+1 555-{random.randint(1000, 9999)}",
            'email': f"{name.lower().replace(' ', '.')}@{random.choice(domains)}",
        }
        
        # Add random noise fields
        if random.random() > 0.5:
            data['empty_field'] = ''
            data['duplicate_email'] = data['email'] + "_backup"
            data['temp_field'] = 'temporary_data'
            
        return data
    
    def generate_music_data(self):
        """Generate sample music project data"""
        projects = ["Sacred Beats", "Mystical Flow", "Geometric Harmony"]
        keys = ["C major", "A minor", "D major", "G minor"]
        
        project_name = random.choice(projects)
        version = random.randint(1, 10)
        
        data = {
            'project': f"{project_name} v{version}",
            'tempo': random.randint(60, 180),
            'key': random.choice(keys),
            'stems': ['drums', 'bass', 'melody', 'harmony']
        }
        
        # Add backup/duplicate data
        if random.random() > 0.6:
            data['backup_file'] = f"{project_name}_backup.als"
            data['old_version'] = f"{project_name}_v{version-1}.als"
            data['stems'].append('drums')  # Duplicate stem
            
        return data
    
    def generate_code_data(self):
        """Generate sample code repository data"""
        files = ["main.py", "utils.js", "config.yaml", "README.md"]
        functions = ["process", "analyze", "clean", "validate", "export"]
        
        data = {
            'file': random.choice(files),
            'functions': random.sample(functions, 3),
            'imports': ['os', 'json', 'time', 'hashlib']
        }
        
        # Add build artifacts and cache
        if random.random() > 0.5:
            data['__pycache__'] = 'cache_data'
            data['build/'] = 'build_artifacts'
            data['node_modules/'] = 'dependencies'
            data['functions'].append(data['functions'][0])  # Duplicate function
            
        return data
    
    def data_generator_thread(self, context: str, generator_func, interval: float):
        """Thread to continuously generate and ingest data"""
        while self.running:
            try:
                data = generator_func()
                purity = random.choice([
                    DataPurity.MIRROR_DECAY,
                    DataPurity.EXPERIMENTAL,
                    DataPurity.SACRED
                ])
                
                self.repo.ingest_data(data, context=context, purity=purity)
                time.sleep(interval)
                
            except Exception as e:
                print(f"Error in {context} generator: {e}")
                
    def monitor_thread_func(self):
        """Monitor thread to display real-time metrics"""
        last_blockchain_metrics = {}
        
        while self.running:
            try:
                # Clear screen for dashboard effect
                print("\033[2J\033[H")  # Clear screen and move cursor to top
                
                # Header
                print(f"{SACRED_SYMBOLS['AKRON']} AKRON SOVEREIGN REPOSITORY - REAL-TIME MONITOR")
                print(f"{'='*70}")
                print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                
                # Repository Metrics
                print("📊 Repository Metrics:")
                print(f"  Total Data Processed: {self.repo.metrics['total_data_processed']}")
                print(f"  Efficiency Gain: {self.repo.metrics['efficiency_gain']:.1f}%")
                print(f"  Sacred Alignments: {self.repo.metrics['sacred_alignments']}")
                print(f"  Active Strippers: {self.repo.metrics['active_strippers']}")
                print()
                
                # Blockchain Metrics
                print("⛓️  Blockchain Metrics:")
                bc_metrics = self.repo.blockchain.metrics
                print(f"  Chain ID: {self.repo.blockchain.chain_id}")
                print(f"  Blocks Processed: {bc_metrics['blocks_processed']}")
                print(f"  Transactions Processed: {bc_metrics['transactions_processed']}")
                print(f"  Data Stripped: {bc_metrics['data_stripped']}")
                print(f"  Processing Time: {bc_metrics['processing_time']:.2f}s")
                print(f"  Pending Transactions: {self.repo.blockchain.pending_transactions.qsize()}")
                
                # Calculate rate
                if last_blockchain_metrics:
                    tx_rate = (bc_metrics['transactions_processed'] - 
                              last_blockchain_metrics.get('transactions_processed', 0))
                    print(f"  Transaction Rate: {tx_rate} tx/s")
                    
                last_blockchain_metrics = bc_metrics.copy()
                print()
                
                # Stripper Performance
                print("🧹 Database Stripper Performance:")
                for context, stripper in self.repo.strippers.items():
                    metrics = stripper.get_metrics()
                    if any(v > 0 for v in metrics.values()):
                        print(f"  {context}:")
                        print(f"    Duplicates Removed: {metrics['duplicates_removed']}")
                        print(f"    Null Fields Cleaned: {metrics['null_fields_cleaned']}")
                        print(f"    Patterns Matched: {metrics['patterns_matched']}")
                print()
                
                # Latest Block Info
                if self.repo.blockchain.blocks:
                    latest_block = self.repo.blockchain.blocks[-1]
                    print("📦 Latest Block:")
                    print(f"  Index: {latest_block['index']}")
                    print(f"  Transactions: {len(latest_block['transactions'])}")
                    print(f"  Symbolic Alignment: {latest_block['symbolic_alignment']}")
                    print(f"  Hash: {latest_block['hash'][:16]}...")
                    
                    if latest_block.get('stripped_data'):
                        total_reduction = sum(
                            s['original_size'] - s['cleaned_size'] 
                            for s in latest_block['stripped_data'].values()
                        )
                        print(f"  Data Reduced: {total_reduction} bytes")
                print()
                
                # Sacred Geometry Status
                print("🔺 Sacred Geometry Status:")
                if self.repo.blockchain.blocks:
                    alignment = latest_block.get('symbolic_alignment', '⟡')
                    if '▲' in alignment:
                        print(f"  {SACRED_SYMBOLS['ATLAS']} ATLAS: Active (Tooling Validation)")
                    if '▼' in alignment:
                        print(f"  {SACRED_SYMBOLS['TATA']} TATA: Active (Temporal Truth)")
                    if '●' in alignment:
                        print(f"  {SACRED_SYMBOLS['OBI_WAN']} OBI-WAN: Active (Living Memory)")
                    if '◼︎' in alignment:
                        print(f"  {SACRED_SYMBOLS['DOJO']} DOJO: Active (Manifestation)")
                    if alignment == '⟡':
                        print(f"  {SACRED_SYMBOLS['AKRON']} AKRON: Default Alignment")
                        
                time.sleep(1)
                
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(1)
    
    def start(self, duration: int = 60):
        """Start the monitoring system"""
        print(f"\n{SACRED_SYMBOLS['AKRON']} Starting Akron Sovereign Repository Monitor")
        print(f"Duration: {duration} seconds")
        print("Initializing data generators...\n")
        
        self.running = True
        
        # Start data generator threads
        generators = [
            ('contacts', self.generate_contact_data, 0.5),
            ('music', self.generate_music_data, 1.0),
            ('code', self.generate_code_data, 0.8)
        ]
        
        for context, func, interval in generators:
            thread = threading.Thread(
                target=self.data_generator_thread,
                args=(context, func, interval),
                daemon=True
            )
            thread.start()
            self.data_generators.append(thread)
            print(f"  ✓ {context.capitalize()} generator started (interval: {interval}s)")
        
        # Start monitor thread
        self.monitor_thread = threading.Thread(
            target=self.monitor_thread_func,
            daemon=True
        )
        self.monitor_thread.start()
        print("  ✓ Monitor thread started\n")
        
        print("Press Enter to view real-time dashboard...")
        input()
        
        # Run for specified duration
        start_time = time.time()
        try:
            while time.time() - start_time < duration:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
        
        self.stop()
        
    def stop(self):
        """Stop the monitoring system"""
        self.running = False
        
        # Wait for threads to finish
        time.sleep(2)
        
        # Print final report
        print("\n" + "="*70)
        print(f"{SACRED_SYMBOLS['AKRON']} FINAL REPORT")
        print("="*70)
        
        self.repo.print_metrics()
        
        # Show sample of stored data
        print("\n📚 Sample Sovereign Data:")
        results = self.repo.query_sovereign_data({
            'access_level': 'archive_only'
        })
        
        if results:
            for i, record in enumerate(results[:3]):
                print(f"\nRecord {i+1}:")
                print(f"  ID: {record['id'][:8]}...")
                print(f"  Purity: {record['purity']}")
                print(f"  Symbolic: {record['symbolic_anchor']}")
                print(f"  Blockchain: {record['blockchain_hash'][:16]}...")
                
                # Show cleaned content preview
                content_str = json.dumps(record['content'], indent=2)
                if len(content_str) > 200:
                    content_str = content_str[:200] + "..."
                print(f"  Content: {content_str}")
        
        print(f"\n✅ Monitor stopped. Database saved to: {self.repo.db_path}")

def main():
    """Main execution"""
    monitor = AkronMonitor()
    
    # Run for 30 seconds by default
    monitor.start(duration=30)

if __name__ == "__main__":
    main()
