#!/usr/bin/env python3
"""
Unified documentation aggregation script for docs-ng

This script orchestrates documentation aggregation from multiple repositories.
All heavy lifting is done by the aggregation package modules.
"""

import argparse
import sys
import tempfile
from pathlib import Path

from aggregation import (
    load_config,
    save_config,
    DocsFetcher,
    transform_directory_structure,
    copy_targeted_docs,
    process_all_markdown,
)
from aggregation.releases import generate_release_docs
from aggregation.release_notes import generate_release_notes_docs


def transform_repo_docs(
    repo,
    docs_dir: Path,
    temp_dir: Path,
) -> bool:
    """Transform documentation for a single repository."""
    repo_name = repo.name
    print(f"\n{'='*60}")
    print(f"Transforming docs for: {repo_name}")
    print(f"{'='*60}")
    
    source_dir = temp_dir / repo_name
    target_dir = docs_dir / repo.target_path
    
    # Step 1: Copy files with 'github_target_path:' frontmatter
    print(f"\nStep 1: Processing targeted files...")
    copy_targeted_docs(str(source_dir), str(docs_dir), repo_name, repo.media_directories, repo.root_files)
    
    # Step 2: Transform project structure
    print(f"\nStep 2: Transforming project structure...")
    transform_directory_structure(
        str(source_dir),
        str(target_dir),
        repo.structure,
        repo.special_files,
        repo.media_directories,
    )
    
    # Step 3: Process markdown files
    print(f"\nStep 3: Processing markdown files...")
    process_all_markdown(str(target_dir), repo_name)
    
    print(f"\n✓ Transformation complete for {repo_name}")
    return True


def aggregate_repo(
    repo,
    docs_dir: Path,
    temp_dir: Path,
    fetcher: DocsFetcher,
) -> tuple:
    """
    Aggregate documentation for a single repository.
    
    Returns:
        Tuple of (success, resolved_commit_hash)
    """
    print(f"\n{'='*60}")
    print(f"Aggregating: {repo.name}")
    print(f"{'='*60}")
    
    # Create output directory for this repo
    repo_output_dir = temp_dir / repo.name
    repo_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Fetch the repository
    result = fetcher.fetch(repo, repo_output_dir)
    
    if not result.success:
        print(f"✗ Failed to fetch {repo.name}")
        return False, result.resolved_commit
    
    # Transform the fetched docs
    transform_success = transform_repo_docs(repo, docs_dir, temp_dir)
    
    if not transform_success:
        print(f"✗ Failed to transform {repo.name}")
        return False, result.resolved_commit
    
    return True, result.resolved_commit


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Aggregate documentation from multiple repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Aggregate all repositories
  %(prog)s

  # Aggregate with local config (file:// URLs, no git)
  %(prog)s --config repos-config.local.json

  # Aggregate specific repository
  %(prog)s --repo gardenlinux

  # Update commit locks (fetch and update config with resolved commit hashes)
  %(prog)s --update-locks
        """,
    )
    
    parser.add_argument(
        "--config",
        default="repos-config.json",
        help="Path to repos-config.json (default: repos-config.json)",
    )
    parser.add_argument(
        "--docs-dir",
        default="docs",
        help="Path to docs directory (default: docs)",
    )
    parser.add_argument(
        "--repo",
        help="Only aggregate specific repository",
    )
    parser.add_argument(
        "--update-locks",
        action="store_true",
        help="Update commit locks: fetch and update config with resolved commit hashes",
    )
    
    args = parser.parse_args()
    
    # Determine script directory
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent
    
    # Resolve paths
    # Config files are in project root, not in src/
    if not Path(args.config).is_absolute():
        config_path = project_root / args.config
    else:
        config_path = Path(args.config)
    
    if not Path(args.docs_dir).is_absolute():
        docs_dir = project_root / args.docs_dir
    else:
        docs_dir = Path(args.docs_dir)
    
    # Load configuration
    print(f"{'='*60}")
    print("Garden Linux Documentation Aggregation")
    print(f"{'='*60}\n")
    print(f"Configuration: {config_path}")
    print(f"Docs directory: {docs_dir}")
    if args.repo:
        print(f"Repository filter: {args.repo}")
    if args.update_locks:
        print("Update commit locks: ENABLED")
    print()
    
    repos = load_config(str(config_path))
    
    # Create temporary directory for fetched docs
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        print(f"Temporary directory: {temp_dir}\n")
        
        # Initialize fetcher
        fetcher = DocsFetcher(project_root, update_locks=args.update_locks)
        
        # Track resolved commits for locking
        resolved_commits = {}
        success_count = 0
        fail_count = 0
        
        # Aggregate each repository
        for repo in repos:
            # Filter by repo if specified
            if args.repo and repo.name != args.repo:
                continue
            
            success, resolved_commit = aggregate_repo(
                repo,
                docs_dir,
                temp_dir,
                fetcher,
            )
            
            if success:
                success_count += 1
                if resolved_commit:
                    resolved_commits[repo.name] = resolved_commit
            else:
                fail_count += 1
        
        # Update config with resolved commits if locking
        if args.update_locks and resolved_commits:
            print(f"\n{'='*60}")
            print("Updating config with resolved commits...")
            print(f"{'='*60}\n")
            
            for repo in repos:
                if repo.name in resolved_commits:
                    repo.commit = resolved_commits[repo.name]
                    print(f"  {repo.name}: {resolved_commits[repo.name]}")
            
            save_config(str(config_path), repos)
            print(f"\n✓ Config updated: {config_path}")
    
    # Generate release documentation from GLRD
    print(f"\n{'='*60}")
    print("Generating release documentation...")
    print(f"{'='*60}\n")
    generate_release_docs(docs_dir)
    
    # Generate release notes from GitHub
    print(f"\n{'='*60}")
    print("Fetching release notes from GitHub...")
    print(f"{'='*60}\n")
    generate_release_notes_docs(docs_dir)
    
    # Summary
    print(f"\n{'='*60}")
    print("Documentation aggregation complete!")
    print(f"{'='*60}\n")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    
    print("\nNext steps:")
    print("  1. Review the changes in docs/projects/")
    print("  2. Run 'make dev' or 'pnpm run docs:dev' to preview")
    print("  3. Commit the changes if satisfied")
    
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())