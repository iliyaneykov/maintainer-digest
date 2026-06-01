from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from .models import PullRequest

SECTION_RULES = {
    "Breaking changes": ("breaking", "breaking-change", "major"),
    "Features": ("feature", "enhancement", "feat"),
    "Fixes": ("bug", "fix", "regression"),
    "Security": ("security", "cve"),
    "Documentation": ("documentation", "docs"),
    "Maintenance": ("dependencies", "chore", "ci", "tests"),
}


def _section_for(pr: PullRequest) -> str:
    labels = {label.lower() for label in pr.labels}
    title = pr.title.lower()
    for section, markers in SECTION_RULES.items():
        if labels.intersection(markers) or any(marker in title for marker in markers):
            return section
    return "Other changes"


def build_release_notes(prs: Iterable[PullRequest]) -> str:
    sections: dict[str, list[PullRequest]] = defaultdict(list)
    for pr in prs:
        sections[_section_for(pr)].append(pr)

    order = [*SECTION_RULES.keys(), "Other changes"]
    output: list[str] = ["# Release notes draft", ""]
    wrote_section = False

    for section in order:
        items = sections.get(section, [])
        if not items:
            continue
        wrote_section = True
        output.append(f"## {section}")
        output.append("")
        for pr in sorted(items, key=lambda p: p.number):
            output.append(f"- {pr.title} (#{pr.number})")
        output.append("")

    if not wrote_section:
        output.append("No merged pull requests found for this range.")
        output.append("")

    return "\n".join(output).rstrip() + "\n"
