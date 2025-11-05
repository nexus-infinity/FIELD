#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Sacred File Header
# Symbol: ▼
# Origin: ~/FIELD/scripts/
# Created: 2025-08-06T10:14:51+10:00
# Geometry: tetrahedral-manifest
# Lineage: ⟡Akron > FIELD > TATA

"""
Sacred Protocol Validation Script
=================================

Validates all sacred protocols, configurations, and validation scripts
to ensure complete documentation and compliance with sacred geometry.
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

class SacredProtocolValidator:
    """Validates sacred protocol documentation and compliance"""
    
    def __init__(self):
        self.field_path = Path("/Users/jbear/FIELD")
        self.protocols = {}
        self.configs = {}
        self.validation_scripts = {}
        self.audit_results = {
            'protocols': {'documented': 0, 'total': 0, 'missing': []},
            'configs': {'documented': 0, 'total': 0, 'missing': []},
            'scripts': {'documented': 0, 'total': 0, 'missing': []},
            'compliance_score': 0.0
        }
    
    def validate_all_protocols(self) -> Dict[str, Any]:
        """Run complete protocol validation"""
        print("🔍 Sacred Protocol Validation Starting...")
        print("=" * 60)
        
        # Validate core protocols
        self._validate_sacred_protocols()
        
        # Validate configuration files
        self._validate_configuration_files()
        
        # Validate validation scripts
        self._validate_validation_scripts()
        
        # Calculate compliance score
        self._calculate_compliance_score()
        
        # Generate report
        return self._generate_validation_report()
    
    def _validate_sacred_protocols(self):
        """Validate sacred protocol documentation"""
        print("\n▲ Validating Sacred Protocols...")
        
        expected_protocols = [
            "SACRED_SOVEREIGN_INTEGRATION.md",
            "sovereign_field_motion_protocol.md", 
            "sacred-chat-bridge.js",
            "sacred_validation_demo.py",
            "sacred-cli-tools.js",
            "sacred-startup.sh"
        ]
        
        for protocol in expected_protocols:
            found = self._find_file(protocol)
            if found:
                self.protocols[protocol] = {
                    'path': found,
                    'exists': True,
                    'documented': True
                }
                self.audit_results['protocols']['documented'] += 1
                print(f"  ✅ {protocol}")
            else:
                self.protocols[protocol] = {
                    'path': None,
                    'exists': False,
                    'documented': False
                }
                self.audit_results['protocols']['missing'].append(protocol)
                print(f"  ❌ {protocol} - NOT FOUND")
        
        self.audit_results['protocols']['total'] = len(expected_protocols)
    
    def _validate_configuration_files(self):
        """Validate configuration file documentation"""
        print("\n◼︎ Validating Configuration Files...")
        
        expected_configs = [
            "sacred-config.json",
            "FIELD_COMPLETION_INDEX.md",
            "package.json"  # For DOJO node modules
        ]
        
        for config in expected_configs:
            found = self._find_file(config)
            if found:
                self.configs[config] = {
                    'path': found,
                    'exists': True,
                    'valid': self._validate_config_syntax(found, config)
                }
                self.audit_results['configs']['documented'] += 1
                status = "✅" if self.configs[config]['valid'] else "⚠️"
                print(f"  {status} {config}")
            else:
                self.configs[config] = {
                    'path': None,
                    'exists': False,
                    'valid': False
                }
                self.audit_results['configs']['missing'].append(config)
                print(f"  ❌ {config} - NOT FOUND")
        
        self.audit_results['configs']['total'] = len(expected_configs)
    
    def _validate_validation_scripts(self):
        """Validate validation script documentation"""
        print("\n● Validating Validation Scripts...")
        
        expected_scripts = [
            "sacred_validation_demo.py",
            "sacred_dashboard_monitor.py", 
            "sacred_incremental_deployment.py",
            "run_sacred_deployment.sh"
        ]
        
        for script in expected_scripts:
            found = self._find_file(script)
            if found:
                self.validation_scripts[script] = {
                    'path': found,
                    'exists': True,
                    'executable': os.access(found, os.X_OK)
                }
                self.audit_results['scripts']['documented'] += 1
                exec_status = "✅" if self.validation_scripts[script]['executable'] else "⚠️"
                print(f"  {exec_status} {script}")
            else:
                self.validation_scripts[script] = {
                    'path': None,
                    'exists': False,
                    'executable': False
                }
                self.audit_results['scripts']['missing'].append(script)
                print(f"  ❌ {script} - NOT FOUND")
        
        self.audit_results['scripts']['total'] = len(expected_scripts)
    
    def _find_file(self, filename: str) -> str:
        """Find a file within the FIELD directory structure"""
        for root, dirs, files in os.walk(self.field_path):
            if filename in files:
                return os.path.join(root, filename)
        return None
    
    def _validate_config_syntax(self, filepath: str, filename: str) -> bool:
        """Validate configuration file syntax"""
        try:
            if filename.endswith('.json'):
                with open(filepath, 'r') as f:
                    json.load(f)
                return True
            elif filename.endswith('.md'):
                # Check for sacred header format
                with open(filepath, 'r') as f:
                    content = f.read()
                    return '---' in content and 'symbol:' in content
            else:
                return True  # Assume other files are valid if they exist
        except (json.JSONDecodeError, IOError):
            return False
    
    def _calculate_compliance_score(self):
        """Calculate overall protocol compliance score"""
        total_items = (
            self.audit_results['protocols']['total'] +
            self.audit_results['configs']['total'] +
            self.audit_results['scripts']['total']
        )
        
        documented_items = (
            self.audit_results['protocols']['documented'] +
            self.audit_results['configs']['documented'] +
            self.audit_results['scripts']['documented']
        )
        
        if total_items > 0:
            self.audit_results['compliance_score'] = (documented_items / total_items) * 100
        else:
            self.audit_results['compliance_score'] = 0.0
    
    def _generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        print("\n" + "=" * 60)
        print("🏆 SACRED PROTOCOL VALIDATION REPORT")
        print("=" * 60)
        
        # Summary
        print(f"\nProtocols Documented: {self.audit_results['protocols']['documented']}/{self.audit_results['protocols']['total']}")
        print(f"Configurations Valid: {self.audit_results['configs']['documented']}/{self.audit_results['configs']['total']}")
        print(f"Scripts Available: {self.audit_results['scripts']['documented']}/{self.audit_results['scripts']['total']}")
        
        # Compliance score
        score = self.audit_results['compliance_score']
        print(f"\nOverall Compliance Score: {score:.1f}%")
        
        if score >= 95:
            print("🌟 EXCELLENT - Sacred protocols fully documented")
        elif score >= 85:
            print("✅ GOOD - Minor documentation gaps")
        elif score >= 70:
            print("⚠️ WARNING - Significant documentation needed")
        else:
            print("❌ CRITICAL - Major protocol documentation required")
        
        # Missing items
        if self.audit_results['protocols']['missing']:
            print("\nMissing Protocols:")
            for protocol in self.audit_results['protocols']['missing']:
                print(f"  - {protocol}")
        
        if self.audit_results['configs']['missing']:
            print("\nMissing Configurations:")
            for config in self.audit_results['configs']['missing']:
                print(f"  - {config}")
        
        if self.audit_results['scripts']['missing']:
            print("\nMissing Scripts:")
            for script in self.audit_results['scripts']['missing']:
                print(f"  - {script}")
        
        # Recommendations
        print("\n🔮 RECOMMENDATIONS:")
        if score < 100:
            print("  • Document missing protocols in canonical locations")
            print("  • Ensure all configuration files are valid and accessible")
            print("  • Make validation scripts executable with proper permissions")
            print("  • Update FIELD_COMPLETION_INDEX.md with any changes")
        else:
            print("  • Maintain current excellent documentation standards")
            print("  • Continue regular protocol validation checks")
            print("  • Monitor for new protocols requiring documentation")
        
        print(f"\n⟡ Sacred Protocol Validation Complete: {score:.1f}% Compliance")
        print("=" * 60)
        
        return self.audit_results


def main():
    """Main validation function"""
    validator = SacredProtocolValidator()
    results = validator.validate_all_protocols()
    
    # Exit with appropriate code based on compliance
    if results['compliance_score'] >= 95:
        sys.exit(0)  # Excellent
    elif results['compliance_score'] >= 85:
        sys.exit(1)  # Good but needs attention
    else:
        sys.exit(2)  # Critical issues


if __name__ == "__main__":
    main()
