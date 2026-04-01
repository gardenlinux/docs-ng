"""Data models for documentation aggregation."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class RepoConfig:
    """Configuration for a single repository."""
    
    name: str
    url: str
    docs_path: str
    target_path: str
    ref: Optional[str] = None
    commit: Optional[str] = None
    root_files: List[str] = field(default_factory=list)
    structure: Union[str, Dict[str, str]] = "flat"
    special_files: Dict[str, str] = field(default_factory=dict)
    media_directories: List[str] = field(default_factory=list)
    
    @property
    def is_local(self) -> bool:
        """Check if this is a local file:// repository."""
        return self.url.startswith("file://")
    
    @property
    def is_remote(self) -> bool:
        """Check if this is a remote https:// repository."""
        return self.url.startswith("https://")
    
    @property
    def local_path(self) -> str:
        """Get local path by stripping file:// prefix."""
        return self.url[7:] if self.is_local else ""
    
    def validate(self) -> None:
        """Validate repository configuration."""
        if not (self.is_local or self.is_remote):
            raise ValueError(f"Invalid URL scheme for {self.name}: {self.url}")
        
        if self.is_remote and not self.ref:
            raise ValueError(f"Remote repository {self.name} must have 'ref' field")
    
    @classmethod
    def from_dict(cls, data: Dict) -> "RepoConfig":
        """Create RepoConfig from dictionary."""
        return cls(
            name=data["name"],
            url=data["url"],
            docs_path=data["docs_path"],
            target_path=data["target_path"],
            ref=data.get("ref"),
            commit=data.get("commit"),
            root_files=data.get("root_files", []),
            structure=data.get("structure", "flat"),
            special_files=data.get("special_files", {}),
            media_directories=data.get("media_directories", []),
        )


@dataclass
class AggregateResult:
    """Result of aggregating a single repository."""
    
    repo_name: str
    success: bool
    resolved_commit: Optional[str] = None