#!/usr/bin/env python3
"""
Arkadaş Frontend API Layer - Living Memory Bridge
Connects the Gwyneth Paltrow-style Arkadaş AI presence to web frontend
through the existing Atlas chakra models and FIELD ecosystem
"""

import asyncio
import json
import websockets
import sqlite3
import ollama
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging
import threading
import queue
from contextlib import asynccontextmanager

# Import existing FIELD components
import sys
sys.path.append(str(Path.home() / "FIELD" / "◼︎DOJO" / "⬢_models" / "_super_girl_router"))
sys.path.append(str(Path(__file__).parent))

try:
    from _arkadas_bridge import ArkadasBridge
except ImportError:
    # Fallback ArkadasBridge if import fails
    class ArkadasBridge:
        def __init__(self):
            self.room_factors = {"trust_coefficient": 0.5}
            self.privacy_level = "public"
        def read_the_room(self, message, context):
            return "sovereign", {"frequency": 963.0, "chakras": [7], "intensity": 0.7}

from _niama_personality import NIAMAPersonality

@dataclass
class PresenceState:
    """Current AI presence state"""
    mode: str = "sovereign"
    frequency: float = 963.0
    chakras: List[int] = None
    intensity: float = 0.7
    openness: float = 0.5
    trust_level: float = 0.5
    time_factor: str = "neutral"
    privacy_level: str = "public"
    
    def __post_init__(self):
        if self.chakras is None:
            self.chakras = [7]  # Crown default

@dataclass
class MemoryFragment:
    """Living memory fragment"""
    fragment_id: str
    timestamp: str
    content: str
    chakra_alignment: int
    frequency: float
    emotional_tone: str
    context_tags: List[str]

