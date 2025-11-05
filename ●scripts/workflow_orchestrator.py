#!/usr/bin/env python3
"""
Workflow Orchestration Master Script
Coordinates all storage optimization components for FIELD/FIELD-DEV workflow
"""

import os
import sys
import json
import time
import subprocess
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime

class WorkflowOrchestrator:
    def __init__(self):
        self.base_dir = Path("/Users/jbear/FIELD")
        self.field_dev_dir = Path("/Users/jbear/FIELD-DEV")
        self.scripts_dir = self.base_dir / "scripts"
        
        # Ensure scripts directory exists
        self.scripts_dir.mkdir(exist_ok=True)
        
        self.setup_logging()
        self.status = {
            'analysis_complete': False,
            'symlinks_optimized': False,
            'services_running': False,
            'optimization_active': False
        }
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / "workflow_orchestrator.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if all required dependencies are available"""
        dependencies = {
            'python3': False,
            'sqlite3': False,
            'asyncio': False,
            'aiohttp': False
        }
        
        # Check Python 3
        try:
            result = subprocess.run(['python3', '--version'], 
                                 capture_output=True, text=True)
            dependencies['python3'] = result.returncode == 0
        except FileNotFoundError:
            pass
        
        # Check SQLite3
        try:
            import sqlite3
            dependencies['sqlite3'] = True
        except ImportError:
            pass
        
        # Check asyncio
        try:
            import asyncio
            dependencies['asyncio'] = True
        except ImportError:
            pass
        
        # Check aiohttp
        try:
            import aiohttp
            dependencies['aiohttp'] = True
        except ImportError:
            pass
        
        return dependencies
    
    def install_missing_dependencies(self, missing: List[str]):
        """Install missing Python dependencies"""
        if missing:
            self.logger.info(f"Installing missing dependencies: {missing}")
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install'
                ] + missing, check=True)
                self.logger.info("Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to install dependencies: {e}")
    
    async def run_access_analysis(self) -> bool:
        """Run file access pattern analysis"""
        self.logger.info("Starting file access pattern analysis...")
        
        try:
            # Run access pattern analyzer
            result = subprocess.run([
                'python3', str(self.scripts_dir / 'access_pattern_analyzer.py')
            ], capture_output=True, text=True, cwd=str(self.base_dir))
            
            if result.returncode == 0:
                self.logger.info("Access pattern analysis completed successfully")
                self.status['analysis_complete'] = True
                return True
            else:
                self.logger.error(f"Access analysis failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error running access analysis: {e}")
            return False
    
    async def optimize_symlinks(self) -> bool:
        """Optimize symlink structure"""
        if not self.status['analysis_complete']:
            self.logger.warning("Skipping symlink optimization - analysis not complete")
            return False
        
        self.logger.info("Starting symlink optimization...")
        
        try:
            # Run symlink manager
            result = subprocess.run([
                'python3', str(self.scripts_dir / 'symlink_manager.py')
            ], capture_output=True, text=True, cwd=str(self.base_dir),
            input='y\ny\n')  # Auto-confirm migrations and repairs
            
            if result.returncode == 0:
                self.logger.info("Symlink optimization completed successfully")
                self.status['symlinks_optimized'] = True
                return True
            else:
                self.logger.error(f"Symlink optimization failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error running symlink optimization: {e}")
            return False
    
    async def start_port_services(self) -> bool:
        """Start port-based routing services"""
        self.logger.info("Starting port-based routing services...")
        
        try:
            # Start port routing service as background process
            self.port_service_process = subprocess.Popen([
                'python3', str(self.scripts_dir / 'port_routing_service.py')
            ], cwd=str(self.base_dir))
            
            # Give it time to start
            await asyncio.sleep(5)
            
            # Check if process is still running
            if self.port_service_process.poll() is None:
                self.logger.info("Port routing services started successfully")
                self.status['services_running'] = True
                return True
            else:
                self.logger.error("Port routing services failed to start")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting port services: {e}")
            return False
    
    def create_monitoring_dashboard(self):
        """Create a simple monitoring dashboard"""
        dashboard_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>FIELD Storage Optimization Dashboard</title>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="30">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .status {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .active {{ background-color: #d4edda; border: 1px solid #c3e6cb; }}
        .inactive {{ background-color: #f8d7da; border: 1px solid #f5c6cb; }}
        .services {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .service {{ border: 1px solid #ccc; padding: 15px; border-radius: 5px; }}
        h1, h2 {{ color: #333; }}
        .metrics {{ font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>FIELD Storage Optimization Dashboard</h1>
    
    <h2>System Status</h2>
    <div class="status {'active' if self.status['analysis_complete'] else 'inactive'}">
        Analysis Complete: {'✓' if self.status['analysis_complete'] else '✗'}
    </div>
    <div class="status {'active' if self.status['symlinks_optimized'] else 'inactive'}">
        Symlinks Optimized: {'✓' if self.status['symlinks_optimized'] else '✗'}
    </div>
    <div class="status {'active' if self.status['services_running'] else 'inactive'}">
        Services Running: {'✓' if self.status['services_running'] else '✗'}
    </div>
    
    <h2>Port Services</h2>
    <div class="services">
        <div class="service">
            <h3>High-Frequency Operations (9630)</h3>
            <p>Fast file operations, search, and metadata</p>
            <p>Target: FIELD directory</p>
        </div>
        <div class="service">
            <h3>Archive Operations (9640)</h3>
            <p>Archival, compression, batch processing</p>
            <p>Target: FIELD-DEV directory</p>
        </div>
        <div class="service">
            <h3>Cross-Directory Sync (9650)</h3>
            <p>Synchronization and symlink management</p>
            <p>Target: Both directories</p>
        </div>
        <div class="service">
            <h3>Performance Monitoring (9652)</h3>
            <p>Real-time metrics and performance data</p>
            <p>Target: System-wide</p>
        </div>
    </div>
    
    <h2>Quick Actions</h2>
    <ul>
        <li><a href="http://localhost:9630?operation=list" target="_blank">Browse FIELD Files</a></li>
        <li><a href="http://localhost:9640?operation=batch_process&batch_type=cleanup" target="_blank">Run Archive Cleanup</a></li>
        <li><a href="http://localhost:9650?operation=validate" target="_blank">Validate Symlinks</a></li>
        <li><a href="http://localhost:9652?type=summary" target="_blank">Performance Summary</a></li>
    </ul>
    
    <div class="metrics">
        <h3>System Metrics</h3>
        <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>FIELD Directory: {self.get_directory_size(self.base_dir):.2f} GB</p>
        <p>FIELD-DEV Directory: {self.get_directory_size(self.field_dev_dir):.2f} GB</p>
        <p>Active Services: {sum(self.status.values())}/4</p>
    </div>
</body>
</html>"""
        
        dashboard_path = self.base_dir / "optimization_dashboard.html"
        with open(dashboard_path, 'w') as f:
            f.write(dashboard_content)
        
        self.logger.info(f"Dashboard created at {dashboard_path}")
        return dashboard_path
    
    def get_directory_size(self, directory: Path) -> float:
        """Get directory size in GB"""
        try:
            result = subprocess.run(['du', '-s', str(directory)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # Convert from KB to GB
                size_kb = int(result.stdout.split()[0])
                return size_kb / (1024 * 1024)
        except:
            pass
        return 0.0
    
    def generate_performance_report(self) -> str:
        """Generate comprehensive performance report"""
        report = f"""
FIELD Storage Optimization Performance Report
============================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

System Status:
- Analysis Complete: {'✓' if self.status['analysis_complete'] else '✗'}
- Symlinks Optimized: {'✓' if self.status['symlinks_optimized'] else '✗'}
- Services Running: {'✓' if self.status['services_running'] else '✗'}
- Optimization Active: {'✓' if self.status['optimization_active'] else '✗'}

Directory Sizes:
- FIELD: {self.get_directory_size(self.base_dir):.2f} GB
- FIELD-DEV: {self.get_directory_size(self.field_dev_dir):.2f} GB

Optimization Benefits:
1. High-frequency access files kept in lightweight FIELD directory
2. Archive and infrequent files moved to FIELD-DEV with symlinks
3. Port-based routing enables specialized performance optimization
4. Memory-mapped indexes provide O(1) file lookups
5. Automated monitoring and maintenance workflows

Port Service Architecture:
- 9630: High-frequency FIELD operations (search, metadata, quick access)
- 9640: FIELD-DEV archival operations (compression, batch processing)
- 9650: Cross-directory synchronization (symlink management)
- 9652: Performance monitoring and metrics collection

Performance Optimizations Implemented:
1. Symlink-based storage tiering (hot/cold data separation)
2. Memory-mapped file indexes for rapid lookups
3. Port-based task routing for workload-specific optimization
4. Automated access pattern analysis and optimization
5. Real-time performance monitoring and alerting

Recommendations:
1. Run full optimization cycle weekly
2. Monitor symlink health daily
3. Review access patterns monthly for further optimization
4. Consider implementing compression for archive files > 6 months old
5. Set up automated cleanup policies for temporary files

Files and Logs:
- Main log: {self.base_dir}/workflow_orchestrator.log
- Access analysis: {self.base_dir}/access_analysis_results.json
- Symlink operations: {self.base_dir}/symlink_operations.log
- Port routing: {self.base_dir}/port_routing.log
- Dashboard: {self.base_dir}/optimization_dashboard.html
"""
        return report
    
    async def run_full_optimization(self):
        """Run complete storage optimization workflow"""
        self.logger.info("Starting full storage optimization workflow...")
        
        # Check dependencies
        deps = self.check_dependencies()
        missing = [dep for dep, available in deps.items() if not available]
        if 'aiohttp' in missing:
            self.install_missing_dependencies(['aiohttp'])
        
        # Step 1: Analyze access patterns
        if await self.run_access_analysis():
            self.logger.info("✓ Access pattern analysis completed")
        else:
            self.logger.error("✗ Access pattern analysis failed")
            return False
        
        # Step 2: Optimize symlinks
        if await self.optimize_symlinks():
            self.logger.info("✓ Symlink optimization completed")
        else:
            self.logger.error("✗ Symlink optimization failed")
            return False
        
        # Step 3: Start port services
        if await self.start_port_services():
            self.logger.info("✓ Port services started")
        else:
            self.logger.error("✗ Port services failed to start")
            return False
        
        # Step 4: Create monitoring dashboard
        dashboard_path = self.create_monitoring_dashboard()
        self.logger.info(f"✓ Monitoring dashboard created at {dashboard_path}")
        
        # Step 5: Generate performance report
        report = self.generate_performance_report()
        report_path = self.base_dir / "optimization_report.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        
        self.logger.info(f"✓ Performance report saved to {report_path}")
        
        self.status['optimization_active'] = True
        self.logger.info("🎉 Full storage optimization workflow completed successfully!")
        
        print("\\n" + "="*60)
        print("FIELD STORAGE OPTIMIZATION COMPLETE")
        print("="*60)
        print(f"Dashboard: file://{dashboard_path}")
        print(f"Report: {report_path}")
        print("\\nPort Services Running:")
        print("  - 9630: High-frequency operations")
        print("  - 9640: Archive operations") 
        print("  - 9650: Cross-directory sync")
        print("  - 9652: Performance monitoring")
        print("\\nOptimization is now active and monitoring.")
        
        return True
    
    def stop_services(self):
        """Stop all running services"""
        if hasattr(self, 'port_service_process'):
            self.port_service_process.terminate()
            self.logger.info("Port services stopped")
        self.status['services_running'] = False

async def main():
    """Main execution function"""
    orchestrator = WorkflowOrchestrator()
    
    print("FIELD Storage & Data Access Workflow Optimization")
    print("=" * 55)
    print("This will optimize your FIELD/FIELD-DEV workflow with:")
    print("1. File access pattern analysis")
    print("2. Symlink-based storage optimization") 
    print("3. Port-based task routing services")
    print("4. Memory-mapped indexes for performance")
    print("5. Real-time monitoring and metrics")
    
    response = input("\\nProceed with full optimization? (y/N): ")
    if response.lower() != 'y':
        print("Optimization cancelled.")
        return
    
    try:
        success = await orchestrator.run_full_optimization()
        
        if success:
            print("\\nOptimization running. Press Ctrl+C to stop services.")
            # Keep services running
            while True:
                await asyncio.sleep(10)
                # Update dashboard periodically
                orchestrator.create_monitoring_dashboard()
                
    except KeyboardInterrupt:
        print("\\nStopping optimization services...")
        orchestrator.stop_services()
        print("Services stopped. Optimization data preserved.")

if __name__ == "__main__":
    asyncio.run(main())
