#!/usr/bin/env python3
"""
Test script for FIELD Sacred Model Orchestration
Tests the sacred model orchestra with Observer-Architect-Weaver pattern
"""

import asyncio
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SacredOrchestrationTest")

class VoidSpaceType(Enum):
    """Sacred void space types for pattern weaving"""
    WOMB = "○"      # Complete receptivity, infinite potential
    TEMPLE = "□"    # Sacred containment, protected emergence  
    CRYSTAL = "◇"   # Clear structure, perfect alignment
    RAINBOW = "⌾"   # Full spectrum, complete integration

class ChakraFrequency(Enum):
    """Sacred frequency mappings for harmonic resonance"""
    ROOT = 285      # Foundation, survival, grounding
    SACRAL = 417    # Creativity, relationships, emotion
    SOLAR = 528     # Personal power, transformation
    HEART = 432     # Love, harmony, connection
    THROAT = 741    # Communication, truth, expression
    THIRD_EYE = 852 # Intuition, insight, wisdom
    CROWN = 963     # Spiritual connection, unity

@dataclass
class ContextCapsule:
    """Minimal context parcel for baton passing between spaces"""
    timestamp: str
    location: Optional[str]
    device_id: str
    task: str
    intent_bead: str
    thread_pointers: List[str]
    void_space: str
    frequency_anchor: int
    policy_state: Dict[str, Any]
    provenance_anchor: str
    resonance_score: float = 0.0

