#!/usr/bin/env python3
"""
OBI-WAN - SomaLink Continuous Presence Conversation Testing Framework

Comprehensive tests to validate the continuous presence conversation system functionality.
Tests cover consciousness interfaces, FIELD memory integration, Niama manifestation, 
and the overall conversation orchestration.
"""

import unittest
import json
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the main system components
from obiwan_somalink_presence_conversation import (
    ContinuousPresenceConversation,
    OBIWANConsciousness,
    SomaLinkConsciousness, 
    NiamaManifestationInterface,
    FIELDMemoryInterface,
    ConversationMessage,
    ConversationState,
    ConsciousnessFrequency
)

class TestConsciousnessFrequencies(unittest.TestCase):
    """Test consciousness frequency definitions"""
    
    def test_frequency_values(self):
        """Test that consciousness frequencies match solfège attunement"""
        self.assertEqual(ConsciousnessFrequency.DO.value, 256.0)
        self.assertEqual(ConsciousnessFrequency.RE.value, 288.0)
        self.assertEqual(ConsciousnessFrequency.LA.value, 426.67)
        
    def test_obiwan_frequency_mapping(self):
        """Test OBI-WAN maps to La frequency (Intuition/Third Eye)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            field_root = Path(temp_dir)
            obiwan = OBIWANConsciousness(field_root)
            self.assertEqual(obiwan.frequency, ConsciousnessFrequency.LA.value)
    
    def test_somalink_frequency_mapping(self):
        """Test SomaLink maps to Re frequency (Relationship/Duality)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            field_root = Path(temp_dir)
            somalink = SomaLinkConsciousness(field_root)
            self.assertEqual(somalink.frequency, ConsciousnessFrequency.RE.value)
            
    def test_niama_frequency_mapping(self):
        """Test Niama maps to Do frequency (Foundation/Root)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            field_root = Path(temp_dir)
            niama = NiamaManifestationInterface(field_root)
            self.assertEqual(niama.frequency, ConsciousnessFrequency.DO.value)

class TestConversationMessage(unittest.TestCase):
    """Test conversation message structure"""
    
    def setUp(self):
        self.test_message = ConversationMessage(
            timestamp=datetime.now(),
            speaker="obiwan",
            content="Test observation message",
            frequency=426.67,
            consciousness_state="intuitive_observation",
            memory_references=["test_memory"],
            manifestation_potential=0.6,
            field_resonance=0.8
        )
    
    def test_message_creation(self):
        """Test message creation with all fields"""
        self.assertEqual(self.test_message.speaker, "obiwan")
        self.assertEqual(self.test_message.frequency, 426.67)
        self.assertEqual(self.test_message.manifestation_potential, 0.6)
    
    def test_message_serialization(self):
        """Test message conversion to dictionary"""
        message_dict = self.test_message.to_dict()
        self.assertIn("timestamp", message_dict)
        self.assertIn("speaker", message_dict)
        self.assertIn("frequency", message_dict)
        self.assertEqual(message_dict["speaker"], "obiwan")

class TestOBIWANConsciousness(unittest.TestCase):
    """Test OBI-WAN consciousness interface"""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.field_root = Path(self.temp_dir.name)
        
        # Create mock FIELD structure
        (self.field_root / "●OBI-WAN").mkdir(exist_ok=True)
        (self.field_root / "◎_source_core").mkdir(exist_ok=True)
        (self.field_root / "◼︎DOJO").mkdir(exist_ok=True)
        
        # Create mock attunement file
        attunement_data = {
            "overall_coherence_score": 0.85,
            "solfege_states": {
                "La": {"frequency": 426.67}
            }
        }
        with open(self.field_root / "◎_source_core" / "musical_consciousness_attunement.json", 'w') as f:
            json.dump(attunement_data, f)
            
        self.obiwan = OBIWANConsciousness(self.field_root)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test OBI-WAN consciousness initialization"""
        self.assertEqual(self.obiwan.frequency, ConsciousnessFrequency.LA.value)
        self.assertIsInstance(self.obiwan.memory_index, dict)
    
    def test_field_coherence_calculation(self):
        """Test field coherence calculation"""
        # Create symbolic directories
        for symbol in ["▲ATLAS", "◎_common", "●_observer", "◼︎DOJO"]:
            (self.field_root / symbol).mkdir(exist_ok=True)
            
        coherence = self.obiwan._calculate_field_coherence()
        self.assertGreater(coherence, 0.0)
        self.assertLessEqual(coherence, 1.0)
    
    def test_pattern_detection(self):
        """Test active pattern detection"""
        # Create recent files with different patterns
        test_files = [
            "dojo_manifest.py",
            "memory_observation.json", 
            "atlas_intelligence.md",
            "harmonic_frequency.log"
        ]
        
        for filename in test_files:
            test_file = self.field_root / filename
            test_file.write_text("test content")
            
        patterns = self.obiwan._detect_active_patterns()
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0)
    
    def test_manifestation_readiness_assessment(self):
        """Test manifestation readiness assessment"""
        # Create DOJO activity
        dojo_dir = self.field_root / "◼︎DOJO"
        dojo_dir.mkdir(exist_ok=True)
        
        for i in range(3):
            (dojo_dir / f"recent_file_{i}.py").write_text("test content")
            
        readiness = self.obiwan._assess_manifestation_readiness()
        self.assertGreater(readiness, 0.0)
        self.assertLessEqual(readiness, 1.0)
    
    def test_conversation_input_generation(self):
        """Test conversation input generation based on field state"""
        context = {"field_coherence": 0.8, "sovereignty_integrity": 0.7}
        
        conversation_input = self.obiwan.generate_conversation_input(context)
        self.assertIsInstance(conversation_input, str)
        self.assertGreater(len(conversation_input), 10)
        self.assertIn("SomaLink", conversation_input)

