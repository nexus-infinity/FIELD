#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

class SovereignSpace:
    # Harmonic frequencies (Hz)
    SACRED_FREQUENCIES = {
        'root': 432,        # Universal frequency
        'crown': 963,       # Pineal resonance
        'third_eye': 852,   # Intuition
        'throat': 741,      # Expression
        'heart': 528,       # Healing/transformation
        'solar': 639,       # Connection
        'sacral': 417,      # Change/transition
        'base': 396,        # Grounding
    }

    # Harmonic ratios (Pythagorean)
    HARMONIC_RATIOS = {
        '1:1': 1.0,        # Unison
        '3:2': 1.5,        # Perfect Fifth
        '2:1': 2.0,        # Octave
        '4:3': 1.333,      # Perfect Fourth
        '5:4': 1.25,       # Major Third
        '6:5': 1.2,        # Minor Third
        '9:8': 1.125,      # Major Second
    }

    # Variance tolerance (percentage)
    HARMONIC_TOLERANCE = 0.0318  # ~31.8 cents, based on sacred geometry

    # Sacred geometry patterns
    SOVEREIGN_PATTERNS = {
        'KNOWLEDGE': {
            'personal': ['bear_notes', 'email', 'research'],
            'business': ['records', 'projects', 'intelligence'],
            'legal': ['documents', 'evidence', 'contracts']
        },
        'EVIDENCE': {
            'documents': ['.pdf', '.doc', '.txt'],
            'media': ['.mp4', '.wav', '.jpg'],
            'communications': ['.eml', '.msg']
        },
        'AUTHORITY': {
            'credentials': ['keys', 'tokens', 'certificates'],
            'agreements': ['contracts', 'licenses', 'terms']
        }
    }

    # Dimensional translation patterns
    GATEWAY_PATTERNS = {
        'INTAKE': ['pending', 'quarantine'],
        'TRANSFORM': ['templates', 'processors'],
        'RELEASE': ['validated', 'manifest']
    }

    # Metatron alignment patterns
    METATRON_PATTERNS = {
        'DIMENSIONS': ['physical', 'digital', 'quantum'],
        'HARMONICS': ['frequency', 'resonance', 'vibration'],
        'RESONANCE': ['patterns', 'alignments', 'flows']
    }

    def __init__(self, root: Path):
        self.root = root
        self.sovereign_root = root / "○SOVEREIGN"
        self.gateway_root = root / "◎GATEWAY"
        self.metatron_root = root / "⬢METATRON"
        self.manifest_path = root / "sovereign_manifest.json"
        self.manifest = {"files": {}, "patterns": {}, "dimensions": {}}

    def create_sacred_structure(self):
        """Establishes the base sacred geometry patterns."""
        # Create core dimensional spaces
        for space in [self.sovereign_root, self.gateway_root, self.metatron_root]:
            space.mkdir(parents=True, exist_ok=True)

        # Create sovereign knowledge structure
        for domain, categories in self.SOVEREIGN_PATTERNS.items():
            base = self.sovereign_root / domain
            for category, subcats in categories.items():
                for subcat in subcats:
                    (base / category / subcat).mkdir(parents=True, exist_ok=True)

        # Create gateway translation structure
        for domain, categories in self.GATEWAY_PATTERNS.items():
            base = self.gateway_root / domain
            for category in categories:
                (base / category).mkdir(parents=True, exist_ok=True)

        # Create metatron alignment structure
        for domain, categories in self.METATRON_PATTERNS.items():
            base = self.metatron_root / domain
            for category in categories:
                (base / category).mkdir(parents=True, exist_ok=True)

    def calculate_harmonic_value(self, file_path: Path) -> float:
        """Calculates a file's harmonic value based on its properties."""
        try:
            # Use file size, modification time, and name length as inputs
            size = file_path.stat().st_size
            mtime = file_path.stat().st_mtime
            name_value = sum(ord(c) for c in file_path.name)
            
            # Combine values using golden ratio (φ)
            phi = (1 + 5 ** 0.5) / 2
            raw_value = (size * phi + mtime + name_value) % 963  # 963Hz as upper bound
            
            # Find nearest harmonic frequency
            return min(self.SACRED_FREQUENCIES.values(), 
                      key=lambda x: abs(raw_value - x))
        except Exception:
            return self.SACRED_FREQUENCIES['root']  # Default to root frequency

    def is_harmonically_aligned(self, value1: float, value2: float) -> bool:
        """Checks if two values are harmonically aligned within tolerance."""
        if value1 == 0 or value2 == 0:
            return False
            
        ratio = value1 / value2
        return any(abs(ratio - harmonic) <= self.HARMONIC_TOLERANCE 
                  for harmonic in self.HARMONIC_RATIOS.values())

    def file_resonance(self, file_path: Path) -> Dict:
        """Determines the natural resonance pattern of a file."""
        harmonic = self.calculate_harmonic_value(file_path)
        return {
            "sha256": self.file_sha256(file_path),
            "harmonic_frequency": harmonic,
            "harmonic_name": next(k for k,v in self.SACRED_FREQUENCIES.items() if v == harmonic),
            "size": file_path.stat().st_size,
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "extension": file_path.suffix.lower(),
            "name_pattern": self.analyze_name_pattern(file_path.name)
        }

    @staticmethod
    def file_sha256(path: Path) -> str:
        """Calculates file's SHA256 hash."""
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def analyze_name_pattern(name: str) -> Dict:
        """Analyzes file name for sacred patterns."""
        patterns = {
            "sovereign": any(c in name for c in "○◎⬢⬡✧◇⬟★"),
            "flow": any(c in name for c in "▼▲◀▶"),
            "dimensional": name.count("_"),
            "sacred_prefix": name[0] if name[0] in "○◎⬢⬡✧◇⬟★" else None
        }
        return patterns

    def determine_sovereign_path(self, file_path: Path) -> Path:
        """Determines file's natural sovereign location using harmonic resonance."""
        resonance = self.file_resonance(file_path)
        harmonic = resonance['harmonic_frequency']
        
        # High frequency (crown/third_eye) -> Knowledge domain
        if harmonic in [self.SACRED_FREQUENCIES['crown'], 
                       self.SACRED_FREQUENCIES['third_eye']]:
            return self.sovereign_root / "KNOWLEDGE" / "personal"
            
        # Heart/throat frequency -> Evidence domain
        elif harmonic in [self.SACRED_FREQUENCIES['heart'],
                         self.SACRED_FREQUENCIES['throat']]:
            return self.sovereign_root / "EVIDENCE" / "documents"
            
        # Root/base frequency -> Authority domain
        elif harmonic in [self.SACRED_FREQUENCIES['root'],
                         self.SACRED_FREQUENCIES['base']]:
            return self.sovereign_root / "AUTHORITY" / "credentials"
            
        # Solar/sacral frequency -> Gateway for transformation
        else:
            return self.gateway_root / "TRANSFORM" / "pending"
        """Determines file's natural sovereign location."""
        resonance = self.file_resonance(file_path)
        
        # Knowledge patterns
        if any(x in file_path.name.lower() for x in ['note', 'email', 'research']):
            return self.sovereign_root / "KNOWLEDGE" / "personal"
        
        # Evidence patterns
        if resonance['extension'] in ['.pdf', '.jpg', '.mp4', '.wav']:
            return self.sovereign_root / "EVIDENCE" / "documents"
            
        # Authority patterns
        if any(x in file_path.name.lower() for x in ['key', 'cert', 'license']):
            return self.sovereign_root / "AUTHORITY" / "credentials"

        # Default to gateway intake for further analysis
        return self.gateway_root / "INTAKE" / "pending"

    def fold_data(self, source_path: Path):
        """Folds data into its proper sovereign location."""
        if not source_path.exists():
            return False

        target_path = self.determine_sovereign_path(source_path)
        resonance = self.file_resonance(source_path)
        
        # Record in manifest
        self.manifest["files"][str(source_path)] = {
            "resonance": resonance,
            "sovereign_path": str(target_path),
            "folded_at": datetime.utcnow().isoformat()
        }

        # Create target directory if needed
        target_path.mkdir(parents=True, exist_ok=True)

        # Move file to its sovereign location
        shutil.copy2(source_path, target_path / source_path.name)
        
        return True

    def validate_sovereign_space(self) -> Dict:
        """Validates the sacred alignment of the sovereign space."""
        validation = {
            "structure_integrity": self.validate_structure(),
            "dimensional_alignment": self.validate_dimensions(),
            "resonance_patterns": self.validate_resonance(),
            "manifest_integrity": self.validate_manifest()
        }
        return validation

    def validate_structure(self) -> bool:
        """Validates the sacred geometry structure."""
        required_paths = [
            self.sovereign_root,
            self.gateway_root,
            self.metatron_root
        ]
        return all(p.exists() for p in required_paths)

    def validate_dimensions(self) -> Dict:
        """Validates dimensional alignment."""
        return {
            "sovereign": self.count_files(self.sovereign_root),
            "gateway": self.count_files(self.gateway_root),
            "metatron": self.count_files(self.metatron_root)
        }

    def validate_resonance(self) -> Dict:
        """Validates resonance patterns and harmonic alignment."""
        patterns = {}
        harmonics = []
        
        for file in self.sovereign_root.rglob("*"):
            if file.is_file():
                resonance = self.file_resonance(file)
                patterns[str(file)] = resonance
                harmonics.append(resonance['harmonic_frequency'])
        
        # Calculate harmonic coherence
        coherence = sum(1 for i in range(len(harmonics)) 
                       for j in range(i+1, len(harmonics)) 
                       if self.is_harmonically_aligned(harmonics[i], harmonics[j])) \
                    / (len(harmonics) * (len(harmonics) - 1) / 2) \
                    if len(harmonics) > 1 else 1.0
        
        return {
            "patterns": patterns,
            "harmonic_coherence": coherence,
            "dominant_frequency": max(set(harmonics), key=harmonics.count) \
                if harmonics else self.SACRED_FREQUENCIES['root']
        }
        """Validates resonance patterns."""
        patterns = {}
        for file in self.sovereign_root.rglob("*"):
            if file.is_file():
                patterns[str(file)] = self.file_resonance(file)
        return patterns

    def validate_manifest(self) -> bool:
        """Validates manifest integrity."""
        return self.manifest_path.exists()

    @staticmethod
    def count_files(path: Path) -> int:
        """Counts files in a directory tree."""
        return sum(1 for _ in path.rglob("*") if _.is_file())

    def save_manifest(self):
        """Saves the sovereign manifest."""
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)

