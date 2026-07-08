"""Unit tests for _generate_anchor method."""

from pathlib import Path

import pytest

from aggregation.auto_glossary import AutoGlossary


class TestGenerateAnchor:
    """Tests for VitePress-compatible anchor generation."""

    @pytest.fixture
    def linker(self, tmp_path):
        """Create a basic AutoGlossary instance for testing."""
        glossary = tmp_path / "glossary.md"
        glossary.write_text("# Glossary\n\n### Test\n\nDefinition.")
        return AutoGlossary(glossary)

    def test_simple_term(self, linker):
        """Test simple single-word term."""
        assert linker._generate_anchor("AWS") == "aws"
        assert linker._generate_anchor("Azure") == "azure"

    def test_multiword_term(self, linker):
        """Test multi-word terms preserve hyphens."""
        assert linker._generate_anchor("Garden Linux") == "garden-linux"
        assert linker._generate_anchor("Bare Metal") == "bare-metal"

    def test_term_with_parentheses(self, linker):
        """Test terms with parentheses."""
        result = linker._generate_anchor("ADR (Architecture Decision Record)")
        assert result == "adr-architecture-decision-record"

        result = linker._generate_anchor("CIS (Center for Internet Security)")
        assert result == "cis-center-for-internet-security"

    def test_term_with_hyphens(self, linker):
        """Test terms that already contain hyphens."""
        assert linker._generate_anchor("end-to-end") == "end-to-end"
        assert linker._generate_anchor("Just-in-Time") == "just-in-time"

    def test_term_with_special_characters(self, linker):
        """Test removal of special characters."""
        assert linker._generate_anchor("Test: Example") == "test-example"
        assert linker._generate_anchor("Test/Example") == "test-example"
        assert linker._generate_anchor("Test.Example") == "test-example"

    def test_term_with_numbers(self, linker):
        """Test terms containing numbers."""
        assert linker._generate_anchor("IPv4") == "ipv4"
        assert linker._generate_anchor("HTTP/2") == "http-2"

    def test_leading_trailing_whitespace(self, linker):
        """Test that whitespace is stripped."""
        assert linker._generate_anchor("  AWS  ") == "aws"
        assert linker._generate_anchor("  Garden Linux  ") == "garden-linux"

    def test_consecutive_spaces(self, linker):
        """Test that consecutive spaces become single hyphen."""
        assert linker._generate_anchor("Garden  Linux") == "garden-linux"
        assert (
            linker._generate_anchor("Test   Multiple   Spaces")
            == "test-multiple-spaces"
        )

    def test_consecutive_hyphens(self, linker):
        """Test that consecutive hyphens are collapsed."""
        assert linker._generate_anchor("Test--Example") == "test-example"
        assert linker._generate_anchor("Test---Example") == "test-example"

    def test_leading_trailing_hyphens(self, linker):
        """Test that leading/trailing hyphens are removed."""
        assert linker._generate_anchor("-AWS-") == "aws"
        assert linker._generate_anchor("--Test--") == "test"

    def test_mixed_special_characters(self, linker):
        """Test complex terms with mixed special characters."""
        # Parentheses, commas, ampersands, etc.
        result = linker._generate_anchor("SAP (S/4HANA, ERP & CRM)")
        assert result == "sap-s-4hana-erp-crm"

    def test_underscores(self, linker):
        """Test handling of underscores."""
        # VitePress typically converts underscores to hyphens or removes them
        assert linker._generate_anchor("my_term") in ["my-term", "myterm"]

    def test_real_glossary_terms(self, linker):
        """Test against actual terms from the glossary."""
        real_terms = {
            "ADR (Architecture Decision Record)": "adr-architecture-decision-record",
            "Architecture": "architecture",
            "AWS": "aws",
            "Azure": "azure",
            "Bare Metal": "bare-metal",
            "Builder": "builder",
            "Build Flavor String": "build-flavor-string",
            "CIS (Center for Internet Security)": "cis-center-for-internet-security",
            "Cloud Image": "cloud-image",
            "Garden Linux": "garden-linux",
            "GitHub Actions": "github-actions",
            "KVM": "kvm",
            "Lima (Linux Machines)": "lima-linux-machines",
            "LTS Kernel": "lts-kernel",
            "OCI (OCI Image Format)": "oci-oci-image-format",
            "Patch Version": "patch-version",
            "Secure Boot": "secure-boot",
            "SELinux": "selinux",
            "TPM2": "tpm2",
        }

        for term, expected_anchor in real_terms.items():
            result = linker._generate_anchor(term)
            assert (
                result == expected_anchor
            ), f"Failed for '{term}': got '{result}', expected '{expected_anchor}'"

    def test_unicode_handling(self, linker):
        """Test handling of unicode characters."""
        # Should convert or remove non-ASCII characters
        result = linker._generate_anchor("Café")
        assert result in ["cafe", "caf"]  # Either remove or transliterate

    def test_empty_and_whitespace_only(self, linker):
        """Test edge cases with empty/whitespace strings."""
        with pytest.raises(ValueError, match="empty or whitespace-only"):
            linker._generate_anchor("")

        with pytest.raises(ValueError, match="empty or whitespace-only"):
            linker._generate_anchor("   ")

        with pytest.raises(ValueError, match="empty or whitespace-only"):
            linker._generate_anchor("\t\n")

    def test_case_preservation_then_lowercase(self, linker):
        """Test that case is properly converted to lowercase."""
        assert linker._generate_anchor("CamelCase") == "camelcase"
        assert linker._generate_anchor("UPPERCASE") == "uppercase"
        assert linker._generate_anchor("MixedCASE") == "mixedcase"
