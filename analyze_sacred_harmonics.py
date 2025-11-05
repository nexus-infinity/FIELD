#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Dict, List

# Sacred frequencies (Hz)
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
}

# Variance tolerance
HARMONIC_TOLERANCE = 0.0318  # ~31.8 cents

def analyze_file_harmonics(file_path: Path) -> Dict:
    """Calculate harmonic properties of a file."""
    try:
        # Get file properties
        stats = file_path.stat()
        size = stats.st_size
        mtime = stats.st_mtime
        name_value = sum(ord(c) for c in file_path.name)
        
        # Calculate using golden ratio (φ)
        phi = (1 + 5 ** 0.5) / 2
        raw_value = (size * phi + mtime + name_value) % 963
        
        # Find nearest sacred frequency
        nearest = min(SACRED_FREQUENCIES.values(), 
                     key=lambda x: abs(raw_value - x))
        freq_name = next(k for k,v in SACRED_FREQUENCIES.items() 
                        if v == nearest)
        
        return {
            "path": str(file_path),
            "frequency": nearest,
            "frequency_name": freq_name,
            "size": size
        }
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None

def process_directory(path: Path, results: Dict) -> None:
    """Process a directory for harmonic analysis."""
    try:
        # Skip hidden directories
        if path.name.startswith('.'):
            return
            
        # Process files in directory
        for item in path.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                result = analyze_file_harmonics(item)
                if result:
                    freq_name = result["frequency_name"]
                    if freq_name not in results["frequencies"]:
                        results["frequencies"][freq_name] = 0
                    results["frequencies"][freq_name] += 1
                    results["patterns"].append(result)
            elif item.is_dir():
                process_directory(item, results)
    except Exception as e:
        print(f"Error processing directory {path}: {e}")

def main():
    akron_path = Path("/Volumes/Akron")
    print("🔮 Analyzing harmonic patterns...")
    
    results = {
        "frequencies": {},
        "patterns": []
    }
    
    # Process main directories first
    important_dirs = [
        "bear_data",
        "Legal_Documentation",
        "FIELD_ARCHIVE",
        "PROCESSED"
    ]
    
    for dirname in important_dirs:
        dir_path = akron_path / dirname
        if dir_path.exists():
            print(f"\n📂 Analyzing {dirname}...")
            process_directory(dir_path, results)
    
    # Show results
    print("\n📜 Harmonic Analysis Results:")
    print("\n🎵 Frequency Distribution:")
    total_files = sum(results["frequencies"].values())
    
    for freq, count in sorted(results["frequencies"].items(), 
                            key=lambda x: x[1], reverse=True):
        percentage = (count / total_files) * 100 if total_files > 0 else 0
        print(f"{freq:10} {SACRED_FREQUENCIES[freq]:4}Hz: {count:6} files ({percentage:5.1f}%)")
    
    # Show sample files for each frequency
    print("\n🔍 Representative Files by Frequency:")
    shown = set()
    for freq in SACRED_FREQUENCIES:
        patterns = [p for p in results["patterns"] if p["frequency_name"] == freq]
        if patterns:
            print(f"\n{freq} ({SACRED_FREQUENCIES[freq]} Hz):")
            for p in sorted(patterns, key=lambda x: x["size"], reverse=True)[:3]:
                if p["path"] not in shown:
                    size_mb = p["size"] / (1024 * 1024)
                    print(f"  {size_mb:6.1f}MB  {p['path']}")
                    shown.add(p["path"])

if __name__ == "__main__":
    main()