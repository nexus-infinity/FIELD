#!/usr/bin/env python3
"""
Development Frontend MCP Bridge
--------------------------------

Coordinates FIELD frontend deployments with the digital-support trident.
"""

from __future__ import annotations

import argparse
import asyncio
import json
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

NEXT_APPS = Path("/Users/jbear/FIELD-DEV/berjak-website")
TRAIN_STATION = Path("/Users/jbear/FIELD-LIVING/●train_station_GEOMETRIC.py")
AKRON = Path("/Volumes/Akron")


def gather_frontend_status() -> Dict[str, Any]:
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "geometry": "digital_support_trident",
        "resources": {
            "next_apps": {"path": str(NEXT_APPS), "exists": NEXT_APPS.exists()},
            "train_station": {"path": str(TRAIN_STATION), "exists": TRAIN_STATION.exists()},
            "akron": {"path": str(AKRON), "exists": AKRON.exists()},
        },
        "notes": [
            "⬢ Development ensures Vercel/Tailwind builds honour sacred geometry.",
            "All deployments must pass through Train Station at 432 Hz before DOJO manifests them.",
        ],
    }


def run_cli(verbose: bool) -> int:
    status = gather_frontend_status()
    if verbose:
        print(json.dumps(status, indent=2))
    else:
        print(json.dumps(status))
    missing = [
        name for name, info in status["resources"].items() if not info["exists"]
    ]
    return 1 if missing else 0


if MCP_AVAILABLE:
    app = Server("dev-frontend-bridge")

    @app.list_tools()
    async def list_tools() -> List[types.Tool]:
        return [
            types.Tool(
                name="dev_frontend_status",
                description="Report frontend readiness against the digital-support trident.",
                inputSchema={"type": "object", "properties": {}},
            )
        ]

    @app.call_tool()
    async def call_tool(
        name: str, arguments: Dict[str, Any] | None
    ) -> List[types.TextContent]:
        if name != "dev_frontend_status":  # pragma: no cover
            raise ValueError(f"Unknown tool: {name}")
        return [
            types.TextContent(
                type="text", text=json.dumps(gather_frontend_status(), indent=2)
            )
        ]


async def run_mcp() -> int:
    if not MCP_AVAILABLE:
        raise RuntimeError("mcp.server not available")
    async with mcp.server.stdio.stdio_server() as (reader, writer):
        await app.run(reader, writer)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Development frontend MCP bridge")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--mcp-mode", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mcp_mode:
        if not MCP_AVAILABLE:
            print("❌ mcp.server not installed")
            return 1
        return asyncio.run(run_mcp())
    return run_cli(verbose=args.verbose)


if __name__ == "__main__":
    import sys

    sys.exit(main())
