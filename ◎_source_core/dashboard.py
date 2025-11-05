#!/usr/bin/env python3
"""
Data Processing Dashboard for FIELD System
==========================================

Quick dashboard to view processing status and system health.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def display_dashboard():
    """Display the current status of the data processing system."""
    base_path = Path("/Users/jbear")
    
    print("═" * 80)
    print("🔮 FIELD UNIVERSAL DATA PROCESSING SYSTEM")
    print("═" * 80)
    
    # System Status
    print("\n📊 SYSTEM STATUS")
    print("-" * 40)
    
    # Check if automation is running
    automation_status = "✅ ACTIVE" if Path.home().joinpath("Library/LaunchAgents/com.field.dataprocessor.plist").exists() else "⚠️  NOT CONFIGURED"
    print(f"Automation Status: {automation_status}")
    
    # Check logs
    log_path = base_path / "FIELD" / "◎_source_core" / "logs" / "data_processor.log"
    if log_path.exists():
        log_size = log_path.stat().st_size / 1024  # KB
        print(f"Log Status: ✅ Active ({log_size:.1f} KB)")
    else:
        print("Log Status: ⚠️  No logs yet")
    
    # Data Sources Status
    print("\n📂 DATA SOURCES")
    print("-" * 40)
    
    sources = {
        "CZUR Scanner": base_path / "CZURImages",
        "DATA Folder": base_path / "DATA", 
        "Downloads": base_path / "Downloads",
        "Desktop": base_path / "Desktop",
        "Documents": base_path / "Documents"
    }
    
    for name, path in sources.items():
        if path.exists():
            file_count = len([f for f in path.rglob('*') if f.is_file()])
            status = f"✅ {file_count} files"
        else:
            status = "❌ Not found"
        print(f"{name:15}: {status}")
    
    # FIELD Destinations
    print("\n🎯 FIELD DESTINATIONS")
    print("-" * 40)
    
    destinations = {
        "FIELD-DEV": base_path / "FIELD-DEV",
        "FIELD-LIVING": base_path / "FIELD-LIVING",
        "FIELD": base_path / "FIELD",
        "FIELD-QUARANTINE": base_path / "FIELD-QUARANTINE",
        "FIELD-REPORTS": base_path / "FIELD-REPORTS"
    }
    
    for name, path in destinations.items():
        if path.exists():
            status = "✅ Ready"
        else:
            status = "⚠️  Creating..."
            path.mkdir(parents=True, exist_ok=True)
        print(f"{name:18}: {status}")
    
    # Recent Activity
    print("\n⚡ RECENT ACTIVITY")
    print("-" * 40)
    
    processed_log = base_path / "FIELD" / "◎_source_core" / "logs" / "processed_files.json"
    if processed_log.exists():
        try:
            with open(processed_log, 'r') as f:
                processed = json.load(f)
            print(f"Files Processed: {len(processed)}")
            
            # Show recent files
            recent = sorted(processed.values(), 
                          key=lambda x: x.get('processed', ''), 
                          reverse=True)[:5]
            
            if recent:
                print("\nRecent Files:")
                for item in recent:
                    filename = Path(item['source_path']).name
                    category = item.get('category', 'unknown')
                    destination = item.get('destination', 'unknown')
                    print(f"  • {filename[:30]:30} → {category} ({destination})")
                    
        except Exception as e:
            print(f"Error reading processed files: {e}")
    else:
        print("No processing activity yet")
    
    # Configuration Status
    print("\n⚙️  CONFIGURATION")
    print("-" * 40)
    
    config_path = base_path / "FIELD" / "◎_source_core" / "config" / "processing_rules.json"
    if config_path.exists():
        print("Processing Rules: ✅ Configured")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"Auto Process: {'✅ ON' if config.get('auto_process') else '❌ OFF'}")
            print(f"Scanner Integration: {'✅ ON' if config.get('scanner_integration', {}).get('czur_scanner', {}).get('enabled') else '❌ OFF'}")
        except Exception as e:
            print(f"Error reading config: {e}")
    else:
        print("Processing Rules: ⚠️  Default settings")
    
    # Quick Actions
    print("\n🚀 QUICK ACTIONS")
    print("-" * 40)
    print("Scan for new files:     python3 universal_data_processor.py --scan-only")
    print("Process files:          python3 universal_data_processor.py")
    print("Setup automation:       python3 universal_data_processor.py --setup")
    print("View this dashboard:    python3 dashboard.py")
    
    # Storage Analysis
    print("\n💾 STORAGE ANALYSIS")
    print("-" * 40)
    
    total_size = 0
    for source_name, source_path in sources.items():
        if source_path.exists():
            size = sum(f.stat().st_size for f in source_path.rglob('*') if f.is_file()) / (1024*1024)  # MB
            total_size += size
            print(f"{source_name:15}: {size:.1f} MB")
    
    print(f"{'Total Data':15}: {total_size:.1f} MB")
    
    print("\n" + "═" * 80)
    print(f"Dashboard generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 80)

if __name__ == '__main__':
    display_dashboard()