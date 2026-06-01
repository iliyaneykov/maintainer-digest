from __future__ import annotations

import json
from pathlib import Path

from .models import Issue, PullRequest


def load_issues(path: str | Path) -> list[Issue]:
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Fixture file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(
            f"Issue fixture must be a JSON array, got {type(data).__name__} in {path}"
        )
    return [Issue.from_github(item) for item in data]


def load_pull_requests(path: str | Path) -> list[PullRequest]:
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Fixture file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(
            f"Pull request fixture must be a JSON array, got {type(data).__name__} in {path}"
        )
    return [PullRequest.from_github(item) for item in data]
