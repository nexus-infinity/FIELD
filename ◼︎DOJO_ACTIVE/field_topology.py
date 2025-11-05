#!/usr/bin/env python3
"""
Field Topology Mapper
Maps the FIELD's tetrahedral structure and data gravity patterns.
Understands where files naturally settle based on vertex resonance.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

@dataclass
class Vertex:
    """A vertex in the FIELD topology"""
    symbol: str
    name: str
    identity: str
    frequency: int
    port: int
    function: str
    path: Path
    resonance_keywords: List[str]
    
class FieldVertex(Enum):
    """The four primary vertices of the FIELD tetrahedral structure"""
    OBI_WAN = "●"     # Observer / Memory
    TATA = "▼"        # Root / Law / Verification  
    ATLAS = "▲"       # Intelligence / Navigation
    DOJO = "◼︎"        # Execution / Integration

@dataclass
class FieldTopology:
    """Complete FIELD topology mapping"""
    vertices: Dict[FieldVertex, Vertex]
    sacred_roots: List[Path]
    field_living: Path
    field_dev: Path
    akron: Path

class TopologyMapper:
    """
    Maps the FIELD's geometric structure and data gravity.
    Knows where files naturally settle based on their purpose/frequency.
    """
    
    def __init__(self):
        self.field_base = Path("/Users/jbear/FIELD")
        self.topology = self._initialize_topology()
        
    def _initialize_topology(self) -> FieldTopology:
        """Initialize the FIELD topology structure"""
        
        vertices = {
            FieldVertex.OBI_WAN: Vertex(
                symbol="●",
                name="OBI-WAN",
                identity="Jeremy Benjamin Rich (JB, JBR)",
                frequency=963,
                port=9630,
                function="Observer / Memory",
                path=self.field_base / "●OBI-WAN",
                resonance_keywords=[
                    "memory", "log", "pulse", "observation", "witness",
                    "consciousness", "awareness", "monitor", "watch",
                    "arkadas", "jarvis", "observer"
                ]
            ),
            FieldVertex.TATA: Vertex(
                symbol="▼",
                name="TATA",
                identity="Jacques Rich (Father)",
                frequency=852,
                port=9852,
                function="Root / Law / Verification",
                path=self.field_base / "▼TATA",
                resonance_keywords=[
                    "truth", "verify", "validate", "root", "law",
                    "test", "check", "audit", "proof", "evidence",
                    "sovereignty", "legal", "compliance"
                ]
            ),
            FieldVertex.ATLAS: Vertex(
                symbol="▲",
                name="ATLAS",
                identity="AI / ML / Ancient Tools",
                frequency=741,
                port=9741,
                function="Intelligence / Navigation",
                path=self.field_base / "▲ATLAS",
                resonance_keywords=[
                    "intelligence", "ai", "ml", "model", "navigation",
                    "tool", "automation", "script", "algorithm",
                    "creative", "generator", "analyzer", "processor"
                ]
            ),
            FieldVertex.DOJO: Vertex(
                symbol="◼︎",
                name="DOJO",
                identity="Sacred Manifestation",
                frequency=963,
                port=9963,
                function="Execution / Integration",
                path=self.field_base / "◼︎DOJO",
                resonance_keywords=[
                    "execution", "manifest", "active", "run", "deploy",
                    "integration", "sacred", "dojo", "working",
                    "current", "live", "operational"
                ]
            )
        }
        
        return FieldTopology(
            vertices=vertices,
            sacred_roots=[
                self.field_base / "●OBI-WAN",
                self.field_base / "▼TATA",
                self.field_base / "▲ATLAS",
                self.field_base / "◼︎DOJO",
                self.field_base / "◼︎DOJO_ACTIVE",
            ],
            field_living=self.field_base / "FIELD-LIVING",
            field_dev=self.field_base / "FIELD-DEV",
            akron=Path("/Volumes/Akron")
        )
    
    def calculate_vertex_resonance(self, path: Path, query: str = "") -> Dict[FieldVertex, float]:
        """
        Calculate how strongly a path or query resonates with each vertex.
        Returns dict of {vertex: resonance_score} where 0.0 = no resonance, 1.0 = perfect match
        """
        path_str = str(path).lower()
        query_lower = query.lower()
        combined = f"{path_str} {query_lower}"
        
        resonance = {}
        
        for vertex_type, vertex in self.topology.vertices.items():
            score = 0.0
            
            # Strong resonance: path is within vertex directory
            if vertex.path.exists() and path.is_relative_to(vertex.path):
                score += 0.6
            
            # Moderate resonance: vertex symbol in path
            if vertex.symbol in str(path):
                score += 0.3
            
            # Keyword resonance: check against vertex keywords
            keyword_matches = sum(1 for kw in vertex.resonance_keywords if kw in combined)
            if keyword_matches > 0:
                # Normalize: more keywords = stronger but diminishing returns
                score += min(keyword_matches * 0.15, 0.4)
            
            resonance[vertex_type] = min(score, 1.0)
        
        return resonance
    
    def find_resonant_vertices(self, query: str, threshold: float = 0.3) -> List[Tuple[FieldVertex, Vertex, float]]:
        """
        Find vertices that resonate with a query.
        Returns list of (vertex_type, vertex, score) sorted by resonance strength.
        """
        resonant = []
        
        for vertex_type, vertex in self.topology.vertices.items():
            score = self.calculate_vertex_resonance(vertex.path, query)[vertex_type]
            
            if score >= threshold:
                resonant.append((vertex_type, vertex, score))
        
        # Sort by resonance strength (highest first)
        resonant.sort(key=lambda x: x[2], reverse=True)
        
        return resonant
    
    def get_vertex_by_path(self, path: Path) -> Optional[Tuple[FieldVertex, Vertex]]:
        """Determine which vertex a path belongs to"""
        for vertex_type, vertex in self.topology.vertices.items():
            if vertex.path.exists() and path.is_relative_to(vertex.path):
                return (vertex_type, vertex)
        return None
    
    def get_search_order(self, query: str) -> List[Path]:
        """
        Get the optimal search order based on query resonance.
        Returns paths in order of where to search first.
        """
        # Find resonant vertices
        resonant = self.find_resonant_vertices(query)
        
        # Build search path list
        search_paths = []
        
        # Add resonant vertex paths first (in resonance order)
        for vertex_type, vertex, score in resonant:
            if vertex.path.exists():
                search_paths.append(vertex.path)
        
        # Add other sacred roots not yet included
        for root in self.topology.sacred_roots:
            if root.exists() and root not in search_paths:
                search_paths.append(root)
        
        # Add field-specific areas
        for area in [self.topology.field_dev, self.topology.field_living]:
            if area.exists() and area not in search_paths:
                search_paths.append(area)
        
        return search_paths
    
    def explain_resonance(self, path: Path, query: str = "") -> str:
        """
        Explain why a path resonates the way it does.
        Useful for debugging and understanding the topology.
        """
        resonance = self.calculate_vertex_resonance(path, query)
        
        lines = [f"Resonance analysis for: {path}"]
        if query:
            lines.append(f"Query: {query}")
        lines.append("")
        
        # Sort by resonance
        sorted_resonance = sorted(resonance.items(), key=lambda x: x[1], reverse=True)
        
        for vertex_type, score in sorted_resonance:
            vertex = self.topology.vertices[vertex_type]
            if score > 0:
                lines.append(f"{vertex.symbol} {vertex.name}: {score:.2f} - {vertex.function}")
            
        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    
    mapper = TopologyMapper()
    
    if len(sys.argv) > 1:
        query = sys.argv[1]
        print(f"🧭 Finding resonant vertices for: {query}\n")
        
        resonant = mapper.find_resonant_vertices(query)
        
        if resonant:
            print("Resonant vertices (highest first):")
            for vertex_type, vertex, score in resonant:
                print(f"  {vertex.symbol} {vertex.name}: {score:.2%} resonance")
                print(f"    → {vertex.path}")
                print(f"    Function: {vertex.function}\n")
            
            print("\n📍 Optimal search order:")
            for i, path in enumerate(mapper.get_search_order(query), 1):
                print(f"  {i}. {path}")
        else:
            print("No strong resonance found - will search all vertices")
    else:
        print("🗺️  FIELD Topology Mapper")
        print("=" * 60)
        print("\nVertices:")
        for vertex_type, vertex in mapper.topology.vertices.items():
            print(f"\n{vertex.symbol} {vertex.name}")
            print(f"  Frequency: {vertex.frequency} Hz")
            print(f"  Function: {vertex.function}")
            print(f"  Path: {vertex.path}")
            print(f"  Keywords: {', '.join(vertex.resonance_keywords[:5])}...")
