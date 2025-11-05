"""Heartbeat emission and status tracking for FIELD subsystems."""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from . import paths

_STATUS_LOCK = threading.Lock()


SERVICE_SONIC_PROFILE: Dict[str, Dict[str, Any]] = {
    "GLOBAL_ROOT": {"note": "C3", "instrument": "cello_drone"},
    "DOJO_SOVEREIGN": {"note": "E4", "instrument": "harp_pad"},
    "MCP_BRIDGE": {"note": "G4", "instrument": "digital_chime"},
    "LANGCHAIN_CORE": {"note": "B3", "instrument": "resonant_pad"},
    "OBI_WAN_MEMORY": {"note": "D5", "instrument": "airy_choir"},
}


STATE_PROFILES: Dict[str, Dict[str, float]] = {
    "active": {"pressure": 1.0, "flow": 1.6},
    "idle": {"pressure": 0.75, "flow": 0.9},
    "standby": {"pressure": 0.55, "flow": 0.4},
    "offline": {"pressure": 0.2, "flow": 0.1},
}


def _ensure_logs_dir() -> None:
    log_dir = paths.logs_dir()
    log_dir.mkdir(parents=True, exist_ok=True)


def _load_status_map(status_path) -> Dict[str, Dict[str, Any]]:
    if not status_path.exists():
        return {}
    try:
        data = json.loads(status_path.read_text(encoding="utf-8") or "{}")
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    return {}


def _default_intensity(pressure: float, flow: float) -> float:
    score = (pressure * 0.6) + (flow * 0.4)
    return max(0.05, min(1.0, score / 2.5))


def emit_heartbeat(
    service: str,
    state: str,
    *,
    pressure: Optional[float] = None,
    flow: Optional[float] = None,
    note: Optional[str] = None,
    intensity: Optional[float] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Emit a heartbeat event and persist the latest status snapshot."""
    profile = STATE_PROFILES.get(state.lower(), {})
    pressure_val = pressure if pressure is not None else profile.get("pressure", 1.0)
    flow_val = flow if flow is not None else profile.get("flow", 1.0)

    sonic = SERVICE_SONIC_PROFILE.get(service, {})
    note_val = note or sonic.get("note", "C4")
    payload = {
        "service": service,
        "state": state,
        "pressure": round(float(pressure_val), 3),
        "flow": round(float(flow_val), 3),
        "timestamp": time.time(),
        "note": note_val,
        "intensity": round(float(intensity if intensity is not None else _default_intensity(pressure_val, flow_val)), 3),
        "instrument": sonic.get("instrument", "neutral_pad"),
    }

    if extra:
        payload.update(extra)

    _ensure_logs_dir()

    status_path = paths.heartbeat_status_path()
    stream_path = paths.heartbeat_stream_path()

    with _STATUS_LOCK:
        status_map = _load_status_map(status_path)
        status_map[service] = payload
        status_path.write_text(json.dumps(status_map, indent=2), encoding="utf-8")

        with stream_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(payload) + "\n")

    return payload


def load_status() -> Dict[str, Dict[str, Any]]:
    """Load the current heartbeat status snapshot."""
    return _load_status_map(paths.heartbeat_status_path())


def service_profile(service: str) -> Dict[str, Any]:
    """Return the sonic profile for a given service."""
    return SERVICE_SONIC_PROFILE.get(service, {"note": "C4", "instrument": "neutral_pad"})
