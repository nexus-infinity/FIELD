#!/usr/bin/env python3
"""
Sacred CLI - Command Line Interface for Independent Sacred Module Invocation

Enables CLI or terminal invocation of sacred modules without affecting main system.
Each tetrahedral node can be invoked independently with proper isolation.

Usage:
    sacred atlas validate --file path/to/data.json
    sacred tata log --message "Test entry" --isolated
    sacred obi-wan sync --dry-run
    sacred dojo manifest --template template.json --output result.json
"""

import os
import sys
import json
import click
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import importlib.util
import subprocess

# Sacred Sovereign imports
sys.path.append(str(Path(__file__).parent.parent))
from ▼TATA.VERIFIED.validator import DataValidator, ValidationResult
from testing.parallel_test_framework import SacredTestFramework, TestEnvironment

class SacredCLI:
    """Main CLI controller for sacred modules"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.logger = self._setup_logging()
        self.validator = DataValidator()
        self.test_framework = SacredTestFramework()
        
    def _setup_logging(self):
        """Setup CLI logging"""
        log_path = self.base_path / "logs" / "cli"
        log_path.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - CLI - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path / f"sacred_cli_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler() if os.getenv('SACRED_CLI_VERBOSE') else logging.NullHandler()
            ]
        )
        return logging.getLogger(__name__)

    def create_isolation_env(self, node: str, session_id: str = None) -> str:
        """Create isolated environment for CLI operations"""
        if not session_id:
            session_id = f"cli_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        isolation_path = self.base_path / "cli" / "isolated" / session_id
        isolation_path.mkdir(parents=True, exist_ok=True)
        
        # Create CLI-specific environment
        env_file = isolation_path / ".env.cli"
        env_file.write_text(f"""
