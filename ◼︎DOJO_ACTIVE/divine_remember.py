#!/usr/bin/env python3
"""
🧠✨ Divine Remember - Sacred Memory Keeper ✨🧠
Never lose track of what you were working on again
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import sys
import os

class DivineRemember:
    """Sacred memory keeper for tracking work context"""
    
    def __init__(self):
        self.dojo_active = Path("/Users/jbear/FIELD/◼︎DOJO_ACTIVE")
        self.memory_db = self.dojo_active / "divine_memory.db"
        self.init_memory_db()
    
    def init_memory_db(self):
        """Initialize the sacred memory database"""
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_sessions (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                intention TEXT,
                context TEXT,
                files_accessed TEXT,
                completed INTEGER DEFAULT 0,
                notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quick_thoughts (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                thought TEXT,
                tags TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_intention(self, intention: str, context: str = ""):
        """Log what you're about to work on"""
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO work_sessions (timestamp, intention, context, notes)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().timestamp(),
            intention,
            context,
            f"Started at {datetime.now().strftime('%H:%M')}"
        ))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"🎯 Intention logged: {intention}")
        print(f"📝 Session ID: {session_id}")
        
        return session_id
    
    def complete_session(self, session_id: int, notes: str = ""):
        """Mark a work session as completed"""
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE work_sessions 
            SET completed = 1, notes = notes || ? 
            WHERE id = ?
        ''', (f"\nCompleted: {notes}", session_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Session {session_id} marked complete")
    
    def quick_thought(self, thought: str, tags: str = ""):
        """Capture a quick thought or idea"""
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quick_thoughts (timestamp, thought, tags)
            VALUES (?, ?, ?)
        ''', (
            datetime.now().timestamp(),
            thought,
            tags
        ))
        
        conn.commit()
        conn.close()
        
        print(f"💭 Thought captured: {thought[:50]}...")
    
    def what_was_i_doing(self, hours_back: int = 8):
        """Show what you were working on recently"""
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cutoff_time = (datetime.now() - timedelta(hours=hours_back)).timestamp()
        
        cursor.execute('''
            SELECT id, timestamp, intention, context, completed, notes
            FROM work_sessions 
            WHERE timestamp > ?
            ORDER BY timestamp DESC
            LIMIT 10
        ''', (cutoff_time,))
        
        sessions = cursor.fetchall()
        
        cursor.execute('''
            SELECT timestamp, thought, tags
            FROM quick_thoughts
            WHERE timestamp > ?
            ORDER BY timestamp DESC
            LIMIT 5
        ''', (cutoff_time,))
        
        thoughts = cursor.fetchall()
        
        conn.close()
        
        print(f"🧠 What you were working on (last {hours_back} hours):")
        print("=" * 60)
        
        if sessions:
            for session in sessions:
                session_id, timestamp, intention, context, completed, notes = session
                time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M")
                status = "✅" if completed else "🔄"
                
                print(f"\n{status} [{time_str}] Session {session_id}")
                print(f"🎯 {intention}")
                if context:
                    print(f"📋 Context: {context}")
                if notes:
                    print(f"📝 {notes}")
        
        if thoughts:
            print(f"\n💭 Quick thoughts:")
            for timestamp, thought, tags in thoughts:
                time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M")
                print(f"   [{time_str}] {thought}")
                if tags:
                    print(f"            Tags: {tags}")
        
        if not sessions and not thoughts:
            print("🤔 No recent activity found. Time to log an intention!")
        
        return sessions, thoughts
    
    def current_focus(self):
        """Show your current/most recent focus"""
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        # Get the most recent incomplete session
        cursor.execute('''
            SELECT id, timestamp, intention, context, notes
            FROM work_sessions 
            WHERE completed = 0
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        
        current = cursor.fetchone()
        conn.close()
        
        if current:
            session_id, timestamp, intention, context, notes = current
            time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
            
            print("🎯 Current Focus:")
            print("=" * 40)
            print(f"Session: {session_id}")
            print(f"Started: {time_str}")
            print(f"Intention: {intention}")
            if context:
                print(f"Context: {context}")
            if notes:
                print(f"Notes: {notes}")
            
            return session_id, intention
        else:
            print("🤷 No current focus. What would you like to work on?")
            return None, None
    
    def search_memory(self, query: str):
        """Search through your work history"""
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, intention, context, completed, notes
            FROM work_sessions 
            WHERE intention LIKE ? OR context LIKE ? OR notes LIKE ?
            ORDER BY timestamp DESC
            LIMIT 20
        ''', (f"%{query}%", f"%{query}%", f"%{query}%"))
        
        sessions = cursor.fetchall()
        
        cursor.execute('''
            SELECT timestamp, thought, tags
            FROM quick_thoughts
            WHERE thought LIKE ? OR tags LIKE ?
            ORDER BY timestamp DESC
            LIMIT 10
        ''', (f"%{query}%", f"%{query}%"))
        
        thoughts = cursor.fetchall()
        
        conn.close()
        
        print(f"🔍 Memory search for '{query}':")
        print("=" * 50)
        
        if sessions:
            print("\n📋 Work Sessions:")
            for session in sessions:
                session_id, timestamp, intention, context, completed, notes = session
                time_str = datetime.fromtimestamp(timestamp).strftime("%m-%d %H:%M")
                status = "✅" if completed else "🔄"
                
                print(f"  {status} [{time_str}] {intention}")
        
        if thoughts:
            print("\n💭 Thoughts:")
            for timestamp, thought, tags in thoughts:
                time_str = datetime.fromtimestamp(timestamp).strftime("%m-%d %H:%M")
                print(f"  [{time_str}] {thought}")
        
        if not sessions and not thoughts:
            print(f"🤔 No memories found for '{query}'")

def main():
    """Divine Remember command line interface"""
    
    remember = DivineRemember()
    
    if len(sys.argv) < 2:
        print("🧠✨ Divine Remember - Sacred Memory Keeper")
        print()
        print("Usage:")
        print("  remember start 'intention' ['context']  - Log what you're starting")
        print("  remember done <session_id> ['notes']   - Mark session complete") 
        print("  remember think 'thought' ['tags']      - Capture quick thought")
        print("  remember what                          - What was I doing?")
        print("  remember focus                         - Current focus")
        print("  remember search 'query'                - Search memory")
        print()
        print("Examples:")
        print("  remember start 'Fix the login bug' 'user auth system'")
        print("  remember think 'Need to check email server logs' 'debugging'")
        print("  remember what")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        if len(sys.argv) < 3:
            print("❌ Usage: remember start 'intention' ['context']")
            return
        
        intention = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        remember.log_intention(intention, context)
    
    elif command == "done":
        if len(sys.argv) < 3:
            print("❌ Usage: remember done <session_id> ['notes']")
            return
        
        try:
            session_id = int(sys.argv[2])
            notes = sys.argv[3] if len(sys.argv) > 3 else ""
            remember.complete_session(session_id, notes)
        except ValueError:
            print("❌ Session ID must be a number")
    
    elif command == "think":
        if len(sys.argv) < 3:
            print("❌ Usage: remember think 'thought' ['tags']")
            return
        
        thought = sys.argv[2]
        tags = sys.argv[3] if len(sys.argv) > 3 else ""
        remember.quick_thought(thought, tags)
    
    elif command == "what":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        remember.what_was_i_doing(hours)
    
    elif command == "focus":
        remember.current_focus()
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Usage: remember search 'query'")
            return
        
        query = sys.argv[2]
        remember.search_memory(query)
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()