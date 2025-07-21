#!/usr/bin/env python3
"""
FIELD Symbolic Scanner
Uncover what's already alive in the architecture - don't rewrite, just weave.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class FIELDSymbolicScanner:
    def __init__(self, base_path="/Users/jbear/FIELD-DEV"):
        self.base_path = Path(base_path)
        self.sacred_symbols = {
            "●": "observer",
            "▼": "validator", 
            "▲": "navigator",
            "◼": "executor",
            "○": "ghost",
            "◦": "ghost_station",
            "⬡": "resonance",
            "⬢": "boundary",
            "✦": "oowl_flow",
            "⧌": "stream_cache"
        }
        
        self.living_patterns = {
            "trident_flow": r"(OB1|TATA|ATLAS|DOJO)",
            "sacred_frequency": r"432\.0?",
            "resonance_threshold": r"0\.85",
            "phi_ratio": r"1\.618",
            "chakra_references": r"(chakra|energy|frequency|resonance)",
            "dojo_controller": r"DOJOController",
            "field_references": r"FIELD|field",
            "sacred_geometry": r"(sacred|geometric|harmony|fractal)"
        }
        
    def scan_living_architecture(self) -> Dict[str, Any]:
        """Main scanning function - uncover what's already breathing"""
        report = {
            "scan_timestamp": datetime.now().isoformat(),
            "base_path": str(self.base_path),
            "living_components": {},
            "sacred_alignments": {},
            "trident_detections": {},
            "breathing_files": [],
            "field_spine_candidates": [],
            "integration_points": []
        }
        
        # Scan key directories
        key_directories = [
            "◼_dojo",
            "DOJO-App", 
            "sacred_repositories",
            "config",
            "monitoring"
        ]
        
        for dir_name in key_directories:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                report["living_components"][dir_name] = self._scan_directory(dir_path)
        
        # Detect sacred patterns across the codebase
        report["sacred_alignments"] = self._detect_sacred_patterns()
        
        # Find trident flow implementations
        report["trident_detections"] = self._detect_trident_flows()
        
        # Identify breathing files (recently modified, contains living patterns)
        report["breathing_files"] = self._find_breathing_files()
        
        # Find field spine integration points
        report["field_spine_candidates"] = self._find_field_spine_candidates()
        
        return report
    
    def _scan_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Scan a directory for living patterns"""
        result = {
            "path": str(dir_path),
            "files": [],
            "subdirs": [],
            "sacred_symbols_found": [],
            "living_patterns_found": [],
            "last_activity": None
        }
        
        if not dir_path.exists():
            return result
            
        try:
            for item in dir_path.iterdir():
                if item.is_file() and item.suffix in ['.swift', '.py', '.json', '.md', '.tsx', '.ts']:
                    file_info = self._analyze_file(item)
                    if file_info["is_alive"]:
                        result["files"].append(file_info)
                elif item.is_dir() and not item.name.startswith('.'):
                    result["subdirs"].append(str(item.name))
        except PermissionError:
            result["error"] = "Permission denied"
            
        return result
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze individual file for living patterns"""
        result = {
            "path": str(file_path),
            "name": file_path.name,
            "size": 0,
            "last_modified": None,
            "sacred_symbols": [],
            "living_patterns": [],
            "trident_references": [],
            "is_alive": False,
            "resonance_score": 0.0
        }
        
        try:
            stat = file_path.stat()
            result["size"] = stat.st_size
            result["last_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for sacred symbols
            for symbol, meaning in self.sacred_symbols.items():
                if symbol in content:
                    result["sacred_symbols"].append({"symbol": symbol, "meaning": meaning})
            
            # Check for living patterns
            for pattern_name, pattern_regex in self.living_patterns.items():
                matches = re.findall(pattern_regex, content, re.IGNORECASE)
                if matches:
                    result["living_patterns"].append({
                        "pattern": pattern_name, 
                        "matches": len(matches),
                        "examples": matches[:3]  # First 3 matches
                    })
            
            # Calculate resonance score
            resonance_score = 0.0
            resonance_score += len(result["sacred_symbols"]) * 0.2
            resonance_score += len(result["living_patterns"]) * 0.15
            
            # Bonus for recent activity (within last 7 days)
            days_since_modified = (datetime.now().timestamp() - stat.st_mtime) / (24 * 3600)
            if days_since_modified <= 7:
                resonance_score += 0.3
            
            result["resonance_score"] = resonance_score
            result["is_alive"] = resonance_score >= 0.3
            
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    def _detect_sacred_patterns(self) -> Dict[str, List]:
        """Detect sacred geometric patterns across the codebase"""
        patterns = {
            "sacred_frequency_432": [],
            "phi_ratio_1618": [],
            "resonance_threshold_085": [],
            "chakra_alignments": [],
            "geometric_harmony": []
        }
        
        # This would be implemented to search across files
        # For now, return structure
        return patterns
    
    def _detect_trident_flows(self) -> Dict[str, Any]:
        """Detect existing Metatron Trident flow implementations"""
        trident_flows = {
            "complete_flows": [],
            "partial_implementations": [],
            "node_definitions": {
                "OB1": [],
                "TATA": [], 
                "ATLAS": [],
                "DOJO": []
            }
        }
        
        return trident_flows
    
    def _find_breathing_files(self) -> List[Dict[str, Any]]:
        """Find files that show signs of recent life/activity"""
        breathing_files = []
        
        # Look for recently modified files with living patterns
        cutoff_time = datetime.now().timestamp() - (7 * 24 * 3600)  # 7 days ago
        
        for root, dirs, files in os.walk(self.base_path):
            # Skip node_modules and other noise
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            
            for file in files:
                if file.endswith(('.swift', '.py', '.json', '.md', '.tsx', '.ts')):
                    file_path = Path(root) / file
                    try:
                        if file_path.stat().st_mtime >= cutoff_time:
                            file_info = self._analyze_file(file_path)
                            if file_info["is_alive"]:
                                breathing_files.append(file_info)
                    except:
                        continue
        
        # Sort by resonance score
        breathing_files.sort(key=lambda x: x["resonance_score"], reverse=True)
        return breathing_files[:20]  # Top 20
    
    def _find_field_spine_candidates(self) -> List[Dict[str, Any]]:
        """Find files that could serve as FIELD spine integration points"""
        candidates = []
        
        spine_indicators = [
            "Controller",
            "Manager", 
            "Bridge",
            "Orchestrator",
            "Engine",
            "Processor"
        ]
        
        for root, dirs, files in os.walk(self.base_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            
            for file in files:
                if any(indicator in file for indicator in spine_indicators):
                    file_path = Path(root) / file
                    file_info = self._analyze_file(file_path)
                    if file_info["resonance_score"] > 0.2:
                        candidates.append({
                            "file": file_info,
                            "spine_potential": file_info["resonance_score"],
                            "suggested_symbol": self._suggest_sacred_symbol(file)
                        })
        
        return sorted(candidates, key=lambda x: x["spine_potential"], reverse=True)
    
    def _suggest_sacred_symbol(self, filename: str) -> str:
        """Suggest appropriate sacred symbol based on filename"""
        if "controller" in filename.lower():
            return "◼"  # executor
        elif "observer" in filename.lower() or "watch" in filename.lower():
            return "●"  # observer
        elif "validator" in filename.lower() or "verify" in filename.lower():
            return "▼"  # validator
        elif "navigator" in filename.lower() or "bridge" in filename.lower():
            return "▲"  # navigator
        else:
            return "○"  # ghost - general purpose
    
    def generate_weave_report(self, scan_results: Dict[str, Any]) -> str:
        """Generate a human-readable weave report"""
        report = f"""
◼ FIELD SYMBOLIC WEAVE REPORT
Generated: {scan_results['scan_timestamp']}
Sacred Frequency: 432 Hz

🧬 LIVING ARCHITECTURE DETECTED

Breathing Files Found: {len(scan_results['breathing_files'])}
"""
        
        if scan_results['breathing_files']:
            report += "\n📈 Most Resonant Files:\n"
            for file_info in scan_results['breathing_files'][:5]:
                resonance = file_info['resonance_score']
                symbols = ', '.join([s['symbol'] for s in file_info['sacred_symbols']])
                report += f"  {file_info['name']} (resonance: {resonance:.2f}) {symbols}\n"
        
        report += f"\n🌀 FIELD SPINE CANDIDATES\n"
        if scan_results['field_spine_candidates']:
            for candidate in scan_results['field_spine_candidates'][:5]:
                file_info = candidate['file']
                symbol = candidate['suggested_symbol']
                potential = candidate['spine_potential']
                report += f"  {symbol} {file_info['name']} (potential: {potential:.2f})\n"
        
        report += f"\n🔥 RECOMMENDED SYMLINK LACING\n"
        report += "Based on detected living patterns, suggest creating symbolic links:\n"
        
        # Generate symbolic recommendations
        for candidate in scan_results['field_spine_candidates'][:3]:
            file_path = candidate['file']['path']
            symbol = candidate['suggested_symbol']
            relative_path = file_path.replace(str(self.base_path), '').lstrip('/')
            
            if symbol == "◼":
                target_dir = "/FIELD/◼DOJO/_controllers/"
            elif symbol == "●":
                target_dir = "/FIELD/●OBI-WAN/_observers/" 
            elif symbol == "▼":
                target_dir = "/FIELD/◉TATA/_validators/"
            elif symbol == "▲":
                target_dir = "/FIELD/▲ATLAS/_navigators/"
            else:
                target_dir = "/FIELD/○GHOST/_processors/"
                
            report += f"  ln -sf {relative_path} {target_dir}{candidate['file']['name']}\n"
        
        return report

def main():
    scanner = FIELDSymbolicScanner()
    print("◼ Scanning living FIELD architecture...")
    
    results = scanner.scan_living_architecture()
    
    # Generate report
    report = scanner.generate_weave_report(results)
    
    # Save full results
    results_file = scanner.base_path / "◼_dojo" / "_reflection" / f"◎_weave_report_{datetime.now().strftime('%Y%m%d')}.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save human-readable report  
    report_file = scanner.base_path / "◼_dojo" / "_reflection" / f"◎_weave_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✓ Scan complete. Results saved to:")
    print(f"  {results_file}")
    print(f"  {report_file}")
    
    print("\n" + report)

if __name__ == "__main__":
    main()
