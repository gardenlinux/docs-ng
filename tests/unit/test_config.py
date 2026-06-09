"""Unit tests for aggregation.config module."""

import json
import tempfile
from pathlib import Path

import pytest
from aggregation import load_config, save_config, RepoConfig


class TestLoadConfig:
    """Tests for load_config function."""
    
    def test_load_valid_config(self, tmp_path):
        """Test loading valid configuration."""
        config_data = {
            "repos": [
                {
                    "name": "test-repo",
                    "url": "https://github.com/test/repo",
                    "docs_path": "docs",
                    "target_path": "projects/test",
                    "ref": "main",
                }
            ]
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))
        
        repos = load_config(str(config_file))
        assert len(repos) == 1
        assert repos[0].name == "test-repo"
        assert repos[0].url == "https://github.com/test/repo"
    
    def test_load_multiple_repos(self, tmp_path):
        """Test loading config with multiple repositories."""
        config_data = {
            "repos": [
                {
                    "name": "repo1",
                    "url": "https://github.com/test/repo1",
                    "docs_path": "docs",
                    "target_path": "projects/repo1",
                    "ref": "main",
                },
                {
                    "name": "repo2",
                    "url": "file://../repo2",
                    "docs_path": "docs",
                    "target_path": "projects/repo2",
                },
            ]
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))
        
        repos = load_config(str(config_file))
        assert len(repos) == 2
        assert repos[0].name == "repo1"
        assert repos[1].name == "repo2"
    
    def test_load_config_with_optional_fields(self, tmp_path):
        """Test loading config with optional fields."""
        config_data = {
            "repos": [
                {
                    "name": "test-repo",
                    "url": "https://github.com/test/repo",
                    "docs_path": "docs",
                    "target_path": "projects/test",
                    "ref": "main",
                    "commit": "abc123",
                    "root_files": ["README.md"],
                    "structure": {"old": "new"},
                }
            ]
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))
        
        repos = load_config(str(config_file))
        assert repos[0].commit == "abc123"
        assert repos[0].root_files == ["README.md"]
        assert repos[0].structure == {"old": "new"}
    
    def test_load_invalid_json(self, tmp_path):
        """Test that invalid JSON causes exit."""
        config_file = tmp_path / "config.json"
        config_file.write_text("{ invalid json")
        
        with pytest.raises(SystemExit):
            load_config(str(config_file))
    
    def test_load_missing_repos_key(self, tmp_path):
        """Test that missing 'repos' key causes exit."""
        config_data = {"other": "data"}
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))
        
        with pytest.raises(SystemExit):
            load_config(str(config_file))


