from lecture_align_kit import align_slides_to_cues, detect_transitions, parse_slides_markdown
from lecture_align_kit.srt import SrtCue


def test_parse_slides_markdown_with_markers():
    slides = parse_slides_markdown(
        """
# Deck

<!-- slide_idx: 1 -->
## First
Intro text

<!-- slide_idx: 2 -->
## Second
More text
"""
    )

    assert [slide.slide_idx for slide in slides] == [1, 2]
    assert slides[0].title == "First"


def test_detect_transitions():
    cues = [
        SrtCue(idx=1, start_ms=0, end_ms=1000, text="Intro"),
        SrtCue(idx=2, start_ms=1000, end_ms=2000, text="Next slide, the main idea"),
    ]

    assert detect_transitions(cues) == [2]


def test_align_slides_to_cues_is_monotonic():
    slides = parse_slides_markdown(
        """
<!-- slide_idx: 1 -->
First slide

<!-- slide_idx: 2 -->
Second slide
"""
    )
    cues = [
        SrtCue(idx=1, start_ms=0, end_ms=1000, text="A"),
        SrtCue(idx=2, start_ms=1000, end_ms=2000, text="Next slide B"),
        SrtCue(idx=3, start_ms=2000, end_ms=3000, text="C"),
        SrtCue(idx=4, start_ms=3000, end_ms=4000, text="D"),
    ]

    aligned = align_slides_to_cues(slides, cues)

    assert aligned[0]["cue_range"][0] <= aligned[1]["cue_range"][0]
    assert 2 in {idx for row in aligned for idx in row["detected_transitions"]}
