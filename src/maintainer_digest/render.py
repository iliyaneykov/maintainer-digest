from __future__ import annotations

from collections.abc import Iterable

from .labels import suggest_labels
from .models import Issue, PullRequest
from .scoring import priority_bucket, score_issue, score_pull_request

_MD_ESCAPE = str.maketrans({"[": "\\[", "]": "\\]", "(": "\\(", ")": "\\)"})


def render_digest(repo: str, issues: Iterable[Issue], prs: Iterable[PullRequest]) -> str:
    issue_rows = sorted(
        ((score_issue(issue), issue) for issue in issues), reverse=True, key=lambda x: x[0]
    )
    pr_rows = sorted(
        ((score_pull_request(pr), pr) for pr in prs), reverse=True, key=lambda x: x[0]
    )

    lines: list[str] = [f"# Maintainer digest for `{repo}`", ""]
    lines.extend(_render_prs(pr_rows[:10]))
    lines.extend(_render_issues(issue_rows[:10]))
    lines.extend(_render_next_steps(issue_rows, pr_rows))
    return "\n".join(lines).rstrip() + "\n"


def _render_prs(rows: list[tuple[int, PullRequest]]) -> list[str]:
    lines = ["## Pull requests needing attention", ""]
    if not rows:
        return lines + ["No open pull requests found.", ""]
    for score, pr in rows:
        size = pr.additions + pr.deletions
        labels = ", ".join(pr.labels) if pr.labels else "no labels"
        lines.append(
            f"- **{priority_bucket(score)} / {score}** #{pr.number} "
            f"{pr.title.translate(_MD_ESCAPE)} ({labels}; {pr.changed_files} files; {size} lines)"
        )
    lines.append("")
    return lines


def _render_issues(rows: list[tuple[int, Issue]]) -> list[str]:
    lines = ["## Issues needing triage", ""]
    if not rows:
        return lines + ["No open issues found.", ""]
    for score, issue in rows:
        labels = ", ".join(issue.labels) if issue.labels else "no labels"
        suggested = ", ".join(suggest_labels(issue.title, issue.body, issue.labels))
        lines.append(
            f"- **{priority_bucket(score)} / {score}** #{issue.number} "
            f"{issue.title.translate(_MD_ESCAPE)} ({labels}; "
            f"suggested: {suggested}; comments: {issue.comments})"
        )
    lines.append("")
    return lines


def _render_next_steps(
    issue_rows: list[tuple[int, Issue]], pr_rows: list[tuple[int, PullRequest]]
) -> list[str]:
    high_issues = sum(1 for score, _issue in issue_rows if priority_bucket(score) == "high")
    high_prs = sum(1 for score, _pr in pr_rows if priority_bucket(score) == "high")
    return [
        "## Suggested maintainer workflow",
        "",
        f"- Review {high_prs} high-priority PR(s) first.",
        f"- Triage {high_issues} high-priority issue(s) before broad backlog work.",
        "- Use the release-notes command after merging PRs to produce a draft changelog.",
        "",
    ]
