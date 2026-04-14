---
title: "Documentation Aggregation Technical Reference"
description: "Source code documentation for the documentation aggregation system - modules, APIs, and implementation details"
---

# Documentation Aggregation Technical Reference

Source code documentation for the documentation aggregation system.

> **Source Repository:**
> [gardenlinux/docs-ng](https://github.com/gardenlinux/docs-ng) > **Source
> File:**
> [src/README.md](https://github.com/gardenlinux/docs-ng/blob/main/src/README.md)

## Source Code Structure

```
src/
├── aggregate.py          # CLI entry point
├── migration_tracker.py  # Standalone utility
└── aggregation/          # Core package
    ├── __init__.py
    ├── models.py         # Data classes
    ├── config.py         # Config I/O
    ├── fetcher.py        # Git + local fetch
    ├── transformer.py    # Content transforms
    └── structure.py      # Directory transforms
```

## Module Reference

### `aggregation/models.py`

Data classes for type safety:

- **`RepoConfig`** — Repository configuration data class
- **`AggregateResult`** — Fetch result with commit hash

### `aggregation/config.py`

Configuration file handling:

- **`load_config()`** — Parse repos-config.json
- **`save_config()`** — Write updated config (commit locks)

### `aggregation/fetcher.py`

Repository fetching:

**`DocsFetcher`** — Main fetcher class

Methods:

- **`__init__(project_root, update_locks=False)`** — Initialize with optional
  commit lock updating
- **`fetch()`** — Fetch repository and return result with commit hash
- **`_fetch_remote()`** — Git sparse checkout from remote repository
- **`_fetch_local()`** — Filesystem copy from local repository
- **`_copy_docs()`** — Static method to copy docs directory
- **`_copy_root_files()`** — Static method to copy root-level files (e.g.,
  CONTRIBUTING.md)

### `aggregation/transformer.py`

Content transformation:

- **`rewrite_links()`** — Fix markdown links for cross-repository references
- **`quote_yaml_value()`** — YAML safety for front-matter values
- **`ensure_frontmatter()`** — Add or fix front-matter in markdown files
- **`parse_frontmatter()`** — Extract metadata from markdown front-matter
- **`fix_broken_project_links()`** — Validate and fix links to project mirrors

### `aggregation/structure.py`

Directory operations:

- **`transform_directory_structure()`** — Restructure docs based on config
  mapping
- **`copy_targeted_docs(source_dir, docs_dir, repo_name, media_dirs=None, root_files=None)`**
  — Copy files with `github_target_path` front-matter to specified locations
  - Handles nested media dirs (e.g., `tutorials/assets/`) by copying to same
    relative path
  - Handles root-level media dirs (e.g., `_static/`) by copying to common
    ancestor of targeted files
  - Supports scanning root_files for targeted placement
- **`process_markdown_file()`** — Transform single markdown file (links,
  front-matter)
- **`process_all_markdown()`** — Batch process all markdown files in directory

### `aggregate.py`

CLI orchestration — Combines all modules into the complete aggregation workflow.

## Usage Example

Basic programmatic usage:

```python
from aggregation import load_config, DocsFetcher, process_all_markdown

# Load configuration
repos = load_config("repos-config.json")

# Initialize fetcher
fetcher = DocsFetcher(project_root)

# Fetch documentation
result = fetcher.fetch(repo, output_dir)

# Transform markdown files
process_all_markdown(target_dir, repo_name)
```

## Key Concepts

### Targeted Documentation

Files with `github_target_path` in their front-matter are automatically placed
at that exact path:

```yaml
---
github_target_path: "docs/tutorials/example.md"
---
```

The `copy_targeted_docs()` function scans all markdown files and copies those
with this front-matter to their specified locations.

### Link Rewriting

The `rewrite_links()` function transforms markdown links to work in the
aggregated site:

- Relative links within the same repo are maintained
- Cross-repository links are rewritten to point to the correct locations
- Links to project mirrors are validated

### Media Handling

Media directories specified in `media_directories` configuration are:

1. Discovered recursively in the source repository
2. Copied alongside their associated documentation
3. Placed according to whether they're nested (same relative path) or root-level
   (common ancestor)

### Commit Locking

When `update_locks=True` is passed to `DocsFetcher.__init__()`, the system:

1. Fetches from the `ref` (branch/tag)
2. Records the resolved commit hash
3. Updates `repos-config.json` with the lock

This ensures reproducible builds.

## Development

### Running Tests

See [Testing Reference](./testing.md) for details on the test suite.

### Adding New Transformation

To add a new transformation:

1. Add function to `transformer.py`
2. Call it from `process_markdown_file()` or `process_all_markdown()`
3. Add tests in `tests/unit/test_transformer.py`

### Adding New Structure Type

To add a new structure mapping type:

1. Update `transform_directory_structure()` in `structure.py`
2. Add corresponding structure key handling
3. Update configuration documentation

## Architecture Decisions

Key architectural decisions are documented in the source repository:

- Sparse git checkout for efficiency
- Front-matter-based targeting for flexibility
- Separate fetch/transform/structure stages for modularity

## See Also

- [Documentation Workflow](./documentation_workflow.md)
- [Documentation Quality Markers](./writing_good_docs.md)
- [Documentation Aggregator Architecture](./aggregation-architecture.md)
- [How to Documentation - Adding Repos to Aggregate](./adding-repos.md)
- [How to Documentation - Working With the Aggregator Locally](./working-locally.md)
- [Documentation Aggregator Technical Reference](./technical.md)
- [Documentation Aggregator Local Testing Guide](./testing.md)
- [Working with the Documentation Hub on Your Machine](./working-locally.md)
