# Contributing

Maintainer feedback is the most valuable contribution. Useful issues include:

- Examples of triage rules that surfaced the wrong item.
- Release-note grouping mistakes.
- Repository workflows this tool should support.
- Security or privacy risks in generated prompts.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
```

## Pull request expectations

- Include tests for behavior changes.
- Update README/docs for CLI changes.
- Keep runtime dependencies minimal.
- Explain why a new rule helps maintainers make better decisions.
