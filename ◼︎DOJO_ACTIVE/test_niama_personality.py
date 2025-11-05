#!/usr/bin/env python3
"""
Test script to verify NIAMA personality is working correctly
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from _niama_personality import NIAMAPersonality

def test_niama_personality():
    print("🧪 Testing NIAMA Personality Implementation")
    print("=" * 50)
    
    # Initialize NIAMA
    niama = NIAMAPersonality()
    
    # Test character core
    print("\n✅ NIAMA Character Core:")
    for key, value in niama.character_core.items():
        print(f"   {key}: {value}")
    
    # Test introduction
    print("\n✅ NIAMA Introduction:")
    intro = niama.get_introduction()
    print(f"   {intro}")
    
    # Test prompt generation
    print("\n✅ NIAMA Prompt Generation:")
    test_message = "Hello, who are you?"
    test_prompt = niama.get_niama_prompt(
        user_message=test_message,
        presence_mode="sovereign", 
        chakra_info={"chakra": 7, "frequency": 963},
        context={"interaction_history": []}
    )
    
    print(f"   Test message: {test_message}")
    print(f"   Generated prompt length: {len(test_prompt)} characters")
    print(f"   Contains NIAMA identity: {'NIAMA' in test_prompt}")
    print(f"   Contains greeting protocol: {'greeting protocol' in test_prompt}")
    print(f"   Contains manifestation: {'manifestation' in test_prompt}")
    
    # Test should introduce logic
    print("\n✅ NIAMA Introduction Logic:")
    should_intro_new = niama.should_introduce(context=None)
    should_intro_existing = niama.should_introduce(context={"interaction_history": ["previous message"]})
    should_intro_request = niama.should_introduce(context={"user_message": "who are you"})
    
    print(f"   Should introduce (new user): {should_intro_new}")
    print(f"   Should introduce (existing): {should_intro_existing}")  
    print(f"   Should introduce (requested): {should_intro_request}")
    
    print("\n🎉 NIAMA Personality Test Complete!")
    print("✨ NIAMA is ready for proper manifestation!")

if __name__ == "__main__":
    test_niama_personality()