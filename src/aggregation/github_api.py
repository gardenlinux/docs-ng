"""GitHub API HTTP client for docs aggregation.

This module is the single entry point for all GitHub HTTP calls in docs.
Future callers should use :func:`get_json` or :func:`list_repo_releases` rather
than writing ad-hoc HTTP requests.

Authentication
--------------
Set the ``GITHUB_TOKEN`` environment variable to a personal access token (PAT)
or an OAuth token.  No scopes are required for accessing public repositories.
When ``GITHUB_TOKEN`` is not set (or is empty after stripping whitespace),
requests are sent unauthenticated; GitHub applies a rate limit of 60 requests
per hour for unauthenticated access vs. 5 000 per hour for authenticated access.

Recommended for local development::

    export GITHUB_TOKEN=$(gh auth token)

Failure handling
----------------
Any network error, non-2xx HTTP status, rate-limit response (403 with
``X-RateLimit-Remaining: 0``), or JSON decode error raises
:class:`GitHubAPIError`.  Callers should let this propagate so the make target
can hard-fail with a non-zero exit code.
"""

import json
import os
import urllib.error
import urllib.request
from typing import Any

GITHUB_API_BASE = "https://api.github.com"


class GitHubAPIError(Exception):
    """Raised when any GitHub API request fails.

    The message includes the HTTP status code (when available) and the values
    of the ``X-RateLimit-Remaining`` and ``X-RateLimit-Reset`` response headers
    so that CI logs surface actionable information immediately.
    """


def _build_request(url: str) -> urllib.request.Request:
    """Build a :class:`urllib.request.Request` with standard GitHub API headers.

    Adds ``Authorization: Bearer <token>`` when ``GITHUB_TOKEN`` is set and
    non-empty.
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "gardenlinux-docs",
    }

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return urllib.request.Request(url, headers=headers)


def get_json(url: str) -> Any:
    """Perform a GET request to *url* and return the parsed JSON body.

    Args:
        url: Fully-qualified HTTPS URL of the GitHub API endpoint.

    Returns:
        Parsed JSON value (usually a :class:`list` or :class:`dict`).

    Raises:
        GitHubAPIError: On any network error, non-2xx HTTP status, or JSON
            decode failure.  The error message includes rate-limit headers when
            present.
    """
    req = _build_request(url)

    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        # Extract rate-limit info from error headers when available.
        rate_remaining = None
        rate_reset = None
        if exc.headers:
            rate_remaining = exc.headers.get("X-RateLimit-Remaining")
            rate_reset = exc.headers.get("X-RateLimit-Reset")

        msg = f"GitHub API request failed: HTTP {exc.code} for {url}"
        if rate_remaining is not None:
            msg += f" (X-RateLimit-Remaining: {rate_remaining}"
            if rate_reset is not None:
                msg += f", X-RateLimit-Reset: {rate_reset}"
            msg += ")"
        if rate_remaining == "0":
            msg += (
                " — rate limit exhausted; set GITHUB_TOKEN to raise the limit "
                "(export GITHUB_TOKEN=$(gh auth token))"
            )
        raise GitHubAPIError(msg) from exc
    except urllib.error.URLError as exc:
        raise GitHubAPIError(
            f"GitHub API request failed (network error) for {url}: {exc.reason}"
        ) from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise GitHubAPIError(
            f"GitHub API returned invalid JSON for {url}: {exc}"
        ) from exc


def list_repo_releases(
    owner: str, repo: str, per_page: int = 100
) -> list[dict]:
    """Fetch every release for *owner*/*repo* from the GitHub Releases API.

    Paginates automatically until GitHub returns an empty page.  The full list
    is returned only after all pages have been fetched successfully; a partial
    list is never returned on error.

    Args:
        owner: GitHub organisation or user name (e.g. ``"gardenlinux"``).
        repo: Repository name (e.g. ``"gardenlinux"``).
        per_page: Number of releases to request per page (max 100).

    Returns:
        List of release objects as returned by the GitHub Releases API.

    Raises:
        GitHubAPIError: On any fetch failure *or* when the first page is empty
            (indicating the repository has no releases, which would break the
            generated documentation).  See module docstring for ``GITHUB_TOKEN``
            advice.
    """
    all_releases: list[dict] = []
    page = 1

    while True:
        url = (
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/releases"
            f"?per_page={per_page}&page={page}"
        )
        page_data = get_json(url)

        if not isinstance(page_data, list):
            raise GitHubAPIError(
                f"GitHub API returned unexpected type for releases page {page}: "
                f"{type(page_data).__name__}"
            )

        if len(page_data) == 0:
            break

        all_releases.extend(page_data)
        page += 1

    if not all_releases:
        raise GitHubAPIError(
            f"GitHub API returned zero releases for {owner}/{repo}.  "
            "If this is unexpected, check that the repository exists and that "
            "GITHUB_TOKEN (if set) has access to it.  "
            "Set GITHUB_TOKEN to authenticate: export GITHUB_TOKEN=$(gh auth token)"
        )

    return all_releases
