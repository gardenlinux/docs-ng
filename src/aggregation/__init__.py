"""Aggregation package for docs documentation aggregation."""

# Re-export commonly used functions for backward compatibility with tests
from .config import load_config, save_config
from .fetcher import DocsFetcher
from .flavor_matrix import generate_flavor_matrix_docs
from .models import AggregateResult, RepoConfig
from .releases import generate_release_docs
from .sphinx_builder import build_sphinx_markdown
from .structure import (copy_targeted_docs, process_all_markdown,
                        verify_internal_links)
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
    "copy_targeted_docs",
    "process_all_markdown",
    "verify_internal_links",
    # Releases
    "generate_release_docs",
    # Flavor Matrix
    "generate_flavor_matrix_docs",
    # Sphinx builder
    "build_sphinx_markdown",
]
