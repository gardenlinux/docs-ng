"""Tests for alias extraction and auto-linking features."""

from pathlib import Path

import pytest

from aggregation.auto_glossary import AutoGlossary


class TestAliasExtraction:
    """Tests for automatic alias extraction from glossary terms."""

    @pytest.fixture
    def glossary_with_aliases(self, tmp_path):
        """Create glossary with terms that have aliases."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("""# Glossary

### ADR (Architecture Decision Record)

A document that captures decisions.

### CIS (Center for Internet Security)

A security framework.

### Lima (Linux Machines)

A VM tool for macOS.

### OCI (OCI Image Format)

Container image format.
""")
        return glossary

    def test_extract_aliases_from_parentheses(self, glossary_with_aliases):
        """Test that aliases are extracted from parenthesized expansions."""
        linker = AutoGlossary(glossary_with_aliases)

        # Main term should exist
        assert "adr (architecture decision record)" in linker.terms

        # Expansion should be an alias
        assert "architecture decision record" in linker.aliases
        assert (
            linker.aliases["architecture decision record"]
            == "adr (architecture decision record)"
        )

        # Abbreviation alone should be an alias
        assert "adr" in linker.aliases
        assert linker.aliases["adr"] == "adr (architecture decision record)"

    def test_multiple_aliases(self, glossary_with_aliases):
        """Test that multiple terms with aliases work correctly."""
        linker = AutoGlossary(glossary_with_aliases)

        # Check CIS aliases
        assert "cis" in linker.aliases
        assert "center for internet security" in linker.aliases

        # Check Lima aliases
        assert "lima" in linker.aliases
        assert "linux machines" in linker.aliases

    def test_link_via_alias(self, glossary_with_aliases):
        """Test linking using an alias instead of main term."""
        linker = AutoGlossary(glossary_with_aliases)

        # Link using expansion alias
        content = "See {glossary:Architecture Decision Record} for details."
        result = linker.link_terms(content)
        assert (
            "[Architecture Decision Record](/reference/glossary#adr-architecture-decision-record)"
            in result
        )

        # Link using abbreviation alias
        content2 = "Use {glossary:ADR} format."
        result2 = linker.link_terms(content2)
        assert "[ADR](/reference/glossary#adr-architecture-decision-record)" in result2

    def test_alias_case_insensitive(self, glossary_with_aliases):
        """Test that alias matching is case-insensitive."""
        linker = AutoGlossary(glossary_with_aliases)

        content = "Use {glossary:adr} or {glossary:ARCHITECTURE DECISION RECORD}."
        result = linker.link_terms(content)

        assert "[adr](/reference/glossary#adr-architecture-decision-record)" in result
        assert (
            "[ARCHITECTURE DECISION RECORD](/reference/glossary#adr-architecture-decision-record)"
            in result
        )


class TestAutoLinking:
    """Tests for automatic term linking without explicit markers."""

    @pytest.fixture
    def glossary_for_autolink(self, tmp_path):
        """Create glossary for auto-link testing."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("""# Glossary

### AWS

Amazon Web Services.

### Garden Linux

A Linux distribution.

### KVM

Kernel-based Virtual Machine.

### Azure

