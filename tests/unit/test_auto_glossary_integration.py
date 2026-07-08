"""Integration tests for AutoGlossary functionality."""

from pathlib import Path

import pytest

from aggregation.auto_glossary import AutoGlossary, process_glossary_links


class TestAutoGlossaryIntegration:
    """Integration tests for complete glossary linking workflow."""

    @pytest.fixture
    def glossary_file(self, tmp_path):
        """Create a test glossary file."""
        glossary = tmp_path / "reference"
        glossary.mkdir()
        glossary_md = glossary / "glossary.md"
        glossary_md.write_text("""---
title: "Glossary"
---

# Glossary

## A

### AWS

Amazon Web Services. A cloud platform.

### Azure

Microsoft Azure cloud platform.

## G

### Garden Linux

A Debian-based Linux distribution.

### GitHub Actions

Continuous integration platform.

## K

### KVM

Kernel-based Virtual Machine.
""")
        return glossary_md

    def test_parse_glossary_basic(self, glossary_file):
        """Test that glossary terms are parsed correctly."""
        linker = AutoGlossary(glossary_file)

        assert "aws" in linker.terms
        assert "azure" in linker.terms
        assert "garden linux" in linker.terms
        assert "github actions" in linker.terms
        assert "kvm" in linker.terms

        # Check anchor generation
        anchor, display_name = linker.terms["aws"]
        assert anchor == "aws"
        assert display_name == "AWS"

        anchor, display_name = linker.terms["garden linux"]
        assert anchor == "garden-linux"
        assert display_name == "Garden Linux"

    def test_link_terms_basic(self, glossary_file):
        """Test basic term linking."""
        linker = AutoGlossary(glossary_file)

        content = "Use {glossary:AWS} for cloud deployment."
        result = linker.link_terms(content)

        assert "[AWS](/reference/glossary#aws)" in result
        assert "{glossary:AWS}" not in result

    def test_link_terms_multiple(self, glossary_file):
        """Test linking multiple terms in same content."""
        linker = AutoGlossary(glossary_file)

        content = (
            "Deploy {glossary:Garden Linux} on {glossary:AWS} or {glossary:Azure}."
        )
        result = linker.link_terms(content)

        assert "[Garden Linux](/reference/glossary#garden-linux)" in result
        assert "[AWS](/reference/glossary#aws)" in result
        assert "[Azure](/reference/glossary#azure)" in result

    def test_link_terms_case_insensitive(self, glossary_file):
        """Test that term matching is case-insensitive."""
        linker = AutoGlossary(glossary_file)

        content = "Use {glossary:aws} or {glossary:AWS} or {glossary:Aws}."
        result = linker.link_terms(content)

        # All variants should be linked
        assert result.count("[aws](/reference/glossary#aws)") == 1
        assert result.count("[AWS](/reference/glossary#aws)") == 1
        assert result.count("[Aws](/reference/glossary#aws)") == 1

    def test_link_terms_preserves_code_blocks(self, glossary_file):
        """Test that code blocks are not modified."""
        linker = AutoGlossary(glossary_file)

        content = """# Example

```bash
# Do not link {glossary:AWS} in code
echo "AWS"
```

Regular text with {glossary:AWS}.
"""
        result = linker.link_terms(content)

        # Code block should remain unchanged
        assert "# Do not link {glossary:AWS} in code" in result
        # But regular text should be linked
        assert "[AWS](/reference/glossary#aws)" in result

    def test_link_terms_preserves_inline_code(self, glossary_file):
        """Test that inline code is not modified."""
        linker = AutoGlossary(glossary_file)

        content = "Use `{glossary:AWS}` configuration or {glossary:AWS} directly."
        result = linker.link_terms(content)

        # Inline code should remain unchanged
        assert "`{glossary:AWS}`" in result
        # But regular text should be linked
        assert "[AWS](/reference/glossary#aws)" in result

    def test_link_terms_preserves_existing_links(self, glossary_file):
        """Test that existing markdown links are not modified."""
        linker = AutoGlossary(glossary_file)

        content = "See [AWS docs](https://aws.amazon.com) and {glossary:AWS}."
        result = linker.link_terms(content)

        # Existing link should remain unchanged
        assert "[AWS docs](https://aws.amazon.com)" in result
        # Glossary marker should be linked
        assert "[AWS](/reference/glossary#aws)" in result

    def test_link_terms_unknown_term_warning(self, glossary_file, capsys):
        """Test that unknown terms produce warnings."""
        linker = AutoGlossary(glossary_file)

        content = "Use {glossary:UnknownTerm} here."
        result = linker.link_terms(content, file_path="test.md")

        # Unknown term should remain unchanged
        assert "{glossary:UnknownTerm}" in result
        # Should produce warning
        captured = capsys.readouterr()
        assert "UnknownTerm" in captured.out
        assert "not found" in captured.out

    def test_custom_entry_format(self, glossary_file):
        """Test using custom entry format."""
        linker = AutoGlossary(glossary_file, entry_format="[[*]]")

        content = "Use [[AWS]] for deployment."
        result = linker.link_terms(content)

        assert "[AWS](/reference/glossary#aws)" in result
        assert "[[AWS]]" not in result

    def test_skip_glossary_file_itself(self, glossary_file):
        """Test that glossary file itself is not modified."""
        linker = AutoGlossary(glossary_file)

        content = "### AWS\n\nUse {glossary:AWS} for testing."
        result = linker.link_terms(content, file_path="reference/glossary.md")

        # Should remain unchanged
        assert result == content
        assert "{glossary:AWS}" in result

    def test_process_glossary_links_integration(self, tmp_path):
        """Test the complete process_glossary_links function."""
        docs_dir = tmp_path

        # Create glossary
        ref_dir = docs_dir / "reference"
        ref_dir.mkdir()
        glossary = ref_dir / "glossary.md"
        glossary.write_text("""# Glossary

### Test Term

A test term definition.
""")

        # Create test markdown file
        test_file = docs_dir / "test.md"
        test_file.write_text("This is a {glossary:Test Term} example.")

        # Process files
        count = process_glossary_links(docs_dir)

        assert count == 1

        # Check that file was modified
        result = test_file.read_text()
        assert "[Test Term](/reference/glossary#test-term)" in result
        assert "{glossary:Test Term}" not in result

    def test_process_glossary_links_no_changes(self, tmp_path):
        """Test that files without markers are not modified."""
        docs_dir = tmp_path

        # Create glossary
        ref_dir = docs_dir / "reference"
        ref_dir.mkdir()
        glossary = ref_dir / "glossary.md"
        glossary.write_text("# Glossary\n\n### Test\n\nDefinition.")

        # Create file without glossary markers
        test_file = docs_dir / "test.md"
        test_file.write_text("This is plain content.")

        # Process files
        count = process_glossary_links(docs_dir)

        # No files should be modified
        assert count == 0
        assert test_file.read_text() == "This is plain content."

    def test_multiword_terms_with_parentheses(self, glossary_file):
        """Test terms with parentheses like 'ADR (Architecture Decision Record)'."""
        # Add term with parentheses to glossary
        glossary_content = glossary_file.read_text()
        glossary_content += (
            "\n### ADR (Architecture Decision Record)\n\nA documentation pattern.\n"
        )
        glossary_file.write_text(glossary_content)

        linker = AutoGlossary(glossary_file)

        content = "See {glossary:ADR (Architecture Decision Record)} for details."
        result = linker.link_terms(content)

        assert (
            "[ADR (Architecture Decision Record)](/reference/glossary#adr-architecture-decision-record)"
            in result
        )
