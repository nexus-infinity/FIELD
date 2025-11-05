#!/usr/bin/env python3
from __future__ import annotations

"""
FIELD_WATER_LOOP.py
⟡ Sequential orchestration for FIELD subsystems based on Assyrian water dynamics.
Each service is a gate; pressure (demand) determines flow (activation).
"""

import asyncio
import importlib.machinery
import importlib.util
import inspect
import os
import signal
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = Path.home() / "FIELD-LIVING" / "logs" / "boot_validation.log"


def _append_log(message: str) -> None:
    """Append a timestamped message to the orchestration log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


def _service_path(relative: str) -> Path:
    """Resolve a service path relative to the FIELD project root."""
    return (PROJECT_ROOT / relative).resolve()


SERVICES: List[Dict[str, Any]] = [
    {
        "name": "GLOBAL_ROOT",
        "path": _service_path("◼︎DOJO_SOVEREIGN/global_root_system.py"),
        "package_hint": "◼︎DOJO_SOVEREIGN",
        "dependencies": [],
        "cooldown": 2,
        "standby_after": 600,
    },
    {
        "name": "DOJO_SOVEREIGN",
        "path": _service_path("◼︎DOJO_SOVEREIGN/field_cluster_init.py"),
        "package_hint": "◼︎DOJO_SOVEREIGN",
        "dependencies": ["GLOBAL_ROOT"],
        "cooldown": 3,
        "standby_after": 600,
    },
    {
        "name": "MCP_BRIDGE",
        "path": _service_path("pieces_monitor/mcp_pieces_bridge.py"),
        "package_hint": "pieces_monitor",
        "dependencies": ["DOJO_SOVEREIGN"],
        "cooldown": 2,
        "standby_after": 600,
    },
    {
        "name": "LANGCHAIN_CORE",
        "path": _service_path("◼︎DOJO_SOVEREIGN/langchain_v1.py"),
        "package_hint": "◼︎DOJO_SOVEREIGN",
        "dependencies": ["DOJO_SOVEREIGN"],
        "cooldown": 1,
        "standby_after": 480,
    },
    {
        "name": "OBI_WAN_MEMORY",
        "path": _service_path("●OBI-WAN/enhanced_obi_wan_memory.py"),
        "package_hint": "●OBI-WAN",
        "dependencies": ["LANGCHAIN_CORE"],
        "cooldown": 2,
        "standby_after": 900,
    },
]


class ServiceState:
    """Runtime bookkeeping for a managed FIELD service."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.module: Optional[ModuleType] = None
        self.active: bool = False
        self.last_wake: float = time.time()
        self.monitor_task: Optional[asyncio.Task] = None

    @property
    def name(self) -> str:
        return self.config["name"]

    @property
    def standby_after(self) -> int:
        return int(self.config.get("standby_after", 0))

    @property
    def cooldown(self) -> float:
        return float(self.config.get("cooldown", 0))

    @property
    def path(self) -> Path:
        path_value = self.config["path"]
        if isinstance(path_value, Path):
            return path_value
        return Path(os.path.expanduser(str(path_value))).resolve()


RUNNING_SERVICES: Dict[str, ServiceState] = {}
SHUTDOWN_EVENT = asyncio.Event()


def _load_service_module(service: ServiceState) -> ModuleType:
    """Dynamically load a service module without polluting sys.modules unduly."""
    package_hint = service.config.get("package_hint")
    module_name = f"field_service_{service.name.lower()}"

    if package_hint:
        module_name = f"{package_hint}.{service.path.stem}"
        if package_hint not in sys.modules:
            package_spec = importlib.machinery.ModuleSpec(package_hint, loader=None)
            package_module = importlib.util.module_from_spec(package_spec)
            package_module.__path__ = [str(service.path.parent)]  # type: ignore[attr-defined]
            sys.modules[package_hint] = package_module

    loader = importlib.util.spec_from_file_location(
        module_name,
        service.path,
        submodule_search_locations=[str(service.path.parent)],
    )
    if loader is None or loader.loader is None:
        raise ImportError(f"Unable to load module for {service.name} from {service.path}")
    module = importlib.util.module_from_spec(loader)
    if package_hint:
        module.__package__ = package_hint
    loader.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


