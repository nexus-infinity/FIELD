#!/Users/jbear/FIELD/.venv/bin/python
"""
Mobile Conversation Client for OBI-WAN - SomaLink
Connects iPhone/Watch to the continuous conversation system on your Mac

This client script can be used to:
- Connect to the conversation system WebSocket
- Send voice input from iPhone/Watch
- Switch speakers remotely
- Receive real-time conversation updates
- Trigger manifestations from mobile devices

For integration with iOS Shortcuts or Watch complications
"""

import asyncio
import json
import websockets
import aiohttp
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConversationStatus:
    """Status of the conversation system"""
    conversation_active: bool
    current_speaker: str
    total_messages: int
    field_coherence: float
    sovereignty_integrity: float
    sacred_frequencies: Dict[str, float]
    connected_clients: int

class MobileConversationClient:
    """Client for connecting mobile devices to the conversation system"""
    
    def __init__(self, mac_host="localhost", websocket_port=8765, api_port=8766):
        self.mac_host = mac_host
        self.websocket_port = websocket_port
        self.api_port = api_port
        self.websocket_url = f"ws://{mac_host}:{websocket_port}"
        self.api_base_url = f"http://{mac_host}:{api_port}"
        
        self.websocket = None
        self.connected = False
        self.status = None
        
    async def connect(self) -> bool:
        """Connect to the conversation system"""
        try:
            # Test API connection first
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/status") as response:
                    if response.status == 200:
                        status_data = await response.json()
                        logger.info(f"Connected to conversation system API: {status_data}")
                        self.status = ConversationStatus(**status_data)
                    else:
                        logger.error(f"API connection failed: {response.status}")
                        return False
            
            # Connect WebSocket
            self.websocket = await websockets.connect(self.websocket_url)
            self.connected = True
            
            logger.info("Successfully connected to conversation system")
            print("🔗 Connected to OBI-WAN - SomaLink conversation system")
            print(f"🎵 Current speaker: {self.status.current_speaker}")
            print(f"💫 Field coherence: {self.status.field_coherence:.2f}")
            print(f"🔒 Sovereignty integrity: {self.status.sovereignty_integrity:.2f}")
            
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from the conversation system"""
        if self.websocket:
            await self.websocket.close()
        self.connected = False
        logger.info("Disconnected from conversation system")
    
    async def send_voice_input(self, text: str, speaker: Optional[str] = None) -> bool:
        """Send voice input to the conversation system"""
        try:
            data = {"text": text}
            if speaker:
                data["speaker"] = speaker
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/voice-input",
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Voice input sent successfully: {result}")
                        return True
                    else:
                        logger.error(f"Voice input failed: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error sending voice input: {e}")
            return False
    
    async def switch_speaker(self, speaker: str) -> bool:
        """Switch the active speaker"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/switch-speaker",
                    json={"speaker": speaker}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Speaker switched to {speaker}")
                        print(f"🎯 Switched to {speaker}")
                        return True
                    else:
                        logger.error(f"Speaker switch failed: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error switching speaker: {e}")
            return False
    
    async def trigger_manifestation(self, intent: str) -> bool:
        """Trigger a manifestation through Niama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/manifestation-trigger",
                    json={"intent": intent}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Manifestation triggered: {result}")
                        print(f"✨ Manifestation triggered: {intent}")
                        return True
                    else:
                        logger.error(f"Manifestation trigger failed: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error triggering manifestation: {e}")
            return False
    
    async def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/conversation-history") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("history", [])
                    else:
                        logger.error(f"History request failed: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    async def listen_for_updates(self):
        """Listen for real-time updates from the conversation system"""
        if not self.connected or not self.websocket:
            logger.error("Not connected to WebSocket")
            return
        
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self.handle_update(data)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
            self.connected = False
        except Exception as e:
            logger.error(f"Error listening for updates: {e}")
    
    async def handle_update(self, data: Dict[str, Any]):
        """Handle updates from the conversation system"""
        update_type = data.get("type")
        
        if update_type == "connection_established":
            print(f"✅ Connection established")
            print(f"🎵 Sacred frequencies: {data.get('sacred_frequencies', {})}")
            
        elif update_type == "new_message":
            speaker = data.get("speaker")
            content = data.get("content")
            frequency = data.get("frequency")
            potential = data.get("manifestation_potential", 0)
            
            print(f"\n🗣️  {speaker.upper()}: {content}")
            print(f"🎵 Frequency: {frequency}Hz | ✨ Potential: {potential:.2f}")
            
            if potential > 0.7:
                print("🔥 HIGH MANIFESTATION POTENTIAL!")
                
        elif update_type == "speaker_changed":
            new_speaker = data.get("new_speaker")
            frequency = data.get("frequency")
            print(f"🎯 Speaker changed to {new_speaker} ({frequency}Hz)")
            
        elif update_type == "voice_processed":
            input_text = data.get("input_text")
            current_speaker = data.get("current_speaker")
            print(f"🎤 Voice processed by {current_speaker}: {input_text}")
            
        else:
            logger.info(f"Unknown update type: {update_type}")
    
    async def send_websocket_message(self, message_type: str, **kwargs):
        """Send a message via WebSocket"""
        if not self.connected or not self.websocket:
            logger.error("Not connected to WebSocket")
            return False
        
        try:
            message = {"type": message_type, **kwargs}
            await self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
            return False
    
    async def request_sacred_tone(self, speaker: Optional[str] = None):
        """Request a sacred frequency tone"""
        speaker = speaker or self.status.current_speaker if self.status else "obiwan"
        return await self.send_websocket_message("sacred_frequency_tone", speaker=speaker)
    
    async def request_status_update(self):
        """Request a status update"""
        return await self.send_websocket_message("request_status")

class InteractiveClient:
    """Interactive command-line client for testing"""
    
    def __init__(self, client: MobileConversationClient):
        self.client = client
        
    async def run_interactive_session(self):
        """Run an interactive session"""
        print("\n" + "="*70)
        print("🎵 OBI-WAN - SomaLink Mobile Client")
        print("🔗 Interactive Conversation Interface")
        print("="*70)
        
        # Connect to system
        connected = await self.client.connect()
        if not connected:
            print("❌ Failed to connect to conversation system")
            return
        
        # Start listening for updates in background
        listen_task = asyncio.create_task(self.client.listen_for_updates())
        
        print("\nCommands:")
        print("  say <text>                - Send voice input")
        print("  switch <obiwan|somalink|niama> - Switch speaker")
        print("  manifest <intent>         - Trigger manifestation")
        print("  history                   - Show conversation history")
        print("  tone [speaker]            - Play sacred frequency tone")
        print("  status                    - Get system status")
        print("  help                      - Show this help")
        print("  quit                      - Exit")
        print("\nType your commands below:\n")
        
        try:
            while True:
                try:
                    command = input("🎤 > ").strip()
                    
                    if not command:
                        continue
                        
                    parts = command.split(None, 1)
                    cmd = parts[0].lower()
                    args = parts[1] if len(parts) > 1 else ""
                    
                    if cmd == "quit" or cmd == "exit":
                        break
                        
                    elif cmd == "say":
                        if args:
                            await self.client.send_voice_input(args)
                        else:
                            print("Usage: say <text>")
                            
                    elif cmd == "switch":
                        if args in ["obiwan", "somalink", "niama"]:
                            await self.client.switch_speaker(args)
                        else:
                            print("Usage: switch <obiwan|somalink|niama>")
                            
                    elif cmd == "manifest":
                        if args:
                            await self.client.trigger_manifestation(args)
                        else:
                            print("Usage: manifest <intent>")
                            
                    elif cmd == "history":
                        history = await self.client.get_conversation_history()
                        print("\n📜 Recent Conversation History:")
                        for msg in history[-10:]:  # Last 10 messages
                            timestamp = msg.get("timestamp", "")[:19]  # Remove microseconds
                            speaker = msg.get("speaker", "").upper()
                            content = msg.get("content", "")
                            print(f"  {timestamp} {speaker}: {content}")
                        print()
                        
                    elif cmd == "tone":
                        speaker = args if args in ["obiwan", "somalink", "niama"] else None
                        await self.client.request_sacred_tone(speaker)
                        
                    elif cmd == "status":
                        await self.client.request_status_update()
                        
                    elif cmd == "help":
                        print("\nCommands:")
                        print("  say <text>                - Send voice input")
                        print("  switch <obiwan|somalink|niama> - Switch speaker")
                        print("  manifest <intent>         - Trigger manifestation")
                        print("  history                   - Show conversation history")
                        print("  tone [speaker]            - Play sacred frequency tone")
                        print("  status                    - Get system status")
                        print("  help                      - Show this help")
                        print("  quit                      - Exit")
                        
                    else:
                        print(f"Unknown command: {cmd}. Type 'help' for available commands.")
                        
                    # Small delay to prevent overwhelming the system
                    await asyncio.sleep(0.1)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"Command error: {e}")
                    
        finally:
            listen_task.cancel()
            await self.client.disconnect()
            print("👋 Disconnected from conversation system")

async def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Command-line mode
        command = sys.argv[1].lower()
        client = MobileConversationClient()
        
        try:
            connected = await client.connect()
            if not connected:
                print("❌ Failed to connect to conversation system")
                return
            
            if command == "say" and len(sys.argv) > 2:
                text = " ".join(sys.argv[2:])
                await client.send_voice_input(text)
                
            elif command == "switch" and len(sys.argv) > 2:
                speaker = sys.argv[2]
                await client.switch_speaker(speaker)
                
            elif command == "manifest" and len(sys.argv) > 2:
                intent = " ".join(sys.argv[2:])
                await client.trigger_manifestation(intent)
                
            elif command == "history":
                history = await client.get_conversation_history()
                for msg in history[-10:]:
                    timestamp = msg.get("timestamp", "")[:19]
                    speaker = msg.get("speaker", "").upper()
                    content = msg.get("content", "")
                    print(f"{timestamp} {speaker}: {content}")
                    
            elif command == "status":
                status_data = {}
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{client.api_base_url}/status") as response:
                        if response.status == 200:
                            status_data = await response.json()
                            
                print("🎵 Conversation System Status:")
                print(f"  Active: {status_data.get('conversation_active', False)}")
                print(f"  Current speaker: {status_data.get('current_speaker', 'unknown')}")
                print(f"  Total messages: {status_data.get('total_messages', 0)}")
                print(f"  Field coherence: {status_data.get('field_coherence', 0):.2f}")
                print(f"  Connected clients: {status_data.get('connected_clients', 0)}")
                
            else:
                print("Usage:")
                print("  python mobile_conversation_client.py say <text>")
                print("  python mobile_conversation_client.py switch <obiwan|somalink|niama>") 
                print("  python mobile_conversation_client.py manifest <intent>")
                print("  python mobile_conversation_client.py history")
                print("  python mobile_conversation_client.py status")
                print("  python mobile_conversation_client.py  # Interactive mode")
                
        finally:
            await client.disconnect()
    else:
        # Interactive mode
        client = MobileConversationClient()
        interactive = InteractiveClient(client)
        await interactive.run_interactive_session()

if __name__ == "__main__":
    asyncio.run(main())
