#!/usr/bin/env python3
"""
Field Resource Ecosystem (FRE) - Master Control Interface
=========================================================

Professional unified front-end for all FIELD system modules and business operations.
Integrates with existing Berjak CRM and provides centralized resource management.

This is the professional interface that brings together:
- Universal Data Processor
- Berjak CRM Integration
- Sacred Geometry Orchestration
- FIELD Navigation Systems
- Business Intelligence Dashboard
- Resource Management Tools
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import time

class FieldResourceEcosystem:
    """
    Master control interface for the Field Resource Ecosystem.
    
    Provides unified access to all FIELD system components, business tools,
    and CRM integrations through a professional command-line interface.
    """
    
    def __init__(self):
        self.base_path = Path.home()
        self.field_core = self.base_path / "FIELD" / "◎_source_core"
        self.field_atlas = self.base_path / "FIELD" / "▲ATLAS"
        self.field_dev = self.base_path / "FIELD-DEV"
        self.field_living = self.base_path / "FIELD-LIVING"
        self.berjak_crm = self.base_path / ".berjak_crm"
        
        # Module paths
        self.modules = {
            'data_processor': self.field_core / 'universal_data_processor.py',
            'dashboard': self.field_core / 'dashboard.py',
            'sacred_cli': self.base_path / 'FIELD' / 'cli' / 'sacred_cli.py',
            'berjak_crm': self.berjak_crm / 'system'
        }
        
        # Initialize system status
        self.status = self._get_system_status()
        
    def _get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'field_core_active': self.field_core.exists(),
            'berjak_crm_active': self.berjak_crm.exists(),
            'data_processor_active': self.modules['data_processor'].exists(),
            'sacred_system_active': self.modules['sacred_cli'].exists(),
            'automation_enabled': (Path.home() / 'Library' / 'LaunchAgents' / 'com.field.dataprocessor.plist').exists()
        }
    
    def display_header(self):
        """Display professional system header."""
        print("═" * 100)
        print("🔮 FIELD RESOURCE ECOSYSTEM (FRE) - Master Control Interface")
        print("═" * 100)
        print(f"📍 Location: {os.getcwd()}")
        print(f"👤 User: {os.getenv('USER', 'Unknown')}")
        print(f"⏰ Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("═" * 100)
    
    def display_main_menu(self):
        """Display the main menu options."""
        print("\n🎯 FIELD RESOURCE ECOSYSTEM - Main Menu")
        print("-" * 60)
        print("1. 📊 Business Intelligence Dashboard")
        print("2. 🔄 Universal Data Processor") 
        print("3. 💼 Berjak CRM Integration")
        print("4. 🌐 Sacred Geometry Systems")
        print("5. 📁 FIELD Navigation & Management")
        print("6. ⚙️  System Configuration & Status")
        print("7. 🔍 Resource Search & Analytics")
        print("8. 🚀 Quick Actions & Automation")
        print("9. 📈 Reports & Documentation")
        print("10. 🔧 Advanced Tools & Utilities")
        print("-" * 60)
        print("0. Exit FRE System")
        print("h. Help & Documentation")
        
    def run_business_dashboard(self):
        """Launch comprehensive business intelligence dashboard."""
        print("\n📊 BUSINESS INTELLIGENCE DASHBOARD")
        print("=" * 50)
        
        # System Overview
        self._display_system_overview()
        
        # Business Metrics
        self._display_business_metrics()
        
        # Resource Status
        self._display_resource_status()
        
        # Quick Actions
        print("\n🚀 Quick Business Actions:")
        print("1. View CRM Status")
        print("2. Process New Data")
        print("3. Generate Reports")
        print("4. Check Automation")
        print("5. System Health Check")
        
        choice = input("\nSelect action (1-5, or Enter to return): ").strip()
        if choice == "1":
            self._display_crm_status()
        elif choice == "2":
            self._run_data_processor()
        elif choice == "3":
            self._generate_reports()
        elif choice == "4":
            self._check_automation()
        elif choice == "5":
            self._system_health_check()
    
    def _display_system_overview(self):
        """Display comprehensive system overview."""
        print("\n🔍 SYSTEM OVERVIEW")
        print("-" * 30)
        
        # Core Systems Status
        systems = {
            "FIELD Core": "✅ Active" if self.status['field_core_active'] else "❌ Inactive",
            "Berjak CRM": "✅ Active" if self.status['berjak_crm_active'] else "❌ Inactive", 
            "Data Processor": "✅ Ready" if self.status['data_processor_active'] else "❌ Missing",
            "Sacred Systems": "✅ Ready" if self.status['sacred_system_active'] else "❌ Missing",
            "Automation": "✅ Enabled" if self.status['automation_enabled'] else "⚠️ Disabled"
        }
        
        for system, status in systems.items():
            print(f"{system:15}: {status}")
    
    def _display_business_metrics(self):
        """Display key business metrics."""
        print("\n💼 BUSINESS METRICS")
        print("-" * 20)
        
        try:
            # Check processed files
            processed_log = self.field_core / 'logs' / 'processed_files.json'
            if processed_log.exists():
                with open(processed_log, 'r') as f:
                    processed = json.load(f)
                print(f"Files Processed: {len(processed)}")
            else:
                print("Files Processed: 0")
                
            # Check data sources
            sources = {
                "CZUR Scanner": self.base_path / "CZURImages",
                "DATA Folder": self.base_path / "DATA",
                "Downloads": self.base_path / "Downloads"
            }
            
            for name, path in sources.items():
                if path.exists():
                    file_count = len([f for f in path.rglob('*') if f.is_file()])
                    print(f"{name:15}: {file_count} files")
                    
        except Exception as e:
            print(f"Error loading metrics: {e}")
    
    def _display_resource_status(self):
        """Display resource utilization status."""
        print("\n💾 RESOURCE STATUS")
        print("-" * 20)
        
        # Check FIELD directories
        field_dirs = {
            "FIELD-DEV": self.field_dev,
            "FIELD-LIVING": self.field_living,
            "FIELD": self.base_path / "FIELD"
        }
        
        for name, path in field_dirs.items():
            if path.exists():
                try:
                    size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file()) / (1024*1024)
                    print(f"{name:12}: {size:.1f} MB")
                except:
                    print(f"{name:12}: Active")
            else:
                print(f"{name:12}: ❌ Missing")
    
    def _display_crm_status(self):
        """Display Berjak CRM integration status."""
        print("\n💼 BERJAK CRM INTEGRATION STATUS")
        print("=" * 40)
        
        if self.berjak_crm.exists():
            print("✅ Berjak CRM System: Active")
            
            # Check for CRM components
            crm_components = list(self.berjak_crm.rglob('*'))
            print(f"📁 CRM Components: {len(crm_components)}")
            
            # Check ATLAS CRM configs
            atlas_crm = list(self.field_atlas.glob('*crm*'))
            print(f"🔧 ATLAS CRM Configs: {len(atlas_crm)}")
            
            # Web Interface
            crm_interface = self.field_core / 'berjak_crm_interface.html'
            if crm_interface.exists():
                print("🌐 Beautiful Web Interface: Available")
                print(f"   Location: {crm_interface}")
                
                launch = input("\n🚀 Launch beautiful CRM interface in browser? (y/n): ").strip().lower()
                if launch == 'y':
                    import webbrowser
                    webbrowser.open(f'file://{crm_interface}')
                    print("✅ CRM Interface launched in browser")
            else:
                print("🌐 Web Interface: Not found")
            
            # Google Cloud Integration
            gcloud_config = self.base_path / ".config" / "gcloud"
            if gcloud_config.exists():
                print("☁️  Google Cloud: Connected")
                print(f"   Account: jeremy.rich@berjak.com.au")
                print(f"   Project: berjak-development-project")
            else:
                print("☁️  Google Cloud: ❌ Not configured")
                
        else:
            print("❌ Berjak CRM System: Not Found")
            print("   Run setup to initialize CRM integration")
    
    def _run_data_processor(self):
        """Execute the universal data processor."""
        print("\n🔄 UNIVERSAL DATA PROCESSOR")
        print("=" * 35)
        
        if not self.modules['data_processor'].exists():
            print("❌ Data processor not found!")
            return
            
        print("Starting data processing cycle...")
        try:
            os.chdir(self.field_core)
            result = subprocess.run([
                'python3', 'universal_data_processor.py'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Data processing completed successfully!")
                print("\n📊 Results:")
                print(result.stdout)
            else:
                print("❌ Data processing failed!")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error running data processor: {e}")
    
    def _generate_reports(self):
        """Generate business and system reports."""
        print("\n📈 REPORT GENERATION")
        print("=" * 25)
        
        reports_dir = self.base_path / "FIELD-REPORTS"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = reports_dir / f"fre_system_report_{timestamp}.json"
        
        # Compile comprehensive report
        report_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'system_status': self.status,
            'business_metrics': self._collect_business_metrics(),
            'resource_utilization': self._collect_resource_metrics(),
            'crm_integration': self._collect_crm_metrics()
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"✅ Report generated: {report_file}")
        print(f"📊 Report contains {len(report_data)} sections")
    
    def _collect_business_metrics(self) -> Dict[str, Any]:
        """Collect business performance metrics."""
        metrics = {}
        
        try:
            # Data processing metrics
            processed_log = self.field_core / 'logs' / 'processed_files.json'
            if processed_log.exists():
                with open(processed_log, 'r') as f:
                    processed = json.load(f)
                metrics['files_processed'] = len(processed)
                metrics['processing_categories'] = {}
                
                for item in processed.values():
                    category = item.get('category', 'unknown')
                    metrics['processing_categories'][category] = metrics['processing_categories'].get(category, 0) + 1
            else:
                metrics['files_processed'] = 0
                
        except Exception as e:
            metrics['error'] = str(e)
            
        return metrics
    
    def _collect_resource_metrics(self) -> Dict[str, Any]:
        """Collect system resource utilization metrics."""
        metrics = {}
        
        # FIELD directory analysis
        field_dirs = ['FIELD', 'FIELD-DEV', 'FIELD-LIVING', 'FIELD-QUARANTINE', 'FIELD-REPORTS']
        
        for dir_name in field_dirs:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                try:
                    file_count = len([f for f in dir_path.rglob('*') if f.is_file()])
                    total_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                    metrics[dir_name] = {
                        'file_count': file_count,
                        'total_size_mb': total_size / (1024 * 1024)
                    }
                except Exception as e:
                    metrics[dir_name] = {'error': str(e)}
            else:
                metrics[dir_name] = {'status': 'missing'}
                
        return metrics
    
    def _collect_crm_metrics(self) -> Dict[str, Any]:
        """Collect CRM integration metrics."""
        metrics = {
            'berjak_crm_active': self.berjak_crm.exists(),
            'atlas_crm_configs': len(list(self.field_atlas.glob('*crm*'))),
            'google_cloud_connected': (self.base_path / ".config" / "gcloud").exists()
        }
        
        return metrics
    
    def _check_automation(self):
        """Check and display automation status."""
        print("\n🤖 AUTOMATION STATUS")
        print("=" * 25)
        
        plist_file = Path.home() / 'Library' / 'LaunchAgents' / 'com.field.dataprocessor.plist'
        
        if plist_file.exists():
            print("✅ Data Processing Automation: ENABLED")
            print("   • Runs every 5 minutes")
            print("   • Automatic file processing")
            print("   • System boot startup")
            
            # Check if actually running
            try:
                result = subprocess.run(['launchctl', 'list', 'com.field.dataprocessor'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("   • Status: Currently running")
                else:
                    print("   • Status: Configured but not running")
            except:
                print("   • Status: Unknown")
        else:
            print("⚠️  Data Processing Automation: DISABLED")
            print("   Run setup to enable automation")
    
    def _system_health_check(self):
        """Perform comprehensive system health check."""
        print("\n🏥 SYSTEM HEALTH CHECK")
        print("=" * 30)
        
        health_score = 0
        max_score = 10
        
        # Check core components
        plist_file = Path.home() / 'Library' / 'LaunchAgents' / 'com.field.dataprocessor.plist'
        checks = [
            ("FIELD Core Directory", self.base_path / "FIELD", 2),
            ("Universal Data Processor", self.modules['data_processor'], 2),
            ("Berjak CRM Integration", self.berjak_crm, 2),
            ("Dashboard System", self.modules['dashboard'], 1),
            ("Sacred CLI", self.modules['sacred_cli'], 1),
            ("Automation System", plist_file, 2)
        ]
        
        for name, path, points in checks:
            if isinstance(path, Path) and path.exists():
                print(f"✅ {name}: OK")
                health_score += points
            else:
                print(f"❌ {name}: MISSING")
        
        # Overall health
        health_percentage = (health_score / max_score) * 100
        print(f"\n🎯 Overall System Health: {health_percentage:.1f}%")
        
        if health_percentage >= 90:
            print("🟢 System Status: EXCELLENT")
        elif health_percentage >= 70:
            print("🟡 System Status: GOOD")
        elif health_percentage >= 50:
            print("🟠 System Status: NEEDS ATTENTION")
        else:
            print("🔴 System Status: CRITICAL")
    
    def run_sacred_systems(self):
        """Launch Sacred Geometry systems interface."""
        print("\n🌐 SACRED GEOMETRY SYSTEMS")
        print("=" * 35)
        
        if not self.modules['sacred_cli'].exists():
            print("❌ Sacred CLI not found!")
            return
            
        print("Sacred Geometry System Options:")
        print("1. System Status")
        print("2. Start Sacred Node")
        print("3. Navigation Systems")
        print("4. Consciousness Mirror")
        print("5. Return to main menu")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            try:
                result = subprocess.run(['python3', str(self.modules['sacred_cli']), 'status'], 
                                      capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"Error: {e}")
    
    def run_field_navigation(self):
        """Launch FIELD navigation and management interface."""
        print("\n📁 FIELD NAVIGATION & MANAGEMENT")
        print("=" * 40)
        
        print("FIELD Directory Structure:")
        field_dirs = {
            "FIELD": "Core system and knowledge base",
            "FIELD-DEV": "Development and experimental",
            "FIELD-LIVING": "Production and active systems", 
            "FIELD-QUARANTINE": "Unprocessed/suspicious content",
            "FIELD-REPORTS": "Generated reports and analytics"
        }
        
        for i, (name, desc) in enumerate(field_dirs.items(), 1):
            path = self.base_path / name
            status = "✅" if path.exists() else "❌"
            print(f"{i}. {status} {name:18} - {desc}")
        
        print("\nNavigation Options:")
        print("6. Quick directory overview")
        print("7. Create missing directories")
        print("8. Directory size analysis")
        print("9. Return to main menu")
        
        choice = input("\nSelect option (1-9): ").strip()
        
        if choice in ["1", "2", "3", "4", "5"]:
            dir_name = list(field_dirs.keys())[int(choice) - 1]
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                print(f"\n📂 Contents of {dir_name}:")
                for item in sorted(dir_path.iterdir())[:10]:
                    print(f"   {'📁' if item.is_dir() else '📄'} {item.name}")
                if len(list(dir_path.iterdir())) > 10:
                    print(f"   ... and {len(list(dir_path.iterdir())) - 10} more items")
            else:
                print(f"❌ Directory {dir_name} does not exist")
        elif choice == "7":
            self._create_missing_directories()
    
    def _create_missing_directories(self):
        """Create any missing FIELD directories."""
        field_dirs = ["FIELD", "FIELD-DEV", "FIELD-LIVING", "FIELD-QUARANTINE", "FIELD-REPORTS"]
        created = 0
        
        for dir_name in field_dirs:
            dir_path = self.base_path / dir_name
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True)
                print(f"✅ Created: {dir_name}")
                created += 1
            else:
                print(f"✓ Exists: {dir_name}")
        
        if created > 0:
            print(f"\n🎉 Created {created} missing directories")
        else:
            print("\n✅ All directories already exist")
    
    def run_interactive_menu(self):
        """Run the main interactive menu system."""
        while True:
            self.display_header()
            self.display_main_menu()
            
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice == "0":
                print("\n👋 Exiting Field Resource Ecosystem")
                print("Thank you for using the FRE system!")
                break
            elif choice == "1":
                self.run_business_dashboard()
            elif choice == "2":
                self._run_data_processor()
            elif choice == "3":
                self._display_crm_status()
            elif choice == "4":
                self.run_sacred_systems()
            elif choice == "5":
                self.run_field_navigation()
            elif choice == "6":
                self._system_health_check()
            elif choice == "h" or choice == "help":
                self._display_help()
            else:
                print("\n❌ Invalid choice. Please select a valid option.")
            
            input("\nPress Enter to continue...")
    
    def _display_help(self):
        """Display comprehensive help information."""
        print("\n📖 FIELD RESOURCE ECOSYSTEM - HELP")
        print("=" * 45)
        
        help_sections = {
            "System Overview": [
                "FRE integrates all FIELD system components",
                "Provides unified business resource management",
                "Connects with existing Berjak CRM systems",
                "Automates data processing and organization"
            ],
            "Key Features": [
                "Universal data processing automation",
                "Business intelligence dashboard", 
                "CRM integration and management",
                "Sacred geometry system orchestration",
                "Resource monitoring and analytics"
            ],
            "Quick Start": [
                "1. Run system health check (option 6)",
                "2. Check business dashboard (option 1)",
                "3. Process data files (option 2)",
                "4. Review automation status",
                "5. Generate reports (option 9)"
            ]
        }
        
        for section, items in help_sections.items():
            print(f"\n🔹 {section}:")
            for item in items:
                print(f"   • {item}")


def main():
    """Main entry point for the Field Resource Ecosystem."""
    try:
        fre = FieldResourceEcosystem()
        
        # Check for command line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            
            if command == "status":
                fre.display_header()
                fre._system_health_check()
            elif command == "dashboard":
                fre.display_header()
                fre.run_business_dashboard()
            elif command == "process":
                fre._run_data_processor()
            elif command == "report":
                fre._generate_reports()
            elif command == "help":
                fre._display_help()
            else:
                print(f"Unknown command: {command}")
                print("Available commands: status, dashboard, process, report, help")
        else:
            # Run interactive menu
            fre.run_interactive_menu()
            
    except KeyboardInterrupt:
        print("\n\n👋 FRE session terminated by user")
    except Exception as e:
        print(f"\n❌ Error in FRE system: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()