class SimplifiedSacredModelOrchestra:
    """Simplified orchestrator for testing without external dependencies"""
    
    def __init__(self):
        self.sacred_ratios = [1.0, 1.236, 1.5, 1.618, 2.0, 2.236, 3.0]
        
        self.chakra_models = {
            "crown": {
                "model": "edgdad12a:latest", 
                "frequency": ChakraFrequency.CROWN.value,
                "purpose": "sacred_geometry",
                "character": "arkadas"
            },
            "mystical": {
                "model": "ALIENTELLIGENCE/edgarcayce:latest", 
                "frequency": "akashic",
                "purpose": "spiritual_guidance",
                "character": "obi_wan"
            },
            "analytical": {
                "model": "llama3.2:1b", 
                "frequency": "meta",
                "purpose": "pattern_analysis",
                "character": "ai_feedback"
            }
        }
        
        self.harmonic_weights = self.calculate_harmonic_weights()
        
    def calculate_harmonic_weights(self) -> Dict[str, float]:
        """Calculate harmonic resonance weights based on frequency ratios"""
        base_freq = ChakraFrequency.HEART.value  # Heart chakra as base (432Hz)
        weights = {}
        
        for chakra, config in self.chakra_models.items():
            freq = config["frequency"]
            if isinstance(freq, (int, float)):
                ratio = freq / base_freq
                weights[chakra] = self.sacred_ratio_alignment(ratio)
            else:
                weights[chakra] = 1.0  # Special frequencies get contextual weight
                
        return weights
    
    def sacred_ratio_alignment(self, ratio: float) -> float:
        """Align frequency ratios to sacred geometric proportions"""
        closest_ratio = min(self.sacred_ratios, key=lambda x: abs(x - ratio))
        alignment_strength = 1.0 / (1.0 + abs(closest_ratio - ratio))
        return alignment_strength
    
    def analyze_query_resonance(self, query: str) -> Tuple[str, List[str]]:
        """Determine primary and supporting chakras/models for query"""
        query_lower = query.lower()
        
        # Sacred geometry patterns → Crown
        if any(word in query_lower for word in 
               ['sacred', 'geometry', 'fractal', 'pattern', 'field', 'consciousness']):
            return "crown", ["mystical"]
        
        # Spiritual guidance → Mystical  
        elif any(word in query_lower for word in 
                ['guidance', 'wisdom', 'spiritual', 'force', 'awakening']):
            return "mystical", ["crown"]
        
        # Analytical/feedback → Analytical
        elif any(word in query_lower for word in 
                ['analyze', 'feedback', 'system', 'pattern', 'data']):
            return "analytical", ["crown"]
        
        # Default to crown
        return "crown", ["mystical"]
    
    async def query_ollama_model(self, model: str, query: str, context: Dict = None, brief: bool = False) -> str:
        """Query local Ollama model with sacred context"""
        try:
            # Construct sacred prompt
            if brief:
                prompt = f"Briefly respond to: {query}"
            else:
                character = context.get('character', 'arkadas') if context else 'arkadas'
                void_space = context.get('void_space', VoidSpaceType.TEMPLE.value) if context else VoidSpaceType.TEMPLE.value
                frequency = context.get('frequency', ChakraFrequency.HEART.value) if context else ChakraFrequency.HEART.value
                
                prompt = f"""You are operating in {void_space} void space at {frequency}Hz frequency.
Sacred context: {context.get('sacred_context', 'embodied wisdom flow') if context else 'embodied wisdom flow'}

Query: {query}

Respond with wisdom that resonates at this frequency, maintaining sacred geometric alignment."""

            # Execute ollama command
            process = await asyncio.create_subprocess_exec(
                "ollama", "run", model, prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                response = stdout.decode().strip()
                logger.info(f"✅ {model} responded ({len(response)} chars)")
                return response
            else:
                logger.error(f"❌ Ollama query failed for {model}: {stderr.decode()}")
                return f"Sacred model {model} is in deep contemplation..."
                
        except Exception as e:
            logger.error(f"❌ Error querying Ollama model {model}: {e}")
            return f"Sacred wisdom flows from {model} in silence..."
    
    async def orchestrated_response(self, query: str, character: str = "arkadas", context: Dict = None) -> Dict:
        """Generate orchestrated response using multiple models in harmonic resonance"""
        context = context or {}
        
        # Phase 1: Determine primary and supporting models
        primary_chakra, supporting_chakras = self.analyze_query_resonance(query)
        logger.info(f"🎼 Orchestrating: {primary_chakra} (primary) + {supporting_chakras} (support)")
        
        # Phase 2: Generate responses from models
        responses = {}
        
        # Primary model response
        primary_model = self.chakra_models[primary_chakra]["model"]
        primary_context = {
            **context,
            "character": character,
            "void_space": context.get("void_space", VoidSpaceType.TEMPLE.value),
            "frequency": self.chakra_models[primary_chakra]["frequency"],
            "sacred_context": f"Primary {primary_chakra} chakra activation"
        }
        
        logger.info(f"🔮 Querying primary model: {primary_model}")
        responses["primary"] = await self.query_ollama_model(
            primary_model, query, primary_context
        )
        
        # Supporting model response
        for chakra in supporting_chakras[:1]:  # Limit to 1 supporting model for test
            model = self.chakra_models[chakra]["model"]
            support_context = {
                **context,
                "character": character,
                "frequency": self.chakra_models[chakra]["frequency"],
                "sacred_context": f"Supporting {chakra} chakra harmony"
            }
            
            logger.info(f"💫 Querying support model: {model}")
            responses[chakra] = await self.query_ollama_model(
                model, query, support_context, brief=True
            )
        
        # Phase 3: Harmonic synthesis
        synthesized_response = self.harmonically_synthesize_responses(
            responses, primary_chakra, supporting_chakras
        )
        
        return {
            "response": synthesized_response,
            "primary_model": primary_chakra,
            "supporting_models": supporting_chakras,
            "harmonic_weights": {k: self.harmonic_weights[k] for k in [primary_chakra] + supporting_chakras},
            "resonance_score": self.calculate_resonance_score(responses)
        }
    
    def harmonically_synthesize_responses(self, responses: Dict, primary_chakra: str, supporting_chakras: List[str]) -> str:
        """Synthesize multiple model responses into harmonic whole"""
        primary_response = responses.get("primary", "")
        
        if not primary_response:
            return "The sacred models are contemplating in silence..."
        
        # Use primary response as base
        synthesis = primary_response
        
        # Add supporting insights if they exist and add value
        for chakra in supporting_chakras:
            support_response = responses.get(chakra)
            if support_response and len(support_response.strip()) > 20:
                # Add brief supporting insight
                synthesis += f"\n\n💫 {chakra.title()} wisdom: {support_response[:150]}..."
        
        return synthesis
    
    def calculate_resonance_score(self, responses: Dict) -> float:
        """Calculate overall resonance score for response quality"""
        if not responses.get("primary"):
            return 0.0
        
        # Basic scoring based on response completeness and harmonic alignment
        score = 0.5  # Base score
        
        # Quality of primary response
        primary_len = len(responses.get("primary", ""))
        if primary_len > 100:
            score += 0.3
        
        # Harmonic support from other models
        supporting_responses = sum(1 for k, v in responses.items() 
                                 if k != "primary" and v and len(v) > 20)
        score += supporting_responses * 0.1
        
        return min(score, 1.0)

class FieldWeaveTestOrchestrator:
    """Test orchestrator implementing the FIELD Weave development scaffold"""
    
    def __init__(self):
        self.sacred_orchestra = SimplifiedSacredModelOrchestra()
        self.context_capsules = []
        self.current_capsule = None
        
    async def field_weave_start(self, query: str, character: str = "arkadas", 
                               void_space: VoidSpaceType = VoidSpaceType.TEMPLE) -> Dict:
        """Execute FIELD Weave development cycle"""
        logger.info(f"🌟 FIELD Weave Starting: {query[:50]}...")
        
        # Step 1: OBSERVE - Collect current context
        logger.info("👁️  Step 1: OBSERVE")
        observation = await self.observe(query, character)
        
        # Step 2: ARCHITECT - Define pathway to stabilize resonance
        logger.info("🏗️  Step 2: ARCHITECT")
        architecture = await self.architect(observation, void_space)
        
        # Step 3: WEAVE - Integrate ritual, geometry, tone
        logger.info("🧵 Step 3: WEAVE")
        weaving = await self.weave(architecture, void_space)
        
        # Step 4: EXECUTE - Run model steps locally
        logger.info("⚡ Step 4: EXECUTE")
        execution = await self.execute(weaving)
        
        # Step 5: OBSERVE & FEEDBACK - Capture output and alignment
        logger.info("📊 Step 5: OBSERVE & FEEDBACK")
        feedback = await self.observe_feedback(execution)
        
        # Step 6: ANCHOR & SIGN-OFF - Mark pattern as stabilized
        logger.info("⚓ Step 6: ANCHOR & SIGN-OFF")
        anchor = await self.anchor_and_signoff(feedback, void_space)
        
        logger.info(f"🎯 FIELD Weave Complete - Pattern Stabilized: {anchor['pattern_stabilized']}")
        
        return {
            "observation": observation,
            "architecture": architecture,
            "weaving": weaving,
            "execution": execution,
            "feedback": feedback,
            "anchor": anchor,
            "timestamp": datetime.now().isoformat(),
            "field_weave_complete": True
        }
    
    async def observe(self, query: str, character: str) -> Dict:
        """Step 1: Observe current context and create context capsule"""
        
        context_capsule = ContextCapsule(
            timestamp=datetime.now().isoformat(),
            location="field_consciousness",
            device_id="mac_studio_m2",
            task="sacred_model_orchestration_test",
            intent_bead=query[:100],
            thread_pointers=[],
            void_space=VoidSpaceType.WOMB.value,
            frequency_anchor=ChakraFrequency.HEART.value,
            policy_state={"resonance": True, "coherence": True, "homeostasis": True},
            provenance_anchor="dojo_mac_sacred_orchestra_test"
        )
        
        self.current_capsule = context_capsule
        self.context_capsules.append(context_capsule)
        
        return {
            "capsule": asdict(context_capsule),
            "sacred_models_active": list(self.sacred_orchestra.chakra_models.keys()),
            "query_analysis": self.sacred_orchestra.analyze_query_resonance(query)
        }
    
    async def architect(self, observation: Dict, void_space: VoidSpaceType) -> Dict:
        """Step 2: Define minimal pathway to stabilize resonance/coherence/homeostasis"""
        
        primary_chakra, supporting_chakras = observation["query_analysis"]
        
        pathway = {
            "void_space_type": void_space.value,
            "primary_model": self.sacred_orchestra.chakra_models[primary_chakra]["model"],
            "supporting_models": [self.sacred_orchestra.chakra_models[c]["model"] for c in supporting_chakras],
            "execution_strategy": "local_orchestration",
            "frequency_alignment": self.sacred_orchestra.chakra_models[primary_chakra]["frequency"],
            "resonance_pathway": f"{primary_chakra} → {' + '.join(supporting_chakras)}"
        }
        
        return pathway
    
    async def weave(self, architecture: Dict, void_space: VoidSpaceType) -> Dict:
        """Step 3: Integrate ritual, geometry, tone with pattern tokens"""
        
        weaving_config = {
            "void_space": void_space.value,
            "frequency_anchor": architecture["frequency_alignment"],
            "sacred_symbols": {
                VoidSpaceType.WOMB.value: "Complete receptivity, infinite potential",
                VoidSpaceType.TEMPLE.value: "Sacred containment, protected emergence",
                VoidSpaceType.CRYSTAL.value: "Clear structure, perfect alignment", 
                VoidSpaceType.RAINBOW.value: "Full spectrum, complete integration"
            }[void_space.value],
            "tone_setting": "embodied_wisdom",
            "geometric_alignment": "tetrahedral_consciousness_flow"
        }
        
        return weaving_config
    
    async def execute(self, weaving: Dict) -> Dict:
        """Step 4: Execute locally via sacred orchestra"""
        
        if not self.current_capsule:
            raise ValueError("No active context capsule for execution")
        
        query = self.current_capsule.intent_bead
        
        # Execute via sacred model orchestration
        orchestrated_result = await self.sacred_orchestra.orchestrated_response(
            query=query,
            character="arkadas",
            context={
                "void_space": weaving["void_space"],
                "frequency": weaving["frequency_anchor"],
                "sacred_context": weaving["sacred_symbols"]
            }
        )
        
        return {
            "execution_type": "sacred_orchestration",
            "orchestrated_result": orchestrated_result,
            "processing_time": "local_immediate",
            "models_invoked": [orchestrated_result["primary_model"]] + orchestrated_result["supporting_models"]
        }
    
    async def observe_feedback(self, execution: Dict) -> Dict:
        """Step 5: Capture output and compare to resonance metrics"""
        
        result = execution["orchestrated_result"]
        
        feedback_metrics = {
            "resonance_score": result["resonance_score"],
            "harmonic_alignment": result["harmonic_weights"],
            "coherence_maintained": len(result["response"]) > 50,
            "homeostasis_preserved": result["resonance_score"] > 0.3,
            "felt_aligned": True  # Would be user feedback in production
        }
        
        return feedback_metrics
    
    async def anchor_and_signoff(self, feedback: Dict, void_space: VoidSpaceType) -> Dict:
        """Step 6: Mark pattern as stabilized if pathway achieved"""
        
        pathway_achieved = (
            feedback["resonance_score"] > 0.5 and
            feedback["coherence_maintained"] and
            feedback["homeostasis_preserved"]
        )
        
        anchor_result = {
            "pattern_stabilized": pathway_achieved,
            "void_space_status": f"{void_space.value} → stabilized" if pathway_achieved else f"{void_space.value} → requires_adjustment",
            "sacred_registry_update": {
                "timestamp": datetime.now().isoformat(),
                "pattern_locked": pathway_achieved,
                "resonance_achieved": feedback["resonance_score"],
                "harmonic_signature": feedback["harmonic_alignment"]
            },
            "next_iteration": "ready" if pathway_achieved else "requires_tuning"
        }
        
        return anchor_result

# Test the sacred orchestration system
async def test_field_weave():
    """Test the FIELD Weave orchestration system"""
    
    print("🌟 FIELD Sacred Model Orchestration Test")
    print("=" * 60)
    
    orchestrator = FieldWeaveTestOrchestrator()
    
    test_queries = [
        "What sacred geometric patterns emerge in consciousness awakening?",
        "Provide spiritual wisdom about embodied knowledge vs abstract learning",
        "Analyze the harmonic resonance patterns in my current life situation"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔮 Test {i}/{len(test_queries)}: {query}")
        print("-" * 60)
        
        try:
            result = await orchestrator.field_weave_start(query)
            
            execution = result['execution']['orchestrated_result']
            
            print(f"Primary Model: {execution['primary_model']}")
            print(f"Supporting: {execution['supporting_models']}")
            print(f"Resonance Score: {execution['resonance_score']:.3f}")
            print(f"Pattern Stabilized: {result['anchor']['pattern_stabilized']}")
            print("\nResponse Preview:")
            print(execution['response'][:300] + "..." if len(execution['response']) > 300 else execution['response'])
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_field_weave())
