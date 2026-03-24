#!/usr/bin/env python3
"""
Transform documentation content for VitePress integration
- Renames numbered directories (00_introduction -> introduction)
- Rewrites internal links
- Adds/fixes frontmatter
- Converts RST to Markdown (if needed)
"""

import argparse
import json
import os
import re
import shutil
import yaml
from pathlib import Path


def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)


def transform_directory_structure(
    source_dir, target_dir, structure_map, special_files=None, media_dirs=None
):
    """
    Transform directory structure based on mapping
    e.g., 00_introduction -> introduction
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    special_files = special_files or {}
    media_dirs = media_dirs or []

    if isinstance(structure_map, dict):
        # Structured transformation (e.g. with subdirectories specified in JSON file)
        for old_name, new_name in structure_map.items():
            old_path = source_path / old_name
            new_path = target_path / new_name

            if old_path.exists():
                print(f"  Transforming: {old_name} -> {new_name}")
                shutil.copytree(old_path, new_path, dirs_exist_ok=True)

        for item in source_path.iterdir():
            if item.name in structure_map:
                continue

            if item.name in special_files:
                target_subdir = target_path / special_files[item.name]
                target_subdir.mkdir(parents=True, exist_ok=True)
                if item.is_file():
                    print(f"  Moving {item.name} to {special_files[item.name]}")
                    shutil.copy2(item, target_subdir / item.name)
                elif item.is_dir():
                    print(f"  Moving {item.name} to {special_files[item.name]}")
                    shutil.copytree(item, target_subdir / item.name, dirs_exist_ok=True)
            elif item.name in media_dirs:
                print(f"  Copying media directory: {item.name}")
                shutil.copytree(item, target_path / item.name, dirs_exist_ok=True)
            elif item.is_file() and not item.name.startswith("_"):
                shutil.copy2(item, target_path / item.name)
            elif (
                item.is_dir()
                and not item.name.startswith("_")
                and not item.name.startswith(".")
            ):
                shutil.copytree(item, target_path / item.name, dirs_exist_ok=True)
    elif structure_map == "flat":
        # Flat structure. Only copy.
        print(f"  Copying flat structure")
        for item in source_path.glob("*"):
            if item.is_file():
                shutil.copy2(item, target_path / item.name)
            elif item.is_dir():
                shutil.copytree(item, target_path / item.name, dirs_exist_ok=True)
    elif structure_map == "sphinx":
        # Sphinx structure. Copy and convert later
        print(f"  Copying Sphinx structure (RST files)")
        for item in source_path.glob("*"):
            target_item = target_path / item.name
            if item.is_file():
                shutil.copy2(item, target_item)
            elif item.is_dir():
                shutil.copytree(item, target_item, dirs_exist_ok=True)
    else:
        # Default: simply copy
        shutil.copytree(source_path, target_path, dirs_exist_ok=True)


def rewrite_links(
    content,
    repo_name,
    file_rel_path="",
    base_path="/projects",
    github_base="https://github.com/gardenlinux",
):
    """
    Rewrite internal markdown links to work with VitePress structure

    Args:
        content: The markdown content
        repo_name: Name of the repository (e.g., "gardenlinux")
        file_rel_path: Relative path of the file within the repo (e.g., "introduction/index.md")
        base_path: Base path for projects (default: "/projects")
        github_base: Base URL for GitHub organization (default: "https://github.com/gardenlinux")

    Examples:
      [link](../01_developers/build.md) -> [link](/projects/gardenlinux/developers/build)
      [link](./intro.md) -> [link](/projects/gardenlinux/introduction/intro)
      [link](kernel.md) -> [link](/projects/gardenlinux/introduction/kernel) (when in introduction/)
      [link](/SECURITY.md) -> [link](https://github.com/gardenlinux/gardenlinux/blob/main/SECURITY.md)
    """

    file_dir = str(Path(file_rel_path).parent) if file_rel_path else ""
    if file_dir == ".":
        file_dir = ""

    def replace_link(match):
        text = match.group(1)
        link = match.group(2)

        if link.startswith("http://") or link.startswith("https://"):
            return match.group(0)

        if link.startswith("#"):
            return match.group(0)

        # Skip if already a /projects/ link
        if link.startswith(f"{base_path}/"):
            return match.group(0)

        # handle relative paths for .media directory
        if ".media/" in link:
            media_part = link
            while media_part.startswith("../"):
                media_part = media_part[3:]
            media_part = media_part.replace("./", "")
            new_link = f"{base_path}/{repo_name}/{media_part}"
            return f"[{text}]({new_link})"

        if link.startswith("../") or link.startswith("./"):
            stripped_link = link.replace(".md", "")

            # For ./ links (same directory), use the file's directory
            if link.startswith("./"):
                stripped_link = stripped_link.replace("./", "")
                if file_dir:
                    new_link = f"{base_path}/{repo_name}/{file_dir}/{stripped_link}"
                else:
                    new_link = f"{base_path}/{repo_name}/{stripped_link}"
            else:
                # For ../ links, check if they go outside docs/
                # Count how many levels up we go
                levels_up = link.count("../")
                stripped_link = stripped_link.replace("../", "")

                # Do we go outside docs/ ?
                if file_dir:
                    dir_depth = len(file_dir.split("/"))
                    if levels_up > dir_depth:
                        # Link to GitHub
                        new_link = f"{github_base}/{repo_name}/blob/main/{file_dir}"
                        return f"[{text}]({new_link})"

                stripped_link = re.sub(r"\d+_(\w+)", r"\1", stripped_link)
                new_link = f"{base_path}/{repo_name}/{stripped_link}"

            return f"[{text}]({new_link})"

        # Handle absolute paths from root
        if link.startswith("/"):
            # If it's already pointing to /projects/, leave it
            if link.startswith(f"{base_path}/"):
                return match.group(0)
            # Otherwise, this is a link to a file outside docs/ - point to GitHub
            stripped_link = link.lstrip("/")
            new_link = f"{github_base}/{repo_name}/blob/main/{stripped_link}"
            return f"[{text}]({new_link})"

        # Handle simple filenames (same directory)
        if "/" not in link:
            stripped_link = link.replace(".md", "")
            # If we know the file's directory, use it
            if file_dir:
                new_link = f"{base_path}/{repo_name}/{file_dir}/{stripped_link}"
            else:
                new_link = f"{base_path}/{repo_name}/{stripped_link}"
            return f"[{text}]({new_link})"

        return match.group(0)

    # Apply transform
    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, content)

    def replace_html_media_link(match):
        attr_name = match.group(1)
        link = match.group(2)

        if link.startswith(f"{base_path}/"):
            return match.group(0)
        if ".media/" in link:
            media_part = link
            while media_part.startswith("../"):
                media_part = media_part[3:]
            media_part = media_part.replace("./", "")
            new_link = f"{base_path}/{repo_name}/{media_part}"
            return f'{attr_name}="{new_link}"'
        return match.group(0)

    content = re.sub(
        r'(src|srcset)="([^"]*\.media/[^"]*)"', replace_html_media_link, content
    )

    return content


def escape_angle_brackets(content):
    """
    Escape angle brackets that are not part of HTML tags.

    This is needed for content like "<release number>" which should be
    displayed as text, not parsed as an HTML tag.

    Skip escaping inside:
    - Code blocks (``` or indented)
    - Inline code (``)
    """
    # Split content by code blocks and inline code to process only text parts
    lines = content.split("\n")
    result_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result_lines.append(line)
            continue

        if in_code_block:
            result_lines.append(line)
            continue

        if line.startswith("    ") or line.startswith("\t"):
            result_lines.append(line)
            continue

        parts = []
        in_inline_code = False
        current = ""
        i = 0

        while i < len(line):
            if line[i] == "`":
                if current:
                    if in_inline_code:
                        parts.append(current)
                    else:
                        parts.append(escape_text_angle_brackets(current))
                    current = ""
                parts.append("`")
                in_inline_code = not in_inline_code
                i += 1
            else:
                current += line[i]
                i += 1

        if current:
            if in_inline_code:
                parts.append(current)
            else:
                parts.append(escape_text_angle_brackets(current))

        result_lines.append("".join(parts))

    return "\n".join(result_lines)


def escape_text_angle_brackets(text):
    """
    Escape angle brackets in plain text (not in code).
    Only escape if they look like placeholders, not HTML tags.
    """
    import re

    known_html_tags = {
        "a",
        "b",
        "i",
        "u",
        "p",
        "div",
        "span",
        "br",
        "hr",
        "img",
        "picture",
        "source",
        "table",
        "tr",
        "td",
        "th",
        "ul",
        "ol",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "code",
        "pre",
        "blockquote",
        "em",
        "strong",
        "del",
        "ins",
        "sub",
        "sup",
        "html",
        "head",
        "body",
        "title",
        "link",
        "meta",
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "section",
        "article",
        "aside",
        "main",
        "figure",
        "figcaption",
        "details",
        "summary",
        "video",
        "audio",
        "iframe",
        "canvas",
        "svg",
        "path",
        "form",
        "input",
        "button",
        "select",
        "option",
        "textarea",
        "label",
    }

    def replace_bracket(match):
        content = match.group(1)

        tag_content = content.strip()
        if tag_content.startswith("/"):
            tag_content = tag_content[1:]

        tag_name = (
            tag_content.split()[0].lower()
            if " " in tag_content
            else tag_content.lower()
        )

        if tag_name in known_html_tags:
            return f"<{content}>"

        return f"&lt;{content}&gt;"

    text = re.sub(r"<([^>]+)>", replace_bracket, text)

    return text


def ensure_frontmatter(content):
    """
    Ensure frontmatter exists and fix YAML formatting.
    Only fixes existing frontmatter - does not inject new fields.
    
    Args:
        content: The markdown content
    """
    # Check if frontmatter already exists
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
            print(f"[Warning] Frontmatter: Couldn't parse existing frontmatter!")
            pass
    
    return content


def quote_yaml_value(value):
    """Quote YAML value if needed, handling already-quoted values."""
    # If value is already properly quoted, return as-is
    if value.startswith('"') and value.endswith('"'):
        # Check if it's properly quoted (not escaped quotes)
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
        # Don't escape quotes that are already inside the value
        # Just wrap in quotes
        if '"' not in value:
            return f'"{value}"'
        elif "'" not in value:
            return f"'{value}'"
        else:
            # If both quote types exist, escape double quotes and use them
            escaped_value = value.replace('"', '\\"')
            return f'"{escaped_value}"'

    return value


def fix_yaml_frontmatter(frontmatter_text):
    lines = frontmatter_text.split("\n")
    fixed_lines = []

    for line in lines:
        if not line.strip():
            fixed_lines.append(line)
            continue

        # Check if line contains a key-value pair
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


def fix_broken_project_links(
    content,
    repo_name,
    target_dir,
    base_path="/projects",
    github_base="https://github.com/gardenlinux",
):
    """
    In case a link in /projects/ points to a file that doesn't exist,
    replace it with a GitHub link.
    """
    target_path = Path(target_dir)

    def check_and_fix_link(match):
        text = match.group(1)
        link = match.group(2)

        # Only process /projects/{repo}/ links
        if not link.startswith(f"{base_path}/{repo_name}/"):
            return match.group(0)

        # Extract the path after /projects/{repo}/
        rel_path = link[len(f"{base_path}/{repo_name}/") :]

        potential_file = target_path / f"{rel_path}.md"
        potential_index = target_path / rel_path / "index.md"
        potential_dir = target_path / rel_path

        # If file or directory exists, keep the link
        if (
            potential_file.exists()
            or potential_index.exists()
            or (potential_dir.exists() and potential_dir.is_dir())
        ):
            return match.group(0)

        github_link = f"{github_base}/{repo_name}/blob/main/{rel_path}"
        return f"[{text}]({github_link})"

    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", check_and_fix_link, content)

    return content


def process_markdown_file(file_path, repo_name, target_dir, base_path="/projects"):
    """
    Process a single markdown file:
    - Escape angle brackets
    - Rewrite links
    - Fix broken project links
    - Fix frontmatter YAML formatting
    
    Args:
        file_path: Path to the markdown file
        repo_name: Name of the repository
        target_dir: Target directory where files are being processed
        base_path: Base path for projects (default: "/projects")
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Calculate relative path from target_dir
        file_path_obj = Path(file_path)
        target_path_obj = Path(target_dir)
        try:
            file_rel_path = str(file_path_obj.relative_to(target_path_obj))
        except ValueError:
            file_rel_path = ""

        content = escape_angle_brackets(content)
        content = rewrite_links(content, repo_name, file_rel_path, base_path)
        content = fix_broken_project_links(content, repo_name, target_dir, base_path)
        content = ensure_frontmatter(content)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"  [Warning] Error processing {file_path}: {e}")
        return False


def process_all_markdown(target_dir, repo_name):
    """
    Process all markdown files in target directory
    
    Args:
        target_dir: Target directory containing markdown files
        repo_name: Name of the repository
    """
    target_path = Path(target_dir)

    # Rename all README.md to index.md for VitePress
    readme_files = list(target_path.rglob("README.md"))
    for readme in readme_files:
        index_file = readme.parent / "index.md"
        if not index_file.exists():
            readme.rename(index_file)
            print(f"  Renamed {readme.relative_to(target_path)} to index.md")

    md_files = list(target_path.rglob("*.md"))

    print(f"  Processing {len(md_files)} markdown files...")

    success_count = 0
    for md_file in md_files:
        if process_markdown_file(md_file, repo_name, target_dir):
            success_count += 1

    print(f"  [Success] Processed {success_count}/{len(md_files)} files successfully")


def parse_frontmatter(content):
    """
    Parse YAML frontmatter from markdown content.
    Returns (frontmatter_dict, content_without_frontmatter) or (None, original_content)
    """
    if not content.startswith("---\n"):
        return None, content
    
    try:
        end_match = re.search(r"\n---\n", content[4:])
        if not end_match:
            return None, content
        
        frontmatter_text = content[4 : 4 + end_match.start()]
        rest_content = content[4 + end_match.end() :]
        
        frontmatter_dict = yaml.safe_load(frontmatter_text)
        return frontmatter_dict, rest_content
    except Exception as e:
        print(f"  [Warning] Failed to parse frontmatter: {e}")
        return None, content


def copy_targeted_docs(source_dir, docs_dir, repo_name):
    """
    Copy markdown files with 'github_target_path:' frontmatter to their specified locations.
    
    Args:
        source_dir: Source directory containing fetched docs (e.g., /tmp/xxx/gardenlinux)
        docs_dir: Target docs directory (e.g., /path/to/docs-ng/docs)
        repo_name: Name of the repository for logging
    """
    source_path = Path(source_dir)
    docs_path = Path(docs_dir)
    
    if not source_path.exists():
        print(f"  [Warning] Source directory not found: {source_dir}")
        return
    
    # Find all markdown files
    md_files = list(source_path.rglob("*.md"))
    targeted_files = []
    
    print(f"  Scanning {len(md_files)} files for 'github_target_path:' frontmatter...")
    
    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            frontmatter, _ = parse_frontmatter(content)
            
            # Check for 'github_target_path' in frontmatter
            if frontmatter and ("github_target_path" in frontmatter):
                target_path = frontmatter.get("github_target_path") or frontmatter.get("target")
                
                # Strip leading 'docs/' if present
                if target_path.startswith("docs/"):
                    target_path = target_path[5:]
                
                target_file = docs_path / target_path
                
                # Create parent directories if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the file
                shutil.copy2(md_file, target_file)
                
                # Apply markdown processing (but not project-specific link rewriting)
                # These files live in main docs tree, not under /projects/
                content = escape_angle_brackets(content)
                content = ensure_frontmatter(content)
                
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(content)
                
                targeted_files.append((md_file.relative_to(source_path), target_path))
                print(f"    ✓ Copied: {md_file.name} → {target_path}")
                
        except Exception as e:
            print(f"  [Warning] Error processing {md_file.name}: {e}")
    
    if targeted_files:
        print(f"  [Success] Copied {len(targeted_files)} targeted file(s)")
    else:
        print(f"  No files with 'github_target_path:' frontmatter found")


def transform_repo_docs(repo_config, docs_dir, temp_dir):
    """
    Transform documentation for a single repository
    """
    repo_name = repo_config["name"]
    print(f"\nTransforming docs for: {repo_name}")

    source_dir = os.path.join(temp_dir, repo_name)
    target_dir = os.path.join(docs_dir, repo_config["target_path"])

    structure = repo_config.get("structure", "flat")
    special_files = repo_config.get("special_files", {})
    media_dirs = repo_config.get("media_directories", [])

    # First, copy files with 'target:' frontmatter to their specified locations
    print(f"\n  Step 2a: Processing targeted files...")
    copy_targeted_docs(source_dir, docs_dir, repo_name)
    
    # Then, do the standard structure transformation to projects/ directory
    print(f"\n  Step 2b: Transforming project structure...")
    transform_directory_structure(
        source_dir, target_dir, structure, special_files, media_dirs
    )
    process_all_markdown(target_dir, repo_name)

    print(f"[Complete] Transformation complete for {repo_name}")


def main():
    parser = argparse.ArgumentParser(description="Transform documentation content")
    parser.add_argument("--config", required=True, help="Path to repos-config.json")
    parser.add_argument("--docs-dir", required=True, help="Path to docs directory")
    parser.add_argument(
        "--temp-dir",
        required=True,
        help="Path to temporary directory with fetched docs",
    )
    parser.add_argument("--repo", help="Only transform specific repo (optional)")

    args = parser.parse_args()

    config = load_config(args.config)

    for repo in config["repos"]:
        if args.repo and repo["name"] != args.repo:
            continue

        transform_repo_docs(repo, args.docs_dir, args.temp_dir)

    print("\n[Complete] All transformations complete!")


if __name__ == "__main__":
    main()
