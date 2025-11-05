#!/usr/bin/env python3
"""
FIELD System Walker - High-Level Scanner
Performs lightweight system inventory with minimal resource impact
Respects Sacred Field priorities and HOME FIELD homeostasis
"""

import os
import json
import sqlite3
import subprocess
import socket
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import psutil
import yaml

class FIELDScanner:
    """High-level resource scanner for FIELD system"""
    
    def __init__(self, config_path: str = "../policy/homeostasis.yaml"):
        self.config = self._load_config(config_path)
        self.node_id = self._determine_node_id()
        self.scan_id = f"{self.node_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.db_path = "/Volumes/Akron/bear_data/field_resource_graph.db"
        
    def _load_config(self, path: str) -> dict:
        """Load homeostasis policy configuration"""
        config_file = Path(__file__).parent / path
        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)
        return {}
        
    def _determine_node_id(self) -> str:
        """Determine which FIELD node we're running on"""
        hostname = socket.gethostname().lower()
        
        # Map hostnames to node IDs
        if "studio" in hostname or hostname == "mac-studio.local":
            return "MAC_STUDIO"
        elif "kitchen" in hostname or "nixos" in hostname:
            return "KITCHEN_IMAC"
        elif "den" in hostname:
            return "DEN_IMAC"
        elif "air" in hostname or "rose" in hostname:
            return "MACBOOK_AIR"
        else:
            return f"UNKNOWN_{hostname}"
            
    def check_homeostasis(self) -> Dict[str, bool]:
        """Check if system is within homeostasis budgets"""
        status = {}
        
        # CPU check (5-minute average)
        cpu_avg = psutil.cpu_percent(interval=1)
        cpu_threshold = self.config.get('homeostasis', {}).get('cpu', {}).get('threshold', 70)
        status['cpu_ok'] = cpu_avg < cpu_threshold
        
        # Memory check
        mem = psutil.virtual_memory()
        mem_threshold = self.config.get('homeostasis', {}).get('memory', {}).get('threshold', 80)
        status['memory_ok'] = mem.percent < mem_threshold
        
        # Disk check
        disk = psutil.disk_usage('/')
        disk_threshold = self.config.get('homeostasis', {}).get('disk', {}).get('threshold', 20)
        status['disk_ok'] = (100 - disk.percent) > disk_threshold
        
        # Overall status
        status['within_budget'] = all(status.values())
        
        return status
        
    def scan_hardware(self) -> Dict[str, Any]:
        """Collect hardware information"""
        print(f"🔍 Scanning hardware on {self.node_id}...")
        
        hardware = {
            'node_id': self.node_id,
            'scan_id': self.scan_id,
            'timestamp': datetime.now().isoformat(),
            'cpu': {},
            'memory': {},
            'disk': {},
            'network': {}
        }
        
        # CPU info
        hardware['cpu'] = {
            'count': psutil.cpu_count(logical=False),
            'count_logical': psutil.cpu_count(logical=True),
            'percent': psutil.cpu_percent(interval=1),
            'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
        }
        
        # Memory info
        mem = psutil.virtual_memory()
        hardware['memory'] = {
            'total': mem.total,
            'available': mem.available,
            'percent': mem.percent,
            'used': mem.used,
            'free': mem.free
        }
        
        # Disk info
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except PermissionError:
                continue
                
        hardware['disk'] = {'partitions': partitions}
        
        # Network interfaces
        interfaces = {}
        for name, addrs in psutil.net_if_addrs().items():
            interfaces[name] = []
            for addr in addrs:
                interfaces[name].append({
                    'family': addr.family.name,
                    'address': addr.address,
                    'netmask': addr.netmask
                })
        hardware['network'] = {'interfaces': interfaces}
        
        return hardware
        
    def scan_processes(self) -> List[Dict[str, Any]]:
        """Scan running processes, identify Sacred Field operations"""
        print("🔍 Scanning processes...")
        
        sacred_keywords = [
            'sdr', 'backup', 'sovereignty', 'pieces', '963',
            'field', 'akron', 'dedup'
        ]
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                
                # Check if this is a sacred process
                is_sacred = any(keyword in pinfo['name'].lower() for keyword in sacred_keywords)
                
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'username': pinfo['username'],
                    'cpu_percent': pinfo['cpu_percent'],
                    'memory_percent': pinfo['memory_percent'],
                    'is_sacred': is_sacred
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return processes
        
    def scan_ports(self) -> List[Dict[str, Any]]:
        """Scan open ports, especially port 963"""
        print("🔍 Scanning ports...")
        
        ports = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN':
                ports.append({
                    'port': conn.laddr.port,
                    'address': conn.laddr.ip,
                    'pid': conn.pid,
                    'is_sacred': conn.laddr.port == 963
                })
                
        return ports
        
    def scan_services(self) -> List[Dict[str, Any]]:
        """Scan LaunchAgents and services"""
        print("🔍 Scanning services...")
        
        services = []
        
        # Check LaunchAgents
        try:
            result = subprocess.run(
                ['launchctl', 'list'], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            
            for line in result.stdout.splitlines()[1:]:  # Skip header
                parts = line.split('\t')
                if len(parts) >= 3:
                    pid, status, label = parts[0], parts[1], parts[2]
                    
                    # Check if this is a FIELD service
                    is_field = 'field' in label.lower() or 'pieces' in label.lower()
                    
                    services.append({
                        'label': label,
                        'pid': pid if pid != '-' else None,
                        'status': status,
                        'is_field': is_field
                    })
        except Exception as e:
            print(f"⚠️ Error scanning services: {e}")
            
        return services
        
    def estimate_sovereignty_metrics(self) -> Dict[str, float]:
        """Estimate current sovereignty levels"""
        print("📊 Estimating sovereignty metrics...")
        
        metrics = {
            'electricity': 0.0,  # Will need hardware sensors
            'compute': 0.3,      # Rough estimate based on local vs cloud
            'data': 0.6,         # Based on local storage
            'network_independence': 0.0  # Days we can operate offline
        }
        
        # Check if Akron volumes are mounted (data sovereignty indicator)
        if Path("/Volumes/Akron").exists():
            metrics['data'] = 0.7
            
        # Check for local development tools (compute sovereignty)
        if any(Path(p).exists() for p in ["/usr/local/bin/python3", "/opt/homebrew/bin/python3"]):
            metrics['compute'] = 0.4
            
        return metrics
        
    def save_scan_results(self, results: Dict[str, Any]):
        """Save scan results to database"""
        print(f"💾 Saving results to {self.db_path}...")
        
        # Ensure Akron volume is mounted
        if not Path("/Volumes/Akron/bear_data").exists():
            print("⚠️ Akron volume not mounted, saving locally")
            self.db_path = Path.home() / "field_scan_results.json"
            with open(self.db_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            return
            
        # Save to SQLite (simplified for now)
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scans (
                    scan_id TEXT PRIMARY KEY,
                    node_id TEXT,
                    timestamp TEXT,
                    data TEXT
                )
            ''')
            
            # Insert scan results
            cursor.execute(
                "INSERT INTO scans (scan_id, node_id, timestamp, data) VALUES (?, ?, ?, ?)",
                (self.scan_id, self.node_id, datetime.now().isoformat(), json.dumps(results, default=str))
            )
            
            conn.commit()
            conn.close()
            print("✅ Results saved successfully")
        except Exception as e:
            print(f"❌ Error saving to database: {e}")
            
    def run_scan(self) -> Dict[str, Any]:
        """Run complete high-level scan"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║           FIELD System Walker - High-Level Scanner           ║
║                    Node: {self.node_id:20s}            ║
║                    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}            ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Check homeostasis first
        homeostasis = self.check_homeostasis()
        
        if not homeostasis['within_budget']:
            print("⚠️ System not within homeostasis budgets, running minimal scan only")
            
        results = {
            'scan_id': self.scan_id,
            'node_id': self.node_id,
            'timestamp': datetime.now().isoformat(),
            'homeostasis': homeostasis
        }
        
        # Only run full scan if within budgets
        if homeostasis['within_budget']:
            results['hardware'] = self.scan_hardware()
            results['processes'] = self.scan_processes()
            results['ports'] = self.scan_ports()
            results['services'] = self.scan_services()
            results['sovereignty'] = self.estimate_sovereignty_metrics()
        else:
            print("⏸️ Deferring detailed scan until system returns to homeostasis")
            
        # Always save results
        self.save_scan_results(results)
        
        # Print summary
        self._print_summary(results)
        
        return results
        
    def _print_summary(self, results: Dict[str, Any]):
        """Print scan summary"""
        print("\n" + "="*60)
        print("📊 SCAN SUMMARY")
        print("="*60)
        
        print(f"Node ID: {results['node_id']}")
        print(f"Scan ID: {results['scan_id']}")
        print(f"Timestamp: {results['timestamp']}")
        
        if 'homeostasis' in results:
            h = results['homeostasis']
            status = "✅ OK" if h['within_budget'] else "⚠️ EXCEEDED"
            print(f"\nHomeostasis: {status}")
            print(f"  CPU: {'✅' if h.get('cpu_ok') else '❌'}")
            print(f"  Memory: {'✅' if h.get('memory_ok') else '❌'}")
            print(f"  Disk: {'✅' if h.get('disk_ok') else '❌'}")
            
        if 'sovereignty' in results:
            s = results['sovereignty']
            print(f"\nSovereignty Metrics:")
            print(f"  Electricity: {s['electricity']*100:.0f}%")
            print(f"  Compute: {s['compute']*100:.0f}%")
            print(f"  Data: {s['data']*100:.0f}%")
            print(f"  Network Independence: {s['network_independence']} days")
            
        if 'processes' in results:
            sacred_count = sum(1 for p in results['processes'] if p.get('is_sacred'))
            print(f"\nProcesses: {len(results['processes'])} total, {sacred_count} sacred")
            
        if 'ports' in results:
            port_963 = any(p['port'] == 963 for p in results['ports'])
            status = "✅ Active" if port_963 else "❌ Inactive"
            print(f"Port 963 Health API: {status}")
            
        print("\n" + "="*60)
        print("✨ Scan complete - Building sovereignty through sacred priorities")
        print("="*60)

if __name__ == "__main__":
    scanner = FIELDScanner()
    scanner.run_scan()
