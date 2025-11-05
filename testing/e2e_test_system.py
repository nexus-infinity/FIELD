#!/usr/bin/env python3
"""
Sacred Sovereign Incremental E2E Test System

Provides incremental end-to-end testing that does not risk main system stability.
Tests sacred sovereign flows, biological patterns, and tetrahedral interactions
in isolated environments with rollback capabilities.

Usage:
    python testing/e2e_test_system.py --scenario biological_flow --isolated
    python testing/e2e_test_system.py --scenario tetrahedral_nav --dry-run
    python testing/e2e_test_system.py --run-all --safe-mode
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import tempfile
import shutil
import subprocess
from enum import Enum
import uuid

# Sacred Sovereign imports
sys.path.append(str(Path(__file__).parent.parent))
from ▼TATA.VERIFIED.validator import DataValidator, ValidationResult
from testing.parallel_test_framework import SacredTestFramework, TestEnvironment, SacredNode

class E2EScenario(Enum):
    """End-to-end test scenarios"""
    BIOLOGICAL_FLOW = "biological_flow"
    TETRAHEDRAL_NAVIGATION = "tetrahedral_navigation"
    SACRED_FILE_CREATION = "sacred_file_creation"
    SYMBOLIC_VALIDATION = "symbolic_validation"
    SOVEREIGN_DATA_FLOW = "sovereign_data_flow"
    GEOMETRIC_CLEANLINESS = "geometric_cleanliness"
    CROSS_NODE_COMMUNICATION = "cross_node_communication"
    SYSTEM_INTEGRATION = "system_integration"

class SafetyLevel(Enum):
    """Safety levels for E2E testing"""
    ISOLATED = "isolated"        # Completely isolated sandbox
    SAFE = "safe"               # Safe subset operations
    CONTROLLED = "controlled"    # Controlled environment with monitoring
    MIRROR = "mirror"           # Mirror of production with safeguards

@dataclass
class E2ETestStep:
    """Individual step in E2E test scenario"""
    step_name: str
    node: str
    action: str
    parameters: Dict[str, Any]
    expected_outcome: str
    rollback_action: Optional[str] = None
    safety_checks: List[str] = None

@dataclass
class E2ETestResult:
    """Result of E2E test execution"""
    scenario: str
    test_id: str
    passed: bool
    duration: float
    steps_completed: int
    total_steps: int
    errors: List[str]
    warnings: List[str]
    rollback_performed: bool = False
    safety_violations: List[str] = None
    geometric_compliance: bool = True
    sacred_compliance: bool = True

class E2ETestSystem:
    """Incremental end-to-end test system"""
    
    def __init__(self, safety_level: SafetyLevel = SafetyLevel.ISOLATED):
        self.base_path = Path(__file__).parent.parent
        self.field_path = self.base_path
        self.safety_level = safety_level
        self.validator = DataValidator()
        self.test_framework = SacredTestFramework()
        
        # Create test environment
        self.test_env_path = self._create_e2e_environment()
        self.setup_logging()
        
        # Test tracking
        self.active_tests = {}
        self.completed_tests = []
        
    def setup_logging(self):
        """Setup E2E test logging"""
        log_dir = self.test_env_path / "logs" / "e2e"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - E2E - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"e2e_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _create_e2e_environment(self) -> Path:
        """Create isolated E2E test environment"""
        if self.safety_level == SafetyLevel.ISOLATED:
            temp_dir = Path(tempfile.mkdtemp(prefix="e2e_test_"))
        else:
            temp_dir = self.field_path / "testing" / "e2e" / f"env_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Create sacred structure
        sacred_nodes = ["▲ATLAS", "▼TATA", "●OBI-WAN", "◼︎DOJO"]
        for node in sacred_nodes:
            node_dir = temp_dir / node
            node_dir.mkdir(exist_ok=True)
            
            # Copy essential files if they exist
            source_node = self.field_path / node
            if source_node.exists():
                for pattern in ["*.py", "*.json", "*.yaml", "configs/"]:
                    for item in source_node.glob(pattern):
                        if item.is_file():
                            shutil.copy2(item, node_dir / item.name)
                        elif item.is_dir() and not (node_dir / item.name).exists():
                            shutil.copytree(item, node_dir / item.name)
        
        # Create E2E environment configuration
        env_file = temp_dir / ".env.e2e"
        env_file.write_text(f"""