async def _invoke_callable(obj: ModuleType, attr: str, **kwargs: Any) -> Any:
    """Invoke a wake/standby callable if it exists on the module."""
    func = getattr(obj, attr, None)
    if func is None or not callable(func):
        _append_log(f"[{attr}] ⚠️ callable missing on module {obj.__name__}")
        return None

    sig = inspect.signature(func)
    bound_kwargs = {name: value for name, value in kwargs.items() if name in sig.parameters}
    result = func(**bound_kwargs)

    if inspect.isawaitable(result):
        return await result

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: result)


async def _wake_service(service: ServiceState, base_path: Optional[Path] = None) -> None:
    """Activate a service by calling its wake hook."""
    if service.module is None:
        service.module = _load_service_module(service)

    await _invoke_callable(
        service.module,
        "wake_from_standby",
        base_path=str(base_path) if base_path else None,
        service_config=service.config,
    )
    service.active = True
    service.last_wake = time.time()
    _append_log(f"[{service.name}] 🌊 wake_from_standby invoked")


async def _enter_standby(service: ServiceState) -> None:
    """Call the enter_standby hook for a service if active."""
    if not service.active or service.module is None:
        return

    try:
        await _invoke_callable(service.module, "enter_standby")
        _append_log(f"[{service.name}] 🌫️ enter_standby invoked")
    finally:
        service.active = False
        service.module = None


async def _monitor_service(service: ServiceState) -> None:
    """Monitor a service and trigger standby once it exceeds the configured window."""
    if service.standby_after <= 0:
        return

    try:
        while not SHUTDOWN_EVENT.is_set():
            await asyncio.sleep(service.standby_after)
            if not service.active:
                return
            await _enter_standby(service)
            RUNNING_SERVICES.pop(service.name, None)
            return
    except asyncio.CancelledError:
        return


async def shutdown_services() -> None:
    """Gracefully transition all active services to standby."""
    tasks = []
    for state in list(RUNNING_SERVICES.values()):
        tasks.append(asyncio.create_task(_enter_standby(state)))
        if state.monitor_task:
            state.monitor_task.cancel()

    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    RUNNING_SERVICES.clear()


def _handle_shutdown(*_: Any) -> None:
    """Handle external shutdown signals by setting the shared event."""
    if not SHUTDOWN_EVENT.is_set():
        _append_log("⚙️ FIELD_WATER_LOOP received shutdown signal.")
        SHUTDOWN_EVENT.set()


async def field_water_loop(
    services: Optional[List[Dict[str, Any]]] = None,
    base_path: Optional[Path] = None,
    stop_event: Optional[asyncio.Event] = None,
    monitor_interval: float = 30.0,
) -> None:
    """Sequential orchestration based on dependency order."""
    configured_services = services or SERVICES
    RUNNING_SERVICES.clear()
    stop_signal = stop_event or SHUTDOWN_EVENT

    _append_log("\n=== FIELD Boot {} ===".format(time.ctime()))

    for service_cfg in configured_services:
        service = ServiceState(service_cfg)

        if not service.path.exists():
            _append_log(f"[{service.name}] ❌ path not found: {service.path}")
            continue

        # Wait for dependencies to become active
        for dependency in service.config.get("dependencies", []):
            while dependency not in RUNNING_SERVICES or not RUNNING_SERVICES[dependency].active:
                if stop_signal.is_set():
                    break
                await asyncio.sleep(0.2)

        if stop_signal.is_set():
            break

        await _wake_service(service, base_path=base_path)
        service.monitor_task = asyncio.create_task(_monitor_service(service))
        RUNNING_SERVICES[service.name] = service

        if service.cooldown:
            await asyncio.sleep(service.cooldown)

    _append_log("💧 All requested FIELD currents activated. Monitoring equilibrium...")

    try:
        while not stop_signal.is_set():
            await asyncio.sleep(monitor_interval)
    finally:
        await shutdown_services()
        _append_log("🏁 FIELD flow loop shutdown complete.")


def main() -> None:
    """Entry point for CLI usage."""
    signal.signal(signal.SIGINT, _handle_shutdown)
    signal.signal(signal.SIGTERM, _handle_shutdown)

    try:
        asyncio.run(field_water_loop())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
