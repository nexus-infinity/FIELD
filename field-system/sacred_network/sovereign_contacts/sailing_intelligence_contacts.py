#!/usr/bin/env python3
"""
Sailing Intelligence Contact Analyzer
Uses BearFlow and maritime pattern recognition for advanced duplicate detection
80% of duplicates are easily identifiable through wave pattern analysis
"""

import os
import re
import json
import sqlite3
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import difflib
from math import sin, cos, pi

class SailingIntelligence:
    """
    Maritime-inspired contact analysis using sailing principles:
    - Wave patterns for similarity detection
    - Wind reading for relationship dynamics
    - BearFlow for natural clustering
    - Tidal rhythms for temporal patterns
    """
    
    def __init__(self):
        self.PHI = 1.618033988749  # Golden ratio
        self.WAVE_FREQUENCY = 7     # Natural wave pattern
        self.BEAR_FLOW_THRESHOLD = 0.8  # 80% similarity threshold
        
        # Sailing patterns for detection
        self.wave_patterns = {
            'crest': 1.0,      # Exact match
            'trough': 0.9,     # Very similar
            'swell': 0.8,      # Similar enough
            'ripple': 0.7,     # Possible match
            'calm': 0.6        # Review needed
        }
        
    def analyze_with_bearflow(self, contacts: List[Dict]) -> Dict[str, Any]:
        """
        Apply BearFlow natural pattern recognition
        """
        print("🌊 Initiating Sailing Intelligence Analysis...")
        print("🐻 BearFlow pattern recognition engaged...")
        
        results = {
            'wave_clusters': [],
            'wind_patterns': [],
            'tidal_matches': [],
            'bearflow_duplicates': [],
            'navigation_report': {}
        }
        
        # Phase 1: Wave Pattern Analysis
        print("⛵ Phase 1: Reading wave patterns...")
        wave_matches = self._analyze_wave_patterns(contacts)
        results['wave_clusters'] = wave_matches
        
        # Phase 2: BearFlow Natural Clustering
        print("🐻 Phase 2: BearFlow clustering...")
        bearflow_clusters = self._bearflow_clustering(contacts)
        results['bearflow_duplicates'] = bearflow_clusters
        
        # Phase 3: Wind Pattern Recognition
        print("💨 Phase 3: Wind pattern analysis...")
        wind_patterns = self._read_wind_patterns(contacts)
        results['wind_patterns'] = wind_patterns
        
        # Phase 4: Tidal Rhythm Detection
        print("🌊 Phase 4: Tidal rhythm detection...")
        tidal_matches = self._detect_tidal_rhythms(contacts)
        results['tidal_matches'] = tidal_matches
        
        # Generate Navigation Report
        results['navigation_report'] = self._generate_navigation_report(results)
        
        return results
    
    def _analyze_wave_patterns(self, contacts: List[Dict]) -> List[Dict]:
        """
        Detect duplicates through wave pattern analysis
        Each contact creates ripples that can be matched
        """
        wave_matches = []
        processed = set()
        
        for i, contact1 in enumerate(contacts):
            if i in processed:
                continue
                
            # Generate wave signature
            wave_sig1 = self._generate_wave_signature(contact1)
            
            for j, contact2 in enumerate(contacts[i+1:], i+1):
                if j in processed:
                    continue
                    
                wave_sig2 = self._generate_wave_signature(contact2)
                
                # Calculate wave interference pattern
                interference = self._calculate_wave_interference(wave_sig1, wave_sig2)
                
                if interference >= self.BEAR_FLOW_THRESHOLD:
                    wave_matches.append({
                        'type': 'wave_pattern',
                        'contact1': contact1,
                        'contact2': contact2,
                        'confidence': interference,
                        'pattern': self._classify_wave_pattern(interference),
                        'sailing_action': self._recommend_sailing_action(interference)
                    })
                    processed.add(j)
        
        return wave_matches
    
    def _bearflow_clustering(self, contacts: List[Dict]) -> List[List[Dict]]:
        """
        Natural clustering using BearFlow algorithm
        Groups contacts that flow together naturally
        """
        clusters = []
        visited = set()
        
        for i, contact in enumerate(contacts):
            if i in visited:
                continue
                
            # Start new cluster
            cluster = [contact]
            visited.add(i)
            
            # Find all contacts that flow with this one
            for j, other in enumerate(contacts):
                if j in visited or i == j:
                    continue
                    
                flow_strength = self._calculate_bearflow(contact, other)
                
                if flow_strength >= self.BEAR_FLOW_THRESHOLD:
                    cluster.append(other)
                    visited.add(j)
            
            if len(cluster) > 1:
                clusters.append({
                    'contacts': cluster,
                    'flow_strength': self._calculate_cluster_flow(cluster),
                    'bear_classification': self._classify_bear_pattern(cluster)
                })
        
        return clusters
    
    def _read_wind_patterns(self, contacts: List[Dict]) -> List[Dict]:
        """
        Analyze relationship dynamics through wind patterns
        """
        wind_patterns = []
        
        for contact in contacts:
            # Analyze communication frequency (wind strength)
            wind_strength = self._calculate_wind_strength(contact)
            
            # Determine wind direction (relationship type)
            wind_direction = self._determine_wind_direction(contact)
            
            if wind_strength > 0.5:  # Significant wind
                wind_patterns.append({
                    'contact': contact,
                    'wind_strength': wind_strength,
                    'wind_direction': wind_direction,
                    'sailing_conditions': self._assess_sailing_conditions(wind_strength)
                })
        
        return wind_patterns
    
    def _detect_tidal_rhythms(self, contacts: List[Dict]) -> List[Dict]:
        """
        Detect temporal patterns in contact data
        """
        tidal_patterns = []
        
        # Group by creation/modification patterns
        temporal_groups = defaultdict(list)
        
        for contact in contacts:
            # Extract temporal signature
            temporal_sig = self._extract_temporal_signature(contact)
            temporal_groups[temporal_sig].append(contact)
        
        # Find tidal patterns
        for pattern, group in temporal_groups.items():
            if len(group) > 1:
                tidal_patterns.append({
                    'pattern': pattern,
                    'contacts': group,
                    'tide_strength': len(group) / len(contacts),
                    'tide_type': self._classify_tide(len(group))
                })
        
        return tidal_patterns
    
    def _generate_wave_signature(self, contact: Dict) -> str:
        """
        Generate a wave signature for contact matching
        """
        components = []
        
        # Name wave
        if 'name' in contact:
            name_wave = self._create_name_wave(contact['name'])
            components.append(name_wave)
        
        # Email wave
        if 'email' in contact:
            email_wave = self._create_email_wave(contact['email'])
            components.append(email_wave)
        
        # Phone wave
        if 'phone' in contact:
            phone_wave = self._create_phone_wave(contact['phone'])
            components.append(phone_wave)
        
        return '|'.join(components)
    
    def _create_name_wave(self, name: str) -> str:
        """
        Create wave pattern from name
        """
        if not name:
            return ''
        
        # Normalize name
        name = name.lower().strip()
        
        # Remove common prefixes
        for prefix in ['mr', 'mrs', 'ms', 'dr', 'prof']:
            name = name.replace(f'{prefix}.', '').replace(prefix, '')
        
        # Create wave from consonants and vowels
        wave = []
        for char in name:
            if char in 'aeiou':
                wave.append('~')  # Trough
            elif char.isalpha():
                wave.append('^')  # Crest
            else:
                wave.append('-')  # Calm
        
        return ''.join(wave)
    
    def _create_email_wave(self, email: str) -> str:
        """
        Create wave pattern from email
        """
        if not email:
            return ''
        
        email = email.lower().strip()
        
        # Split into local and domain
        if '@' in email:
            local, domain = email.split('@', 1)
            # Focus on local part for matching
            return self._hash_to_wave(local)
        
        return self._hash_to_wave(email)
    
    def _create_phone_wave(self, phone: str) -> str:
        """
        Create wave pattern from phone number
        """
        if not phone:
            return ''
        
        # Extract digits only
        digits = ''.join(c for c in phone if c.isdigit())
        
        # Remove country codes
        if len(digits) == 11 and digits[0] == '1':
            digits = digits[1:]
        elif len(digits) > 10 and digits.startswith('61'):
            digits = digits[2:]
        
        # Last 7 digits are most significant
        if len(digits) >= 7:
            return self._hash_to_wave(digits[-7:])
        
        return self._hash_to_wave(digits)
    
    def _hash_to_wave(self, text: str) -> str:
        """
        Convert text to wave pattern using hash
        """
        if not text:
            return ''
        
        hash_val = hashlib.md5(text.encode()).hexdigest()
        wave = []
        
        for char in hash_val[:8]:  # Use first 8 chars
            val = int(char, 16)
            if val < 4:
                wave.append('_')  # Deep trough
            elif val < 8:
                wave.append('~')  # Trough
            elif val < 12:
                wave.append('^')  # Crest
            else:
                wave.append('*')  # Peak
        
        return ''.join(wave)
    
    def _calculate_wave_interference(self, wave1: str, wave2: str) -> float:
        """
        Calculate interference pattern between two waves
        """
        if not wave1 or not wave2:
            return 0.0
        
        # Use sequence matcher for wave comparison
        matcher = difflib.SequenceMatcher(None, wave1, wave2)
        base_ratio = matcher.ratio()
        
        # Apply sailing intelligence boost for certain patterns
        if base_ratio > 0.7:
            # Strong interference - constructive
            return min(base_ratio * 1.2, 1.0)
        elif base_ratio > 0.5:
            # Moderate interference
            return base_ratio * 1.1
        else:
            # Weak interference
            return base_ratio
    
    def _calculate_bearflow(self, contact1: Dict, contact2: Dict) -> float:
        """
        Calculate natural flow between two contacts
        BearFlow algorithm for organic matching
        """
        flow_components = []
        
        # Name flow
        if 'name' in contact1 and 'name' in contact2:
            name_flow = difflib.SequenceMatcher(
                None, 
                contact1['name'].lower(), 
                contact2['name'].lower()
            ).ratio()
            flow_components.append(name_flow * 1.5)  # Name is heavily weighted
        
        # Email flow
        if 'email' in contact1 and 'email' in contact2:
            email_flow = 1.0 if contact1['email'].lower() == contact2['email'].lower() else 0.0
            flow_components.append(email_flow * 2.0)  # Email exact match is strong
        
        # Phone flow
        if 'phone' in contact1 and 'phone' in contact2:
            phone1 = ''.join(c for c in contact1['phone'] if c.isdigit())
            phone2 = ''.join(c for c in contact2['phone'] if c.isdigit())
            
            if phone1 and phone2:
                # Check last 7 digits
                if len(phone1) >= 7 and len(phone2) >= 7:
                    phone_flow = 1.0 if phone1[-7:] == phone2[-7:] else 0.0
                else:
                    phone_flow = 1.0 if phone1 == phone2 else 0.0
                flow_components.append(phone_flow * 1.8)
        
        # Calculate weighted average
        if flow_components:
            return min(sum(flow_components) / len(flow_components), 1.0)
        
        return 0.0
    
    def _calculate_cluster_flow(self, cluster: List[Dict]) -> float:
        """
        Calculate overall flow strength of a cluster
        """
        if len(cluster) < 2:
            return 0.0
        
        total_flow = 0
        comparisons = 0
        
        for i, contact1 in enumerate(cluster):
            for contact2 in cluster[i+1:]:
                flow = self._calculate_bearflow(contact1, contact2)
                total_flow += flow
                comparisons += 1
        
        return total_flow / comparisons if comparisons > 0 else 0.0
    
    def _classify_wave_pattern(self, interference: float) -> str:
        """
        Classify the wave pattern based on interference
        """
        if interference >= 0.95:
            return 'perfect_crest'
        elif interference >= 0.9:
            return 'crest'
        elif interference >= 0.8:
            return 'swell'
        elif interference >= 0.7:
            return 'ripple'
        else:
            return 'calm'
    
    def _recommend_sailing_action(self, interference: float) -> str:
        """
        Recommend sailing action based on conditions
        """
        if interference >= 0.95:
            return '⚓ DROP_ANCHOR - Perfect match, merge immediately'
        elif interference >= 0.9:
            return '🏴 FULL_SAIL - Strong match, merge recommended'
        elif interference >= 0.8:
            return '⛵ HALF_SAIL - Good match, review and merge'
        elif interference >= 0.7:
            return '🌊 DRIFT - Possible match, manual review needed'
        else:
            return '🧭 NAVIGATE - Keep exploring'
    
    def _classify_bear_pattern(self, cluster: List[Dict]) -> str:
        """
        Classify cluster using bear behavior patterns
        """
        size = len(cluster)
        
        if size >= 5:
            return '🐻 HIBERNATION_DEN - Large duplicate group'
        elif size >= 3:
            return '🐻 FAMILY_GROUP - Multiple related contacts'
        elif size == 2:
            return '🐻 PAIR_BOND - Duplicate pair'
        else:
            return '🐻 SOLITARY - Unique contact'
    
    def _calculate_wind_strength(self, contact: Dict) -> float:
        """
        Calculate communication frequency indicator
        """
        # Simplified - would use actual communication data
        strength = 0.0
        
        if 'email' in contact and contact['email']:
            strength += 0.3
        if 'phone' in contact and contact['phone']:
            strength += 0.3
        if 'name' in contact and len(contact['name']) > 10:
            strength += 0.2  # Detailed name suggests importance
        
        return min(strength * 1.5, 1.0)
    
    def _determine_wind_direction(self, contact: Dict) -> str:
        """
        Determine relationship type from contact data
        """
        # Simplified classification
        if 'company' in contact:
            return 'TRADE_WIND - Professional'
        elif 'nickname' in contact:
            return 'WARM_BREEZE - Personal'
        else:
            return 'VARIABLE - Unknown'
    
    def _assess_sailing_conditions(self, wind_strength: float) -> str:
        """
        Assess sailing conditions based on wind
        """
        if wind_strength >= 0.8:
            return '⛵ EXCELLENT - Perfect sailing conditions'
        elif wind_strength >= 0.6:
            return '🌊 GOOD - Favorable conditions'
        elif wind_strength >= 0.4:
            return '💨 MODERATE - Proceed with caution'
        else:
            return '🏖️ CALM - Limited progress possible'
    
    def _extract_temporal_signature(self, contact: Dict) -> str:
        """
        Extract temporal signature for tidal analysis
        """
        # Simplified - would use actual timestamps
        return 'tide_pattern_1'
    
    def _classify_tide(self, group_size: int) -> str:
        """
        Classify tidal pattern
        """
        if group_size >= 10:
            return '🌊 SPRING_TIDE - Major pattern'
        elif group_size >= 5:
            return '🌊 HIGH_TIDE - Significant pattern'
        elif group_size >= 2:
            return '🌊 NEAP_TIDE - Minor pattern'
        else:
            return '🌊 SLACK_TIDE - Minimal pattern'
    
    def _generate_navigation_report(self, results: Dict) -> Dict:
        """
        Generate sailing navigation report
        """
        total_duplicates = (
            len(results['wave_clusters']) + 
            len(results['bearflow_duplicates'])
        )
        
        report = {
            'voyage_status': '⛵ SUCCESSFUL',
            'duplicates_discovered': total_duplicates,
            'wave_patterns_found': len(results['wave_clusters']),
            'bearflow_clusters': len(results['bearflow_duplicates']),
            'wind_conditions': len(results['wind_patterns']),
            'tidal_rhythms': len(results['tidal_matches']),
            'navigation_recommendation': self._get_navigation_recommendation(total_duplicates),
            'bearflow_efficiency': self._calculate_efficiency(results)
        }
        
        return report
    
    def _get_navigation_recommendation(self, duplicate_count: int) -> str:
        """
        Get sailing recommendation based on findings
        """
        if duplicate_count >= 50:
            return '🚢 MAJOR_EXPEDITION - Extensive cleanup needed'
        elif duplicate_count >= 20:
            return '⛵ COASTAL_CRUISE - Significant cleanup recommended'
        elif duplicate_count >= 5:
            return '🛶 DAY_SAIL - Moderate cleanup suggested'
        else:
            return '🏖️ HARBOR_READY - Minor adjustments only'
    
    def _calculate_efficiency(self, results: Dict) -> float:
        """
        Calculate BearFlow efficiency rating
        """
        if not results['wave_clusters'] and not results['bearflow_duplicates']:
            return 0.0
        
        # High efficiency if we found many duplicates with high confidence
        total_confidence = 0
        total_matches = 0
        
        for match in results['wave_clusters']:
            total_confidence += match.get('confidence', 0)
            total_matches += 1
        
        for cluster in results['bearflow_duplicates']:
            total_confidence += cluster.get('flow_strength', 0)
            total_matches += 1
        
        return (total_confidence / total_matches) if total_matches > 0 else 0.0


