#!/usr/bin/env python3
"""
BERJAK | NEXUS | INFINITY FRE Test Runner
Validates the integration between pure design and field implementation
"""

import unittest
from pathlib import Path
from extraction_engine import ExtractionEngine
from pipeline_config import PipelineConfig

class TestFREIntegration(unittest.TestCase):
    def setUp(self):
        self.pipeline = PipelineConfig()
        self.engine = ExtractionEngine(Path('name_mappings.json'))
        
    def test_name_normalization(self):
        """Test entity name normalization"""
        test_cases = [
            ('Bircheck Pty Ltd', 'Berjak Pty Ltd'),
            ('Sentosa Trust', 'Centosa Trust'),
            ('Wisewould Mahoney', 'Wisewould Mahony')
        ]
        
        for input_name, expected in test_cases:
            normalized = self.engine.normalize_name(input_name)
            self.assertEqual(normalized, expected)
            
    def test_provenance_tracking(self):
        """Test provenance logging"""
        test_file = "test_document.pdf"
        test_content = "Test content"
        
        # Create test document
        with open(test_file, 'w') as f:
            f.write(test_content)
            
        file_hash = self.engine.compute_file_hash(test_file)
        self.assertTrue(len(file_hash) == 64)  # SHA-256 hash length
        
        Path(test_file).unlink()  # Cleanup
        
    def test_pipeline_configuration(self):
        """Test pipeline configuration"""
        self.pipeline.create_directory_structure()
        
        # Verify directory structure
        for source in self.pipeline.config['input_sources'].values():
            self.assertTrue(source['path'].exists())
            
        for output_dir in self.pipeline.config['output'].values():
            self.assertTrue(output_dir.exists())
            
    def test_manifest_generation(self):
        """Test processing manifest generation"""
        manifest = self.pipeline.generate_processing_manifest()
        
        self.assertIn('timestamp', manifest)
        self.assertIn('input_files', manifest)
        self.assertIn('processing_rules', manifest)
        self.assertIn('output_paths', manifest)

if __name__ == '__main__':
    unittest.main()