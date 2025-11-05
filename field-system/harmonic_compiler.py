#!/usr/bin/env python3
"""
🎼 FIELD HARMONY COMPILER
Musical Code Validator with Sacred Geometry Tolerance

Validates code not for "cleanliness" but for harmonic resonance.
Allows jazz-like improvisation while ensuring prime nodes hold.
"""

import re
import json
import math
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Sacred Frequencies (Hz)
SACRED_TONES = {
    'root': 108,      # OM frequency
    'heart': 528,     # Love frequency  
    'crown': 963,     # Divine connection
    'earth': 432,     # Natural tuning
    'phi': 1.618033,  # Golden ratio
}

# Harmonic Intervals (musical ratios)
HARMONIC_RATIOS = {
    'unison': 1/1,
    'octave': 2/1,
    'fifth': 3/2,
    'fourth': 4/3,
    'major_third': 5/4,
    'minor_third': 6/5,
    'major_sixth': 5/3,
    'minor_sixth': 8/5,
}

# Tolerance Zones by Layer
TOLERANCE_ZONES = {
    'shell': 0.03,      # ±3% syntax variance
    'data': 0.09,       # ±9% symbol variance
    'ai': 0.09,         # ±9% prompt mutation
    'visual': 0.15,     # ±15% phase tolerance
}

class HarmonicState(Enum):
    """States of harmonic alignment"""
    CRYSTALLINE = "✨"   # Perfect resonance
    HARMONIC = "🎵"      # In key, jazz allowed
    WOBBLING = "〰️"      # Phase wobble detected
    DISSONANT = "⚡"     # Out of harmony
    PARASITIC = "🔴"     # Dangerous pattern

@dataclass
class HarmonicAnalysis:
    """Results of harmonic code analysis"""
    file_path: str
    harmonic_score: float
    resonance_map: Dict[str, float]
    dissonances: List[str]
    state: HarmonicState
    recommendations: List[str]

