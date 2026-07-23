"""Directory structure transformation and markdown processing."""

import shutil
from pathlib import Path
from typing import List

from .transformer import ensure_frontmatter, parse_frontmatter, rewrite_links


def copy_targeted_docs(
    source_dir: str,
    docs_dir: str,
    repo_name: str,
    media_dirs: List[str] | None = None,
    root_files: List[str] | None = None,
) -> None:
    """
    Copy markdown files with 'github_target_path:' frontmatter to their specified locations.
    Also copies media directories to the common target path of targeted files.

    Args:
        source_dir: Source directory with fetched docs
        docs_dir: Docs root directory
        repo_name: Repository name
        media_dirs: List of media directories to copy alongside targeted files
        root_files: List of root-level files to scan for github_target_path (e.g., README.md)
    """
    source_path = Path(source_dir)
    docs_path = Path(docs_dir)

    if not source_path.exists():
        print(f"  [Warning] Source directory not found: {source_dir}")
        return

    # Find all markdown files (recursively in source_dir)
    md_files = list(source_path.rglob("*.md"))

    # Also check root_files if provided
    # Note: root_files may have been flattened by the fetcher (e.g., src/README.md -> README.md)
    # So we need to check both the original path and just the basename
    if root_files:
        print(f"  Checking {len(root_files)} root_files for github_target_path...")
        for root_file in root_files:
            # Try the full path first
            root_file_path = source_path / root_file

            # If that doesn't exist, try just the basename (in case fetcher flattened it)
            if not root_file_path.exists():
                root_file_path = source_path / Path(root_file).name

            print(f"    Checking: {root_file} -> {root_file_path}")
            print(
                f"      Exists: {root_file_path.exists()}, Is file: {root_file_path.is_file() if root_file_path.exists() else 'N/A'}, Ends with .md: {root_file.endswith('.md')}"
            )

            if (
                root_file_path.exists()
                and root_file_path.is_file()
                and root_file.endswith(".md")
            ):
                # Add to list if not already there
                if root_file_path not in md_files:
                    md_files.append(root_file_path)
                    print(f"      ✓ Added to scan list")
                else:
                    print(f"      Already in list")
            else:
                print(f"      ✗ Skipped")

    targeted_files = []

    print(f"  Scanning {len(md_files)} files for 'github_target_path:' frontmatter...")

    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            frontmatter, _ = parse_frontmatter(content)

            # Check for 'github_target_path' in frontmatter
            if frontmatter and ("github_target_path" in frontmatter):
                target_path = frontmatter.get("github_target_path") or frontmatter.get(
                    "target"
                )

                if target_path is None:
                    continue

                # Strip leading 'docs/' if present
                if target_path.startswith("docs/"):
                    target_path = target_path[5:]

                target_file = docs_path / target_path

                # Create parent directories if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)

                # Copy the file
                shutil.copy2(md_file, target_file)

                # Apply markdown processing
                content = ensure_frontmatter(content)

                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(content)

                targeted_files.append((md_file.relative_to(source_path), target_path))
                print(f"    ✓ Copied: {md_file.name} → {target_path}")

        except Exception as e:
            print(f"  [Warning] Error processing {md_file.name}: {e}")

    if targeted_files:
        print(f"  ✓ Copied {len(targeted_files)} targeted file(s)")

        # Copy media directories to maintain relative paths with targeted files
        if media_dirs:
            print(f"  Copying media directories recursively...")

            # Compute common ancestor of all targeted files for root-level media
            target_paths = [Path(target_path) for _, target_path in targeted_files]
            common_parent = None
            if target_paths:
                # Get all parent directories and find the most common one
                all_parents = [list(p.parents) for p in target_paths]
                if all_parents:
                    # Find the deepest common ancestor
                    for p in target_paths[0].parents:
                        if all(p in parents for parents in all_parents):
                            common_parent = p
                            break

            # Build mapping from source parent dir to set of target parent dirs.
            # Used to colocate nested media dirs with retargeted markdown files.
            source_to_target_parents: dict[Path, set[Path]] = {}
            for src_rel, target_rel in targeted_files:
                src_parent = Path(src_rel).parent  # e.g. Path("overview")
                target_parent = Path(
                    target_rel
                ).parent  # e.g. Path("reference/supporting_tools")
                source_to_target_parents.setdefault(src_parent, set()).add(
                    target_parent
                )

            for media_dir_name in media_dirs:
                # Recursively find all instances of this media directory in the source
                for media_dir in source_path.rglob(media_dir_name):
                    if media_dir.is_dir():
                        # Calculate relative path from source_path
                        rel_path = media_dir.relative_to(source_path)

                        # Determine if this is a root-level or nested media directory
                        if len(rel_path.parts) == 1:
                            # Root-level media directory: copy to common ancestor of targeted files
                            if common_parent and common_parent != Path("."):
                                target_media = (
                                    docs_path / common_parent / media_dir_name
                                )
                                target_media.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copytree(
                                    media_dir, target_media, dirs_exist_ok=True
                                )
                                print(
                                    f"    ✓ Copied media: {common_parent / media_dir_name}"
                                )
                        else:
                            # Nested media directory: look up source parent in mapping
                            # to colocate media with the retargeted markdown file(s).
                            media_source_parent = (
                                rel_path.parent
                            )  # e.g. Path("overview")
                            if media_source_parent in source_to_target_parents:
                                for target_parent in source_to_target_parents[
                                    media_source_parent
                                ]:
                                    target_media = (
                                        docs_path / target_parent / media_dir_name
                                    )
                                    target_media.parent.mkdir(
                                        parents=True, exist_ok=True
                                    )
                                    shutil.copytree(
                                        media_dir, target_media, dirs_exist_ok=True
                                    )
                                    print(
                                        f"    ✓ Copied media: {target_parent / media_dir_name}"
                                    )
                            else:
                                # No mapping found: fall back to source-relative placement
                                target_media = docs_path / rel_path
                                target_media.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copytree(
                                    media_dir, target_media, dirs_exist_ok=True
                                )
                                print(f"    ✓ Copied media: {rel_path}")
    else:
        print("  No files with 'github_target_path:' frontmatter found")


