#!/usr/bin/env python3
"""
merge_variants.py – unite glyph-prefixed duplicates into the canonical folder.
"""
import pathlib, re, subprocess, json, shutil, sys

FIELD = pathlib.Path.home() / "FIELD"
MAP = {
    r"[●▼]*TATA.*": FIELD / "TATA",
    r"[▲△]*ATLAS.*": FIELD / "ATLAS",
    r"[■◼︎]*DOJO.*": FIELD / "DOJO",
    r"[●•○]*OBI[-_ ]?WAN.*": FIELD / "OBI-WAN",
}

def move_all(src: pathlib.Path, dst: pathlib.Path):
    """Move contents while preserving tags and structure."""
    for item in src.iterdir():
        target = dst / item.name
        if target.exists():
            print(f"⚠️  {target} exists; manual review.")
            continue
        shutil.move(item, target)
    subprocess.run(["tag", "--add", dst.name.lower()+"_manifested", str(dst)], check=False)
    src.rmdir()

def main(dry=True):
    """Execute folder consolidation with optional dry-run."""
    actions = []
    for p in FIELD.iterdir():
        for regex, canonical in MAP.items():
            if re.fullmatch(regex, p.name) and p != canonical:
                actions.append((p, canonical))
    if dry:
        print(json.dumps([{"from": str(s), "to": str(d)} for s,d in actions], indent=2))
    else:
        for s,d in actions: move_all(s,d)

if __name__ == "__main__":
    main(dry=True)   # change to dry=False only after you inspect
