"""Unit tests for aggregation.transformer module."""

import pytest
from aggregation import (
    rewrite_links,
    quote_yaml_value,
    ensure_frontmatter,
)


class TestRewriteLinks:
    """Tests for rewrite_links function."""
    
    def test_relative_links(self):
        """Test that relative links are rewritten correctly."""
        content = "[Link](./other.md)"
        result = rewrite_links(content, "gardenlinux", "introduction/index.md")
        assert "/projects/gardenlinux/introduction/other" in result
    
    def test_numbered_directory_links(self):
        """Test that numbered directories in links are transformed."""
        content = "[Link](../01_developers/guide.md)"
        result = rewrite_links(content, "gardenlinux", "introduction/index.md")
        assert "developers/guide" in result
    
    def test_preserve_external_links(self):
        """Test that external links are not modified."""
        content = "[External](https://github.com/gardenlinux/gardenlinux)"
        result = rewrite_links(content, "gardenlinux", "")
        assert result == content
    
    def test_preserve_anchor_links(self):
        """Test that anchor links are preserved."""
        content = "[Anchor](#section)"
        result = rewrite_links(content, "gardenlinux", "")
        assert result == content
    
    def test_media_links(self):
        """Test that .media/ links are rewritten correctly."""
        content = "[Image](../.media/image.png)"
        result = rewrite_links(content, "gardenlinux", "introduction/index.md")
        assert "/projects/gardenlinux/.media/image.png" in result
    
    def test_absolute_paths_to_github(self):
        """Test that absolute paths outside docs/ link to GitHub."""
        content = "[File](/README.md)"
        result = rewrite_links(content, "gardenlinux", "")
        assert "https://github.com/gardenlinux/gardenlinux/blob/main/README.md" in result


class TestQuoteYamlValue:
    """Tests for quote_yaml_value function."""
    
    def test_quote_value_with_colon(self):
        """Test that YAML values with colons are quoted."""
        value = "Getting Started: Creating Images"
        result = quote_yaml_value(value)
        assert '"' in result
        assert "Getting Started: Creating Images" in result
    
    def test_simple_value_not_quoted(self):
        """Test that simple YAML values are not quoted."""
        value = "Simple Title"
        result = quote_yaml_value(value)
        assert result == "Simple Title"
    
    def test_already_quoted_value(self):
        """Test that already-quoted values are not double-quoted."""
        value = '"Already Quoted"'
        result = quote_yaml_value(value)
        assert result == '"Already Quoted"'
    
    def test_value_with_hash(self):
        """Test that values with # are quoted."""
        value = "Title #1"
        result = quote_yaml_value(value)
        assert '"' in result
    
    def test_value_with_special_chars(self):
        """Test various special characters that require quoting."""
        special_chars = [":", "#", "@", "*", "&", "!"]
        for char in special_chars:
            value = f"Text {char} more"
            result = quote_yaml_value(value)
            assert '"' in result or "'" in result


class TestEnsureFrontmatter:
    """Tests for ensure_frontmatter function."""
    
    def test_no_change_when_missing(self):
        """Test that content without frontmatter is returned unchanged."""
        content = "# Test Title\n\nContent here."
        result = ensure_frontmatter(content)
        assert result == content
    
    def test_preserve_existing(self):
        """Test that existing frontmatter is preserved."""
        content = "---\ntitle: Existing\n---\n\nContent"
        result = ensure_frontmatter(content)
        assert "title: Existing" in result
    
    def test_fix_colons(self):
        """Test that colons in existing frontmatter are quoted."""
        content = "---\ntitle: Test: Example\n---\n\nContent"
        result = ensure_frontmatter(content)
        assert '"Test: Example"' in result
    
    def test_fix_multiple_fields(self):
        """Test that multiple frontmatter fields are fixed."""
        content = "---\ntitle: Test: Example\nauthor: John Doe\ntags: tag1, tag2\n---\n\nContent"
        result = ensure_frontmatter(content)
        assert '"Test: Example"' in result
        assert "John Doe" in result
        assert '"tag1, tag2"' in result