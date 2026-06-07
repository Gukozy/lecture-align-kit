"""Public, dependency-light lecture alignment helpers."""

from .align import align_slides_to_cues, detect_transitions
from .slides import Slide, parse_slides_markdown
from .srt import SrtCue, parse_srt_text

__all__ = [
    "Slide",
    "SrtCue",
    "align_slides_to_cues",
    "detect_transitions",
    "parse_slides_markdown",
    "parse_srt_text",
]
