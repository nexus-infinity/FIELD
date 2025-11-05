import importlib
import importlib.util
from pathlib import Path


def load_module(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def test_harmony_index_and_frequency(tmp_path, monkeypatch):
    monkeypatch.setenv("FIELD_LOG_DIR", str(tmp_path))

    import field_runtime.paths as paths
    importlib.reload(paths)
    import field_runtime.telemetry as telemetry
    importlib.reload(telemetry)

    telemetry.emit_heartbeat("GLOBAL_ROOT", "active", pressure=1.1, flow=1.6)
    telemetry.emit_heartbeat("DOJO_SOVEREIGN", "active", pressure=0.95, flow=1.2)
    status = telemetry.load_status()

    sound_module = load_module(
        Path(__file__).resolve().parents[1] / "FIELD-LIVING/auto_boot/FIELD_SOUND_BRIDGE.py",
        "field_sound_bridge",
    )

    harmony = sound_module.compute_harmony_index(status)
    assert 0.0 <= harmony <= 1.0

    freq = sound_module.note_to_frequency("E4")
    assert freq > 0

    # Ensure function handles unknown notes gracefully.
    assert sound_module.note_to_frequency("Z9") == sound_module.note_to_frequency("C4")
