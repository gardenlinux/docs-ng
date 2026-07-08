"""Unit tests for aggregation.models module."""

import pytest

from aggregation import AggregateResult, RepoConfig
from aggregation.models import _DEFAULT_MEDIA_DIRECTORIES


class TestRepoConfig:
    """Tests for RepoConfig dataclass."""

    def test_from_dict_minimal(self):
        """Test creating RepoConfig from minimal valid dict."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "docs_path": "docs",
            "ref": "main",
        }
        repo = RepoConfig.from_dict(data)
        assert repo.name == "test-repo"
        assert repo.url == "https://github.com/test/repo"
        assert repo.docs_path == "docs"
        assert repo.target_path == ""
        assert repo.ref == "main"
        assert repo.commit is None
        assert repo.root_files == []
        assert repo.structure == "flat"

    def test_from_dict_with_target_path(self):
        """Test creating RepoConfig from dict including optional target_path."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "docs_path": "docs",
            "target_path": "projects/test-repo",
            "ref": "main",
        }
        repo = RepoConfig.from_dict(data)
        assert repo.target_path == "projects/test-repo"

    def test_from_dict_full(self):
        """Test creating RepoConfig from dict with all fields."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "docs_path": "docs",
            "ref": "main",
            "commit": "abc123",
            "root_files": ["README.md", "LICENSE"],
            "structure": "sphinx",
            "media_directories": [".media"],
        }
        repo = RepoConfig.from_dict(data)
        assert repo.commit == "abc123"
        assert repo.root_files == ["README.md", "LICENSE"]
        assert repo.structure == "sphinx"
        assert repo.media_directories == [".media"]

    def test_from_dict_defaults_docs_path(self):
        """Test that from_dict defaults docs_path to 'docs' when key is absent."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "ref": "main",
        }
        repo = RepoConfig.from_dict(data)
        assert repo.docs_path == "docs"

    def test_from_dict_defaults_media_directories(self):
        """Test that from_dict defaults media_directories to the standard list when absent."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "ref": "main",
        }
        repo = RepoConfig.from_dict(data)
        assert repo.media_directories == list(_DEFAULT_MEDIA_DIRECTORIES)

    def test_from_dict_explicit_empty_media_directories_preserved(self):
        """Test that an explicit empty media_directories [] is preserved, not replaced by default."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "ref": "main",
            "media_directories": [],
        }
        repo = RepoConfig.from_dict(data)
        assert repo.media_directories == []

    def test_from_dict_rejects_dict_structure(self):
        """Test that a dict-typed structure value raises ValueError."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "ref": "main",
            "structure": {"tutorials": "tutorials"},
        }
        with pytest.raises(ValueError, match="'structure' must be a string"):
            RepoConfig.from_dict(data)

    def test_is_local_file_url(self):
        """Test is_local property with file:// URL."""
        repo = RepoConfig(
            name="local",
            url="file://../gardenlinux",
            docs_path="docs",
            ref="",
        )
        assert repo.is_local is True
        assert repo.is_remote is False

    def test_is_remote_https_url(self):
        """Test is_remote property with https:// URL."""
        repo = RepoConfig(
            name="remote",
            url="https://github.com/test/repo",
            docs_path="docs",
            ref="main",
        )
        assert repo.is_remote is True
        assert repo.is_local is False

    def test_local_path_property(self):
        """Test local_path property strips file:// prefix."""
        repo = RepoConfig(
            name="local",
            url="file://../gardenlinux",
            docs_path="docs",
            ref="",
        )
        assert repo.local_path == "../gardenlinux"

    def test_validate_local_without_ref(self):
        """Test that local repos don't require ref."""
        repo = RepoConfig(
            name="local",
            url="file://../gardenlinux",
            docs_path="docs",
            ref="",
        )
        repo.validate()  # Should not raise

    def test_validate_remote_requires_ref(self):
        """Test that remote repos must have ref."""
        repo = RepoConfig(
            name="remote",
            url="https://github.com/test/repo",
            docs_path="docs",
            ref="",
        )
        with pytest.raises(ValueError, match="must have 'ref' field"):
            repo.validate()

    def test_validate_invalid_url_scheme(self):
        """Test that invalid URL schemes are rejected."""
        repo = RepoConfig(
            name="invalid",
            url="ftp://example.com/repo",
            docs_path="docs",
            ref="",
        )
        with pytest.raises(ValueError, match="Invalid URL scheme"):
            repo.validate()

    def test_from_dict_defaults_ref_to_main(self):
        """Test that from_dict defaults ref to 'main' when key is absent."""
        data = {
            "name": "local-repo",
            "url": "file://../some-repo",
            "docs_path": "docs",
        }
        repo = RepoConfig.from_dict(data)
        assert repo.ref == "main"

    def test_from_dict_explicit_empty_ref_falls_back_to_main(self):
        """Test that from_dict defaults empty ref to 'main' (the 'or main' behavior)."""
        data = {
            "name": "local-repo",
            "url": "file://../some-repo",
            "docs_path": "docs",
            "ref": "",
        }
        repo = RepoConfig.from_dict(data)
        assert repo.ref == "main"

    def test_validate_remote_with_ref_passes(self):
        """Test that remote repos with a valid ref pass validation."""
        repo = RepoConfig(
            name="remote",
            url="https://github.com/test/repo",
            docs_path="docs",
            ref="main",
        )
        repo.validate()  # Should not raise

    def test_local_path_with_absolute_url(self):
        """Test local_path strips file:// from an absolute path."""
        repo = RepoConfig(
            name="local",
            url="file:///abs/path/to/repo",
            docs_path="docs",
            ref="",
        )
        assert repo.local_path == "/abs/path/to/repo"


class TestAggregateResult:
    """Tests for AggregateResult dataclass."""

    def test_success_result(self):
        """Test creating success result."""
        result = AggregateResult("test-repo", True, "abc123")
        assert result.repo_name == "test-repo"
        assert result.success is True
        assert result.resolved_commit == "abc123"

    def test_failure_result(self):
        """Test creating failure result."""
        result = AggregateResult("test-repo", False, None)
        assert result.repo_name == "test-repo"
        assert result.success is False
        assert result.resolved_commit is None
