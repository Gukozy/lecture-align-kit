# lecture-align-kit

Local-first utilities for aligning lecture slide text with SRT transcript cues.

This repository is an OSS candidate extracted from a private lecture automation
workflow. It intentionally contains only generic code and synthetic fixtures. It
does not include course materials, private transcripts, OAuth flows, school
folders, medical exam content, or provider-specific credentials.

## Why this exists

Lecture tooling often needs a reviewable bridge between:

- slide text exported as Markdown
- speech-to-text output exported as `.srt`
- a human-reviewable mapping before any downstream summarization

`lecture-align-kit` keeps that bridge small, testable, and local-first.

## Current scope

- Parse SRT subtitle cues without external dependencies.
- Parse slide Markdown files with `<!-- slide_idx: N -->` markers.
- Detect common transition phrases.
- Produce a deterministic, reviewable slide-to-cue assignment.
- Emit JSON for downstream tools.

Out of scope:

- No LLM calls.
- No automatic lecture summaries.
- No credential handling.
- No course-material downloaders.
- No medical, legal, or clinical claims.

## Install

```bash
python -m pip install -e .
```

## Quick start

```bash
lecture-align \
  --slides examples/synthetic_lecture/slides.md \
  --srt examples/synthetic_lecture/transcript.srt \
  --out /tmp/aligned.json
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## Safety and privacy

- Use synthetic or properly licensed input fixtures in public issues and tests.
- Do not commit real student, patient, classroom, or copyrighted lecture data.
- Do not commit API keys, OAuth files, transcripts from private sessions, or
  provider caches.

## Roadmap

- Add a richer scoring model that remains dependency-light.
- Add fixture validators for public issue reproduction.
- Add optional adapters for slide text exported from PDF/PPTX tools.
- Keep the core package separate from private course workflows.

## License

MIT. See `LICENSE`.
