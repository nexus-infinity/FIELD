#!/usr/bin/env python3
"""Extract network amplification and bridge patterns"""

import json
from pathlib import Path
from collections import defaultdict

def extract_network_bridges():
    """Extract bridge patterns from social networks"""
    bridges = {
        'primary_bridges': [],
        'amplification_nodes': [],
        'network_clusters': {}
    }
    
    # Mock LinkedIn data (would parse CSV export in production)
    mock_connections = [
        {'name': 'Alice Smith', 'mutual_connections': 15, 'industries': ['Tech', 'AI']},
        {'name': 'Bob Johnson', 'mutual_connections': 8, 'industries': ['Finance']},
        {'name': 'Charlie Brown', 'mutual_connections': 25, 'industries': ['Tech', 'Education']},
        {'name': 'David Lee', 'mutual_connections': 3, 'industries': ['Healthcare']}
    ]
    
    # Identify bridge nodes (high mutual connections)
    for connection in mock_connections:
        if connection['mutual_connections'] > 10:
            bridges['primary_bridges'].append({
                'name': connection['name'],
                'bridge_strength': connection['mutual_connections'],
                'domains': connection['industries']
            })
    
    # Find amplification nodes
    industry_nodes = defaultdict(list)
    for connection in mock_connections:
        for industry in connection['industries']:
            industry_nodes[industry].append(connection['name'])
    
    for industry, nodes in industry_nodes.items():
        if len(nodes) > 1:
            bridges['network_clusters'][industry] = nodes
    
    return bridges

if __name__ == "__main__":
    bridges = extract_network_bridges()
    output_path = Path("$DATA_DIR/network_bridges.json")
    
    with open(output_path, 'w') as f:
        json.dump(bridges, f, indent=2)
    
    print(f"✅ Network bridges extracted: {len(bridges['primary_bridges'])} bridge nodes")
    print(f"   Network clusters: {len(bridges['network_clusters'])}")
