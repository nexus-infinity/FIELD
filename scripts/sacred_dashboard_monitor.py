#!/usr/bin/env python3
"""
Sacred Component Real-Time Dashboard Monitor
===========================================
Provides live monitoring and backward compatibility checking for sacred components.
Implements real-time dashboard integration with sacred deployment system.
"""

import json
import time
import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
import websockets
import redis
from flask import Flask, jsonify, render_template_string
import threading
import psutil
import sqlite3

class SacredDashboardMonitor:
    """Real-time monitoring system for sacred components with dashboard integration."""
    
    def __init__(self, field_path: str = "/Users/jbear/FIELD"):
        self.field_path = Path(field_path)
        self.monitoring_db_path = self.field_path / "logs" / "monitoring.db"
        self.dashboard_state_path = self.field_path / "logs" / "dashboard_state.json"
        
        # Setup logging
        self._setup_logging()
        
        # Initialize Redis
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.redis_client.ping()
            self.logger.info("Connected to Redis for real-time monitoring")
        except:
            self.logger.warning("Redis not available")
            self.redis_client = None
        
        # Initialize SQLite database for persistent monitoring
        self._setup_monitoring_db()
        
        # Flask app for dashboard
        self.app = Flask(__name__)
        self._setup_flask_routes()
        
        # Sacred component definitions
        self.sacred_components = {
            "ATLAS": {"symbol": "▲", "type": "tooling_validation"},
            "TATA": {"symbol": "▼", "type": "temporal_truth"}, 
            "OBI-WAN": {"symbol": "●", "type": "living_memory"},
            "DOJO": {"symbol": "◼", "type": "manifestation"}
        }
        
        # Monitoring state
        self.monitoring_active = False
        self.websocket_clients = set()
    
    def _setup_logging(self):
        """Setup logging system."""
        log_path = self.field_path / "logs" / "dashboard_monitor.log"
        log_path.parent.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger("SacredDashboard")
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _setup_monitoring_db(self):
        """Setup SQLite database for monitoring data."""
        os.makedirs(self.monitoring_db_path.parent, exist_ok=True)
        
        conn = sqlite3.connect(str(self.monitoring_db_path))
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS component_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                component TEXT NOT NULL,
                symbol TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                details TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_usage REAL,
                active_components INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deployment_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                component TEXT NOT NULL,
                event_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                success BOOLEAN,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self.logger.info("Monitoring database initialized")
    
    def _setup_flask_routes(self):
        """Setup Flask routes for dashboard API."""
        
        @self.app.route('/api/status')
        def get_status():
            """Get current system status."""
            return jsonify(self.get_system_status())
        
        @self.app.route('/api/components')
        def get_components():
            """Get sacred component status."""
            return jsonify(self.get_component_status())
        
        @self.app.route('/api/metrics')
        def get_metrics():
            """Get system metrics."""
            return jsonify(self.get_system_metrics())
        
        @self.app.route('/api/deployment-log')
        def get_deployment_log():
            """Get deployment event log."""
            return jsonify(self.get_deployment_events())
        
        @self.app.route('/dashboard')
        def dashboard():
            """Serve the dashboard interface."""
            return render_template_string(DASHBOARD_HTML_TEMPLATE)
        
        @self.app.route('/')
        def index():
            """Redirect to dashboard."""
            return render_template_string(DASHBOARD_HTML_TEMPLATE)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available_gb": round(memory.available / (1024**3), 2),
                    "disk_usage_percent": round(disk.used / disk.total * 100, 2),
                    "disk_free_gb": round(disk.free / (1024**3), 2)
                },
                "sacred_components": self.get_component_deployment_status(),
                "monitoring_active": self.monitoring_active,
                "redis_connected": self.redis_client is not None
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {str(e)}")
            return {"error": str(e)}
    
    def get_component_status(self) -> Dict[str, Any]:
        """Get detailed sacred component status."""
        component_status = {}
        
        for name, info in self.sacred_components.items():
            component_path = self.field_path / f"{info['symbol']}{name}"
            
            status = {
                "name": name,
                "symbol": info["symbol"],
                "type": info["type"],
                "exists": component_path.exists(),
                "deployed": (component_path / ".deployed").exists() if component_path.exists() else False,
                "file_count": len(list(component_path.rglob("*"))) if component_path.exists() else 0,
                "last_modified": None,
                "validation_status": "unknown"
            }
            
            # Get last modified time
            if component_path.exists():
                try:
                    stat = component_path.stat()
                    status["last_modified"] = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
                except:
                    pass
            
            # Check deployment status from Redis if available
            if self.redis_client:
                try:
                    redis_status = self.redis_client.get(f"sacred_component:{name}:status")
                    if redis_status:
                        status["redis_status"] = redis_status
                except:
                    pass
            
            component_status[name] = status
        
        return component_status
    
    def get_component_deployment_status(self) -> Dict[str, str]:
        """Get simple deployment status for each component."""
        status = {}
        for name, info in self.sacred_components.items():
            component_path = self.field_path / f"{info['symbol']}{name}"
            deployed_marker = component_path / ".deployed"
            
            if not component_path.exists():
                status[name] = "missing"
            elif deployed_marker.exists():
                status[name] = "deployed"
            else:
                status[name] = "present"
        
        return status
    
    def get_system_metrics(self) -> List[Dict[str, Any]]:
        """Get recent system metrics from database."""
        conn = sqlite3.connect(str(self.monitoring_db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, cpu_percent, memory_percent, disk_usage, active_components
            FROM system_metrics 
            ORDER BY id DESC 
            LIMIT 100
        ''')
        
        metrics = []
        for row in cursor.fetchall():
            metrics.append({
                "timestamp": row[0],
                "cpu_percent": row[1],
                "memory_percent": row[2], 
                "disk_usage": row[3],
                "active_components": row[4]
            })
        
        conn.close()
        return metrics
    
    def get_deployment_events(self) -> List[Dict[str, Any]]:
        """Get recent deployment events."""
        conn = sqlite3.connect(str(self.monitoring_db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT component, event_type, timestamp, success, details
            FROM deployment_events
            ORDER BY id DESC
            LIMIT 50
        ''')
        
        events = []
        for row in cursor.fetchall():
            events.append({
                "component": row[0],
                "event_type": row[1],
                "timestamp": row[2],
                "success": row[3],
                "details": json.loads(row[4]) if row[4] else {}
            })
        
        conn.close()
        return events
    
    def record_system_metrics(self):
        """Record current system metrics to database."""
        try:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').used / psutil.disk_usage('/').total * 100
            
            # Count active (deployed) components
            active_components = sum(1 for status in self.get_component_deployment_status().values() 
                                  if status == "deployed")
            
            conn = sqlite3.connect(str(self.monitoring_db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_metrics (timestamp, cpu_percent, memory_percent, disk_usage, active_components)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now(timezone.utc).isoformat(),
                cpu_percent,
                memory_percent,
                disk_usage,
                active_components
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error recording system metrics: {str(e)}")
    
    def record_deployment_event(self, component: str, event_type: str, success: bool, details: Dict = None):
        """Record a deployment event."""
        conn = sqlite3.connect(str(self.monitoring_db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO deployment_events (component, event_type, timestamp, success, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            component,
            event_type,
            datetime.now(timezone.utc).isoformat(),
            success,
            json.dumps(details) if details else None
        ))
        
        conn.commit()
        conn.close()
    
    async def monitor_components(self):
        """Main monitoring loop."""
        self.logger.info("Starting component monitoring loop")
        self.monitoring_active = True
        
        while self.monitoring_active:
            try:
                # Record system metrics
                self.record_system_metrics()
                
                # Check component status changes
                current_status = self.get_component_deployment_status()
                
                # Broadcast updates via WebSocket if there are clients
                if self.websocket_clients:
                    status_update = {
                        "type": "status_update",
                        "data": self.get_system_status()
                    }
                    
                    # Send to all connected clients
                    disconnected = set()
                    for client in self.websocket_clients:
                        try:
                            await client.send(json.dumps(status_update))
                        except websockets.exceptions.ConnectionClosed:
                            disconnected.add(client)
                    
                    # Remove disconnected clients
                    self.websocket_clients -= disconnected
                
                # Update dashboard state file for backward compatibility
                self.update_dashboard_state()
                
                await asyncio.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(10)  # Wait longer on error
    
    def update_dashboard_state(self):
        """Update dashboard state file for backward compatibility."""
        dashboard_state = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "components": self.get_component_deployment_status(),
            "system_status": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent
            },
            "api_endpoints": [
                "/api/status",
                "/api/components", 
                "/api/metrics",
                "/api/deployment-log"
            ],
            "data_schemas": {
                "atlas": {"version": "1.0", "type": "tooling_validation"},
                "tata": {"version": "1.0", "type": "temporal_truth"},
                "obi-wan": {"version": "1.0", "type": "living_memory"},
                "dojo": {"version": "1.0", "type": "manifestation"}
            }
        }
        
        with open(self.dashboard_state_path, 'w') as f:
            json.dump(dashboard_state, f, indent=2)
    
    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connections for real-time updates."""
        self.websocket_clients.add(websocket)
        self.logger.info(f"WebSocket client connected. Total: {len(self.websocket_clients)}")
        
        try:
            # Send initial status
            initial_status = {
                "type": "initial_status",
                "data": self.get_system_status()
            }
            await websocket.send(json.dumps(initial_status))
            
            # Keep connection alive
            async for message in websocket:
                # Handle any incoming messages
                pass
                
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.websocket_clients.discard(websocket)
            self.logger.info(f"WebSocket client disconnected. Total: {len(self.websocket_clients)}")
    
    def run_flask_app(self):
        """Run the Flask dashboard app."""
        self.logger.info("Starting Flask dashboard on http://localhost:8080")
        self.app.run(host='0.0.0.0', port=8080, debug=False)
    
    def start_monitoring(self):
        """Start the complete monitoring system."""
        self.logger.info("Starting Sacred Dashboard Monitoring System")
        
        # Start Flask app in separate thread
        flask_thread = threading.Thread(target=self.run_flask_app)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Start WebSocket server
        websocket_server = websockets.serve(self.handle_websocket, "localhost", 8765)
        
        # Start monitoring loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(
            websocket_server,
            self.monitor_components()
        ))
    
    def stop_monitoring(self):
        """Stop monitoring system."""
        self.monitoring_active = False
        self.logger.info("Monitoring system stopped")

# Dashboard HTML Template
DASHBOARD_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sacred Component Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
        .component { padding: 15px; border-left: 4px solid #ccc; }
        .component.deployed { border-color: #4CAF50; }
        .component.present { border-color: #FF9800; }
        .component.missing { border-color: #F44336; }
        .symbol { font-size: 24px; font-weight: bold; display: inline-block; margin-right: 10px; }
        .metrics { display: flex; justify-content: space-between; flex-wrap: wrap; }
        .metric { text-align: center; padding: 10px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #2196F3; }
        .refresh-btn { background: #2196F3; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .refresh-btn:hover { background: #1976D2; }
        #status { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🔮 Sacred Component Dashboard</h1>
            <p>Status: <span id="status">Loading...</span></p>
            <button class="refresh-btn" onclick="refreshData()">Refresh</button>
        </div>
        
        <div class="card">
            <h2>System Metrics</h2>
            <div class="metrics" id="system-metrics">
                <div class="metric">
                    <div class="metric-value" id="cpu">--</div>
                    <div>CPU %</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="memory">--</div>
                    <div>Memory %</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="disk">--</div>
                    <div>Disk %</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>Sacred Components</h2>
            <div class="status-grid" id="components-grid">
                <!-- Components will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        let ws = null;
        
        function connectWebSocket() {
            ws = new WebSocket('ws://localhost:8765');
            
            ws.onopen = function() {
                document.getElementById('status').textContent = 'Connected (Real-time)';
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === 'status_update' || data.type === 'initial_status') {
                    updateDashboard(data.data);
                }
            };
            
            ws.onclose = function() {
                document.getElementById('status').textContent = 'Disconnected';
                setTimeout(connectWebSocket, 5000);
            };
        }
        
        function refreshData() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => updateDashboard(data))
                .catch(error => console.error('Error:', error));
        }
        
        function updateDashboard(data) {
            if (data.system) {
                document.getElementById('cpu').textContent = Math.round(data.system.cpu_percent);
                document.getElementById('memory').textContent = Math.round(data.system.memory_percent);
                document.getElementById('disk').textContent = Math.round(data.system.disk_usage_percent || 0);
            }
            
            if (data.sacred_components) {
                updateComponents(data.sacred_components);
            }
        }
        
        function updateComponents(components) {
            const grid = document.getElementById('components-grid');
            grid.innerHTML = '';
            
            const componentOrder = ['ATLAS', 'TATA', 'OBI-WAN', 'DOJO'];
            const symbols = { 'ATLAS': '▲', 'TATA': '▼', 'OBI-WAN': '●', 'DOJO': '◼' };
            
            componentOrder.forEach(name => {
                const status = components[name] || 'missing';
                const div = document.createElement('div');
                div.className = `component ${status}`;
                div.innerHTML = `
                    <div class="symbol">${symbols[name]}</div>
                    <strong>${name}</strong>
                    <div>Status: ${status.toUpperCase()}</div>
                `;
                grid.appendChild(div);
            });
        }
        
        // Initialize
        connectWebSocket();
        refreshData();
        
        // Refresh every 30 seconds as fallback
        setInterval(refreshData, 30000);
    </script>
</body>
</html>
"""

def main():
    """Main execution function."""
    import os
    
    monitor = SacredDashboardMonitor()
    
    try:
        print("🔮 Starting Sacred Component Dashboard Monitor")
        print("Dashboard available at: http://localhost:8080")
        print("WebSocket server on: ws://localhost:8765")
        print("Press Ctrl+C to stop")
        
        monitor.start_monitoring()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping monitoring system...")
        monitor.stop_monitoring()
        print("Monitor stopped.")

if __name__ == "__main__":
    main()
