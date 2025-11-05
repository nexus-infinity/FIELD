#!/usr/bin/env python3
"""
Sacred Parallel Testing Manager

Orchestrates and manages parallel testing infrastructure for the sacred sovereign system.
Enables multiple developer/AI agent sessions with independent validation and testing
without risking main system stability.

Usage:
    python testing/test_manager.py --status
    python testing/test_manager.py --launch session_id --node atlas --suite unit
    python testing/test_manager.py --launch-multiple --nodes atlas,tata --isolated
    python testing/test_manager.py --run-e2e biological_flow --safety isolated
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import subprocess
import uuid
import threading
import signal
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Sacred Sovereign imports
sys.path.append(str(Path(__file__).parent.parent))
from testing.parallel_test_framework import (
    SacredTestFramework, SacredNode, TestSuite, TestEnvironment, TestSession
)
from testing.e2e_test_system import E2ETestSystem, E2EScenario, SafetyLevel
from cli.sacred_cli import SacredCLI

@dataclass
class ActiveSession:
    """Represents an active testing session"""
    session_id: str
    session_type: str  # 'test', 'cli', 'e2e'
    node: Optional[str]
    suite: Optional[str]
    status: str
    start_time: datetime
    process_id: Optional[int] = None
    isolation_path: Optional[str] = None
    environment: str = "isolated"

class TestingManager:
    """Central manager for parallel testing infrastructure"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.testing_path = self.base_path / "testing"
        self.cli_path = self.base_path / "cli"
        
        # Create directories
        self.testing_path.mkdir(exist_ok=True)
        self.cli_path.mkdir(exist_ok=True)
        
        # Session tracking
        self.active_sessions = {}
        self.session_history = []
        
        # Testing infrastructure
        self.test_framework = SacredTestFramework()
        self.cli_system = SacredCLI()
        
        # Setup logging
        self.setup_logging()
        
        # Load existing sessions
        self._load_session_state()
        
        # Setup cleanup handlers
        signal.signal(signal.SIGINT, self._cleanup_handler)
        signal.signal(signal.SIGTERM, self._cleanup_handler)
        
    def setup_logging(self):
        """Setup test manager logging"""
        log_dir = self.testing_path / "logs" / "manager"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - TestManager - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_session_state(self):
        """Load existing session state from disk"""
        state_file = self.testing_path / "session_state.json"
        if state_file.exists():
            try:
                with open(state_file) as f:
                    state = json.load(f)
                    
                # Restore active sessions (check if still running)
                for session_data in state.get('active_sessions', []):
                    session = ActiveSession(**session_data)
                    
                    # Check if process is still running
                    if self._is_process_running(session.process_id):
                        self.active_sessions[session.session_id] = session
                    else:
                        # Mark as completed
                        session.status = 'completed'
                        self.session_history.append(session)
                        
                self.logger.info(f"Loaded {len(self.active_sessions)} active sessions")
                
            except Exception as e:
                self.logger.error(f"Failed to load session state: {str(e)}")
                
    def _save_session_state(self):
        """Save current session state to disk"""
        state_file = self.testing_path / "session_state.json"
        
        try:
            state = {
                'active_sessions': [asdict(session) for session in self.active_sessions.values()],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Failed to save session state: {str(e)}")

    def _is_process_running(self, pid: Optional[int]) -> bool:
        """Check if a process is still running"""
        if not pid:
            return False
            
        try:
            os.kill(pid, 0)
            return True
        except (OSError, TypeError):
            return False

    async def launch_test_session(self, 
                                node: str,
                                suite: str, 
                                environment: str = "isolated",
                                specific_tests: Optional[List[str]] = None,
                                session_id: Optional[str] = None) -> str:
        """Launch a new parallel test session"""
        
        if not session_id:
            session_id = f"test_{node}_{suite}_{datetime.now().strftime('%H%M%S')}"
        
        # Map string inputs to enums
        node_map = {
            'atlas': SacredNode.ATLAS,
            'tata': SacredNode.TATA,
            'obiwan': SacredNode.OBI_WAN,
            'dojo': SacredNode.DOJO
        }
        
        suite_map = {
            'unit': TestSuite.UNIT,
            'integration': TestSuite.INTEGRATION,
            'geometry': TestSuite.GEOMETRY,
            'sovereign': TestSuite.SOVEREIGN,
            'e2e': TestSuite.E2E
        }
        
        env_map = {
            'isolated': TestEnvironment.ISOLATED,
            'field_dev': TestEnvironment.FIELD_DEV,
            'mirror': TestEnvironment.MIRROR,
            'safe': TestEnvironment.SAFE
        }
        
        try:
            # Create test session
            test_session = self.test_framework.create_test_session(
                node=node_map[node],
                suite=suite_map[suite],
                environment=env_map[environment]
            )
            
            # Track active session
            active_session = ActiveSession(
                session_id=session_id,
                session_type='test',
                node=node,
                suite=suite,
                status='launching',
                start_time=datetime.now(),
                isolation_path=test_session.isolation_path,
                environment=environment
            )
            
            self.active_sessions[session_id] = active_session
            self.logger.info(f"Launching test session {session_id}: {node} {suite}")
            
            # Run test in background
            async def run_test():
                try:
                    active_session.status = 'running'
                    result = await self.test_framework.run_node_tests(test_session, specific_tests)
                    
                    active_session.status = 'completed'
                    self.logger.info(f"Test session {session_id} completed: {'PASS' if result.passed else 'FAIL'}")
                    
                    # Move to history
                    self.session_history.append(active_session)
                    del self.active_sessions[session_id]
                    
                    self._save_session_state()
                    return result
                    
                except Exception as e:
                    active_session.status = 'failed'
                    self.logger.error(f"Test session {session_id} failed: {str(e)}")
                    
                    # Move to history
                    self.session_history.append(active_session)
                    del self.active_sessions[session_id]
                    
                    self._save_session_state()
                    
            # Start background task
            asyncio.create_task(run_test())
            self._save_session_state()
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to launch test session: {str(e)}")
            raise

    async def launch_multiple_sessions(self,
                                     nodes: List[str],
                                     suites: List[str] = None,
                                     environment: str = "isolated",
                                     max_concurrent: int = 4) -> List[str]:
        """Launch multiple test sessions in parallel"""
        
        if not suites:
            suites = ['unit', 'integration', 'geometry']
            
        session_ids = []
        tasks = []
        
        for node in nodes:
            for suite in suites:
                session_id = f"multi_{node}_{suite}_{datetime.now().strftime('%H%M%S')}"
                
                task = self.launch_test_session(
                    node=node,
                    suite=suite,
                    environment=environment,
                    session_id=session_id
                )
                tasks.append(task)
                session_ids.append(session_id)
                
                # Limit concurrent launches
                if len(tasks) >= max_concurrent:
                    launched = await asyncio.gather(*tasks, return_exceptions=True)
                    tasks = []
        
        # Launch remaining tasks
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
        self.logger.info(f"Launched {len(session_ids)} test sessions")
        return session_ids

    async def launch_cli_session(self,
                                node: str,
                                command: str,
                                args: List[str] = None,
                                session_id: Optional[str] = None) -> str:
        """Launch CLI session"""
        
        if not session_id:
            session_id = f"cli_{node}_{datetime.now().strftime('%H%M%S')}"
        
        if not args:
            args = []
            
        try:
            # Create isolation environment
            isolation_path = self.cli_system.create_isolation_env(node, session_id)
            
            # Track active session
            active_session = ActiveSession(
                session_id=session_id,
                session_type='cli',
                node=node,
                suite=command,
                status='running',
                start_time=datetime.now(),
                isolation_path=isolation_path,
                environment='isolated'
            )
            
            self.active_sessions[session_id] = active_session
            
            # Build CLI command
            cli_cmd = ['python', str(self.cli_path / 'sacred_cli.py'), node, command] + args
            cli_cmd.extend(['--isolated', '--session-id', session_id])
            
            # Execute CLI command
            process = subprocess.Popen(
                cli_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.base_path)
            )
            
            active_session.process_id = process.pid
            self.logger.info(f"Launched CLI session {session_id}: {node} {command}")
            
            self._save_session_state()
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to launch CLI session: {str(e)}")
            raise

    async def launch_e2e_session(self,
                               scenario: str,
                               safety_level: str = "isolated",
                               session_id: Optional[str] = None) -> str:
        """Launch E2E test session"""
        
        if not session_id:
            session_id = f"e2e_{scenario}_{datetime.now().strftime('%H%M%S')}"
        
        # Map safety level
        safety_map = {s.value: s for s in SafetyLevel}
        safety = safety_map[safety_level]
        
        try:
            # Create E2E system
            e2e_system = E2ETestSystem(safety)
            
            # Track active session
            active_session = ActiveSession(
                session_id=session_id,
                session_type='e2e',
                node=None,
                suite=scenario,
                status='launching',
                start_time=datetime.now(),
                isolation_path=str(e2e_system.test_env_path),
                environment=safety_level
            )
            
            self.active_sessions[session_id] = active_session
            self.logger.info(f"Launching E2E session {session_id}: {scenario}")
            
            # Run E2E in background
            async def run_e2e():
                try:
                    active_session.status = 'running'
                    
                    # Map scenario to method
                    scenario_map = {
                        'biological_flow': e2e_system.run_biological_flow_scenario,
                        'tetrahedral_navigation': e2e_system.run_tetrahedral_navigation_scenario,
                        'sacred_file_creation': e2e_system.run_sacred_file_creation_scenario,
                        'symbolic_validation': e2e_system.run_symbolic_validation_scenario,
                        'geometric_cleanliness': e2e_system.run_geometric_cleanliness_scenario
                    }
                    
                    if scenario in scenario_map:
                        result = await scenario_map[scenario]()
                    else:
                        # Run all scenarios
                        results = await e2e_system.run_all_scenarios()
                        result = results[0] if results else None
                    
                    active_session.status = 'completed'
                    self.logger.info(f"E2E session {session_id} completed: {'PASS' if result.passed else 'FAIL'}")
                    
                    # Move to history
                    self.session_history.append(active_session)
                    del self.active_sessions[session_id]
                    
                    e2e_system.cleanup()
                    self._save_session_state()
                    return result
                    
                except Exception as e:
                    active_session.status = 'failed'
                    self.logger.error(f"E2E session {session_id} failed: {str(e)}")
                    
                    # Move to history
                    self.session_history.append(active_session)
                    del self.active_sessions[session_id]
                    
                    e2e_system.cleanup()
                    self._save_session_state()
            
            # Start background task
            asyncio.create_task(run_e2e())
            self._save_session_state()
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to launch E2E session: {str(e)}")
            raise

    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific session"""
        session = self.active_sessions.get(session_id)
        if not session:
            # Check history
            for hist_session in self.session_history:
                if hist_session.session_id == session_id:
                    session = hist_session
                    break
        
        if not session:
            return None
        
        return {
            'session_id': session.session_id,
            'session_type': session.session_type,
            'node': session.node,
            'suite': session.suite,
            'status': session.status,
            'start_time': session.start_time.isoformat(),
            'environment': session.environment,
            'isolation_path': session.isolation_path,
            'process_id': session.process_id,
            'duration': (datetime.now() - session.start_time).total_seconds() if session.status in ['running', 'launching'] else None
        }

    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions"""
        sessions = []
        
        for session in self.active_sessions.values():
            # Check if still active
            if session.process_id and not self._is_process_running(session.process_id):
                session.status = 'completed'
                self.session_history.append(session)
                continue
                
            sessions.append({
                'session_id': session.session_id,
                'session_type': session.session_type,
                'node': session.node,
                'suite': session.suite,
                'status': session.status,
                'start_time': session.start_time.isoformat(),
                'environment': session.environment,
                'duration': (datetime.now() - session.start_time).total_seconds()
            })
        
        # Remove completed sessions from active
        for session in list(self.active_sessions.values()):
            if session.status == 'completed':
                del self.active_sessions[session.session_id]
        
        self._save_session_state()
        return sessions

    def list_session_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List recent session history"""
        history = sorted(self.session_history, key=lambda x: x.start_time, reverse=True)[:limit]
        
        return [{
            'session_id': session.session_id,
            'session_type': session.session_type,
            'node': session.node,
            'suite': session.suite,
            'status': session.status,
            'start_time': session.start_time.isoformat(),
            'environment': session.environment
        } for session in history]

    def terminate_session(self, session_id: str) -> bool:
        """Terminate an active session"""
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        try:
            if session.process_id and self._is_process_running(session.process_id):
                os.kill(session.process_id, signal.SIGTERM)
                time.sleep(1)  # Give it a moment
                
                if self._is_process_running(session.process_id):
                    os.kill(session.process_id, signal.SIGKILL)
            
            session.status = 'terminated'
            self.session_history.append(session)
            del self.active_sessions[session_id]
            
            self.logger.info(f"Terminated session {session_id}")
            self._save_session_state()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to terminate session {session_id}: {str(e)}")
            return False

    def cleanup_session(self, session_id: str) -> bool:
        """Clean up session resources"""
        # Check active sessions first
        session = self.active_sessions.get(session_id)
        if not session:
            # Check history
            for hist_session in self.session_history:
                if hist_session.session_id == session_id:
                    session = hist_session
                    break
        
        if not session:
            return False
        
        try:
            # Clean up isolation directory
            if session.isolation_path and Path(session.isolation_path).exists():
                import shutil
                shutil.rmtree(session.isolation_path)
                self.logger.info(f"Cleaned up isolation path for {session_id}")
            
            # Remove from history
            self.session_history = [s for s in self.session_history if s.session_id != session_id]
            
            # Remove from active if present
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            
            self._save_session_state()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup session {session_id}: {str(e)}")
            return False

    def generate_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        active_sessions = self.list_active_sessions()
        recent_history = self.list_session_history(50)
        
        # Statistics
        total_active = len(active_sessions)
        by_type = {}
        by_status = {}
        by_node = {}
        
        for session in active_sessions:
            by_type[session['session_type']] = by_type.get(session['session_type'], 0) + 1
            by_status[session['status']] = by_status.get(session['status'], 0) + 1
            if session['node']:
                by_node[session['node']] = by_node.get(session['node'], 0) + 1
        
        # Recent activity
        recent_completed = len([s for s in recent_history if s['status'] in ['completed', 'failed']])
        success_rate = 0
        if recent_completed > 0:
            success_count = len([s for s in recent_history if s['status'] == 'completed'])
            success_rate = success_count / recent_completed
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system_status': 'operational',
            'active_sessions': {
                'total': total_active,
                'by_type': by_type,
                'by_status': by_status,
                'by_node': by_node
            },
            'recent_activity': {
                'total_sessions': len(recent_history),
                'completed_sessions': recent_completed,
                'success_rate': success_rate
            },
            'sessions': {
                'active': active_sessions,
                'recent_history': recent_history[:10]
            },
            'infrastructure': {
                'test_framework_available': True,
                'cli_system_available': True,
                'e2e_system_available': True,
                'isolation_supported': True
            }
        }

    def _cleanup_handler(self, signum, frame):
        """Handle cleanup on shutdown"""
        self.logger.info("Shutting down test manager...")
        
        # Terminate active sessions
        for session_id in list(self.active_sessions.keys()):
            self.terminate_session(session_id)
        
        self._save_session_state()
        self.logger.info("Test manager shutdown complete")

async def main():
    """Main test manager execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sacred Parallel Testing Manager")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--launch", help="Launch single test session")
    parser.add_argument("--launch-multiple", action="store_true", help="Launch multiple sessions")
    parser.add_argument("--launch-cli", help="Launch CLI session")
    parser.add_argument("--launch-e2e", help="Launch E2E session")
    parser.add_argument("--node", help="Sacred node for session")
    parser.add_argument("--nodes", help="Comma-separated nodes for multiple sessions")
    parser.add_argument("--suite", help="Test suite to run")
    parser.add_argument("--suites", help="Comma-separated test suites")
    parser.add_argument("--scenario", help="E2E scenario to run")
    parser.add_argument("--environment", default="isolated", help="Test environment")
    parser.add_argument("--safety", default="isolated", help="E2E safety level")
    parser.add_argument("--session-id", help="Custom session ID")
    parser.add_argument("--terminate", help="Terminate session by ID")
    parser.add_argument("--cleanup", help="Cleanup session by ID")
    parser.add_argument("--list-active", action="store_true", help="List active sessions")
    parser.add_argument("--list-history", action="store_true", help="List session history")
    parser.add_argument("--report", help="Generate status report to file")
    
    args = parser.parse_args()
    
    # Create test manager
    manager = TestingManager()
    
    try:
        if args.status:
            report = manager.generate_status_report()
            print(f"Sacred Testing Manager Status:")
            print(f"  Active Sessions: {report['active_sessions']['total']}")
            print(f"  System Status: {report['system_status']}")
            
            if report['active_sessions']['total'] > 0:
                print(f"  By Type: {report['active_sessions']['by_type']}")
                print(f"  By Status: {report['active_sessions']['by_status']}")
                print(f"  By Node: {report['active_sessions']['by_node']}")
            
            print(f"  Recent Success Rate: {report['recent_activity']['success_rate']:.1%}")
            
        elif args.launch:
            if not args.node or not args.suite:
                print("Error: --node and --suite required for single session launch")
                return
            
            session_id = await manager.launch_test_session(
                node=args.node,
                suite=args.suite,
                environment=args.environment,
                session_id=args.session_id
            )
            print(f"Launched test session: {session_id}")
            
        elif args.launch_multiple:
            if not args.nodes:
                print("Error: --nodes required for multiple session launch")
                return
            
            nodes = args.nodes.split(',')
            suites = args.suites.split(',') if args.suites else None
            
            session_ids = await manager.launch_multiple_sessions(
                nodes=nodes,
                suites=suites,
                environment=args.environment
            )
            print(f"Launched {len(session_ids)} test sessions:")
            for sid in session_ids:
                print(f"  - {sid}")
                
        elif args.launch_cli:
            if not args.node:
                print("Error: --node required for CLI session launch")
                return
            
            session_id = await manager.launch_cli_session(
                node=args.node,
                command=args.launch_cli,
                session_id=args.session_id
            )
            print(f"Launched CLI session: {session_id}")
            
        elif args.launch_e2e:
            session_id = await manager.launch_e2e_session(
                scenario=args.launch_e2e,
                safety_level=args.safety,
                session_id=args.session_id
            )
            print(f"Launched E2E session: {session_id}")
            
        elif args.terminate:
            if manager.terminate_session(args.terminate):
                print(f"Terminated session: {args.terminate}")
            else:
                print(f"Failed to terminate session: {args.terminate}")
                
        elif args.cleanup:
            if manager.cleanup_session(args.cleanup):
                print(f"Cleaned up session: {args.cleanup}")
            else:
                print(f"Failed to cleanup session: {args.cleanup}")
                
        elif args.list_active:
            sessions = manager.list_active_sessions()
            if sessions:
                print(f"Active Sessions ({len(sessions)}):")
                for session in sessions:
                    duration = f"{session['duration']:.1f}s"
                    print(f"  {session['session_id']}: {session['session_type']} {session['node'] or ''} {session['suite'] or ''} - {session['status']} ({duration})")
            else:
                print("No active sessions")
                
        elif args.list_history:
            history = manager.list_session_history()
            if history:
                print(f"Recent Sessions ({len(history)}):")
                for session in history:
                    print(f"  {session['session_id']}: {session['session_type']} {session['node'] or ''} {session['suite'] or ''} - {session['status']}")
            else:
                print("No session history")
                
        else:
            # Default to status
            report = manager.generate_status_report()
            
            print("Sacred Parallel Testing Manager")
            print("=" * 40)
            print(f"Status: {report['system_status']}")
            print(f"Active Sessions: {report['active_sessions']['total']}")
            
            if report['active_sessions']['total'] > 0:
                active = report['sessions']['active']
                for session in active:
                    status_icon = {"running": "🟢", "launching": "🟡", "failed": "🔴"}.get(session['status'], "⚪")
                    print(f"  {status_icon} {session['session_id']}: {session['session_type']} - {session['status']}")
            
            if args.report:
                with open(args.report, 'w') as f:
                    json.dump(report, f, indent=2)
                print(f"Status report saved to: {args.report}")
                
    except KeyboardInterrupt:
        print("\nShutdown requested...")
    except Exception as e:
        print(f"Error: {str(e)}")
        manager.logger.error(f"Manager error: {str(e)}")
    
if __name__ == "__main__":
    asyncio.run(main())