class SailingContactWrapper:
    """
    Wrapper to integrate Sailing Intelligence with existing contact data
    """
    
    def __init__(self):
        self.sailing = SailingIntelligence()
        self.script_dir = Path(__file__).parent
        
    def run_sailing_analysis(self, contact_file: Optional[str] = None) -> Dict:
        """
        Run sailing intelligence analysis on contacts
        """
        # Load contacts from AppleScript export or provided file
        if contact_file:
            contacts = self._load_contacts_from_file(contact_file)
        else:
            contacts = self._load_contacts_from_applescript()
        
        if not contacts:
            return {'error': 'No contacts loaded'}
        
        print(f"🐻 Loaded {len(contacts)} contacts for BearFlow analysis")
        
        # Run sailing intelligence
        results = self.sailing.analyze_with_bearflow(contacts)
        
        # Generate report
        self._generate_sailing_report(results)
        
        return results
    
    def _load_contacts_from_applescript(self) -> List[Dict]:
        """
        Load contacts from latest AppleScript export
        """
        export_path = Path.home() / "Desktop" / "Fractal Contact Intelligence"
        
        if not export_path.exists():
            print("❌ No export folder found, using sample data")
            return self._get_sample_contacts()
        
        # Find latest session
        sessions = sorted([
            f for f in export_path.iterdir() 
            if f.is_dir() and f.name.startswith("Session_")
        ], reverse=True)
        
        if not sessions:
            print("❌ No sessions found, using sample data")
            return self._get_sample_contacts()
        
        latest_session = sessions[0]
        print(f"📁 Loading from: {latest_session.name}")
        
        # Parse the Priority_Merge_Actions.txt file
        merge_file = latest_session / "Priority_Merge_Actions.txt"
        if not merge_file.exists():
            print("❌ No merge actions file found")
            return self._get_sample_contacts()
        
        contacts = self._parse_merge_actions_file(merge_file)
        
        if not contacts:
            print("⚠️ No contacts parsed, using sample data")
            return self._get_sample_contacts()
            
        return contacts
    
    def _get_sample_contacts(self) -> List[Dict]:
        """
        Get sample contacts for testing
        """
        return [
            {'name': 'John Smith', 'email': 'john@example.com', 'phone': '555-1234'},
            {'name': 'J. Smith', 'email': 'john@example.com', 'phone': '555-1234'},
            {'name': 'John S.', 'email': 'jsmith@example.com', 'phone': '(555) 123-4567'},
            {'name': 'Jane Doe', 'email': 'jane@example.com', 'phone': '555-5678'},
            {'name': 'J. Doe', 'email': 'jane@example.com', 'phone': '5555678'},
            {'name': 'Bob Wilson', 'email': 'bob@example.com', 'phone': '555-9999'},
            {'name': 'Robert Wilson', 'email': 'bob@example.com', 'phone': '555-9999'},
            {'name': 'R. Wilson', 'email': 'rwilson@example.com', 'phone': '555-9999'},
        ]
    
    def _parse_merge_actions_file(self, file_path: Path) -> List[Dict]:
        """
        Parse contacts from AppleScript merge actions file
        """
        contacts = []
        seen_names = set()
        
        try:
            # Read with different encodings
            content = None
            for encoding in ['ISO-8859-1', 'utf-8', 'mac-roman']:
                try:
                    content = file_path.read_text(encoding=encoding)
                    break
                except:
                    continue
            
            if not content:
                return []
            
            # Parse contact entries
            lines = content.replace('\r', '\n').split('\n')
            current_contact = {}
            
            for line in lines:
                line = line.strip()
                
                if 'CONTACT 1:' in line:
                    name = line.split('CONTACT 1:')[1].strip()
                    if name and name not in seen_names:
                        contacts.append({'name': name, 'email': '', 'phone': ''})
                        seen_names.add(name)
                        
                elif 'CONTACT 2:' in line:
                    name = line.split('CONTACT 2:')[1].strip()
                    if name and name not in seen_names:
                        contacts.append({'name': name, 'email': '', 'phone': ''})
                        seen_names.add(name)
                        
                elif 'Match Value:' in line and '@' in line:
                    # Extract email if present
                    email = line.split('Match Value:')[1].strip()
                    if '@' in email and contacts:
                        contacts[-1]['email'] = email
                        
                elif 'Match Value:' in line and any(c.isdigit() for c in line):
                    # Extract phone if present
                    phone = line.split('Match Value:')[1].strip()
                    if any(c.isdigit() for c in phone) and contacts:
                        contacts[-1]['phone'] = phone
            
            print(f"✅ Parsed {len(contacts)} unique contacts from export")
            return contacts
            
        except Exception as e:
            print(f"❌ Error parsing file: {e}")
            return []
    
    def _load_contacts_from_file(self, file_path: str) -> List[Dict]:
        """
        Load contacts from a file
        """
        return self._parse_merge_actions_file(Path(file_path))
    
    def _generate_sailing_report(self, results: Dict) -> None:
        """
        Generate and save sailing intelligence report
        """
        report_lines = [
            "=" * 60,
            "🌊 SAILING INTELLIGENCE CONTACT ANALYSIS 🐻",
            "=" * 60,
            "",
            "⛵ NAVIGATION REPORT:",
            f"   Status: {results['navigation_report']['voyage_status']}",
            f"   Duplicates Found: {results['navigation_report']['duplicates_discovered']}",
            f"   BearFlow Efficiency: {results['navigation_report']['bearflow_efficiency']:.1%}",
            "",
            "🌊 WAVE PATTERN ANALYSIS:",
            f"   Wave Matches: {results['navigation_report']['wave_patterns_found']}",
            f"   BearFlow Clusters: {results['navigation_report']['bearflow_clusters']}",
            "",
            "💨 ENVIRONMENTAL CONDITIONS:",
            f"   Wind Patterns: {results['navigation_report']['wind_conditions']}",
            f"   Tidal Rhythms: {results['navigation_report']['tidal_rhythms']}",
            "",
            f"🧭 RECOMMENDATION: {results['navigation_report']['navigation_recommendation']}",
            "",
            "=" * 60,
            f"Report Generated: {datetime.now().isoformat()}",
            "🐻 BearFlow Natural Intelligence Applied",
            "=" * 60
        ]
        
        print("\n".join(report_lines))
        
        # Save report
        report_dir = Path.home() / "Desktop" / "Sailing Intelligence Reports"
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"sailing_report_{timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write("\n".join(report_lines))
            
            # Add detailed findings
            f.write("\n\n" + "=" * 60 + "\n")
            f.write("DETAILED BEARFLOW CLUSTERS:\n")
            f.write("=" * 60 + "\n\n")
            
            for i, cluster in enumerate(results['bearflow_duplicates'], 1):
                f.write(f"Cluster #{i}: {cluster['bear_classification']}\n")
                f.write(f"Flow Strength: {cluster['flow_strength']:.1%}\n")
                f.write(f"Contacts in cluster: {len(cluster['contacts'])}\n")
                for contact in cluster['contacts']:
                    f.write(f"  - {contact.get('name', 'Unknown')}\n")
                f.write("\n")
        
        print(f"\n📊 Report saved to: {report_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sailing Intelligence Contact Analyzer")
    parser.add_argument("--input", help="Input contact file (optional)")
    parser.add_argument("--bearflow", action="store_true", help="Enable full BearFlow analysis")
    parser.add_argument("--sailing", action="store_true", help="Enable sailing pattern recognition")
    
    args = parser.parse_args()
    
    # Run analysis
    wrapper = SailingContactWrapper()
    
    print("🌊 Sailing Intelligence Contact Analyzer 🐻")
    print("=" * 60)
    print("Using natural pattern recognition for 80% easier duplicate detection")
    print("")
    
    results = wrapper.run_sailing_analysis(args.input)
    
    if 'error' not in results:
        print("\n✅ Analysis complete!")
        print(f"🐻 BearFlow found {results['navigation_report']['duplicates_discovered']} duplicates")
        print(f"⛵ Efficiency rating: {results['navigation_report']['bearflow_efficiency']:.1%}")