Microsoft Azure platform.
""")
        return glossary

    def test_auto_link_first_occurrence(self, glossary_for_autolink):
        """Test that first occurrence of term is auto-linked."""
        linker = AutoGlossary(glossary_for_autolink)

        content = "Deploy on AWS. AWS is a cloud platform."
        result = linker.link_terms(content, auto_link=True)

        # First AWS should be linked
        assert "[AWS](/reference/glossary#aws)" in result
        # Second AWS should remain unlinked
        assert result.count("[AWS](/reference/glossary#aws)") == 1
        assert result.count("AWS") == 2

    def test_auto_link_multiword_term(self, glossary_for_autolink):
        """Test auto-linking multi-word terms."""
        linker = AutoGlossary(glossary_for_autolink)

        content = "Garden Linux is great. Use Garden Linux for deployment."
        result = linker.link_terms(content, auto_link=True)

        # First occurrence should be linked
        assert "[Garden Linux](/reference/glossary#garden-linux)" in result
        # Only one occurrence should be linked
        assert result.count("[Garden Linux](/reference/glossary#garden-linux)") == 1

    def test_auto_link_multiple_terms(self, glossary_for_autolink):
        """Test auto-linking multiple different terms."""
        linker = AutoGlossary(glossary_for_autolink)

        content = "Deploy Garden Linux on AWS using KVM virtualization."
        result = linker.link_terms(content, auto_link=True)

        assert "[Garden Linux](/reference/glossary#garden-linux)" in result
        assert "[AWS](/reference/glossary#aws)" in result
        assert "[KVM](/reference/glossary#kvm)" in result

    def test_auto_link_case_insensitive(self, glossary_for_autolink):
        """Test that auto-linking is case-insensitive."""
        linker = AutoGlossary(glossary_for_autolink)

        content = "Use aws for deployment."
        result = linker.link_terms(content, auto_link=True)

        # Should link even with lowercase
        assert "[aws](/reference/glossary#aws)" in result

    def test_auto_link_preserves_existing_markers(self, glossary_for_autolink):
        """Test that explicit markers take precedence over auto-linking."""
        linker = AutoGlossary(glossary_for_autolink)

        content = "Use {glossary:AWS} and AWS again."
        result = linker.link_terms(content, auto_link=True)

        # Marker should be processed
        assert "[AWS](/reference/glossary#aws)" in result
        # Auto-link should still work for second occurrence
        # (but only first unlinked occurrence)
        assert result.count("[AWS](/reference/glossary#aws)") >= 1

    def test_auto_link_disabled_by_default(self, glossary_for_autolink):
        """Test that auto-linking is disabled by default."""
        linker = AutoGlossary(glossary_for_autolink)

        content = "Deploy on AWS using KVM."
        result = linker.link_terms(content, auto_link=False)

        # No links should be created without markers
        assert "[AWS]" not in result
        assert "[KVM]" not in result
        assert result == content

    def test_auto_link_preserves_code_blocks(self, glossary_for_autolink):
        """Test that auto-linking doesn't affect code blocks."""
        linker = AutoGlossary(glossary_for_autolink)

        content = """Deploy AWS outside code.

```bash
# Do not link AWS in code
echo "AWS"
```
"""
        result = linker.link_terms(content, auto_link=True)

        # AWS outside code should be linked
        lines = result.split("\n")
        assert "[AWS](/reference/glossary#aws)" in lines[0]
        # AWS in code should not be linked
        assert "# Do not link AWS in code" in result
        assert 'echo "AWS"' in result

    def test_auto_link_preserves_inline_code(self, glossary_for_autolink):
        """Test that auto-linking doesn't affect inline code."""
        linker = AutoGlossary(glossary_for_autolink)

        content = "Use AWS with `AWS` config."
        result = linker.link_terms(content, auto_link=True)

        # First AWS should be linked
        assert "[AWS](/reference/glossary#aws)" in result
        # Inline code AWS should not be linked
        assert "`AWS`" in result

    def test_auto_link_word_boundaries(self, glossary_for_autolink):
        """Test that auto-linking respects word boundaries."""
        linker = AutoGlossary(glossary_for_autolink)

        content = "AWSXYZ is not AWS. Use AWS here."
        result = linker.link_terms(content, auto_link=True)

        # AWSXYZ should not be linked
        assert "AWSXYZ" in result
        assert "[AWSXYZ]" not in result
        # Standalone AWS should be linked
        assert "[AWS](/reference/glossary#aws)" in result

    def test_auto_link_longest_match_first(self, glossary_for_autolink):
        """Test that longer terms are matched before shorter ones."""
        linker = AutoGlossary(glossary_for_autolink)

        # "Garden Linux" should be matched before "Linux" if both were terms
        content = "Garden Linux is great."
        result = linker.link_terms(content, auto_link=True)

        # Whole phrase should be linked
        assert "[Garden Linux](/reference/glossary#garden-linux)" in result
        # Should not have partial matches
        assert result.count("[") == 1


class TestAliasAndAutoLinkCombined:
    """Test interaction between aliases and auto-linking."""

    @pytest.fixture
    def combined_glossary(self, tmp_path):
        """Create glossary with aliases for auto-link testing."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("""# Glossary

### ADR (Architecture Decision Record)

A document format.

### VM (Virtual Machine)

Virtualization technology.
""")
        return glossary

    def test_auto_link_via_alias(self, combined_glossary):
        """Test that aliases can be auto-linked."""
        linker = AutoGlossary(combined_glossary)

        # Use expansion in text
        content = "An Architecture Decision Record documents choices."
        result = linker.link_terms(content, auto_link=True)

        # Should link via alias
        assert "/reference/glossary#adr-architecture-decision-record" in result

    def test_auto_link_abbreviation_alias(self, combined_glossary):
        """Test auto-linking abbreviation aliases."""
        linker = AutoGlossary(combined_glossary)

        content = "Use ADR format for documentation."
        result = linker.link_terms(content, auto_link=True)

        assert "[ADR](/reference/glossary#adr-architecture-decision-record)" in result
