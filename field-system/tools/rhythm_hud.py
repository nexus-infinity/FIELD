#!/usr/bin/env python3
"""
Rhythm HUD Prototype
Visualizes cognitive rhythm cycles derived from FIELD_COGNITIVE_STANDARD.yaml.
Provides fractal alignment summary and mode switching guidance.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


CURRENT_PATH = Path(__file__).resolve()
FIELD_LIVING_ROOT = CURRENT_PATH.parents[1]
if str(FIELD_LIVING_ROOT) not in sys.path:
    sys.path.insert(0, str(FIELD_LIVING_ROOT))

from notion_sync.notionscribe_reflection import (  # type: ignore
    NotionScribeWorkflow,
    ReflectionCue,
)


class RhythmHUD:
    """Console HUD for visualizing rhythmic cognitive modes."""

    def __init__(self, now: Optional[datetime] = None):
        self.workflow = NotionScribeWorkflow(now=now)
        self.cues: List[ReflectionCue] = self.workflow.build_cues()

    def refresh(self) -> None:
        """Refresh cues using latest standard data."""
        self.workflow = NotionScribeWorkflow()
        self.cues = self.workflow.build_cues()

    def current_phase(self, moment: Optional[datetime] = None) -> Tuple[Optional[ReflectionCue], Optional[ReflectionCue]]:
        moment = moment or datetime.utcnow()
        for cue in self.cues:
            if cue.start <= moment < cue.end:
                next_cue = self._next_cue(cue)
                return cue, next_cue
        return None, self.cues[0] if self.cues else None

    def _next_cue(self, cue: ReflectionCue) -> Optional[ReflectionCue]:
        try:
            idx = self.cues.index(cue)
        except ValueError:
            return None
        if idx + 1 < len(self.cues):
            return self.cues[idx + 1]
        return None

    def render_text(self, moment: Optional[datetime] = None) -> str:
        moment = moment or datetime.utcnow()
        current, nxt = self.current_phase(moment)
        header = [
            "================ RHYTHM HUD (Prototype) ================",
            f"Now (UTC): {moment.isoformat()}",
        ]

        if current:
            remaining = int((current.end - moment).total_seconds() // 60)
            header.append(
                f"Current Mode: {current.mode} ({current.phase}) "
                f"| Remaining: {remaining} min"
            )
            header.append(f"Fractal Alignment: {current.fractal_layer}")
        else:
            header.append("Current Mode: Unscheduled (consider Drift)")

        if nxt:
            until_next = int((nxt.start - moment).total_seconds() // 60)
            header.append(
                f"Next Mode: {nxt.mode} at {nxt.start.strftime('%H:%M')} "
                f"(in {until_next} min)"
            )

        body = ["", "Fractal Cycle Overview:"]
        for cycle, group in self._group_by_cycle():
            body.append(f"  Cycle {cycle}:")
            for cue in group:
                body.append(
                    "    "
                    f"{cue.phase:<7} | {cue.start.strftime('%H:%M')} → {cue.end.strftime('%H:%M')} "
                    f"| {cue.mode:<18} | {cue.duration_minutes:>3} min"
                )
            body.append("")

        footer = [
            "Alignment Principle: Each mode nests within Cycle → Day recursion.",
            "Use this HUD to trigger mode switches rather than volume-based context switching.",
        ]
        return "\n".join(header + body + footer)

    def _group_by_cycle(self) -> Iterable[Tuple[int, List[ReflectionCue]]]:
        cycle_map: dict[int, List[ReflectionCue]] = {}
        for cue in self.cues:
            cycle_map.setdefault(cue.cycle_index, []).append(cue)
        for cycle in sorted(cycle_map.keys()):
            yield cycle, cycle_map[cycle]


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prototype Rhythm HUD renderer.")
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Continuously redraw the HUD every 60 seconds.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Render a single snapshot (default).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    hud = RhythmHUD()

    def draw():
        hud.refresh()
        print(hud.render_text())

    draw()
    if args.watch and not args.once:
        try:
            while True:
                time.sleep(60)
                draw()
        except KeyboardInterrupt:
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
