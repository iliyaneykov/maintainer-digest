from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def parse_datetime(value: str | None) -> datetime | None:
    """Parse GitHub ISO datetimes while accepting missing values."""
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Author:
    login: str = "unknown"
    association: str = "NONE"

    @classmethod
    def from_github(cls, payload: dict[str, Any]) -> Author:
        user = payload.get("user") or {}
        return cls(
            login=str(user.get("login") or "unknown"),
            association=str(payload.get("author_association") or "NONE"),
        )


@dataclass(frozen=True)
class Issue:
    number: int
    title: str
    state: str
    url: str
    author: Author
    labels: tuple[str, ...] = ()
    created_at: datetime | None = None
    updated_at: datetime | None = None
    comments: int = 0
    body: str = ""
    is_pull_request: bool = False

    @classmethod
    def from_github(cls, payload: dict[str, Any]) -> Issue:
        labels = tuple(str(label.get("name", "")) for label in payload.get("labels", []))
        return cls(
            number=int(payload.get("number") or 0),
            title=str(payload.get("title") or ""),
            state=str(payload.get("state") or "unknown"),
            url=str(payload.get("html_url") or payload.get("url") or ""),
            author=Author.from_github(payload),
            labels=tuple(label for label in labels if label),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
            comments=int(payload.get("comments") or 0),
            body=str(payload.get("body") or ""),
            is_pull_request="pull_request" in payload,
        )


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    state: str
    url: str
    author: Author
    labels: tuple[str, ...] = ()
    created_at: datetime | None = None
    updated_at: datetime | None = None
    merged_at: datetime | None = None
    draft: bool = False
    additions: int = 0
    deletions: int = 0
    changed_files: int = 0
    body: str = ""

    @classmethod
    def from_github(cls, payload: dict[str, Any]) -> PullRequest:
        labels = tuple(str(label.get("name", "")) for label in payload.get("labels", []))
        return cls(
            number=int(payload.get("number") or 0),
            title=str(payload.get("title") or ""),
            state=str(payload.get("state") or "unknown"),
            url=str(payload.get("html_url") or payload.get("url") or ""),
            author=Author.from_github(payload),
            labels=tuple(label for label in labels if label),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
            merged_at=parse_datetime(payload.get("merged_at")),
            draft=bool(payload.get("draft") or False),
            additions=int(payload.get("additions") or 0),
            deletions=int(payload.get("deletions") or 0),
            changed_files=int(payload.get("changed_files") or 0),
            body=str(payload.get("body") or ""),
        )


@dataclass
class Digest:
    repository: str
    generated_at: datetime = field(default_factory=utc_now)
    issues: list[Issue] = field(default_factory=list)
    pull_requests: list[PullRequest] = field(default_factory=list)