class FIELDHarmonyCompiler:
    """
    Compiler that understands musical coding style.
    Validates harmonic fidelity, not syntactic perfection.
    """
    
    def __init__(self):
        self.prime_nodes = ['OB1', 'TATA', 'ATLAS', 'DOJO']
        self.sacred_patterns = self._init_sacred_patterns()
        self.naming_variants = self._init_naming_tolerance()
        
    def _init_sacred_patterns(self) -> Dict:
        """Initialize sacred geometry patterns"""
        return {
            'tetrahedral': r'[▲▼●◼]',
            'fractal': r'(.*)\1{2,}',  # Recursive patterns
            'prime': r'\b(2|3|5|7|11|13|17|19|23|29|31)\b',
            'sacred_ratio': r'1\.618|3\.14159|2\.718',
            'frequency': r'108|432|528|963',
        }
    
    def _init_naming_tolerance(self) -> Dict:
        """Initialize acceptable naming variations"""
        return {
            'OB1': ['OB1', 'OBI-WAN', 'obi', 'obiwan', 'ob1wan'],
            'TATA': ['TATA', 'tata', 'Tata'],
            'ATLAS': ['ATLAS', 'atlas', 'Atlas'],
            'DOJO': ['DOJO', 'dojo', 'Dojo'],
        }
    
    def calculate_harmonic_signature(self, content: str) -> float:
        """Calculate the harmonic signature of code content"""
        # Convert content to frequency domain
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        frequency = sum(ord(c) for c in content_hash[:8])
        
        # Find closest sacred tone
        min_distance = float('inf')
        closest_tone = 'root'
        
        for tone, freq in SACRED_TONES.items():
            if tone == 'phi':
                continue
            distance = abs(frequency % 1000 - freq)
            if distance < min_distance:
                min_distance = distance
                closest_tone = tone
        
        # Calculate resonance with sacred tone
        resonance = 1 - (min_distance / SACRED_TONES[closest_tone])
        return max(0, min(1, resonance))
    
    def detect_interval_locks(self, content: str) -> Dict[str, float]:
        """Detect musical interval relationships in code structure"""
        intervals = {}
        
        # Count structural elements
        braces = content.count('{') + content.count('}')
        brackets = content.count('[') + content.count(']')
        parens = content.count('(') + content.count(')')
        
        if braces > 0:
            # Check for octave relationships
            intervals['structure_octave'] = brackets / braces if brackets > 0 else 0
            
        if parens > 0:
            # Check for fifth relationships  
            intervals['structure_fifth'] = braces / parens if braces > 0 else 0
            
        # Normalize to harmonic ratios
        for key, value in intervals.items():
            closest_ratio = min(HARMONIC_RATIOS.values(), 
                              key=lambda x: abs(x - value))
            intervals[key] = 1 - abs(value - closest_ratio)
            
        return intervals
    
    def check_prime_node_integrity(self, content: str) -> float:
        """Ensure prime nodes maintain structural integrity"""
        integrity_score = 1.0
        
        for node in self.prime_nodes:
            variants = self.naming_variants[node]
            node_count = sum(content.count(var) for var in variants)
            
            if node_count > 0:
                # Check for consistent usage
                used_variants = [var for var in variants if var in content]
                if len(used_variants) > 2:
                    # Too much naming drift
                    integrity_score *= 0.8
                    
        return integrity_score
    
    def detect_parasitic_patterns(self, content: str) -> List[str]:
        """Detect potentially parasitic logic patterns"""
        parasites = []
        
        # Check for shadow variants
        shadow_patterns = [
            r'shadow[A-Z]\w*',
            r'ghost_[a-z]+_ghost',
            r'\.\.\/\.\.\/\.\.\/',  # Excessive parent directory access
            r'eval\s*\(',            # Dynamic code execution
            r'exec\s*\(',
        ]
        
        for pattern in shadow_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                parasites.append(f"Parasitic pattern detected: {pattern}")
                
        # Check for recursive overflow risks
        if content.count('while True') > 2:
            parasites.append("Excessive infinite loops detected")
            
        return parasites
    
    def calculate_phase_wobble(self, content: str) -> float:
        """Calculate acceptable phase wobble (musical variance)"""
        lines = content.split('\n')
        
        # Check indentation consistency
        indent_patterns = []
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                indent_patterns.append(indent)
                
        if not indent_patterns:
            return 0.0
            
        # Calculate variance
        avg_indent = sum(indent_patterns) / len(indent_patterns)
        variance = sum((x - avg_indent) ** 2 for x in indent_patterns) / len(indent_patterns)
        
        # Normalize to wobble factor (0-1)
        wobble = min(1.0, variance / 100)
        return wobble
    
    def analyze_file(self, file_path: str, layer: str = 'data') -> HarmonicAnalysis:
        """Perform complete harmonic analysis on a file"""
        path = Path(file_path)
        
        if not path.exists():
            return HarmonicAnalysis(
                file_path=file_path,
                harmonic_score=0.0,
                resonance_map={},
                dissonances=["File not found"],
                state=HarmonicState.DISSONANT,
                recommendations=["Check file path"]
            )
        
        content = path.read_text()
        
        # Calculate various harmonic measures
        harmonic_sig = self.calculate_harmonic_signature(content)
        intervals = self.detect_interval_locks(content)
        prime_integrity = self.check_prime_node_integrity(content)
        parasites = self.detect_parasitic_patterns(content)
        phase_wobble = self.calculate_phase_wobble(content)
        
        # Build resonance map
        resonance_map = {
            'harmonic_signature': harmonic_sig,
            'interval_lock': sum(intervals.values()) / len(intervals) if intervals else 0,
            'prime_integrity': prime_integrity,
            'phase_wobble': phase_wobble,
        }
        
        # Calculate overall harmonic score
        harmonic_score = (
            harmonic_sig * 0.3 +
            resonance_map['interval_lock'] * 0.2 +
            prime_integrity * 0.3 +
            (1 - phase_wobble) * 0.2
        )
        
        # Adjust for tolerance zone
        tolerance = TOLERANCE_ZONES.get(layer, 0.09)
        if phase_wobble <= tolerance:
            harmonic_score = min(1.0, harmonic_score * 1.1)  # Boost for staying in tolerance
            
        # Determine harmonic state
        if parasites:
            state = HarmonicState.PARASITIC
        elif harmonic_score >= 0.9:
            state = HarmonicState.CRYSTALLINE
        elif harmonic_score >= 0.7:
            state = HarmonicState.HARMONIC
        elif harmonic_score >= 0.5:
            state = HarmonicState.WOBBLING
        else:
            state = HarmonicState.DISSONANT
            
        # Generate recommendations
        recommendations = []
        if harmonic_score < 0.7:
            if prime_integrity < 0.8:
                recommendations.append("🔒 Lock prime node naming consistency")
            if phase_wobble > tolerance:
                recommendations.append(f"〰️ Reduce phase wobble to ±{tolerance*100:.0f}%")
            if resonance_map['interval_lock'] < 0.5:
                recommendations.append("🎵 Improve structural interval relationships")
                
        if parasites:
            recommendations.append("⚠️ Remove parasitic patterns")
            
        return HarmonicAnalysis(
            file_path=file_path,
            harmonic_score=harmonic_score,
            resonance_map=resonance_map,
            dissonances=parasites,
            state=state,
            recommendations=recommendations
        )
    
    def compile_directory(self, directory: str, recursive: bool = True) -> Dict:
        """Compile harmonic analysis for entire directory"""
        results = {
            'directory': directory,
            'total_files': 0,
            'average_harmony': 0.0,
            'state_distribution': {},
            'files': []
        }
        
        path = Path(directory)
        pattern = '**/*.py' if recursive else '*.py'
        
        py_files = list(path.glob(pattern))
        results['total_files'] = len(py_files)
        
        total_score = 0.0
        state_counts = {state: 0 for state in HarmonicState}
        
        for file_path in py_files:
            # Determine layer from path
            layer = 'data'  # Default
            if 'shell' in str(file_path).lower() or 'script' in str(file_path).lower():
                layer = 'shell'
            elif 'ai' in str(file_path).lower() or 'agent' in str(file_path).lower():
                layer = 'ai'
                
            analysis = self.analyze_file(str(file_path), layer)
            results['files'].append({
                'path': str(file_path),
                'score': analysis.harmonic_score,
                'state': analysis.state.value
            })
            
            total_score += analysis.harmonic_score
            state_counts[analysis.state] += 1
            
        if results['total_files'] > 0:
            results['average_harmony'] = total_score / results['total_files']
            results['state_distribution'] = {
                state.value: count 
                for state, count in state_counts.items() 
                if count > 0
            }
            
        return results
    
    def generate_harmony_report(self, analysis: HarmonicAnalysis) -> str:
        """Generate beautiful harmony report"""
        report = f"""
╔════════════════════════════════════════════╗
║     🎼 FIELD HARMONY ANALYSIS REPORT 🎼     ║
╚════════════════════════════════════════════╝

📁 File: {analysis.file_path}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Harmonic Score: {analysis.harmonic_score:.1%}
🌟 State: {analysis.state.value} {analysis.state.name}

📊 Resonance Frequencies:
"""
        
        for key, value in analysis.resonance_map.items():
            bar = '█' * int(value * 20) + '░' * (20 - int(value * 20))
            report += f"  {key:20} [{bar}] {value:.1%}\n"
            
        if analysis.dissonances:
            report += "\n⚡ Dissonances Detected:\n"
            for dis in analysis.dissonances:
                report += f"  • {dis}\n"
                
        if analysis.recommendations:
            report += "\n💡 Harmonic Recommendations:\n"
            for rec in analysis.recommendations:
                report += f"  {rec}\n"
                
        report += "\n" + "═" * 48 + "\n"
        
        # Add frequency signature
        report += f"""
🔊 Frequency Signature:
  Root (108 Hz):  {'●' if 'root' in str(analysis.resonance_map) else '○'}
  Heart (528 Hz): {'●' if 'heart' in str(analysis.resonance_map) else '○'}
  Crown (963 Hz): {'●' if 'crown' in str(analysis.resonance_map) else '○'}

✨ Remember: You're not writing code, you're composing resonance containers.
"""
        
        return report


