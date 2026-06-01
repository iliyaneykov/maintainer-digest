# Agent instructions

This repository builds a small OSS maintainer automation CLI.

When changing code:

- Keep runtime dependencies at zero unless there is a strong reason.
- Prefer deterministic, auditable rules before AI-generated output.
- Do not add automation that comments on GitHub, changes labels, or merges PRs without an explicit dry-run mode and documentation.
- Add tests for scoring, label, and rendering behavior.
- Keep CLI output stable and Markdown-friendly.
- Do not claim this project is affiliated with OpenAI, GitHub, or Microsoft.

Useful commands:

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
```
