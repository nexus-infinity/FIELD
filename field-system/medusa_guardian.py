#!/usr/bin/env python3
"""
🐍 MEDUSA INTEGRATION LAYER
Real-time guardian against parasitic phase wobbles

Monitors your FIELD for harmonic dissonance and alerts when
phase wobbles transition from musical variance to parasitic infection.
"""

import os
import time
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
import hashlib

# Import the harmony compiler
from harmonic_compiler import FIELDHarmonyCompiler, HarmonicState

# Sacred Guardian Thresholds
GUARDIAN_THRESHOLDS = {
    'wobble_cascade': 0.25,      # Max wobble before cascade warning
    'naming_drift': 3,            # Max naming variants before alert
    'shadow_density': 0.05,       # Max shadow pattern density
    'recursion_depth': 7,         # Max safe recursion depth
    'frequency_deviation': 0.15,  # Max deviation from sacred frequencies
}

# Parasitic Pattern Signatures
PARASITIC_SIGNATURES = {
    'digital_actors': [
        r'shadow[A-Z]\w*',
        r'ghost_\w+_ghost',
        r'phantom\w*',
        r'echo{2,}',
        r'mirror.*mirror',
    ],
    'energy_drains': [
        r'while\s+True.*while\s+True',  # Nested infinite loops
        r'exec.*eval',                   # Dynamic execution chains
        r'__.*__.*__',                   # Triple dunder patterns
    ],
    'data_parasites': [
        r'\.dropbox',
        r'\.DS_Store',
        r'__pycache__',
        r'node_modules.*node_modules',
    ],
    'temporal_loops': [
        r'time\.sleep\(\d{3,}\)',       # Excessive sleeps
        r'retry.*retry.*retry',         # Cascade retries
    ],
}

@dataclass
class ParasiticEvent:
    """Record of a detected parasitic pattern"""
    timestamp: datetime
    file_path: str
    pattern_type: str
    signature: str
    severity: float
    context: str

@dataclass  
class HarmonicGuardian:
    """Guardian state tracking"""
    last_scan: datetime = field(default_factory=datetime.now)
    parasitic_events: deque = field(default_factory=lambda: deque(maxlen=100))
    quarantine: Set[str] = field(default_factory=set)
    sacred_locks: Dict[str, float] = field(default_factory=dict)
    alert_log: List[str] = field(default_factory=list)