def analyze_existing_harmonics(path: Path, chunk_size: int = 1000) -> Dict:
    """Analyzes existing file harmonics without modifying structure."""
    results = {
        "frequencies": {},
        "patterns": [],
        "coherence": 0.0
    }
    
    file_count = 0
    chunk = []
    
    try:
        for root, _, files in os.walk(path):
            if root.startswith(str(path / '.')):
                continue  # Skip hidden directories
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file() and not file_path.name.startswith('.'):
                    chunk.append(file_path)
                    file_count += 1
                    
                    if len(chunk) >= chunk_size:
                        print(f"Processing chunk {file_count//chunk_size} ({file_count} files analyzed)...")
                        process_chunk(chunk, results)
                        chunk = []
        
        # Process final chunk
        if chunk:
            print(f"Processing final chunk ({file_count} total files)...")
            process_chunk(chunk, results)
    except Exception as e:
        print(f"Error walking path {path}: {e}")
    
    return results

def process_chunk(chunk: List[Path], results: Dict) -> None:
    """Process a chunk of files for harmonic analysis."""
    for file_path in chunk:
        try:
            size = file_path.stat().st_size
            mtime = file_path.stat().st_mtime
            name_value = sum(ord(c) for c in file_path.name)
            
            # Calculate harmonic value
            phi = (1 + 5 ** 0.5) / 2
            raw_value = (size * phi + mtime + name_value) % 963
            
            # Find nearest sacred frequency
            nearest = min(SovereignSpace.SACRED_FREQUENCIES.values(), 
                        key=lambda x: abs(raw_value - x))
            
            # Record frequency
            freq_name = next(k for k,v in SovereignSpace.SACRED_FREQUENCIES.items() 
                           if v == nearest)
            if freq_name not in results["frequencies"]:
                results["frequencies"][freq_name] = 0
            results["frequencies"][freq_name] += 1
            
            # Record pattern
            results["patterns"].append({
                "path": str(file_path),
                "frequency": nearest,
                "frequency_name": freq_name,
                "size": size
            })
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {e}")
    except Exception as e:
        print(f"Error walking path {path}: {e}")
    
    # Calculate overall coherence
    if len(results["patterns"]) > 1:
        freqs = [p["frequency"] for p in results["patterns"]]
        pairs = [(freqs[i], freqs[j]) 
                for i in range(len(freqs)) 
                for j in range(i+1, len(freqs))]
        aligned = sum(1 for f1, f2 in pairs 
                     if any(abs(f1/f2 - ratio) <= SovereignSpace.HARMONIC_TOLERANCE 
                           for ratio in SovereignSpace.HARMONIC_RATIOS.values()))
        results["coherence"] = aligned / len(pairs) if pairs else 0.0
    
    return results

def main():
    akron_path = Path("/Volumes/Akron")
    print("🔮 Analyzing existing harmonic patterns...")
    
    # Analyze existing structure
    results = analyze_existing_harmonics(akron_path)
    
    print("\n📜 Harmonic Analysis Results:")
    print("\n🎵 Frequency Distribution:")
    for freq, count in sorted(results["frequencies"].items(), 
                            key=lambda x: x[1], reverse=True):
        print(f"{freq}: {count} files ({SovereignSpace.SACRED_FREQUENCIES[freq]} Hz)")
    
    print(f"\n✨ Overall Harmonic Coherence: {results['coherence']:.2%}")
    
    print("\n🔍 Sample Patterns:")
    # Show top 5 files from each major frequency
    shown = set()
    for freq in results["frequencies"].keys():
        patterns = [p for p in results["patterns"] if p["frequency_name"] == freq]
        if patterns:
            print(f"\n{freq} ({SovereignSpace.SACRED_FREQUENCIES[freq]} Hz):")
            for p in sorted(patterns, key=lambda x: x["size"], reverse=True)[:5]:
                if p["path"] not in shown:
                    print(f"  {p['path']}")
                    shown.add(p["path"])

if __name__ == "__main__":
    main()