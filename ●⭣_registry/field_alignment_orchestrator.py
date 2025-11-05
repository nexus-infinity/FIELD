#!/usr/bin/env python3
"""
FIELD Alignment Orchestrator
----------------------------

MCP-friendly status service that reports sacred/digital/organic alignment.
Designed to replace the legacy FIELD-OOWL wisdom bridge with the triple-trident
architecture anchored in a single DOJO tetrahedral core.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

try:
    from mcp.server import Server
    import mcp.server.stdio
    import mcp.types as types

    MCP_AVAILABLE = True
except ImportError:  # pragma: no cover
    MCP_AVAILABLE = False
    Server = None  # type: ignore
    types = None  # type: ignore

SACRED_NODES = {
    "obi_wan": Path("/Users/jbear/FIELD/●OBI-WAN"),
    "tata": Path("/Users/jbear/FIELD/▼TATA"),
    "atlas": Path("/Users/jbear/FIELD/▲ATLAS"),
    "dojo": Path("/Users/jbear/DOJO"),
}

DIGITAL_SUPPORT_NODES = {
    "akron": Path("/Volumes/Akron"),
    "field_dev": Path("/Users/jbear/FIELD-DEV"),
    "field_living": Path("/Users/jbear/FIELD-LIVING"),
}

ORGANIC_SUPPORT_NODES = {
    "arkadas": Path("/Users/jbear/FIELD-LIVING/◆_soma_embodied"),
    "ob_link": Path("/Users/jbear/FIELD-LIVING/◆_living_memory"),
    "somalink": Path("/Users/jbear/FIELD-LIVING/◆_living_memory"),
}


def node_status(nodes: Dict[str, Path]) -> Dict[str, Dict[str, Any]]:
    return {
        name: {
            "path": str(path),
            "exists": path.exists(),
            "is_dir": path.is_dir(),
        }
        for name, path in nodes.items()
    }


def collect_alignment() -> Dict[str, Any]:
    return {
        "timestamp": datetime.now().isoformat(),
        "geometry": "single_tetrahedron_triple_trident",
        "rules": [
            "All flows reconverge through ◼︎ DOJO at 432 Hz",
            "Digital-support trident: ⟡ Akron • ⬛ FIELD-DEV • ⊞ FIELD-LIVING",
            "Organic-support trident: Arkadaş • OB-Link • SomaLink",
            "Observer → Architect → Weaver cycle remains canonical",
        ],
        "sacred_nodes": node_status(SACRED_NODES),
        "digital_support": node_status(DIGITAL_SUPPORT_NODES),
        "organic_support": node_status(ORGANIC_SUPPORT_NODES),
        "train_station": {
            "path": "/Users/jbear/FIELD-LIVING/●train_station_GEOMETRIC.py",
            "exists": Path("/Users/jbear/FIELD-LIVING/●train_station_GEOMETRIC.py").exists(),
        },
    }


def run_cli(verbose: bool = False) -> int:
    status = collect_alignment()
    if verbose:
        print(json.dumps(status, indent=2))
    else:
        print(json.dumps(status))
    missing = [
        name
        for section in ("sacred_nodes", "digital_support", "organic_support")
        for name, info in status[section].items()
        if not info["exists"]
    ]
    return 1 if missing else 0


if MCP_AVAILABLE:
    app = Server("field-alignment-orchestrator")

    @app.list_tools()
    async def list_tools() -> List[types.Tool]:
        return [
            types.Tool(
                name="field_alignment_status",
                description="Report sacred/digital/organic alignment readiness.",
                inputSchema={"type": "object", "properties": {}},
            )
        ]

    @app.call_tool()
    async def call_tool(
        name: str, arguments: Dict[str, Any] | None
    ) -> List[types.TextContent]:
        if name != "field_alignment_status":  # pragma: no cover - defensive
            raise ValueError(f"Unknown tool: {name}")
        payload = collect_alignment()
        return [
            types.TextContent(
                type="text",
                text=json.dumps(payload, indent=2),
            )
        ]


async def run_mcp_server() -> int:
    if not MCP_AVAILABLE:
        raise RuntimeError("mcp.server not available in this environment")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="FIELD Alignment Orchestrator")
    parser.add_argument("--verbose", "-v", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--mcp-mode", action="store_true", help="Run as MCP stdio server")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mcp_mode:
        if not MCP_AVAILABLE:
            print("❌ mcp.server module not available", file=sys.stderr)
            return 1
        return asyncio.run(run_mcp_server())

    return run_cli(verbose=args.verbose)


if __name__ == "__main__":  # pragma: no cover
    import sys

    sys.exit(main())
