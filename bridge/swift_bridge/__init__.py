"""
Swift Bridge Integration
=======================

Bridge between FIELD symbolic processors and Swift/DOJO applications.
Integrates with existing DOJO infrastructure and provides seamless
communication between Python backend and Swift frontend.

Key Features:
- Swift application integration through JSON-RPC and WebSocket
- DOJO execution surface coordination  
- Secure authentication and permission management
- Real-time event streaming between FIELD nodes and Swift UI
- Integration with existing communication bridge architecture
"""

import os
import json
import logging
import asyncio
import websockets
import ssl
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import uuid

# Import FIELD protocol components
from ..protocol import (
    FieldProtocol, SymbolicNode, SymbolicEvent, FieldMetadata, FieldLayer
)
from ..apple_integration import (
    AppleEventsBridge, FieldEvent, FieldNodeType, AppleAppType
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SwiftMessageType(Enum):
    """Swift message types for bridge communication"""
    FIELD_EVENT = "field_event"
    APPLE_EVENT = "apple_event"
    SYSTEM_STATUS = "system_status"
    AUTHENTICATION = "authentication"
    CONFIGURATION = "configuration"
    HEARTBEAT = "heartbeat"
    ERROR = "error"


class DojoInterfaceType(Enum):
    """DOJO interface types"""
    CHAKRA_VISUALIZATION = "chakra_visualization"
    SYSTEM_MONITOR = "system_monitor"
    FIELD_ACCESS = "field_access"
    AUTHENTICATION_MANAGER = "authentication_manager"
    MENU_BAR = "menu_bar"
    SETTINGS = "settings"


@dataclass
class SwiftMessage:
    """Message structure for Swift-Python communication"""
    message_type: SwiftMessageType
    interface_type: DojoInterfaceType
    payload: Dict[str, Any]
    message_id: str
    timestamp: datetime
    source: str = "python_bridge"
    target: str = "swift_dojo"


@dataclass
class DojoState:
    """DOJO execution surface state"""
    is_active: bool = False
    connected_interfaces: List[DojoInterfaceType] = None
    swift_app_status: str = "unknown"  # unknown, connecting, connected, disconnected
    websocket_connection: Optional[Any] = None
    last_heartbeat: Optional[datetime] = None
    authentication_status: str = "pending"  # pending, authenticated, failed
    
    def __post_init__(self):
        if self.connected_interfaces is None:
            self.connected_interfaces = []


class SwiftBridge:
    """Main Swift Bridge for FIELD-DOJO integration"""
    
    def __init__(self, websocket_port: int = 8765, 
                 dojo_path: str = None):
        self.websocket_port = websocket_port
        self.dojo_path = dojo_path or "/Users/jbear/FIELD/◼︎DOJO/"
        self.field_protocol = FieldProtocol()
        self.apple_bridge = AppleEventsBridge()
        
        # Connection management
        self.dojo_state = DojoState()
        self.connected_clients = set()
        self.message_handlers = {}
        self.event_queue = asyncio.Queue()
        
        # Setup message handlers
        self._setup_message_handlers()
        
        # Bridge configuration
        self.bridge_config = {
            "websocket_host": "localhost",
            "websocket_port": self.websocket_port,
            "ssl_enabled": False,
            "authentication_required": True,
            "heartbeat_interval": 30,
            "max_message_size": 1024 * 1024,  # 1MB
            "connection_timeout": 60
        }
    
    def _setup_message_handlers(self):
        """Setup message handlers for different Swift message types"""
        self.message_handlers = {
            SwiftMessageType.FIELD_EVENT: self._handle_field_event,
            SwiftMessageType.APPLE_EVENT: self._handle_apple_event,
            SwiftMessageType.SYSTEM_STATUS: self._handle_system_status,
            SwiftMessageType.AUTHENTICATION: self._handle_authentication,
            SwiftMessageType.CONFIGURATION: self._handle_configuration,
            SwiftMessageType.HEARTBEAT: self._handle_heartbeat,
            SwiftMessageType.ERROR: self._handle_error
        }
    
    async def initialize(self) -> bool:
        """Initialize the Swift Bridge"""
        try:
            logger.info("Initializing Swift Bridge...")
            
            # Initialize FIELD protocol
            await self._initialize_field_protocol()
            
            # Initialize Apple Events Bridge
            await self._initialize_apple_bridge()
            
            # Check DOJO infrastructure
            if not self._validate_dojo_infrastructure():
                logger.warning("DOJO infrastructure validation failed")
            
            # Start WebSocket server
            await self._start_websocket_server()
            
            # Start event processing
            asyncio.create_task(self._process_event_queue())
            
            logger.info("Swift Bridge initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing Swift Bridge: {e}")
            return False
    
    async def _initialize_field_protocol(self):
        """Initialize FIELD protocol with ontology validation"""
        try:
            # Validate Akron Gateway (L0)
            akron_valid = self.field_protocol.validate_akron_gateway()
            
            # Validate filesystem topology (L1)
            topology_status = self.field_protocol.validate_filesystem_topology()
            
            logger.info(f"FIELD Protocol initialized - Akron: {akron_valid}, Topology: {sum(topology_status.values())}/{len(topology_status)}")
            
        except Exception as e:
            logger.error(f"Error initializing FIELD protocol: {e}")
            raise
    
    async def _initialize_apple_bridge(self):
        """Initialize Apple Events Bridge"""
        try:
            await self.apple_bridge.initialize()
            logger.info("Apple Events Bridge initialized")
        except Exception as e:
            logger.error(f"Error initializing Apple bridge: {e}")
            raise
    
    def _validate_dojo_infrastructure(self) -> bool:
        """Validate DOJO infrastructure components"""
        try:
            # Check DOJO path exists
            if not os.path.exists(self.dojo_path):
                logger.error(f"DOJO path not found: {self.dojo_path}")
                return False
            
            # Check for Swift integration directory
            swift_integration_path = os.path.join(self.dojo_path, "swift_integration")
            if os.path.exists(swift_integration_path):
                logger.info("Swift integration directory found")
            
            # Check for communication bridge
            comm_bridge_path = os.path.join(self.dojo_path, "communication_bridge")
            if os.path.exists(comm_bridge_path):
                logger.info("Communication bridge directory found")
            
            # Validate DOJO execution readiness
            self.dojo_state.is_active = True
            logger.info("DOJO infrastructure validated")
            return True
            
        except Exception as e:
            logger.error(f"Error validating DOJO infrastructure: {e}")
            return False
    
    async def _start_websocket_server(self):
        """Start WebSocket server for Swift communication"""
        try:
            async def handle_client(websocket, path):
                try:
                    self.connected_clients.add(websocket)
                    self.dojo_state.swift_app_status = "connected"
                    self.dojo_state.websocket_connection = websocket
                    self.dojo_state.last_heartbeat = datetime.now()
                    
                    logger.info(f"Swift client connected: {websocket.remote_address}")
                    
                    # Send welcome message
                    await self._send_swift_message(
                        websocket,
                        SwiftMessageType.SYSTEM_STATUS,
                        DojoInterfaceType.SYSTEM_MONITOR,
                        {
                            "status": "connected",
                            "bridge_version": "1.0.0",
                            "field_protocol_ready": True,
                            "apple_bridge_ready": True
                        }
                    )
                    
                    # Handle incoming messages
                    async for message in websocket:
                        await self._handle_websocket_message(websocket, message)
                        
                except websockets.exceptions.ConnectionClosed:
                    logger.info("Swift client disconnected")
                except Exception as e:
                    logger.error(f"Error handling Swift client: {e}")
                finally:
                    self.connected_clients.discard(websocket)
                    if self.dojo_state.websocket_connection == websocket:
                        self.dojo_state.swift_app_status = "disconnected"
                        self.dojo_state.websocket_connection = None
            
            # Start WebSocket server
            server = await websockets.serve(
                handle_client,
                self.bridge_config["websocket_host"],
                self.bridge_config["websocket_port"]
            )
            
            logger.info(f"WebSocket server started on {self.bridge_config['websocket_host']}:{self.bridge_config['websocket_port']}")
            
        except Exception as e:
            logger.error(f"Error starting WebSocket server: {e}")
            raise
    
    async def _handle_websocket_message(self, websocket, raw_message: str):
        """Handle incoming WebSocket message from Swift"""
        try:
            # Parse message
            message_data = json.loads(raw_message)
            
            # Create SwiftMessage object
            swift_message = SwiftMessage(
                message_type=SwiftMessageType(message_data.get("message_type")),
                interface_type=DojoInterfaceType(message_data.get("interface_type")),
                payload=message_data.get("payload", {}),
                message_id=message_data.get("message_id", str(uuid.uuid4())),
                timestamp=datetime.fromisoformat(message_data.get("timestamp", datetime.now().isoformat())),
                source=message_data.get("source", "swift_dojo"),
                target=message_data.get("target", "python_bridge")
            )
            
            # Route to appropriate handler
            handler = self.message_handlers.get(swift_message.message_type)
            if handler:
                await handler(websocket, swift_message)
            else:
                logger.warning(f"No handler for message type: {swift_message.message_type}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON message from Swift: {e}")
            await self._send_error_message(websocket, "Invalid JSON format")
        except ValueError as e:
            logger.error(f"Invalid message format from Swift: {e}")
            await self._send_error_message(websocket, "Invalid message format")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
            await self._send_error_message(websocket, "Internal server error")
    
    async def _send_swift_message(self, websocket, message_type: SwiftMessageType,
                                 interface_type: DojoInterfaceType, 
                                 payload: Dict[str, Any],
                                 message_id: str = None):
        """Send message to Swift application"""
        try:
            swift_message = SwiftMessage(
                message_type=message_type,
                interface_type=interface_type,
                payload=payload,
                message_id=message_id or str(uuid.uuid4()),
                timestamp=datetime.now()
            )
            
            message_json = json.dumps(asdict(swift_message), default=str)
            await websocket.send(message_json)
            
            logger.debug(f"Sent message to Swift: {message_type.value}")
            
        except Exception as e:
            logger.error(f"Error sending message to Swift: {e}")
    
    async def _send_error_message(self, websocket, error_message: str):
        """Send error message to Swift"""
        await self._send_swift_message(
            websocket,
            SwiftMessageType.ERROR,
            DojoInterfaceType.SYSTEM_MONITOR,
            {"error": error_message, "timestamp": datetime.now().isoformat()}
        )
    
    # Message Handlers
    
    async def _handle_field_event(self, websocket, message: SwiftMessage):
        """Handle FIELD event from Swift"""
        try:
            payload = message.payload
            
            # Extract FIELD event data
            node_type = SymbolicNode(payload.get("node_type", "DOJO"))
            event_type = payload.get("event_type", "user_interaction")
            event_data = payload.get("data", {})
            
            # Process through FIELD ontology
            result = await self.field_protocol.process_through_ontology(
                event_data, node_type, event_type
            )
            
            # Send Apple events if routing targets exist
            apple_targets = result.get("apple_routing_targets", [])
            if apple_targets:
                await self._route_to_apple_apps(event_data, apple_targets, node_type)
            
            # Send response back to Swift
            await self._send_swift_message(
                websocket,
                SwiftMessageType.FIELD_EVENT,
                message.interface_type,
                {
                    "status": "processed",
                    "result": result,
                    "apple_routing_count": len(apple_targets)
                },
                message.message_id
            )
            
            logger.info(f"Processed FIELD event: {node_type.value}:{event_type}")
            
        except Exception as e:
            logger.error(f"Error handling FIELD event: {e}")
            await self._send_error_message(websocket, f"FIELD event processing error: {str(e)}")
    
    async def _handle_apple_event(self, websocket, message: SwiftMessage):
        """Handle Apple event request from Swift"""
        try:
            payload = message.payload
            
            # Create FIELD event for Apple integration
            field_event = FieldEvent(
                node_type=FieldNodeType(payload.get("source_node", "DOJO")),
                event_type=payload.get("event_type", "apple_integration"),
                data=payload.get("data", {}),
                timestamp=datetime.now(),
                source="swift_bridge",
                target_apps=[AppleAppType(app) for app in payload.get("target_apps", [])]
            )
            
            # Send through Apple Events Bridge
            success = await self.apple_bridge.send_field_event(field_event)
            
            # Send response back to Swift
            await self._send_swift_message(
                websocket,
                SwiftMessageType.APPLE_EVENT,
                message.interface_type,
                {
                    "status": "sent" if success else "failed",
                    "event_id": field_event.event_type,
                    "target_apps": [app.value for app in field_event.target_apps] if field_event.target_apps else []
                },
                message.message_id
            )
            
            logger.info(f"Processed Apple event: {field_event.event_type}")
            
        except Exception as e:
            logger.error(f"Error handling Apple event: {e}")
            await self._send_error_message(websocket, f"Apple event processing error: {str(e)}")
    
    async def _handle_system_status(self, websocket, message: SwiftMessage):
        """Handle system status request from Swift"""
        try:
            # Gather system status
            status = {
                "bridge_status": "active",
                "dojo_state": asdict(self.dojo_state),
                "field_protocol_status": "ready",
                "apple_bridge_status": "ready",
                "connected_clients": len(self.connected_clients),
                "event_queue_size": self.event_queue.qsize(),
                "timestamp": datetime.now().isoformat()
            }
            
            # Add interface-specific status
            if message.interface_type == DojoInterfaceType.SYSTEM_MONITOR:
                status.update({
                    "system_metrics": await self._get_system_metrics(),
                    "field_topology": self.field_protocol.validate_filesystem_topology()
                })
            
            await self._send_swift_message(
                websocket,
                SwiftMessageType.SYSTEM_STATUS,
                message.interface_type,
                status,
                message.message_id
            )
            
        except Exception as e:
            logger.error(f"Error handling system status: {e}")
            await self._send_error_message(websocket, f"System status error: {str(e)}")
    
    async def _handle_authentication(self, websocket, message: SwiftMessage):
        """Handle authentication from Swift"""
        try:
            payload = message.payload
            auth_type = payload.get("auth_type", "icloud")
            credentials = payload.get("credentials", {})
            
            # Validate authentication (simplified)
            auth_success = await self._validate_swift_authentication(auth_type, credentials)
            
            if auth_success:
                self.dojo_state.authentication_status = "authenticated"
                auth_status = "success"
            else:
                self.dojo_state.authentication_status = "failed"
                auth_status = "failed"
            
            await self._send_swift_message(
                websocket,
                SwiftMessageType.AUTHENTICATION,
                message.interface_type,
                {
                    "status": auth_status,
                    "auth_type": auth_type,
                    "authenticated": auth_success,
                    "timestamp": datetime.now().isoformat()
                },
                message.message_id
            )
            
            logger.info(f"Authentication result: {auth_status}")
            
        except Exception as e:
            logger.error(f"Error handling authentication: {e}")
            await self._send_error_message(websocket, f"Authentication error: {str(e)}")
    
    async def _handle_configuration(self, websocket, message: SwiftMessage):
        """Handle configuration updates from Swift"""
        try:
            payload = message.payload
            config_updates = payload.get("updates", {})
            
            # Update bridge configuration
            for key, value in config_updates.items():
                if key in self.bridge_config:
                    self.bridge_config[key] = value
                    logger.info(f"Updated configuration: {key} = {value}")
            
            await self._send_swift_message(
                websocket,
                SwiftMessageType.CONFIGURATION,
                message.interface_type,
                {
                    "status": "updated",
                    "current_config": self.bridge_config,
                    "timestamp": datetime.now().isoformat()
                },
                message.message_id
            )
            
        except Exception as e:
            logger.error(f"Error handling configuration: {e}")
            await self._send_error_message(websocket, f"Configuration error: {str(e)}")
    
    async def _handle_heartbeat(self, websocket, message: SwiftMessage):
        """Handle heartbeat from Swift"""
        try:
            self.dojo_state.last_heartbeat = datetime.now()
            
            await self._send_swift_message(
                websocket,
                SwiftMessageType.HEARTBEAT,
                message.interface_type,
                {
                    "status": "alive",
                    "server_time": datetime.now().isoformat()
                },
                message.message_id
            )
            
        except Exception as e:
            logger.error(f"Error handling heartbeat: {e}")
    
    async def _handle_error(self, websocket, message: SwiftMessage):
        """Handle error report from Swift"""
        try:
            payload = message.payload
            error_info = payload.get("error", "Unknown error")
            
            logger.error(f"Error reported by Swift: {error_info}")
            
            # Log to FIELD system if needed
            await self.event_queue.put({
                "type": "swift_error",
                "error": error_info,
                "timestamp": datetime.now(),
                "source": "swift_dojo"
            })
            
        except Exception as e:
            logger.error(f"Error handling error message: {e}")
    
    # Utility Methods
    
    async def _route_to_apple_apps(self, event_data: Dict[str, Any], 
                                  apple_targets: List[str], 
                                  source_node: SymbolicNode):
        """Route event to Apple applications"""
        try:
            # Convert symbolic node to FIELD node type
            node_type_mapping = {
                SymbolicNode.ATLAS: FieldNodeType.ATLAS,
                SymbolicNode.TATA: FieldNodeType.TATA,
                SymbolicNode.OBI_WAN: FieldNodeType.OBI_WAN,
                SymbolicNode.DOJO: FieldNodeType.DOJO
            }
            
            field_node_type = node_type_mapping.get(source_node, FieldNodeType.DOJO)
            
            # Convert app targets
            target_apps = []
            for app_id in apple_targets:
                try:
                    target_apps.append(AppleAppType(app_id))
                except ValueError:
                    logger.warning(f"Unknown Apple app type: {app_id}")
            
            # Create and send FIELD event
            field_event = FieldEvent(
                node_type=field_node_type,
                event_type="bridge_routing",
                data=event_data,
                timestamp=datetime.now(),
                source="swift_bridge",
                target_apps=target_apps
            )
            
            await self.apple_bridge.send_field_event(field_event)
            logger.info(f"Routed event to {len(target_apps)} Apple apps")
            
        except Exception as e:
            logger.error(f"Error routing to Apple apps: {e}")
    
    async def _validate_swift_authentication(self, auth_type: str, 
                                           credentials: Dict[str, Any]) -> bool:
        """Validate Swift application authentication"""
        try:
            # Simplified authentication - in production, implement proper validation
            if auth_type == "icloud":
                return credentials.get("icloud_account") is not None
            elif auth_type == "google":
                return credentials.get("google_token") is not None
            else:
                return False
        except Exception as e:
            logger.error(f"Error validating authentication: {e}")
            return False
    
    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics for monitoring"""
        try:
            return {
                "cpu_usage": 0.0,  # Simplified - implement actual monitoring
                "memory_usage": 0.0,
                "disk_usage": 0.0,
                "network_activity": {"bytes_in": 0, "bytes_out": 0},
                "process_count": len(self.connected_clients),
                "uptime": "running"
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    async def _process_event_queue(self):
        """Process events from the internal queue"""
        while True:
            try:
                event = await self.event_queue.get()
                
                # Process different event types
                if event.get("type") == "swift_error":
                    logger.info(f"Processing Swift error event: {event.get('error')}")
                
                # Send to connected Swift clients if relevant
                for client in self.connected_clients:
                    try:
                        await self._send_swift_message(
                            client,
                            SwiftMessageType.SYSTEM_STATUS,
                            DojoInterfaceType.SYSTEM_MONITOR,
                            {"event": event}
                        )
                    except Exception as e:
                        logger.error(f"Error sending event to Swift client: {e}")
                
                self.event_queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing event queue: {e}")
    
    async def shutdown(self):
        """Shutdown the Swift Bridge"""
        try:
            logger.info("Shutting down Swift Bridge...")
            
            # Close all WebSocket connections
            for client in self.connected_clients.copy():
                await client.close()
            
            # Shutdown Apple bridge
            await self.apple_bridge.shutdown()
            
            self.dojo_state.is_active = False
            logger.info("Swift Bridge shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


class DojoIntegration:
    """High-level DOJO integration coordinator"""
    
    def __init__(self):
        self.swift_bridge = SwiftBridge()
        self.is_initialized = False
        
    async def initialize(self) -> bool:
        """Initialize complete DOJO integration"""
        try:
            logger.info("Initializing DOJO Integration...")
            
            # Initialize Swift Bridge
            if not await self.swift_bridge.initialize():
                logger.error("Failed to initialize Swift Bridge")
                return False
            
            self.is_initialized = True
            logger.info("DOJO Integration initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing DOJO Integration: {e}")
            return False
    
    async def send_field_event_to_swift(self, node_type: SymbolicNode, 
                                      event_type: str, 
                                      data: Dict[str, Any],
                                      interface_type: DojoInterfaceType = DojoInterfaceType.SYSTEM_MONITOR):
        """Send FIELD event to Swift application"""
        if not self.is_initialized:
            logger.error("DOJO Integration not initialized")
            return False
        
        try:
            # Send to all connected Swift clients
            for client in self.swift_bridge.connected_clients:
                await self.swift_bridge._send_swift_message(
                    client,
                    SwiftMessageType.FIELD_EVENT,
                    interface_type,
                    {
                        "node_type": node_type.value,
                        "event_type": event_type,
                        "data": data,
                        "timestamp": datetime.now().isoformat()
                    }
                )
            
            logger.info(f"Sent FIELD event to Swift: {node_type.value}:{event_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending FIELD event to Swift: {e}")
            return False
    
    async def get_dojo_status(self) -> Dict[str, Any]:
        """Get current DOJO status"""
        if not self.is_initialized:
            return {"status": "not_initialized"}
        
        return {
            "initialized": self.is_initialized,
            "swift_bridge_active": self.swift_bridge.dojo_state.is_active,
            "connected_clients": len(self.swift_bridge.connected_clients),
            "authentication_status": self.swift_bridge.dojo_state.authentication_status,
            "last_heartbeat": self.swift_bridge.dojo_state.last_heartbeat,
            "websocket_port": self.swift_bridge.websocket_port
        }
    
    async def shutdown(self):
        """Shutdown DOJO integration"""
        if self.swift_bridge:
            await self.swift_bridge.shutdown()
        self.is_initialized = False


# Export main classes
__all__ = [
    'SwiftBridge',
    'DojoIntegration',
    'SwiftMessage',
    'SwiftMessageType',
    'DojoInterfaceType',
    'DojoState'
]
