from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SrtCue:
    idx: int
    start_ms: int
    end_ms: int
    text: str


_TIME_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}:\d{2},\d{3})"
)


def parse_srt_text(text: str) -> list[SrtCue]:
    """Parse SRT text into cue objects and renumber cues from 1."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []

    cues: list[SrtCue] = []
    blocks = re.split(r"\n\s*\n", normalized)
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2:
            continue

        time_line_index = 1 if lines[0].isdigit() and len(lines) > 1 else 0
        match = _TIME_RE.search(lines[time_line_index])
        if not match:
            continue

        body = " ".join(lines[time_line_index + 1 :]).strip()
        cues.append(
            SrtCue(
                idx=len(cues) + 1,
                start_ms=_parse_timestamp(match.group("start")),
                end_ms=_parse_timestamp(match.group("end")),
                text=body,
            )
        )
    return cues


def _parse_timestamp(value: str) -> int:
    hours, minutes, rest = value.split(":")
    seconds, millis = rest.split(",")
    return (
        int(hours) * 3_600_000
        + int(minutes) * 60_000
        + int(seconds) * 1_000
        + int(millis)
    )