class TestSaveConfig:
    """Tests for save_config function."""
    
    def test_save_single_repo(self, tmp_path):
        """Test saving configuration with single repository."""
        repos = [
            RepoConfig(
                name="test-repo",
                url="https://github.com/test/repo",
                docs_path="docs",
                target_path="projects/test",
                ref="main",
            )
        ]
        config_file = tmp_path / "config.json"
        
        save_config(str(config_file), repos)
        
        # Verify file was created and contains correct data
        assert config_file.exists()
        with open(config_file) as f:
            data = json.load(f)
        
        assert "repos" in data
        assert len(data["repos"]) == 1
        assert data["repos"][0]["name"] == "test-repo"
        assert data["repos"][0]["ref"] == "main"
    
    def test_save_multiple_repos(self, tmp_path):
        """Test saving configuration with multiple repositories."""
        repos = [
            RepoConfig(
                name="repo1",
                url="https://github.com/test/repo1",
                docs_path="docs",
                target_path="projects/repo1",
                ref="main",
            ),
            RepoConfig(
                name="repo2",
                url="file://../repo2",
                docs_path="docs",
                target_path="projects/repo2",
                ref="",
            ),
        ]
        config_file = tmp_path / "config.json"
        
        save_config(str(config_file), repos)
        
        with open(config_file) as f:
            data = json.load(f)
        
        assert len(data["repos"]) == 2
    
    def test_save_with_commit_lock(self, tmp_path):
        """Test saving configuration with commit field."""
        repos = [
            RepoConfig(
                name="test-repo",
                url="https://github.com/test/repo",
                docs_path="docs",
                target_path="projects/test",
                ref="main",
                commit="abc123",
            )
        ]
        config_file = tmp_path / "config.json"
        
        save_config(str(config_file), repos)
        
        with open(config_file) as f:
            data = json.load(f)
        
        assert data["repos"][0]["commit"] == "abc123"
    
    def test_save_omits_empty_optional_fields(self, tmp_path):
        """Test that empty optional fields are omitted."""
        repos = [
            RepoConfig(
                name="test-repo",
                url="https://github.com/test/repo",
                docs_path="docs",
                target_path="projects/test",
                ref="main",
            )
        ]
        config_file = tmp_path / "config.json"
        
        save_config(str(config_file), repos)
        
        with open(config_file) as f:
            data = json.load(f)
        
        # Should not have empty optional fields
        assert "commit" not in data["repos"][0]
        assert "root_files" not in data["repos"][0]
    
    def test_round_trip(self, tmp_path):
        """Test that load/save round-trip preserves data."""
        original_repos = [
            RepoConfig(
                name="test-repo",
                url="https://github.com/test/repo",
                docs_path="docs",
                target_path="projects/test",
                ref="main",
                commit="abc123",
                root_files=["README.md"],
            )
        ]
        config_file = tmp_path / "config.json"
        
        # Save and load
        save_config(str(config_file), original_repos)
        loaded_repos = load_config(str(config_file))
        
        # Compare
        assert len(loaded_repos) == 1
        assert loaded_repos[0].name == original_repos[0].name
        assert loaded_repos[0].url == original_repos[0].url
        assert loaded_repos[0].commit == original_repos[0].commit
        assert loaded_repos[0].root_files == original_repos[0].root_files

    def test_load_config_rejects_invalid_scheme(self, tmp_path):
        """Test that a repo with an invalid URL scheme causes SystemExit via validate()."""
        config_data = {
            "repos": [
                {
                    "name": "bad",
                    "url": "ftp://example.com/repo",
                    "docs_path": "docs",
                    "target_path": "projects/bad",
                    "ref": "main",
                }
            ]
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))

        with pytest.raises(SystemExit):
            load_config(str(config_file))

    def test_save_preserves_structure_dict(self, tmp_path):
        """Test that a dict structure survives a save/load round trip."""
        structure_map = {"old_dir": "new_dir", "another": "different"}
        repos = [
            RepoConfig(
                name="test-repo",
                url="https://github.com/test/repo",
                docs_path="docs",
                target_path="projects/test",
                ref="main",
                structure=structure_map,
            )
        ]
        config_file = tmp_path / "config.json"

        save_config(str(config_file), repos)
        loaded_repos = load_config(str(config_file))

        assert loaded_repos[0].structure == structure_map

    def test_save_omits_default_structure_flat(self, tmp_path):
        """Test that structure='flat' is not written to the JSON output."""
        repos = [
            RepoConfig(
                name="test-repo",
                url="https://github.com/test/repo",
                docs_path="docs",
                target_path="projects/test",
                ref="main",
            )
        ]
        config_file = tmp_path / "config.json"

        save_config(str(config_file), repos)

        with open(config_file) as f:
            data = json.load(f)

        assert "structure" not in data["repos"][0]

    def test_save_preserves_target_map_and_special_files(self, tmp_path):
        """Test that target_map and special_files survive a save/load round trip."""
        repos = [
            RepoConfig(
                name="test-repo",
                url="https://github.com/test/repo",
                docs_path="docs",
                target_path="projects/test",
                ref="main",
                target_map={"src/api.md": "api/index.md"},
                special_files={"CHANGELOG.md": "reference/"},
            )
        ]
        config_file = tmp_path / "config.json"

        save_config(str(config_file), repos)
        loaded_repos = load_config(str(config_file))

        assert loaded_repos[0].target_map == {"src/api.md": "api/index.md"}
        assert loaded_repos[0].special_files == {"CHANGELOG.md": "reference/"}

    def test_save_local_repo_omits_empty_ref(self, tmp_path):
        """Test that local repos with ref='' do not emit a 'ref' key in JSON."""
        repos = [
            RepoConfig(
                name="local-repo",
                url="file://../some-repo",
                docs_path="docs",
                target_path="projects/some-repo",
                ref="",
            )
        ]
        config_file = tmp_path / "config.json"

        save_config(str(config_file), repos)

        with open(config_file) as f:
            data = json.load(f)

        assert "ref" not in data["repos"][0]
