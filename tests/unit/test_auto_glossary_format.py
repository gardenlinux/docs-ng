"""Unit tests for AutoGlossary entry format functionality."""

from pathlib import Path

import pytest

from aggregation.auto_glossary import GLOSSARY_ENTRY_FORMAT, AutoGlossary


class TestGlossaryEntryFormat:
    """Tests for glossary entry format configuration."""

    def test_default_format(self, tmp_path):
        """Test that default format is used when none is provided."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Test Term\n\nDefinition.")

        linker = AutoGlossary(glossary)
        assert linker.entry_format == GLOSSARY_ENTRY_FORMAT
        assert linker.entry_format == "{glossary:*}"

    def test_custom_format(self, tmp_path):
        """Test that custom format can be provided."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Test Term\n\nDefinition.")

        custom_format = "{{*}}"
        linker = AutoGlossary(glossary, entry_format=custom_format)
        assert linker.entry_format == custom_format

    def test_format_validation_requires_placeholder(self, tmp_path):
        """Test that format must contain * placeholder."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Test Term\n\nDefinition.")

        with pytest.raises(ValueError, match="must contain '\\*' as placeholder"):
            AutoGlossary(glossary, entry_format="{glossary:term}")

    def test_get_entry_format_example_default(self, tmp_path):
        """Test getting example with default format."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### AWS\n\nAmazon Web Services.")

        linker = AutoGlossary(glossary)
        example = linker.get_entry_format_example("AWS")
        assert example == "{glossary:AWS}"

    def test_get_entry_format_example_custom(self, tmp_path):
        """Test getting example with custom format."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### KVM\n\nKernel-based VM.")

        linker = AutoGlossary(glossary, entry_format="[[g:*]]")
        example = linker.get_entry_format_example("KVM")
        assert example == "[[g:KVM]]"

    def test_pattern_building_default_format(self, tmp_path):
        """Test that regex pattern is built correctly from default format."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Test\n\nDefinition.")

        linker = AutoGlossary(glossary)

        # Test the pattern matches the format correctly
        match = linker._entry_pattern.search("{glossary:AWS}")
        assert match is not None
        assert match.group("term") == "AWS"

    def test_pattern_building_custom_format(self, tmp_path):
        """Test that regex pattern is built correctly from custom format."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Test\n\nDefinition.")

        linker = AutoGlossary(glossary, entry_format="{{*}}")

        # Test the pattern matches the custom format
        match = linker._entry_pattern.search("{{Azure}}")
        assert match is not None
        assert match.group("term") == "Azure"

    def test_pattern_captures_multiword_terms(self, tmp_path):
        """Test that pattern captures multi-word terms."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Garden Linux\n\nA Linux distribution.")

        linker = AutoGlossary(glossary)

        match = linker._entry_pattern.search("{glossary:Garden Linux}")
        assert match is not None
        assert match.group("term") == "Garden Linux"

    def test_pattern_captures_terms_with_parentheses(self, tmp_path):
        """Test that pattern captures terms with parentheses."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text(
            "# Glossary\n\n### ADR (Architecture Decision Record)\n\nDefinition."
        )

        linker = AutoGlossary(glossary)

        match = linker._entry_pattern.search(
            "{glossary:ADR (Architecture Decision Record)}"
        )
        assert match is not None
        assert match.group("term") == "ADR (Architecture Decision Record)"

    def test_pattern_does_not_match_without_format(self, tmp_path):
        """Test that plain terms without format markers are not matched."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### AWS\n\nDefinition.")

        linker = AutoGlossary(glossary)

        # Plain term should not match
        match = linker._entry_pattern.search("AWS is a cloud provider")
        assert match is None

    def test_multiple_formats_in_content(self, tmp_path):
        """Test finding multiple formatted terms in content."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### AWS\n### Azure\n### GCP")

        linker = AutoGlossary(glossary)

        content = "Use {glossary:AWS} or {glossary:Azure} or {glossary:GCP}."
        matches = list(linker._entry_pattern.finditer(content))

        assert len(matches) == 3
        assert matches[0].group("term") == "AWS"
        assert matches[1].group("term") == "Azure"
        assert matches[2].group("term") == "GCP"

    def test_alternative_format_brackets(self, tmp_path):
        """Test alternative format using double brackets."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Kubernetes\n\nDefinition.")

        linker = AutoGlossary(glossary, entry_format="[[*]]")

        match = linker._entry_pattern.search("[[Kubernetes]]")
        assert match is not None
        assert match.group("term") == "Kubernetes"

    def test_alternative_format_shorthand(self, tmp_path):
        """Test alternative format using shorthand notation."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Docker\n\nDefinition.")

        linker = AutoGlossary(glossary, entry_format="[g:*]")

        match = linker._entry_pattern.search("[g:Docker]")
        assert match is not None
        assert match.group("term") == "Docker"
