"""Generate release documentation from GLRD."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

from .constants import (
    GANTT_THEME,
    RELEASES_TAG_URL,
    COMMITS_URL,
    LIFECYCLE_LINKS,
)


def run_glrd_json(args: list[str]) -> Optional[dict]:
    """Run glrd command with JSON output and return parsed data."""
    try:
        result = subprocess.run(
            ["glrd"] + args + ["--output-format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        print(f"glrd command failed: {result.stderr}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("glrd not found - install with: pip install glrd", file=sys.stderr)
        return None
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error running glrd: {e}", file=sys.stderr)
        return None


def format_version(release: dict) -> tuple[str, str]:
    """Extract version string and link from release data.

    Returns:
        Tuple of (version_string, version_link)
        - Minor releases: link to release notes page
        - Major releases: no link (just plain text)
    """
    version_obj = release.get("version", {})

    has_minor = "minor" in version_obj

    if "major" in version_obj and "minor" in version_obj:
        if "patch" in version_obj:
            version_str = f"{version_obj['major']}.{version_obj['minor']}.{version_obj['patch']}"
        else:
            version_str = f"{version_obj['major']}.{version_obj['minor']}"
    elif "major" in version_obj:
        version_str = str(version_obj["major"])
    else:
        return "N/A", "N/A"

    # Only link minor releases to release notes; major releases have no link
    if has_minor:
        version_link = f"[{version_str}](release-notes/{version_str.replace('.', '-')}.html)"
    else:
        version_link = version_str  # Major release - no link

    return version_str, version_link


def format_commit(release: dict) -> str:
    """Extract commit info and create GitHub link from release data."""
    git_info = release.get("git", {})
    commit_short = git_info.get("commit_short", "")
    commit_full = git_info.get("commit", "")

    if commit_short and commit_full:
        return f"[`{commit_short}`]({COMMITS_URL}/{commit_full})"
    elif commit_short:
        return f"`{commit_short}`"
    return "—"


def format_lifecycle_date(lifecycle: dict, key: str) -> str:
    """Extract and format lifecycle date with link."""
    date_obj = lifecycle.get(key, {})
    isodate = date_obj.get("isodate", "")

    if not isodate:
        return "—"

    # Map keys to LIFECYCLE_LINKS
    link_key = key
    if key == "released":
        link_key = "standard"  # released = start of standard maintenance

    anchor = LIFECYCLE_LINKS.get(link_key, "")
    return f"[{isodate}]({anchor})" if anchor else isodate


def generate_mermaid_gantt(releases_data: dict) -> str:
    """Generate Mermaid Gantt chart from GLRD JSON data."""
    if not releases_data or "releases" not in releases_data:
        return ""

    releases = releases_data.get("releases", [])
    major_releases = [r for r in releases if r.get("type") == "major"]

    if not major_releases:
        return ""

    gantt = GANTT_THEME + """
gantt
    title Garden Linux Release Maintenance Phases
    dateFormat YYYY-MM-DD
    axisFormat %m/%y
"""
    for release in major_releases:
        version = release.get("version", {}).get("major")
        if not version:
            continue

        lifecycle = release.get("lifecycle", {})
        released = lifecycle.get("released", {})
        extended = lifecycle.get("extended", {})
        eol = lifecycle.get("eol", {})

        if not released or not eol:
            continue

        released_date = released.get("isodate", "")
        extended_date = extended.get("isodate", "") if extended else ""
        eol_date = eol.get("isodate", "")

        if not released_date or not eol_date:
            continue

        gantt += f"    section {version}\n"

        if extended_date:
            gantt += f"    SMaint           :active, sm{version}, {released_date}, {extended_date}\n"
            gantt += f"    ExtMaint         :crit, em{version}, {extended_date}, {eol_date}\n"
        else:
            gantt += f"    SMaint           :active, sm{version}, {released_date}, {eol_date}\n"

        gantt += f"    EoMaint          :milestone, eom{version}, {eol_date}, 0d\n"

    return gantt


def generate_release_table(releases_data: dict) -> str:
    """Generate markdown table from GLRD JSON data."""
    if not releases_data or "releases" not in releases_data:
        return "*No releases found*"

    releases = releases_data.get("releases", [])
    if not releases:
        return "*No releases found*"

    table = "| Version | Commit | Standard Maintenance | Extended Maintenance | End of Maintenance |\n"
    table += "|:--------|:-------|:---------------------|:---------------------|:-------------------|\n"

    for release in releases:
        _, version_link = format_version(release)
        commit_link = format_commit(release)

        lifecycle = release.get("lifecycle", {})
        standard_maint = format_lifecycle_date(lifecycle, "released")
        extended_maint = format_lifecycle_date(lifecycle, "extended")
        eol_date = format_lifecycle_date(lifecycle, "eol")

        table += f"| {version_link} | {commit_link} | {standard_maint} | {extended_maint} | {eol_date} |\n"

    return table


def get_timeline_section(gantt_chart: str, title: str) -> str:
    """Build timeline section with Gantt chart and legend."""
    if not gantt_chart:
        return ""

    return f"""

