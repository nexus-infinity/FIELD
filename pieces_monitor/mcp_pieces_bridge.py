#!/usr/bin/env python3
"""
FIELD-Pieces MCP Bridge
Connects Pieces OS to FIELD memory systems while preserving normal Pieces functionality
"""
import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional
import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from field_runtime.telemetry import emit_heartbeat

# Pieces OS configuration
PIECES_HOST = os.getenv("PIECES_OS_HOST", "http://localhost:39300")
PIECES_PORT = os.getenv("PIECES_OS_PORT", "39300")

BRIDGE_RELATIVE_PATH = Path("_resonance/_reflection/memory_layers/langchain_bridge.json")
MEMORY_LAYERS = ("l1_inference", "l2_symbolic", "l3_integration")

app = Server("pieces-field-bridge")
logger = logging.getLogger("PiecesMCPBridge")


def resolve_base_path() -> Path:
    """Resolve the FIELD base path for bridge assets."""
    return Path(os.getenv("FIELD_BASE_PATH", os.getcwd())).expanduser()


def resolve_bridge_path(base_path: Path) -> Path:
    """Resolve the bridge configuration location with optional override."""
    override = os.getenv("FIELD_LANGCHAIN_BRIDGE")
    if override:
        return Path(override).expanduser()
    return base_path / BRIDGE_RELATIVE_PATH


def load_bridge_configuration(bridge_path: Path) -> Dict[str, Any]:
    """Load and validate the LangChain bridge configuration."""
    config_data = json.loads(bridge_path.read_text())
    structured_tool = (
        config_data.get("structured_tool")
        or config_data.get("memory_tools", {}).get("structured_tool")
        or {}
    )
    tool_name = structured_tool.get("name")
    if not tool_name:
        raise ValueError("structured_tool.name missing in bridge configuration")

    return {
        "structured_tool": structured_tool,
        "memory_tools": config_data.get("memory_tools", {}),
        "symbolic_mapping": config_data.get("symbolic_mapping", {}),
    }


async def perform_memory_sync(base_path: Path) -> Dict[str, Any]:
    """Validate bridge configuration and memory layer readiness."""
    bridge_path = resolve_bridge_path(base_path)
    layer_root = base_path / "_resonance" / "_reflection" / "memory_layers"

    sync_state: Dict[str, Any] = {
        "bridge_path": str(bridge_path),
        "bridge_exists": bridge_path.exists(),
        "layer_root": str(layer_root),
        "layer_directories": {},
        "config_valid": False,
    }

    for layer in MEMORY_LAYERS:
        layer_dir = layer_root / layer
        sync_state["layer_directories"][layer] = layer_dir.is_dir()

    if not bridge_path.exists():
        sync_state["error"] = "Bridge configuration missing"
        return sync_state

    try:
        config = load_bridge_configuration(bridge_path)
        sync_state["config_valid"] = True
        structured_tool = config["structured_tool"]
        sync_state["structured_tool"] = {
            "name": structured_tool.get("name"),
            "description": structured_tool.get("description"),
        }
        sync_state["symbolic_mapping"] = config.get("symbolic_mapping", {})
    except Exception as exc:
        sync_state["error"] = f"Bridge validation failed: {exc}"

    return sync_state

