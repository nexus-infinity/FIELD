#!/usr/bin/env python3
"""
NotionScribe Reflection Workflow
Reads FIELD_COGNITIVE_STANDARD.yaml and generates reflection cues.
Pushes cues into Notion (if configured) and Pieces OS (file + optional HTTP).
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import yaml

try:
    from notion_client import Client as NotionClient
except ImportError:  # pragma: no cover
    NotionClient = None  # type: ignore[assignment]

try:
    import httpx
except ImportError:  # pragma: no cover
    httpx = None  # type: ignore[assignment]


BASE_DIR = Path("/Users/jbear/FIELD")
STANDARD_PATH = BASE_DIR / "◼︎DOJO" / "config" / "FIELD_COGNITIVE_STANDARD.yaml"
PIECES_CACHE_PATH = BASE_DIR / "pieces_monitor" / "reflection_cues.json"
NOTION_FALLBACK_PATH = Path("/Users/jbear/FIELD-LIVING/notion_sync/reflection_cues.json")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class ReflectionCue:
    """Represents a single rhythmic cue for reflection workflow."""

    phase: str
    mode: str
    start: datetime
    end: datetime
    cycle_index: int
    fractal_layer: str

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)

    def to_dict(self) -> Dict[str, str]:
        return {
            "phase": self.phase,
            "mode": self.mode,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "duration_minutes": self.duration_minutes,
            "cycle_index": self.cycle_index,
            "fractal_layer": self.fractal_layer,
        }


class NotionScribeWorkflow:
    """Generates and dispatches reflection cues from the cognitive standard."""

    def __init__(self, now: Optional[datetime] = None):
        self.now = now or datetime.utcnow()
        self.standard_path = STANDARD_PATH
        self.standard = self._load_standard()
        self.notion_token = os.getenv("NOTION_API_KEY") or os.getenv("NOTION_TOKEN")
        self.notion_db_id = os.getenv("NOTION_REFLECTION_DB_ID")
        self.pieces_endpoint = os.getenv("PIECES_OS_HOST", "http://localhost:39300")
        self.pieces_enabled = bool(os.getenv("PIECES_PUSH_ENABLED", "1") != "0")

        self.notion_client = None
        if self.notion_token and NotionClient:
            self.notion_client = NotionClient(auth=self.notion_token)
        elif self.notion_db_id:
            logger.warning("Notion reflection DB configured but no Notion client available.")

    def _load_standard(self) -> dict:
        if not self.standard_path.exists():
            raise FileNotFoundError(f"Cognitive standard not found at {self.standard_path}")
        with open(self.standard_path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)

    def _parse_duration(self, text: str, default_minutes: int) -> int:
        """Extract a representative duration from descriptive text."""
        lower = text.lower()
        numbers = [int(n) for n in re.findall(r"\d+", lower)]
        if not numbers:
            return default_minutes

        base_value = numbers[0]
        if "hour" in lower:
            return base_value * 60
        return base_value

    def _cycle_count(self) -> int:
        descriptor = self.standard.get("rhythm_protocol", {}).get("cycle_repeat", "")
        numbers = [int(n) for n in re.findall(r"\d+", descriptor)]
        return numbers[0] if numbers else 3

    def build_cues(self) -> List[ReflectionCue]:
        protocol = self.standard.get("rhythm_protocol", {})
        inhale_minutes = self._parse_duration(protocol.get("inhale", ""), 90)
        hold_minutes = self._parse_duration(protocol.get("hold", ""), 25)
        exhale_minutes = self._parse_duration(protocol.get("exhale", ""), 60)
        drift_minutes = self._parse_duration(protocol.get("drift_phase", ""), 30)

        cycle_count = self._cycle_count()
        cues: List[ReflectionCue] = []
        current_start = self.now.replace(second=0, microsecond=0)

        # Fractal recursion layers: Macro (day), Meso (cycle), Micro (phase)
        for cycle in range(1, cycle_count + 1):
            for phase, duration in (
                ("Inhale", inhale_minutes),
                ("Hold", hold_minutes),
                ("Exhale", exhale_minutes),
                ("Drift", drift_minutes),
            ):
                end = current_start + timedelta(minutes=duration)
                cues.append(
                    ReflectionCue(
                        phase=phase,
                        mode=self._phase_to_mode(phase),
                        start=current_start,
                        end=end,
                        cycle_index=cycle,
                        fractal_layer=f"macro:day → meso:cycle{cycle} → micro:{phase.lower()}",
                    )
                )
                current_start = end

        return cues

    @staticmethod
    def _phase_to_mode(phase: str) -> str:
        return {
            "Inhale": "Focused Flow",
            "Hold": "Integration Sync",
            "Exhale": "Expression Release",
            "Drift": "Diffuse Reflection",
        }.get(phase, "Focused Flow")

    def dispatch(self) -> List[ReflectionCue]:
        cues = self.build_cues()
        self._write_local_manifest(cues)
        self._push_to_notion(cues)
        self._push_to_pieces(cues)
        return cues

    def _write_local_manifest(self, cues: List[ReflectionCue]) -> None:
        NOTION_FALLBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "generated_at": self.now.isoformat(),
            "standard_path": str(self.standard_path),
            "cues": [cue.to_dict() for cue in cues],
        }
        NOTION_FALLBACK_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info("Reflection cues written to local manifest at %s", NOTION_FALLBACK_PATH)

    def _push_to_notion(self, cues: List[ReflectionCue]) -> None:
        if not self.notion_db_id:
            logger.info("NOTION_REFLECTION_DB_ID not set; skipping Notion cue creation.")
            return
        if not self.notion_client:
            logger.warning("Notion client unavailable; cues logged locally for manual import.")
            return

        for cue in cues:
            title = f"{cue.phase} Cycle {cue.cycle_index}"
            properties = {
                "Name": {"title": [{"text": {"content": title}}]},
                "Mode": {"select": {"name": cue.mode}},
                "Phase Start": {"date": {"start": cue.start.isoformat(), "end": cue.end.isoformat()}},
                "Duration (min)": {"number": cue.duration_minutes},
                "Fractal Layer": {"rich_text": [{"text": {"content": cue.fractal_layer}}]},
                "Source": {"rich_text": [{"text": {"content": "FIELD_COGNITIVE_STANDARD"}}]},
            }

            try:
                self.notion_client.pages.create(
                    database_id=self.notion_db_id,
                    properties=properties,
                )
            except Exception as exc:  # pragma: no cover - Notion errors vary
                logger.error("Failed to create Notion reflection cue: %s", exc)
                break
        else:
            logger.info("Reflection cues pushed to Notion database %s", self.notion_db_id)

    def _push_to_pieces(self, cues: List[ReflectionCue]) -> None:
        payload = {
            "generated_at": self.now.isoformat(),
            "cues": [cue.to_dict() for cue in cues],
        }

        # Always write a cache file Pieces OS can poll
        PIECES_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        PIECES_CACHE_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        logger.info("Reflection cues cached for Pieces OS at %s", PIECES_CACHE_PATH)

        if not self.pieces_enabled or httpx is None:
            logger.info("Pieces push disabled or httpx unavailable; cache only.")
            return

        try:
            with httpx.Client(timeout=5.0) as client:
                for cue in cues:
                    description = (
                        f"{cue.phase} window ({cue.duration_minutes} min) • "
                        f"Cycle {cue.cycle_index} • {cue.fractal_layer}"
                    )
                    payload = {
                        "title": f"{cue.phase} – Cycle {cue.cycle_index}",
                        "text": description,
                        "metadata": {
                            "mode": cue.mode,
                            "start": cue.start.isoformat(),
                            "end": cue.end.isoformat(),
                            "fractal_layer": cue.fractal_layer,
                            "source": "FIELD_COGNITIVE_STANDARD",
                        },
                    }
                    client.post(
                        f"{self.pieces_endpoint.rstrip('/')}/api/v1/assets",
                        json=payload,
                    )
        except Exception as exc:  # pragma: no cover - depends on Pieces OS
            logger.warning("Pieces API push failed (%s); cues remain cached.", exc)


def run_notionscribe_dispatch() -> List[ReflectionCue]:
    workflow = NotionScribeWorkflow()
    return workflow.dispatch()


if __name__ == "__main__":
    run_notionscribe_dispatch()
