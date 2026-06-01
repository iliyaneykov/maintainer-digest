from __future__ import annotations

from collections.abc import Iterable

LABEL_RULES: dict[str, tuple[str, ...]] = {
    "bug": ("bug", "error", "exception", "crash", "broken", "fails", "failure"),
    "security": ("security", "vulnerability", "cve", "xss", "csrf", "rce", "injection"),
    "regression": ("regression", "used to work", "after upgrade", "since version"),
    "documentation": ("docs", "documentation", "readme", "example", "typo"),
    "performance": ("slow", "performance", "latency", "memory", "cpu", "timeout"),
    "question": ("how do i", "question", "help", "is it possible", "support"),
    "good first issue": ("beginner", "easy", "simple", "small change"),
    "release": ("release", "changelog", "version", "semver"),
}


def suggest_labels(title: str, body: str = "", existing: Iterable[str] = ()) -> list[str]:
    """Suggest labels using deterministic keyword rules."""
    text = f"{title}\n{body}".lower()
    existing_normalized = {label.lower() for label in existing}
    suggestions: list[str] = []

    for label, keywords in LABEL_RULES.items():
        if label in existing_normalized:
            continue
        if any(keyword in text for keyword in keywords):
            suggestions.append(label)

    if not suggestions:
        suggestions.append("needs triage")

    return suggestions
