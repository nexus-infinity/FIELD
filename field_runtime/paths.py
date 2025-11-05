"""Centralised path helpers for FIELD runtime tooling."""

from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    """Return the root of the FIELD repository."""
    return Path(__file__).resolve().parents[1]


def default_logs_dir() -> Path:
    """Default logs directory within the repository."""
    return project_root() / "FIELD-LIVING" / "logs"


def logs_dir() -> Path:
    """Return the directory used for runtime logs (override via FIELD_LOG_DIR)."""
    override = os.getenv("FIELD_LOG_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return default_logs_dir()


def heartbeat_status_path() -> Path:
    """Return the JSON file that stores the latest heartbeat snapshot."""
    return logs_dir() / "field_status.json"


def heartbeat_stream_path() -> Path:
    """Return the JSON Lines file used for streaming heartbeat history."""
    return logs_dir() / "field_heartbeat.jsonl"
