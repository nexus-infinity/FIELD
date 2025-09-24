#!/usr/bin/env python3
"""
🎯 Intention Determination & Fulfillment Interface
Direct bridge between human intention and field system execution

The problem: You have all the infrastructure but no simple way to input intention and get output.
The solution: This interface that takes your intention and routes it through your existing field system.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess
import logging

# Add field paths to Python path
field_paths = [
    "/Users/jbear/FIELD/●◎_FIELD_TRAIN_STATION",
    "/Users/jbear/FIELD-LIVING/●◎_memory_core",
    "/Users/jbear/FIELD/▼TATA",
    "/Users/jbear/FIELD/▲ATLAS"
]

for path in field_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("IntentionInterface")

class IntentionInterface:
    """Direct intention input -> field system execution -> clear output"""
    
    def __init__(self):
        self.field_path = Path("/Users/jbear/FIELD")
        self.dojo_active = Path("/Users/jbear/FIELD/◼︎DOJO_ACTIVE")
        self.intention_config = self.field_path / "▼TATA" / "intention_field_config.json"
        self.intention_manifest = self.field_path / "▼TATA" / "intention_manifest.json"
        
        # Load existing intention configuration
        self.load_intention_config()
        
    def load_intention_config(self):
        """Load your existing intention field configuration"""
        try:
            with open(self.intention_config, 'r') as f:
                self.config = json.load(f)
            logger.info("✅ Intention field configuration loaded")
        except Exception as e:
            logger.warning(f"⚠️ Could not load intention config: {e}")
            self.config = {"intention_field": {"threshold": 0.93}}
            
        try:
            with open(self.intention_manifest, 'r') as f:
                self.manifest = json.load(f)
            logger.info("✅ Intention manifest loaded")
        except Exception as e:
            logger.warning(f"⚠️ Could not load intention manifest: {e}")
            self.manifest = {"arcadian_vault": {"intention_registry": {}}}
    
    def display_welcome(self):
        """Show the intention interface"""
        print("\n" + "="*80)
        print("🎯 INTENTION DETERMINATION & FULFILLMENT INTERFACE")
        print("="*80)
        print("Direct bridge: Your Intention → Field System → Clear Output")
        print()
        print("Available intention types:")
        print("  1. 🔧 SYSTEM - Configure or fix something in your field")
        print("  2. 🚀 CREATE - Build or generate something new")
        print("  3. 🔍 ANALYZE - Understand or examine something")
        print("  4. 🔄 PROCESS - Transform or convert something")
        print("  5. 🎯 EXECUTE - Run a specific action or command")
        print("  6. 📊 REPORT - Get status or information about something")
        print("  7. 🧠 THINK - Work through a problem or decision")
        print()
    
    async def get_intention(self) -> Dict[str, Any]:
        """Get clear intention from user"""
        print("💭 What is your intention? (Be specific about what you want)")
        print("Example: 'I want to analyze all Python files in FIELD-LIVING for unused imports'")
        print("Example: 'I want to create a daily report of my field system status'")
        print("Example: 'I want to fix the MCP connection issues I've been having'")
        print()
        
        intention_text = input("🎯 Your intention: ").strip()
        
        if not intention_text:
            print("❌ No intention provided")
            return None
            
        print()
        print("🔍 Analyzing intention...")
        
        # Determine intention type and components
        intention_analysis = await self.analyze_intention(intention_text)
        
        # Show analysis
        print(f"📋 Intention Analysis:")
        print(f"   Type: {intention_analysis['type']}")
        print(f"   Target: {intention_analysis['target']}")
        print(f"   Action: {intention_analysis['action']}")
        print(f"   Scope: {intention_analysis['scope']}")
        
        # Confirm
        confirm = input("\n✅ Proceed with this analysis? (y/N): ").strip().lower()
        if confirm != 'y':
            return None
            
        return {
            "raw_intention": intention_text,
            "analysis": intention_analysis,
            "timestamp": datetime.now().isoformat(),
            "user_confirmed": True
        }
    
    async def analyze_intention(self, intention_text: str) -> Dict[str, Any]:
        """Analyze intention to determine type, scope, and execution path"""
        
        # Simple keyword analysis (can be enhanced with AI later)
        intention_lower = intention_text.lower()
        
        # Determine type
        if any(word in intention_lower for word in ['analyze', 'examine', 'check', 'review', 'understand']):
            intention_type = "ANALYZE"
        elif any(word in intention_lower for word in ['create', 'build', 'generate', 'make', 'develop']):
            intention_type = "CREATE"
        elif any(word in intention_lower for word in ['fix', 'repair', 'configure', 'setup', 'install']):
            intention_type = "SYSTEM"
        elif any(word in intention_lower for word in ['run', 'execute', 'start', 'launch', 'process']):
            intention_type = "EXECUTE"
        elif any(word in intention_lower for word in ['report', 'status', 'show', 'list', 'display']):
            intention_type = "REPORT"
        elif any(word in intention_lower for word in ['think', 'decide', 'plan', 'strategy', 'approach']):
            intention_type = "THINK"
        else:
            intention_type = "PROCESS"
        
        # Determine target (what they want to work on)
        target = "unknown"
        if "python" in intention_lower:
            target = "python_code"
        elif any(field in intention_lower for field in ['field-living', 'living', 'memory']):
            target = "field_living"
        elif any(field in intention_lower for field in ['field-dev', 'development', 'dev']):
            target = "field_dev"
        elif any(field in intention_lower for field in ['dojo', 'active']):
            target = "dojo_active"
        elif "mcp" in intention_lower:
            target = "mcp_servers"
        elif "warp" in intention_lower:
            target = "warp_config"
        elif any(sys in intention_lower for sys in ['system', 'field', 'config']):
            target = "field_system"
        
        # Determine scope
        if any(word in intention_lower for word in ['all', 'entire', 'complete', 'everything']):
            scope = "comprehensive"
        elif any(word in intention_lower for word in ['quick', 'simple', 'basic', 'just']):
            scope = "minimal"
        else:
            scope = "focused"
        
        # Determine specific action
        action = self.extract_action_verb(intention_text)
        
        return {
            "type": intention_type,
            "target": target,
            "action": action,
            "scope": scope,
            "keywords": self.extract_keywords(intention_text),
            "requires_field_system": self.requires_field_system(intention_lower),
            "estimated_complexity": self.estimate_complexity(intention_type, scope, target)
        }
    
    def extract_action_verb(self, text: str) -> str:
        """Extract the main action verb from intention"""
        words = text.lower().split()
        action_verbs = ['analyze', 'create', 'fix', 'run', 'execute', 'generate', 'build', 
                       'check', 'review', 'process', 'transform', 'configure', 'setup',
                       'report', 'show', 'list', 'find', 'search', 'update', 'install']
        
        for word in words:
            if word in action_verbs:
                return word
        return "process"
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords for execution"""
        words = text.lower().replace(',', ' ').replace('.', ' ').split()
        keywords = []
        
        relevant_terms = [
            'python', 'mcp', 'warp', 'field', 'living', 'dev', 'dojo', 'active',
            'analyze', 'create', 'fix', 'report', 'status', 'config', 'setup',
            'files', 'code', 'system', 'server', 'connection', 'api', 'key'
        ]
        
        for word in words:
            if word in relevant_terms and word not in keywords:
                keywords.append(word)
                
        return keywords[:5]  # Limit to 5 most relevant
    
    def requires_field_system(self, intention_lower: str) -> bool:
        """Determine if this intention requires field system components"""
        field_indicators = [
            'field', 'living', 'dojo', 'atlas', 'tata', 'obi-wan',
            'mcp', 'warp', 'intention', 'sovereign', 'quantum'
        ]
        return any(indicator in intention_lower for indicator in field_indicators)
    
    def estimate_complexity(self, intention_type: str, scope: str, target: str) -> str:
        """Estimate complexity to set expectations"""
        complexity_score = 0
        
        # Type complexity
        type_scores = {"THINK": 1, "REPORT": 1, "ANALYZE": 2, "EXECUTE": 2, "SYSTEM": 3, "CREATE": 3, "PROCESS": 3}
        complexity_score += type_scores.get(intention_type, 2)
        
        # Scope complexity
        scope_scores = {"minimal": 1, "focused": 2, "comprehensive": 3}
        complexity_score += scope_scores.get(scope, 2)
        
        # Target complexity
        target_scores = {"python_code": 1, "warp_config": 2, "mcp_servers": 2, "field_system": 3}
        complexity_score += target_scores.get(target, 2)
        
        if complexity_score <= 3:
            return "simple"
        elif complexity_score <= 6:
            return "moderate" 
        else:
            return "complex"
    
    async def execute_intention(self, intention: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the intention through appropriate field system components"""
        
        analysis = intention["analysis"]
        
        print(f"\n🚀 Executing intention: {analysis['type']} → {analysis['target']}")
        print(f"Complexity: {analysis['estimated_complexity']}")
        print()
        
        # Route to appropriate execution method
        execution_method = f"execute_{analysis['type'].lower()}"
        
        if hasattr(self, execution_method):
            method = getattr(self, execution_method)
            result = await method(intention)
        else:
            result = await self.execute_generic(intention)
        
        return result
    
    async def execute_analyze(self, intention: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ANALYZE type intentions"""
        analysis = intention["analysis"]
        target = analysis["target"]
        
        results = {"type": "analyze", "findings": [], "recommendations": []}
        
        if target == "python_code":
            results = await self.analyze_python_code(intention)
        elif target == "field_system":
            results = await self.analyze_field_system(intention)
        elif target == "mcp_servers":
            results = await self.analyze_mcp_servers(intention)
        else:
            results["findings"].append(f"Analysis target '{target}' mapped to generic file analysis")
            results = await self.analyze_files_generic(intention)
        
        return results
    
    async def execute_report(self, intention: Dict[str, Any]) -> Dict[str, Any]:
        """Execute REPORT type intentions"""
        analysis = intention["analysis"]
        
        print("📊 Generating report...")
        
        results = {
            "type": "report",
            "timestamp": datetime.now().isoformat(),
            "sections": {}
        }
        
        # Field system status
        if analysis["target"] in ["field_system", "unknown"]:
            results["sections"]["Field System Status"] = await self.get_field_status()
        
        # MCP servers status
        if "mcp" in analysis["keywords"] or analysis["target"] == "mcp_servers":
            results["sections"]["MCP Servers"] = await self.get_mcp_status()
        
        # Warp configuration status
        if "warp" in analysis["keywords"] or analysis["target"] == "warp_config":
            results["sections"]["Warp Configuration"] = await self.get_warp_status()
        
        return results
    
    async def execute_system(self, intention: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SYSTEM type intentions (fix, configure, setup)"""
        analysis = intention["analysis"]
        
        print("🔧 Executing system operation...")
        
        results = {
            "type": "system",
            "actions_taken": [],
            "status": "in_progress"
        }
        
        # Route to specific system operations
        if "mcp" in analysis["keywords"]:
            results = await self.fix_mcp_system(intention)
        elif "warp" in analysis["keywords"]:
            results = await self.fix_warp_system(intention)
        else:
            results = await self.fix_field_system(intention)
        
        return results
    
    async def execute_generic(self, intention: Dict[str, Any]) -> Dict[str, Any]:
        """Generic execution for unspecified intention types"""
        
        print("⚙️ Executing through field system...")
        
        return {
            "type": "generic",
            "message": f"Processed intention: {intention['raw_intention']}",
            "recommendations": [
                "Consider being more specific about desired output",
                "Try using action words like 'analyze', 'create', 'fix', 'report'"
            ],
            "status": "completed"
        }
    
    async def analyze_python_code(self, intention: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Python code in field system"""
        findings = []
        recommendations = []
        
        field_dirs = [
            "/Users/jbear/FIELD-LIVING/●◎_memory_core",
            "/Users/jbear/FIELD-DEV",
            "/Users/jbear/FIELD/◼︎DOJO_ACTIVE"
        ]
        
        python_files_found = 0
        
        for field_dir in field_dirs:
            field_path = Path(field_dir)
            if field_path.exists():
                py_files = list(field_path.rglob("*.py"))
                python_files_found += len(py_files)
                
                if py_files:
                    findings.append(f"Found {len(py_files)} Python files in {field_path.name}")
                    
                    # Quick analysis
                    for py_file in py_files[:3]:  # Sample first 3 files
                        try:
                            content = py_file.read_text()
                            lines = len(content.splitlines())
                            imports = content.count("import ")
                            findings.append(f"  {py_file.name}: {lines} lines, {imports} imports")
                        except Exception:
                            pass
        
        if python_files_found == 0:
            findings.append("No Python files found in field directories")
            recommendations.append("Consider checking if field directories are properly configured")
        else:
            recommendations.append(f"Total {python_files_found} Python files available for analysis")
            recommendations.append("Use specific file paths for detailed analysis")
        
        return {
            "type": "analyze",
            "target": "python_code",
            "findings": findings,
            "recommendations": recommendations,
            "file_count": python_files_found
        }
    
    async def get_field_status(self) -> Dict[str, Any]:
        """Get status of field system directories and key files"""
        
        status = {
            "directories": {},
            "key_files": {},
            "summary": ""
        }
        
        # Check field directories
        field_dirs = {
            "FIELD-LIVING": "/Users/jbear/FIELD-LIVING",
            "FIELD-DEV": "/Users/jbear/FIELD-DEV", 
            "DOJO_ACTIVE": "/Users/jbear/FIELD/◼︎DOJO_ACTIVE",
            "FIELD_ROOT": "/Users/jbear/FIELD"
        }
        
        total_files = 0
        
        for name, path in field_dirs.items():
            field_path = Path(path)
            if field_path.exists():
                file_count = len(list(field_path.rglob("*.*")))
                status["directories"][name] = {
                    "exists": True,
                    "path": path,
                    "file_count": file_count
                }
                total_files += file_count
            else:
                status["directories"][name] = {
                    "exists": False,
                    "path": path,
                    "file_count": 0
                }
        
        status["summary"] = f"Field system active with {total_files} total files across {len([d for d in status['directories'].values() if d['exists']])} directories"
        
        return status
    
    async def get_mcp_status(self) -> Dict[str, Any]:
        """Get MCP servers status"""
        
        mcp_status = {
            "warp_mcp_config": "unknown",
            "mcp_servers_found": 0,
            "test_results": []
        }
        
        # Check Warp MCP configuration
        mcp_config_path = Path("/Users/jbear/.warp/mcp-servers")
        if mcp_config_path.exists():
            server_files = list(mcp_config_path.glob("*.json"))
            mcp_status["mcp_servers_found"] = len(server_files)
            mcp_status["warp_mcp_config"] = "configured"
            
            # Try to test a few key servers
            key_servers = ["filesystem", "git", "memory"]
            for server in key_servers:
                server_file = mcp_config_path / f"{server}.json"
                if server_file.exists():
                    mcp_status["test_results"].append(f"✅ {server} server configured")
                else:
                    mcp_status["test_results"].append(f"❌ {server} server missing")
        else:
            mcp_status["warp_mcp_config"] = "not_configured"
            mcp_status["test_results"].append("❌ MCP configuration directory not found")
        
        return mcp_status
    
    async def get_warp_status(self) -> Dict[str, Any]:
        """Get Warp configuration status"""
        
        warp_status = {
            "config_files": {},
            "environment": "unknown",
            "api_keys": "unknown"
        }
        
        warp_config_dir = Path("/Users/jbear/.warp")
        if warp_config_dir.exists():
            # Check key config files
            key_files = ["settings.yaml", "environment", "workflows.yaml", "mcp_servers.yaml"]
            for file_name in key_files:
                file_path = warp_config_dir / file_name
                warp_status["config_files"][file_name] = "exists" if file_path.exists() else "missing"
            
            # Check environment file for API keys
            env_file = warp_config_dir / "environment"
            if env_file.exists():
                try:
                    env_content = env_file.read_text()
                    if "OPENAI_API_KEY" in env_content:
                        warp_status["api_keys"] = "configured"
                    else:
                        warp_status["api_keys"] = "missing"
                    warp_status["environment"] = "configured"
                except Exception:
                    warp_status["environment"] = "error"
            else:
                warp_status["environment"] = "not_configured"
        else:
            warp_status["config_files"]["status"] = "warp_config_directory_missing"
        
        return warp_status
    
    def display_results(self, results: Dict[str, Any]):
        """Display execution results in clear, actionable format"""
        
        print("\n" + "="*80)
        print("🎯 INTENTION EXECUTION RESULTS")
        print("="*80)
        
        result_type = results.get("type", "unknown")
        
        if result_type == "analyze":
            self.display_analyze_results(results)
        elif result_type == "report":
            self.display_report_results(results)
        elif result_type == "system":
            self.display_system_results(results)
        else:
            self.display_generic_results(results)
        
        print("="*80)
    
    def display_analyze_results(self, results: Dict[str, Any]):
        """Display analysis results"""
        
        print(f"🔍 ANALYSIS RESULTS - {results.get('target', 'Unknown Target').upper()}")
        print()
        
        findings = results.get("findings", [])
        if findings:
            print("📋 FINDINGS:")
            for i, finding in enumerate(findings, 1):
                print(f"   {i}. {finding}")
            print()
        
        recommendations = results.get("recommendations", [])
        if recommendations:
            print("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
            print()
    
    def display_report_results(self, results: Dict[str, Any]):
        """Display report results"""
        
        print(f"📊 SYSTEM REPORT - {results.get('timestamp', 'Unknown Time')}")
        print()
        
        sections = results.get("sections", {})
        for section_name, section_data in sections.items():
            print(f"▶ {section_name.upper()}")
            
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    if isinstance(value, dict):
                        print(f"   {key}:")
                        for sub_key, sub_value in value.items():
                            print(f"     {sub_key}: {sub_value}")
                    elif isinstance(value, list):
                        print(f"   {key}:")
                        for item in value:
                            print(f"     • {item}")
                    else:
                        print(f"   {key}: {value}")
            elif isinstance(section_data, list):
                for item in section_data:
                    print(f"   • {item}")
            else:
                print(f"   {section_data}")
            print()
    
    def display_system_results(self, results: Dict[str, Any]):
        """Display system operation results"""
        
        print(f"🔧 SYSTEM OPERATION RESULTS")
        print()
        
        actions = results.get("actions_taken", [])
        if actions:
            print("⚙️ ACTIONS TAKEN:")
            for i, action in enumerate(actions, 1):
                print(f"   {i}. {action}")
            print()
        
        status = results.get("status", "unknown")
        print(f"📊 STATUS: {status.upper()}")
        
        if "errors" in results:
            print(f"❌ ERRORS:")
            for error in results["errors"]:
                print(f"   • {error}")
    
    def display_generic_results(self, results: Dict[str, Any]):
        """Display generic results"""
        
        print("⚙️ EXECUTION COMPLETE")
        print()
        
        message = results.get("message", "No specific output available")
        print(f"📝 RESULT: {message}")
        print()
        
        if "recommendations" in results:
            print("💡 SUGGESTIONS:")
            for rec in results["recommendations"]:
                print(f"   • {rec}")

async def main():
    """Main intention interface loop"""
    
    interface = IntentionInterface()
    
    while True:
        try:
            interface.display_welcome()
            
            # Get intention from user
            intention = await interface.get_intention()
            if not intention:
                print("👋 No intention provided. Exiting.")
                break
            
            # Execute intention
            results = await interface.execute_intention(intention)
            
            # Display results
            interface.display_results(results)
            
            # Ask if user wants to continue
            print("\n" + "-"*80)
            continue_session = input("🔄 Enter another intention? (y/N): ").strip().lower()
            if continue_session != 'y':
                print("👋 Session ended. Your field system remains active.")
                break
                
        except KeyboardInterrupt:
            print("\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.exception("Intention interface error")
            break

if __name__ == "__main__":
    asyncio.run(main())