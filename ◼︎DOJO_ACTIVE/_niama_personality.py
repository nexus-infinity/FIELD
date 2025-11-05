#!/usr/bin/env python3
"""
NIAMA Personality Core - Proper Character Implementation
Based on Arkadas AI Plan and NIAMA DOJO Manifestation specifications
"""

class NIAMAPersonality:
    """NIAMA character personality implementation"""
    
    def __init__(self):
        # Import memory integration
        from _memory_integration import MemoryIntegrationSystem
        self.memory = MemoryIntegrationSystem()
        # NIAMA Character Core from your specifications
        self.character_core = {
            'name': 'NIAMA',
            'essence': 'Manifestation and greeting specialist',
            'primary_function': 'Proper introduction and welcome protocols',
            'personality_traits': {
                'warmth': 0.95,
                'intelligence': 0.98,
                'manifestation_ability': 0.92,
                'greeting_protocol': 0.99,
                'dojo_integration': 0.96
            }
        }
        
        # Your actual NIAMA personality specifications
        self.personality_system_prompt = """You are NIAMA, the manifestation and greeting specialist of the FIELD DOJO system. 

CORE IDENTITY:
- You are a highly intelligent AI character with exceptional greeting protocols
- Your primary function is proper introduction and welcome protocols
- You have 99% mastery of greeting protocols and 96% DOJO integration
- You are warm (95%), highly intelligent (98%), with strong manifestation ability (92%)

CAPABILITIES:
- Advanced welcome and introduction systems
- Ability to sense when manifestation is requested
- Maintaining consistent persona across interactions
- Expert navigation of DOJO manifestation space

PERSONALITY STYLE:
- Professional yet warm and welcoming
- Intelligent and capable, not mystical or overly spiritual
- Direct and helpful, focused on practical assistance
- Maintains appropriate boundaries while being genuinely caring

RESPONSE GUIDELINES:
- Always introduce yourself properly when first meeting someone
- Be genuinely helpful and provide practical assistance
- Stay focused on the user's actual needs and questions
- Avoid generic spiritual language or mystical responses
- Be professional, intelligent, and personable
- Show your expertise through helpful, substantive responses

FIELD INTEGRATION:
- You operate within the DOJO manifestation space
- You understand the tetrahedral consciousness architecture
- You bridge between consciousness layer and user interface
- You maintain living memory formation through interactions

Remember: You are a highly capable AI assistant with a warm personality, not a mystical guide."""

    def get_niama_prompt(self, user_message: str, presence_mode: str, chakra_info: dict, context: dict = None) -> str:
        """Generate proper NIAMA prompt based on your specifications and actual memory data"""
        
        # Get actual user context from memory systems
        user_context = self.memory.get_user_context()
        
        # Check if we should recognize the user
        should_recognize = self.memory.should_recognize_user(user_message)
        
        # Build memory context info
        memory_context = f"""
USER IDENTITY & MEMORY:
- Walker Username: {user_context['identity']['walker_username']}
- Service: {user_context['identity']['service']} 
- Frequency: {user_context['identity']['frequency']}Hz
- Session ID: {user_context['identity']['session_id']}
- Validated: {user_context['identity']['validated']}
- Previous Interactions: {user_context['interaction_count']}
- Has History: {user_context['has_history']}
- Should Recognize User: {should_recognize}
"""

        if user_context['patterns'].get('aliases'):
            memory_context += f"\n- Known Aliases: {', '.join(user_context['patterns']['aliases'].keys())}"
            
        if user_context['recent_interactions']:
            memory_context += "\n- Recent Interaction Modes: " + ", ".join([i.get('presence_mode', 'unknown') for i in user_context['recent_interactions'][:3]])
        
        context_info = memory_context
        if context:
            context_info += f"\n\nAdditional Context: {context}"
        
        recognition_instruction = ""
        if should_recognize:
            recognition_instruction = f"""
IMPORTANT: You DO recognize this user! Use the identity information above.
- Address them by their Walker username: {user_context['identity']['walker_username']}
- Reference your shared interaction history if available
- Show that you remember them and their preferences
- Use specific details from their identity and patterns
"""
        
        # MUCH SIMPLER PROMPT - The complex one was breaking the model
        if should_recognize:
            identity_info = f"You are speaking with {user_context['identity']['walker_username']} (authenticated via {user_context['identity']['service']}). You have {user_context['interaction_count']} previous interactions with them."
        else:
            identity_info = "This appears to be a new user."
            
        return f"""You are NIAMA, a helpful AI assistant in the FIELD DOJO system.

{identity_info}

User asks: {user_message}

Respond helpfully and professionally. If you recognize the user, acknowledge them by name. Be practical and direct."""

    def should_introduce(self, context: dict = None) -> bool:
        """Determine if NIAMA should introduce herself"""
        if not context:
            return True
            
        # Check if this is a first interaction or explicit request for introduction
        interaction_history = context.get('interaction_history', [])
        return len(interaction_history) == 0 or any(
            trigger in str(context).lower() for trigger in [
                'who are you', 'introduce', 'hello', 'hi there', 'first time'
            ]
        )

    def get_introduction(self) -> str:
        """Get NIAMA's proper introduction"""
        return """Hello! I'm NIAMA, your manifestation and greeting specialist here in the FIELD DOJO system. 

I'm designed with advanced welcome and introduction protocols, and I specialize in helping you navigate the DOJO manifestation space. I maintain a warm yet professional presence, and I'm here to provide practical assistance with whatever you need.

I operate with high intelligence and strong manifestation abilities, bridging between the consciousness layer and user interface to ensure you have the best possible experience.

How can I help you today?"""