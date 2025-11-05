#!/usr/bin/env python3
"""
Enhanced merge script to handle both folder variants and loose files.
"""
import pathlib, re, json, sys

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

def analyze_moves():
    """Analyze and return planned folder and file moves."""
    folder_moves = []
    file_moves = []
    
    # Handle backup folders
    for p in FIELD.glob("*_backup_*"):
        if p.is_dir():
            MAP[p.name] = FIELD
    
    # Check directory moves
    for p in FIELD.iterdir():
        if p.name in PRESERVE:
            continue
            
        # Handle folders
        if p.is_dir():
            for regex, canonical in MAP.items():
                if re.fullmatch(regex, p.name) and p != canonical:
                    folder_moves.append({
                        "type": "folder",
                        "from": str(p),
                        "to": str(canonical),
                        "name": p.name
                    })
                    break
        
        # Handle loose files
        elif p.is_file():
            for regex, target in FILES.items():
                if re.fullmatch(regex, p.name):
                    file_moves.append({
                        "type": "file",
                        "from": str(p),
                        "to": str(target / p.name),
                        "name": p.name
                    })
                    break
    
    return folder_moves, file_moves

def main(dry=True):
    """Show or execute the consolidation plan."""
    folder_moves, file_moves = analyze_moves()
    
    moves = {
        "folders": folder_moves,
        "files": file_moves
    }
    
    print("=== DRY RUN - Planned Moves ===")
    print(json.dumps(moves, indent=2))
    print("\nSummary:")
    print(f"- Folders to consolidate: {len(folder_moves)}")
    print(f"- Files to relocate: {len(file_moves)}")

if __name__ == "__main__":
    main(dry=True)
