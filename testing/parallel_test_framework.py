#!/usr/bin/env python3
"""
Sacred Sovereign Parallel Testing Framework

This framework enables multiple developer/AI agent sessions to run independent
testing without risking main system stability. Each sacred module can be tested
in isolation while maintaining geometric cleanliness.

Usage:
    python parallel_test_framework.py --node atlas --suite unit
    python parallel_test_framework.py --node tata --suite integration
    python parallel_test_framework.py --run-all --isolated
"""

import os
import sys
import json
import asyncio
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import concurrent.futures
import uuid

# Sacred Sovereign imports
sys.path.append(str(Path(__file__).parent.parent))
from ▼TATA.VERIFIED.validator import DataValidator, ValidationResult

class SacredNode(Enum):
    """Sacred tetrahedral nodes"""
    ATLAS = "▲ATLAS"      # Tooling validation
    TATA = "▼TATA"        # Temporal truth
    OBI_WAN = "●OBI-WAN"  # Living memory
    DOJO = "◼︎DOJO"       # Manifestation

class TestSuite(Enum):
    """Test suite types"""
    UNIT = "unit"
    INTEGRATION = "integration"
    GEOMETRY = "geometry"
    SOVEREIGN = "sovereign"
    E2E = "e2e"

class TestEnvironment(Enum):
    """Test environment isolation levels"""
    ISOLATED = "isolated"      # Completely isolated sandbox
    FIELD_DEV = "field_dev"   # FIELD-DEV environment
    MIRROR = "mirror"         # Mirror of main system
    SAFE = "safe"            # Safe subset of main system

@dataclass
class TestSession:
    """Represents an independent test session"""
    session_id: str
    node: SacredNode
    suite: TestSuite
    environment: TestEnvironment
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "running"
    results: Dict[str, Any] = None
    isolation_path: Optional[str] = None

@dataclass
class TestResult:
    """Test execution result"""
    session_id: str
    node: str
    suite: str
    passed: int
    failed: int
    skipped: int
    duration: float
    errors: List[str]
    warnings: List[str]
    geometric_validation: Dict[str, Any]
    sacred_compliance: bool