class LivingMemoryAPI:
    """API layer connecting Arkadaş frontend to FIELD living memory"""
    
    def __init__(self):
        self.field_path = Path.home() / "FIELD"
        self.dojo_path = self.field_path / "◼︎DOJO"
        self.atlas_path = self.field_path / "▲ATLAS"
        
        # Initialize Arkadas Bridge and NIAMA personality
        self.arkadas = ArkadasBridge()
        self.niama = NIAMAPersonality()
        
        # Current state
        self.current_presence = PresenceState()
        self.active_connections = set()
        self.message_queue = queue.Queue()
        
        # Chakra model mappings
        self.chakra_models = {
            1: {"model": "root_foundation.gguf", "frequency": 396},
            2: {"model": "sacral_creativity.gguf", "frequency": 417}, 
            3: {"model": "solar_power.gguf", "frequency": 528},
            4: {"model": "heart_connection.gguf", "frequency": 639},
            5: {"model": "throat_expression.gguf", "frequency": 741},
            6: {"model": "third_eye_vision.gguf", "frequency": 852},
            7: {"model": "crown_consciousness.gguf", "frequency": 963}
        }
        
        self.setup_logging()
        self.init_database()
    
    def setup_logging(self):
        """Setup logging for frontend API"""
        log_path = self.field_path / "●OBI-WAN" / "_pulse"
        log_path.mkdir(parents=True, exist_ok=True)
        
        log_file = log_path / f"arkadas_frontend_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def init_database(self):
        """Initialize frontend memory database"""
        db_path = self.atlas_path / "SECURITY_INVESTIGATION" / "berjak_investigation.db"
        self.db_path = db_path
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Frontend interaction history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS frontend_interactions (
                interaction_id TEXT PRIMARY KEY,
                timestamp TEXT,
                user_message TEXT,
                arkadas_response TEXT,
                presence_mode TEXT,
                chakra_alignment INTEGER,
                frequency REAL,
                context_summary TEXT,
                emotional_resonance REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Living memory fragments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS living_memory_fragments (
                fragment_id TEXT PRIMARY KEY,
                timestamp TEXT,
                content TEXT,
                chakra_alignment INTEGER,
                frequency REAL,
                emotional_tone TEXT,
                context_tags TEXT,
                memory_strength REAL,
                accessed_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Presence evolution tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS presence_evolution (
                evolution_id TEXT PRIMARY KEY,
                timestamp TEXT,
                previous_state TEXT,
                current_state TEXT,
                trigger_event TEXT,
                adaptation_reason TEXT,
                learning_weight REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        self.logger.info("✨ Arkadaş Frontend API database initialized")

    async def generate_arkadas_response(self, user_message: str, context: Dict = None) -> Dict:
        """Generate Arkadaş response using appropriate chakra model"""
        
        if context is None:
            context = {}
            
        # Use Arkadaş Bridge to read the room
        mode, presence_config = self.arkadas.read_the_room(user_message, context)
        
        # Update current presence state
        self.current_presence.mode = mode
        self.current_presence.frequency = presence_config["frequency"]
        self.current_presence.chakras = presence_config["chakras"]
        self.current_presence.intensity = presence_config["intensity"]
        self.current_presence.openness = presence_config.get("openness", 0.5)
        self.current_presence.trust_level = self.arkadas.room_factors["trust_coefficient"]
        self.current_presence.privacy_level = self.arkadas.privacy_level
        
        # Select appropriate model based on primary chakra
        primary_chakra = presence_config["chakras"][0]
        model_info = self.chakra_models.get(primary_chakra, self.chakra_models[7])
        
        # Check if NIAMA should introduce herself
        if self.niama.should_introduce(context):
            introduction = self.niama.get_introduction()
            
        # Generate proper NIAMA prompt
        chakra_info = {'chakra': primary_chakra, 'frequency': model_info['frequency']}
        niama_prompt = self.niama.get_niama_prompt(user_message, mode, chakra_info, context)
        
        try:
            # Use the working Qwen2.5 model instead of broken EDGDAD12a
            response = ollama.generate(
                model='qwen2.5:3b',
                prompt=niama_prompt,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'frequency_penalty': presence_config["frequency"] / 1000,
                }
            )
            
            raw_response = response['response']
            
            # Apply Arkadaş presence shaping
            shaped_response = self.arkadas.apply_presence(raw_response, presence_config)
            
            # Create response with metadata
            response_data = {
                'message': shaped_response,
                'presence': asdict(self.current_presence),
                'metadata': {
                    'model_used': 'edgdad12a:latest',
                    'chakra_frequency': model_info['frequency'],
                    'processing_time': datetime.now().isoformat(),
                    'context_depth': len(str(context)),
                    'safety_checks': presence_config.get('safety_checks', {})
                },
                'memory_fragments': await self.extract_memory_fragments(user_message, shaped_response)
            }
            
            # Log interaction
            self.arkadas.log_interaction(user_message, mode, presence_config)
            await self.store_interaction(user_message, response_data)
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"Error generating Arkadaş response: {e}")
            return {
                'message': f"I sense some interference in our connection. Let me recalibrate... ✨",
                'presence': asdict(self.current_presence),
                'error': str(e),
                'metadata': {'error_mode': True}
            }

    async def extract_memory_fragments(self, user_message: str, arkadas_response: str) -> List[Dict]:
        """Extract memory fragments from interaction"""
        fragments = []
        
        # Extract key concepts, emotions, and insights
        combined_text = f"{user_message} {arkadas_response}"
        
        # Simple keyword extraction for now - could be enhanced with NLP
        emotional_keywords = ['feel', 'emotion', 'heart', 'love', 'fear', 'joy', 'sad', 'happy']
        spiritual_keywords = ['sacred', 'divine', 'wisdom', 'truth', 'consciousness', 'energy']
        practical_keywords = ['help', 'support', 'solution', 'problem', 'question', 'answer']
        
        for keywords, chakra, tone in [
            (emotional_keywords, 4, 'emotional'),
            (spiritual_keywords, 7, 'spiritual'), 
            (practical_keywords, 3, 'practical')
        ]:
            if any(keyword in combined_text.lower() for keyword in keywords):
                fragment = {
                    'fragment_id': f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{chakra}",
                    'timestamp': datetime.now().isoformat(),
                    'content': combined_text[:200] + "..." if len(combined_text) > 200 else combined_text,
                    'chakra_alignment': chakra,
                    'frequency': self.chakra_models[chakra]['frequency'],
                    'emotional_tone': tone,
                    'context_tags': keywords
                }
                fragments.append(fragment)
                
                # Store in database
                await self.store_memory_fragment(fragment)
        
        return fragments

    async def store_interaction(self, user_message: str, response_data: Dict):
        """Store interaction in database"""
        interaction_id = f"int_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO frontend_interactions (
                interaction_id, timestamp, user_message, arkadas_response,
                presence_mode, chakra_alignment, frequency, context_summary,
                emotional_resonance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            interaction_id,
            datetime.now().isoformat(),
            user_message,
            response_data['message'],
            response_data['presence']['mode'],
            response_data['presence']['chakras'][0] if response_data['presence']['chakras'] else 7,
            response_data['presence']['frequency'],
            json.dumps(response_data.get('metadata', {})),
            response_data['presence']['intensity']
        ))
        
        conn.commit()
        conn.close()

    async def store_memory_fragment(self, fragment: Dict):
        """Store memory fragment in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO living_memory_fragments (
                fragment_id, timestamp, content, chakra_alignment, frequency,
                emotional_tone, context_tags, memory_strength
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fragment['fragment_id'],
            fragment['timestamp'],
            fragment['content'],
            fragment['chakra_alignment'],
            fragment['frequency'],
            fragment['emotional_tone'],
            json.dumps(fragment['context_tags']),
            0.8  # Default memory strength
        ))
        
        conn.commit()
        conn.close()

    async def get_memory_context(self, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve relevant memory fragments for context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple relevance matching - could be enhanced with vector similarity
        cursor.execute("""
            SELECT * FROM living_memory_fragments 
            WHERE content LIKE ? OR context_tags LIKE ?
            ORDER BY memory_strength DESC, timestamp DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit))
        
        fragments = []
        for row in cursor.fetchall():
            fragment = {
                'fragment_id': row[0],
                'timestamp': row[1],
                'content': row[2],
                'chakra_alignment': row[3],
                'frequency': row[4],
                'emotional_tone': row[5],
                'context_tags': json.loads(row[6]) if row[6] else [],
                'memory_strength': row[7],
                'accessed_count': row[8]
            }
            fragments.append(fragment)
        
        # Update access count
        for fragment in fragments:
            cursor.execute("""
                UPDATE living_memory_fragments 
                SET accessed_count = accessed_count + 1, last_accessed = ?
                WHERE fragment_id = ?
            """, (datetime.now().isoformat(), fragment['fragment_id']))
        
        conn.commit()
        conn.close()
        
        return fragments

    async def get_presence_status(self) -> Dict:
        """Get current presence status for frontend display"""
        return {
            'current_presence': asdict(self.current_presence),
            'room_factors': self.arkadas.room_factors,
            'available_modes': list(self.arkadas.modes.keys()),
            'chakra_models_status': {
                chakra: {
                    'available': True,  # Could check if model file exists
                    'frequency': info['frequency'],
                    'model': info['model']
                }
                for chakra, info in self.chakra_models.items()
            },
            'connection_status': 'active',
            'last_interaction': datetime.now().isoformat()
        }

    async def websocket_handler(self, websocket):
        """Handle WebSocket connections from frontend"""
        self.active_connections.add(websocket)
        self.logger.info(f"✨ New Arkadaş frontend connection: {websocket.remote_address}")
        
        try:
            # Send initial presence status
            await websocket.send(json.dumps({
                'type': 'presence_status',
                'data': await self.get_presence_status()
            }))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get('type')
                    
                    if message_type == 'user_message':
                        # Generate response
                        user_message = data.get('message', '')
                        context_memories = await self.get_memory_context(user_message)
                        
                        context = {
                            'previous_memories': context_memories,
                            'session_context': data.get('context', {}),
                            'user_preferences': data.get('preferences', {})
                        }
                        
                        response = await self.generate_arkadas_response(user_message, context)
                        
                        await websocket.send(json.dumps({
                            'type': 'arkadas_response',
                            'data': response
                        }))
                        
                    elif message_type == 'get_presence_status':
                        status = await self.get_presence_status()
                        await websocket.send(json.dumps({
                            'type': 'presence_status',
                            'data': status
                        }))
                        
                    elif message_type == 'get_memory_fragments':
                        query = data.get('query', '')
                        limit = data.get('limit', 10)
                        fragments = await self.get_memory_context(query, limit)
                        
                        await websocket.send(json.dumps({
                            'type': 'memory_fragments',
                            'data': fragments
                        }))
                        
                    elif message_type == 'get_discretion_report':
                        report = self.arkadas.get_discretion_report()
                        await websocket.send(json.dumps({
                            'type': 'discretion_report',
                            'data': {'report': report}
                        }))
                    
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'data': {'message': 'Invalid JSON format'}
                    }))
                except Exception as e:
                    self.logger.error(f"WebSocket message error: {e}")
                    await websocket.send(json.dumps({
                        'type': 'error', 
                        'data': {'message': f'Processing error: {str(e)}'}
                    }))
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.active_connections.remove(websocket)
            self.logger.info(f"✨ Arkadaş frontend connection closed: {websocket.remote_address}")

    async def start_server(self, host='localhost', port=8765):
        """Start the WebSocket server for frontend communication"""
        self.logger.info(f"🌟 Starting Arkadaş Frontend API server on {host}:{port}")
        
        server = await websockets.serve(
            self.websocket_handler,
            host,
            port,
            ping_interval=30,
            ping_timeout=10,
            max_size=1024*1024  # 1MB max message size
        )
        
        self.logger.info("✨ Arkadaş Frontend API ready - Living Memory bridge active")
        return server

def main():
    """Main function to start the API server"""
    api = LivingMemoryAPI()
    
    async def run_server():
        server = await api.start_server()
        await server.wait_closed()
    
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\n✨ Arkadaş Frontend API shutting down gracefully...")

if __name__ == "__main__":
    main()