from lecture_align_kit.srt import parse_srt_text


def test_parse_srt_text_renumbers_and_converts_time():
    cues = parse_srt_text(
        """
7
00:00:01,500 --> 00:00:03,250
First cue

8
00:00:04,000 --> 00:00:05,000
Second cue
"""
    )

    assert [cue.idx for cue in cues] == [1, 2]
    assert cues[0].start_ms == 1500
    assert cues[0].end_ms == 3250
    assert cues[1].text == "Second cue"


def test_parse_srt_text_empty():
    assert parse_srt_text("") == []
