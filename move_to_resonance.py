#!/usr/bin/env python3
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from implement_harmonic_field import (
    FREQUENCY_DOMAINS,
    analyze_resonance,
    determine_target_path
)

# Source directories to process
SOURCE_DIRS = [
    "bear_data",
    "Legal_Documentation",
    "FIELD_ARCHIVE",
    "PROCESSED"
]

def create_resonance_manifest(path: Path) -> Dict:
    """Creates a manifest of file resonances."""
    manifest = {
        "created_at": datetime.utcnow().isoformat(),
        "files": {},
        "frequencies": {str(freq): 0 for freq in FREQUENCY_DOMAINS.keys()}
    }
    return manifest

def process_file(file_path: Path, base_path: Path, manifest: Dict) -> None:
    """Process a single file for resonant movement."""
    try:
        # Calculate resonance
        frequency = analyze_resonance(file_path)
        manifest["frequencies"][str(frequency)] += 1
        
        # Determine target
        target_path = determine_target_path(file_path, base_path, frequency)
        rel_path = str(file_path.relative_to(base_path))
        
        # Record in manifest
        manifest["files"][rel_path] = {
            "frequency": frequency,
            "source": str(file_path),
            "target": str(target_path / file_path.name),
            "size": file_path.stat().st_size
        }
        
        print(f"🎵 {frequency}Hz: {rel_path} -> {target_path.name}")
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def move_to_resonance(file_info: Dict, base_path: Path) -> bool:
    """Moves a file to its resonant location."""
    try:
        source = Path(file_info["source"])
        target = Path(file_info["target"])
        
        # Create target directory
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.copy2(source, target)
        return True
        
    except Exception as e:
        print(f"❌ Error moving {source}: {e}")
        return False

def main():
    akron_path = Path("/Volumes/Akron")
    manifest_path = akron_path / "resonance_manifest.json"
    
    print("🌟 Beginning Resonant Movement")
    
    # Create manifest
    manifest = create_resonance_manifest(akron_path)
    
    # Process each source directory
    for dirname in SOURCE_DIRS:
        source_path = akron_path / dirname
        if not source_path.exists():
            continue
            
        print(f"\n📂 Processing {dirname}...")
        
        # Walk directory
        for root, _, files in os.walk(source_path):
            root_path = Path(root)
            for file in files:
                if file.startswith('.'):
                    continue
                file_path = root_path / file
                process_file(file_path, akron_path, manifest)
    
    # Show frequency distribution
    print("\n🎵 Frequency Distribution:")
    total = sum(int(count) for count in manifest["frequencies"].values())
    for freq, count in sorted(manifest["frequencies"].items()):
        if int(count) > 0:
            percentage = (int(count) / total) * 100
            print(f"{freq:4}Hz: {count:6} files ({percentage:5.1f}%)")
    
    # Confirm movement
    response = input("\n⚡️ Ready to move files to their resonant spaces? [y/N] ")
    if response.lower() != 'y':
        print("🛑 Movement cancelled")
        return
    
    # Move files
    print("\n🌊 Moving files to resonant spaces...")
    moved = 0
    total = len(manifest["files"])
    
    for file_info in manifest["files"].values():
        if move_to_resonance(file_info, akron_path):
            moved += 1
            if moved % 100 == 0:
                print(f"✨ Moved {moved}/{total} files...")
    
    print(f"\n🎵 Movement complete: {moved}/{total} files placed in resonant harmony")

if __name__ == "__main__":
    main()