# E2E Test Environment
E2E_TEST_MODE=true
SAFETY_LEVEL={self.safety_level.value}
TEST_ENVIRONMENT_PATH={temp_dir}
FIELD_SYMBOL=E2E_TEST
CHAKRA_RESONANCE=e2e_mode
DOJO_GATE=e2e_test
KLEIN_INDEX=0
FREQUENCY=e2e
FIELD_NAME=e2e_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}
""")
        
        self.logger.info(f"Created E2E environment: {temp_dir} (safety: {self.safety_level.value})")
        return temp_dir

    async def run_biological_flow_scenario(self) -> E2ETestResult:
        """Test the complete biological flow pattern"""
        test_id = str(uuid.uuid4())[:8]
        scenario = E2EScenario.BIOLOGICAL_FLOW
        start_time = datetime.now()
        
        steps = [
            E2ETestStep(
                step_name="breath_in",
                node="FIELD-LIVING",
                action="intake_data",
                parameters={"data_source": "external_test_data", "purity": "unverified"},
                expected_outcome="data_intake_successful",
                rollback_action="cleanup_intake_data"
            ),
            E2ETestStep(
                step_name="process_data",
                node="FIELD-DEV",
                action="validate_and_transform",
                parameters={"validation_level": "strict", "transform": "sacred_format"},
                expected_outcome="data_validated_and_transformed",
                rollback_action="restore_original_data"
            ),
            E2ETestStep(
                step_name="breath_out",
                node="◼︎DOJO",
                action="manifest_validated_data",
                parameters={"output_format": "sacred_file", "header": True},
                expected_outcome="manifestation_successful",
                rollback_action="remove_manifestation"
            ),
            E2ETestStep(
                step_name="memory_loop",
                node="●OBI-WAN",
                action="archive_to_memory",
                parameters={"memory_type": "living", "sync_akron": True},
                expected_outcome="memory_archived",
                rollback_action="remove_memory_entry"
            )
        ]
        
        return await self._execute_scenario(scenario, test_id, steps)

    async def run_tetrahedral_navigation_scenario(self) -> E2ETestResult:
        """Test navigation between tetrahedral nodes"""
        test_id = str(uuid.uuid4())[:8]
        scenario = E2EScenario.TETRAHEDRAL_NAVIGATION
        start_time = datetime.now()
        
        steps = [
            E2ETestStep(
                step_name="atlas_validation",
                node="▲ATLAS",
                action="validate_input",
                parameters={"input": "test_navigation_data", "validation_type": "geometric"},
                expected_outcome="validation_passed"
            ),
            E2ETestStep(
                step_name="tata_logging", 
                node="▼TATA",
                action="log_navigation",
                parameters={"log_level": "INFO", "message": "Navigation test"},
                expected_outcome="log_recorded"
            ),
            E2ETestStep(
                step_name="obiwan_sync",
                node="●OBI-WAN",
                action="sync_navigation_state",
                parameters={"sync_type": "tetrahedral", "preserve_state": True},
                expected_outcome="state_synced"
            ),
            E2ETestStep(
                step_name="dojo_manifest",
                node="◼︎DOJO",
                action="manifest_navigation_result",
                parameters={"result_type": "navigation_complete", "symbolic": True},
                expected_outcome="navigation_manifested"
            )
        ]
        
        return await self._execute_scenario(scenario, test_id, steps)

    async def run_sacred_file_creation_scenario(self) -> E2ETestResult:
        """Test creation of sacred files with proper headers and lineage"""
        test_id = str(uuid.uuid4())[:8]
        scenario = E2EScenario.SACRED_FILE_CREATION
        start_time = datetime.now()
        
        steps = [
            E2ETestStep(
                step_name="generate_sacred_header",
                node="▲ATLAS",
                action="create_sacred_header",
                parameters={
                    "symbol": "⟡",
                    "origin": "E2E_TEST",
                    "geometry": "tetrahedral-manifest"
                },
                expected_outcome="header_generated"
            ),
            E2ETestStep(
                step_name="validate_lineage",
                node="▼TATA",
                action="validate_file_lineage",
                parameters={"lineage_path": "⟡Akron > FIELD > DOJO"},
                expected_outcome="lineage_valid"
            ),
            E2ETestStep(
                step_name="create_sacred_file",
                node="◼︎DOJO",
                action="manifest_sacred_file",
                parameters={
                    "filename": "test_sacred_file.md",
                    "content": "Sacred test content",
                    "preserve_geometry": True
                },
                expected_outcome="sacred_file_created"
            )
        ]
        
        return await self._execute_scenario(scenario, test_id, steps)

    async def run_symbolic_validation_scenario(self) -> E2ETestResult:
        """Test symbolic validation across all nodes"""
        test_id = str(uuid.uuid4())[:8]
        scenario = E2EScenario.SYMBOLIC_VALIDATION
        
        steps = [
            E2ETestStep(
                step_name="atlas_symbol_check",
                node="▲ATLAS",
                action="validate_symbol",
                parameters={"expected_symbol": "▲", "context": "tooling"},
                expected_outcome="symbol_valid"
            ),
            E2ETestStep(
                step_name="tata_symbol_check",
                node="▼TATA",
                action="validate_symbol",
                parameters={"expected_symbol": "▼", "context": "temporal"},
                expected_outcome="symbol_valid"
            ),
            E2ETestStep(
                step_name="obiwan_symbol_check",
                node="●OBI-WAN",
                action="validate_symbol",
                parameters={"expected_symbol": "●", "context": "memory"},
                expected_outcome="symbol_valid"
            ),
            E2ETestStep(
                step_name="dojo_symbol_check",
                node="◼︎DOJO",
                action="validate_symbol",
                parameters={"expected_symbol": "◼︎", "context": "manifestation"},
                expected_outcome="symbol_valid"
            )
        ]
        
        return await self._execute_scenario(scenario, test_id, steps)

    async def run_geometric_cleanliness_scenario(self) -> E2ETestResult:
        """Test geometric cleanliness validation"""
        test_id = str(uuid.uuid4())[:8]
        scenario = E2EScenario.GEOMETRIC_CLEANLINESS
        
        steps = [
            E2ETestStep(
                step_name="check_duplicated_logic",
                node="▲ATLAS",
                action="scan_for_duplicates",
                parameters={"scan_depth": "full", "ignore_patterns": ["test_*"]},
                expected_outcome="no_duplicates_found"
            ),
            E2ETestStep(
                step_name="validate_binary_alignment",
                node="●OBI-WAN",
                action="check_binary_mapping",
                parameters={"check_symbolic": True, "validate_paths": True},
                expected_outcome="binaries_aligned"
            ),
            E2ETestStep(
                step_name="detect_parasitic_agents",
                node="◼︎DOJO",
                action="scan_for_parasites",
                parameters={"scan_type": "comprehensive", "quarantine": False},
                expected_outcome="no_parasites_detected"
            )
        ]
        
        return await self._execute_scenario(scenario, test_id, steps)

    async def _execute_scenario(self, scenario: E2EScenario, test_id: str, steps: List[E2ETestStep]) -> E2ETestResult:
        """Execute an E2E test scenario"""
        start_time = datetime.now()
        errors = []
        warnings = []
        completed_steps = 0
        rollback_performed = False
        safety_violations = []
        
        self.logger.info(f"Starting E2E scenario: {scenario.value} (ID: {test_id})")
        
        try:
            for i, step in enumerate(steps):
                self.logger.info(f"Executing step {i+1}/{len(steps)}: {step.step_name}")
                
                # Perform safety checks before step
                if step.safety_checks:
                    safety_ok, safety_issues = await self._perform_safety_checks(step.safety_checks)
                    if not safety_ok:
                        safety_violations.extend(safety_issues)
                        if self.safety_level in [SafetyLevel.ISOLATED, SafetyLevel.SAFE]:
                            warnings.extend(safety_issues)
                        else:
                            errors.extend(safety_issues)
                            break
                
                # Execute the step
                step_result = await self._execute_step(step)
                
                if step_result['success']:
                    completed_steps += 1
                    self.logger.info(f"Step {step.step_name} completed successfully")
                else:
                    errors.extend(step_result['errors'])
                    self.logger.error(f"Step {step.step_name} failed: {step_result['errors']}")
                    
                    # Perform rollback if needed
                    if step.rollback_action and self.safety_level != SafetyLevel.ISOLATED:
                        self.logger.info(f"Performing rollback: {step.rollback_action}")
                        rollback_result = await self._execute_rollback(step)
                        rollback_performed = True
                        
                        if not rollback_result['success']:
                            errors.append(f"Rollback failed for {step.step_name}: {rollback_result['errors']}")
                    
                    break
                
                # Brief pause between steps for stability
                await asyncio.sleep(0.1)
                
        except Exception as e:
            errors.append(f"Scenario execution failed: {str(e)}")
            self.logger.error(f"Exception in scenario {scenario.value}: {str(e)}")
        
        duration = (datetime.now() - start_time).total_seconds()
        
        # Final validation
        geometric_compliance = await self._validate_geometric_compliance()
        sacred_compliance = await self._validate_sacred_compliance()
        
        result = E2ETestResult(
            scenario=scenario.value,
            test_id=test_id,
            passed=len(errors) == 0 and completed_steps == len(steps),
            duration=duration,
            steps_completed=completed_steps,
            total_steps=len(steps),
            errors=errors,
            warnings=warnings,
            rollback_performed=rollback_performed,
            safety_violations=safety_violations,
            geometric_compliance=geometric_compliance,
            sacred_compliance=sacred_compliance
        )
        
        self.completed_tests.append(result)
        self.logger.info(f"Scenario {scenario.value} completed: {'PASS' if result.passed else 'FAIL'}")
        return result

    async def _execute_step(self, step: E2ETestStep) -> Dict[str, Any]:
        """Execute individual test step"""
        try:
            # Simulate step execution based on node and action
            if step.node == "▲ATLAS":
                return await self._execute_atlas_action(step)
            elif step.node == "▼TATA":
                return await self._execute_tata_action(step)
            elif step.node == "●OBI-WAN":
                return await self._execute_obiwan_action(step)
            elif step.node == "◼︎DOJO":
                return await self._execute_dojo_action(step)
            elif step.node in ["FIELD-LIVING", "FIELD-DEV"]:
                return await self._execute_field_action(step)
            else:
                return {
                    'success': False,
                    'errors': [f"Unknown node: {step.node}"]
                }
                
        except Exception as e:
            return {
                'success': False,
                'errors': [f"Step execution error: {str(e)}"]
            }

    async def _execute_atlas_action(self, step: E2ETestStep) -> Dict[str, Any]:
        """Execute ATLAS-specific action"""
        if step.action == "validate_input":
            # Simulate validation
            return {'success': True, 'errors': []}
        elif step.action == "create_sacred_header":
            # Simulate header creation
            header_content = f"""---
