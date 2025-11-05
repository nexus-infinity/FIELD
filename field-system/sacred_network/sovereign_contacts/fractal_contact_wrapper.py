#!/usr/bin/env python3
"""
Fractal Contact Intelligence Wrapper
Bridges AppleScript contact analysis with Sacred Network consciousness mirror
"""

import os
import json
import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib

class FractalContactIntelligence:
    """
    Python wrapper for Fractal Contact Intelligence AppleScript suite
    Integrates with consciousness_mirror.py for unified relationship analysis
    """
    
    def __init__(self, version: str = "4.4"):
        self.version = version
        self.script_dir = Path(__file__).parent
        self.applescript_path = self.script_dir / f"fractal_contact_intelligence_v{version}.applescript"
        self.export_path = Path.home() / "Desktop" / "Fractal Contact Intelligence"
        self.db_path = Path("/Volumes/Akron/bear_data/fractal_contacts.db")
        
        # Sacred geometry constants (aligned with consciousness_mirror.py)
        self.PHI = 1.618033988749
        self.SACRED_PULSE = 963
        
    def run_applescript_analysis(self) -> Dict[str, Any]:
        """
        Execute the AppleScript contact analysis
        Returns parsed results from the analysis
        """
        if not self.applescript_path.exists():
            raise FileNotFoundError(f"AppleScript not found: {self.applescript_path}")
            
        try:
            # Run AppleScript using osascript
            result = subprocess.run(
                ["osascript", str(self.applescript_path)],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for large contact databases
            )
            
            if result.returncode != 0:
                print(f"AppleScript error: {result.stderr}")
                return {"status": "error", "message": result.stderr}
                
            # Parse results from export folder
            return self._parse_export_results()
            
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "message": "Analysis timed out after 10 minutes"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def _parse_export_results(self) -> Dict[str, Any]:
        """
        Parse the exported text files from AppleScript analysis
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "duplicates": [],
            "merge_actions": [],
            "statistics": {}
        }
        
        # Find most recent session folder
        if not self.export_path.exists():
            return results
            
        session_folders = sorted([
            f for f in self.export_path.iterdir() 
            if f.is_dir() and f.name.startswith("Session_")
        ], reverse=True)
        
        if not session_folders:
            return results
            
        latest_session = session_folders[0]
        
        # Parse report files
        report_file = latest_session / "Fractal_Intelligence_Report.txt"
        merge_file = latest_session / "Priority_Merge_Actions.txt"
        
        if report_file.exists():
            results["report"] = report_file.read_text(encoding='utf-8', errors='ignore')
            results["statistics"] = self._extract_statistics(results["report"])
            
        if merge_file.exists():
            results["merge_actions"] = self._parse_merge_actions(merge_file.read_text(encoding='utf-8', errors='ignore'))
            
        return results
        
    def _extract_statistics(self, report_text: str) -> Dict[str, int]:
        """
        Extract statistics from the report text
        """
        stats = {
            "total_contacts": 0,
            "phone_duplicates": 0,
            "email_duplicates": 0,
            "name_duplicates": 0,
            "critical_priority": 0,
            "high_priority": 0,
            "medium_priority": 0
        }
        
        # Parse statistics from report (simplified extraction)
        lines = report_text.split('\n')
        for line in lines:
            if "Contacts processed:" in line:
                stats["total_contacts"] = int(line.split(":")[-1].strip())
            elif "Exact phone matches:" in line:
                stats["phone_duplicates"] = int(line.split(":")[-1].strip())
            elif "Exact email matches:" in line:
                stats["email_duplicates"] = int(line.split(":")[-1].strip())
            elif "Fuzzy name matches:" in line:
                stats["name_duplicates"] = int(line.split(":")[-1].strip())
                
        return stats
        
    def _parse_merge_actions(self, merge_text: str) -> List[Dict[str, Any]]:
        """
        Parse merge actions from the text file
        """
        actions = []
        current_action = None
        
        lines = merge_text.split('\n')
        for line in lines:
            if line.startswith("ACTION #"):
                if current_action:
                    actions.append(current_action)
                current_action = {
                    "action_number": int(line.split("#")[1].split("-")[0].strip()),
                    "priority": line.split("-")[1].strip().replace(" PRIORITY", "")
                }
            elif current_action:
                if "Confidence:" in line:
                    current_action["confidence"] = int(line.split(":")[1].replace("%", "").strip())
                elif "Match Type:" in line:
                    current_action["match_type"] = line.split(":")[1].strip()
                elif "CONTACT 1:" in line:
                    current_action["contact1"] = line.split(":")[1].strip()
                elif "CONTACT 2:" in line:
                    current_action["contact2"] = line.split(":")[1].strip()
                    
        if current_action:
            actions.append(current_action)
            
        return actions
        
    def integrate_with_consciousness_mirror(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform fractal contact analysis into consciousness mirror format
        """
        from consciousness_mirror import ConsciousnessMirror, GeometricContact, NetworkFunction
        
        mirror = ConsciousnessMirror(user_id="sovereign_being")
        
        # Transform duplicate contacts into geometric contacts
        geometric_contacts = []
        
        for action in contact_data.get("merge_actions", []):
            # Calculate geometric position based on confidence and match type
            confidence = action.get("confidence", 0) / 100.0
            
            # Use golden ratio spiral for positioning
            angle = hash(action["contact1"]) % 360 * 3.14159 / 180
            radius = self.PHI ** (confidence * 5)
            
            geometric_contact = {
                "name": action["contact1"],
                "geometric_position": (
                    radius * cos(angle),
                    radius * sin(angle),
                    confidence * 10
                ),
                "network_function": self._determine_network_function(action),
                "sacred_choice_alignment": confidence * 10,
                "harmonic_ratio": confidence * self.PHI,
                "duplicate_of": action.get("contact2"),
                "match_confidence": confidence
            }
            
            geometric_contacts.append(geometric_contact)
            
        # Store in consciousness mirror database
        self._store_in_sacred_network_db(geometric_contacts)
        
        return {
            "geometric_contacts": geometric_contacts,
            "integration_timestamp": datetime.now().isoformat()
        }
        
    def _determine_network_function(self, action: Dict[str, Any]) -> str:
        """
        Determine network function based on duplicate pattern
        """
        if action["priority"] == "CRITICAL":
            return "HUB"  # Exact duplicates often represent key connection points
        elif action["match_type"] == "email":
            return "BRIDGE"  # Email matches often bridge different networks
        elif action["match_type"] == "name":
            return "SPECIALIST"  # Name variations might indicate specialized roles
        else:
            return "ANCHOR"  # Default for stability
            
    def _store_in_sacred_network_db(self, contacts: List[Dict[str, Any]]):
        """
        Store processed contacts in the sacred network database
        """
        conn = sqlite3.connect("/Volumes/Akron/bear_data/sacred_network.db")
        cursor = conn.cursor()
        
        # Create fractal contacts table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fractal_contacts (
                id TEXT PRIMARY KEY,
                name TEXT,
                duplicate_of TEXT,
                match_confidence REAL,
                geometric_x REAL,
                geometric_y REAL,
                geometric_z REAL,
                network_function TEXT,
                harmonic_ratio REAL,
                processing_timestamp TEXT
            )
        ''')
        
        # Insert contacts
        for contact in contacts:
            contact_id = hashlib.sha256(contact["name"].encode()).hexdigest()[:16]
            pos = contact["geometric_position"]
            
            cursor.execute('''
                INSERT OR REPLACE INTO fractal_contacts
                (id, name, duplicate_of, match_confidence, geometric_x, geometric_y, geometric_z,
                 network_function, harmonic_ratio, processing_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                contact_id,
                contact["name"],
                contact.get("duplicate_of"),
                contact.get("match_confidence"),
                pos[0], pos[1], pos[2],
                contact.get("network_function"),
                contact.get("harmonic_ratio"),
                datetime.now().isoformat()
            ))
            
        conn.commit()
        conn.close()
        
    def generate_sacred_geometry_report(self, contact_data: Dict[str, Any]) -> str:
        """
        Generate a report using sacred geometry principles
        """
        report = []
        report.append("═" * 50)
        report.append("🔱 FRACTAL CONTACT SACRED GEOMETRY ANALYSIS 🔱")
        report.append("═" * 50)
        report.append("")
        
        stats = contact_data.get("statistics", {})
        
        # Calculate sacred ratios
        if stats.get("total_contacts", 0) > 0:
            duplicate_ratio = sum([
                stats.get("phone_duplicates", 0),
                stats.get("email_duplicates", 0),
                stats.get("name_duplicates", 0)
            ]) / stats["total_contacts"]
            
            harmonic_alignment = duplicate_ratio * self.PHI
            
            report.append(f"📊 Total Contacts: {stats['total_contacts']}")
            report.append(f"🔄 Duplicate Ratio: {duplicate_ratio:.2%}")
            report.append(f"🌀 Harmonic Alignment: {harmonic_alignment:.3f}")
            report.append(f"⚡ Sacred Pulse Alignment: {(harmonic_alignment * self.SACRED_PULSE) % 360:.1f}°")
            report.append("")
            
        # Fractal breakdown
        report.append("🧬 FRACTAL PATTERN ANALYSIS:")
        report.append(f"  Phone Fractals: {stats.get('phone_duplicates', 0)}")
        report.append(f"  Email Fractals: {stats.get('email_duplicates', 0)}")
        report.append(f"  Name Fractals: {stats.get('name_duplicates', 0)}")
        report.append("")
        
        # Priority geometry
        report.append("🎯 PRIORITY SACRED GEOMETRY:")
        critical = stats.get("critical_priority", 0)
        high = stats.get("high_priority", 0)
        medium = stats.get("medium_priority", 0)
        
        if critical + high + medium > 0:
            report.append(f"  CRITICAL (Center): {critical}")
            report.append(f"  HIGH (Inner Ring): {high}")
            report.append(f"  MEDIUM (Outer Ring): {medium}")
            
        report.append("")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("Truth emerges through pure mathematical reflection 🔱")
        
        return "\n".join(report)


