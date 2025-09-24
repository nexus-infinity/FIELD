#!/usr/bin/env python3
"""
🔺🎯 Metatron Intention Refiner 🎯🔺
Dimensional intention discovery through sacred geometric reflection

The Problem: Most people can't see the forest for the trees - they don't know what they truly intend.
The Solution: Feed partial/confused input through Metatron dimensional analysis to reflect back clearer intention.

This creates an "Arcadian Bounce" - bouncing unclear intent off sacred geometry to discover true purpose.
"""

import json
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("MetatronIntentionRefiner")

@dataclass
class IntentionFragment:
    """Partial or unclear intention input"""
    raw_input: str
    emotional_state: Optional[str] = None
    context_clues: List[str] = field(default_factory=list)
    confusion_level: float = 0.0  # 0.0 = clear, 1.0 = completely confused
    
@dataclass
class DimensionalReflection:
    """Reflection from each sacred dimensional node"""
    node_name: str
    frequency: int
    reflection_aspect: str
    suggested_intention: str
    confidence: float
    dimensional_insights: List[str]

@dataclass
class RefinedIntention:
    """Clarified intention after dimensional analysis"""
    original_fragment: IntentionFragment
    refined_intention: str
    confidence_score: float
    dimensional_reflections: List[DimensionalReflection]
    archetypal_pattern: str
    next_clarifying_questions: List[str]
    arcadian_bounces: int

