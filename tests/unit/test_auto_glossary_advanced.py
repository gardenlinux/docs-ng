"""Tests for alias extraction features."""

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