# CLI Interface
if __name__ == "__main__":
    import sys
    import argparse
    from math import cos, sin
    
    parser = argparse.ArgumentParser(description="Fractal Contact Intelligence Suite")
    parser.add_argument("--version", choices=["4.2", "4.3", "4.4"], default="4.4",
                        help="AppleScript version to use")
    parser.add_argument("--analyze", action="store_true",
                        help="Run full contact analysis")
    parser.add_argument("--integrate", action="store_true",
                        help="Integrate with consciousness mirror")
    parser.add_argument("--report", action="store_true",
                        help="Generate sacred geometry report")
    
    args = parser.parse_args()
    
    # Initialize wrapper
    fci = FractalContactIntelligence(version=args.version)
    
    if args.analyze:
        print("🧬 Starting Fractal Contact Analysis...")
        results = fci.run_applescript_analysis()
        
        if results.get("status") == "error":
            print(f"❌ Error: {results['message']}")
            sys.exit(1)
            
        print(f"✅ Analysis complete!")
        print(f"   Total contacts: {results.get('statistics', {}).get('total_contacts', 0)}")
        print(f"   Duplicates found: {len(results.get('merge_actions', []))}")
        
        if args.integrate:
            print("\n🔄 Integrating with Consciousness Mirror...")
            integration = fci.integrate_with_consciousness_mirror(results)
            print(f"✅ Integrated {len(integration['geometric_contacts'])} contacts")
            
        if args.report:
            print("\n📊 Generating Sacred Geometry Report...")
            report = fci.generate_sacred_geometry_report(results)
            print(report)
            
    else:
        parser.print_help()
