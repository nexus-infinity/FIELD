#!/usr/bin/env python3
"""
Execute the consolidation of folders and files according to the Metatron Trident structure.
"""
import pathlib, re, shutil, subprocess
from typing import Dict, List, Tuple

FIELD = pathlib.Path.home() / "FIELD"

# 1. Folder variants to merge into canonical nodes
MAP = {
    r"[●▼]*TATA.*": FIELD / "TATA",
    r"[▲△]*ATLAS.*": FIELD / "ATLAS",
    r"[■◼︎]*DOJO.*": FIELD / "DOJO",
    r"[●•○◎]*OBI[-_ ]?WAN.*": FIELD / "OBI-WAN",
}

# 2. File types to relocate
FILES = {
    r".*\.ya?ml$": FIELD / "TATA",      # config files
    r".*\.json$": FIELD / "TATA",       # config, manifests
    r".*\.md$": FIELD / "ATLAS",        # documentation
    r".*\.py$": FIELD / "DOJO",         # scripts
    r".*\.log$": FIELD / "OBI-WAN",     # logs
}

# 3. Special directories to preserve
PRESERVE = {
    "_registry",
    "scripts",
    "_sandbox",
    ".git",
    ".warp",
    "TATA",
    "ATLAS", 
    "DOJO",
    "OBI-WAN"
}

def add_tag(path: pathlib.Path, tag: str):
    """Add a tag to a file/directory if the tag command is available."""
    try:
        subprocess.run(["tag", "--add", tag, str(path)], check=False, capture_output=True)
        return True
    except FileNotFoundError:
        print(f"Note: 'tag' command not found; skipping tag {tag} for {path}")
        return True

def move_file(src: pathlib.Path, dst: pathlib.Path):
    """Move a file while preserving its attributes."""
    if dst.exists():
        print(f"⚠️  {dst} exists; skipping")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    add_tag(dst, dst.parent.name.lower()+"_manifested")
    return True

def move_directory(src: pathlib.Path, dst: pathlib.Path):
    """Move directory contents while preserving structure."""
    if not src.is_dir():
        return False
    
    success = True
    for item in src.iterdir():
        target = dst / item.name
        if target.exists():
            print(f"⚠️  {target} exists; manual review needed")
            success = False
            continue
            
        if item.is_file():
            # Check if file should go somewhere specific based on extension
            final_dst = target
            for regex, file_dst in FILES.items():
                if re.fullmatch(regex, item.name):
                    final_dst = file_dst / item.name
                    break
            success &= move_file(item, final_dst)
        else:
            dst.mkdir(parents=True, exist_ok=True)
            success &= move_directory(item, target)
            
    if success:
        add_tag(dst, dst.name.lower()+"_manifested")
        try:
            src.rmdir()  # Only removes if empty
        except OSError:
            print(f"⚠️  Could not remove {src}; not empty")
            success = False
    
    return success

def main():
    """Execute the consolidation plan."""
    print("=== Executing Consolidation ===")
    
    # First handle directory consolidation
    print("\n1. Consolidating directories...")
    dir_success = True
    for p in FIELD.iterdir():
        if p.name in PRESERVE:
            continue
            
        if p.is_dir():
            for regex, canonical in MAP.items():
                if re.fullmatch(regex, p.name) and p != canonical:
                    print(f"Moving {p.name} → {canonical.name}")
                    dir_success &= move_directory(p, canonical)
                    break
    
    # Then handle loose files
    print("\n2. Relocating loose files...")
    file_success = True
    for p in FIELD.iterdir():
        if p.name in PRESERVE or not p.is_file():
            continue
            
        for regex, target in FILES.items():
            if re.fullmatch(regex, p.name):
                print(f"Moving {p.name} → {target.name}/")
                file_success &= move_file(p, target / p.name)
                break
    
    print("\nSummary:")
    if dir_success and file_success:
        print("✅ All moves completed successfully")
    else:
        print("⚠️  Some moves required manual review")
        print("   Run the script again after resolving conflicts")

if __name__ == "__main__":
    main()
