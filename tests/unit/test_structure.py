"""Unit tests for aggregation.structure module."""

from pathlib import Path

import pytest
from aggregation.structure import copy_targeted_docs, verify_internal_links


class TestCopyTargetedDocs:
    """Tests for copy_targeted_docs function."""

    def test_copies_file_with_github_target_path(self, tmp_path):
        """Files with github_target_path are copied to the specified location."""
        source = tmp_path / "source"
        source.mkdir()
        docs = tmp_path / "docs"
        docs.mkdir()

        content = (
            "---\n"
            "title: Example\n"
            "github_target_path: docs/how-to/example.md\n"
            "---\n\n# Example\n"
        )
        (source / "example.md").write_text(content)

        copy_targeted_docs(str(source), str(docs), "myrepo")

        assert (docs / "how-to" / "example.md").exists()

    def test_skips_file_without_github_target_path(self, tmp_path):
        """Files without github_target_path are not copied."""
        source = tmp_path / "source"
        source.mkdir()
        docs = tmp_path / "docs"
        docs.mkdir()

        (source / "untargeted.md").write_text("# No target\n")

        copy_targeted_docs(str(source), str(docs), "myrepo")

        # Nothing should be copied to docs/
        assert list(docs.rglob("*.md")) == []

    def test_missing_source_dir_warns_gracefully(self, tmp_path, capsys):
        """Missing source dir logs a warning and returns without error."""
        docs = tmp_path / "docs"
        docs.mkdir()

        copy_targeted_docs(str(tmp_path / "nonexistent"), str(docs), "myrepo")

        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_retargeted_media_colocated_with_target(self, tmp_path):
        """Media next to a retargeted file lands at the target parent, not source parent.

        Concrete case: glrd overview/README.md → reference/supporting_tools/glrd.md
        Media at overview/assets/ must end up at reference/supporting_tools/assets/.
        """
        source = tmp_path / "source"
        (source / "overview" / "assets").mkdir(parents=True)
        docs = tmp_path / "docs"
        docs.mkdir()

        content = (
            "---\n"
            "title: GLRD\n"
            "github_target_path: docs/reference/supporting_tools/glrd.md\n"
            "---\n\n![Overview](assets/x.png)\n"
        )
        (source / "overview" / "README.md").write_text(content)
        (source / "overview" / "assets" / "x.png").write_bytes(b"\x89PNG")

        copy_targeted_docs(
            str(source), str(docs), "glrd", media_dirs=["assets"]
        )

        # Targeted file copied to correct location
        assert (docs / "reference" / "supporting_tools" / "glrd.md").exists()
        # Media colocated with retargeted file
        assert (docs / "reference" / "supporting_tools" / "assets" / "x.png").exists()
        # Media must NOT appear at the source-relative path
        assert not (docs / "overview").exists()

    def test_identity_mapped_media_unchanged(self, tmp_path):
        """Media next to an identity-mapped file stays at its source-relative location.

        Gardenlinux case: tutorials/cloud/first-boot-aws.md → tutorials/cloud/first-boot-aws.md
        Media at tutorials/assets/img.png must still end up at tutorials/assets/img.png.
        """
        source = tmp_path / "source"
        (source / "tutorials" / "cloud").mkdir(parents=True)
        (source / "tutorials" / "assets").mkdir(parents=True)
        docs = tmp_path / "docs"
        docs.mkdir()

        content = (
            "---\n"
            "title: First Boot AWS\n"
            "github_target_path: docs/tutorials/cloud/first-boot-aws.md\n"
            "---\n\n![Img](../assets/img.png)\n"
        )
        (source / "tutorials" / "cloud" / "first-boot-aws.md").write_text(content)
        (source / "tutorials" / "assets" / "img.png").write_bytes(b"\x89PNG")

        copy_targeted_docs(
            str(source), str(docs), "gardenlinux", media_dirs=["assets"]
        )

        # Targeted file at its correct location
        assert (docs / "tutorials" / "cloud" / "first-boot-aws.md").exists()
        # Media at source-relative path (identity mapping: source parent "tutorials/cloud"
        # maps to target parent "tutorials/cloud"; the assets dir parent is "tutorials",
        # which has no file mapped from it, so fallback fires and preserves the path)
        assert (docs / "tutorials" / "assets" / "img.png").exists()


class TestVerifyInternalLinks:
    """Tests for verify_internal_links function."""

    def test_no_errors_when_no_shipped_files(self, tmp_path):
        """Returns 0 when no files are shipped (no github_target_path)."""
        source = tmp_path / "source"
        source.mkdir()
        docs = tmp_path / "docs"
        docs.mkdir()

        (source / "untargeted.md").write_text("[Link](other.md)\n")

        errors = verify_internal_links(str(source), str(docs), "myrepo")
        assert errors == 0

    def test_no_errors_when_links_are_external(self, tmp_path):
        """External links and anchors in shipped files do not trigger errors."""
        source = tmp_path / "source"
        source.mkdir()
        docs = tmp_path / "docs"
        docs.mkdir()

        content = (
            "---\n"
            "github_target_path: docs/reference/page.md\n"
            "---\n\n"
            "[External](https://example.com)\n"
            "[Anchor](#section)\n"
        )
        (source / "page.md").write_text(content)

        errors = verify_internal_links(str(source), str(docs), "myrepo")
        assert errors == 0

    def test_no_errors_when_linked_file_also_shipped(self, tmp_path):
        """A shipped file linking to another shipped file produces no errors."""
        source = tmp_path / "source"
        source.mkdir()
        docs = tmp_path / "docs"
        docs.mkdir()

        content_a = (
            "---\n"
            "github_target_path: docs/reference/a.md\n"
            "---\n\n[B](b.md)\n"
        )
        content_b = (
            "---\n"
            "github_target_path: docs/reference/b.md\n"
            "---\n\n# B\n"
        )
        (source / "a.md").write_text(content_a)
        (source / "b.md").write_text(content_b)

        errors = verify_internal_links(str(source), str(docs), "myrepo")
        assert errors == 0

    def test_error_when_shipped_file_links_to_unshipped_file(self, tmp_path):
        """A shipped file linking to an existing but unshipped file causes an error."""
        source = tmp_path / "source"
        source.mkdir()
        docs = tmp_path / "docs"
        docs.mkdir()

        content_a = (
            "---\n"
            "github_target_path: docs/reference/a.md\n"
            "---\n\n[Unshipped](unshipped.md)\n"
        )
        # unshipped.md exists in source but has no github_target_path
        content_u = "# Unshipped\n"
        (source / "a.md").write_text(content_a)
        (source / "unshipped.md").write_text(content_u)

        errors = verify_internal_links(str(source), str(docs), "myrepo")
        assert errors == 1

    def test_no_error_for_missing_linked_file(self, tmp_path):
        """Links to files that do not exist in the source tree are not flagged
        (they may be VitePress-resolved or external paths)."""
        source = tmp_path / "source"
        source.mkdir()
        docs = tmp_path / "docs"
        docs.mkdir()

        content = (
            "---\n"
            "github_target_path: docs/reference/page.md\n"
            "---\n\n[Gone](does-not-exist.md)\n"
        )
        (source / "page.md").write_text(content)

        errors = verify_internal_links(str(source), str(docs), "myrepo")
        assert errors == 0