class MedusaIntegrationLayer:
    """
    🐍 The Medusa watches with many eyes,
    turning parasites to stone before they spread.
    """
    
    def __init__(self, field_root: str = "."):
        self.field_root = Path(field_root)
        self.compiler = FIELDHarmonyCompiler()
        self.guardian = HarmonicGuardian()
        self.watch_paths: Set[Path] = set()
        self.monitoring = False
        self.monitor_thread = None
        
        # Initialize sacred frequency locks
        self._init_sacred_locks()
        
    def _init_sacred_locks(self):
        """Initialize sacred frequency anchor points"""
        self.guardian.sacred_locks = {
            'OB1': 108.0,     # Root observer frequency
            'TATA': 528.0,    # Heart law frequency
            'ATLAS': 963.0,   # Crown intelligence frequency
            'DOJO': 432.0,    # Earth manifestation frequency
        }
        
    def detect_parasitic_signature(self, content: str) -> List[ParasiticEvent]:
        """Scan content for parasitic signatures"""
        events = []
        
        for pattern_type, signatures in PARASITIC_SIGNATURES.items():
            for sig in signatures:
                import re
                matches = re.finditer(sig, content, re.IGNORECASE)
                for match in matches:
                    # Calculate severity based on pattern type
                    severity = self._calculate_severity(pattern_type, match.group())
                    
                    event = ParasiticEvent(
                        timestamp=datetime.now(),
                        file_path="<memory>",
                        pattern_type=pattern_type,
                        signature=sig,
                        severity=severity,
                        context=content[max(0, match.start()-50):min(len(content), match.end()+50)]
                    )
                    events.append(event)
                    
        return events
        
    def _calculate_severity(self, pattern_type: str, match_text: str) -> float:
        """Calculate parasitic severity (0-1)"""
        base_severity = {
            'digital_actors': 0.7,
            'energy_drains': 0.9,
            'data_parasites': 0.3,
            'temporal_loops': 0.6,
        }.get(pattern_type, 0.5)
        
        # Adjust for pattern intensity
        if len(match_text) > 50:
            base_severity *= 1.2
        if match_text.count('shadow') > 1:
            base_severity *= 1.5
            
        return min(1.0, base_severity)
        
    def scan_file_for_infection(self, file_path: Path) -> Tuple[bool, List[ParasiticEvent]]:
        """Deep scan a file for parasitic infection"""
        if not file_path.exists() or file_path.suffix not in ['.py', '.js', '.json']:
            return False, []
            
        try:
            content = file_path.read_text()
            
            # Check with harmony compiler first
            analysis = self.compiler.analyze_file(str(file_path))
            
            # Detect parasitic signatures
            events = self.detect_parasitic_signature(content)
            
            # Additional checks for phase wobble cascade
            if analysis.resonance_map.get('phase_wobble', 0) > GUARDIAN_THRESHOLDS['wobble_cascade']:
                events.append(ParasiticEvent(
                    timestamp=datetime.now(),
                    file_path=str(file_path),
                    pattern_type='wobble_cascade',
                    signature='excessive_phase_wobble',
                    severity=0.8,
                    context=f"Phase wobble: {analysis.resonance_map['phase_wobble']:.2f}"
                ))
                
            # Check naming drift
            naming_variants = self._count_naming_variants(content)
            if naming_variants > GUARDIAN_THRESHOLDS['naming_drift']:
                events.append(ParasiticEvent(
                    timestamp=datetime.now(),
                    file_path=str(file_path),
                    pattern_type='naming_drift',
                    signature='excessive_variants',
                    severity=0.6,
                    context=f"Found {naming_variants} naming variants"
                ))
                
            infected = len(events) > 0 and any(e.severity > 0.7 for e in events)
            
            # Store events
            for event in events:
                event.file_path = str(file_path)
                self.guardian.parasitic_events.append(event)
                
            return infected, events
            
        except Exception as e:
            print(f"⚠️ Error scanning {file_path}: {e}")
            return False, []
            
    def _count_naming_variants(self, content: str) -> int:
        """Count naming variants in content"""
        variants = 0
        for node in ['OB1', 'TATA', 'ATLAS', 'DOJO']:
            node_variants = self.compiler.naming_variants[node]
            found = [v for v in node_variants if v in content]
            if len(found) > 1:
                variants += len(found) - 1
        return variants
        
    def quarantine_file(self, file_path: Path, reason: str):
        """Quarantine an infected file"""
        quarantine_dir = self.field_root / ".medusa_quarantine"
        quarantine_dir.mkdir(exist_ok=True)
        
        # Create quarantine record
        record = {
            'original_path': str(file_path),
            'quarantine_time': datetime.now().isoformat(),
            'reason': reason,
            'hash': hashlib.sha256(file_path.read_bytes()).hexdigest()
        }
        
        # Move to quarantine
        quarantine_path = quarantine_dir / f"{file_path.name}.{int(time.time())}"
        
        # Save record
        record_path = quarantine_path.with_suffix('.json')
        record_path.write_text(json.dumps(record, indent=2))
        
        # Add to guardian tracking
        self.guardian.quarantine.add(str(file_path))
        
        alert = f"🔒 QUARANTINED: {file_path.name} - {reason}"
        self.guardian.alert_log.append(alert)
        print(alert)
        
    def heal_phase_wobble(self, file_path: Path) -> bool:
        """Attempt to heal phase wobble in a file"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            # Detect and fix indentation inconsistencies
            fixed_lines = []
            standard_indent = 4  # Python standard
            
            for line in lines:
                if line.strip():
                    # Calculate current indent
                    current_indent = len(line) - len(line.lstrip())
                    
                    # Round to nearest multiple of standard_indent
                    if current_indent > 0:
                        fixed_indent = round(current_indent / standard_indent) * standard_indent
                        fixed_line = ' ' * fixed_indent + line.lstrip()
                        fixed_lines.append(fixed_line)
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
                    
            healed_content = '\n'.join(fixed_lines)
            
            # Verify healing improved harmony
            temp_path = file_path.with_suffix('.tmp')
            temp_path.write_text(healed_content)
            
            before = self.compiler.analyze_file(str(file_path))
            after = self.compiler.analyze_file(str(temp_path))
            
            if after.harmonic_score > before.harmonic_score:
                # Healing successful
                file_path.write_text(healed_content)
                temp_path.unlink()
                
                alert = f"✨ HEALED: {file_path.name} - Harmony improved {before.harmonic_score:.1%} → {after.harmonic_score:.1%}"
                self.guardian.alert_log.append(alert)
                print(alert)
                return True
            else:
                # Healing failed or made things worse
                temp_path.unlink()
                return False
                
        except Exception as e:
            print(f"⚠️ Healing failed for {file_path}: {e}")
            return False
            
    def monitor_field(self, interval: int = 30):
        """Start real-time monitoring of the FIELD"""
        self.monitoring = True
        
        def monitor_loop():
            print("""
