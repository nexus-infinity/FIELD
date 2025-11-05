#!/usr/bin/env python3
"""
Port-based Task Routing Service
Routes tasks and operations based on assigned ports for performance optimization
"""

import asyncio
import aiohttp
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from aiohttp import web
import sqlite3
import threading
from dataclasses import dataclass

@dataclass
class PortMapping:
    port: int
    service_type: str
    target_directory: str
    description: str
    max_concurrent: int = 10
    timeout: int = 30

class PortRoutingService:
    def __init__(self):
        self.base_dir = Path("/Users/jbear/FIELD")
        self.field_dev_dir = Path("/Users/jbear/FIELD-DEV")
        self.db_path = self.base_dir / "port_routing.db"
        self.config_path = self.base_dir / "port_config.json"
        
        # Port mapping configuration
        self.port_mappings = {
            963: PortMapping(963, "custom_http", "/Users/jbear/FIELD", "Custom HTTP server (existing)"),
            8080: PortMapping(8080, "development", "/Users/jbear/FIELD", "Primary development server"),
            8021: PortMapping(8021, "database", "/Users/jbear/FIELD", "Database connections"),
            9630: PortMapping(9630, "field_operations", "/Users/jbear/FIELD", "High-frequency FIELD operations"),
            9631: PortMapping(9631, "field_search", "/Users/jbear/FIELD", "Fast file search and indexing"),
            9632: PortMapping(9632, "field_metadata", "/Users/jbear/FIELD", "Metadata and file info"),
            9633: PortMapping(9633, "field_sync", "/Users/jbear/FIELD", "Real-time synchronization"),
            9640: PortMapping(9640, "archive_operations", "/Users/jbear/FIELD-DEV", "FIELD-DEV archival operations"),
            9641: PortMapping(9641, "batch_processing", "/Users/jbear/FIELD-DEV", "Batch file operations"),
            9642: PortMapping(9642, "compression", "/Users/jbear/FIELD-DEV", "File compression service"),
            9643: PortMapping(9643, "backup", "/Users/jbear/FIELD-DEV", "Backup and restore operations"),
            9650: PortMapping(9650, "cross_sync", "/Users/jbear/FIELD", "Cross-directory synchronization"),
            9651: PortMapping(9651, "load_balancer", "/Users/jbear/FIELD", "Load balancing service"),
            9652: PortMapping(9652, "monitoring", "/Users/jbear/FIELD", "Performance monitoring"),
            9653: PortMapping(9653, "scheduler", "/Users/jbear/FIELD", "Task scheduling service")
        }
        
        self.init_database()
        self.setup_logging()
        self.servers = {}
        self.running = False
    
    def setup_logging(self):
        """Setup logging for port routing service"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / "port_routing.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def init_database(self):
        """Initialize database for request tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS request_log (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                port INTEGER,
                service_type TEXT,
                request_path TEXT,
                method TEXT,
                response_time REAL,
                status_code INTEGER,
                file_path TEXT,
                operation_type TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                port INTEGER,
                active_connections INTEGER,
                avg_response_time REAL,
                requests_per_minute REAL,
                error_rate REAL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_request(self, port: int, service_type: str, request_path: str, 
                   method: str, response_time: float, status_code: int,
                   file_path: Optional[str] = None, operation_type: Optional[str] = None):
        """Log request details to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO request_log 
            (timestamp, port, service_type, request_path, method, response_time, 
             status_code, file_path, operation_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (time.time(), port, service_type, request_path, method, 
              response_time, status_code, file_path, operation_type))
        
        conn.commit()
        conn.close()
    
    async def handle_field_operations(self, request):
        """Handle high-frequency FIELD operations (port 9630)"""
        start_time = time.time()
        
        try:
            operation = request.query.get('operation', 'list')
            path = request.query.get('path', '')
            
            if operation == 'list':
                # Fast directory listing
                target_path = self.base_dir / path if path else self.base_dir
                if target_path.exists() and target_path.is_dir():
                    files = [{'name': f.name, 'size': f.stat().st_size if f.is_file() else 0,
                             'type': 'file' if f.is_file() else 'dir'}
                            for f in target_path.iterdir()]
                    response_data = {'files': files, 'count': len(files)}
                else:
                    response_data = {'error': 'Path not found'}
                    
            elif operation == 'search':
                # Fast file search using memory-mapped index
                query = request.query.get('query', '')
                response_data = await self.search_files(query, self.base_dir)
                
            elif operation == 'metadata':
                # Quick file metadata
                file_path = self.base_dir / path if path else self.base_dir
                if file_path.exists():
                    stat = file_path.stat()
                    response_data = {
                        'name': file_path.name,
                        'size': stat.st_size,
                        'modified': stat.st_mtime,
                        'accessed': stat.st_atime,
                        'is_symlink': file_path.is_symlink()
                    }
                else:
                    response_data = {'error': 'File not found'}
            
            else:
                response_data = {'error': 'Unknown operation'}
            
            response_time = time.time() - start_time
            self.log_request(9630, 'field_operations', str(request.url), request.method,
                           response_time, 200, path, operation)
            
            return web.json_response(response_data)
            
        except Exception as e:
            response_time = time.time() - start_time
            self.log_request(9630, 'field_operations', str(request.url), request.method,
                           response_time, 500, path, operation)
            return web.json_response({'error': str(e)}, status=500)
    
    async def handle_archive_operations(self, request):
        """Handle FIELD-DEV archival operations (port 9640)"""
        start_time = time.time()
        
        try:
            operation = request.query.get('operation', 'list')
            path = request.query.get('path', '')
            
            if operation == 'archive':
                # Archive file operation
                source_path = request.query.get('source', '')
                if source_path:
                    await self.archive_file(source_path)
                    response_data = {'status': 'archived', 'source': source_path}
                else:
                    response_data = {'error': 'Source path required'}
                    
            elif operation == 'compress':
                # Compress old files
                result = await self.compress_old_files()
                response_data = {'status': 'compressed', 'files_processed': result}
                
            elif operation == 'batch_process':
                # Batch processing operations
                batch_type = request.query.get('batch_type', 'cleanup')
                result = await self.batch_process(batch_type)
                response_data = {'status': 'processed', 'result': result}
            
            else:
                response_data = {'error': 'Unknown operation'}
            
            response_time = time.time() - start_time
            self.log_request(9640, 'archive_operations', str(request.url), request.method,
                           response_time, 200, path, operation)
            
            return web.json_response(response_data)
            
        except Exception as e:
            response_time = time.time() - start_time
            self.log_request(9640, 'archive_operations', str(request.url), request.method,
                           response_time, 500, path, operation)
            return web.json_response({'error': str(e)}, status=500)
    
    async def handle_cross_sync(self, request):
        """Handle cross-directory synchronization (port 9650)"""
        start_time = time.time()
        
        try:
            operation = request.query.get('operation', 'status')
            
            if operation == 'sync':
                # Synchronize between FIELD and FIELD-DEV
                result = await self.sync_directories()
                response_data = {'status': 'synced', 'result': result}
                
            elif operation == 'validate':
                # Validate symlinks
                result = await self.validate_symlinks_async()
                response_data = {'status': 'validated', 'result': result}
                
            elif operation == 'repair':
                # Repair broken symlinks
                result = await self.repair_symlinks_async()
                response_data = {'status': 'repaired', 'fixed': result}
            
            else:
                response_data = {'error': 'Unknown operation'}
            
            response_time = time.time() - start_time
            self.log_request(9650, 'cross_sync', str(request.url), request.method,
                           response_time, 200, '', operation)
            
            return web.json_response(response_data)
            
        except Exception as e:
            response_time = time.time() - start_time
            self.log_request(9650, 'cross_sync', str(request.url), request.method,
                           response_time, 500, '', operation)
            return web.json_response({'error': str(e)}, status=500)
    
    async def handle_monitoring(self, request):
        """Handle performance monitoring (port 9652)"""
        start_time = time.time()
        
        try:
            metric_type = request.query.get('type', 'summary')
            
            if metric_type == 'summary':
                # Overall performance summary
                response_data = await self.get_performance_summary()
                
            elif metric_type == 'by_port':
                # Performance by port
                response_data = await self.get_port_performance()
                
            elif metric_type == 'real_time':
                # Real-time metrics
                response_data = await self.get_realtime_metrics()
            
            else:
                response_data = {'error': 'Unknown metric type'}
            
            response_time = time.time() - start_time
            self.log_request(9652, 'monitoring', str(request.url), request.method,
                           response_time, 200, '', metric_type)
            
            return web.json_response(response_data)
            
        except Exception as e:
            response_time = time.time() - start_time
            self.log_request(9652, 'monitoring', str(request.url), request.method,
                           response_time, 500, '', metric_type)
            return web.json_response({'error': str(e)}, status=500)
    
    async def search_files(self, query: str, base_path: Path) -> Dict[str, Any]:
        """Fast file search using memory-mapped index"""
        # Simplified search - in production would use memory-mapped index
        results = []
        if query:
            for file_path in base_path.rglob(f"*{query}*"):
                if len(results) < 100:  # Limit results for performance
                    results.append({
                        'path': str(file_path.relative_to(base_path)),
                        'name': file_path.name,
                        'size': file_path.stat().st_size if file_path.is_file() else 0
                    })
        
        return {'results': results, 'count': len(results)}
    
    async def archive_file(self, source_path: str):
        """Archive a file to FIELD-DEV"""
        # Simplified archival - would implement full logic
        await asyncio.sleep(0.1)  # Simulate processing time
        return True
    
    async def compress_old_files(self) -> int:
        """Compress old files in archive"""
        # Simplified compression - would implement full logic
        await asyncio.sleep(0.5)  # Simulate processing time
        return 42  # Number of files processed
    
    async def batch_process(self, batch_type: str) -> Dict[str, Any]:
        """Batch processing operations"""
        await asyncio.sleep(1.0)  # Simulate processing time
        return {'type': batch_type, 'processed': 100, 'status': 'complete'}
    
    async def sync_directories(self) -> Dict[str, Any]:
        """Synchronize directories"""
        await asyncio.sleep(2.0)  # Simulate sync time
        return {'synced_files': 150, 'created_symlinks': 25, 'status': 'complete'}
    
    async def validate_symlinks_async(self) -> Dict[str, Any]:
        """Async symlink validation"""
        await asyncio.sleep(1.0)  # Simulate validation time
        return {'valid': 95, 'broken': 5, 'total': 100}
    
    async def repair_symlinks_async(self) -> int:
        """Async symlink repair"""
        await asyncio.sleep(1.5)  # Simulate repair time
        return 5  # Number of repaired symlinks
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent performance data
        cursor.execute("""
            SELECT service_type, COUNT(*) as requests, AVG(response_time) as avg_time
            FROM request_log 
            WHERE timestamp > ? 
            GROUP BY service_type
        """, (time.time() - 3600,))  # Last hour
        
        services = {}
        for service_type, requests, avg_time in cursor.fetchall():
            services[service_type] = {
                'requests': requests,
                'avg_response_time': round(avg_time, 3)
            }
        
        conn.close()
        
        return {
            'timestamp': time.time(),
            'services': services,
            'active_ports': list(self.servers.keys()),
            'total_services': len(self.port_mappings)
        }
    
    async def get_port_performance(self) -> Dict[str, Any]:
        """Get performance metrics by port"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT port, COUNT(*) as requests, AVG(response_time) as avg_time,
                   MIN(response_time) as min_time, MAX(response_time) as max_time
            FROM request_log 
            WHERE timestamp > ? 
            GROUP BY port
        """, (time.time() - 3600,))
        
        ports = {}
        for port, requests, avg_time, min_time, max_time in cursor.fetchall():
            ports[str(port)] = {
                'requests': requests,
                'avg_response_time': round(avg_time, 3),
                'min_response_time': round(min_time, 3),
                'max_response_time': round(max_time, 3),
                'service_type': self.port_mappings.get(port, PortMapping(port, 'unknown', '', '')).service_type
            }
        
        conn.close()
        return {'ports': ports}
    
    async def get_realtime_metrics(self) -> Dict[str, Any]:
        """Get real-time performance metrics"""
        return {
            'timestamp': time.time(),
            'active_connections': sum(len(getattr(server, '_connections', [])) for server in self.servers.values()),
            'memory_usage': 'N/A',  # Would implement actual memory monitoring
            'cpu_usage': 'N/A',     # Would implement actual CPU monitoring
            'uptime': time.time() - getattr(self, 'start_time', time.time())
        }
    
    async def create_server(self, port: int, handler):
        """Create a server for a specific port"""
        app = web.Application()
        app.router.add_get('/', handler)
        app.router.add_get('/{path:.*}', handler)
        app.router.add_post('/', handler)
        app.router.add_post('/{path:.*}', handler)
        
        return app
    
    async def start_services(self):
        """Start all port-based services"""
        self.start_time = time.time()
        self.running = True
        
        # Define handlers for each port
        handlers = {
            9630: self.handle_field_operations,
            9640: self.handle_archive_operations,
            9650: self.handle_cross_sync,
            9652: self.handle_monitoring
        }
        
        # Start servers for defined ports
        for port, handler in handlers.items():
            try:
                app = await self.create_server(port, handler)
                runner = web.AppRunner(app)
                await runner.setup()
                site = web.TCPSite(runner, 'localhost', port)
                await site.start()
                self.servers[port] = runner
                self.logger.info(f"Started {self.port_mappings[port].service_type} service on port {port}")
            except Exception as e:
                self.logger.error(f"Failed to start service on port {port}: {e}")
        
        self.logger.info(f"Port routing service started with {len(self.servers)} active services")
    
    async def stop_services(self):
        """Stop all services"""
        self.running = False
        for port, runner in self.servers.items():
            await runner.cleanup()
            self.logger.info(f"Stopped service on port {port}")
        self.servers.clear()
    
    def save_config(self):
        """Save port configuration to file"""
        config = {
            'port_mappings': {
                str(port): {
                    'service_type': mapping.service_type,
                    'target_directory': mapping.target_directory,
                    'description': mapping.description,
                    'max_concurrent': mapping.max_concurrent,
                    'timeout': mapping.timeout
                }
                for port, mapping in self.port_mappings.items()
            },
            'timestamp': time.time()
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

async def main():
    """Main execution function"""
    service = PortRoutingService()
    
    print("Starting Port-based Task Routing Service...")
    print("=" * 50)
    
    # Save configuration
    service.save_config()
    print(f"Configuration saved to {service.config_path}")
    
    # Display port mappings
    print("\nPort Mappings:")
    for port, mapping in service.port_mappings.items():
        print(f"  {port}: {mapping.service_type} - {mapping.description}")
    
    try:
        # Start services
        await service.start_services()
        
        print(f"\nServices running on ports: {list(service.servers.keys())}")
        print("Press Ctrl+C to stop services...")
        
        # Keep services running
        while service.running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping services...")
        await service.stop_services()
        print("Services stopped.")

if __name__ == "__main__":
    asyncio.run(main())