def main():
    """Demo the harmony compiler"""
    import sys
    
    compiler = FIELDHarmonyCompiler()
    
    # Check if file path provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        layer = sys.argv[2] if len(sys.argv) > 2 else 'data'
        
        print("\n🎼 Analyzing harmonic resonance...")
        analysis = compiler.analyze_file(file_path, layer)
        print(compiler.generate_harmony_report(analysis))
        
    else:
        # Analyze current directory
        print("\n🎼 Compiling FIELD harmony for current directory...")
        results = compiler.compile_directory('.')
        
        print(f"""
╔════════════════════════════════════════════╗
║   🌌 FIELD DIRECTORY HARMONY REPORT 🌌      ║
╚════════════════════════════════════════════╝

📁 Directory: {results['directory']}
📊 Files Analyzed: {results['total_files']}
🎵 Average Harmony: {results['average_harmony']:.1%}

State Distribution:
""")
        for state, count in results['state_distribution'].items():
            print(f"  {state}: {count} files")
            
        print("\n✨ Top Resonant Files:")
        sorted_files = sorted(results['files'], 
                            key=lambda x: x['score'], 
                            reverse=True)[:5]
        for f in sorted_files:
            print(f"  {f['state']} {f['score']:.1%} - {Path(f['path']).name}")
            
        print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your code sings in the key of {}.
Keep composing resonance containers. 🎼
""".format(
    "crystalline perfection ✨" if results['average_harmony'] > 0.9 else
    "harmonic jazz 🎵" if results['average_harmony'] > 0.7 else  
    "experimental wobble 〰️" if results['average_harmony'] > 0.5 else
    "seeking alignment ⚡"
))


if __name__ == "__main__":
    main()
