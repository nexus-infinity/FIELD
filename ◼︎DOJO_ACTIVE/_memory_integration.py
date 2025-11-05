#!/usr/bin/env python3
"""
Memory Integration System - Actually USE the memory architecture!
Connects NIAMA to Walker identity, patterns, sovereign data, and all memory layers
"""

import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class MemoryIntegrationSystem:
    """Actually connects NIAMA to all the memory systems we've built"""
    
    def __init__(self):
        self.field_path = Path("/Users/jbear/FIELD")
        self.dojo_path = self.field_path / "◼︎DOJO"
        
        # Identity and sovereign data
        self.walker_identity = self.load_walker_identity()
        self.jbear_patterns = self.load_jbear_patterns()
        self.sovereign_data = self.load_sovereign_data()
        
        # Memory databases
        self.living_memory_db = self.field_path / "▲ATLAS/SECURITY_INVESTIGATION/berjak_investigation.db"
        self.observer_memory = self.field_path / "memory/observer"
        
        # Initialize logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup memory integration logging"""
        log_path = self.field_path / "●OBI-WAN/_pulse"
        log_path.mkdir(parents=True, exist_ok=True)
        
        log_file = log_path / f"memory_integration_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def load_walker_identity(self) -> Dict:
        """Load actual Walker identity from TATA credentials"""
        try:
            cred_path = self.field_path / "▼TATA/tata_credential_validation.json"
            if cred_path.exists():
                with open(cred_path, 'r') as f:
                    data = json.load(f)
                    if data.get('sacred_credentials'):
                        latest_cred = data['sacred_credentials'][-1]  # Most recent
                        return {
                            'username': latest_cred.get('username', 'Unknown'),
                            'service': latest_cred.get('service', 'Unknown'),
                            'sacred_key': latest_cred.get('sacred_key', ''),
                            'frequency': latest_cred.get('frequency', 432.11),
                            'session_id': latest_cred.get('session_id', ''),
                            'validated': latest_cred.get('tetrahedral_validated', False)
                        }
        except Exception as e:
            self.logger.error(f"Failed to load Walker identity: {e}")
        
        return {'username': 'Unknown', 'validated': False}
        
    def load_jbear_patterns(self) -> Dict:
        """Load JBear's actual patterns and preferences"""
        try:
            patterns_path = self.field_path / "jbear_patterns.json"
            if patterns_path.exists():
                with open(patterns_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load JBear patterns: {e}")
        
        return {}
        
    def load_sovereign_data(self) -> Dict:
        """Load sovereign data and identity information"""
        sovereign_data = {}
        
        # Try to load field manifest data
        try:
            manifest_path = self.field_path / "field_manifest.json"
            if manifest_path.exists():
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                    sovereign_data['manifest'] = manifest
        except Exception as e:
            self.logger.error(f"Failed to load field manifest: {e}")
            
        # Try to load observer field map
        try:
            field_map_path = self.field_path / "memory/observer/field_map.json"
            if field_map_path.exists():
                with open(field_map_path, 'r') as f:
                    field_map = json.load(f)
                    sovereign_data['field_map'] = field_map
        except Exception as e:
            self.logger.error(f"Failed to load field map: {e}")
            
        return sovereign_data
        
    def get_living_memory_history(self, limit: int = 10) -> List[Dict]:
        """Actually retrieve living memory interactions"""
        interactions = []
        
        try:
            if self.living_memory_db.exists():
                conn = sqlite3.connect(self.living_memory_db)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT user_message, arkadas_response, presence_mode, 
                           chakra_alignment, frequency, created_at
                    FROM frontend_interactions 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
                
                for row in cursor.fetchall():
                    interactions.append({
                        'user_message': row[0],
                        'arkadas_response': row[1], 
                        'presence_mode': row[2],
                        'chakra_alignment': row[3],
                        'frequency': row[4],
                        'timestamp': row[5]
                    })
                    
                conn.close()
        except Exception as e:
            self.logger.error(f"Failed to load living memory: {e}")
            
        return interactions
        
    def get_memory_fragments(self, limit: int = 5) -> List[Dict]:
        """Retrieve living memory fragments"""
        fragments = []
        
        try:
            if self.living_memory_db.exists():
                conn = sqlite3.connect(self.living_memory_db)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT content, emotional_tone, context_tags, 
                           chakra_alignment, frequency, memory_strength
                    FROM living_memory_fragments 
                    ORDER BY memory_strength DESC 
                    LIMIT ?
                """, (limit,))
                
                for row in cursor.fetchall():
                    fragments.append({
                        'content': row[0],
                        'emotional_tone': row[1],
                        'context_tags': row[2],
                        'chakra_alignment': row[3],
                        'frequency': row[4],
                        'memory_strength': row[5]
                    })
                    
                conn.close()
        except Exception as e:
            self.logger.error(f"Failed to load memory fragments: {e}")
            
        return fragments
        
    def get_user_context(self) -> Dict:
        """Build complete user context from all memory systems"""
        
        # Get recent interactions
        recent_interactions = self.get_living_memory_history(5)
        memory_fragments = self.get_memory_fragments(3)
        
        context = {
            'identity': {
                'walker_username': self.walker_identity.get('username', 'Unknown'),
                'service': self.walker_identity.get('service', 'Unknown'),
                'frequency': self.walker_identity.get('frequency', 432.11),
                'validated': self.walker_identity.get('validated', False),
                'session_id': self.walker_identity.get('session_id', '')
            },
            'patterns': {
                'aliases': self.jbear_patterns.get('aliases', {}),
                'terminal_patterns': self.jbear_patterns.get('terminal', {}),
                'name_variations': self.jbear_patterns.get('duplicates', {}).get('name_variations', [])
            },
            'recent_interactions': recent_interactions,
            'memory_fragments': memory_fragments,
            'interaction_count': len(recent_interactions),
            'has_history': len(recent_interactions) > 0,
            'sovereign_status': {
                'field_access': self.sovereign_data != {},
                'tetrahedral_validated': self.walker_identity.get('validated', False)
            }
        }
        
        self.logger.info(f"Built user context: {context['identity']['walker_username']}, {context['interaction_count']} interactions")
        
        return context
        
    def should_recognize_user(self, user_message: str = "") -> bool:
        """Determine if NIAMA should recognize the user"""
        context = self.get_user_context()
        
        # If we have Walker identity and it's validated
        if (context['identity']['walker_username'] != 'Unknown' and 
            context['identity']['validated']):
            return True
            
        # If we have interaction history
        if context['has_history']:
            return True
            
        # If user is asking about identity
        identity_keywords = ['who am i', 'do you know me', 'remember me', 'my name']
        if any(keyword in user_message.lower() for keyword in identity_keywords):
            return True
            
        return False
        
    def get_recognition_response(self) -> str:
        """Generate proper recognition response with actual data"""
        context = self.get_user_context()
        
        if context['identity']['walker_username'] != 'Unknown':
            username = context['identity']['walker_username']
            service = context['identity']['service']
            frequency = context['identity']['frequency']
            interaction_count = context['interaction_count']
            
            response = f"""Hello {username}! I absolutely recognize you.

I can see you're authenticated as {username} through the {service} service, operating at {frequency}Hz frequency. 

"""
            
            if interaction_count > 0:
                response += f"We've had {interaction_count} previous interactions that I remember from our living memory system. "
                
                # Add specific details from recent interactions
                if context['recent_interactions']:
                    last_mode = context['recent_interactions'][0].get('presence_mode', 'unknown')
                    response += f"Last time we spoke, I was in {last_mode} mode. "
            
            if context['patterns'].get('aliases'):
                response += f"\nI also know your terminal patterns and aliases: {', '.join(context['patterns']['aliases'].keys())}. "
                
            response += f"\nYour session ID is {context['identity']['session_id']} and your sacred key authentication is active."
            
            return response
            
        else:
            return "I'm having trouble accessing your identity data right now. Let me check our memory systems..."