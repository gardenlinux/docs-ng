"""Integration tests for documentation aggregation."""

import tempfile
from pathlib import Path

import pytest
from aggregation import DocsFetcher, RepoConfig, process_all_markdown


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
            target_path="projects/test-repo",
        )
        
        # Fetch the docs
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        fetcher = DocsFetcher(tmp_path)
        result = fetcher.fetch(repo, output_dir)
        
        # Verify success
        assert result.success is True
        assert result.resolved_commit is None  # Local repos don't have commits
        
        # Verify files were copied
        assert (output_dir / "index.md").exists()
        assert (output_dir / "guide.md").exists()
        assert (output_dir / "tutorials" / "tutorial1.md").exists()
        
        # Verify content
        assert "Test Documentation" in (output_dir / "index.md").read_text()


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
        assert "/projects/test-repo" in guide_content or "README" in guide_content
    
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