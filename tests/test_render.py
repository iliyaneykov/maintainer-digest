from maintainer_digest.models import Author, Issue, PullRequest
from maintainer_digest.render import render_digest


def test_render_digest_contains_sections():
    issue = Issue(1, "Crash on startup", "open", "", Author("u"), comments=2, body="crash")
    pr = PullRequest(
        2, "fix: startup crash", "open", "", Author("u"), additions=10, changed_files=1
    )
    output = render_digest("example/project", [issue], [pr])
    assert "Maintainer digest" in output
    assert "Issues needing triage" in output
    assert "Pull requests needing attention" in output
