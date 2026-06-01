# Maintainer Digest

Maintainer Digest is a small CLI for open-source maintainers who need a fast, repeatable view of what needs attention across GitHub issues, pull requests, and release notes.

It is intentionally boring: deterministic scoring first, LLM/Codex prompt generation second. That makes it safe to run in GitHub Actions and easy to audit before a maintainer asks an AI coding agent to help.

## Why this exists

Open-source maintainers spend a lot of time on non-coding work: issue triage, PR prioritization, release-note drafting, and handoff notes for contributors. Maintainer Digest turns GitHub metadata into a compact Markdown digest and a Codex-ready prompt.

## Features

- Generate a prioritized Markdown digest from open issues and PRs.
- Suggest labels from issue text using transparent rules.
- Draft release notes from merged PRs.
- Build a compact prompt for Codex or another coding agent.
- Run locally, in CI, or against fixture data with no network access.
- Uses only the Python standard library at runtime.

## Install

```bash
python -m pip install .
```

For development:

```bash
python -m pip install -e '.[dev]'
pytest
```

## Quick demo without GitHub access

```bash
maintainer-digest digest \
  --repo example/project \
  --issues-file examples/issues.json \
  --prs-file examples/prs.json
```

Generate a prompt for Codex:

```bash
maintainer-digest prompt \
  --repo example/project \
  --issues-file examples/issues.json \
  --prs-file examples/prs.json \
  --out codex-triage-prompt.txt
```

Suggest labels:

```bash
maintainer-digest labels \
  --title "Regression: CLI crashes after upgrading" \
  --body "This used to work in 0.7 but fails in 0.8"
```

Draft release notes from fixture PRs:

```bash
maintainer-digest release-notes \
  --repo example/project \
  --prs-file examples/prs.json
```

## Use against a live GitHub repository

Set a token for higher rate limits and private repository access:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

Then run:

```bash
maintainer-digest digest --repo owner/name --out MAINTAINER_DIGEST.md
```

## GitHub Actions workflow

This repo includes `.github/workflows/maintainer-digest.yml`, which can generate a scheduled digest as a workflow artifact. You can adapt it to open or update a tracking issue.

## How scoring works

The scorer is deliberately simple:

- Security, regression, crash, data loss, and urgent terms increase priority.
- Existing high-priority labels increase priority.
- Duplicate/question/wontfix-style labels lower priority.
- Old items and high-comment items are surfaced.
- Draft or very large PRs are deprioritized compared with small fixes.

See `src/maintainer_digest/scoring.py` for the full rules.

## Roadmap

- Optional OpenAI API summarizer with explicit dry-run mode.
- MCP server adapter for agent-native workflows.
- GitHub issue updater that maintains a rolling maintainer digest issue.
- More release-note grouping rules.
- Repository health dashboard.

## Project status

Alpha. The current version is useful for small repositories and fixture-based workflows, but the rules will need real maintainer feedback before a stable release.

## License

MIT
