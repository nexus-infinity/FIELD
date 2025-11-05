#!/usr/bin/env python3
"""
Test script for Fractal Contact Intelligence Suite
Verifies all components are working correctly
"""

import os
import sys
from pathlib import Path
import subprocess

def test_applescript_availability():
    """Test if AppleScript is available and working"""
    print("🧪 Testing AppleScript availability...")
    try:
        result = subprocess.run(
            ["osascript", "-e", 'return "AppleScript is working"'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ AppleScript is working")
            return True
        else:
            print(f"❌ AppleScript error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Cannot run AppleScript: {e}")
        return False

def test_contacts_access():
    """Test if we can access the Contacts app"""
    print("\n🧪 Testing Contacts app access...")
    test_script = '''
    try
        tell application "Contacts"
            set contactCount to count of every person
            return "Found " & contactCount & " contacts"
        end tell
    on error errMsg
        return "Error: " & errMsg
    end try
    '''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", test_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ Contacts access working: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Cannot access Contacts: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Contacts access timed out - database might be too large")
        return False
    except Exception as e:
        print(f"❌ Error accessing Contacts: {e}")
        return False

def test_file_paths():
    """Test if all required files exist"""
    print("\n🧪 Testing file paths...")
    
    script_dir = Path(__file__).parent
    files_to_check = [
        ("Python wrapper", script_dir / "fractal_contact_wrapper.py"),
        ("AppleScript v4.4", script_dir / "fractal_contact_intelligence_v4.4.applescript"),
    ]
    
    all_good = True
    for name, path in files_to_check:
        if path.exists():
            print(f"✅ {name}: {path.name}")
        else:
            print(f"❌ {name} not found: {path}")
            all_good = False
    
    return all_good

def test_database_access():
    """Test if we can access the Akron database path"""
    print("\n🧪 Testing database access...")
    
    db_dir = Path("/Volumes/Akron/bear_data")
    if db_dir.exists():
        print(f"✅ Database directory exists: {db_dir}")
        
        # Check write permissions
        test_file = db_dir / ".test_write"
        try:
            test_file.touch()
            test_file.unlink()
            print("✅ Database directory is writable")
            return True
        except Exception as e:
            print(f"⚠️  Database directory is read-only: {e}")
            return True  # Still OK, just read-only
    else:
        print(f"⚠️  Database directory not found: {db_dir}")
        print("    The system will work but won't save to database")
        return True  # Not critical

def test_mini_analysis():
    """Run a minimal contact analysis test"""
    print("\n🧪 Running minimal analysis test...")
    
    mini_script = '''
    -- Minimal test - just check first contact
    try
        tell application "Contacts"
            set contactCount to count of every person
            if contactCount > 0 then
                set firstContact to first person
                try
                    set contactName to name of firstContact
                on error
                    set contactName to "Unnamed"
                end try
                return "Success: First contact is " & contactName
            else
                return "No contacts in database"
            end if
        end tell
    on error errMsg
        return "Error: " & errMsg
    end try
    '''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", mini_script],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ Mini analysis successful: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Mini analysis failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Mini analysis error: {e}")
        return False

def main():
    print("=" * 60)
    print("🔬 FRACTAL CONTACT INTELLIGENCE SYSTEM TEST")
    print("=" * 60)
    
    tests = [
        ("AppleScript", test_applescript_availability),
        ("File Paths", test_file_paths),
        ("Contacts Access", test_contacts_access),
        ("Database Access", test_database_access),
        ("Mini Analysis", test_mini_analysis),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            results.append((name, test_func()))
        except Exception as e:
            print(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready to use.")
        print("\nTo run the full analysis:")
        print("  python3 fractal_contact_wrapper.py --analyze --report")
    elif passed >= 3:
        print("\n⚠️  Some tests failed but the system should still work.")
        print("Check the failed tests above for details.")
    else:
        print("\n❌ Critical tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
