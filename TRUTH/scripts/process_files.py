#!/usr/bin/env python3

import os
import shutil
import re
from datetime import datetime
import hashlib
from pathlib import Path

class FileProcessor:
    def __init__(self, truth_root="/Users/jbear/FIELD/TRUTH"):
        self.truth_root = truth_root
        self.file_registry = {}  # Track processed files to avoid duplicates

    def generate_file_hash(self, filepath):
        """Generate SHA-256 hash of file contents."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def clean_filename(self, filename):
        """Clean filename by removing special characters and standardizing format."""
        # Handle .rtfd extension specially
        if filename.endswith('.rtfd'):
            name = filename[:-5]  # Remove .rtfd
            ext = '.rtfd'
        else:
            name, ext = os.path.splitext(filename)
        
        # Convert spaces and special characters to underscores
        clean_name = re.sub(r'[^\w\s-]', '_', name)
        clean_name = re.sub(r'\s+', '_', clean_name)
        
        # Remove multiple consecutive underscores
        clean_name = re.sub(r'_+', '_', clean_name)
        
        # Convert to title case for readability
        clean_name = clean_name.title()
        
        # Add extension back
        return clean_name.strip('_') + ext.lower()

    def extract_date(self, filename):
        """Extract date from filename if present, otherwise use file modification time."""
        # Look for common date patterns
        date_patterns = [
            r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})',  # YYYY-MM-DD
            r'(\d{2})[-_]?(\d{2})[-_]?(\d{4})',  # DD-MM-YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, filename)
            if match:
                groups = match.groups()
                if len(groups[0]) == 4:  # YYYY-MM-DD
                    return f"{groups[0]}{groups[1]}{groups[2]}"
                else:  # DD-MM-YYYY
                    return f"{groups[2]}{groups[1]}{groups[0]}"
        
        # Default to current date if no date found
        return datetime.now().strftime("%Y%m%d")

    def determine_target_path(self, source_path, filename):
        """Determine the appropriate target path based on file type and content."""
        # Example mapping logic - expand based on needs
        if "WorkCover" in source_path:
            return os.path.join(self.truth_root, "Personal/JBR/Legal/WorkCover")
        elif "Medical" in source_path:
            return os.path.join(self.truth_root, "Personal/JBR/Health")
        elif "Fraud" in source_path or "Scam" in source_path:
            return os.path.join(self.truth_root, "Personal/JBR/Legal/Investigations")
        else:
            return os.path.join(self.truth_root, "Personal/JBR/Documents")

    def process_file(self, source_path, filename):
        """Process a single file."""
        full_source_path = os.path.join(source_path, filename)
        
        # Handle .rtfd directories as special case
        if filename.endswith('.rtfd'):
            if os.path.isdir(full_source_path):
                # For .rtfd bundles, we'll zip them up
                zip_name = filename.replace('.rtfd', '.zip')
                shutil.make_archive(os.path.join(source_path, zip_name.replace('.zip', '')), 
                                  'zip', full_source_path)
                # Update path to point to the zip file
                full_source_path = os.path.join(source_path, zip_name)
                filename = zip_name
            else:
                return
        # Skip if file doesn't exist or is a directory (and not .rtfd)
        elif not os.path.isfile(full_source_path):
            return
        
        # Generate file hash
        file_hash = self.generate_file_hash(full_source_path)
        if file_hash in self.file_registry:
            print(f"Duplicate file found: {filename}")
            return
        
        self.file_registry[file_hash] = full_source_path
        
        # Clean filename and extract date
        date_str = self.extract_date(filename)
        clean_name = self.clean_filename(filename)
        
        # Construct new filename with date prefix
        new_filename = f"{date_str}_{clean_name}"
        
        # Determine target directory
        target_dir = self.determine_target_path(source_path, filename)
        os.makedirs(target_dir, exist_ok=True)
        
        target_path = os.path.join(target_dir, new_filename)
        
        # Copy file
        shutil.copy2(full_source_path, target_path)
        print(f"Processed: {filename} -> {target_path}")

    def process_directory(self, source_dir):
        """Process all files in a directory recursively."""
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                self.process_file(root, file)

def main():
    # Initialize processor
    processor = FileProcessor()
    
    # Process Bear folder
    bear_folder = "/Users/jbear/iCloud Drive (Archive)/1. Bear "
    processor.process_directory(bear_folder)

if __name__ == "__main__":
    main()