from __future__ import annotations

import re
from dataclasses import asdict

from .slides import Slide
from .srt import SrtCue


TRANSITION_RE = re.compile(
    r"\b(next slide|next topic|moving on|this figure|this table|now let's|to summarize)\b",
    flags=re.IGNORECASE,
)


def detect_transitions(cues: list[SrtCue]) -> list[int]:
    """Return cue indexes that look like slide/topic transitions."""
    return [cue.idx for cue in cues if TRANSITION_RE.search(cue.text)]


def align_slides_to_cues(slides: list[Slide], cues: list[SrtCue]) -> list[dict]:
    """
    Produce a deterministic, monotonic slide-to-cue mapping.

    This deliberately stays simple for the public core. It is good enough for
    synthetic fixtures and leaves advanced semantic scoring to future releases.
    """
    if not slides:
        return []
    if not cues:
        return [
            {
                "slide_idx": slide.slide_idx,
                "title": slide.title,
                "text": slide.text,
                "cue_range": None,
                "cues": [],
                "detected_transitions": [],
            }
            for slide in slides
        ]

    assignments = _initial_ranges(len(slides), len(cues))
    transition_ids = set(detect_transitions(cues))

    rows: list[dict] = []
    for slide, (start, end) in zip(slides, assignments, strict=True):
        assigned = cues[start : end + 1]
        rows.append(
            {
                "slide_idx": slide.slide_idx,
                "title": slide.title,
                "text": slide.text,
                "cue_range": [assigned[0].idx, assigned[-1].idx] if assigned else None,
                "cues": [asdict(cue) for cue in assigned],
                "detected_transitions": [cue.idx for cue in assigned if cue.idx in transition_ids],
            }
        )
    return rows


def _initial_ranges(slide_count: int, cue_count: int) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for slide_zero_idx in range(slide_count):
        start = round(slide_zero_idx * cue_count / slide_count)
        end = round((slide_zero_idx + 1) * cue_count / slide_count) - 1
        end = max(start, min(end, cue_count - 1))
        ranges.append((start, end))
    return ranges
