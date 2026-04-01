"""Unit tests for aggregation.models module."""

import pytest
from aggregation import RepoConfig, AggregateResult


class TestRepoConfig:
    """Tests for RepoConfig dataclass."""
    
    def test_from_dict_minimal(self):
        """Test creating RepoConfig from minimal valid dict."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "docs_path": "docs",
            "target_path": "projects/test-repo",
            "ref": "main",
        }
        repo = RepoConfig.from_dict(data)
        assert repo.name == "test-repo"
        assert repo.url == "https://github.com/test/repo"
        assert repo.docs_path == "docs"
        assert repo.target_path == "projects/test-repo"
        assert repo.ref == "main"
        assert repo.commit is None
        assert repo.root_files == []
        assert repo.structure == "flat"
    
    def test_from_dict_full(self):
        """Test creating RepoConfig from dict with all fields."""
        data = {
            "name": "test-repo",
            "url": "https://github.com/test/repo",
            "docs_path": "docs",
            "target_path": "projects/test-repo",
            "ref": "main",
            "commit": "abc123",
            "root_files": ["README.md", "LICENSE"],
            "structure": {"old": "new"},
            "special_files": {"file.md": "special/"},
            "media_directories": [".media"],
        }
        repo = RepoConfig.from_dict(data)
        assert repo.commit == "abc123"
        assert repo.root_files == ["README.md", "LICENSE"]
        assert repo.structure == {"old": "new"}
        assert repo.special_files == {"file.md": "special/"}
        assert repo.media_directories == [".media"]
    
    def test_is_local_file_url(self):
        """Test is_local property with file:// URL."""
        repo = RepoConfig(
            name="local",
            url="file://../gardenlinux",
            docs_path="docs",
            target_path="projects/gardenlinux",
        )
        assert repo.is_local is True
        assert repo.is_remote is False
    
    def test_is_remote_https_url(self):
        """Test is_remote property with https:// URL."""
        repo = RepoConfig(
            name="remote",
            url="https://github.com/test/repo",
            docs_path="docs",
            target_path="projects/test",
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
            target_path="projects/gardenlinux",
        )
        assert repo.local_path == "../gardenlinux"
    
    def test_validate_local_without_ref(self):
        """Test that local repos don't require ref."""
        repo = RepoConfig(
            name="local",
            url="file://../gardenlinux",
            docs_path="docs",
            target_path="projects/gardenlinux",
        )
        repo.validate()  # Should not raise
    
    def test_validate_remote_requires_ref(self):
        """Test that remote repos must have ref."""
        repo = RepoConfig(
            name="remote",
            url="https://github.com/test/repo",
            docs_path="docs",
            target_path="projects/test",
        )
        with pytest.raises(ValueError, match="must have 'ref' field"):
            repo.validate()
    
    def test_validate_invalid_url_scheme(self):
        """Test that invalid URL schemes are rejected."""
        repo = RepoConfig(
            name="invalid",
            url="ftp://example.com/repo",
            docs_path="docs",
            target_path="projects/test",
        )
        with pytest.raises(ValueError, match="Invalid URL scheme"):
            repo.validate()


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