import asyncio
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys


def _load_module(path: Path, module_name: str, package_hint: str | None = None):
    if package_hint and package_hint not in sys.modules:
        package_spec = importlib.machinery.ModuleSpec(package_hint, loader=None)
        package_module = importlib.util.module_from_spec(package_spec)
        package_module.__path__ = [str(path.parent)]  # type: ignore[attr-defined]
        sys.modules[package_hint] = package_module

    fullname = module_name
    if package_hint:
        fullname = f"{package_hint}.{path.stem}"

    spec = importlib.util.spec_from_file_location(
        fullname,
        path,
        submodule_search_locations=[str(path.parent)] if package_hint else None,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    if package_hint:
        module.__package__ = package_hint
    spec.loader.exec_module(module)
    return module


def _prepare_base_environment(base_path: Path) -> Path:
    base_path.mkdir(parents=True, exist_ok=True)

    layers_root = base_path / "_resonance" / "_reflection" / "memory_layers"
    for layer in ("l1_inference", "l2_symbolic", "l3_integration"):
        (layers_root / layer).mkdir(parents=True, exist_ok=True)

    bridge_config = {
        "memory_tools": {
            "add_documents": {
                "input_format": "jsonl",
                "schema": {
                    "page_content": "string",
                    "metadata": {
                        "source": "string",
                        "timestamp": "datetime",
                        "confidence": "float",
                        "symbolic_layer": "string",
                    },
                },
            }
        },
        "structured_tool": {
            "name": "pieces_inference",
            "description": "Test inference engine",
            "input_schema": {
                "content": "string",
                "type": ["code", "text", "mixed"],
                "symbolic_layer": "string",
            },
        },
        "symbolic_mapping": {
            "l1_inference": "DELTA",
            "l2_symbolic": "THETA",
            "l3_integration": "ALPHA",
        },
    }

    (layers_root / "langchain_bridge.json").write_text(json.dumps(bridge_config, indent=2))

    monitor_script = base_path / "_core" / "_pulse" / "agent_pieces_ghost" / "monitor_layers.sh"
    monitor_script.parent.mkdir(parents=True, exist_ok=True)
    monitor_script.write_text("#!/bin/bash\nexit 0\n")
    monitor_script.chmod(0o755)

    return base_path


def test_field_water_loop_sequence(tmp_path, monkeypatch):
    project_root = Path.cwd()
    loop_module = _load_module(project_root / "FIELD-LIVING/auto_boot/FIELD_WATER_LOOP.py", "field_water_loop")

    base = _prepare_base_environment(tmp_path / "field_runtime")
    monkeypatch.setenv("FIELD_BASE_PATH", str(base))
    logs_dir = base / "logs"
    monkeypatch.setenv("FIELD_LOG_DIR", str(logs_dir))

    import field_runtime.paths as paths  # noqa: WPS433
    import importlib

    importlib.reload(paths)
    import field_runtime.telemetry as telemetry  # noqa: WPS433

    importlib.reload(telemetry)

    loop_module.LOG_PATH = base / "boot.log"

    service_dir = base / "services"
    service_dir.mkdir(parents=True, exist_ok=True)

    services = []
    for svc in loop_module.SERVICES:
        cfg = dict(svc)
        cfg["standby_after"] = 1
        cfg["cooldown"] = 0.05
        stub_path = service_dir / f"{svc['name'].lower()}.py"
        stub_path.write_text(
            f"from field_runtime.telemetry import emit_heartbeat\n"
            f"async def wake_from_standby(base_path=None, service_config=None):\n"
            f"    emit_heartbeat('{svc['name']}', 'active', pressure=1.0, flow=1.0)\n"
            f"    return {{}}\n"
            f"async def enter_standby():\n"
            f"    emit_heartbeat('{svc['name']}', 'standby', pressure=0.5, flow=0.2)\n",
            encoding="utf-8",
        )
        cfg["path"] = stub_path
        cfg.pop("package_hint", None)
        services.append(cfg)

    stop_event = asyncio.Event()

    async def runner():
        task = asyncio.create_task(
            loop_module.field_water_loop(
                services=services,
                base_path=base,
                stop_event=stop_event,
                monitor_interval=0.1,
            )
        )
        await asyncio.sleep(1.2)
        stop_event.set()
        await task

    asyncio.run(runner())

    log_text = loop_module.LOG_PATH.read_text(encoding="utf-8")
    for svc in ["GLOBAL_ROOT", "DOJO_SOVEREIGN", "MCP_BRIDGE", "LANGCHAIN_CORE", "OBI_WAN_MEMORY"]:
        assert svc in log_text

    status_snapshot = telemetry.load_status()
    assert set(status_snapshot.keys()) >= {"GLOBAL_ROOT", "DOJO_SOVEREIGN"}

    # Verify global root wake/standby cycle and field strength behaviour
    global_root_module = _load_module(
        project_root / "◼︎DOJO_SOVEREIGN/global_root_system.py",
        "global_root_system",
        package_hint="◼︎DOJO_SOVEREIGN",
    )

    async def root_cycle():
        root = await global_root_module.wake_from_standby(base_path=base)
        assert root.state.field_state.field_strength > 0
        await global_root_module.enter_standby()

    asyncio.run(root_cycle())
