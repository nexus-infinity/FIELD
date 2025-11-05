#!/usr/bin/env python3
"""
🔍✨ Divine Find - Sacred Geometric Search ✨🔍
Instantly locate anything across your entire field using geometric resonance
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import subprocess
import re

class DivineFinder:
    """Sacred geometric search across the entire field"""
    
    def __init__(self):
        self.field_roots = [
            Path("/Users/jbear/FIELD"),
            Path("/Users/jbear/FIELD-LIVING"), 
            Path("/Users/jbear/FIELD-DEV"),
            Path("/Users/jbear"),  # Home directory
            Path("/Volumes")  # External drives
        ]
        
        self.dojo_active = Path("/Users/jbear/FIELD/◼︎DOJO_ACTIVE")
        self.sacred_index = self.dojo_active / "sacred_index.db"
        
        # Initialize sacred index
        self.init_sacred_index()
    
    def init_sacred_index(self):
        """Initialize the sacred geometric index"""
        
        conn = sqlite3.connect(self.sacred_index)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sacred_files (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE,
                name TEXT,
                type TEXT,
                size INTEGER,
                modified REAL,
                geometric_signature TEXT,
                semantic_tags TEXT,
                last_indexed REAL
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_name ON sacred_files(name);
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_type ON sacred_files(type);
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_tags ON sacred_files(semantic_tags);
        ''')
        
        conn.commit()
        conn.close()
    
    def divine_search(self, query: str, search_type: str = "all"):
        """Divine search using sacred geometric resonance"""
        
        print(f"🔍✨ Divine Search: '{query}' (type: {search_type})")
        
        # First, try instant recall from sacred index
        cached_results = self.search_sacred_index(query, search_type)
        
        # If index is empty or old, refresh it
        if not cached_results or self.needs_refresh():
            print("📡 Refreshing sacred geometric index...")
            self.refresh_sacred_index()
            cached_results = self.search_sacred_index(query, search_type)
        
        # Live search for anything very recent
        live_results = self.live_geometric_search(query, search_type)
        
        # Combine and deduplicate
        all_results = self.merge_results(cached_results, live_results)
        
        # Sort by geometric resonance
        sorted_results = self.sort_by_resonance(all_results, query)
        
        return sorted_results
    
    def search_sacred_index(self, query: str, search_type: str):
        """Search the sacred geometric index"""
        
        conn = sqlite3.connect(self.sacred_index)
        cursor = conn.cursor()
        
        # Build query based on type
        where_clauses = []
        params = []
        
        if search_type == "files":
            where_clauses.append("type NOT LIKE 'directory'")
        elif search_type == "folders":
            where_clauses.append("type = 'directory'")
        elif search_type == "photos":
            where_clauses.append("type IN ('jpg', 'jpeg', 'png', 'gif', 'heic', 'raw', 'tiff')")
        
        # Search in name and tags
        search_terms = query.lower().split()
        for term in search_terms:
            where_clauses.append("(LOWER(name) LIKE ? OR LOWER(semantic_tags) LIKE ?)")
            params.extend([f"%{term}%", f"%{term}%"])
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query_sql = f"""
            SELECT path, name, type, size, modified, geometric_signature, semantic_tags
            FROM sacred_files 
            WHERE {where_clause}
            ORDER BY last_indexed DESC
            LIMIT 50
        """
        
        cursor.execute(query_sql, params)
        results = cursor.fetchall()
        conn.close()
        
        return [self.format_result(r) for r in results]
    
    def live_geometric_search(self, query: str, search_type: str):
        """Live search using macOS spotlight and find"""
        
        results = []
        
        # Use mdfind (spotlight) for semantic search
        try:
            cmd = ["mdfind", "-name", query]
            if search_type == "photos":
                cmd = ["mdfind", "kMDItemKind == 'Image'", query]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                paths = result.stdout.strip().split('\n')
                for path in paths[:20]:  # Limit results
                    if path and Path(path).exists():
                        results.append(self.analyze_path(Path(path)))
        except:
            pass
        
        # Fallback: geometric find across field roots
        for root in self.field_roots:
            if not root.exists():
                continue
                
            try:
                # Use find for pattern matching (use real binary, not alias)
                cmd = ["/usr/bin/find", str(root), "-iname", f"*{query}*", "-type", "f"]
                if search_type == "folders":
                    cmd[-1] = "d"
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    paths = result.stdout.strip().split('\n')
                    for path in paths[:10]:  # Limit per root
                        if path and Path(path).exists():
                            results.append(self.analyze_path(Path(path)))
            except:
                continue
        
        return results
    
    def analyze_path(self, path: Path):
        """Analyze a path for geometric signature"""
        
        try:
            stat = path.stat()
            
            # Determine type
            if path.is_dir():
                file_type = "directory"
            else:
                file_type = path.suffix.lower().lstrip('.')
            
            # Generate geometric signature
            geometric_sig = self.generate_geometric_signature(path)
            
            # Generate semantic tags
            semantic_tags = self.generate_semantic_tags(path)
            
            return {
                'path': str(path),
                'name': path.name,
                'type': file_type,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'geometric_signature': geometric_sig,
                'semantic_tags': semantic_tags,
                'resonance_score': 1.0
            }
        except:
            return None
    
    def generate_geometric_signature(self, path: Path):
        """Generate sacred geometric signature for a file"""
        
        # Based on path structure and sacred symbols
        path_str = str(path)
        
        if "●OBI-WAN" in path_str:
            return "memory_node"
        elif "▲ATLAS" in path_str:
            return "intelligence_node"
        elif "▼TATA" in path_str:
            return "validation_node"
        elif "◼︎DOJO" in path_str:
            return "execution_node"
        elif "LIVING" in path_str:
            return "living_field"
        elif "DEV" in path_str:
            return "development_field"
        else:
            return "base_field"
    
    def generate_semantic_tags(self, path: Path):
        """Generate semantic tags for better finding"""
        
        tags = []
        
        # Based on file type
        if path.suffix.lower() in ['.py', '.js', '.go', '.rs']:
            tags.append("code")
        elif path.suffix.lower() in ['.md', '.txt', '.doc']:
            tags.append("document")
        elif path.suffix.lower() in ['.jpg', '.png', '.heic', '.gif']:
            tags.append("photo image")
        elif path.suffix.lower() in ['.mp4', '.mov', '.avi']:
            tags.append("video")
        elif path.suffix.lower() in ['.mp3', '.wav', '.m4a']:
            tags.append("audio")
        
        # Based on path components
        path_parts = str(path).lower()
        if "project" in path_parts:
            tags.append("project")
        if "config" in path_parts:
            tags.append("configuration")
        if "backup" in path_parts:
            tags.append("backup")
        if "archive" in path_parts:
            tags.append("archived")
        
        return " ".join(tags)
    
    def refresh_sacred_index(self):
        """Refresh the sacred geometric index"""
        
        conn = sqlite3.connect(self.sacred_index)
        cursor = conn.cursor()
        
        # Clear old entries
        cursor.execute("DELETE FROM sacred_files WHERE last_indexed < ?", 
                      (datetime.now().timestamp() - 86400,))  # Older than 1 day
        
        indexed_count = 0
        now = datetime.now().timestamp()
        
        for root in self.field_roots:
            if not root.exists():
                continue
            
            print(f"🌀 Indexing {root}...")
            
            try:
                for path in root.rglob("*"):
                    if indexed_count > 10000:  # Reasonable limit
                        break
                        
                    if path.name.startswith('.'):  # Skip hidden
                        continue
                    
                    result = self.analyze_path(path)
                    if result:
                        cursor.execute('''
                            INSERT OR REPLACE INTO sacred_files 
                            (path, name, type, size, modified, geometric_signature, semantic_tags, last_indexed)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            result['path'], result['name'], result['type'], result['size'],
                            result['modified'], result['geometric_signature'], 
                            result['semantic_tags'], now
                        ))
                        indexed_count += 1
                        
                        if indexed_count % 1000 == 0:
                            print(f"   📡 {indexed_count} items indexed...")
            except Exception as e:
                print(f"⚠️ Error indexing {root}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        print(f"✨ Sacred index refreshed with {indexed_count} items")
    
    def needs_refresh(self):
        """Check if sacred index needs refresh"""
        
        if not self.sacred_index.exists():
            return True
        
        # Check if index is older than 1 hour
        index_age = datetime.now().timestamp() - self.sacred_index.stat().st_mtime
        return index_age > 3600
    
    def merge_results(self, cached_results, live_results):
        """Merge and deduplicate results"""
        
        seen_paths = set()
        merged = []
        
        # Add cached results first (higher quality)
        for result in cached_results:
            if result['path'] not in seen_paths:
                seen_paths.add(result['path'])
                merged.append(result)
        
        # Add live results if not already seen
        for result in live_results:
            if result and result['path'] not in seen_paths:
                seen_paths.add(result['path'])
                merged.append(result)
        
        return merged
    
    def sort_by_resonance(self, results, query):
        """Sort results by geometric resonance with query"""
        
        query_lower = query.lower()
        
        def calculate_resonance(result):
            score = 0
            name_lower = result['name'].lower()
            
            # Exact match gets highest score
            if query_lower == name_lower:
                score += 100
            # Name starts with query
            elif name_lower.startswith(query_lower):
                score += 50
            # Query is in name
            elif query_lower in name_lower:
                score += 25
            
            # Boost for recent files
            age_days = (datetime.now().timestamp() - result['modified']) / 86400
            if age_days < 7:
                score += 10
            elif age_days < 30:
                score += 5
            
            # Boost for sacred geometry nodes
            if result['geometric_signature'] in ['memory_node', 'intelligence_node']:
                score += 5
            
            return score
        
        for result in results:
            result['resonance_score'] = calculate_resonance(result)
        
        return sorted(results, key=lambda x: x['resonance_score'], reverse=True)
    
    def format_result(self, result_tuple):
        """Format database result tuple"""
        
        if isinstance(result_tuple, tuple):
            path, name, type_, size, modified, geo_sig, tags = result_tuple
            return {
                'path': path,
                'name': name,
                'type': type_,
                'size': size,
                'modified': modified,
                'geometric_signature': geo_sig,
                'semantic_tags': tags,
                'resonance_score': 1.0
            }
        return result_tuple

def divine_find(query: str, search_type: str = "all", limit: int = 20):
    """Main divine find function"""
    
    finder = DivineFinder()
    results = finder.divine_search(query, search_type)
    
    print(f"\n🔍 Found {len(results)} results for '{query}':")
    print("=" * 80)
    
    for i, result in enumerate(results[:limit], 1):
        path = Path(result['path'])
        
        # Get file size in human readable format
        size = result['size']
        if size > 1024*1024*1024:
            size_str = f"{size/(1024*1024*1024):.1f}GB"
        elif size > 1024*1024:
            size_str = f"{size/(1024*1024):.1f}MB"
        elif size > 1024:
            size_str = f"{size/1024:.1f}KB"
        else:
            size_str = f"{size}B"
        
        # Format modified time
        mod_time = datetime.fromtimestamp(result['modified']).strftime("%Y-%m-%d %H:%M")
        
        # Sacred symbol for geometric signature
        geo_symbols = {
            'memory_node': '●',
            'intelligence_node': '▲', 
            'validation_node': '▼',
            'execution_node': '◼︎',
            'living_field': '🌱',
            'development_field': '🔧',
            'base_field': '⚪'
        }
        symbol = geo_symbols.get(result['geometric_signature'], '○')
        
        print(f"{i:2d}. {symbol} {result['name']}")
        print(f"    📍 {path.parent}")
        print(f"    📊 {size_str} | {mod_time} | {result['type']}")
        
        if result.get('semantic_tags'):
            print(f"    🏷️  {result['semantic_tags']}")
        
        print()
    
    if len(results) > limit:
        print(f"... and {len(results) - limit} more results")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🔍✨ Divine Find - Sacred Geometric Search")
        print("Usage: divine_find.py <query> [type]")
        print("Types: all, files, folders, photos")
        print("Examples:")
        print("  divine_find.py 'config'")
        print("  divine_find.py 'vacation' photos") 
        print("  divine_find.py 'project' folders")
        sys.exit(1)
    
    query = sys.argv[1]
    search_type = sys.argv[2] if len(sys.argv) > 2 else "all"
    
    divine_find(query, search_type)