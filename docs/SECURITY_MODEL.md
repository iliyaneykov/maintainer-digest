# Security model

Maintainer Digest should be safe to run in CI because the default commands are deterministic and read-only.

## Defaults

- Runtime has no third-party dependencies.
- GitHub API access is read-only for digest generation.
- The CLI does not post comments, change labels, merge PRs, or write to GitHub.
- Generated prompts are local files unless the maintainer sends them elsewhere.

## Sensitive data

Issue and PR text may contain secrets or embargoed security details. Maintainers should review generated prompt files before sending them to any hosted model.

Planned mitigations:

- Optional redaction rules.
- Explicit `--allow-network-ai` style flag before any API summarization feature.
- Dry-run output for every command.
