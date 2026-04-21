"""Generate release documentation from GLRD."""

import json
import subprocess
import sys
from typing import Optional

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


def get_active_minor_versions() -> set[str]:
    """Get set of active minor release versions from GLRD.

    Returns:
        Set of version strings (e.g., {"1877.14", "2150.1.0"})
    """
    active_versions = set()

    try:
        result = subprocess.run(
            ["glrd", "--active", "--type", "minor", "--output-format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            releases = data.get("releases", [])
            for release in releases:
                version_obj = release.get("version", {})
                if "major" in version_obj and "minor" in version_obj:
                    if "patch" in version_obj:
                        version = f"{version_obj['major']}.{version_obj['minor']}.{version_obj['patch']}"
                    else:
                        version = f"{version_obj['major']}.{version_obj['minor']}"
                    active_versions.add(version)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Warning: Failed to query active minor versions: {e}", file=sys.stderr)

    return active_versions