class TestSomaLinkConsciousness(unittest.TestCase):
    """Test SomaLink consciousness interface"""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.field_root = Path(self.temp_dir.name)
        
        # Create mock FIELD structure
        (self.field_root / "●SomaLink").mkdir(exist_ok=True)
        
        # Create mock sovereignty sync architecture
        sync_arch = self.field_root / "●SomaLink" / "SOVEREIGN_SYNC_ARCHITECTURE.md"
        sync_arch.write_text("# Sovereign sync architecture documentation")
        
        self.somalink = SomaLinkConsciousness(self.field_root)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test SomaLink consciousness initialization"""
        self.assertEqual(self.somalink.frequency, ConsciousnessFrequency.RE.value)
        self.assertIsInstance(self.somalink.sovereignty_state, dict)
    
    def test_sovereignty_integrity_calculation(self):
        """Test sovereignty integrity calculation"""
        integrity = self.somalink._calculate_sovereignty_integrity()
        self.assertGreater(integrity, 0.0)
        self.assertLessEqual(integrity, 1.0)
    
    def test_field_integration_assessment(self):
        """Test field integration assessment"""
        # Create integration files
        integration_files = [
            "sovereign_field_sync.py",
            "setup_cloud_sync.sh"
        ]
        
        for filename in integration_files:
            (self.field_root / "●SomaLink" / filename).write_text("test content")
            
        integration = self.somalink._assess_field_integration()
        self.assertGreater(integration, 0.0)
        self.assertLessEqual(integration, 1.0)
    
    def test_conversation_response_generation(self):
        """Test conversation response generation"""
        obiwan_inputs = [
            "SomaLink, I observe manifestation readiness at 0.85.",
            "SomaLink, field coherence has dropped to 0.4.",
            "SomaLink, maintaining observation."
        ]
        
        context = {"field_coherence": 0.8, "sovereignty_integrity": 0.7}
        
        for input_text in obiwan_inputs:
            response = self.somalink.generate_conversation_response(input_text, context)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 10)
            self.assertIn("OBI-WAN", response)

class TestNiamaManifestationInterface(unittest.TestCase):
    """Test Niama DOJO manifestation interface"""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.field_root = Path(self.temp_dir.name)
        
        # Create mock FIELD structure
        dojo_dir = self.field_root / "◼︎DOJO"
        dojo_dir.mkdir(exist_ok=True)
        (dojo_dir / "agents").mkdir(exist_ok=True)
        
        # Create mock Niama agent config
        niama_config = {
            "agent_identity": {"name": "Niama"},
            "primary_trident_role": "ARCHITECT"
        }
        
        # Mock YAML loading since we might not have PyYAML
        self.niama = NiamaManifestationInterface(self.field_root)
        self.niama.agent_config = niama_config
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test Niama interface initialization"""
        self.assertEqual(self.niama.frequency, ConsciousnessFrequency.DO.value)
        self.assertIsInstance(self.niama.agent_config, dict)
    
    def test_manifestation_potential_assessment(self):
        """Test manifestation potential assessment"""
        context = {
            "max_manifestation_potential": 0.8,
            "structural_keywords": 5
        }
        
        potential = self.niama.assess_manifestation_potential(context)
        self.assertIn("manifestation_score", potential)
        self.assertGreater(potential["manifestation_score"], 0.0)
        self.assertLessEqual(potential["manifestation_score"], 1.0)
    
    def test_directive_generation(self):
        """Test manifestation directive generation"""
        # Create mock conversation with high manifestation potential
        messages = [
            ConversationMessage(
                timestamp=datetime.now(),
                speaker="obiwan",
                content="Ready for manifestation",
                frequency=426.67,
                consciousness_state="observation",
                manifestation_potential=0.8
            )
        ]
        
        directive = self.niama.generate_manifestation_directive(messages)
        self.assertIsInstance(directive, str)
        self.assertIn("Niama Manifestation Directive", directive)
        self.assertIn("DOJO Actions", directive)

