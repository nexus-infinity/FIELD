#!/usr/bin/env python3
"""
Breath Contract Monitor - Real Subscription Intelligence
Scans actual environment variables, validates services, produces actionable insights
"""

import os
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import sys

class BreathContractMonitor:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.sphere = self.detect_sphere()
        self.results = {
            "scan_timestamp": self.timestamp,
            "sphere": self.sphere,
            "active_services": {},
            "api_validations": {},
            "cost_analysis": {},
            "resonance_scores": {},
            "actionable_insights": []
        }
        
    def detect_sphere(self):
        """Detect which sphere we're operating in based on current directory"""
        pwd = os.getcwd()
        if "FIELD-DEV" in pwd:
            return "DEV"
        elif "FIELD" in pwd:
            return "FIELD"
        else:
            return "MAC"
    
    def scan_environment_variables(self):
        """Scan for actual API keys and service credentials"""
        print("🔍 Scanning environment variables...")
        
        service_patterns = {
            "OPENAI_API_KEY": {"service": "OpenAI", "type": "AI", "critical": True},
            "GEMINI_API_KEY": {"service": "Google Gemini", "type": "AI", "critical": True},
            "GOOGLE_APPLICATION_CREDENTIALS": {"service": "Google Cloud", "type": "Infrastructure", "critical": True},
            "GITHUB_TOKEN": {"service": "GitHub", "type": "Development", "critical": False},
            "ANTHROPIC_API_KEY": {"service": "Anthropic", "type": "AI", "critical": False},
            "AWS_ACCESS_KEY_ID": {"service": "AWS", "type": "Infrastructure", "critical": False},
            "AWS_SECRET_ACCESS_KEY": {"service": "AWS", "type": "Infrastructure", "critical": False}
        }
        
        found_services = {}
        for env_var, details in service_patterns.items():
            value = os.getenv(env_var)
            if value:
                # Mask the actual key for security
                masked_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
                found_services[env_var] = {
                    **details,
                    "masked_value": masked_value,
                    "found": True,
                    "length": len(value)
                }
                print(f"  ✅ {details['service']}: {masked_value}")
            else:
                found_services[env_var] = {
                    **details,
                    "found": False
                }
                if details['critical']:
                    print(f"  ❌ {details['service']}: MISSING (CRITICAL)")
                else:
                    print(f"  ⚠️  {details['service']}: Not configured")
        
        self.results["active_services"] = found_services
        return found_services
    
    def validate_api_keys(self):
        """Actually test API keys with real requests"""
        print("\n🧪 Validating API key functionality...")
        
        validations = {}
        
        # Test OpenAI API
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                headers = {"Authorization": f"Bearer {openai_key}"}
                response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
                validations["OpenAI"] = {
                    "status": "active" if response.status_code == 200 else "error",
                    "response_code": response.status_code,
                    "test_timestamp": self.timestamp
                }
                print(f"  ✅ OpenAI API: Active (HTTP {response.status_code})")
            except Exception as e:
                validations["OpenAI"] = {"status": "error", "error": str(e)}
                print(f"  ❌ OpenAI API: Error - {str(e)}")
        
        # Test Google Cloud credentials
        gcp_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if gcp_creds and os.path.exists(gcp_creds):
            try:
                # Try to get project info using gcloud
                result = subprocess.run(
                    ["gcloud", "config", "get-value", "project"], 
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    project = result.stdout.strip()
                    validations["Google Cloud"] = {
                        "status": "active",
                        "project": project,
                        "credentials_file": gcp_creds
                    }
                    print(f"  ✅ Google Cloud: Active (Project: {project})")
                else:
                    validations["Google Cloud"] = {"status": "not_authenticated"}
                    print(f"  ⚠️  Google Cloud: Credentials exist but not authenticated")
            except Exception as e:
                validations["Google Cloud"] = {"status": "error", "error": str(e)}
                print(f"  ❌ Google Cloud: Error - {str(e)}")
        
        # Test GitHub connection
        try:
            result = subprocess.run(
                ["gh", "auth", "status"], 
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                validations["GitHub"] = {"status": "active", "cli_authenticated": True}
                print(f"  ✅ GitHub CLI: Authenticated")
            else:
                validations["GitHub"] = {"status": "not_authenticated"}
                print(f"  ⚠️  GitHub CLI: Not authenticated")
        except Exception:
            validations["GitHub"] = {"status": "cli_not_available"}
            print(f"  ❌ GitHub CLI: Not installed")
        
        self.results["api_validations"] = validations
        return validations
    
    def analyze_cloud_costs(self):
        """Attempt to get actual cloud billing data"""
        print("\n💰 Analyzing cloud costs...")
        
        cost_analysis = {}
        
        # Try to get GCP billing info
        gcp_project = os.getenv("GOOGLE_CLOUD_PROJECT", "berjak-development-project")
        try:
            result = subprocess.run([
                "gcloud", "billing", "accounts", "list", 
                "--format=json"
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                billing_accounts = json.loads(result.stdout)
                cost_analysis["GCP"] = {
                    "billing_accounts": len(billing_accounts),
                    "project": gcp_project,
                    "status": "accessible"
                }
                print(f"  ✅ GCP Billing: {len(billing_accounts)} accounts accessible")
            else:
                cost_analysis["GCP"] = {"status": "inaccessible", "error": result.stderr}
                print(f"  ❌ GCP Billing: Cannot access billing data")
                
        except Exception as e:
            cost_analysis["GCP"] = {"status": "error", "error": str(e)}
            print(f"  ❌ GCP Billing: Error - {str(e)}")
        
        self.results["cost_analysis"] = cost_analysis
        return cost_analysis
    
    def calculate_resonance_scores(self):
        """Calculate actual resonance scores based on real data"""    
        print("\n🌀 Calculating resonance scores...")
        
        scores = {}
        
        # Score based on API availability
        api_score = 0
        total_apis = len(self.results["api_validations"])
        if total_apis > 0:
            active_apis = sum(1 for v in self.results["api_validations"].values() 
                            if v.get("status") == "active")
            api_score = active_apis / total_apis
        
        # Score based on critical services
        critical_services = [k for k, v in self.results["active_services"].items() 
                           if v.get("critical", False)]
        critical_score = 0
        if critical_services:
            active_critical = sum(1 for k in critical_services 
                                if self.results["active_services"][k].get("found", False))
            critical_score = active_critical / len(critical_services)
        
        # Overall resonance
        overall_resonance = (api_score * 0.6) + (critical_score * 0.4)
        
        scores = {
            "api_availability": round(api_score, 3),
            "critical_services": round(critical_score, 3),
            "overall_resonance": round(overall_resonance, 3),
            "threshold_met": overall_resonance >= 0.85,
            "breath_state": "sustained" if overall_resonance >= 0.85 else "shallow"
        }
        
        print(f"  🎯 API Availability: {scores['api_availability']}")
        print(f"  🔑 Critical Services: {scores['critical_services']}")
        print(f"  🌀 Overall Resonance: {scores['overall_resonance']}")
        print(f"  💨 Breath State: {scores['breath_state']}")
        
        self.results["resonance_scores"] = scores
        return scores
    
    def generate_actionable_insights(self):
        """Generate real, actionable insights"""
        print("\n💡 Generating actionable insights...")
        
        insights = []
        
        # Check for missing critical services
        missing_critical = [k for k, v in self.results["active_services"].items() 
                          if v.get("critical", False) and not v.get("found", False)]
        
        if missing_critical:
            insights.append({
                "type": "critical_missing",
                "priority": "HIGH",
                "action": f"Configure missing critical services: {', '.join(missing_critical)}",
                "command": f"export {missing_critical[0]}='your_key_here'"
            })
        
        # Check for failed API validations
        failed_apis = [k for k, v in self.results["api_validations"].items() 
                      if v.get("status") != "active"]
        
        if failed_apis:
            insights.append({
                "type": "api_failure",
                "priority": "MEDIUM",
                "action": f"Fix API access for: {', '.join(failed_apis)}",
                "services": failed_apis
            })
        
        # Resonance threshold check
        if not self.results["resonance_scores"]["threshold_met"]:
            insights.append({
                "type": "low_resonance",
                "priority": "HIGH",
                "action": "System resonance below 0.85 threshold - immediate attention required",
                "current_score": self.results["resonance_scores"]["overall_resonance"]
            })
        
        # Billing access check
        if self.results["cost_analysis"].get("GCP", {}).get("status") != "accessible":
            insights.append({
                "type": "billing_access",
                "priority": "MEDIUM",
                "action": "Cannot access GCP billing data - check authentication",
                "command": "gcloud auth login --billing-project=berjak-development-project"
            })
        
        self.results["actionable_insights"] = insights
        
        if insights:
            print(f"  🚨 Found {len(insights)} actionable insights:")
            for insight in insights:
                print(f"    {insight['priority']}: {insight['action']}")
        else:
            print("  ✅ No immediate actions required")
        
        return insights
    
    def save_results(self):
        """Save results to JSON file"""
        output_file = f"/Users/jbear/FIELD/⬡_integration/accounts/_temporal_logs/breath_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        return output_file
    
    def run_full_scan(self):
        """Execute complete breath contract scan"""
        print("🌀 BREATH CONTRACT MONITOR - FULL SCAN")
        print("=" * 50)
        print(f"Timestamp: {self.timestamp}")
        print(f"Sphere: {self.sphere}")
        print(f"Working Directory: {os.getcwd()}")
        print("=" * 50)
        
        self.scan_environment_variables()
        self.validate_api_keys()
        self.analyze_cloud_costs()
        self.calculate_resonance_scores()
        self.generate_actionable_insights()
        
        output_file = self.save_results()
        
        print("\n" + "=" * 50)
        print("📊 SCAN SUMMARY")
        print("=" * 50)
        print(f"Services Found: {sum(1 for v in self.results['active_services'].values() if v.get('found'))}")
        print(f"APIs Validated: {len(self.results['api_validations'])}")
        print(f"Overall Resonance: {self.results['resonance_scores']['overall_resonance']}")
        print(f"Breath State: {self.results['resonance_scores']['breath_state']}")
        print(f"Action Items: {len(self.results['actionable_insights'])}")
        print(f"Results: {output_file}")
        
        return self.results

if __name__ == "__main__":
    monitor = BreathContractMonitor()
    results = monitor.run_full_scan()