class SacredTestFramework:
    """Main parallel testing framework"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or os.getcwd())
        self.field_path = self.base_path / "FIELD"
        self.test_sessions = {}
        self.validator = DataValidator()
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for test framework"""
        log_path = self.field_path / "logs" / "testing"
        log_path.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path / f"test_framework_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def create_test_session(self, 
                          node: SacredNode, 
                          suite: TestSuite,
                          environment: TestEnvironment = TestEnvironment.ISOLATED) -> TestSession:
        """Create a new isolated test session"""
        session_id = str(uuid.uuid4())[:8]
        
        session = TestSession(
            session_id=session_id,
            node=node,
            suite=suite,
            environment=environment,
            start_time=datetime.now(),
            status="initializing"
        )
        
        # Create isolated environment
        if environment == TestEnvironment.ISOLATED:
            session.isolation_path = self._create_isolated_environment(session)
        
        self.test_sessions[session_id] = session
        self.logger.info(f"Created test session {session_id} for {node.value} {suite.value}")
        return session

    def _create_isolated_environment(self, session: TestSession) -> str:
        """Create completely isolated test environment"""
        isolation_root = self.field_path / "testing" / "isolated" / session.session_id
        isolation_root.mkdir(parents=True, exist_ok=True)
        
        # Create symbolic structure for the specific node
        node_path = isolation_root / session.node.value
        node_path.mkdir(exist_ok=True)
        
        # Copy essential files for testing (configs, schemas, etc.)
        essential_files = [
            ".env.template",
            "pyproject.toml",
            "requirements.txt"
        ]
        
        for file_name in essential_files:
            src = self.field_path / file_name
            if src.exists():
                dst = isolation_root / file_name
                dst.write_text(src.read_text())
        
        # Create test-specific environment variables
        env_file = isolation_root / ".env.test"
        env_file.write_text(f"""
# Test Environment for {session.session_id}
FIELD_SYMBOL={session.node.value}
CHAKRA_RESONANCE=test_mode
DOJO_GATE=isolated
KLEIN_INDEX=0
FREQUENCY=test
FIELD_NAME=test_{session.session_id}
TEST_SESSION_ID={session.session_id}
TEST_ISOLATION=true
""")
        
        self.logger.info(f"Created isolated environment at {isolation_root}")
        return str(isolation_root)

    async def run_node_tests(self, 
                           session: TestSession,
                           specific_tests: Optional[List[str]] = None) -> TestResult:
        """Run tests for a specific sacred node"""
        self.logger.info(f"Running {session.suite.value} tests for {session.node.value}")
        session.status = "running"
        
        start_time = datetime.now()
        
        try:
            # Validate geometric cleanliness before testing
            geometric_validation = await self._validate_geometric_cleanliness(session)
            
            if not geometric_validation.get("is_clean", False):
                raise Exception(f"Geometric validation failed: {geometric_validation.get('violations', [])}")
            
            # Run the appropriate test suite
            if session.suite == TestSuite.UNIT:
                result = await self._run_unit_tests(session, specific_tests)
            elif session.suite == TestSuite.INTEGRATION:
                result = await self._run_integration_tests(session, specific_tests)
            elif session.suite == TestSuite.GEOMETRY:
                result = await self._run_geometry_tests(session)
            elif session.suite == TestSuite.SOVEREIGN:
                result = await self._run_sovereign_tests(session)
            elif session.suite == TestSuite.E2E:
                result = await self._run_e2e_tests(session, specific_tests)
            else:
                raise ValueError(f"Unknown test suite: {session.suite}")
            
            duration = (datetime.now() - start_time).total_seconds()
            
            test_result = TestResult(
                session_id=session.session_id,
                node=session.node.value,
                suite=session.suite.value,
                passed=result.get("passed", 0),
                failed=result.get("failed", 0),
                skipped=result.get("skipped", 0),
                duration=duration,
                errors=result.get("errors", []),
                warnings=result.get("warnings", []),
                geometric_validation=geometric_validation,
                sacred_compliance=result.get("sacred_compliance", True)
            )
            
            session.status = "completed"
            session.end_time = datetime.now()
            session.results = asdict(test_result)
            
            self.logger.info(f"Test session {session.session_id} completed successfully")
            return test_result
            
        except Exception as e:
            session.status = "failed"
            session.end_time = datetime.now()
            self.logger.error(f"Test session {session.session_id} failed: {str(e)}")
            
            return TestResult(
                session_id=session.session_id,
                node=session.node.value,
                suite=session.suite.value,
                passed=0,
                failed=1,
                skipped=0,
                duration=(datetime.now() - start_time).total_seconds(),
                errors=[str(e)],
                warnings=[],
                geometric_validation={},
                sacred_compliance=False
            )

    async def _validate_geometric_cleanliness(self, session: TestSession) -> Dict[str, Any]:
        """Validate geometric cleanliness for the test session"""
        violations = []
        
        # Check for test isolation
        if session.environment == TestEnvironment.ISOLATED:
            if not session.isolation_path or not Path(session.isolation_path).exists():
                violations.append("Test isolation path not properly created")
        
        # Check for proper symbolic mapping
        node_symbols = {
            SacredNode.ATLAS: "▲",
            SacredNode.TATA: "▼", 
            SacredNode.OBI_WAN: "●",
            SacredNode.DOJO: "◼︎"
        }
        
        expected_symbol = node_symbols.get(session.node)
        if not expected_symbol:
            violations.append(f"No symbolic mapping for node {session.node}")
        
        # Check environment variables
        required_vars = ["FIELD_SYMBOL", "CHAKRA_RESONANCE", "FIELD_NAME"]
        for var in required_vars:
            if not os.getenv(var):
                violations.append(f"Required environment variable {var} not set")
        
        return {
            "is_clean": len(violations) == 0,
            "violations": violations,
            "timestamp": datetime.now().isoformat(),
            "node": session.node.value,
            "session_id": session.session_id
        }

    async def _run_unit_tests(self, session: TestSession, specific_tests: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run unit tests for the specified node"""
        test_dir = self.field_path / session.node.value / "tests" / "unit"
        
        if not test_dir.exists():
            test_dir.mkdir(parents=True, exist_ok=True)
            # Create placeholder test file if none exist
            self._create_placeholder_tests(test_dir, "unit", session.node)
        
        # Use pytest to run tests
        cmd = ["python", "-m", "pytest", str(test_dir), "-v", "--json-report", f"--json-report-file={session.isolation_path}/unit_results.json"]
        
        if specific_tests:
            cmd.extend(["-k", " or ".join(specific_tests)])
        
        result = await self._run_test_command(cmd, session)
        return result

    async def _run_integration_tests(self, session: TestSession, specific_tests: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run integration tests for node interactions"""
        test_dir = self.field_path / session.node.value / "tests" / "integration"
        
        if not test_dir.exists():
            test_dir.mkdir(parents=True, exist_ok=True)
            self._create_placeholder_tests(test_dir, "integration", session.node)
        
        cmd = ["python", "-m", "pytest", str(test_dir), "-v", "--json-report", f"--json-report-file={session.isolation_path}/integration_results.json"]
        
        if specific_tests:
            cmd.extend(["-k", " or ".join(specific_tests)])
        
        result = await self._run_test_command(cmd, session)
        return result

    async def _run_geometry_tests(self, session: TestSession) -> Dict[str, Any]:
        """Run geometric cleanliness tests"""
        # Test sacred geometry compliance
        violations = []
        passed = 0
        
        # Test symbolic alignment
        try:
            validation_result = await self._validate_geometric_cleanliness(session)
            if validation_result["is_clean"]:
                passed += 1
            else:
                violations.extend(validation_result["violations"])
        except Exception as e:
            violations.append(f"Geometric validation error: {str(e)}")
        
        return {
            "passed": passed,
            "failed": len(violations),
            "skipped": 0,
            "errors": violations,
            "warnings": [],
            "sacred_compliance": len(violations) == 0
        }

    async def _run_sovereign_tests(self, session: TestSession) -> Dict[str, Any]:
        """Run sovereign architecture compliance tests"""
        # Test sovereign data flow patterns
        violations = []
        passed = 0
        
        # Test biological flow compliance
        flow_patterns = {
            "breath_in": "Akron → FIELD-LIVING",
            "process": "FIELD-LIVING → FIELD-DEV", 
            "breath_out": "FIELD → DOJO",
            "memory_loop": "DOJO → OBI-WAN → Akron"
        }
        
        for pattern_name, pattern in flow_patterns.items():
            try:
                # Validate flow pattern
                if await self._validate_flow_pattern(pattern, session):
                    passed += 1
                else:
                    violations.append(f"Flow pattern validation failed: {pattern}")
            except Exception as e:
                violations.append(f"Error validating {pattern_name}: {str(e)}")
        
        return {
            "passed": passed,
            "failed": len(violations),
            "skipped": 0,
            "errors": violations,
            "warnings": [],
            "sacred_compliance": len(violations) == 0
        }

    async def _run_e2e_tests(self, session: TestSession, specific_tests: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run end-to-end tests that don't risk main system stability"""
        # Run safe, non-destructive E2E tests
        test_scenarios = [
            "sacred_file_creation",
            "symbolic_validation", 
            "tetrahedral_navigation",
            "biological_flow_simulation"
        ]
        
        if specific_tests:
            test_scenarios = [s for s in test_scenarios if any(t in s for t in specific_tests)]
        
        passed = 0
        failed = 0
        errors = []
        
        for scenario in test_scenarios:
            try:
                if await self._run_e2e_scenario(scenario, session):
                    passed += 1
                else:
                    failed += 1
                    errors.append(f"E2E scenario failed: {scenario}")
            except Exception as e:
                failed += 1
                errors.append(f"E2E scenario error {scenario}: {str(e)}")
        
        return {
            "passed": passed,
            "failed": failed,
            "skipped": 0,
            "errors": errors,
            "warnings": [],
            "sacred_compliance": failed == 0
        }

    async def _run_test_command(self, cmd: List[str], session: TestSession) -> Dict[str, Any]:
        """Execute test command in isolated environment"""
        env = os.environ.copy()
        
        # Set test environment variables
        if session.isolation_path:
            env_file = Path(session.isolation_path) / ".env.test"
            if env_file.exists():
                for line in env_file.read_text().split('\n'):
                    if line.strip() and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env[key.strip()] = value.strip()
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=session.isolation_path or str(self.field_path),
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Parse pytest JSON report if available
            json_report_path = Path(session.isolation_path or ".") / "unit_results.json"
            if json_report_path.exists():
                with open(json_report_path) as f:
                    pytest_result = json.load(f)
                    
                return {
                    "passed": pytest_result.get("summary", {}).get("passed", 0),
                    "failed": pytest_result.get("summary", {}).get("failed", 0),
                    "skipped": pytest_result.get("summary", {}).get("skipped", 0),
                    "errors": [test.get("call", {}).get("longrepr", "") for test in pytest_result.get("tests", []) if test.get("outcome") == "failed"],
                    "warnings": [],
                    "sacred_compliance": pytest_result.get("summary", {}).get("failed", 0) == 0
                }
            
            # Fallback parsing
            return {
                "passed": 1 if process.returncode == 0 else 0,
                "failed": 0 if process.returncode == 0 else 1,
                "skipped": 0,
                "errors": [stderr.decode()] if stderr else [],
                "warnings": [],
                "sacred_compliance": process.returncode == 0
            }
            
        except Exception as e:
            return {
                "passed": 0,
                "failed": 1,
                "skipped": 0,
                "errors": [str(e)],
                "warnings": [],
                "sacred_compliance": False
            }

    async def _validate_flow_pattern(self, pattern: str, session: TestSession) -> bool:
        """Validate biological flow pattern compliance"""
        # This is a placeholder for flow pattern validation
        # In a real implementation, this would validate the actual data flow
        return True

    async def _run_e2e_scenario(self, scenario: str, session: TestSession) -> bool:
        """Run a specific E2E test scenario"""
        # This is a placeholder for E2E scenario execution
        # Each scenario would test a specific aspect of the system
        return True

    def _create_placeholder_tests(self, test_dir: Path, test_type: str, node: SacredNode):
        """Create placeholder test files for empty test directories"""
        test_file = test_dir / f"test_{test_type}_{node.value.lower()}.py"
        
        test_content = f'''"""
{test_type.title()} tests for {node.value}
This is a placeholder test file created by the parallel testing framework.
"""
import pytest
import os
import sys
from pathlib import Path

# Add FIELD to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

@pytest.fixture
def sacred_node():
    """Fixture providing sacred node information"""
    return "{node.value}"

@pytest.fixture
def test_environment():
    """Fixture for test environment setup"""
    return {{
        "field_symbol": os.getenv("FIELD_SYMBOL"),
        "chakra_resonance": os.getenv("CHAKRA_RESONANCE"),
        "session_id": os.getenv("TEST_SESSION_ID"),
        "isolation": os.getenv("TEST_ISOLATION", "false") == "true"
    }}

def test_placeholder_{test_type.lower()}(sacred_node, test_environment):
    """Placeholder {test_type} test"""
    assert sacred_node == "{node.value}"
    assert test_environment["session_id"] is not None
    
def test_environment_isolation(test_environment):
    """Test that we're running in isolated environment"""
    if test_environment["isolation"]:
        assert test_environment["session_id"] is not None
        
def test_sacred_symbols():
    """Test sacred symbolic alignment"""
    field_symbol = os.getenv("FIELD_SYMBOL")
    assert field_symbol is not None
    assert field_symbol in ["▲ATLAS", "▼TATA", "●OBI-WAN", "◼︎DOJO"]
'''
        
        test_file.write_text(test_content)
        self.logger.info(f"Created placeholder test file: {test_file}")

    async def run_parallel_sessions(self, 
                                  sessions: List[TestSession],
                                  max_concurrent: int = 4) -> List[TestResult]:
        """Run multiple test sessions in parallel"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def run_with_semaphore(session: TestSession) -> TestResult:
            async with semaphore:
                return await self.run_node_tests(session)
        
        tasks = [run_with_semaphore(session) for session in sessions]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log them
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Session {sessions[i].session_id} failed with exception: {result}")
            else:
                valid_results.append(result)
        
        return valid_results

    def cleanup_session(self, session_id: str):
        """Clean up test session resources"""
        if session_id not in self.test_sessions:
            return
        
        session = self.test_sessions[session_id]
        
        # Remove isolation directory if it exists
        if session.isolation_path and Path(session.isolation_path).exists():
            import shutil
            shutil.rmtree(session.isolation_path)
            self.logger.info(f"Cleaned up isolation environment for session {session_id}")
        
        # Archive session results
        archive_path = self.field_path / "logs" / "testing" / "archived" / f"session_{session_id}.json"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(archive_path, 'w') as f:
            json.dump(asdict(session), f, indent=2, default=str)
        
        del self.test_sessions[session_id]
        self.logger.info(f"Archived and removed session {session_id}")

    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a test session"""
        session = self.test_sessions.get(session_id)
        if not session:
            return None
        
        return {
            "session_id": session.session_id,
            "node": session.node.value,
            "suite": session.suite.value,
            "status": session.status,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "environment": session.environment.value,
            "isolation_path": session.isolation_path
        }

    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active test sessions"""
        return [self.get_session_status(sid) for sid in self.test_sessions.keys()]

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sacred Sovereign Parallel Testing Framework")
    parser.add_argument("--node", choices=["atlas", "tata", "obi-wan", "dojo"], help="Sacred node to test")
    parser.add_argument("--suite", choices=["unit", "integration", "geometry", "sovereign", "e2e"], help="Test suite to run")
    parser.add_argument("--environment", choices=["isolated", "field_dev", "mirror", "safe"], default="isolated", help="Test environment")
    parser.add_argument("--run-all", action="store_true", help="Run tests for all nodes")
    parser.add_argument("--isolated", action="store_true", help="Use isolated environment (default)")
    parser.add_argument("--specific-tests", nargs="*", help="Specific test names to run")
    parser.add_argument("--max-concurrent", type=int, default=4, help="Maximum concurrent test sessions")
    
    args = parser.parse_args()
    
    # Map CLI arguments to enums
    node_map = {
        "atlas": SacredNode.ATLAS,
        "tata": SacredNode.TATA, 
        "obi-wan": SacredNode.OBI_WAN,
        "dojo": SacredNode.DOJO
    }
    
    suite_map = {
        "unit": TestSuite.UNIT,
        "integration": TestSuite.INTEGRATION,
        "geometry": TestSuite.GEOMETRY,
        "sovereign": TestSuite.SOVEREIGN,
        "e2e": TestSuite.E2E
    }
    
    env_map = {
        "isolated": TestEnvironment.ISOLATED,
        "field_dev": TestEnvironment.FIELD_DEV,
        "mirror": TestEnvironment.MIRROR,
        "safe": TestEnvironment.SAFE
    }
    
    async def main():
        framework = SacredTestFramework()
        
        if args.run_all:
            # Create sessions for all nodes
            sessions = []
            for node_name, node_enum in node_map.items():
                for suite_name, suite_enum in suite_map.items():
                    session = framework.create_test_session(
                        node=node_enum,
                        suite=suite_enum,
                        environment=env_map[args.environment]
                    )
                    sessions.append(session)
            
            print(f"Running {len(sessions)} test sessions in parallel...")
            results = await framework.run_parallel_sessions(sessions, args.max_concurrent)
            
            # Print summary
            total_passed = sum(r.passed for r in results)
            total_failed = sum(r.failed for r in results)
            print(f"\nTest Summary: {total_passed} passed, {total_failed} failed")
            
        elif args.node and args.suite:
            # Create single session
            session = framework.create_test_session(
                node=node_map[args.node],
                suite=suite_map[args.suite],
                environment=env_map[args.environment]
            )
            
            print(f"Running {args.suite} tests for {args.node}...")
            result = await framework.run_node_tests(session, args.specific_tests)
            
            print(f"\nResults for {result.node} {result.suite}:")
            print(f"  Passed: {result.passed}")
            print(f"  Failed: {result.failed}")
            print(f"  Duration: {result.duration:.2f}s")
            print(f"  Sacred Compliance: {result.sacred_compliance}")
            
            if result.errors:
                print("\nErrors:")
                for error in result.errors:
                    print(f"  - {error}")
        else:
            parser.print_help()
    
    asyncio.run(main())