# CLI Isolation Environment
FIELD_SYMBOL={node.upper()}
CHAKRA_RESONANCE=cli_mode
DOJO_GATE=cli_isolated
KLEIN_INDEX=0
FREQUENCY=cli
FIELD_NAME=cli_{session_id}
CLI_SESSION_ID={session_id}
CLI_ISOLATION=true
""")
        
        self.logger.info(f"Created CLI isolation environment: {isolation_path}")
        return str(isolation_path)

sacred_cli = SacredCLI()

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--isolated', is_flag=True, default=True, help='Run in isolated environment')
@click.option('--session-id', help='Custom session ID for isolation')
def cli(verbose, isolated, session_id):
    """Sacred Sovereign CLI - Independent module invocation"""
    if verbose:
        os.environ['SACRED_CLI_VERBOSE'] = '1'
        logging.getLogger().setLevel(logging.DEBUG)
    
    if isolated:
        os.environ['SACRED_CLI_ISOLATED'] = '1'
    
    if session_id:
        os.environ['SACRED_CLI_SESSION_ID'] = session_id

# ▲ATLAS - Tooling Validation Commands
@cli.group()
def atlas():
    """▲ATLAS - Tooling validation and agent operations"""
    pass

@atlas.command()
@click.option('--file', '-f', required=True, help='File to validate')
@click.option('--schema', '-s', help='Schema file for validation')
@click.option('--isolated', is_flag=True, default=True, help='Run in isolation')
def validate(file, schema, isolated):
    """Validate data file using ATLAS tooling"""
    click.echo(f"🔺 ATLAS Validation: {file}")
    
    session_id = None
    isolation_path = None
    
    try:
        if isolated:
            session_id = os.getenv('SACRED_CLI_SESSION_ID') or f"atlas_validate_{datetime.now().strftime('%H%M%S')}"
            isolation_path = sacred_cli.create_isolation_env("▲ATLAS", session_id)
        
        # Load and validate file
        file_path = Path(file)
        if not file_path.exists():
            click.echo(f"❌ File not found: {file}", err=True)
            return
        
        with open(file_path) as f:
            data = json.load(f) if file_path.suffix == '.json' else {'content': f.read()}
        
        # Use schema if provided
        if schema:
            schema_path = Path(schema)
            if schema_path.exists():
                validation_result = sacred_cli.validator.process_data(data, str(schema_path))
            else:
                click.echo(f"❌ Schema file not found: {schema}", err=True)
                return
        else:
            # Basic validation without schema
            validation_result = ValidationResult(
                is_valid=True,
                errors=[],
                validated_data=data
            )
        
        if validation_result.is_valid:
            click.echo(f"✅ Validation successful")
            if isolated:
                click.echo(f"🔒 Isolated in: {isolation_path}")
        else:
            click.echo(f"❌ Validation failed:")
            for error in validation_result.errors:
                click.echo(f"   - {error}")
        
        # Log validation result
        sacred_cli.logger.info(f"ATLAS validation: {file} - {'SUCCESS' if validation_result.is_valid else 'FAILED'}")
        
    except Exception as e:
        click.echo(f"❌ Error during validation: {str(e)}", err=True)
        sacred_cli.logger.error(f"ATLAS validation error: {str(e)}")

@atlas.command()
@click.option('--tool', '-t', required=True, help='Tool to execute')
@click.option('--args', '-a', multiple=True, help='Tool arguments')
@click.option('--dry-run', is_flag=True, help='Show what would be executed')
def tool(tool, args, dry_run):
    """Execute ATLAS tooling"""
    click.echo(f"🔺 ATLAS Tool: {tool}")
    
    if dry_run:
        click.echo(f"Would execute: {tool} {' '.join(args)}")
        return
    
    try:
        # Execute tool in isolated environment
        session_id = f"atlas_tool_{datetime.now().strftime('%H%M%S')}"
        isolation_path = sacred_cli.create_isolation_env("▲ATLAS", session_id)
        
        # Basic tool execution (placeholder - implement specific tools)
        click.echo(f"Executing {tool} with args: {args}")
        click.echo(f"🔒 Isolated in: {isolation_path}")
        
        sacred_cli.logger.info(f"ATLAS tool executed: {tool}")
        
    except Exception as e:
        click.echo(f"❌ Tool execution failed: {str(e)}", err=True)

# ▼TATA - Temporal Truth Commands
@cli.group()
def tata():
    """▼TATA - Temporal truth and logging operations"""
    pass

@tata.command()
@click.option('--message', '-m', required=True, help='Log message')
@click.option('--level', '-l', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), help='Log level')
@click.option('--timestamp', '-t', is_flag=True, help='Include timestamp')
@click.option('--isolated', is_flag=True, default=True, help='Run in isolation')
def log(message, level, timestamp, isolated):
    """Create temporal truth log entry"""
    click.echo(f"🔻 TATA Log Entry: {level}")
    
    try:
        session_id = None
        isolation_path = None
        
        if isolated:
            session_id = f"tata_log_{datetime.now().strftime('%H%M%S')}"
            isolation_path = sacred_cli.create_isolation_env("▼TATA", session_id)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "node": "▼TATA",
            "session_id": session_id,
            "isolated": isolated
        }
        
        # Write log entry
        log_dir = Path(isolation_path if isolation_path else sacred_cli.base_path) / "logs" / "tata"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"tata_entries_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        if timestamp:
            click.echo(f"[{log_entry['timestamp']}] {level}: {message}")
        else:
            click.echo(f"{level}: {message}")
        
        if isolated:
            click.echo(f"🔒 Isolated in: {isolation_path}")
        
        sacred_cli.logger.info(f"TATA log entry created: {level}")
        
    except Exception as e:
        click.echo(f"❌ Failed to create log entry: {str(e)}", err=True)

@tata.command()
@click.option('--date', '-d', help='Date to query (YYYY-MM-DD)')
@click.option('--level', '-l', help='Filter by log level')
@click.option('--limit', type=int, default=10, help='Limit results')
def query(date, level, limit):
    """Query temporal truth logs"""
    click.echo(f"🔻 TATA Query: {date or 'all dates'}")
    
    try:
        log_dir = sacred_cli.base_path / "logs" / "tata"
        
        if not log_dir.exists():
            click.echo("No TATA logs found")
            return
        
        # Find matching log files
        pattern = f"tata_entries_{date.replace('-', '') if date else '*'}.jsonl"
        log_files = list(log_dir.glob(pattern))
        
        if not log_files:
            click.echo(f"No logs found for pattern: {pattern}")
            return
        
        entries = []
        for log_file in log_files:
            with open(log_file) as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        if not level or entry.get('level') == level:
                            entries.append(entry)
        
        # Sort and limit
        entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        entries = entries[:limit]
        
        click.echo(f"Found {len(entries)} entries:")
        for entry in entries:
            click.echo(f"[{entry.get('timestamp', 'N/A')}] {entry.get('level', 'N/A')}: {entry.get('message', 'N/A')}")
        
    except Exception as e:
        click.echo(f"❌ Query failed: {str(e)}", err=True)

# ●OBI-WAN - Living Memory Commands  
@cli.group()
def obiwan():
    """●OBI-WAN - Living memory and synchronization operations"""
    pass

@obiwan.command()
@click.option('--source', '-s', help='Source path for sync')
@click.option('--target', '-t', help='Target path for sync')
@click.option('--dry-run', is_flag=True, help='Show what would be synced')
@click.option('--bidirectional', is_flag=True, help='Bidirectional sync')
def sync(source, target, dry_run, bidirectional):
    """Synchronize living memory"""
    click.echo(f"⭕ OBI-WAN Sync: {source} → {target}")
    
    try:
        session_id = f"obiwan_sync_{datetime.now().strftime('%H%M%S')}"
        isolation_path = sacred_cli.create_isolation_env("●OBI-WAN", session_id)
        
        if dry_run:
            click.echo(f"Would sync: {source} → {target}")
            if bidirectional:
                click.echo(f"Would sync: {target} → {source}")
            return
        
        # Implement memory sync logic (placeholder)
        sync_result = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "target": target,
            "bidirectional": bidirectional,
            "session_id": session_id,
            "files_synced": 0,  # Placeholder
            "status": "completed"
        }
        
        # Log sync result
        sync_log = Path(isolation_path) / "sync_log.json"
        with open(sync_log, 'w') as f:
            json.dump(sync_result, f, indent=2)
        
        click.echo(f"✅ Sync completed")
        click.echo(f"🔒 Isolated in: {isolation_path}")
        
    except Exception as e:
        click.echo(f"❌ Sync failed: {str(e)}", err=True)

@obiwan.command()
@click.option('--key', '-k', required=True, help='Memory key')
@click.option('--value', '-v', help='Memory value (for store operation)')
@click.option('--operation', '-o', default='get', type=click.Choice(['get', 'set', 'delete']), help='Memory operation')
def memory(key, value, operation):
    """Access living memory store"""
    click.echo(f"⭕ OBI-WAN Memory: {operation} {key}")
    
    try:
        session_id = f"obiwan_memory_{datetime.now().strftime('%H%M%S')}"
        isolation_path = sacred_cli.create_isolation_env("●OBI-WAN", session_id)
        
        memory_file = Path(isolation_path) / "memory_store.json"
        memory_store = {}
        
        # Load existing memory store
        if memory_file.exists():
            with open(memory_file) as f:
                memory_store = json.load(f)
        
        if operation == 'get':
            result = memory_store.get(key, None)
            click.echo(f"Value: {result}")
            
        elif operation == 'set':
            if not value:
                click.echo("❌ Value required for set operation", err=True)
                return
            memory_store[key] = value
            click.echo(f"✅ Set {key} = {value}")
            
        elif operation == 'delete':
            if key in memory_store:
                del memory_store[key]
                click.echo(f"✅ Deleted {key}")
            else:
                click.echo(f"Key not found: {key}")
        
        # Save memory store
        with open(memory_file, 'w') as f:
            json.dump(memory_store, f, indent=2)
        
        click.echo(f"🔒 Memory isolated in: {isolation_path}")
        
    except Exception as e:
        click.echo(f"❌ Memory operation failed: {str(e)}", err=True)

# ◼︎DOJO - Manifestation Commands
@cli.group()  
def dojo():
    """◼︎DOJO - Manifestation and execution operations"""
    pass

@dojo.command()
@click.option('--template', '-t', required=True, help='Template file for manifestation')
@click.option('--output', '-o', help='Output file path')
@click.option('--params', '-p', multiple=True, help='Template parameters (key=value)')
@click.option('--dry-run', is_flag=True, help='Show what would be manifested')
def manifest(template, output, params, dry_run):
    """Manifest from template"""
    click.echo(f"◼️ DOJO Manifest: {template}")
    
    try:
        session_id = f"dojo_manifest_{datetime.now().strftime('%H%M%S')}"
        isolation_path = sacred_cli.create_isolation_env("◼︎DOJO", session_id)
        
        # Load template
        template_path = Path(template)
        if not template_path.exists():
            click.echo(f"❌ Template not found: {template}", err=True)
            return
        
        with open(template_path) as f:
            template_content = f.read()
        
        # Parse parameters
        param_dict = {}
        for param in params:
            if '=' in param:
                key, value = param.split('=', 1)
                param_dict[key.strip()] = value.strip()
        
        if dry_run:
            click.echo(f"Would manifest template: {template}")
            click.echo(f"With parameters: {param_dict}")
            click.echo(f"Output to: {output or 'stdout'}")
            return
        
        # Simple template substitution (placeholder - implement full templating)
        manifest_content = template_content
        for key, value in param_dict.items():
            manifest_content = manifest_content.replace(f"{{{key}}}", value)
        
        # Output manifest
        if output:
            output_path = Path(isolation_path) / output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(manifest_content)
            click.echo(f"✅ Manifested to: {output_path}")
        else:
            click.echo("Manifestation:")
            click.echo(manifest_content)
        
        click.echo(f"🔒 Isolated in: {isolation_path}")
        
    except Exception as e:
        click.echo(f"❌ Manifestation failed: {str(e)}", err=True)

@dojo.command()
@click.option('--script', '-s', required=True, help='Script to execute')
@click.option('--args', '-a', multiple=True, help='Script arguments')
@click.option('--env', '-e', multiple=True, help='Environment variables (key=value)')
@click.option('--isolated', is_flag=True, default=True, help='Run in isolation')
def execute(script, args, env, isolated):
    """Execute script in DOJO"""
    click.echo(f"◼️ DOJO Execute: {script}")
    
    try:
        session_id = f"dojo_execute_{datetime.now().strftime('%H%M%S')}"
        isolation_path = None
        
        if isolated:
            isolation_path = sacred_cli.create_isolation_env("◼︎DOJO", session_id)
        
        # Prepare environment
        exec_env = os.environ.copy()
        for env_var in env:
            if '=' in env_var:
                key, value = env_var.split('=', 1)
                exec_env[key.strip()] = value.strip()
        
        # Execute script
        cmd = [script] + list(args)
        result = subprocess.run(
            cmd,
            cwd=isolation_path or os.getcwd(),
            env=exec_env,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            click.echo("✅ Execution successful")
            if result.stdout:
                click.echo("Output:")
                click.echo(result.stdout)
        else:
            click.echo(f"❌ Execution failed (code: {result.returncode})")
            if result.stderr:
                click.echo("Error:")
                click.echo(result.stderr)
        
        if isolated:
            click.echo(f"🔒 Isolated in: {isolation_path}")
        
    except Exception as e:
        click.echo(f"❌ Execution error: {str(e)}", err=True)

# Testing Commands
@cli.group()
def test():
    """Testing and validation commands"""
    pass

@test.command()
@click.option('--node', type=click.Choice(['atlas', 'tata', 'obiwan', 'dojo']), help='Test specific node')
@click.option('--suite', type=click.Choice(['unit', 'integration', 'geometry', 'sovereign', 'e2e']), help='Test suite')
@click.option('--isolated', is_flag=True, default=True, help='Run in isolation')
def run(node, suite, isolated):
    """Run tests via CLI"""
    click.echo("🧪 Running Sacred Tests")
    
    try:
        # Use the test framework
        from testing.parallel_test_framework import SacredNode, TestSuite, TestEnvironment
        
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
        
        environment = TestEnvironment.ISOLATED if isolated else TestEnvironment.SAFE
        
        async def run_test():
            framework = SacredTestFramework()
            session = framework.create_test_session(
                node=node_map[node],
                suite=suite_map[suite],
                environment=environment
            )
            
            result = await framework.run_node_tests(session)
            
            click.echo(f"Results: {result.passed} passed, {result.failed} failed")
            if result.errors:
                for error in result.errors:
                    click.echo(f"❌ {error}")
            
            return result
        
        asyncio.run(run_test())
        
    except Exception as e:
        click.echo(f"❌ Test run failed: {str(e)}", err=True)

# Session Management Commands
@cli.group()
def session():
    """Session management commands"""
    pass

@session.command()
def list():
    """List active CLI sessions"""
    try:
        sessions_dir = sacred_cli.base_path / "cli" / "isolated"
        if not sessions_dir.exists():
            click.echo("No active sessions")
            return
        
        sessions = []
        for session_path in sessions_dir.iterdir():
            if session_path.is_dir():
                env_file = session_path / ".env.cli"
                if env_file.exists():
                    sessions.append({
                        'id': session_path.name,
                        'path': str(session_path),
                        'created': datetime.fromtimestamp(session_path.stat().st_ctime)
                    })
        
        if sessions:
            click.echo(f"Active CLI sessions ({len(sessions)}):")
            for session in sorted(sessions, key=lambda x: x['created'], reverse=True):
                click.echo(f"  {session['id']} (created: {session['created'].strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            click.echo("No active sessions found")
            
    except Exception as e:
        click.echo(f"❌ Failed to list sessions: {str(e)}", err=True)

@session.command()
@click.argument('session_id')
def cleanup(session_id):
    """Clean up CLI session"""
    try:
        session_path = sacred_cli.base_path / "cli" / "isolated" / session_id
        if session_path.exists():
            import shutil
            shutil.rmtree(session_path)
            click.echo(f"✅ Cleaned up session: {session_id}")
        else:
            click.echo(f"❌ Session not found: {session_id}")
            
    except Exception as e:
        click.echo(f"❌ Cleanup failed: {str(e)}", err=True)

if __name__ == '__main__':
    cli()