## {title}

```mermaid
{gantt_chart}
```

**Legend:**
- **SMaint** = [Standard Maintenance]({LIFECYCLE_LINKS['standard']}) — Active maintenance with regular updates
- **ExtMaint** = [Extended Maintenance]({LIFECYCLE_LINKS['extended']}) — Critical CVE fixes only (CVSS ≥7.0)
- **EoMaint** = [End of Maintenance]({LIFECYCLE_LINKS['eol']}) — No further updates
"""


def build_release_page(title: str, intro: str, table: str, timeline: str, page_type: str = "maintained") -> str:
    """Build release page content with frontmatter and sections."""
    descriptions = {
        "maintained": "Currently maintained Garden Linux releases with support dates and timelines.",
        "archived": "Garden Linux releases that have reached end of maintenance and are no longer supported.",
    }
    orders = {
        "maintained": 2,
        "archived": 3,
    }

    further_reading = f"""

## Further Reading

- [Release Lifecycle](release-lifecycle.md) — Understanding Garden Linux release phases
- [Maintained Releases](maintained-releases.md) — Currently supported releases
- [Archived Releases](archived-releases.md) — Past releases no longer maintained
- [Release Notes](release-notes/) — Detailed release-specific notes
"""

    description = descriptions.get(page_type, "")
    order = orders.get(page_type, 2)

    return f"""---
title: "{title}"
description: "{description}"
order: {order}
---

# {title}

{intro}

:::tip All data is sourced from [GLRD](../../how-to/glrd.html)
:::

{table}{timeline}

{further_reading}

"""


def generate_release_docs(docs_dir: Path) -> bool:
    """Fetch release data from GLRD and generate release documentation pages."""
    releases_dir = docs_dir / "reference" / "releases"
    releases_dir.mkdir(parents=True, exist_ok=True)

    print("Generating release documentation from GLRD...")

    active_data = run_glrd_json(["--active"])
    archived_data = run_glrd_json(["--archived"])

    if active_data is None:
        print("Warning: Could not fetch active releases - skipping generation", file=sys.stderr)
        return False

    active_table = generate_release_table(active_data)
    active_gantt = generate_mermaid_gantt(active_data)
    active_timeline = get_timeline_section(active_gantt, "Release Timeline")

    active_content = build_release_page(
        "Maintained Releases",
        "The table below provides the current list of actively maintained Garden Linux releases. For details about the release lifecycle phases, see [Release Lifecycle](release-lifecycle.md).",
        f"## Active Releases\n\n{active_table}",
        active_timeline,
        "maintained",
    )

    (releases_dir / "maintained-releases.md").write_text(active_content)
    print(f"  Created: {releases_dir / 'maintained-releases.md'}")

    if archived_data is not None:
        archived_table = generate_release_table(archived_data)
        archived_gantt = generate_mermaid_gantt(archived_data)
        archived_timeline = get_timeline_section(archived_gantt, "Archived Releases Timeline")

        archived_content = build_release_page(
            "Archived Releases",
            "The table below lists releases that have reached their end of maintenance and are no longer actively supported. If you use one of these versions, migrate to the latest maintained release as soon as possible. For details about the release lifecycle, see [Release Lifecycle](release-lifecycle.md).",
            f"## Out of Maintenance Releases\n\n{archived_table}",
            archived_timeline,
            "archived",
        )

        (releases_dir / "archived-releases.md").write_text(archived_content)
        print(f"  Created: {releases_dir / 'archived-releases.md'}")
    else:
        print("Warning: Could not fetch archived releases", file=sys.stderr)

    print("Release documentation generation complete.")
    return True