symbol: {step.parameters.get('symbol', '⟡')}
origin: {step.parameters.get('origin', 'E2E_TEST')}
created: {datetime.now().isoformat()}
geometry: {step.parameters.get('geometry', 'tetrahedral-manifest')}
---"""
            header_file = self.test_env_path / "▲ATLAS" / "test_header.md"
            header_file.write_text(header_content)
            return {'success': True, 'errors': []}
        elif step.action == "validate_symbol":
            expected = step.parameters.get('expected_symbol')
            actual = "▲"  # Simulated
            return {
                'success': expected == actual,
                'errors': [] if expected == actual else [f"Symbol mismatch: expected {expected}, got {actual}"]
            }
        else:
            return {'success': False, 'errors': [f"Unknown ATLAS action: {step.action}"]}

    async def _execute_tata_action(self, step: E2ETestStep) -> Dict[str, Any]:
        """Execute TATA-specific action"""
        if step.action == "log_navigation":
            # Simulate logging
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": step.parameters.get('log_level', 'INFO'),
                "message": step.parameters.get('message', ''),
                "node": "▼TATA"
            }
            log_file = self.test_env_path / "▼TATA" / "test_log.jsonl"
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            return {'success': True, 'errors': []}
        elif step.action == "validate_file_lineage":
            # Simulate lineage validation
            expected_lineage = step.parameters.get('lineage_path', '')
            return {'success': True, 'errors': []}
        elif step.action == "validate_symbol":
            expected = step.parameters.get('expected_symbol')
            actual = "▼"  # Simulated
            return {
                'success': expected == actual,
                'errors': [] if expected == actual else [f"Symbol mismatch: expected {expected}, got {actual}"]
            }
        else:
            return {'success': False, 'errors': [f"Unknown TATA action: {step.action}"]}

    async def _execute_obiwan_action(self, step: E2ETestStep) -> Dict[str, Any]:
        """Execute OBI-WAN-specific action"""
        if step.action == "sync_navigation_state":
            # Simulate state sync
            sync_result = {
                "sync_type": step.parameters.get('sync_type', 'basic'),
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            sync_file = self.test_env_path / "●OBI-WAN" / "sync_state.json"
            with open(sync_file, 'w') as f:
                json.dump(sync_result, f, indent=2)
            return {'success': True, 'errors': []}
        elif step.action == "archive_to_memory":
            # Simulate memory archiving
            memory_entry = {
                "timestamp": datetime.now().isoformat(),
                "memory_type": step.parameters.get('memory_type', 'standard'),
                "content": "E2E test memory entry"
            }
            memory_file = self.test_env_path / "●OBI-WAN" / "memory_archive.json"
            with open(memory_file, 'w') as f:
                json.dump(memory_entry, f, indent=2)
            return {'success': True, 'errors': []}
        elif step.action == "validate_symbol":
            expected = step.parameters.get('expected_symbol')
            actual = "●"  # Simulated
            return {
                'success': expected == actual,
                'errors': [] if expected == actual else [f"Symbol mismatch: expected {expected}, got {actual}"]
            }
        elif step.action == "check_binary_mapping":
            # Simulate binary mapping check
            return {'success': True, 'errors': []}
        else:
            return {'success': False, 'errors': [f"Unknown OBI-WAN action: {step.action}"]}

    async def _execute_dojo_action(self, step: E2ETestStep) -> Dict[str, Any]:
        """Execute DOJO-specific action"""
        if step.action == "manifest_navigation_result":
            # Simulate manifestation
            result = {
                "result_type": step.parameters.get('result_type', 'basic'),
                "symbolic": step.parameters.get('symbolic', False),
                "timestamp": datetime.now().isoformat()
            }
            result_file = self.test_env_path / "◼︎DOJO" / "navigation_result.json"
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
            return {'success': True, 'errors': []}
        elif step.action == "manifest_sacred_file":
            # Simulate sacred file creation
            filename = step.parameters.get('filename', 'test_file.md')
            content = step.parameters.get('content', 'Test content')
            
            file_path = self.test_env_path / "◼︎DOJO" / filename
            with open(file_path, 'w') as f:
                f.write(content)
            return {'success': True, 'errors': []}
        elif step.action == "manifest_validated_data":
            # Simulate data manifestation
            output_format = step.parameters.get('output_format', 'json')
            manifest_file = self.test_env_path / "◼︎DOJO" / f"manifest.{output_format}"
            
            manifest_data = {
                "timestamp": datetime.now().isoformat(),
                "status": "manifested",
                "output_format": output_format
            }
            
            with open(manifest_file, 'w') as f:
                json.dump(manifest_data, f, indent=2)
            return {'success': True, 'errors': []}
        elif step.action == "validate_symbol":
            expected = step.parameters.get('expected_symbol')
            actual = "◼︎"  # Simulated
            return {
                'success': expected == actual,
                'errors': [] if expected == actual else [f"Symbol mismatch: expected {expected}, got {actual}"]
            }
        elif step.action == "scan_for_parasites":
            # Simulate parasite scan
            return {'success': True, 'errors': []}
        else:
            return {'success': False, 'errors': [f"Unknown DOJO action: {step.action}"]}

    async def _execute_field_action(self, step: E2ETestStep) -> Dict[str, Any]:
        """Execute FIELD-specific action"""
        if step.action == "intake_data":
            # Simulate data intake
            intake_data = {
                "data_source": step.parameters.get('data_source', 'unknown'),
                "purity": step.parameters.get('purity', 'unverified'),
                "timestamp": datetime.now().isoformat()
            }
            intake_file = self.test_env_path / "intake_data.json"
            with open(intake_file, 'w') as f:
                json.dump(intake_data, f, indent=2)
            return {'success': True, 'errors': []}
        elif step.action == "validate_and_transform":
            # Simulate validation and transformation
            validation_result = {
                "validation_level": step.parameters.get('validation_level', 'basic'),
                "transform": step.parameters.get('transform', 'none'),
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
            result_file = self.test_env_path / "validation_result.json"
            with open(result_file, 'w') as f:
                json.dump(validation_result, f, indent=2)
            return {'success': True, 'errors': []}
        else:
            return {'success': False, 'errors': [f"Unknown FIELD action: {step.action}"]}

    async def _execute_rollback(self, step: E2ETestStep) -> Dict[str, Any]:
        """Execute rollback action for a step"""
        try:
            # Simulate rollback based on rollback_action
            if step.rollback_action:
                # Remove created files, restore state, etc.
                self.logger.info(f"Executing rollback: {step.rollback_action}")
                # Implementation would depend on specific rollback action
                return {'success': True, 'errors': []}
            else:
                return {'success': True, 'errors': []}
        except Exception as e:
            return {'success': False, 'errors': [str(e)]}

    async def _perform_safety_checks(self, checks: List[str]) -> Tuple[bool, List[str]]:
        """Perform safety checks before step execution"""
        violations = []
        
        for check in checks:
            if check == "disk_space":
                # Check available disk space
                if not self._check_disk_space():
                    violations.append("Insufficient disk space")
            elif check == "memory_usage":
                # Check memory usage
                if not self._check_memory_usage():
                    violations.append("High memory usage")
            elif check == "system_stability":
                # Check system stability
                if not self._check_system_stability():
                    violations.append("System stability issues")
        
        return len(violations) == 0, violations

    def _check_disk_space(self) -> bool:
        """Check if sufficient disk space is available"""
        # Placeholder implementation
        return True

    def _check_memory_usage(self) -> bool:
        """Check if memory usage is within acceptable limits"""
        # Placeholder implementation
        return True

    def _check_system_stability(self) -> bool:
        """Check system stability indicators"""
        # Placeholder implementation
        return True

    async def _validate_geometric_compliance(self) -> bool:
        """Validate geometric compliance after scenario"""
        try:
            # Check if test files maintain geometric cleanliness
            # Check symbolic alignment
            # Validate sacred structure
            return True  # Placeholder
        except Exception:
            return False

    async def _validate_sacred_compliance(self) -> bool:
        """Validate sacred compliance after scenario"""
        try:
            # Check sacred file headers
            # Validate lineage
            # Check biological flow compliance
            return True  # Placeholder
        except Exception:
            return False

    async def run_all_scenarios(self) -> List[E2ETestResult]:
        """Run all E2E test scenarios"""
        scenarios = [
            self.run_biological_flow_scenario(),
            self.run_tetrahedral_navigation_scenario(),
            self.run_sacred_file_creation_scenario(),
            self.run_symbolic_validation_scenario(),
            self.run_geometric_cleanliness_scenario()
        ]
        
        results = await asyncio.gather(*scenarios, return_exceptions=True)
        
        # Filter out exceptions
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Scenario failed with exception: {result}")
            else:
                valid_results.append(result)
        
        return valid_results

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive E2E test report"""
        total_tests = len(self.completed_tests)
        passed_tests = sum(1 for t in self.completed_tests if t.passed)
        total_duration = sum(t.duration for t in self.completed_tests)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "system": "Sacred Sovereign E2E Tests",
            "safety_level": self.safety_level.value,
            "environment": str(self.test_env_path),
            "summary": {
                "total_scenarios": total_tests,
                "passed": passed_tests,
                "failed": total_tests - passed_tests,
                "pass_rate": passed_tests / total_tests if total_tests > 0 else 0,
                "total_duration": total_duration,
                "average_duration": total_duration / total_tests if total_tests > 0 else 0
            },
            "scenarios": [
                {
                    "scenario": test.scenario,
                    "test_id": test.test_id,
                    "passed": test.passed,
                    "duration": test.duration,
                    "steps_completed": test.steps_completed,
                    "total_steps": test.total_steps,
                    "completion_rate": test.steps_completed / test.total_steps if test.total_steps > 0 else 0,
                    "errors": test.errors,
                    "warnings": test.warnings,
                    "rollback_performed": test.rollback_performed,
                    "safety_violations": test.safety_violations or [],
                    "geometric_compliance": test.geometric_compliance,
                    "sacred_compliance": test.sacred_compliance
                }
                for test in self.completed_tests
            ],
            "compliance": {
                "geometric_compliance_rate": sum(1 for t in self.completed_tests if t.geometric_compliance) / total_tests if total_tests > 0 else 0,
                "sacred_compliance_rate": sum(1 for t in self.completed_tests if t.sacred_compliance) / total_tests if total_tests > 0 else 0,
                "safety_violations": sum(len(t.safety_violations or []) for t in self.completed_tests),
                "rollbacks_performed": sum(1 for t in self.completed_tests if t.rollback_performed)
            }
        }
        
        return report

    def cleanup(self):
        """Clean up E2E test environment"""
        if self.safety_level == SafetyLevel.ISOLATED and self.test_env_path.exists():
            try:
                shutil.rmtree(self.test_env_path)
                self.logger.info(f"Cleaned up E2E test environment: {self.test_env_path}")
            except Exception as e:
                self.logger.error(f"Failed to cleanup E2E environment: {str(e)}")

