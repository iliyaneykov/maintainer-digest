from maintainer_digest.models import Author, PullRequest
from maintainer_digest.release_notes import build_release_notes


def test_release_notes_group_by_labels():
    prs = [
        PullRequest(1, "feat: add parser", "closed", "", Author("a"), labels=("feature",)),
        PullRequest(2, "fix: handle crash", "closed", "", Author("b"), labels=("bug",)),
    ]
    notes = build_release_notes(prs)
    assert "## Features" in notes
    assert "## Fixes" in notes
    assert "add parser" in notes
