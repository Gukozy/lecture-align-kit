from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Slide:
    slide_idx: int
    title: str | None
    text: str


_SLIDE_MARKER_RE = re.compile(r"<!--\s*slide_idx:\s*(\d+)\s*-->")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")


def parse_slides_markdown(text: str) -> list[Slide]:
    """Parse Markdown with HTML slide markers into ordered slide objects."""
    slides: list[Slide] = []
    current_idx: int | None = None
    current_lines: list[str] = []

    def flush() -> None:
        if current_idx is None:
            return
        body_lines = [line.rstrip() for line in current_lines if line.strip()]
        body = "\n".join(body_lines).strip()
        slides.append(Slide(slide_idx=current_idx, title=_extract_title(body_lines), text=body))

    for raw_line in text.splitlines():
        marker = _SLIDE_MARKER_RE.match(raw_line.strip())
        if marker:
            flush()
            current_idx = int(marker.group(1))
            current_lines = []
            continue
        if current_idx is not None:
            current_lines.append(raw_line)

    flush()
    return slides


def _extract_title(lines: list[str]) -> str | None:
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        heading = _HEADING_RE.match(stripped)
        if heading:
            return heading.group(2).strip()
        return stripped[:80]
    return None