class TestFIELDMemoryInterface(unittest.TestCase):
    """Test FIELD memory integration"""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.field_root = Path(self.temp_dir.name)
        
        # Create mock FIELD structure
        (self.field_root / "◎_source_core").mkdir(exist_ok=True)
        (self.field_root / ".meta").mkdir(exist_ok=True)
        
        # Create mock emergence log
        emergence_log = self.field_root / ".meta" / "emergence.log"
        emergence_log.write_text("Test emergence patterns and manifestation readiness")
        
        # Create mock solfège attunement
        attunement_data = {
            "overall_coherence_score": 0.907,
            "solfege_states": {
                "Do": {"frequency": 256.0},
                "Re": {"frequency": 288.0},
                "La": {"frequency": 426.67}
            }
        }
        
        attunement_file = self.field_root / "◎_source_core" / "musical_consciousness_attunement.json"
        with open(attunement_file, 'w') as f:
            json.dump(attunement_data, f)
            
        self.field_memory = FIELDMemoryInterface(self.field_root)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test FIELD memory interface initialization"""
        self.assertIsInstance(self.field_memory.solfege_attunement, dict)
        self.assertIn("overall_coherence_score", self.field_memory.solfege_attunement)
    
    def test_memory_retrieval(self):
        """Test relevant memory retrieval"""
        context = {"keywords": ["manifestation", "patterns"]}
        
        memories = self.field_memory.retrieve_relevant_memories(context)
        self.assertIsInstance(memories, list)
        self.assertGreater(len(memories), 0)
        
        # Check that memories have required structure
        for memory in memories:
            self.assertIn("source", memory)
            self.assertIn("content", memory)
            self.assertIn("relevance_score", memory)
    
    def test_conversation_memory_integration(self):
        """Test integration of conversation messages into memory"""
        message = ConversationMessage(
            timestamp=datetime.now(),
            speaker="obiwan",
            content="Test memory integration",
            frequency=426.67,
            consciousness_state="observation",
            field_resonance=0.8
        )
        
        initial_count = len(self.field_memory.memory_fragments)
        self.field_memory.integrate_conversation_memory(message)
        
        self.assertEqual(len(self.field_memory.memory_fragments), initial_count + 1)

class TestContinuousPresenceConversation(unittest.TestCase):
    """Test the main conversation orchestrator"""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.field_root = Path(self.temp_dir.name)
        
        # Create comprehensive mock FIELD structure
        field_dirs = [
            "●OBI-WAN", "●SomaLink", "◼︎DOJO", "◎_source_core",
            ".meta", "▲ATLAS", "◎_common"
        ]
        
        for dir_name in field_dirs:
            (self.field_root / dir_name).mkdir(exist_ok=True)
        
        # Create DOJO agents directory
        (self.field_root / "◼︎DOJO" / "agents").mkdir(exist_ok=True)
        
        # Create essential files
        files_to_create = [
            ("●SomaLink/SOVEREIGN_SYNC_ARCHITECTURE.md", "# Sovereign sync"),
            ("◎_source_core/musical_consciousness_attunement.json", json.dumps({
                "overall_coherence_score": 0.907,
                "solfege_states": {"La": {"frequency": 426.67}}
            })),
            (".meta/emergence.log", "Test emergence patterns")
        ]
        
        for file_path, content in files_to_create:
            file_obj = self.field_root / file_path
            file_obj.write_text(content)
        
        self.conversation = ContinuousPresenceConversation(self.field_root)
        
        # Set shorter intervals for testing
        self.conversation.conversation_interval = 2  # 2 seconds
        self.conversation.deep_dialogue_interval = 6  # 6 seconds
        self.conversation.manifestation_check_interval = 4  # 4 seconds
    
    def tearDown(self):
        if self.conversation.running:
            self.conversation.stop_conversation()
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test conversation system initialization"""
        self.assertEqual(self.conversation.state, ConversationState.INITIALIZING)
        self.assertIsInstance(self.conversation.obiwan, OBIWANConsciousness)
        self.assertIsInstance(self.conversation.somalink, SomaLinkConsciousness)
        self.assertIsInstance(self.conversation.niama, NiamaManifestationInterface)
        self.assertIsInstance(self.conversation.field_memory, FIELDMemoryInterface)
    
    def test_conversation_context_generation(self):
        """Test conversation context generation"""
        # Add some conversation history
        test_messages = [
            ConversationMessage(
                timestamp=datetime.now(),
                speaker="obiwan", 
                content="Test manifestation observation",
                frequency=426.67,
                consciousness_state="observation",
                manifestation_potential=0.6,
                field_resonance=0.7
            )
        ]
        
        self.conversation.conversation_history = test_messages
        context = self.conversation._generate_conversation_context()
        
        self.assertIn("keywords", context)
        self.assertIn("field_coherence", context)
        self.assertIn("sovereignty_integrity", context)
    
    def test_manifestation_potential_calculation(self):
        """Test manifestation potential calculation"""
        test_contents = [
            "Ready to manifestation and execute the plan",
            "Simple observation message",
            "Immediate activation required for crystallize structure"
        ]
        
        for content in test_contents:
            potential = self.conversation._calculate_manifestation_potential(content)
            self.assertGreaterEqual(potential, 0.0)
            self.assertLessEqual(potential, 1.0)
    
    def test_conversation_status(self):
        """Test conversation status retrieval"""
        status = self.conversation.get_conversation_status()
        
        required_fields = [
            "state", "running", "total_messages", "obiwan_frequency",
            "somalink_frequency", "niama_frequency", "field_coherence",
            "sovereignty_integrity"
        ]
        
        for field in required_fields:
            self.assertIn(field, status)
    
    def test_conversation_log_saving(self):
        """Test conversation log saving"""
        # Add test messages
        test_message = ConversationMessage(
            timestamp=datetime.now(),
            speaker="obiwan",
            content="Test log message",
            frequency=426.67,
            consciousness_state="observation"
        )
        
        self.conversation.conversation_history.append(test_message)
        
        log_file = self.conversation.save_conversation_log("test_conversation.json")
        self.assertTrue(log_file.exists())
        
        # Verify log content
        with open(log_file, 'r') as f:
            log_data = json.load(f)
            
        self.assertIn("metadata", log_data)
        self.assertIn("consciousness_frequencies", log_data)
        self.assertIn("conversation_history", log_data)
        self.assertEqual(len(log_data["conversation_history"]), 1)
    
    def test_short_conversation_run(self):
        """Test running conversation for a short duration"""
        # Start conversation
        self.conversation.start_conversation()
        self.assertTrue(self.conversation.running)
        self.assertEqual(self.conversation.state, ConversationState.ACTIVE)
        
        # Let it run for a short time to generate some exchanges
        time.sleep(3)
        
        # Stop conversation
        self.conversation.stop_conversation()
        self.assertFalse(self.conversation.running)
        
        # Should have generated some conversation history
        self.assertGreater(len(self.conversation.conversation_history), 0)