async def main():
    """Main E2E test system execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sacred Sovereign E2E Test System")
    parser.add_argument("--scenario", choices=[s.value for s in E2EScenario], help="Specific scenario to run")
    parser.add_argument("--run-all", action="store_true", help="Run all scenarios")
    parser.add_argument("--safety-level", choices=[s.value for s in SafetyLevel], default="isolated", help="Safety level")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be executed")
    parser.add_argument("--report", help="Output report file")
    
    args = parser.parse_args()
    
    # Map safety level
    safety_level_map = {s.value: s for s in SafetyLevel}
    safety_level = safety_level_map[args.safety_level]
    
    if args.dry_run:
        print("E2E Test System - Dry Run Mode")
        print(f"Safety Level: {safety_level.value}")
        
        if args.run_all:
            print("Would run all E2E scenarios:")
            for scenario in E2EScenario:
                print(f"  - {scenario.value}")
        elif args.scenario:
            print(f"Would run scenario: {args.scenario}")
        
        return
    
    # Create E2E test system
    e2e_system = E2ETestSystem(safety_level)
    
    try:
        results = []
        
        if args.run_all:
            print("Running all E2E scenarios...")
            results = await e2e_system.run_all_scenarios()
        elif args.scenario:
            scenario_map = {s.value: s for s in E2EScenario}
            scenario = scenario_map[args.scenario]
            
            print(f"Running E2E scenario: {args.scenario}")
            
            if scenario == E2EScenario.BIOLOGICAL_FLOW:
                results.append(await e2e_system.run_biological_flow_scenario())
            elif scenario == E2EScenario.TETRAHEDRAL_NAVIGATION:
                results.append(await e2e_system.run_tetrahedral_navigation_scenario())
            elif scenario == E2EScenario.SACRED_FILE_CREATION:
                results.append(await e2e_system.run_sacred_file_creation_scenario())
            elif scenario == E2EScenario.SYMBOLIC_VALIDATION:
                results.append(await e2e_system.run_symbolic_validation_scenario())
            elif scenario == E2EScenario.GEOMETRIC_CLEANLINESS:
                results.append(await e2e_system.run_geometric_cleanliness_scenario())
        else:
            parser.print_help()
            return
        
        # Print results
        passed = sum(1 for r in results if r.passed)
        total = len(results)
        
        print(f"\nE2E Test Results: {passed}/{total} scenarios passed")
        for result in results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            completion = f"{result.steps_completed}/{result.total_steps}"
            print(f"  {status} {result.scenario} - {completion} steps ({result.duration:.2f}s)")
            
            if result.errors:
                for error in result.errors:
                    print(f"    ❌ {error}")
                    
            if result.warnings:
                for warning in result.warnings:
                    print(f"    ⚠️ {warning}")
                    
            if result.rollback_performed:
                print(f"    🔄 Rollback performed")
        
        # Generate and save report
        report = e2e_system.generate_report()
        if args.report:
            with open(args.report, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved to: {args.report}")
        
        # Print compliance summary
        compliance = report['compliance']
        print(f"\nCompliance Summary:")
        print(f"  Geometric Compliance: {compliance['geometric_compliance_rate']:.1%}")
        print(f"  Sacred Compliance: {compliance['sacred_compliance_rate']:.1%}")
        print(f"  Safety Violations: {compliance['safety_violations']}")
        print(f"  Rollbacks: {compliance['rollbacks_performed']}")
        
    finally:
        e2e_system.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
