"""Unit tests for aggregation.transformer module."""

import pytest
from pathlib import Path
from aggregation import (
    ensure_frontmatter,
    parse_frontmatter,
    quote_yaml_value,
    rewrite_links,
)
from aggregation.transformer import fix_broken_project_links


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
    
    def test_relative_link_with_anchor(self):
        """Test that relative links with anchors preserve the anchor."""
        content = "[Guide](./guide.md#section-one)"
        result = rewrite_links(content, "gardenlinux", "docs/index.md")
        assert "section-one" in result
        assert "/projects/gardenlinux" in result

    def test_dotdot_outside_docs_falls_back_to_github(self):
        """Test that ../ links going outside docs/ fall back to GitHub."""
        # File is at the root (depth 1); two levels up would escape docs/
        content = "[File](../../README.md)"
        result = rewrite_links(content, "gardenlinux", "subdir/index.md")
        assert "github.com/gardenlinux/gardenlinux/blob/main" in result


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


class TestParseFrontmatter:
    """Tests for parse_frontmatter function."""

    def test_no_frontmatter_returns_none_and_original(self):
        """Content without frontmatter returns (None, original_content)."""
        content = "# Title\n\nSome body text."
        fm, body = parse_frontmatter(content)
        assert fm is None
        assert body == content

    def test_valid_frontmatter_is_parsed(self):
        """Valid frontmatter is returned as a dict; body is the remainder."""
        content = "---\ntitle: Hello\nauthor: Alice\n---\n\n# Body"
        fm, body = parse_frontmatter(content)
        assert isinstance(fm, dict)
        assert fm["title"] == "Hello"
        assert fm["author"] == "Alice"
        assert "# Body" in body

    def test_quoted_values_are_stripped(self):
        """Quoted frontmatter values have their surrounding quotes stripped."""
        content = '---\ntitle: "Quoted Title"\n---\n\nBody'
        fm, _ = parse_frontmatter(content)
        assert fm is not None
        assert fm["title"] == "Quoted Title"

    def test_malformed_frontmatter_returns_none_gracefully(self):
        """Frontmatter that opens with --- but never closes returns (None, original)."""
        content = "---\ntitle: Oops\n# no closing fence"
        fm, body = parse_frontmatter(content)
        assert fm is None
        assert body == content


class TestFixBrokenProjectLinks:
    """Tests for fix_broken_project_links function."""

    def test_existing_file_link_is_kept(self, tmp_path):
        """A /projects/repo/ link whose target exists is left unchanged."""
        (tmp_path / "guide.md").write_text("# Guide")
        content = "[Guide](/projects/myrepo/guide)"
        result = fix_broken_project_links(content, "myrepo", str(tmp_path))
        assert result == content

    def test_missing_file_link_redirects_to_github(self, tmp_path):
        """A /projects/repo/ link whose target is missing becomes a GitHub link."""
        content = "[Missing](/projects/myrepo/does-not-exist)"
        result = fix_broken_project_links(content, "myrepo", str(tmp_path))
        assert result == "[Missing](https://github.com/gardenlinux/myrepo/blob/main/does-not-exist)"

    def test_external_link_is_not_touched(self, tmp_path):
        """External links are left unchanged regardless of target existence."""
        content = "[External](https://example.com/page)"
        result = fix_broken_project_links(content, "myrepo", str(tmp_path))
        assert result == content

    def test_other_project_link_is_not_touched(self, tmp_path):
        """Links to other repos under /projects/ are not modified."""
        content = "[Other](/projects/other-repo/some-page)"
        result = fix_broken_project_links(content, "myrepo", str(tmp_path))
        assert result == content