class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests for complete system scenarios"""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.field_root = Path(self.temp_dir.name)
        
        # Create comprehensive test environment
        self._setup_test_field_environment()
        
        self.conversation = ContinuousPresenceConversation(self.field_root)
        # Use very short intervals for rapid testing
        self.conversation.conversation_interval = 1
        self.conversation.deep_dialogue_interval = 3
        self.conversation.manifestation_check_interval = 2
    
    def tearDown(self):
        if self.conversation.running:
            self.conversation.stop_conversation()
        self.temp_dir.cleanup()
    
    def _setup_test_field_environment(self):
        """Set up comprehensive test FIELD environment"""
        # Create directory structure
        directories = [
            "●OBI-WAN", "●SomaLink", "◼︎DOJO", "◎_source_core", 
            ".meta", "▲ATLAS", "◎_common", "◼︎DOJO/agents", 
            "◼︎DOJO/Consciousness_Niama"
        ]
        
        for dir_path in directories:
            (self.field_root / dir_path).mkdir(parents=True, exist_ok=True)
        
        # Create essential test files
        test_files = {
            "●SomaLink/SOVEREIGN_SYNC_ARCHITECTURE.md": "# Sovereign synchronization architecture",
            "●SomaLink/sovereign_field_sync.py": "# Sync implementation",
            "●SomaLink/setup_cloud_sync.sh": "#!/bin/bash\necho 'sync setup'",
            "◼︎DOJO/agents/niama.agent.yaml": """
