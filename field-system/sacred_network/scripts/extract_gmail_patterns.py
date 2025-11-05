#!/usr/bin/env python3
"""Extract introduction patterns and collaboration flows from email"""

import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def extract_email_patterns():
    """Extract geometric patterns from email metadata"""
    patterns = {
        'introduction_patterns': [],
        'collaboration_flows': [],
        'frequency_mappings': {},
        'bridge_connections': []
    }
    
    # This would connect to Gmail API in production
    # For now, using mock data to demonstrate structure
    mock_emails = [
        {'from': 'alice@example.com', 'to': ['bob@example.com'], 'cc': ['charlie@example.com']},
        {'from': 'bob@example.com', 'to': ['alice@example.com', 'david@example.com']},
        {'from': 'charlie@example.com', 'to': ['alice@example.com'], 'cc': ['bob@example.com', 'eve@example.com']}
    ]
    
    # Extract introduction patterns
    introductions = defaultdict(list)
    for email in mock_emails:
        sender = email['from']
        for recipient in email.get('cc', []):
            if recipient not in email['to']:
                introductions[sender].append(recipient)
                patterns['introduction_patterns'].append({
                    'introducer': sender,
                    'introduced': recipient,
                    'timestamp': datetime.now().isoformat()
                })
    
    # Calculate collaboration flows
    collaborations = defaultdict(int)
    for email in mock_emails:
        sender = email['from']
        for recipient in email['to']:
            collaborations[(sender, recipient)] += 1
    
    patterns['collaboration_flows'] = [
        {'from': k[0], 'to': k[1], 'strength': v}
        for k, v in collaborations.items()
    ]
    
    # Identify bridge connections
    all_contacts = set()
    for email in mock_emails:
        all_contacts.add(email['from'])
        all_contacts.update(email['to'])
        all_contacts.update(email.get('cc', []))
    
    for contact in all_contacts:
        connections = set()
        for email in mock_emails:
            if contact == email['from']:
                connections.update(email['to'])
                connections.update(email.get('cc', []))
        
        if len(connections) > 3:
            patterns['bridge_connections'].append({
                'bridge': contact,
                'connections': list(connections),
                'bridge_strength': len(connections)
            })
    
    return patterns

if __name__ == "__main__":
    patterns = extract_email_patterns()
    output_path = Path("$DATA_DIR/email_patterns.json")
    
    with open(output_path, 'w') as f:
        json.dump(patterns, f, indent=2)
    
    print(f"✅ Email patterns extracted: {len(patterns['introduction_patterns'])} introductions found")
    print(f"   Collaboration flows: {len(patterns['collaboration_flows'])}")
    print(f"   Bridge connections: {len(patterns['bridge_connections'])}")