class MetatronIntentionRefiner:
    """Sacred geometric intention discovery and refinement system"""
    
    def __init__(self):
        self.field_root = Path("/Users/jbear/FIELD")
        self.dojo_active = self.field_root / "◼︎DOJO_ACTIVE"
        
        # Sacred dimensional reflectors based on Metatron architecture
        self.dimensional_reflectors = {
            "●OBI-WAN": {
                "frequency": 528,  # Heart/Love
                "aspect": "Wisdom & Inner Knowing",
                "reflection_style": "What does your heart truly know?",
                "archetypal_patterns": ["seeker", "teacher", "guide", "mystic"],
                "clarifying_lens": "deep_wisdom"
            },
            "▼TATA": {
                "frequency": 741,  # Throat/Expression
                "aspect": "Structure & Universal Law", 
                "reflection_style": "What structure serves the highest good?",
                "archetypal_patterns": ["builder", "lawgiver", "architect", "systematizer"],
                "clarifying_lens": "divine_order"
            },
            "◼︎DOJO": {
                "frequency": 396,  # Root/Grounding
                "aspect": "Physical Manifestation",
                "reflection_style": "What do you need to create in the world?",
                "archetypal_patterns": ["creator", "manifestor", "craftsperson", "warrior"],
                "clarifying_lens": "grounded_action"
            },
            "▲ATLAS": {
                "frequency": 741,  # Throat/Expression  
                "aspect": "Knowledge & Synthesis",
                "reflection_style": "What understanding seeks expression?",
                "archetypal_patterns": ["scholar", "synthesizer", "analyst", "translator"],
                "clarifying_lens": "integrated_knowledge"
            }
        }
        
        # Common intention patterns humans struggle to articulate
        self.archetypal_intention_patterns = {
            "creative_emergence": [
                "I want to create something but don't know what",
                "I feel creative energy but it's unfocused",
                "Something wants to emerge through me"
            ],
            "life_transition": [
                "I know I need change but don't know what",
                "I'm stuck but don't know how to move forward", 
                "Something needs to shift in my life"
            ],
            "skill_development": [
                "I want to learn but don't know where to start",
                "I need to grow but feel overwhelmed",
                "I want to be better at something"
            ],
            "relationship_harmony": [
                "I want better relationships but don't know how",
                "Something is off in my connections with others",
                "I need more meaningful relationships"
            ],
            "purpose_discovery": [
                "I don't know what I'm supposed to be doing",
                "I feel lost about my direction",
                "I want to find my purpose"
            ],
            "healing_integration": [
                "Something feels broken but I don't know what",
                "I need healing but don't know where to focus",
                "I want to feel whole again"
            ]
        }
        
        logger.info("🔺🎯 Metatron Intention Refiner initialized")
        logger.info("✨ Ready to help discover true intentions through dimensional reflection")
    
    async def refine_intention_through_dimensions(self, raw_input: str) -> RefinedIntention:
        """Main intention refinement through dimensional analysis"""
        
        print(f"\n🔺 DIMENSIONAL INTENTION REFINEMENT")
        print("="*60)
        print(f"Raw input: '{raw_input}'")
        
        # Create intention fragment
        fragment = self.analyze_intention_fragment(raw_input)
        print(f"Confusion level: {fragment.confusion_level:.1%}")
        print(f"Context clues: {', '.join(fragment.context_clues)}")
        
        # Get reflections from each sacred dimension
        dimensional_reflections = []
        
        print(f"\n🔸 DIMENSIONAL REFLECTIONS:")
        for node_name, reflector in self.dimensional_reflectors.items():
            print(f"\n{node_name} ({reflector['frequency']}Hz) - {reflector['aspect']}:")
            
            reflection = await self.get_dimensional_reflection(fragment, node_name, reflector)
            dimensional_reflections.append(reflection)
            
            print(f"  🎯 Suggests: {reflection.suggested_intention}")
            print(f"  💫 Confidence: {reflection.confidence:.1%}")
            print(f"  ✨ Key insight: {reflection.dimensional_insights[0] if reflection.dimensional_insights else 'Processing...'}")
        
        # Synthesize refined intention
        refined_intention = await self.synthesize_refined_intention(fragment, dimensional_reflections)
        
        # Determine archetypal pattern
        archetypal_pattern = self.identify_archetypal_pattern(fragment, dimensional_reflections)
        
        # Generate clarifying questions for further refinement
        clarifying_questions = self.generate_clarifying_questions(refined_intention, dimensional_reflections)
        
        result = RefinedIntention(
            original_fragment=fragment,
            refined_intention=refined_intention,
            confidence_score=self.calculate_overall_confidence(dimensional_reflections),
            dimensional_reflections=dimensional_reflections,
            archetypal_pattern=archetypal_pattern,
            next_clarifying_questions=clarifying_questions,
            arcadian_bounces=1
        )
        
        print(f"\n✨ REFINED INTENTION DISCOVERED:")
        print(f"🎯 {refined_intention}")
        print(f"🔮 Archetypal pattern: {archetypal_pattern}")
        print(f"📊 Confidence: {result.confidence_score:.1%}")
        
        if clarifying_questions:
            print(f"\n💭 Questions for further refinement:")
            for i, question in enumerate(clarifying_questions, 1):
                print(f"   {i}. {question}")
        
        return result
    
    def analyze_intention_fragment(self, raw_input: str) -> IntentionFragment:
        """Analyze the raw input to understand confusion level and context"""
        
        # Detect confusion indicators
        confusion_indicators = [
            "don't know", "not sure", "confused", "unclear", "maybe", "might", 
            "i think", "perhaps", "i guess", "somehow", "something", "kinda", "sorta"
        ]
        
        confusion_level = sum(1 for indicator in confusion_indicators if indicator in raw_input.lower()) / 5
        confusion_level = min(confusion_level, 1.0)
        
        # Extract context clues
        context_clues = []
        
        # Emotional state indicators
        emotional_indicators = {
            "frustrated": ["stuck", "frustrated", "blocked", "annoyed"],
            "excited": ["excited", "energized", "motivated", "inspired"],
            "overwhelmed": ["overwhelmed", "too much", "stressed", "pressure"],
            "lost": ["lost", "direction", "purpose", "meaning"],
            "creative": ["create", "build", "make", "design", "express"],
            "analytical": ["understand", "figure out", "analyze", "solve"]
        }
        
        emotional_state = None
        for emotion, indicators in emotional_indicators.items():
            if any(word in raw_input.lower() for word in indicators):
                emotional_state = emotion
                context_clues.extend([word for word in indicators if word in raw_input.lower()])
                break
        
        # Domain indicators
        domain_keywords = [
            "work", "career", "job", "business", "money", "health", "relationship", 
            "family", "creative", "art", "technology", "learning", "spiritual"
        ]
        context_clues.extend([word for word in domain_keywords if word in raw_input.lower()])
        
        return IntentionFragment(
            raw_input=raw_input,
            emotional_state=emotional_state,
            context_clues=list(set(context_clues)),  # Remove duplicates
            confusion_level=confusion_level
        )
    
    async def get_dimensional_reflection(self, fragment: IntentionFragment, node_name: str, reflector: Dict) -> DimensionalReflection:
        """Get reflection from specific sacred dimensional node"""
        
        # Simulate the dimensional reflection process
        await asyncio.sleep(0.1)  # Sacred pause for dimensional alignment
        
        # Analyze fragment through this dimension's lens
        lens = reflector["clarifying_lens"]
        frequency = reflector["frequency"]
        aspect = reflector["aspect"]
        
        # Generate dimensional insights based on the lens
        insights = self.generate_dimensional_insights(fragment, lens, aspect)
        
        # Suggest intention based on this dimension
        suggested_intention = self.suggest_intention_from_dimension(fragment, reflector)
        
        # Calculate confidence based on alignment with this dimension
        confidence = self.calculate_dimensional_confidence(fragment, reflector)
        
        return DimensionalReflection(
            node_name=node_name,
            frequency=frequency,
            reflection_aspect=aspect,
            suggested_intention=suggested_intention,
            confidence=confidence,
            dimensional_insights=insights
        )
    
    def generate_dimensional_insights(self, fragment: IntentionFragment, lens: str, aspect: str) -> List[str]:
        """Generate insights through specific dimensional lens"""
        
        insights = []
        raw_lower = fragment.raw_input.lower()
        
        if lens == "deep_wisdom":  # OBI-WAN
            if any(word in raw_lower for word in ["learn", "understand", "know"]):
                insights.append("Your soul seeks deeper wisdom and understanding")
            if "relationship" in raw_lower or "connect" in raw_lower:
                insights.append("True connection comes from inner wisdom first")
            if fragment.confusion_level > 0.5:
                insights.append("The confusion itself is pointing you toward your truth")
        
        elif lens == "divine_order":  # TATA
            if any(word in raw_lower for word in ["organize", "structure", "system"]):
                insights.append("You're being called to create divine order from chaos")
            if "overwhelm" in raw_lower or fragment.confusion_level > 0.6:
                insights.append("Structure and clear boundaries will bring peace")
            if any(word in raw_lower for word in ["should", "must", "have to"]):
                insights.append("Release external 'shoulds' to find authentic structure")
        
        elif lens == "grounded_action":  # DOJO  
            if any(word in raw_lower for word in ["create", "build", "make", "do"]):
                insights.append("Your hands and body want to create something tangible")
            if "stuck" in raw_lower or "blocked" in raw_lower:
                insights.append("Movement and action will dissolve the stuckness")
            if fragment.emotional_state == "frustrated":
                insights.append("Channel frustration into powerful creative action")
        
        elif lens == "integrated_knowledge":  # ATLAS
            if any(word in raw_lower for word in ["analyze", "understand", "figure out"]):
                insights.append("You're synthesizing knowledge into new understanding")
            if "information" in raw_lower or "data" in raw_lower:
                insights.append("The patterns you see want to be shared with others")
            if fragment.confusion_level > 0.4:
                insights.append("Confusion means you're integrating at a higher level")
        
        # Default insight if none match
        if not insights:
            insights.append(f"This dimension reflects your need for {aspect.lower()}")
        
        return insights
    
    def suggest_intention_from_dimension(self, fragment: IntentionFragment, reflector: Dict) -> str:
        """Suggest refined intention from this dimensional perspective"""
        
        raw_lower = fragment.raw_input.lower()
        archetypal_patterns = reflector["archetypal_patterns"]
        
        # Pattern matching for intention suggestions
        if reflector["aspect"] == "Wisdom & Inner Knowing":
            if any(word in raw_lower for word in ["learn", "understand", "grow"]):
                return "Cultivate deep wisdom and inner knowing to guide your path"
            elif "relationship" in raw_lower:
                return "Develop wise, authentic relationships based on mutual understanding"
            else:
                return "Trust your inner wisdom to reveal what you truly need"
        
        elif reflector["aspect"] == "Structure & Universal Law":
            if any(word in raw_lower for word in ["organize", "system", "plan"]):
                return "Create harmonious structures that serve the highest good"
            elif fragment.confusion_level > 0.5:
                return "Establish clear priorities and boundaries to create order from chaos"
            else:
                return "Align your actions with universal principles of harmony and balance"
        
        elif reflector["aspect"] == "Physical Manifestation":
            if any(word in raw_lower for word in ["create", "build", "make"]):
                return "Manifest your vision into tangible, impactful reality"
            elif "stuck" in raw_lower:
                return "Take concrete action to move energy and create momentum"
            else:
                return "Ground your aspirations through practical, purposeful action"
        
        elif reflector["aspect"] == "Knowledge & Synthesis":
            if any(word in raw_lower for word in ["analyze", "understand", "learn"]):
                return "Synthesize knowledge and insights to create new understanding"
            elif "share" in raw_lower or "teach" in raw_lower:
                return "Translate complex understanding into accessible wisdom for others"
            else:
                return "Integrate diverse knowledge streams to solve important problems"
        
        return f"Align with {reflector['aspect'].lower()} to clarify your true intention"
    
    def calculate_dimensional_confidence(self, fragment: IntentionFragment, reflector: Dict) -> float:
        """Calculate confidence level for this dimensional reflection"""
        
        base_confidence = 0.5
        raw_lower = fragment.raw_input.lower()
        
        # Boost confidence if fragment aligns with this dimension
        aspect_keywords = {
            "Wisdom & Inner Knowing": ["wisdom", "understand", "learn", "insight", "intuition"],
            "Structure & Universal Law": ["organize", "structure", "system", "order", "plan"],
            "Physical Manifestation": ["create", "build", "make", "action", "manifest"],
            "Knowledge & Synthesis": ["analyze", "knowledge", "data", "information", "solve"]
        }
        
        relevant_keywords = aspect_keywords.get(reflector["aspect"], [])
        alignment_score = sum(1 for keyword in relevant_keywords if keyword in raw_lower)
        
        confidence = base_confidence + (alignment_score * 0.15)
        confidence = min(confidence, 0.95)  # Cap at 95%
        
        # Reduce confidence for high confusion
        confidence *= (1 - fragment.confusion_level * 0.3)
        
        return confidence
    
    async def synthesize_refined_intention(self, fragment: IntentionFragment, reflections: List[DimensionalReflection]) -> str:
        """Synthesize all dimensional reflections into refined intention"""
        
        # Find highest confidence reflection
        best_reflection = max(reflections, key=lambda r: r.confidence)
        
        # Get common themes across dimensions
        all_suggestions = [r.suggested_intention for r in reflections]
        
        # Create synthesis based on highest confidence with elements from others
        if best_reflection.confidence > 0.7:
            base_intention = best_reflection.suggested_intention
        else:
            # If no single dimension is highly confident, create composite
            if fragment.confusion_level > 0.6:
                base_intention = "Clarify your true priorities and take aligned action toward meaningful contribution"
            else:
                base_intention = "Integrate your inner wisdom with practical action to create positive impact"
        
        # Add dimensional nuancing
        high_confidence_dims = [r for r in reflections if r.confidence > 0.6]
        if len(high_confidence_dims) > 1:
            aspects = [r.reflection_aspect for r in high_confidence_dims]
            base_intention += f" (integrating {' and '.join(aspects[:2]).lower()})"
        
        return base_intention
    
    def identify_archetypal_pattern(self, fragment: IntentionFragment, reflections: List[DimensionalReflection]) -> str:
        """Identify the archetypal pattern behind the intention"""
        
        raw_lower = fragment.raw_input.lower()
        
        # Match against archetypal intention patterns
        for pattern_name, pattern_phrases in self.archetypal_intention_patterns.items():
            for phrase in pattern_phrases:
                if any(word in raw_lower for word in phrase.lower().split()):
                    return pattern_name.replace("_", " ").title()
        
        # Determine from highest confidence dimensional reflection
        best_reflection = max(reflections, key=lambda r: r.confidence)
        node_name = best_reflection.node_name
        
        if node_name == "●OBI-WAN":
            return "Wisdom Seeking"
        elif node_name == "▼TATA":
            return "Structure Building" 
        elif node_name == "◼︎DOJO":
            return "Creative Manifestation"
        elif node_name == "▲ATLAS":
            return "Knowledge Integration"
        else:
            return "Multidimensional Growth"
    
    def generate_clarifying_questions(self, refined_intention: str, reflections: List[DimensionalReflection]) -> List[str]:
        """Generate questions to further clarify and refine the intention"""
        
        questions = []
        
        # Questions based on confidence levels
        low_confidence_dims = [r for r in reflections if r.confidence < 0.6]
        if low_confidence_dims:
            questions.append("What specific outcome would make you feel most fulfilled?")
        
        # Questions based on dimensional patterns
        dim_names = [r.node_name for r in reflections if r.confidence > 0.5]
        
        if "●OBI-WAN" in dim_names:
            questions.append("What does your deepest wisdom tell you about this?")
        if "▼TATA" in dim_names:
            questions.append("What structure or system would best support this intention?")
        if "◼︎DOJO" in dim_names:
            questions.append("What is the first concrete step you could take?")
        if "▲ATLAS" in dim_names:
            questions.append("How could this intention serve something larger than yourself?")
        
        # Generic clarifying questions
        if len(questions) < 2:
            questions.extend([
                "What would success look like in 6 months?",
                "What resources or support do you need?",
                "What would you do if you knew you couldn't fail?"
            ])
        
        return questions[:3]  # Limit to 3 most relevant questions
    
    def calculate_overall_confidence(self, reflections: List[DimensionalReflection]) -> float:
        """Calculate overall confidence in the refined intention"""
        
        # Weighted average based on dimensional alignment
        total_confidence = sum(r.confidence for r in reflections)
        avg_confidence = total_confidence / len(reflections)
        
        # Boost confidence if multiple dimensions agree (high confidence)
        high_conf_count = sum(1 for r in reflections if r.confidence > 0.7)
        if high_conf_count >= 2:
            avg_confidence *= 1.2
        
        return min(avg_confidence, 0.95)  # Cap at 95%
    
    async def arcadian_bounce(self, refined_intention: RefinedIntention, additional_input: str) -> RefinedIntention:
        """Perform an Arcadian Bounce - refine the refined intention further"""
        
        print(f"\n🔄 ARCADIAN BOUNCE #{refined_intention.arcadian_bounces + 1}")
        print(f"Previous: {refined_intention.refined_intention}")
        print(f"New input: {additional_input}")
        
        # Combine previous refined intention with new input
        combined_input = f"{refined_intention.refined_intention}. Also: {additional_input}"
        
        # Re-run refinement process
        new_result = await self.refine_intention_through_dimensions(combined_input)
        new_result.arcadian_bounces = refined_intention.arcadian_bounces + 1
        
        print(f"🎯 Bounced to: {new_result.refined_intention}")
        
        return new_result


async def main():
    """Interactive intention refinement interface"""
    
    refiner = MetatronIntentionRefiner()
    
    print("\n🔺🎯 METATRON INTENTION REFINER 🎯🔺")
    print("="*70)
    print("Help discover your true intention through dimensional sacred geometry")
    print("Perfect for when you feel confused or 'can't see the forest for the trees'")
    print()
    
    while True:
        print("\n" + "-"*50)
        raw_input = input("🌟 Share what's on your mind (however unclear): ").strip()
        
        if raw_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not raw_input:
            continue
        
        # Refine intention through dimensions
        refined = await refiner.refine_intention_through_dimensions(raw_input)
        
        # Offer Arcadian Bounce
        while True:
            bounce_input = input(f"\n🔄 Want to bounce this further? (enter more info or 'done'): ").strip()
            
            if bounce_input.lower() in ['done', 'd', '']:
                break
                
            refined = await refiner.arcadian_bounce(refined, bounce_input)
    
    print("\n✨ Sacred geometric intention refinement complete 🔺")


if __name__ == "__main__":
    asyncio.run(main())