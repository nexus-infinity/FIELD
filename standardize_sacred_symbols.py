#!/usr/bin/env python3
"""
Sacred Symbol Standardization
Converts directories to empty symbols, maintains filled symbols for files
"""

import os
import shutil
from pathlib import Path

class SacredSymbolStandardizer:
    """Standardizes symbols according to empty (folders) vs filled (files) rules"""
    
    def __init__(self, field_root="/Users/jbear/FIELD"):
        self.field_root = Path(field_root)
        
        # Symbol mappings: current → (empty_folder, filled_file)
        self.symbol_mappings = {
            "●": ("◎", "●"),  # Core: empty circle → filled circle
            "▲": ("△", "▲"),  # Intelligence: empty triangle → filled triangle  
            "▼": ("▽", "▼"),  # Root: empty triangle down → filled triangle down
            "◼︎": ("◻", "◼︎"), # Manifestation: empty square → filled square
            "◼": ("◻", "◼"),   # Alternative square
            "◇": ("◇", "◆"),  # Wisdom: empty diamond → filled diamond
            "⬢": ("⬡", "⬢"),  # Integration: empty hexagon → filled hexagon
        }
        
    def convert_to_empty_symbol(self, name):
        """Convert name to use empty symbol variant for folders"""
        for current, (empty, filled) in self.symbol_mappings.items():
            if name.startswith(current):
                return name.replace(current, empty, 1)
        return name
    
    def standardize_directory_symbols(self, dry_run=True):
        """Convert directories to use empty symbols"""
        print(f"🔮 {'DRY RUN: ' if dry_run else ''}Standardizing directory symbols to empty variants...")
        
        changes_made = []
        
        for item in self.field_root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                new_name = self.convert_to_empty_symbol(item.name)
                if new_name != item.name:
                    new_path = self.field_root / new_name
                    if not new_path.exists():
                        if not dry_run:
                            try:
                                shutil.move(str(item), str(new_path))
                                changes_made.append(f"   ✅ {item.name} → {new_name}")
                            except Exception as e:
                                changes_made.append(f"   ❌ {item.name} → {new_name} (Error: {e})")
                        else:
                            changes_made.append(f"   📋 {item.name} → {new_name} (planned)")
                    else:
                        changes_made.append(f"   ⚠️ {item.name} → {new_name} (target exists)")
                        
        return changes_made
    
    def apply_symbol_standardization(self, dry_run=True):
        """Apply symbol standardization with option for dry run"""
        print("🔮 SACRED SYMBOL STANDARDIZATION")
        print("=" * 40)
        
        # First do dry run
        dir_changes = self.standardize_directory_symbols(dry_run=True)
        
        print("📋 PLANNED CHANGES:")
        if dir_changes:
            for change in dir_changes:
                print(change)
        else:
            print("📁 No directory symbol changes needed")
            
        if not dry_run and dir_changes:
            print("\n🔄 EXECUTING CHANGES...")
            actual_changes = self.standardize_directory_symbols(dry_run=False)
            for change in actual_changes:
                print(change)
            
        print("✅ Symbol standardization analysis complete!")

if __name__ == "__main__":
    standardizer = SacredSymbolStandardizer()
    # First run as dry run to see what would change
    standardizer.apply_symbol_standardization(dry_run=True)
