"""Aggregation package for docs-ng documentation aggregation."""

# Re-export commonly used functions for backward compatibility with tests
from .config import load_config, save_config
from .fetcher import DocsFetcher
from .flavor_matrix import generate_flavor_matrix_docs
from .models import AggregateResult, RepoConfig
from .releases import generate_release_docs
from .structure import (copy_targeted_docs, process_all_markdown,
                        transform_directory_structure)
from .transformer import (ensure_frontmatter, parse_frontmatter,
                          quote_yaml_value, rewrite_links)

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
    # Flavor Matrix
    "generate_flavor_matrix_docs",
]
