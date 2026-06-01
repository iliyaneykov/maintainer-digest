from maintainer_digest.models import Author, Issue, PullRequest
from maintainer_digest.scoring import priority_bucket, score_issue, score_pull_request


def test_security_issue_scores_high():
    issue = Issue(
        number=1,
        title="Security vulnerability in token handling",
        state="open",
        url="",
        author=Author("alice", "NONE"),
        labels=("needs triage",),
        comments=5,
        body="possible CVE / token leak",
    )
    assert score_issue(issue) >= 25
    assert priority_bucket(score_issue(issue)) in {"medium", "high"}


def test_draft_pr_scores_lower_than_small_fix():
    draft = PullRequest(
        number=1,
        title="WIP large refactor",
        state="open",
        url="",
        author=Author("bob", "CONTRIBUTOR"),
        draft=True,
        additions=3000,
        deletions=2000,
        changed_files=80,
    )
    fix = PullRequest(
        number=2,
        title="fix: small regression",
        state="open",
        url="",
        author=Author("bob", "CONTRIBUTOR"),
        labels=("bug",),
        additions=20,
        deletions=5,
        changed_files=1,
    )
    assert score_pull_request(fix) > score_pull_request(draft)
