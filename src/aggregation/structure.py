"""Directory structure transformation and markdown processing."""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .transformer import (
    rewrite_links,
    fix_broken_project_links,
    ensure_frontmatter,
    parse_frontmatter,
)


def transform_directory_structure(
    source_dir: str,
    target_dir: str,
    structure_map,
    special_files: Optional[Dict] = None,
    media_dirs: Optional[List[str]] = None,
) -> None:
    """
    Transform directory structure based on mapping.
    
    Args:
        source_dir: Source directory with fetched docs
        target_dir: Target directory in docs/projects/
        structure_map: Directory structure mapping or copy mode
        special_files: Map of files to move to specific locations
        media_dirs: List of media directories to preserve
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    special_files = special_files or {}
    media_dirs = media_dirs or []
    
    if isinstance(structure_map, dict):
        # Structured transformation with subdirectories specified
        for old_name, new_name in structure_map.items():
            old_path = source_path / old_name
            new_path = target_path / new_name
            
            if old_path.exists():
                print(f"  Transforming: {old_name} -> {new_name}")
                shutil.copytree(old_path, new_path, dirs_exist_ok=True)
        
        # Handle special files
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
    
    else:
        # Flat/sphinx structure - copy all files as-is (merged logic)
        print(f"  Copying {structure_map} structure")
        for item in source_path.glob("*"):
            target_item = target_path / item.name
            if item.is_file():
                shutil.copy2(item, target_item)
            elif item.is_dir():
                shutil.copytree(item, target_item, dirs_exist_ok=True)


def copy_targeted_docs(source_dir: str, docs_dir: str, repo_name: str, media_dirs: Optional[List[str]] = None, root_files: Optional[List[str]] = None) -> None:
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
            print(f"      Exists: {root_file_path.exists()}, Is file: {root_file_path.is_file() if root_file_path.exists() else 'N/A'}, Ends with .md: {root_file.endswith('.md')}")
            
            if root_file_path.exists() and root_file_path.is_file() and root_file.endswith('.md'):
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
                target_path = frontmatter.get("github_target_path") or frontmatter.get("target")
                
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
            
            for media_dir_name in media_dirs:
                # Recursively find all instances of this media directory in the source
                for media_dir in source_path.rglob(media_dir_name):
                    if media_dir.is_dir():
                        # Calculate relative path from source_path
                        rel_path = media_dir.relative_to(source_path)
                        
                        # Determine if this is a root-level or nested media directory
                        if len(rel_path.parts) == 1:
                            # Root-level media directory: copy to common ancestor of targeted files
                            if common_parent and common_parent != Path('.'):
                                target_media = docs_path / common_parent / media_dir_name
                                target_media.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copytree(media_dir, target_media, dirs_exist_ok=True)
                                print(f"    ✓ Copied media: {common_parent / media_dir_name}")
                        else:
                            # Nested media directory: copy to same relative path
                            target_media = docs_path / rel_path
                            target_media.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copytree(media_dir, target_media, dirs_exist_ok=True)
                            print(f"    ✓ Copied media: {rel_path}")
    else:
        print("  No files with 'github_target_path:' frontmatter found")


def process_markdown_file(
    file_path: Path,
    repo_name: str,
    target_dir: str,
    base_path: str = "/projects",
) -> bool:
    """
    Process a single markdown file: rewrite links, fix frontmatter.
    
    Args:
        file_path: Path to markdown file
        repo_name: Repository name
        target_dir: Target directory path
        base_path: Base path for projects
    
    Returns:
        Success status
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
        
        content = rewrite_links(content, repo_name, file_rel_path, base_path)
        content = fix_broken_project_links(content, repo_name, target_dir, base_path)
        content = ensure_frontmatter(content)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"  [Warning] Error processing {file_path}: {e}")
        return False


def process_all_markdown(target_dir: str, repo_name: str) -> None:
    """
    Process all markdown files in target directory.
    
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
        if process_markdown_file(md_file, repo_name, target_dir):
            success_count += 1
    
    print(f"  ✓ Processed {success_count}/{len(md_files)} files successfully")
