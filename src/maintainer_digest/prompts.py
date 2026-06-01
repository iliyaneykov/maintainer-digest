from __future__ import annotations

import re

from .models import Issue, PullRequest
from .scoring import score_issue, score_pull_request

_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def _sanitize(text: str, max_len: int = 120) -> str:
    """Strip HTML comments and newlines that could inject content into an LLM prompt."""
    text = _HTML_COMMENT.sub("", text)
    text = text.replace("\n", " ").replace("\r", " ")
    return text[:max_len].strip()


def build_codex_triage_prompt(repo: str, issues: list[Issue], prs: list[PullRequest]) -> str:
    """Build a compact prompt that can be pasted into Codex or another coding agent."""
    lines = [
        f"You are helping maintain `{repo}`.",
        "Prioritize maintainer work. Be terse, identify risks, and propose concrete next actions.",
        "Do not claim you executed code unless evidence is provided.",
        "",
        "Open pull requests:",
    ]
    for pr in sorted(prs, key=score_pull_request, reverse=True)[:15]:
        diff = pr.additions + pr.deletions
        score = score_pull_request(pr)
        lines.append(
            f"- PR #{pr.number}: {_sanitize(pr.title)}; labels={list(pr.labels)}; "
            f"files={pr.changed_files}; diff={diff}; score={score}"
        )
    lines.append("")
    lines.append("Open issues:")
    for issue in sorted(issues, key=score_issue, reverse=True)[:20]:
        score = score_issue(issue)
        lines.append(
            f"- Issue #{issue.number}: {_sanitize(issue.title)}; labels={list(issue.labels)}; "
            f"comments={issue.comments}; score={score}"
        )
    lines.append("")
    lines.append("Return: 1) urgent items, 2) likely labels, 3) PR review queue, 4) release risks.")
    return "\n".join(lines) + "\n"
