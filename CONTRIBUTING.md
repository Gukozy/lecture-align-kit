# Contributing

Thanks for considering a contribution.

## Ground rules

- Keep fixtures synthetic or clearly licensed for redistribution.
- Do not submit real private transcripts, course materials, medical records,
  student data, or credential files.
- Prefer small pull requests with tests.
- Keep the core package dependency-light.

## Local checks

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```