def verify_internal_links(
    source_dir: str,
    docs_dir: str,
    repo_name: str,
) -> int:
    """
    Verify that all internal relative links in shipped markdown files resolve to
    files that were also shipped (have github_target_path).

    Exits with a non-zero count of errors when any shipped file links to a
    source-repo file that was not itself shipped.

    Args:
        source_dir: Source directory with fetched docs (temp dir)
        docs_dir: Docs root directory (where targeted files were placed)
        repo_name: Repository name

    Returns:
        Number of broken links found (0 = success)
    """
    import re

    source_path = Path(source_dir)
    docs_path = Path(docs_dir)

    # Build set of shipped source paths (files with github_target_path)
    shipped_source_paths = set()
    md_files = list(source_path.rglob("*.md"))

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, _ = parse_frontmatter(content)
            if frontmatter and "github_target_path" in frontmatter:
                shipped_source_paths.add(md_file.resolve())
        except Exception:
            pass

    if not shipped_source_paths:
        return 0

    errors = 0

    # For each shipped file, check its internal links
    for md_file in md_files:
        if md_file.resolve() not in shipped_source_paths:
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # Find all markdown links
        for match in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", content):
            link = match.group(2)

            # Skip external links, anchors, special protocols
            if (
                link.startswith("http://")
                or link.startswith("https://")
                or link.startswith("#")
                or link.startswith("mailto:")
                or (
                    ":" in link
                    and not link.startswith("/")
                    and not link.startswith("./")
                    and not link.startswith("../")
                )
            ):
                continue

            # Skip absolute links starting with / (these are VitePress absolute paths
            # or GitHub-redirected links — not source-repo relative links)
            if link.startswith("/"):
                continue

            # Resolve relative link from the file's directory
            file_dir = md_file.parent
            link_path_str = link.split("#")[0]  # Strip fragment
            if not link_path_str:
                continue

            # Resolve the link target
            resolved = (file_dir / link_path_str).resolve()

            # If it's a .md file, check if it's in the shipped set
            if resolved.suffix == ".md":
                if resolved.is_relative_to(source_path.resolve()):
                    if resolved not in shipped_source_paths and resolved.exists():
                        rel_file = md_file.relative_to(source_path)
                        print(
                            f"  [ERROR] Unshipped link in {repo_name}/{rel_file}: "
                            f"'{link}' → {resolved.relative_to(source_path.resolve())} "
                            f"(file exists but has no github_target_path)"
                        )
                        errors += 1

    return errors


def process_all_markdown(target_dir: str, repo_name: str) -> None:
    """
    Process all markdown files in target directory.
    Renames README.md to index.md for VitePress compatibility.

    Args:
        target_dir: Target directory path
        repo_name: Repository name
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
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            content = ensure_frontmatter(content)

            with open(md_file, "w", encoding="utf-8") as f:
                f.write(content)

            success_count += 1
        except Exception as e:
            print(f"  [Warning] Error processing {md_file}: {e}")

    print(f"  ✓ Processed {success_count}/{len(md_files)} files successfully")
