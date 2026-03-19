#!/usr/bin/env python3
"""
Update VitePress configuration with dynamically generated sidebars
for aggregated documentation from multiple repositories defined in repos-config.json.
"""

import argparse
import json
import re
from pathlib import Path


def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)


def get_section_priority(section, priority_map):
    section_name = section.get("text", "").lower()
    for key, priority in priority_map.items():
        if key in section_name:
            return priority
    return 999


def get_directory_structure(path, docs_dir=None):
    """
    Scan directory and build sidebar structure
    Returns list of sidebar items
    """
    items = []
    path = Path(path)

    if not path.exists():
        return items

    # If docs_dir not provided, use path.parent for backward compatibility
    if docs_dir is None:
        docs_dir = path.parent

    # Get all markdown files and directories
    # Sort with index or README files first, then alphabetically
    def sort_key(entry):
        if entry.name.lower() in ["index.md", "readme.md"]:
            return (0, entry.name)
        else:
            return (1, entry.name)

    entries = sorted(path.iterdir(), key=sort_key)

    # Track added index files for project
    index_added = False

    for entry in entries:
        if entry.name.startswith(".") or entry.name.startswith("_"):
            continue

        if entry.is_file() and entry.suffix == ".md":
            title = get_title_from_file(entry)
            if entry.name == "README.md" or entry.name == "index.md":
                # Add index files (prefer index.md over README.md)
                if not index_added:
                    link = "/" + str(entry.parent.relative_to(docs_dir))
                    if not link.endswith("/"):
                        link += "/"
                    items.append(
                        {
                            "text": title
                            or entry.parent.name.replace("-", " ")
                            .replace("_", " ")
                            .title(),
                            "link": link,
                        }
                    )
                    index_added = True
            else:
                link = "/" + str(entry.relative_to(docs_dir)).replace(".md", "")
                items.append(
                    {
                        "text": title
                        or entry.stem.replace("-", " ").replace("_", " ").title(),
                        "link": link,
                    }
                )

        elif entry.is_dir():
            sub_items = get_directory_structure(entry, docs_dir)

            if sub_items:
                dir_item = {
                    "text": entry.name.replace("-", " ").replace("_", " ").title(),
                    "collapsed": True,
                    "items": sub_items,
                }
                items.append(dir_item)

    return items


