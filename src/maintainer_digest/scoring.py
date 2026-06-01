from __future__ import annotations

from datetime import UTC, datetime

from .models import Issue, PullRequest

HOT_WORDS = {
    "bug": 4,
    "crash": 5,
    "security": 7,
    "vulnerability": 7,
    "regression": 6,
    "broken": 4,
    "release": 3,
    "urgent": 5,
    "data loss": 8,
    "memory leak": 5,
    "token leak": 8,
    "secret": 6,
}

LOW_PRIORITY_LABELS = {"question", "discussion", "wontfix", "duplicate", "invalid"}
HIGH_PRIORITY_LABELS = {"bug", "security", "regression", "p0", "p1", "critical"}
MAINTAINER_ASSOCIATIONS = {"MEMBER", "OWNER", "COLLABORATOR"}


def _age_days(value: datetime | None) -> int:
    if value is None:
        return 0
    now = datetime.now(UTC)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return max(0, (now - value).days)


def score_issue(issue: Issue) -> int:
    """Return a rough priority score from 0 to 100 for maintainer triage."""
    score = 10
    text = f"{issue.title}\n{issue.body}".lower()
    labels = {label.lower() for label in issue.labels}

    for word, points in HOT_WORDS.items():
        if word in text:
            score += points

    if labels & HIGH_PRIORITY_LABELS:
        score += 14
    if labels & LOW_PRIORITY_LABELS:
        score -= 8
    if issue.comments >= 10:
        score += 8
    elif issue.comments >= 3:
        score += 4

    age = _age_days(issue.updated_at or issue.created_at)
    if age >= 30:
        score += 8
    elif age >= 14:
        score += 5
    elif age >= 7:
        score += 2

    if issue.author.association not in MAINTAINER_ASSOCIATIONS:
        score += 3

    return max(0, min(100, score))


def score_pull_request(pr: PullRequest) -> int:
    """Return a rough priority score from 0 to 100 for PR review."""
    score = 10
    labels = {label.lower() for label in pr.labels}
    text = f"{pr.title}\n{pr.body}".lower()

    if pr.draft:
        score -= 10
    if labels & HIGH_PRIORITY_LABELS:
        score += 12
    if "dependencies" in labels or "dependabot" in pr.author.login.lower():
        score += 5
    if "security" in text or "cve" in text:
        score += 12

    size = pr.additions + pr.deletions
    if pr.changed_files > 25 or size > 1200:
        score -= 5
    elif pr.changed_files <= 5 and size <= 250:
        score += 6

    age = _age_days(pr.updated_at or pr.created_at)
    if age >= 21:
        score += 8
    elif age >= 7:
        score += 4

    return max(0, min(100, score))


def priority_bucket(score: int) -> str:
    if score >= 50:
        return "high"
    if score >= 25:
        return "medium"
    return "low"
