from __future__ import annotations

import argparse
import json
from pathlib import Path

from .align import align_slides_to_cues
from .slides import parse_slides_markdown
from .srt import parse_srt_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Align slide Markdown with SRT transcript cues.")
    parser.add_argument("--slides", required=True, type=Path, help="Markdown file with slide markers.")
    parser.add_argument("--srt", required=True, type=Path, help="SRT transcript file.")
    parser.add_argument("--out", required=True, type=Path, help="Output JSON path.")
    args = parser.parse_args()

    slides = parse_slides_markdown(args.slides.read_text(encoding="utf-8"))
    cues = parse_srt_text(args.srt.read_text(encoding="utf-8-sig"))
    aligned = align_slides_to_cues(slides, cues)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(aligned, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