class PiecesConnector:
    def __init__(self):
        self.base_url = PIECES_HOST
        timeout = httpx.Timeout(5.0, read=10.0)
        self.client = httpx.AsyncClient(timeout=timeout, headers={"User-Agent": "FIELD-PiecesBridge/1.0"})
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to Pieces OS"""
        try:
            # Try common Pieces API endpoints
            endpoints_to_try = [
                "/api/v1/health",
                "/health", 
                "/api/health",
                "/wellknown/health",
                "/api/v1/wellknown/health"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = await self.client.get(f"{self.base_url}{endpoint}")
                    if response.status_code == 200:
                        return {
                            "status": "connected",
                            "endpoint": endpoint,
                            "response": response.text[:200]  # First 200 chars
                        }
                except:
                    continue
            
            # If health checks fail, try basic connectivity
            response = await self.client.get(self.base_url)
            return {
                "status": "partial",
                "message": "Pieces OS responding but health endpoint unknown",
                "response": response.text[:100]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_pieces_info(self) -> Dict[str, Any]:
        """Get basic Pieces OS information"""
        try:
            # Try to get basic info about running Pieces
            endpoints = [
                "/api/v1/assets",
                "/api/assets", 
                "/assets",
                "/api/v1/applications",
                "/applications"
            ]
            
            results = {}
            for endpoint in endpoints:
                try:
                    response = await self.client.get(f"{self.base_url}{endpoint}")
                    if response.status_code == 200:
                        results[endpoint] = {
                            "status": "available",
                            "content_type": response.headers.get("content-type", "unknown")
                        }
                except:
                    results[endpoint] = {"status": "unavailable"}
            
            return results
            
        except Exception as e:
            return {"error": str(e)}

    async def close(self) -> None:
        """Close the HTTP client session."""
        await self.client.aclose()

pieces_connector = PiecesConnector()
_BRIDGE_ACTIVE = False

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available FIELD-Pieces bridge tools"""
    return [
        types.Tool(
            name="pieces_status",
            description="Check Pieces OS connection status",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="pieces_info",
            description="Get Pieces OS API information",
            inputSchema={
                "type": "object", 
                "properties": {},
            },
        ),
        types.Tool(
            name="field_pieces_integration",
            description="Test FIELD-Pieces memory integration",
            inputSchema={
                "type": "object",
                "properties": {
                    "test_type": {
                        "type": "string",
                        "description": "Type of integration test to run",
                        "enum": ["connectivity", "memory_sync", "full"]
                    }
                },
                "required": ["test_type"]
            },
        ),
    ]

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls"""
    
    if name == "pieces_status":
        status = await pieces_connector.test_connection()
        return [
            types.TextContent(
                type="text",
                text=f"Pieces OS Status:\n{json.dumps(status, indent=2)}"
            )
        ]
    
    elif name == "pieces_info":
        info = await pieces_connector.get_pieces_info()
        return [
            types.TextContent(
                type="text", 
                text=f"Pieces OS API Information:\n{json.dumps(info, indent=2)}"
            )
        ]
    
    elif name == "field_pieces_integration":
        test_type = arguments.get("test_type", "connectivity")
        base_path = resolve_base_path()
        
        if test_type == "connectivity":
            status = await pieces_connector.test_connection()
            result = {
                "test": "connectivity",
                "pieces_status": status,
                "field_integration": "bridge_active",
                "port": PIECES_PORT
            }
        elif test_type == "memory_sync":
            status = await pieces_connector.test_connection()
            sync_state = await perform_memory_sync(base_path)
            result = {
                "test": "memory_sync",
                "pieces_status": status,
                "sync_state": sync_state
            }
        else:  # full test
            status = await pieces_connector.test_connection()
            info = await pieces_connector.get_pieces_info()
            sync_state = await perform_memory_sync(base_path)
            result = {
                "test": "full_integration",
                "pieces_status": status,
                "api_info": info,
                "bridge_status": "operational",
                "sync_state": sync_state
            }
        
        return [
            types.TextContent(
                type="text",
                text=f"FIELD-Pieces Integration Test:\n{json.dumps(result, indent=2)}"
            )
        ]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the MCP server"""
    # Initialize the server with connection options
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="pieces-field-bridge",
                    server_version="1.0.0",
                    capabilities=app.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )
    finally:
        await pieces_connector.close()

if __name__ == "__main__":
    asyncio.run(main())


# ---------------------------------------------------------------------------
# Orchestration hooks
# ---------------------------------------------------------------------------


async def wake_from_standby(
    base_path: Optional[Path | str] = None,
    service_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Validate bridge readiness and prepare for operation."""
    global _BRIDGE_ACTIVE, pieces_connector

    resolved_base = Path(base_path).expanduser().resolve() if base_path else resolve_base_path()
    logger.info("🌊 Pieces bridge wake_from_standby initiating")
    sync_state = await perform_memory_sync(resolved_base)
    _BRIDGE_ACTIVE = True
    emit_heartbeat(
        "MCP_BRIDGE",
        "active",
        pressure=0.9,
        flow=1.3,
        extra={"bridge_status": sync_state.get("bridge_exists")},
    )
    return sync_state


async def enter_standby() -> None:
    """Gracefully release bridge resources."""
    global _BRIDGE_ACTIVE, pieces_connector

    if not _BRIDGE_ACTIVE:
        return

    try:
        await pieces_connector.close()
    except Exception as exc:  # pragma: no cover - best effort
        logger.error(f"Pieces bridge standby cleanup failed: {exc}")
    finally:
        pieces_connector = PiecesConnector()
        _BRIDGE_ACTIVE = False
        emit_heartbeat("MCP_BRIDGE", "standby", pressure=0.5, flow=0.2)
        logger.info("🌫️ Pieces bridge enter_standby complete")
