"""Aggregation package for docs-ng documentation aggregation."""

# Re-export commonly used functions for backward compatibility with tests
from .transformer import (
    rewrite_links,
    ensure_frontmatter,
    quote_yaml_value,
    parse_frontmatter,
)

from .models import RepoConfig, AggregateResult
from .config import load_config, save_config
from .fetcher import DocsFetcher
from .structure import (
    transform_directory_structure,
    copy_targeted_docs,
    process_all_markdown,
)
from .releases import generate_release_docs

__all__ = [
    # Models
    "RepoConfig",
    "AggregateResult",
    # Config
    "load_config",
    "save_config",
    # Fetcher
    "DocsFetcher",
    # Transformer (for tests)
    "rewrite_links",
    "ensure_frontmatter",
    "quote_yaml_value",
    "parse_frontmatter",
    # Structure
    "transform_directory_structure",
    "copy_targeted_docs",
    "process_all_markdown",
    # Releases
    "generate_release_docs",
]