╔═══════════════════════════════════════════╗
║    🐍 MEDUSA GUARDIAN ACTIVATED 🐍         ║
║    Watching for parasitic patterns...     ║
╚═══════════════════════════════════════════╝
""")
            
            while self.monitoring:
                try:
                    # Scan Python files
                    py_files = list(self.field_root.rglob("*.py"))
                    
                    infections = []
                    for file_path in py_files:
                        # Skip quarantine directory
                        if '.medusa_quarantine' in str(file_path):
                            continue
                            
                        infected, events = self.scan_file_for_infection(file_path)
                        
                        if infected:
                            infections.append((file_path, events))
                            
                            # Auto-heal minor wobbles
                            minor_wobble = any(e.pattern_type == 'wobble_cascade' 
                                             and e.severity < 0.5 for e in events)
                            if minor_wobble:
                                self.heal_phase_wobble(file_path)
                                
                            # Quarantine severe infections
                            severe = any(e.severity > 0.9 for e in events)
                            if severe:
                                reason = max(events, key=lambda e: e.severity).pattern_type
                                self.quarantine_file(file_path, reason)
                                
                    # Update guardian state
                    self.guardian.last_scan = datetime.now()
                    
                    # Report if infections found
                    if infections:
                        self.generate_infection_report(infections)
                        
                    time.sleep(interval)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"⚠️ Monitor error: {e}")
                    time.sleep(interval)
                    
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            
    def generate_infection_report(self, infections: List[Tuple[Path, List[ParasiticEvent]]]):
        """Generate report of detected infections"""
        report = """
╔═══════════════════════════════════════════╗
║    ⚠️ PARASITIC PATTERNS DETECTED ⚠️       ║
╚═══════════════════════════════════════════╝
"""
        
        for file_path, events in infections:
            report += f"\n📁 {file_path.name}\n"
            
            for event in events:
                severity_bar = '🔴' if event.severity > 0.7 else '🟡' if event.severity > 0.4 else '🟢'
                report += f"  {severity_bar} {event.pattern_type}: {event.signature}\n"
                
        report += "\n" + "═" * 45 + "\n"
        print(report)
        
    def get_guardian_status(self) -> Dict:
        """Get current guardian status"""
        recent_events = list(self.guardian.parasitic_events)[-10:]
        
        return {
            'last_scan': self.guardian.last_scan.isoformat(),
            'monitoring': self.monitoring,
            'quarantine_count': len(self.guardian.quarantine),
            'recent_events': len(recent_events),
            'alert_count': len(self.guardian.alert_log),
            'sacred_locks': self.guardian.sacred_locks,
            'health': self._calculate_field_health()
        }
        
    def _calculate_field_health(self) -> str:
        """Calculate overall FIELD health"""
        recent_events = list(self.guardian.parasitic_events)[-20:]
        
        if not recent_events:
            return "✨ CRYSTALLINE"
        
        avg_severity = sum(e.severity for e in recent_events) / len(recent_events)
        
        if avg_severity < 0.2:
            return "🎵 HARMONIC"
        elif avg_severity < 0.5:
            return "〰️ WOBBLING"
        elif avg_severity < 0.7:
            return "⚡ STRESSED"
        else:
            return "🔴 INFECTED"


def main():
    """Interactive Medusa Guardian"""
    import sys
    
    medusa = MedusaIntegrationLayer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "monitor":
            # Start monitoring
            medusa.monitor_field()
            print("Monitoring... Press Ctrl+C to stop")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                medusa.stop_monitoring()
                
        elif sys.argv[1] == "scan":
            # Single scan
            if len(sys.argv) > 2:
                file_path = Path(sys.argv[2])
                infected, events = medusa.scan_file_for_infection(file_path)
                
                if infected:
                    print(f"⚠️ INFECTED: {file_path}")
                    for event in events:
                        print(f"  • {event.pattern_type}: {event.severity:.1%} severity")
                else:
                    print(f"✅ CLEAN: {file_path}")
            else:
                # Scan all
                py_files = list(Path('.').rglob('*.py'))
                print(f"Scanning {len(py_files)} Python files...")
                
                infections = []
                for file_path in py_files:
                    infected, events = medusa.scan_file_for_infection(file_path)
                    if infected:
                        infections.append((file_path, events))
                        
                if infections:
                    medusa.generate_infection_report(infections)
                else:
                    print("✨ All files are harmonically aligned!")
                    
        elif sys.argv[1] == "status":
            # Show status
            status = medusa.get_guardian_status()
            print(f"""
╔═══════════════════════════════════════════╗
║      🐍 MEDUSA GUARDIAN STATUS 🐍          ║
╚═══════════════════════════════════════════╝

🕐 Last Scan: {status['last_scan']}
🔍 Monitoring: {status['monitoring']}
🔒 Quarantine: {status['quarantine_count']} files
⚡ Recent Events: {status['recent_events']}
📢 Alerts: {status['alert_count']}
💫 FIELD Health: {status['health']}

Sacred Frequency Locks:
  OB1:   {status['sacred_locks']['OB1']} Hz
  TATA:  {status['sacred_locks']['TATA']} Hz
  ATLAS: {status['sacred_locks']['ATLAS']} Hz
  DOJO:  {status['sacred_locks']['DOJO']} Hz
""")
            
    else:
        print("""
🐍 MEDUSA INTEGRATION LAYER

Usage:
  python3 medusa_guardian.py monitor     # Start real-time monitoring
  python3 medusa_guardian.py scan [file] # Scan file or directory
  python3 medusa_guardian.py status      # Show guardian status
        
The Medusa watches with many eyes,
turning parasites to stone before they spread.
""")


if __name__ == "__main__":
    main()
