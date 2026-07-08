"""Content transformation functions for documentation aggregation."""

import re
from pathlib import Path
from typing import Dict, Tuple


def rewrite_links(
    content: str,
    repo_name: str,
    file_rel_path: str = "",
    github_base: str = "https://github.com/gardenlinux",
) -> str:
    """
    Rewrite internal markdown links to work with VitePress structure.

    Only rewrites links that escape the docs tree (going too many levels up
    via ../), redirecting them to the corresponding GitHub URL.  All other
    links — relative, absolute /..., or ./ — are left unchanged for VitePress
    to resolve natively.

    Args:
        content: The markdown content
        repo_name: Name of the repository
        file_rel_path: Relative path of the file within the repo
        github_base: Base URL for GitHub organization

    Returns:
        Content with rewritten links
    """
    file_dir = str(Path(file_rel_path).parent) if file_rel_path else ""
    if file_dir == ".":
        file_dir = ""

    def replace_link(match):
        text = match.group(1)
        link = match.group(2)

        # Skip external links
        if link.startswith("http://") or link.startswith("https://"):
            return match.group(0)

        # Skip special protocols (mailto, tel, javascript, etc.)
        if (
            ":" in link
            and not link.startswith("/")
            and not link.startswith("./")
            and not link.startswith("../")
        ):
            return match.group(0)

        # Skip anchors
        if link.startswith("#"):
            return match.group(0)

        # Handle ../ links that go outside docs/ — redirect to GitHub
        if link.startswith("../"):
            levels_up = link.count("../")
            stripped_link = link.replace("../", "").replace(".md", "")

            if file_dir:
                dir_depth = len(file_dir.split("/"))
                if levels_up > dir_depth:
                    new_link = f"{github_base}/{repo_name}/blob/main/{stripped_link}"
                    return f"[{text}]({new_link})"

            # Inside docs tree: leave relative link unchanged for VitePress
            return match.group(0)

        # Handle absolute paths from root — redirect to GitHub
        if link.startswith("/"):
            # Link to file outside docs/ - point to GitHub
            stripped_link = link.lstrip("/")
            new_link = f"{github_base}/{repo_name}/blob/main/{stripped_link}"
            return f"[{text}]({new_link})"

        return match.group(0)

    # Apply transform to markdown links
    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, content)

    return content


def quote_yaml_value(value: str) -> str:
    """
    Quote YAML value if needed, handling already-quoted values.

    Args:
        value: YAML value to potentially quote

    Returns:
        Quoted value if needed, otherwise original value
    """
    # If value is already properly quoted, return as-is
    if value.startswith('"') and value.endswith('"'):
        if not value.startswith('"\\"'):
            return value

    if value.startswith("'") and value.endswith("'"):
        return value

    special_chars = [
        ":",
        "#",
        "@",
        "`",
        "|",
        ">",
        "*",
        "&",
        "!",
        "%",
        "[",
        "]",
        "{",
        "}",
        ",",
        "?",
    ]

    needs_quoting = any(char in value for char in special_chars)

    if value and (value[0] in ['"', "'", " "] or value[-1] in [" "]):
        needs_quoting = True

    if needs_quoting:
        if '"' not in value:
            return f'"{value}"'
        elif "'" not in value:
            return f"'{value}'"
        else:
            escaped_value = value.replace('"', '\\"')
            return f'"{escaped_value}"'

    return value


def parse_frontmatter(content: str) -> Tuple[Dict[str, str] | None, str]:
    """
    Parse YAML frontmatter from markdown content.

    Args:
        content: Markdown content potentially with frontmatter

    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
        or (None, original_content) if no frontmatter found.
    """
    if not content.startswith("---\n"):
        return None, content

    try:
        end_match = re.search(r"\n---\n", content[4:])
        if not end_match:
            return None, content

        frontmatter_text = content[4 : 4 + end_match.start()]
        rest_content = content[4 + end_match.end() :]

        frontmatter_dict = {}
        for line in frontmatter_text.split("\n"):
            line = line.strip()
            if not line or ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            frontmatter_dict[key] = value

        return frontmatter_dict, rest_content
    except Exception as e:
        print(f"  [Warning] Failed to parse frontmatter: {e}")
        return None, content


