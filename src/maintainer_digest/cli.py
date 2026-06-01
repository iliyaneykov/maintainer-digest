from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .fixtures import load_issues, load_pull_requests
from .github_client import GitHubClient, GitHubError
from .labels import suggest_labels
from .prompts import build_codex_triage_prompt
from .release_notes import build_release_notes
from .render import render_digest


def _write_or_print(content: str, out: str | None) -> None:
    if out:
        Path(out).write_text(content, encoding="utf-8")
    else:
        print(content, end="")


def _load_or_fetch(args: argparse.Namespace):
    if args.issues_file:
        issues = load_issues(args.issues_file)
    else:
        issues = GitHubClient.from_env().list_open_issues(args.repo, args.limit)

    if args.prs_file:
        prs = load_pull_requests(args.prs_file)
    else:
        prs = GitHubClient.from_env().list_open_pull_requests(args.repo, args.limit)

    return issues, prs


def cmd_digest(args: argparse.Namespace) -> int:
    issues, prs = _load_or_fetch(args)
    _write_or_print(render_digest(args.repo, issues, prs), args.out)
    return 0


def cmd_prompt(args: argparse.Namespace) -> int:
    issues, prs = _load_or_fetch(args)
    _write_or_print(build_codex_triage_prompt(args.repo, issues, prs), args.out)
    return 0


def cmd_labels(args: argparse.Namespace) -> int:
    suggestions = suggest_labels(args.title, args.body or "", args.existing or [])
    _write_or_print("\n".join(suggestions) + "\n", args.out)
    return 0


def cmd_release_notes(args: argparse.Namespace) -> int:
    if args.prs_file:
        prs = load_pull_requests(args.prs_file)
    else:
        prs = GitHubClient.from_env().list_merged_pull_requests(args.repo, args.limit)
    _write_or_print(build_release_notes(prs), args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-digest",
        description="Generate issue, PR, and release digests for OSS maintainers.",
    )
    parser.add_argument("--version", action="version", version="maintainer-digest 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    digest = subparsers.add_parser("digest", help="Generate a maintainer digest")
    digest.add_argument("--repo", required=True, help="GitHub repository in owner/name format")
    digest.add_argument("--issues-file", help="Use local GitHub issue JSON fixture")
    digest.add_argument("--prs-file", help="Use local GitHub PR JSON fixture")
    digest.add_argument("--limit", type=int, default=50, help="Maximum GitHub records to fetch")
    digest.add_argument("--out", help="Write output to a file")
    digest.set_defaults(func=cmd_digest)

    prompt = subparsers.add_parser("prompt", help="Build a compact prompt for Codex/LLM triage")
    prompt.add_argument("--repo", required=True, help="GitHub repository in owner/name format")
    prompt.add_argument("--issues-file", help="Use local GitHub issue JSON fixture")
    prompt.add_argument("--prs-file", help="Use local GitHub PR JSON fixture")
    prompt.add_argument("--limit", type=int, default=50, help="Maximum GitHub records to fetch")
    prompt.add_argument("--out", help="Write output to a file")
    prompt.set_defaults(func=cmd_prompt)

    labels = subparsers.add_parser("labels", help="Suggest labels from issue text")
    labels.add_argument("--title", required=True)
    labels.add_argument("--body", default="")
    labels.add_argument("--existing", nargs="*", default=[])
    labels.add_argument("--out", help="Write output to a file")
    labels.set_defaults(func=cmd_labels)

    notes = subparsers.add_parser("release-notes", help="Draft release notes from merged PRs")
    notes.add_argument("--repo", required=True, help="GitHub repository in owner/name format")
    notes.add_argument("--prs-file", help="Use local GitHub PR JSON fixture")
    notes.add_argument("--limit", type=int, default=50, help="Maximum GitHub records to fetch")
    notes.add_argument("--out", help="Write output to a file")
    notes.set_defaults(func=cmd_release_notes)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (GitHubError, ValueError, OSError) as exc:
        parser.exit(1, f"maintainer-digest: error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