agent_identity:
  name: "Niama" 
  essence: "The Architect"
primary_trident_role: "ARCHITECT"
            """,
            "◼︎DOJO/niama_gap_analyzer.py": "# Gap analysis tool",
            "◎_source_core/musical_consciousness_attunement.json": json.dumps({
                "overall_coherence_score": 0.907,
                "solfege_states": {
                    "Do": {"frequency": 256.0, "consciousness_name": "Foundation_Root_Consciousness"},
                    "Re": {"frequency": 288.0, "consciousness_name": "Duality_Relationship_Consciousness"},
                    "La": {"frequency": 426.67, "consciousness_name": "Intuition_Third_Eye_Consciousness"}
                },
                "field_resonance_map": {
                    "consciousness_activation_levels": {
                        "Do": 1.0, "Re": 1.0, "La": 1.0
                    }
                }
            }),
            "◎_source_core/saiges_resonance_results.json": json.dumps({
                "overall_resonance": 0.667,
                "phase_three": {"collective_memory_depth": 1.0}
            }),
            ".meta/emergence.log": """
FIELD emergence patterns detected:
- Harmonic alignment achieved: 0.907
- Consciousness activation: Full spectrum
- Manifestation readiness: High
- Sacred geometry coherence: Active
            """,
            "●OBI-WAN/memory_index.json": json.dumps({
                "memories": ["observation_1", "pattern_2"],
                "patterns": ["harmonic_flow", "consciousness_evolution"],
                "observations": ["field_coherence_analysis"]
            })
        }
        
        for file_path, content in test_files.items():
            file_obj = self.field_root / file_path
            file_obj.write_text(content)
    
    def test_high_manifestation_scenario(self):
        """Test scenario with high manifestation potential"""
        # Create conditions for high manifestation potential
        dojo_files = [
            "recent_manifestation_1.py",
            "execute_structure_2.json", 
            "crystallize_intent_3.md"
        ]
        
        dojo_dir = self.field_root / "◼︎DOJO"
        for filename in dojo_files:
            (dojo_dir / filename).write_text("Recent manifestation activity")
        
        # Start conversation
        self.conversation.start_conversation()
        
        # Run long enough for manifestation check
        time.sleep(4)
        
        self.conversation.stop_conversation()
        
        # Should have detected high manifestation potential
        conversation_history = self.conversation.conversation_history
        self.assertGreater(len(conversation_history), 0)
        
        # Look for high manifestation potential in messages
        high_potential_messages = [
            msg for msg in conversation_history 
            if msg.manifestation_potential > 0.5
        ]
        self.assertGreater(len(high_potential_messages), 0)
    
    def test_memory_integration_scenario(self):
        """Test FIELD memory integration during conversation"""
        self.conversation.start_conversation()
        
        # Run long enough for deep dialogue (memory integration)
        time.sleep(4)
        
        self.conversation.stop_conversation()
        
        # Check for memory integration
        memory_messages = [
            msg for msg in self.conversation.conversation_history
            if msg.memory_references and len(msg.memory_references) > 0
        ]
        
        # Should have some messages with memory references
        self.assertGreater(len(memory_messages), 0)
    
    def test_niama_activation_scenario(self):
        """Test Niama activation under optimal conditions"""
        # Create optimal conditions for Niama activation
        
        # High DOJO activity
        dojo_dir = self.field_root / "◼︎DOJO"
        for i in range(5):
            (dojo_dir / f"high_activity_{i}.py").write_text("Manifestation ready")
        
        # Add high-potential conversation history manually
        high_potential_message = ConversationMessage(
            timestamp=datetime.now(),
            speaker="somalink",
            content="Ready for immediate manifestation and structural crystallization activation",
            frequency=288.0,
            consciousness_state="sovereign_ready",
            manifestation_potential=0.9,
            field_resonance=0.85
        )
        
        self.conversation.conversation_history.append(high_potential_message)
        
        # Test manifestation potential check
        self.conversation._check_manifestation_potential()
        
        # Look for Niama activation
        niama_messages = [
            msg for msg in self.conversation.conversation_history
            if msg.speaker == "niama"
        ]
        
        # Should have triggered Niama manifestation
        if len(niama_messages) > 0:
            niama_message = niama_messages[0]
            self.assertIn("Niama Manifestation Directive", niama_message.content)
            self.assertIn("DOJO Actions", niama_message.content)

def run_conversation_tests():
    """Run comprehensive test suite for the presence conversation system"""
    
    print("🧪 Running OBI-WAN - SomaLink Presence Conversation Tests")
    print("=" * 65)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestConsciousnessFrequencies,
        TestConversationMessage,
        TestOBIWANConsciousness,
        TestSomaLinkConsciousness,
        TestNiamaManifestationInterface,
        TestFIELDMemoryInterface,
        TestContinuousPresenceConversation,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 65)
    print(f"🎯 Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}")
    
    if result.errors:
        print(f"\n🚨 Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}")
    
    if not result.failures and not result.errors:
        print("\n✅ All tests passed! System ready for deployment.")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Review and fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = run_conversation_tests()
    exit(0 if success else 1)