def fix_yaml_frontmatter(frontmatter_text: str) -> str:
    """
    Fix YAML frontmatter formatting.

    Args:
        frontmatter_text: Frontmatter content (without --- markers)

    Returns:
        Fixed frontmatter text
    """
    lines = frontmatter_text.split("\n")
    fixed_lines = []

    for line in lines:
        if not line.strip():
            fixed_lines.append(line)
            continue

        if ":" in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                quoted_value = quote_yaml_value(value)
                fixed_lines.append(f"{key}: {quoted_value}")
                continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def ensure_frontmatter(content: str) -> str:
    """
    Ensure frontmatter exists and fix YAML formatting.

    Args:
        content: Markdown content

    Returns:
        Content with fixed frontmatter
    """
    if content.startswith("---\n"):
        try:
            end_match = re.search(r"\n---\n", content[4:])
            if end_match:
                frontmatter_content = content[4 : 4 + end_match.start()]
                rest_content = content[4 + end_match.end() :]

                # Parse and fix the frontmatter
                fixed_frontmatter = fix_yaml_frontmatter(frontmatter_content)

                return f"---\n{fixed_frontmatter}\n---\n\n{rest_content}"
        except Exception:
            print("  [Warning] Couldn't parse existing frontmatter!")

    return content


def cleanup_github_markdown(content: str) -> str:
    """
    Clean up GitHub release notes markdown for VitePress compatibility.

    Handles common issues in GitHub release notes that cause VitePress parsing errors:
    - Orphaned code fences followed by headers
    - Empty code blocks
    - Inconsistent fence markers
    - Windows line endings
    - Content followed by fence on same line

    Args:
        content: Raw markdown from GitHub release notes

    Returns:
        Cleaned markdown safe for VitePress rendering
    """
    if not content:
        return content

    # Fix Windows line endings first
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    # Remove or fix HTML details/summary tags that cause parsing issues
    # Replace <details><summary>content</summary>content</details> with just content
    content = re.sub(r"<details><summary>([^<]*)</summary>", r"\1", content)
    content = re.sub(r"</details>", "", content)
    content = re.sub(r"<details>", "", content)
    content = re.sub(r"<summary>", "", content)
    content = re.sub(r"</summary>", "", content)

    # Fix patterns where content is followed by fence on same line
    # e.g., "tag```" or "content````" should become "tag\n```" or "content\n```"
    content = re.sub(r"([^`])````", r"\1\n```", content)
    content = re.sub(r"([^`])```$", r"\1\n```", content, flags=re.MULTILINE)
    content = re.sub(r"`````", "```", content)  # Fix five backticks
    content = re.sub(r"````", "```", content)  # Fix four backticks

    lines = content.split("\n")
    cleaned = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect code fence
        is_fence_start = stripped in ("```", "````", "`````")

        # Handle orphan fence followed by header (add blank line)
        if is_fence_start and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line.startswith("##") or next_line.startswith("# "):
                cleaned.append(line)
                cleaned.append("")  # Add blank line before header
                i += 1
                continue

        # Handle empty code block (fence followed immediately by another fence)
        if is_fence_start and i + 1 < len(lines):
            next_stripped = lines[i + 1].strip()
            if next_stripped in ("```", "````", "`````"):
                # Skip this empty block
                i += 2
                continue

        # Normalize fence markers (```` or ````` -> ```)
        if stripped == "````" or stripped == "`````":
            cleaned.append("```")
            i += 1
            continue

        cleaned.append(line)
        i += 1

    # Join and fix multiple blank lines
    content = "\n".join(cleaned)
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    return content
