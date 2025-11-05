#!/usr/bin/env python3
"""
Sacred Component Incremental Deployment System
==================================================
Implements Step 10: Incrementally deploy, validate, and monitor each sacred component
with comprehensive validation scripts (geometric, symbolic, flow) and backward compatibility.
"""

import json
import logging
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import yaml
import redis
import psutil

class SacredDeploymentManager:
    """Manages incremental deployment of sacred components with full validation."""
    
    def __init__(self, field_path: str = "/Users/jbear/FIELD"):
        self.field_path = Path(field_path)
        self.deployment_log_path = self.field_path / "logs" / "sacred_deployment.log"
        self.validation_results_path = self.field_path / "logs" / "validation_results.json"
        self.dashboard_state_path = self.field_path / "logs" / "dashboard_state.json"
        
        # Sacred tetrahedral components in deployment order
        self.sacred_components = [
            {
                "name": "ATLAS",
                "symbol": "▲",
                "path": self.field_path / "▲ATLAS",
                "type": "tooling_validation",
                "dependencies": [],
                "validation_types": ["geometric", "symbolic", "flow"]
            },
            {
                "name": "TATA", 
                "symbol": "▼",
                "path": self.field_path / "▼TATA",
                "type": "temporal_truth",
                "dependencies": ["ATLAS"],
                "validation_types": ["geometric", "symbolic", "flow", "temporal"]
            },
            {
                "name": "OBI-WAN",
                "symbol": "●", 
                "path": self.field_path / "●OBI-WAN",
                "type": "living_memory",
                "dependencies": ["ATLAS", "TATA"],
                "validation_types": ["geometric", "symbolic", "flow", "memory"]
            },
            {
                "name": "DOJO",
                "symbol": "◼",
                "path": self.field_path / "◼DOJO", 
                "type": "manifestation",
                "dependencies": ["ATLAS", "TATA", "OBI-WAN"],
                "validation_types": ["geometric", "symbolic", "flow", "execution"]
            }
        ]
        
        # Setup logging
        self._setup_logging()
        
        # Initialize Redis for real-time monitoring
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.redis_client.ping()
        except:
            self.logger.warning("Redis not available, using file-based monitoring only")
            self.redis_client = None
    
    def _setup_logging(self):
        """Setup comprehensive logging system."""
        os.makedirs(self.deployment_log_path.parent, exist_ok=True)
        
        self.logger = logging.getLogger("SacredDeployment")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(self.deployment_log_path)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def run_geometric_validation(self, component: Dict) -> Dict[str, Any]:
        """Run geometric validation on sacred component."""
        self.logger.info(f"Running geometric validation for {component['name']}")
        
        validation_result = {
            "component": component["name"],
            "validation_type": "geometric",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "passed": True,
            "details": {},
            "warnings": []
        }
        
        component_path = component["path"]
        
        # Check sacred geometry alignment
        if component_path.exists():
            # Verify symbolic naming consistency
            symbol_files = list(component_path.glob(f"{component['symbol']}*"))
            validation_result["details"]["symbol_files_count"] = len(symbol_files)
            
            # Check for geometric patterns in file structure
            sacred_patterns = list(component_path.glob("*sacred*"))
            validation_result["details"]["sacred_patterns_count"] = len(sacred_patterns)
            
            # Verify tetrahedral structure integrity
            if component["name"] == "ATLAS":
                required_subdirs = ["tools", "_decoded"]
            elif component["name"] == "TATA":
                required_subdirs = []  # TATA is more flexible
            elif component["name"] == "OBI-WAN":
                required_subdirs = []
            elif component["name"] == "DOJO":
                required_subdirs = ["metrics"]
            
            missing_dirs = []
            for required_dir in required_subdirs:
                if not (component_path / required_dir).exists():
                    missing_dirs.append(required_dir)
            
            if missing_dirs:
                validation_result["warnings"].append(f"Missing directories: {missing_dirs}")
            
            validation_result["details"]["structure_complete"] = len(missing_dirs) == 0
        else:
            validation_result["passed"] = False
            validation_result["details"]["error"] = f"Component path does not exist: {component_path}"
        
        return validation_result
    
    def run_symbolic_validation(self, component: Dict) -> Dict[str, Any]:
        """Run symbolic validation on sacred component."""
        self.logger.info(f"Running symbolic validation for {component['name']}")
        
        validation_result = {
            "component": component["name"],
            "validation_type": "symbolic",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "passed": True,
            "details": {},
            "warnings": []
        }
        
        component_path = component["path"]
        
        if component_path.exists():
            # Check symbolic consistency
            expected_symbol = component["symbol"]
            symbol_usage_count = 0
            
            # Scan for symbol usage in filenames and content
            for file_path in component_path.rglob("*"):
                if file_path.is_file():
                    if expected_symbol in file_path.name:
                        symbol_usage_count += 1
            
            validation_result["details"]["symbol_usage_count"] = symbol_usage_count
            validation_result["details"]["expected_symbol"] = expected_symbol
            
            # Validate symbolic coherence based on component type
            if component["type"] == "tooling_validation" and symbol_usage_count < 2:
                validation_result["warnings"].append("Low symbolic density for tooling component")
            
        else:
            validation_result["passed"] = False
            validation_result["details"]["error"] = f"Component path does not exist: {component_path}"
        
        return validation_result
    
    def run_flow_validation(self, component: Dict, deployed_components: List[str]) -> Dict[str, Any]:
        """Run flow validation on sacred component."""
        self.logger.info(f"Running flow validation for {component['name']}")
        
        validation_result = {
            "component": component["name"],
            "validation_type": "flow",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "passed": True,
            "details": {},
            "warnings": []
        }
        
        # Check dependency satisfaction
        missing_deps = []
        for dep in component["dependencies"]:
            if dep not in deployed_components:
                missing_deps.append(dep)
        
        if missing_deps:
            validation_result["passed"] = False
            validation_result["details"]["missing_dependencies"] = missing_deps
        else:
            validation_result["details"]["dependencies_satisfied"] = True
        
        # Check tetrahedral flow integration
        component_path = component["path"]
        if component_path.exists():
            # Look for flow configuration files
            flow_configs = list(component_path.glob("*flow*")) + list(component_path.glob("*config*"))
            validation_result["details"]["flow_configs_found"] = len(flow_configs)
            
            # Check for integration points with other components
            integration_files = []
            for dep in component["dependencies"]:
                dep_refs = list(component_path.rglob(f"*{dep.lower()}*"))
                integration_files.extend(dep_refs)
            
            validation_result["details"]["integration_points"] = len(integration_files)
        
        return validation_result
    
    def run_comprehensive_validation(self, component: Dict, deployed_components: List[str]) -> Dict[str, Any]:
        """Run all validation types for a component."""
        self.logger.info(f"Starting comprehensive validation for {component['name']}")
        
        validation_results = {
            "component": component["name"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_passed": True,
            "validations": {}
        }
        
        # Run geometric validation
        if "geometric" in component["validation_types"]:
            geometric_result = self.run_geometric_validation(component)
            validation_results["validations"]["geometric"] = geometric_result
            if not geometric_result["passed"]:
                validation_results["overall_passed"] = False
        
        # Run symbolic validation  
        if "symbolic" in component["validation_types"]:
            symbolic_result = self.run_symbolic_validation(component)
            validation_results["validations"]["symbolic"] = symbolic_result
            if not symbolic_result["passed"]:
                validation_results["overall_passed"] = False
        
        # Run flow validation
        if "flow" in component["validation_types"]:
            flow_result = self.run_flow_validation(component, deployed_components)
            validation_results["validations"]["flow"] = flow_result
            if not flow_result["passed"]:
                validation_results["overall_passed"] = False
        
        return validation_results
    
    def check_backward_compatibility(self, component: Dict) -> Dict[str, Any]:
        """Check backward compatibility with live dashboard."""
        self.logger.info(f"Checking backward compatibility for {component['name']}")
        
        compatibility_result = {
            "component": component["name"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "compatible": True,
            "details": {},
            "issues": []
        }
        
        # Check if dashboard state exists
        if self.dashboard_state_path.exists():
            try:
                with open(self.dashboard_state_path, 'r') as f:
                    dashboard_state = json.load(f)
                
                # Check for API compatibility
                if "api_endpoints" in dashboard_state:
                    endpoints = dashboard_state["api_endpoints"]
                    component_endpoints = [ep for ep in endpoints if component["name"].lower() in ep]
                    compatibility_result["details"]["affected_endpoints"] = component_endpoints
                
                # Check for data structure compatibility
                if "data_schemas" in dashboard_state:
                    schemas = dashboard_state["data_schemas"]
                    if component["name"].lower() in schemas:
                        compatibility_result["details"]["schema_version"] = schemas[component["name"].lower()]
                
            except Exception as e:
                compatibility_result["issues"].append(f"Could not read dashboard state: {str(e)}")
        
        # Check system resource impact
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            compatibility_result["details"]["system_resources"] = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent
            }
            
            if cpu_percent > 80 or memory_percent > 85:
                compatibility_result["issues"].append("High system resource usage detected")
                
        except Exception as e:
            compatibility_result["issues"].append(f"Could not check system resources: {str(e)}")
        
        if compatibility_result["issues"]:
            compatibility_result["compatible"] = False
        
        return compatibility_result
    
    def deploy_component(self, component: Dict, deployed_components: List[str]) -> Tuple[bool, Dict[str, Any]]:
        """Deploy a single sacred component with full validation."""
        component_name = component["name"]
        self.logger.info(f"Starting deployment of sacred component: {component_name}")
        
        deployment_result = {
            "component": component_name,
            "symbol": component["symbol"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "validation_results": {},
            "compatibility_check": {},
            "deployment_log": []
        }
        
        try:
            # Step 1: Pre-deployment validation
            deployment_result["deployment_log"].append("Starting pre-deployment validation")
            validation_results = self.run_comprehensive_validation(component, deployed_components)
            deployment_result["validation_results"] = validation_results
            
            if not validation_results["overall_passed"]:
                deployment_result["deployment_log"].append("Pre-deployment validation failed")
                return False, deployment_result
            
            # Step 2: Backward compatibility check
            deployment_result["deployment_log"].append("Checking backward compatibility")
            compatibility_check = self.check_backward_compatibility(component)
            deployment_result["compatibility_check"] = compatibility_check
            
            if not compatibility_check["compatible"]:
                self.logger.warning(f"Compatibility issues detected for {component_name}")
                deployment_result["deployment_log"].append("Compatibility issues detected, proceeding with caution")
            
            # Step 3: Actual deployment (activation)
            deployment_result["deployment_log"].append("Activating component")
            
            # Create deployment marker
            marker_file = component["path"] / ".deployed"
            with open(marker_file, 'w') as f:
                json.dump({
                    "deployed_at": datetime.now(timezone.utc).isoformat(),
                    "deployer": "SacredDeploymentManager",
                    "validation_passed": True
                }, f, indent=2)
            
            # Update Redis if available
            if self.redis_client:
                self.redis_client.set(f"sacred_component:{component_name}:status", "deployed")
                self.redis_client.set(f"sacred_component:{component_name}:deployed_at", 
                                    datetime.now(timezone.utc).isoformat())
            
            # Step 4: Post-deployment monitoring setup
            deployment_result["deployment_log"].append("Setting up monitoring")
            self._setup_component_monitoring(component)
            
            deployment_result["success"] = True
            deployment_result["deployment_log"].append("Deployment completed successfully")
            
            self.logger.info(f"Successfully deployed sacred component: {component_name}")
            
        except Exception as e:
            deployment_result["deployment_log"].append(f"Deployment failed: {str(e)}")
            self.logger.error(f"Failed to deploy {component_name}: {str(e)}")
        
        return deployment_result["success"], deployment_result
    
    def _setup_component_monitoring(self, component: Dict):
        """Setup monitoring for deployed component."""
        monitoring_config = {
            "component": component["name"],
            "symbol": component["symbol"],
            "path": str(component["path"]),
            "monitoring_enabled": True,
            "metrics": {
                "file_count": len(list(component["path"].rglob("*"))),
                "last_modified": datetime.now(timezone.utc).isoformat()
            }
        }
        
        # Save monitoring config
        monitoring_path = self.field_path / "logs" / "monitoring" / f"{component['name']}.json"
        os.makedirs(monitoring_path.parent, exist_ok=True)
        
        with open(monitoring_path, 'w') as f:
            json.dump(monitoring_config, f, indent=2)
        
        if self.redis_client:
            self.redis_client.set(f"monitoring:{component['name']}", json.dumps(monitoring_config))
    
    def run_incremental_deployment(self) -> Dict[str, Any]:
        """Run the complete incremental deployment process."""
        self.logger.info("Starting incremental sacred component deployment")
        
        deployment_summary = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "components": [],
            "deployed_successfully": [],
            "failed_deployments": [],
            "overall_success": True
        }
        
        deployed_components = []
        
        for component in self.sacred_components:
            self.logger.info(f"Processing component {component['name']} ({component['symbol']})")
            
            success, result = self.deploy_component(component, deployed_components)
            deployment_summary["components"].append(result)
            
            if success:
                deployed_components.append(component["name"])
                deployment_summary["deployed_successfully"].append(component["name"])
                self.logger.info(f"✅ {component['name']} deployed successfully")
                
                # Wait between deployments for system stability
                time.sleep(2)
            else:
                deployment_summary["failed_deployments"].append(component["name"])
                deployment_summary["overall_success"] = False
                self.logger.error(f"❌ {component['name']} deployment failed")
                
                # Stop deployment chain on failure for safety
                break
        
        deployment_summary["completed_at"] = datetime.now(timezone.utc).isoformat()
        deployment_summary["deployed_count"] = len(deployed_components)
        
        # Save comprehensive results
        with open(self.validation_results_path, 'w') as f:
            json.dump(deployment_summary, f, indent=2)
        
        self.logger.info(f"Incremental deployment completed. {len(deployed_components)}/{len(self.sacred_components)} components deployed")
        
        return deployment_summary

def main():
    """Main execution function."""
    deployment_manager = SacredDeploymentManager()
    results = deployment_manager.run_incremental_deployment()
    
    print("\n🔮 Sacred Component Deployment Summary:")
    print(f"Overall Success: {'✅' if results['overall_success'] else '❌'}")
    print(f"Components Deployed: {results['deployed_count']}/{len(deployment_manager.sacred_components)}")
    print(f"Successfully Deployed: {', '.join(results['deployed_successfully'])}")
    
    if results['failed_deployments']:
        print(f"Failed Deployments: {', '.join(results['failed_deployments'])}")
    
    print(f"\nDetailed results saved to: {deployment_manager.validation_results_path}")
    
    return results

if __name__ == "__main__":
    main()
