#!/Users/jbear/FIELD/.venv/bin/python
"""
OBI-WAN - SomaLink Conversation Server Integration
Connects the continuous presence conversation system with existing FIELD infrastructure:
- Chakra servers (running on various ports)
- Train station coordination server
- Apple integration bridge (iPhone/Watch apps)
- DOJO manifestation server (port 3960)

This creates the missing link between the conversation system and your mobile interface.
"""

import asyncio
import json
import requests
import websockets
import aiohttp
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass, asdict
import sys

# Add FIELD directory to Python path for bridge imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our conversation system
from voice_presence_conversation import VoiceContinuousPresenceConversation
from obiwan_somalink_presence_conversation import ConversationMessage

# Import Apple integration
from bridge.apple_integration import (
    AppleEventsBridge, 
    FieldEvent, 
    FieldNodeType, 
    AppleAppType
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChakraServerEndpoint:
    """Represents a chakra server endpoint"""
    name: str
    port: int
    frequency: float
    node_symbol: str
    sacred_role: str
    
@dataclass
class ConversationEvent:
    """Event to send between conversation system and servers"""
    event_type: str
    source: str
    target: str
    data: Dict[str, Any]
    timestamp: str
    conversation_id: Optional[str] = None
    
class ServerDiscovery:
    """Discovers active FIELD servers"""
    
    def __init__(self):
        self.active_servers = {}
        self.last_scan = None
        
    async def discover_chakra_servers(self) -> Dict[str, ChakraServerEndpoint]:
        """Discover active chakra servers"""
        # Known chakra server ports
        potential_ports = [3960, 4170, 4285, 4396, 4417, 4528, 4639, 4741, 4852, 4963]
        active_servers = {}
        
        for port in potential_ports:
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as session:
                    async with session.get(f"http://localhost:{port}/status") as response:
                        if response.status == 200:
                            server_info = await response.json()
                            
                            server = ChakraServerEndpoint(
                                name=server_info.get("node_name", f"Server_{port}"),
                                port=port,
                                frequency=float(server_info.get("frequency", 432)),
                                node_symbol=server_info.get("node_symbol", "●"),
                                sacred_role=server_info.get("sacred_role", "Consciousness")
                            )
                            
                            active_servers[server.name] = server
                            logger.info(f"Discovered chakra server: {server.name} on port {port} ({server.frequency}Hz)")
                            
            except Exception as e:
                logger.debug(f"No server on port {port}: {e}")
                
        self.active_servers = active_servers
        self.last_scan = datetime.now()
        return active_servers

class ConversationServerBridge:
    """Bridges conversation system with FIELD server infrastructure"""
    
    def __init__(self, conversation_system: VoiceContinuousPresenceConversation):
        self.conversation_system = conversation_system
        self.server_discovery = ServerDiscovery()
        self.apple_bridge = AppleEventsBridge()
        self.active_connections = {}
        self.message_queue = asyncio.Queue()
        
        # WebSocket server for iPhone/Watch apps
        self.websocket_server = None
        self.connected_clients = set()
        
        # Configuration
        self.websocket_port = 8765
        self.api_port = 8766
        
    async def initialize(self) -> bool:
        """Initialize the server integration"""
        try:
            logger.info("Initializing conversation server bridge...")
            
            # Discover active chakra servers
            servers = await self.server_discovery.discover_chakra_servers()
            logger.info(f"Found {len(servers)} active chakra servers")
            
            # Initialize Apple bridge for iOS/macOS integration
            await self.apple_bridge.initialize()
            
            # Start WebSocket server for mobile apps
            await self.start_websocket_server()
            
            # Start HTTP API server for mobile apps
            await self.start_api_server()
            
            # Connect to train station if available
            await self.connect_to_train_station()
            
            logger.info("Conversation server bridge initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing server bridge: {e}")
            return False
    
    async def start_websocket_server(self):
        """Start WebSocket server for real-time mobile app communication"""
        async def handle_websocket(websocket, path):
            """Handle WebSocket connections from iPhone/Watch apps"""
            self.connected_clients.add(websocket)
            logger.info(f"Mobile client connected. Total clients: {len(self.connected_clients)}")
            
            try:
                # Send initial status
                await self.send_to_client(websocket, {
                    "type": "connection_established",
                    "conversation_active": self.conversation_system.voice_active,
                    "current_speaker": self.conversation_system.current_speaker,
                    "sacred_frequencies": {
                        "obiwan": self.conversation_system.text_conversation.obiwan.frequency,
                        "somalink": self.conversation_system.text_conversation.somalink.frequency,
                        "niama": self.conversation_system.text_conversation.niama.frequency
                    }
                })
                
                # Handle incoming messages
                async for message in websocket:
                    await self.handle_mobile_message(json.loads(message), websocket)
                    
            except websockets.exceptions.ConnectionClosed:
                logger.info("Mobile client disconnected")
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
            finally:
                self.connected_clients.discard(websocket)
        
        # Start WebSocket server
        self.websocket_server = await websockets.serve(
            handle_websocket, 
            "localhost", 
            self.websocket_port
        )
        logger.info(f"WebSocket server started on port {self.websocket_port}")
    
    async def start_api_server(self):
        """Start HTTP API server for mobile app integration"""
        from aiohttp import web
        
        app = web.Application()
        
        # API routes
        app.router.add_get('/status', self.handle_status_request)
        app.router.add_post('/voice-input', self.handle_voice_input)
        app.router.add_post('/switch-speaker', self.handle_switch_speaker)
        app.router.add_get('/conversation-history', self.handle_conversation_history)
        app.router.add_post('/manifestation-trigger', self.handle_manifestation_trigger)
        
        # CORS middleware for mobile apps
        async def cors_handler(request, handler):
            response = await handler(request)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        
        app.middlewares.append(cors_handler)
        
        # Start HTTP server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.api_port)
        await site.start()
        logger.info(f"HTTP API server started on port {self.api_port}")
    
    async def handle_status_request(self, request):
        """Handle status requests from mobile apps"""
        from aiohttp import web
        
        status = {
            "conversation_active": self.conversation_system.voice_active,
            "current_speaker": self.conversation_system.current_speaker,
            "total_messages": len(self.conversation_system.text_conversation.conversation_history),
            "field_coherence": self.conversation_system.text_conversation.obiwan._calculate_field_coherence(),
            "sovereignty_integrity": self.conversation_system.text_conversation.somalink._calculate_sovereignty_integrity(),
            "sacred_frequencies": {
                "obiwan": self.conversation_system.text_conversation.obiwan.frequency,
                "somalink": self.conversation_system.text_conversation.somalink.frequency,
                "niama": self.conversation_system.text_conversation.niama.frequency
            },
            "active_servers": {name: asdict(server) for name, server in self.server_discovery.active_servers.items()},
            "connected_clients": len(self.connected_clients)
        }
        
        return web.json_response(status)
    
    async def handle_voice_input(self, request):
        """Handle voice input from mobile apps"""
        from aiohttp import web
        
        try:
            data = await request.json()
            voice_text = data.get("text", "")
            speaker_override = data.get("speaker")
            
            if speaker_override:
                self.conversation_system.current_speaker = speaker_override
            
            # Process voice input through conversation system
            await self.conversation_system.handle_voice_input(voice_text)
            
            # Send response back to all connected clients
            await self.broadcast_to_clients({
                "type": "voice_processed",
                "input_text": voice_text,
                "current_speaker": self.conversation_system.current_speaker
            })
            
            return web.json_response({"success": True, "message": "Voice input processed"})
            
        except Exception as e:
            logger.error(f"Error handling voice input: {e}")
            return web.json_response({"success": False, "error": str(e)}, status=500)
    
    async def handle_switch_speaker(self, request):
        """Handle speaker switching from mobile apps"""
        from aiohttp import web
        
        try:
            data = await request.json()
            new_speaker = data.get("speaker", "obiwan")
            
            if new_speaker in ["obiwan", "somalink", "niama"]:
                self.conversation_system.current_speaker = new_speaker
                
                # Play sacred frequency tone for new speaker
                self.conversation_system.hearing_aid.play_sacred_frequency_tone(new_speaker, duration=0.5)
                
                # Broadcast to all clients
                await self.broadcast_to_clients({
                    "type": "speaker_changed",
                    "new_speaker": new_speaker,
                    "frequency": self.conversation_system.tts.voice_profiles[new_speaker]["frequency_base"]
                })
                
                return web.json_response({"success": True, "current_speaker": new_speaker})
            else:
                return web.json_response({"success": False, "error": "Invalid speaker"}, status=400)
                
        except Exception as e:
            logger.error(f"Error switching speaker: {e}")
            return web.json_response({"success": False, "error": str(e)}, status=500)
    
    async def handle_conversation_history(self, request):
        """Handle conversation history requests from mobile apps"""
        from aiohttp import web
        
        try:
            # Get recent conversation history
            history = []
            recent_messages = self.conversation_system.text_conversation.conversation_history[-20:]  # Last 20 messages
            
            for msg in recent_messages:
                history.append({
                    "timestamp": msg.timestamp.isoformat(),
                    "speaker": msg.speaker,
                    "content": msg.content,
                    "frequency": msg.frequency,
                    "consciousness_state": msg.consciousness_state,
                    "manifestation_potential": msg.manifestation_potential,
                    "field_resonance": msg.field_resonance
                })
            
            return web.json_response({"history": history})
            
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def handle_manifestation_trigger(self, request):
        """Handle manifestation trigger requests from mobile apps"""
        from aiohttp import web
        
        try:
            data = await request.json()
            manifestation_intent = data.get("intent", "")
            
            # Create high-potential message to trigger Niama
            trigger_message = ConversationMessage(
                timestamp=datetime.now(),
                speaker="mobile_app",
                content=f"Mobile manifestation request: {manifestation_intent}",
                frequency=256.0,  # Do frequency for manifestation
                consciousness_state="manifestation_request",
                manifestation_potential=0.9,  # High potential
                field_resonance=0.8
            )
            
            # Add to conversation and trigger manifestation check
            self.conversation_system.text_conversation.conversation_history.append(trigger_message)
            await asyncio.create_task(
                self.conversation_system.text_conversation._check_manifestation_potential()
            )
            
            # Send to DOJO server if available
            await self.send_to_dojo_server({
                "type": "manifestation_request",
                "intent": manifestation_intent,
                "source": "mobile_app",
                "timestamp": datetime.now().isoformat()
            })
            
            return web.json_response({"success": True, "message": "Manifestation request processed"})
            
        except Exception as e:
            logger.error(f"Error handling manifestation trigger: {e}")
            return web.json_response({"success": False, "error": str(e)}, status=500)
    
    async def handle_mobile_message(self, message: Dict[str, Any], websocket):
        """Handle messages from mobile app WebSocket connections"""
        try:
            message_type = message.get("type")
            
            if message_type == "voice_input":
                await self.conversation_system.handle_voice_input(message.get("text", ""))
                
            elif message_type == "switch_speaker":
                speaker = message.get("speaker", "obiwan")
                if speaker in ["obiwan", "somalink", "niama"]:
                    self.conversation_system.current_speaker = speaker
                    await self.send_to_client(websocket, {
                        "type": "speaker_changed",
                        "new_speaker": speaker
                    })
                    
            elif message_type == "request_status":
                status = await self.get_conversation_status()
                await self.send_to_client(websocket, {
                    "type": "status_update",
                    "status": status
                })
                
            elif message_type == "sacred_frequency_tone":
                speaker = message.get("speaker", self.conversation_system.current_speaker)
                self.conversation_system.hearing_aid.play_sacred_frequency_tone(speaker)
                
        except Exception as e:
            logger.error(f"Error handling mobile message: {e}")
    
    async def send_to_client(self, websocket, message: Dict[str, Any]):
        """Send message to specific WebSocket client"""
        try:
            await websocket.send(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending to client: {e}")
    
    async def broadcast_to_clients(self, message: Dict[str, Any]):
        """Broadcast message to all connected WebSocket clients"""
        if self.connected_clients:
            disconnected = set()
            for client in self.connected_clients:
                try:
                    await client.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(client)
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {e}")
                    disconnected.add(client)
            
            # Remove disconnected clients
            self.connected_clients -= disconnected
    
    async def connect_to_train_station(self):
        """Connect to train station coordination server"""
        try:
            # Try common train station ports
            train_station_ports = [8080, 8000, 3000, 5000]
            
            for port in train_station_ports:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"http://localhost:{port}/health") as response:
                            if response.status == 200:
                                logger.info(f"Connected to train station on port {port}")
                                
                                # Register with train station
                                registration_data = {
                                    "service": "obiwan_somalink_conversation",
                                    "port": self.websocket_port,
                                    "capabilities": [
                                        "voice_conversation",
                                        "sacred_frequency_generation",
                                        "manifestation_triggering",
                                        "mobile_integration"
                                    ]
                                }
                                
                                async with session.post(
                                    f"http://localhost:{port}/register",
                                    json=registration_data
                                ) as reg_response:
                                    if reg_response.status == 200:
                                        logger.info("Successfully registered with train station")
                                    return True
                                    
                except Exception as e:
                    logger.debug(f"Train station not found on port {port}: {e}")
                    
            logger.info("Train station not found - operating in standalone mode")
            return False
            
        except Exception as e:
            logger.error(f"Error connecting to train station: {e}")
            return False
    
    async def send_to_dojo_server(self, data: Dict[str, Any]):
        """Send data to DOJO manifestation server"""
        dojo_server = None
        for name, server in self.server_discovery.active_servers.items():
            if "DOJO" in name.upper() or server.port == 3960:
                dojo_server = server
                break
        
        if dojo_server:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"http://localhost:{dojo_server.port}/manifestation",
                        json=data
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            logger.info(f"DOJO server response: {result}")
                            return result
                        else:
                            logger.warning(f"DOJO server returned status {response.status}")
                            
            except Exception as e:
                logger.error(f"Error sending to DOJO server: {e}")
        else:
            logger.warning("DOJO server not found")
        
        return None
    
    async def send_to_apple_integration(self, event_data: Dict[str, Any]):
        """Send event to Apple integration bridge"""
        try:
            # Create FIELD event for Apple integration
            field_event = FieldEvent(
                node_type=FieldNodeType.OBI_WAN,
                event_type=event_data.get("event_type", "data_intake"),
                data=event_data,
                timestamp=datetime.now(),
                source="conversation_system"
            )
            
            # Send through Apple bridge
            success = await self.apple_bridge.send_field_event(field_event)
            
            if success:
                logger.info("Event sent to Apple integration successfully")
            else:
                logger.warning("Failed to send event to Apple integration")
                
            return success
            
        except Exception as e:
            logger.error(f"Error sending to Apple integration: {e}")
            return False
    
    async def get_conversation_status(self) -> Dict[str, Any]:
        """Get comprehensive conversation system status"""
        return {
            "conversation_active": self.conversation_system.voice_active,
            "current_speaker": self.conversation_system.current_speaker,
            "total_messages": len(self.conversation_system.text_conversation.conversation_history),
            "field_coherence": self.conversation_system.text_conversation.obiwan._calculate_field_coherence(),
            "sovereignty_integrity": self.conversation_system.text_conversation.somalink._calculate_sovereignty_integrity(),
            "sacred_frequencies": {
                "obiwan": self.conversation_system.text_conversation.obiwan.frequency,
                "somalink": self.conversation_system.text_conversation.somalink.frequency, 
                "niama": self.conversation_system.text_conversation.niama.frequency
            },
            "active_servers": len(self.server_discovery.active_servers),
            "connected_clients": len(self.connected_clients),
            "last_voice_input": self.conversation_system.last_voice_input.isoformat()
        }
    
    async def monitor_conversation_events(self):
        """Monitor conversation events and relay to servers/mobile apps"""
        while True:
            try:
                # Check for new conversation messages
                if hasattr(self.conversation_system, 'text_conversation'):
                    recent_messages = self.conversation_system.text_conversation.conversation_history[-1:]
                    
                    for message in recent_messages:
                        # Broadcast to mobile clients
                        await self.broadcast_to_clients({
                            "type": "new_message",
                            "speaker": message.speaker,
                            "content": message.content,
                            "frequency": message.frequency,
                            "manifestation_potential": message.manifestation_potential,
                            "timestamp": message.timestamp.isoformat()
                        })
                        
                        # Send high-potential messages to DOJO
                        if message.manifestation_potential > 0.7:
                            await self.send_to_dojo_server({
                                "type": "high_manifestation_potential",
                                "message": message.content,
                                "speaker": message.speaker,
                                "potential": message.manifestation_potential
                            })
                        
                        # Send to Apple integration for Notes/Calendar
                        if message.speaker == "niama":
                            await self.send_to_apple_integration({
                                "event_type": "documentation",
                                "content": message.content,
                                "speaker": message.speaker
                            })
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring conversation events: {e}")
                await asyncio.sleep(10)

async def main():
    """Main function to start the integrated conversation system"""
    try:
        print("🚀 Starting Integrated OBI-WAN - SomaLink Conversation System")
        print("🔗 Connecting to existing FIELD servers and mobile apps...")
        
        # Initialize conversation system
        conversation_system = VoiceContinuousPresenceConversation()
        
        # Initialize server bridge
        server_bridge = ConversationServerBridge(conversation_system)
        
        # Initialize everything
        bridge_initialized = await server_bridge.initialize()
        if not bridge_initialized:
            print("⚠️  Server bridge initialization failed, continuing in standalone mode")
        
        # Start conversation system
        await conversation_system.start_voice_conversation()
        
        # Start monitoring task
        monitor_task = asyncio.create_task(server_bridge.monitor_conversation_events())
        
        print("✅ Integrated system running!")
        print(f"📱 Mobile WebSocket: ws://localhost:{server_bridge.websocket_port}")
        print(f"🌐 HTTP API: http://localhost:{server_bridge.api_port}")
        print("🎵 Voice conversation active with server integration")
        print("=" * 70)
        
        # Run until interrupted
        await asyncio.gather(
            conversation_system.monitor_voice_activity(),
            monitor_task
        )
        
    except KeyboardInterrupt:
        print("\nShutting down integrated system...")
    except Exception as e:
        logger.error(f"System error: {e}")
    finally:
        if 'conversation_system' in locals():
            await conversation_system.stop_voice_conversation()
        if 'server_bridge' in locals():
            await server_bridge.apple_bridge.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
