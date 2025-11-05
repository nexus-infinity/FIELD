#!/usr/bin/env python3
"""
Symlink Manager for Storage Optimization
Manages creation and maintenance of symlinks between FIELD and FIELD-DEV
"""

import os
import shutil
import json
import logging
from pathlib import Path
from typing import List, Tuple, Dict
import time

class SymlinkManager:
    def __init__(self, field_dir: str, field_dev_dir: str):
        self.field_dir = Path(field_dir)
        self.field_dev_dir = Path(field_dev_dir)
        self.log_file = self.field_dir / "symlink_operations.log"
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for symlink operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def migrate_with_symlink(self, source_path: str, target_path: str, 
                           create_symlink: bool = True) -> bool:
        """
        Migrate file from source to target and optionally create symlink
        
        Args:
            source_path: Original file path
            target_path: Destination file path
            create_symlink: Whether to create symlink at source location
            
        Returns:
            bool: Success status
        """
        source = Path(source_path)
        target = Path(target_path)
        
        try:
            # Ensure target directory exists
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if source exists and is not already a symlink
            if not source.exists():
                self.logger.error(f"Source file does not exist: {source}")
                return False
                
            if source.is_symlink():
                self.logger.warning(f"Source is already a symlink: {source}")
                return False
            
            # Check if target already exists
            if target.exists():
                self.logger.warning(f"Target already exists: {target}")
                return False
            
            # Move file to target location
            shutil.move(str(source), str(target))
            self.logger.info(f"Moved {source} to {target}")
            
            # Create symlink if requested
            if create_symlink:
                os.symlink(str(target), str(source))
                self.logger.info(f"Created symlink {source} -> {target}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to migrate {source} to {target}: {e}")
            return False
    
    def batch_migrate(self, migration_list: List[Tuple[str, str]], 
                     dry_run: bool = False) -> Dict[str, int]:
        """
        Perform batch migration of files
        
        Args:
            migration_list: List of (source, target) tuples
            dry_run: If True, only log what would be done
            
        Returns:
            Dict with success/failure counts
        """
        results = {'success': 0, 'failed': 0, 'skipped': 0}
        
        for source, target in migration_list:
            if dry_run:
                self.logger.info(f"DRY RUN: Would migrate {source} to {target}")
                continue
            
            # Check file size before migration
            try:
                size = Path(source).stat().st_size
                if size > 100 * 1024 * 1024:  # > 100MB
                    self.logger.info(f"Migrating large file ({size/1024/1024:.1f}MB): {source}")
            except:
                pass
            
            if self.migrate_with_symlink(source, target):
                results['success'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def create_archive_structure(self) -> bool:
        """Create organized archive structure in FIELD-DEV"""
        try:
            # Create archive directories
            archive_dirs = [
                'large_files',
                'old_files',
                'infrequent_access',
                'compressed',
                'by_type/python',
                'by_type/json',
                'by_type/media',
                'by_type/documents',
                'by_date/2024',
                'by_date/2023',
                'by_date/older'
            ]
            
            for dir_name in archive_dirs:
                archive_path = self.field_dev_dir / 'archive' / dir_name
                archive_path.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"Created archive directory: {archive_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create archive structure: {e}")
            return False
    
    def organize_by_access_pattern(self, analysis_results: Dict) -> List[Tuple[str, str]]:
        """
        Organize files based on access patterns
        
        Args:
            analysis_results: Results from access pattern analysis
            
        Returns:
            List of (source, target) migration tuples
        """
        migrations = []
        
        if 'migration_candidates' in analysis_results:
            for source, suggested_target in analysis_results['migration_candidates']:
                source_path = Path(source)
                
                # Determine optimal target based on file characteristics
                if source_path.suffix.lower() in ['.py', '.js', '.ts']:
                    target = self.field_dev_dir / 'archive' / 'by_type' / 'python' / source_path.name
                elif source_path.suffix.lower() in ['.json', '.yaml', '.yml']:
                    target = self.field_dev_dir / 'archive' / 'by_type' / 'json' / source_path.name
                elif source_path.suffix.lower() in ['.jpg', '.png', '.mp4', '.mp3']:
                    target = self.field_dev_dir / 'archive' / 'by_type' / 'media' / source_path.name
                elif source_path.stat().st_size > 50 * 1024 * 1024:  # > 50MB
                    target = self.field_dev_dir / 'archive' / 'large_files' / source_path.name
                else:
                    target = self.field_dev_dir / 'archive' / 'infrequent_access' / source_path.name
                
                migrations.append((source, str(target)))
        
        return migrations
    
    def validate_symlinks(self) -> Dict[str, List[str]]:
        """
        Validate existing symlinks and identify broken ones
        
        Returns:
            Dict with 'valid', 'broken', and 'missing_targets' lists
        """
        results = {
            'valid': [],
            'broken': [],
            'missing_targets': []
        }
        
        # Find all symlinks in FIELD directory
        for root, dirs, files in os.walk(self.field_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.is_symlink():
                    target = file_path.resolve()
                    
                    if target.exists():
                        results['valid'].append(str(file_path))
                    else:
                        results['broken'].append(str(file_path))
                        
                        # Check if target exists but link is broken
                        if file_path.readlink().exists():
                            results['missing_targets'].append(str(file_path))
        
        self.logger.info(f"Symlink validation: {len(results['valid'])} valid, "
                        f"{len(results['broken'])} broken, "
                        f"{len(results['missing_targets'])} missing targets")
        
        return results
    
    def repair_broken_symlinks(self) -> int:
        """
        Attempt to repair broken symlinks
        
        Returns:
            Number of repaired symlinks
        """
        validation_results = self.validate_symlinks()
        repaired = 0
        
        for broken_link in validation_results['broken']:
            link_path = Path(broken_link)
            
            try:
                # Try to find the target file in FIELD-DEV
                target_name = link_path.name
                potential_targets = list(self.field_dev_dir.rglob(target_name))
                
                if potential_targets:
                    # Use the first match
                    new_target = potential_targets[0]
                    
                    # Remove broken link
                    link_path.unlink()
                    
                    # Create new symlink
                    os.symlink(str(new_target), str(link_path))
                    self.logger.info(f"Repaired symlink: {link_path} -> {new_target}")
                    repaired += 1
                    
            except Exception as e:
                self.logger.error(f"Failed to repair symlink {link_path}: {e}")
        
        return repaired
    
    def generate_migration_report(self, migration_results: Dict) -> str:
        """Generate a detailed migration report"""
        report = f"""
Storage Optimization Migration Report
=====================================
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}

Migration Summary:
- Successful migrations: {migration_results.get('success', 0)}
- Failed migrations: {migration_results.get('failed', 0)}
- Skipped migrations: {migration_results.get('skipped', 0)}

Symlink Validation:
- Valid symlinks: {len(self.validate_symlinks()['valid'])}
- Broken symlinks: {len(self.validate_symlinks()['broken'])}

Space Optimization:
- Files moved to archive: {migration_results.get('success', 0)}
- Estimated space saved in FIELD: {migration_results.get('space_saved', 0) / (1024**3):.2f} GB

Recommendations:
1. Run symlink validation weekly
2. Monitor access patterns for further optimization
3. Consider compression for old archive files
4. Implement automated cleanup policies

Log file: {self.log_file}
"""
        return report

def main():
    """Main execution function"""
    field_dir = "/Users/jbear/FIELD"
    field_dev_dir = "/Users/jbear/FIELD-DEV"
    
    manager = SymlinkManager(field_dir, field_dev_dir)
    
    print("Storage Optimization - Symlink Manager")
    print("=" * 40)
    
    # Create archive structure
    print("Creating archive structure...")
    manager.create_archive_structure()
    
    # Load analysis results if available
    analysis_file = Path(field_dir) / "access_analysis_results.json"
    if analysis_file.exists():
        with open(analysis_file) as f:
            analysis_results = json.load(f)
        
        print(f"Loaded analysis results with {len(analysis_results.get('migration_candidates', []))} candidates")
        
        # Organize migrations
        migrations = manager.organize_by_access_pattern(analysis_results)
        print(f"Organized {len(migrations)} migrations")
        
        # Perform migrations (dry run first)
        print("\nPerforming dry run...")
        dry_results = manager.batch_migrate(migrations[:10], dry_run=True)  # First 10 as test
        
        # Ask for confirmation
        response = input("\nProceed with actual migrations? (y/N): ")
        if response.lower() == 'y':
            print("Performing actual migrations...")
            results = manager.batch_migrate(migrations[:10])  # Limit for safety
            
            print(f"\nMigration Results:")
            print(f"Success: {results['success']}")
            print(f"Failed: {results['failed']}")
            
            # Generate report
            report = manager.generate_migration_report(results)
            print("\n" + report)
            
            # Save report
            with open(Path(field_dir) / "migration_report.txt", 'w') as f:
                f.write(report)
        else:
            print("Migration cancelled.")
    
    # Validate existing symlinks
    print("\nValidating existing symlinks...")
    validation_results = manager.validate_symlinks()
    
    if validation_results['broken']:
        print(f"Found {len(validation_results['broken'])} broken symlinks")
        repair_response = input("Attempt to repair broken symlinks? (y/N): ")
        if repair_response.lower() == 'y':
            repaired = manager.repair_broken_symlinks()
            print(f"Repaired {repaired} symlinks")
    
    print("\nSymlink management complete!")

if __name__ == "__main__":
    main()
