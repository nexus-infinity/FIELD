#!/usr/bin/env python3
"""
field_router.py - Enhanced FIELD-aware symbolic placement engine
Uses geometric and resonance-based evaluation to route files to their proper nodes.
"""
import json
import pathlib
import re
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
import xattr

# Sacred node definitions from trident_memory_index.json
NODES = {
    "TATA": {
        "glyph": "▼",
        "properties": ["law", "integrity", "verification", "registry", "validation"],
        "path": pathlib.Path.home() / "FIELD/TATA"
    },
    "ATLAS": {
        "glyph": "▲", 
        "properties": ["compass", "logic", "intelligence", "mapping", "navigation"],
        "path": pathlib.Path.home() / "FIELD/ATLAS"
    },
    "DOJO": {
        "glyph": "◼",
        "properties": ["execution", "manifestation", "script", "actuation", "build"],
        "path": pathlib.Path.home() / "FIELD/DOJO"
    },
    "OBI-WAN": {
        "glyph": "●",
        "properties": ["observer", "memory", "resonance", "log", "monitor"],
        "path": pathlib.Path.home() / "FIELD/OBI-WAN"
    }
}

@dataclass
class FileAnalysis:
    """Holds analysis results for a single file."""
    path: pathlib.Path
    content_sample: str
    field_override: Optional[str] = None
    symbol_tag: Optional[str] = None
    resonance_scores: Dict[str, float] = None

def read_file_header(path: pathlib.Path, max_lines: int = 50) -> Tuple[str, Optional[str], Optional[str]]:
    """Read file header to extract field location override and content sample."""
    try:
        content = []
        field_override = None
        symbol_tag = None
        
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                content.append(line)
                
                # Look for field override tags
                if '@field_location:' in line:
                    field_override = line.split('@field_location:')[1].strip()
                if '@symbol_tag:' in line:
                    symbol_tag = line.split('@symbol_tag:')[1].strip()
                    
        return '\n'.join(content), field_override, symbol_tag
    except Exception as e:
        return "", None, None

def calculate_resonance(content: str, properties: List[str]) -> float:
    """Calculate resonance score based on property matches."""
    score = 0
    content_lower = content.lower()
    
    # Check for property term matches
    for prop in properties:
        if prop.lower() in content_lower:
            score += 1
            
    # Check for file type indicators
    extensions = {
        'TATA': ['.json', '.yaml', '.yml'],
        'ATLAS': ['.md', '.txt', '.doc'],
        'DOJO': ['.py', '.sh', '.swift'],
        'OBI-WAN': ['.log', '.jsonl']
    }
    
    for node, exts in extensions.items():
        if any(content_lower.endswith(ext) for ext in exts):
            if node in str(properties):
                score += 0.5
                
    return score / (len(properties) + 0.5)  # Normalize to 0-1

def analyze_file(path: pathlib.Path) -> FileAnalysis:
    """Analyze a file to determine its geometric placement."""
    content, field_override, symbol_tag = read_file_header(path)
    
    resonance_scores = {}
    for node, props in NODES.items():
        resonance_scores[node] = calculate_resonance(content, props["properties"])
        
    return FileAnalysis(
        path=path,
        content_sample=content,
        field_override=field_override,
        symbol_tag=symbol_tag,
        resonance_scores=resonance_scores
    )

def set_xattr_tag(path: str, tag: str):
    """Set extended attribute tag when regular tag command isn't available."""
    try:
        xattr.setxattr(path, "user.field.tag", tag.encode())
        return True
    except Exception as e:
        print(f"Note: Could not set xattr tag {tag} for {path}: {e}")
        return False

def tag_file(path: str, tag: str):
    """Try to tag file using tag command, fall back to xattr."""
    try:
        subprocess.run(["tag", "--add", tag, path], check=False, capture_output=True)
        return True
    except FileNotFoundError:
        return set_xattr_tag(path, tag)

def move_file(analysis: FileAnalysis, dry_run: bool = True) -> Dict:
    """Move file to its geometrically aligned location."""
    # Determine destination based on resonance or override
    if analysis.field_override:
        dest_path = pathlib.Path(analysis.field_override)
        dest_node = dest_path.parent.name
    else:
        # Find highest resonance score
        dest_node = max(analysis.resonance_scores.items(), key=lambda x: x[1])[0]
        dest_path = NODES[dest_node]["path"] / analysis.path.name
        
    result = {
        "file": str(analysis.path),
        "destination": str(dest_path),
        "resonance_scores": analysis.resonance_scores,
        "selected_node": dest_node,
        "glyph": NODES[dest_node]["glyph"],
        "action": "would move" if dry_run else "moved"
    }
    
    if not dry_run:
        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(analysis.path), str(dest_path))
            
            # Apply tags
            if analysis.symbol_tag:
                tag_file(str(dest_path), analysis.symbol_tag)
            else:
                tag_file(str(dest_path), f"{dest_node.lower()}:manifested")
                
            result["status"] = "success"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
    
    return result

def generate_report(results: List[Dict]) -> str:
    """Generate a visual report of file movements."""
    report = ["=== FIELD Router Movement Report ===\n"]
    
    for r in results:
        src = pathlib.Path(r["file"])
        dest = pathlib.Path(r["destination"])
        scores = r["resonance_scores"]
        
        report.append(f"\n{r['glyph']} {src.name}")
        report.append(f"  From: {src.parent}")
        report.append(f"  To:   {dest.parent}")
        report.append("\n  Resonance Scores:")
        for node, score in scores.items():
            report.append(f"    {NODES[node]['glyph']} {node}: {score:.2f}")
        
        if r.get("status") == "error":
            report.append(f"\n  ⚠️  Error: {r['error']}")
            
    return "\n".join(report)

def main(dry_run: bool = True):
    """Main execution function."""
    FIELD = pathlib.Path.home() / "FIELD"
    results = []
    
    # Process all files in FIELD directory
    for path in FIELD.glob("*"):
        if path.is_file() and not path.name.startswith('.'):
            analysis = analyze_file(path)
            result = move_file(analysis, dry_run=dry_run)
            results.append(result)
            
    # Generate and print report
    report = generate_report(results)
    print(report)
    
    # Save report
    report_path = FIELD / "_registry/field_router_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    
    return results

if __name__ == "__main__":
    # Run in dry-run mode first
    print("Executing dry run...")
    results = main(dry_run=True)
    
    response = input("\nProceed with actual file moves? [y/N]: ")
    if response.lower() == 'y':
        print("\nExecuting actual moves...")
        results = main(dry_run=False)
    else:
        print("\nAborted. No files were moved.")
