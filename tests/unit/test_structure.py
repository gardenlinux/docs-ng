"""Unit tests for aggregation.structure module."""

from pathlib import Path

import pytest
from aggregation.structure import transform_directory_structure


class TestTransformDirectoryStructure:
    """Tests for transform_directory_structure function."""

    def test_dict_map_renames_directories(self, tmp_path):
        """Directories are renamed according to the dict structure map."""
        source = tmp_path / "source"
        (source / "01_intro").mkdir(parents=True)
        (source / "01_intro" / "index.md").write_text("# Intro")
        (source / "02_guide").mkdir()
        (source / "02_guide" / "guide.md").write_text("# Guide")

        target = tmp_path / "target"

        transform_directory_structure(
            str(source),
            str(target),
            structure_map={"01_intro": "intro", "02_guide": "guide"},
        )

        assert (target / "intro" / "index.md").exists()
        assert (target / "guide" / "guide.md").exists()
        # Original names should NOT appear in the target
        assert not (target / "01_intro").exists()
        assert not (target / "02_guide").exists()

    def test_flat_structure_copies_files(self, tmp_path):
        """With structure_map='flat', all files are copied as-is."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "readme.md").write_text("# README")
        (source / "guide.md").write_text("# Guide")

        target = tmp_path / "target"

        transform_directory_structure(str(source), str(target), structure_map="flat")

        assert (target / "readme.md").exists()
        assert (target / "guide.md").exists()

    def test_sphinx_structure_cleans_target(self, tmp_path):
        """When structure_map='sphinx', a pre-existing target directory is wiped."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "new.md").write_text("# New")

        target = tmp_path / "target"
        target.mkdir()
        stale = target / "stale.md"
        stale.write_text("# Stale file from previous run")
        assert stale.exists()

        transform_directory_structure(
            str(source), str(target), structure_map="sphinx"
        )

        assert not stale.exists(), "Stale file should have been removed by sphinx clean"
        assert (target / "new.md").exists()

    def test_special_files_placed_in_subdir(self, tmp_path):
        """Files listed in special_files are copied to their configured subdirectory."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "CHANGELOG.md").write_text("# Changelog")
        (source / "intro").mkdir()
        (source / "intro" / "index.md").write_text("# Intro")

        target = tmp_path / "target"

        transform_directory_structure(
            str(source),
            str(target),
            structure_map={"intro": "intro"},
            special_files={"CHANGELOG.md": "reference/"},
        )

        assert (target / "reference" / "CHANGELOG.md").exists()

    def test_creates_target_if_missing(self, tmp_path):
        """Target directory is created automatically if it does not exist."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "page.md").write_text("# Page")

        target = tmp_path / "nested" / "target"
        assert not target.exists()

        transform_directory_structure(str(source), str(target), structure_map="flat")

        assert target.exists()
        assert (target / "page.md").exists()

    def test_underscore_prefixed_files_are_skipped_in_dict_mode(self, tmp_path):
        """In dict-map mode, files/dirs starting with _ are skipped (not in structure_map)."""
        source = tmp_path / "source"
        source.mkdir()
        (source / "_private.md").write_text("# Private")
        (source / "public.md").write_text("# Public")

        target = tmp_path / "target"

        # Use dict mode with an empty map: _private.md is not in map, not special,
        # and starts with _, so the dict branch skips it.
        transform_directory_structure(str(source), str(target), structure_map={})

        assert not (target / "_private.md").exists()
        assert (target / "public.md").exists()