def get_title_from_file(file_path):
    """
    Extract title from markdown file (frontmatter or first heading)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter_match = re.search(
            r"^---\s*\ntitle:\s*(.+?)\s*\n", content, re.MULTILINE
        )
        if frontmatter_match:
            return frontmatter_match.group(1).strip()

        heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if heading_match:
            return heading_match.group(1).strip()
    except Exception:
        pass

    return None


def find_important_guides(repo_docs_path, docs_dir):
    """
    Find important guides like installation, quickstart, getting started, etc.
    Returns a dict with guide type as important and link as value
    """
    important_guides = {}

    guide_keywords = {
        "getting_started": [
            "getting_started",
            "getting-started",
            "gettingstarted",
            "get_started",
            "get-started",
        ],
        "quickstart": ["quickstart", "quick_start", "quick-start"],
        "installation": ["installation", "installing", "setup"],
    }

    for md_file in repo_docs_path.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.name.startswith("_"):
            continue

        filename = md_file.stem.lower()

        for guide_type, keywords in guide_keywords.items():
            if guide_type not in important_guides:
                for keyword in keywords:
                    if keyword in filename:
                        rel_path = md_file.relative_to(Path(docs_dir))
                        link = "/" + str(rel_path).replace(".md", "")

                        title = get_title_from_file(md_file)
                        if not title:
                            title = (
                                md_file.stem.replace("-", " ").replace("_", " ").title()
                            )

                        important_guides[guide_type] = {"link": link, "title": title}
                        break

    return important_guides


def create_missing_index_files(docs_dir, repos):
    """
    Create index.md files for directories that don't have them.
    This prevents dead links when linking to directory paths.
    Also fixes links in existing markdown files to add trailing slashes.
    """
    created_files = []
    directories_with_new_indexes = set()

    for repo in repos:
        target_path = repo["target_path"]
        repo_docs_path = Path(docs_dir) / target_path

        if not repo_docs_path.exists():
            continue

        for dirpath in repo_docs_path.rglob("*"):
            if not dirpath.is_dir():
                continue

            if dirpath.name.startswith(".") or dirpath.name.startswith("_"):
                continue

            has_index = (dirpath / "index.md").exists() or (
                dirpath / "README.md"
            ).exists()

            if not has_index:
                md_files = sorted([f for f in dirpath.glob("*.md") if f.is_file()])

                if md_files:
                    index_path = dirpath / "index.md"

                    dir_name = dirpath.name.replace("-", " ").replace("_", " ").title()

                    content = f"# {dir_name}\n\n"
                    content += f"This section contains the following guides:\n\n"

                    for md_file in md_files:
                        title = get_title_from_file(md_file)
                        if not title:
                            title = (
                                md_file.stem.replace("-", " ").replace("_", " ").title()
                            )

                        link = md_file.stem
                        content += f"- [{title}](./{link})\n"

                    with open(index_path, "w", encoding="utf-8") as f:
                        f.write(content)

                    created_files.append(str(index_path.relative_to(docs_dir)))
                    dir_path_str = "/" + str(dirpath.relative_to(docs_dir))
                    directories_with_new_indexes.add(dir_path_str)
                    print(
                        f"  [Success] Created index for: {dirpath.relative_to(docs_dir)}"
                    )

    if directories_with_new_indexes:
        print("\n  Fixing links to newly indexed directories...")
        for repo in repos:
            target_path = repo["target_path"]
            repo_docs_path = Path(docs_dir) / target_path

            if not repo_docs_path.exists():
                continue

            for md_file in repo_docs_path.rglob("*.md"):
                if not md_file.is_file():
                    continue

                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    modified = False
                    for dir_path in directories_with_new_indexes:
                        # Look for links to this directory without trailing slash
                        # Pattern: ](/path/to/dir) or ](/path/to/dir "title")
                        import re

                        pattern = re.compile(f"\\]\\({re.escape(dir_path)}(\\)|\\s)")
                        if pattern.search(content):
                            content = pattern.sub(f"]({dir_path}/\\1", content)
                            modified = True

                    if modified:
                        with open(md_file, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(
                            f"    [Success] Fixed links in: {md_file.relative_to(docs_dir)}"
                        )

                except Exception as e:
                    print(f"    [Warning] Could not process {md_file}: {e}")

    return created_files


def generate_sidebar_config(repo_config, docs_dir, section_priorities):
    """
    Generate sidebar configuration for a repository
    """
    repo_name = repo_config["name"]
    target_path = repo_config["target_path"]

    repo_docs_path = Path(docs_dir) / target_path

    if not repo_docs_path.exists():
        print(f"  [Warning] Docs path not found for {repo_name}: {repo_docs_path}")
        return None

    print(f"  Generating sidebar for: {repo_name}")

    items = get_directory_structure(repo_docs_path, Path(docs_dir))

    if not items:
        print(f"  [Warning] No items found for {repo_name}")
        return None

    items = sorted(items, key=lambda s: get_section_priority(s, section_priorities))

    sidebar_path = f"/projects/{repo_name}/"

    key_guides = find_important_guides(repo_docs_path, docs_dir)
    print(f"    Found key guides: {list(key_guides.keys())}")

    has_overview = (repo_docs_path / "index.md").exists() or (
        repo_docs_path / "README.md"
    ).exists()
    print(f"    Has overview page: {has_overview}")

    return {
        "path": sidebar_path,
        "items": items,
        "key_guides": key_guides,
        "has_overview": has_overview,
    }


def generate_nav_items(repos, sidebars):
    """
    Generate navigation dropdown items for projects
    For nav, we use simple links (not nested) since VitePress nav only supports 2 levels
    """
    nav_items = []

    # Create a map of repo name to sidebar for quick lookup
    sidebar_map = {s["path"].strip("/").split("/")[-1]: s for s in sidebars if s}

    for repo in repos:
        repo_name = repo["name"]
        # Use display name if configured, otherwise use repo name
        display_name = repo.get("display_name", repo_name.replace("-", " ").title())

        sidebar = sidebar_map.get(repo_name)

        link = None

        if sidebar:
            # Try to use one of the important guides as first link ("getting started", "quickstart", etc.)
            important_guides = sidebar.get("important_guides", {})
            for guide_type in ["getting_started", "quickstart", "installation"]:
                if guide_type in important_guides:
                    link = important_guides[guide_type]["link"]
                    break

            # If there is no important guide, check if there's an overview
            if not link and sidebar.get("has_overview"):
                link = f"/projects/{repo_name}/"

            # If still no link, use first section's first item
            if not link and sidebar.get("items") and len(sidebar["items"]) > 0:
                first_item = sidebar["items"][0]
                if "items" in first_item and len(first_item["items"]) > 0:
                    link = first_item["items"][0].get("link")
                elif "link" in first_item:
                    link = first_item["link"]

        if not link:
            link = f"/projects/{repo_name}/"

        nav_items.append({"text": display_name, "link": link})

    return nav_items


def generate_technical_docs_sidebar_items(repos, sidebars):
    """
    Generate expandable sidebar items for the Technical Documentation section.
    Uses the full sidebar structure with proper expandable sections.
    """
    sidebar_items = []

    sidebar_map = {s["path"].strip("/").split("/")[-1]: s for s in sidebars if s}

    for repo in repos:
        repo_name = repo["name"]
        display_name = repo.get("display_name", repo_name.replace("-", " ").title())

        sidebar = sidebar_map.get(repo_name)

        if not sidebar or not sidebar.get("items"):
            # Simple link if no sidebar found
            sidebar_items.append(
                {"text": display_name, "link": f"/projects/{repo_name}/"}
            )
            continue

        project_item = {"text": display_name, "collapsed": True, "items": []}

        important_guides = sidebar.get("important_guides", {})
        guide_order = ["quickstart", "getting_started", "installation"]
        important_guide_links = set()

        for guide_type in guide_order:
            if guide_type in important_guides:
                guide = important_guides[guide_type]
                project_item["items"].append(
                    {"text": guide["title"], "link": guide["link"]}
                )
                important_guide_links.add(guide["link"])

        # Add the full sidebar items (sections like Introduction, Developers, Operators)
        # Sort sections to put Introduction first
        sections = sidebar.get("items", [])

        section_priority = {
            "introduction": 0,
            "overview": 0,
            "developers": 1,
            "operators": 2,
        }

        def get_section_priority(section):
            section_name = section.get("text", "").lower()
            for key, priority in section_priority.items():
                if key in section_name:
                    return priority
            return 999

        sorted_sections = sorted(sections, key=get_section_priority)

        for section in sorted_sections:
            filtered_section = filter_section_items(section, important_guide_links)
            if filtered_section:
                project_item["items"].append(filtered_section)

        sidebar_items.append(project_item)

    return sidebar_items


def filter_section_items(section, exclude_links):
    """
    Recursively filter out items that are in the exclude_links set.
    Returns None if the section becomes empty after filtering.
    """
    if "items" in section:
        # This is a section with subitems
        filtered_items = []
        for item in section["items"]:
            filtered_item = filter_section_items(item, exclude_links)
            if filtered_item:
                filtered_items.append(filtered_item)

        if filtered_items:
            return {
                "text": section["text"],
                "collapsed": section.get("collapsed", True),
                "items": filtered_items,
            }
        else:
            return None
    elif "link" in section:
        # This is a direct link item
        if section["link"] not in exclude_links:
            return {"text": section["text"], "link": section["link"]}
        else:
            return None
    else:
        # Unknown structure, pass
        return section


def format_items_as_typescript(items, indent_level=3):
    """
    Format items array as TypeScript code

    Args:
        items: List of item dictionaries
        indent_level: Indentation level (3 = 12 spaces for alignment in nav, 4 = 14 spaces in sidebar)
    """
    indent = "  " * indent_level
    lines = []

    for item in items:
        if "items" in item:
            # Expandable item with subitems
            lines.append(f"{indent}{{")
            lines.append(f"{indent}  text: '{item['text']}',")
            if "collapsed" in item:
                collapsed = "true" if item["collapsed"] else "false"
                lines.append(f"{indent}  collapsed: {collapsed},")
            lines.append(f"{indent}  items: [")

            # Process subitems (can be links or nested sections)
            for subitem in item["items"]:
                if "items" in subitem:
                    # Nested section
                    nested_lines = format_items_as_typescript(
                        [subitem], indent_level + 2
                    )
                    lines.append(nested_lines)
                else:
                    # Simple link: clean the title and add it
                    title = subitem["text"].strip('"').replace("'", "\\'")
                    lines.append(
                        f"{indent}    {{ text: '{title}', link: '{subitem['link']}' }},"
                    )

            lines.append(f"{indent}  ]")
            lines.append(f"{indent}}},")
        else:
            title = item["text"].strip('"').replace("'", "\\'")
            lines.append(f"{indent}{{ text: '{title}', link: '{item['link']}' }},")

    return "\n".join(lines)


def update_vitepress_config(config_path, sidebars, nav_items, technical_docs_items):
    """
    Update VitePress config.mts file with generated sidebars and nav items
    Automatically replaces Technical Documentation sections in both nav and sidebar
    """
    print(f"\nUpdating VitePress config: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"  [ERROR] Config file not found: {config_path}")
        return False

    # Find and replace Technical Documentation sections
    i = 0
    sections_updated = 0

    while i < len(lines):
        line = lines[i]

        if "text: 'Technical Documentation'" in line:
            j = i + 1
            while j < len(lines) and "items: [" not in lines[j]:
                j += 1

            if j >= len(lines):
                i += 1
                continue

            items_line_indent = len(lines[j]) - len(lines[j].lstrip())

            k = j + 1
            bracket_count = 1
            while k < len(lines) and bracket_count > 0:
                bracket_count += lines[k].count("[") - lines[k].count("]")
                if bracket_count == 0:
                    break
                k += 1

            if k >= len(lines):
                i += 1
                continue

            # k now points to the line with the closing ]
            # Determine which section this is (nav or sidebar) by checking if we're before or after 'sidebar:'
            is_nav_section = True
            for check_line in lines[:i]:
                if "sidebar:" in check_line:
                    is_nav_section = False
                    break

            # Generate the replacement content
            if is_nav_section:
                replacement_items = format_items_as_typescript(
                    nav_items, indent_level=7
                )
            else:
                replacement_items = format_items_as_typescript(
                    technical_docs_items, indent_level=6
                )

            new_lines = lines[: j + 1] + [replacement_items + "\n"] + lines[k:]
            lines = new_lines

            sections_updated += 1
            print(
                f"  [Success] Updated Technical Documentation ({'nav' if is_nav_section else 'sidebar'} section)"
            )

            i = j + 2
        else:
            i += 1

    if sections_updated == 0:
        print("  [Warning] Could not find any Technical Documentation sections")
        return False

    # Update project-specific sidebars (e.g., '/projects/gardenlinux/')
    print("\n  Updating project-specific sidebars...")
    for sidebar in sidebars:
        if not sidebar:
            continue

        project_path = sidebar["path"]
        project_items = sidebar["items"]

        i = 0
        while i < len(lines):
            if f"'{project_path}': [" in lines[i] or f'"{project_path}": [' in lines[i]:
                j = i
                while j < len(lines) and "[" not in lines[j]:
                    j += 1

                if j >= len(lines):
                    i += 1
                    continue

                k = j + 1
                bracket_count = 1
                while k < len(lines) and bracket_count > 0:
                    bracket_count += lines[k].count("[") - lines[k].count("]")
                    if bracket_count == 0:
                        break
                    k += 1

                if k >= len(lines):
                    i += 1
                    continue

                replacement_items = format_items_as_typescript(
                    project_items, indent_level=4
                )

                new_lines = lines[: j + 1] + [replacement_items + "\n"] + lines[k:]
                lines = new_lines

                sections_updated += 1
                print(f"  [Success] Updated {project_path} sidebar")

                i = j + 2
                break
            else:
                i += 1

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"  [Success] Successfully updated {config_path}")
    except Exception as e:
        print(f"  [ERROR] Error writing config file: {e}")
        return False

    output_file = config_path.replace(".mts", ".generated.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "sidebars": sidebars,
                "nav_items": nav_items,
                "technical_docs_sidebar_items": technical_docs_items,
            },
            f,
            indent=2,
        )

    print(f"\n  Generated config also saved to: {output_file}")
    print(f"\n  Summary:")
    print(f"    - Project sidebars: {len([s for s in sidebars if s])}")
    print(f"    - Nav items: {len(nav_items)}")
    print(f"    - Technical docs sidebar items: {len(technical_docs_items)}")
    print(f"    - Sections updated: {sections_updated}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Update VitePress configuration")
    parser.add_argument("--config", required=True, help="Path to repos-config.json")
    parser.add_argument("--docs-dir", required=True, help="Path to docs directory")
    parser.add_argument(
        "--vitepress-config", required=True, help="Path to VitePress config.mts"
    )

    args = parser.parse_args()

    print("Generating VitePress configuration...")

    config = load_config(args.config)
    section_priorities = config.get("section_priorities", {})

    print("\nChecking for directories without index files...")
    created_files = create_missing_index_files(args.docs_dir, config["repos"])
    if created_files:
        print(f"  Created {len(created_files)} index file(s)")
    else:
        print("  All directories have index files")

    sidebars = []
    for repo in config["repos"]:
        sidebar = generate_sidebar_config(repo, args.docs_dir, section_priorities)
        if sidebar:
            sidebars.append(sidebar)

    nav_items = generate_nav_items(config["repos"], sidebars)

    technical_docs_items = generate_technical_docs_sidebar_items(
        config["repos"], sidebars
    )

    update_vitepress_config(
        args.vitepress_config, sidebars, nav_items, technical_docs_items
    )

    print("\n[Completed] Configuration update complete!")


if __name__ == "__main__":
    main()
