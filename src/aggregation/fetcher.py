"""Repository fetching for documentation aggregation."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Tuple, Optional

from .models import RepoConfig, AggregateResult


class DocsFetcher:
    """Handles fetching documentation from remote or local repositories."""
    
    def __init__(self, project_root: Path, update_locks: bool = False):
        """
        Initialize fetcher.
        
        Args:
            project_root: Root directory of docs-ng project
            update_locks: Whether we're in update-locks mode (allows commit mismatches)
        """
        self.project_root = project_root
        self.update_locks = update_locks
    
    def fetch(self, repo: RepoConfig, output_dir: Path) -> AggregateResult:
        """
        Fetch documentation for a repository.
        
        Args:
            repo: Repository configuration
            output_dir: Where to copy fetched files
        
        Returns:
            AggregateResult with success status and resolved commit
        """
        if repo.is_local:
            success = self._fetch_local(repo, output_dir)
            return AggregateResult(repo.name, success, None)
        else:
            success, commit = self._fetch_remote(repo, output_dir)
            return AggregateResult(repo.name, success, commit)
    
    def _fetch_remote(
        self,
        repo: RepoConfig,
        output_dir: Path,
    ) -> Tuple[bool, Optional[str]]:
        """Fetch from remote repository using git sparse checkout."""
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            print(f"  Fetching from: {repo.url}")
            print(f"  Ref: {repo.ref}")
            if repo.root_files:
                print(f"  Root files: {', '.join(repo.root_files)}")
            print(f"  Output: {output_dir}")
            
            # Initialize sparse checkout
            subprocess.run(["git", "init"], check=True, capture_output=True, cwd=temp_dir)
            subprocess.run(
                ["git", "remote", "add", "origin", repo.url],
                check=True,
                capture_output=True,
                cwd=temp_dir,
            )
            subprocess.run(
                ["git", "config", "core.sparseCheckout", "true"],
                check=True,
                capture_output=True,
                cwd=temp_dir,
            )
            
            # Configure sparse checkout patterns
            sparse_checkout_file = temp_dir / ".git" / "info" / "sparse-checkout"
            with open(sparse_checkout_file, "w") as f:
                f.write(f"{repo.docs_path}/*\n")
                for root_file in repo.root_files:
                    f.write(f"{root_file}\n")
            
            # Fetch and checkout
            print("  Cloning (sparse checkout)...")
            subprocess.run(
                ["git", "fetch", "--depth=1", "origin", repo.ref],
                check=True,
                capture_output=True,
                cwd=temp_dir,
            )
            subprocess.run(
                ["git", "checkout", repo.ref],
                check=True,
                capture_output=True,
                cwd=temp_dir,
            )
            
            # Get resolved commit hash
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
                cwd=temp_dir,
            )
            resolved_commit = result.stdout.strip()
            print(f"  Resolved commit: {resolved_commit}")
            
            # Verify commit lock if specified
            if repo.commit:
                if resolved_commit != repo.commit:
                    if self.update_locks:
                        # In update-locks mode, commit mismatch is expected
                        print(f"  Updating lock: {repo.commit[:8]} → {resolved_commit[:8]}")
                    else:
                        # In normal mode, commit mismatch is an error
                        print(f"  Warning: Commit mismatch!", file=sys.stderr)
                        print(f"    Expected: {repo.commit}", file=sys.stderr)
                        print(f"    Got: {resolved_commit}", file=sys.stderr)
                        return False, resolved_commit
                else:
                    print(f"  ✓ Commit lock verified")
            
            # Copy docs to output directory
            docs_source = temp_dir / repo.docs_path
            if docs_source.exists():
                print(f"  Copying docs to {output_dir}")
                self._copy_docs(docs_source, output_dir)
            else:
                print(f"  Warning: docs_path '{repo.docs_path}' not found in repository")
            
            # Copy root files if specified
            self._copy_root_files(temp_dir, repo.root_files, output_dir)
            
            print("  ✓ Fetch complete")
            return True, resolved_commit
            
        except subprocess.CalledProcessError as e:
            print(f"  Error: Git command failed: {e}", file=sys.stderr)
            if e.stderr:
                print(f"  {e.stderr.decode()}", file=sys.stderr)
            return False, None
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)
            return False, None
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _fetch_local(
        self,
        repo: RepoConfig,
        output_dir: Path,
    ) -> bool:
        """Fetch from local repository via direct filesystem copy."""
        try:
            # Resolve repo path (handle relative paths)
            repo_path = Path(repo.local_path)
            if not repo_path.is_absolute():
                repo_abs_path = (self.project_root / repo_path).resolve()
            else:
                repo_abs_path = repo_path.resolve()
            
            print(f"  Copying from: {repo_abs_path}")
            if repo.root_files:
                print(f"  Root files: {', '.join(repo.root_files)}")
            print(f"  Output: {output_dir}")
            
            if not repo_abs_path.exists():
                print(f"  Error: Local repository not found: {repo_abs_path}", file=sys.stderr)
                return False
            
            # Copy docs directory
            docs_source = repo_abs_path / repo.docs_path
            if docs_source.exists():
                print(f"  Copying docs from {repo.docs_path}/")
                self._copy_docs(docs_source, output_dir)
            else:
                print(f"  Warning: docs_path '{repo.docs_path}' not found in local repository")
            
            # Copy root files if specified
            self._copy_root_files(repo_abs_path, repo.root_files, output_dir)
            
            print("  ✓ Copy complete")
            return True
            
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)
            return False
    
    @staticmethod
    def _copy_docs(source: Path, dest: Path) -> None:
        """
        Copy documentation directory contents.
        
        Args:
            source: Source docs directory
            dest: Destination directory
        """
        dest.mkdir(parents=True, exist_ok=True)
        
        # Copy all regular files and directories
        for item in source.iterdir():
            target = dest / item.name
            if item.is_file():
                shutil.copy2(item, target)
            elif item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
        
        # Also copy hidden directories (like .media)
        for item in source.glob(".*"):
            if item.is_dir() and item.name not in [".", ".."]:
                target = dest / item.name
                shutil.copytree(item, target, dirs_exist_ok=True)
    
    @staticmethod
    def _copy_root_files(repo_root: Path, root_files: list, dest: Path) -> None:
        """
        Copy specified root-level files and directories from repository.
        
        Args:
            repo_root: Root directory of the repository
            root_files: List of filenames/directories to copy
            dest: Destination directory
        """
        if not root_files:
            return
        
        print("  Copying root files")
        for filename in root_files:
            # Strip trailing slash for path resolution
            clean_name = filename.rstrip("/")
            src = repo_root / clean_name
            if src.exists():
                target = dest / src.name
                if src.is_dir():
                    try:
                        shutil.copytree(src, target, dirs_exist_ok=True, symlinks=False)
                        print(f"    ✓ {filename} (directory)")
                    except Exception as e:
                        print(f"    Warning: Failed to copy {filename}: {e}")
                else:
                    shutil.copy2(src, target)
                    print(f"    ✓ {filename}")
            else:
                print(f"    Warning: {filename} not found")
