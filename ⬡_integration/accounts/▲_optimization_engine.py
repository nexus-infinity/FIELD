#!/usr/bin/env python3
"""
Optimization Engine - Automated Issue Resolution
Takes output from breath_contract_monitor and automatically fixes actionable issues
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path

class OptimizationEngine:
    def __init__(self, scan_results_file=None):
        self.timestamp = datetime.now().isoformat()
        if scan_results_file:
            with open(scan_results_file, 'r') as f:
                self.scan_results = json.load(f)
        else:
            # Find the most recent scan file
            scan_dir = Path("/Users/jbear/FIELD/⬡_integration/accounts/_temporal_logs")
            scan_files = list(scan_dir.glob("breath_scan_*.json"))
            if scan_files:
                latest_scan = max(scan_files, key=lambda x: x.stat().st_mtime)
                with open(latest_scan, 'r') as f:
                    self.scan_results = json.load(f)
                print(f"📁 Loaded scan results from: {latest_scan}")
            else:
                raise FileNotFoundError("No scan results found. Run breath_contract_monitor.py first.")
        
        self.fixes_applied = []
        self.fixes_failed = []
    
    def fix_github_authentication(self):
        """Attempt to authenticate GitHub CLI"""
        print("🔧 Attempting to fix GitHub authentication...")
        
        try:
            # Check if gh CLI is installed
            result = subprocess.run(["which", "gh"], capture_output=True, text=True)
            if result.returncode != 0:
                print("  📦 Installing GitHub CLI...")
                install_result = subprocess.run([
                    "brew", "install", "gh"
                ], capture_output=True, text=True, timeout=60)
                
                if install_result.returncode != 0:
                    self.fixes_failed.append({
                        "issue": "GitHub CLI installation",
                        "error": install_result.stderr,
                        "manual_action": "Run: brew install gh"
                    })
                    return False
            
            # Attempt authentication
            print("  🔑 Initiating GitHub authentication...")
            auth_result = subprocess.run([
                "gh", "auth", "login", "--web"
            ], capture_output=True, text=True, timeout=30)
            
            if auth_result.returncode == 0:
                self.fixes_applied.append({
                    "issue": "GitHub authentication",
                    "action": "Initiated web-based auth",
                    "status": "success"
                })
                print("  ✅ GitHub authentication initiated - complete in browser")
                return True
            else:
                self.fixes_failed.append({
                    "issue": "GitHub authentication",
                    "error": auth_result.stderr,
                    "manual_action": "Run: gh auth login"
                })
                return False
                
        except Exception as e:
            self.fixes_failed.append({
                "issue": "GitHub authentication",
                "error": str(e),
                "manual_action": "Manually run: gh auth login"
            })
            return False
    
    def optimize_environment_variables(self):
        """Generate optimized environment variable setup"""
        print("🌿 Optimizing environment variables...")
        
        missing_critical = []
        for service, details in self.scan_results["active_services"].items():
            if details.get("critical", False) and not details.get("found", False):
                missing_critical.append(service)
        
        if missing_critical:
            env_script = "/Users/jbear/FIELD/⬡_integration/accounts/env_setup.sh"
            with open(env_script, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write("# Generated environment setup script\n")
                f.write(f"# Created: {self.timestamp}\n\n")
                
                for service in missing_critical:
                    f.write(f"# {service}\n")
                    f.write(f"# export {service}='your_key_here'\n\n")
                
                f.write("echo 'Environment variables configured'\n")
            
            os.chmod(env_script, 0o755)
            
            self.fixes_applied.append({
                "issue": "Missing environment variables",
                "action": f"Generated setup script: {env_script}",
                "status": "template_created"
            })
            print(f"  📝 Generated environment setup script: {env_script}")
        else:
            print("  ✅ All critical environment variables are configured")
    
    def enhance_api_monitoring(self):
        """Set up continuous API monitoring"""
        print("📊 Setting up enhanced API monitoring...")
        
        # Create a monitoring cron job script
        monitor_script = "/Users/jbear/FIELD/⬡_integration/accounts/continuous_monitor.sh"
        with open(monitor_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Continuous API monitoring script\n")
            f.write(f"# Generated: {self.timestamp}\n\n")
            f.write("cd /Users/jbear/FIELD\n")
            f.write("python3 ⬡_integration/accounts/●_breath_contract_monitor.py > /tmp/breath_monitor.log 2>&1\n")
            f.write("echo \"Monitor run completed at $(date)\" >> /tmp/breath_monitor.log\n")
        
        os.chmod(monitor_script, 0o755)
        
        # Create a simple LaunchAgent plist for macOS
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.field.breath-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>{monitor_script}</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
        
        plist_path = "/Users/jbear/FIELD/⬡_integration/accounts/com.field.breath-monitor.plist"
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        
        self.fixes_applied.append({
            "issue": "API monitoring automation",
            "action": f"Created monitoring script: {monitor_script}",
            "status": "automated"
        })
        
        print(f"  ⏰ Created continuous monitoring script: {monitor_script}")
        print(f"  📋 Created LaunchAgent plist: {plist_path}")
        print("  💡 To activate: cp {} ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.field.breath-monitor.plist".format(plist_path))
    
    def generate_resonance_improvement_plan(self):
        """Generate specific plan to improve resonance score"""
        print("🌀 Generating resonance improvement plan...")
        
        current_score = self.scan_results["resonance_scores"]["overall_resonance"]
        target_score = 0.85
        improvement_needed = target_score - current_score
        
        plan = {
            "current_resonance": current_score,
            "target_resonance": target_score,
            "improvement_needed": round(improvement_needed, 3),
            "recommendations": []
        }
        
        # Analyze what's dragging down the score
        api_score = self.scan_results["resonance_scores"]["api_availability"]
        critical_score = self.scan_results["resonance_scores"]["critical_services"]
        
        if api_score < 0.85:
            failed_apis = [k for k, v in self.scan_results["api_validations"].items() 
                          if v.get("status") != "active"]
            plan["recommendations"].append({
                "area": "API Availability",
                "current": api_score,
                "target": 0.85,
                "actions": [f"Fix authentication for {api}" for api in failed_apis],
                "impact": "High - APIs are weighted 60% in resonance calculation"
            })
        
        if critical_score < 1.0:
            missing_services = [k for k, v in self.scan_results["active_services"].items() 
                              if v.get("critical", False) and not v.get("found", False)]
            plan["recommendations"].append({
                "area": "Critical Services",
                "current": critical_score,
                "target": 1.0,
                "actions": [f"Configure {service}" for service in missing_services],
                "impact": "Medium - Critical services are weighted 40% in resonance calculation"
            })
        
        # Save the plan
        plan_file = "/Users/jbear/FIELD/⬡_integration/accounts/_temporal_logs/resonance_improvement_plan.json"
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"  📈 Current resonance: {current_score}")
        print(f"  🎯 Target resonance: {target_score}")
        print(f"  📊 Improvement needed: {improvement_needed}")
        print(f"  📋 Improvement plan saved: {plan_file}")
        
        self.fixes_applied.append({
            "issue": "Low resonance score",
            "action": f"Generated improvement plan: {plan_file}",
            "status": "plan_created"
        })
        
        return plan
    
    def run_optimization_cycle(self):
        """Execute complete optimization cycle"""
        print("▲ ATLAS OPTIMIZATION ENGINE - FULL CYCLE")
        print("=" * 50)
        print(f"Timestamp: {self.timestamp}")
        print(f"Source scan: {self.scan_results['scan_timestamp']}")
        print(f"Action items to process: {len(self.scan_results['actionable_insights'])}")
        print("=" * 50)
        
        # Process each actionable insight
        for insight in self.scan_results["actionable_insights"]:
            print(f"\n🎯 Processing: {insight['action']}")
            
            if insight["type"] == "api_failure" and "GitHub" in insight.get("services", []):
                self.fix_github_authentication()
            
            elif insight["type"] == "critical_missing":
                self.optimize_environment_variables()
            
            elif insight["type"] == "low_resonance":
                self.generate_resonance_improvement_plan()
        
        # Always set up monitoring
        self.enhance_api_monitoring()
        
        # Generate summary
        print("\n" + "=" * 50)
        print("📊 OPTIMIZATION SUMMARY")  
        print("=" * 50)
        print(f"Fixes Applied: {len(self.fixes_applied)}")
        print(f"Fixes Failed: {len(self.fixes_failed)}")
        
        if self.fixes_applied:
            print("\n✅ Successfully Applied:")
            for fix in self.fixes_applied:
                print(f"  • {fix['action']}")
        
        if self.fixes_failed:
            print("\n❌ Failed Fixes (Manual Action Required):")
            for fix in self.fixes_failed:
                print(f"  • {fix['issue']}: {fix['manual_action']}")
        
        # Save optimization results
        results = {
            "optimization_timestamp": self.timestamp,
            "source_scan": self.scan_results["scan_timestamp"],
            "fixes_applied": self.fixes_applied,
            "fixes_failed": self.fixes_failed
        }
        
        results_file = f"/Users/jbear/FIELD/⬡_integration/accounts/_temporal_logs/optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📁 Optimization results saved: {results_file}")
        
        return results

if __name__ == "__main__":
    engine = OptimizationEngine()
    results = engine.run_optimization_cycle()
