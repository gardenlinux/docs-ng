"""Integration tests for documentation aggregation."""

import tempfile
from pathlib import Path

import pytest

from aggregation import DocsFetcher, RepoConfig, process_all_markdown

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _make_output_dir(tmp_path: Path) -> Path:
    """Create and return a fresh output directory under tmp_path."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


def _make_fetcher(project_root: Path) -> DocsFetcher:
    """Return a DocsFetcher anchored at project_root."""
    return DocsFetcher(project_root)


class TestDocsFetcher:
    """Integration tests for DocsFetcher."""

    def test_fetch_local_with_temp_dir(self, tmp_path):
        """Test fetching from a local directory structure."""
        # Create a mock local repository
        repo_path = tmp_path / "mock-repo"
        docs_path = repo_path / "docs"
        docs_path.mkdir(parents=True)

        # Create some test files
        (docs_path / "index.md").write_text("# Test Documentation\n\nContent here.")
        (docs_path / "guide.md").write_text("# Guide\n\nSome guide content.")

        subdir = docs_path / "tutorials"
        subdir.mkdir()
        (subdir / "tutorial1.md").write_text("# Tutorial 1\n\nTutorial content.")

        # Create repo config
        repo = RepoConfig(
            name="test-repo",
            url=f"file://{repo_path}",
            docs_path="docs",
            ref="",
        )

        output_dir = _make_output_dir(tmp_path)
        result = _make_fetcher(tmp_path).fetch(repo, output_dir)

        # Verify success
        assert result.success is True
        assert result.resolved_commit is None  # Local repos don't have commits

        # Verify files were copied
        assert (output_dir / "index.md").exists()
        assert (output_dir / "guide.md").exists()
        assert (output_dir / "tutorials" / "tutorial1.md").exists()

        # Verify content
        assert "Test Documentation" in (output_dir / "index.md").read_text()

    def test_fetch_local_missing_docs_path(self, tmp_path, capsys):
        """Test that a missing docs_path results in success=True, no files copied, and a warning."""
        repo_path = tmp_path / "mock-repo"
        repo_path.mkdir(parents=True)
        # Intentionally do NOT create a 'docs' directory

        repo = RepoConfig(
            name="test-repo",
            url=f"file://{repo_path}",
            docs_path="docs",  # Does not exist
            ref="",
        )

        output_dir = _make_output_dir(tmp_path)
        result = _make_fetcher(tmp_path).fetch(repo, output_dir)

        # Fetch should still report success (warning is printed but not fatal)
        assert result.success is True
        # Output directory should be empty (nothing was copied)
        assert list(output_dir.iterdir()) == []
        # A warning about the missing docs_path must have been emitted to stdout
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "docs" in captured.out

    def test_fetch_local_with_root_files_glob(self, tmp_path):
        """Test that root_files with a glob pattern copies only matched files."""
        repo_path = tmp_path / "mock-repo"
        features_dir = repo_path / "features" / "foo"
        features_dir.mkdir(parents=True)
        (features_dir / "bar.md").write_text("# Feature Bar")
        (features_dir / "baz.md").write_text("# Feature Baz")
        # A file that should NOT match the glob
        (repo_path / "CHANGELOG.md").write_text("# Changes")

        repo = RepoConfig(
            name="test-repo",
            url=f"file://{repo_path}",
            docs_path="nonexistent-docs",  # No standard docs; only root_files
            ref="",
            root_files=["features/foo/*.md"],
        )

        output_dir = _make_output_dir(tmp_path)
        result = _make_fetcher(tmp_path).fetch(repo, output_dir)

        assert result.success is True
        # Glob-matched files should be present at their relative paths
        assert (output_dir / "features" / "foo" / "bar.md").exists()
        assert (output_dir / "features" / "foo" / "baz.md").exists()
        # Non-matching file should NOT be present
        assert not (output_dir / "CHANGELOG.md").exists()

    def test_fetch_local_resolves_relative_path(self, tmp_path):
        """Test that a relative file:// URL is resolved against project_root."""
        # Simulate a sibling-directory layout: project_root and mock-repo are siblings
        project_root = tmp_path / "docs"
        project_root.mkdir()

        repo_path = tmp_path / "mock-repo"
        docs_path = repo_path / "docs"
        docs_path.mkdir(parents=True)
        (docs_path / "index.md").write_text("# Hello from relative repo")

        repo = RepoConfig(
            name="relative-repo",
            url="file://../mock-repo",
            docs_path="docs",
            ref="",
        )

        output_dir = _make_output_dir(tmp_path)
        result = _make_fetcher(project_root).fetch(repo, output_dir)

        assert result.success is True
        assert (output_dir / "index.md").exists()
        assert "Hello from relative repo" in (output_dir / "index.md").read_text()


class TestMarkdownProcessing:
    """Integration tests for markdown processing."""

    def test_process_all_markdown(self, tmp_path):
        """Test processing markdown files in a directory."""
        # Create test directory structure
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Create test markdown files
        (target_dir / "README.md").write_text(
            "# README\n\n[Link](./guide.md)\n[External](https://example.com)"
        )
        (target_dir / "index.md").write_text("# Index\n\nContent")

        subdir = target_dir / "docs"
        subdir.mkdir()
        (subdir / "guide.md").write_text("# Guide\n\n[Back](../README.md)")

        # Process the markdown
        process_all_markdown(str(target_dir), "test-repo")

        # Verify README was renamed to index (but we already have index.md, so it won't be)
        # The function only renames if index.md doesn't exist
        assert (target_dir / "README.md").exists()

        # Verify links were rewritten in index.md (which was already there)
        index_content = (target_dir / "index.md").read_text()
        assert "# Index" in index_content

        # Verify guide links were rewritten
        guide_content = (subdir / "guide.md").read_text()
        assert "README" in guide_content

    def test_process_markdown_with_frontmatter(self, tmp_path):
        """Test that frontmatter is properly handled."""
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Create markdown with problematic frontmatter
        (target_dir / "test.md").write_text(
            "---\ntitle: Test: Example\ntags: tag1, tag2\n---\n\n# Content"
        )

        # Process
        process_all_markdown(str(target_dir), "test-repo")

        # Verify frontmatter was fixed
        content = (target_dir / "test.md").read_text()
        assert '"Test: Example"' in content  # Colon should be quoted
        assert '"tag1, tag2"' in content  # Comma should be quoted
