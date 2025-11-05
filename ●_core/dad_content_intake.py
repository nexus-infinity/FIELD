#!/usr/bin/env python3
"""
Dad's Legacy Content Intake System
=================================
Helps identify and prepare dad-related content for processing through
the automated legacy system.

This script:
- Scans existing directories for dad-related content
- Moves identified files to Akron intake for processing
- Provides manual content submission interface
"""

import os
import shutil
from pathlib import Path
import logging
from typing import List, Dict
import argparse

class DadContentIntake:
    """Content intake system for dad's legacy materials"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_paths()
        
    def setup_logging(self):
        """Setup logging for intake operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - DAD_INTAKE - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_paths(self):
        """Setup intake and destination paths"""
        self.paths = {
            'akron_intake': Path("/Volumes/Akron/INTAKE"),
            'search_directories': [
                Path("/Users/jbear/Desktop"),
                Path("/Users/jbear/Documents"),
                Path("/Users/jbear/Downloads"),
                Path("/Volumes/Akron/bear_data"),
                Path("/Users/jbear/FIELD/▼TATA"),
            ]
        }
        
        # Ensure intake directory exists
        self.paths['akron_intake'].mkdir(parents=True, exist_ok=True)
        
    def identify_dad_content(self, directory: Path) -> List[Path]:
        """Scan directory for dad-related content"""
        dad_indicators = [
            # Name variations
            'dad', 'father', 'david', 'rich', 'david rich', 'davidrich',
            # Content types
            'recording', 'voice', 'audio', 'conversation', 'transcript',
            'advice', 'wisdom', 'intention', 'meaning', 'legacy',
            # Business context
            'jacques', 'berjak', 'business', 'financial', 'investment'
        ]
        
        found_files = []
        
        if not directory.exists():
            return found_files
            
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    file_name_lower = file_path.name.lower()
                    
                    # Check filename for dad indicators
                    if any(indicator in file_name_lower for indicator in dad_indicators):
                        found_files.append(file_path)
                        
                    # Check file content if it's a text file (and small enough)
                    elif file_path.suffix.lower() in ['.txt', '.md', '.json'] and file_path.stat().st_size < 1024*1024:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read(1000).lower()  # First 1000 chars
                                if any(indicator in content for indicator in dad_indicators):
                                    found_files.append(file_path)
                        except:
                            pass  # Skip files we can't read
                            
        except PermissionError:
            self.logger.warning(f"Permission denied accessing {directory}")
        except Exception as e:
            self.logger.error(f"Error scanning {directory}: {e}")
            
        return found_files
    
    def scan_all_directories(self) -> Dict[str, List[Path]]:
        """Scan all configured directories for dad content"""
        results = {}
        
        for directory in self.paths['search_directories']:
            self.logger.info(f"🔍 Scanning: {directory}")
            found_files = self.identify_dad_content(directory)
            
            if found_files:
                results[str(directory)] = found_files
                self.logger.info(f"📄 Found {len(found_files)} files in {directory}")
            else:
                self.logger.info(f"📭 No dad content found in {directory}")
                
        return results
    
    def move_to_intake(self, file_path: Path, create_subfolder: bool = True) -> bool:
        """Move file to Akron intake for processing"""
        try:
            if create_subfolder:
                # Create subfolder based on source directory
                source_dir_name = file_path.parent.name
                intake_subfolder = self.paths['akron_intake'] / f"from_{source_dir_name}"
                intake_subfolder.mkdir(exist_ok=True)
                destination = intake_subfolder / file_path.name
            else:
                destination = self.paths['akron_intake'] / file_path.name
                
            # Handle name conflicts
            counter = 1
            original_destination = destination
            while destination.exists():
                stem = original_destination.stem
                suffix = original_destination.suffix
                destination = original_destination.parent / f"{stem}_{counter}{suffix}"
                counter += 1
                
            # Move the file
            shutil.move(str(file_path), str(destination))
            self.logger.info(f"📦 Moved to intake: {file_path.name} → {destination}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to move {file_path}: {e}")
            return False
    
    def submit_manual_file(self, file_path: str) -> bool:
        """Manually submit a specific file for processing"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            self.logger.error(f"File not found: {file_path}")
            return False
            
        return self.move_to_intake(file_path, create_subfolder=False)
    
    def interactive_review(self, scan_results: Dict[str, List[Path]]):
        """Interactive review of found files"""
        print("\\n📋 Dad Content Review")
        print("=" * 50)
        
        total_files = sum(len(files) for files in scan_results.values())
        print(f"Found {total_files} potential dad-related files")
        
        for directory, files in scan_results.items():
            print(f"\\n📁 {directory} ({len(files)} files):")
            
            for i, file_path in enumerate(files, 1):
                print(f"  {i}. {file_path.name}")
                print(f"     Size: {file_path.stat().st_size} bytes")
                print(f"     Modified: {file_path.stat().st_mtime}")
                
                # Get user decision
                while True:
                    decision = input(f"     Process this file? (y/n/q): ").lower().strip()
                    if decision == 'y':
                        self.move_to_intake(file_path)
                        break
                    elif decision == 'n':
                        print("     Skipped")
                        break
                    elif decision == 'q':
                        print("\\n🛑 Stopping review")
                        return
                    else:
                        print("     Please enter 'y' for yes, 'n' for no, or 'q' to quit")
    
    def auto_process_all(self, scan_results: Dict[str, List[Path]]) -> int:
        """Automatically move all found files to intake"""
        moved_count = 0
        
        for directory, files in scan_results.items():
            for file_path in files:
                if self.move_to_intake(file_path):
                    moved_count += 1
                    
        return moved_count
    
    def create_test_files(self):
        """Create test files for demonstration"""
        test_dir = Path("/Users/jbear/Desktop/dad_test_content")
        test_dir.mkdir(exist_ok=True)
        
        test_files = [
            ("dad_recording_1985.txt", "This is a test recording from dad about Jacques Rich and financial planning."),
            ("david_rich_advice.md", "# Dad's Advice\\n\\nRemember what Berjak always said about business relationships..."),
            ("father_wisdom.json", '{"speaker": "dad", "topic": "life lessons", "content": "Always honor your commitments"}'),
            ("conversation_with_dad.txt", "Had a great talk with father today about the old days with Jacques.")
        ]
        
        for filename, content in test_files:
            test_file = test_dir / filename
            with open(test_file, 'w') as f:
                f.write(content)
                
        self.logger.info(f"📝 Created test files in {test_dir}")
        return test_dir


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="Dad's Legacy Content Intake System")
    parser.add_argument('--scan', action='store_true', help='Scan directories for dad content')
    parser.add_argument('--interactive', action='store_true', help='Interactive review of found files')
    parser.add_argument('--auto', action='store_true', help='Automatically process all found files')
    parser.add_argument('--submit', type=str, help='Submit specific file for processing')
    parser.add_argument('--test', action='store_true', help='Create test files for demonstration')
    
    args = parser.parse_args()
    
    intake = DadContentIntake()
    
    if args.test:
        test_dir = intake.create_test_files()
        print(f"✅ Test files created in {test_dir}")
        print("Now run with --scan to find them")
        return
    
    if args.submit:
        if intake.submit_manual_file(args.submit):
            print(f"✅ File submitted for processing: {args.submit}")
        else:
            print(f"❌ Failed to submit file: {args.submit}")
        return
    
    if args.scan or args.interactive or args.auto:
        print("🔍 Scanning for dad's content...")
        scan_results = intake.scan_all_directories()
        
        if not scan_results:
            print("📭 No dad-related content found")
            return
            
        if args.interactive:
            intake.interactive_review(scan_results)
        elif args.auto:
            moved_count = intake.auto_process_all(scan_results)
            print(f"✅ Moved {moved_count} files to intake for processing")
        else:
            # Just show what was found
            total = sum(len(files) for files in scan_results.values())
            print(f"📊 Found {total} dad-related files")
            print("Use --interactive or --auto to process them")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
