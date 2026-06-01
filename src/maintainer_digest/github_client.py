from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from .models import Issue, PullRequest

GITHUB_API = "https://api.github.com"


class GitHubError(RuntimeError):
    pass


@dataclass(frozen=True)
class GitHubClient:
    token: str | None = None
    api_base: str = GITHUB_API

    @classmethod
    def from_env(cls) -> GitHubClient:
        return cls(token=os.getenv("GITHUB_TOKEN"))

    def _request(self, path: str, params: dict[str, str] | None = None) -> Any:
        query = ""
        if params:
            query = "?" + urllib.parse.urlencode(params)
        url = f"{self.api_base}{path}{query}"
        request = urllib.request.Request(url)
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        request.add_header("User-Agent", "maintainer-digest/0.1")
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")

        try:
            with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise GitHubError(f"GitHub API returned {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise GitHubError(f"Could not reach GitHub API: {exc.reason}") from exc

    def list_open_issues(self, repo: str, limit: int = 50) -> list[Issue]:
        owner, name = _split_repo(repo)
        payload = self._request(
            f"/repos/{owner}/{name}/issues",
            {"state": "open", "per_page": str(min(limit, 100)), "sort": "updated"},
        )
        return [Issue.from_github(item) for item in payload if "pull_request" not in item]

    def list_open_pull_requests(self, repo: str, limit: int = 50) -> list[PullRequest]:
        owner, name = _split_repo(repo)
        payload = self._request(
            f"/repos/{owner}/{name}/pulls",
            {"state": "open", "per_page": str(min(limit, 100)), "sort": "updated"},
        )
        return [PullRequest.from_github(item) for item in payload]

    def list_merged_pull_requests(self, repo: str, limit: int = 50) -> list[PullRequest]:
        owner, name = _split_repo(repo)
        payload = self._request(
            f"/repos/{owner}/{name}/pulls",
            {"state": "closed", "per_page": str(min(limit, 100)), "sort": "updated"},
        )
        return [PullRequest.from_github(item) for item in payload if item.get("merged_at")]


def _split_repo(repo: str) -> tuple[str, str]:
    parts = repo.strip().split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("Repository must use owner/name format, for example: openai/codex")
    return parts[0], parts[1]
