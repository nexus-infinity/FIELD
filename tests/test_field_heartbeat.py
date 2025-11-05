import importlib
import importlib.util
from pathlib import Path


def load_module(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def test_emit_updates_status(tmp_path, monkeypatch):
    monkeypatch.setenv("FIELD_LOG_DIR", str(tmp_path))

    import field_runtime.paths as paths
    importlib.reload(paths)
    import field_runtime.telemetry as telemetry
    importlib.reload(telemetry)

    payload = telemetry.emit_heartbeat("GLOBAL_ROOT", "active", pressure=1.0, flow=1.5)
    status = telemetry.load_status()

    assert "GLOBAL_ROOT" in status
    assert status["GLOBAL_ROOT"]["state"] == "active"
    assert status["GLOBAL_ROOT"]["note"] == payload["note"]

    stream_path = paths.heartbeat_stream_path()
    assert stream_path.exists()
    assert stream_path.read_text()

    heartbeat_module = load_module(
        Path(__file__).resolve().parents[1] / "FIELD-LIVING/auto_boot/FIELD_HEARTBEAT.py",
        "field_heartbeat_cli",
    )
    lines = heartbeat_module.format_status(status)
    assert any("GLOBAL_ROOT" in line for line in lines)
