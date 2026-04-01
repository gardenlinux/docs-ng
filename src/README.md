# Source Code Documentation

## Structure

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

## Modules

### `aggregation/models.py`
Data classes for type safety:
- `RepoConfig` — repository configuration
- `AggregateResult` — fetch result with commit hash

### `aggregation/config.py`
Configuration file handling:
- `load_config()` — parse repos-config.json
- `save_config()` — write updated config (commit locks)

### `aggregation/fetcher.py`
Repository fetching:
- `DocsFetcher` — main class
  - `__init__(project_root, update_locks=False)` — initialize with optional commit lock updating
  - `fetch()` — fetch repository and return result with commit hash
  - `_fetch_remote()` — git sparse checkout from remote repository
  - `_fetch_local()` — filesystem copy from local repository
  - `_copy_docs()` — static method to copy docs directory
  - `_copy_root_files()` — static method to copy root-level files (e.g., CONTRIBUTING.md)

### `aggregation/transformer.py`
Content transformation:
- `rewrite_links()` — fix markdown links
- `quote_yaml_value()` — YAML safety
- `ensure_frontmatter()` — add/fix frontmatter
- `parse_frontmatter()` — extract metadata
- `fix_broken_project_links()` — validate links

### `aggregation/structure.py`
Directory operations:
- `transform_directory_structure()` — restructure docs based on config
- `copy_targeted_docs(source_dir, docs_dir, repo_name, media_dirs=None)` — place files via `github_target_path` frontmatter and copy associated media directories
  - Handles nested media dirs (e.g., `tutorials/assets/`) by copying to same relative path
  - Handles root-level media dirs (e.g., `_static/`) by copying to common ancestor of targeted files
- `process_markdown_file()` — transform single markdown file
- `process_all_markdown()` — batch process all markdown files in directory

### `aggregate.py`
CLI orchestration — combines all modules into workflow.

## Usage

```python
from aggregation import load_config, DocsFetcher, process_all_markdown

# Load config
repos = load_config("repos-config.json")

# Fetch docs
fetcher = DocsFetcher(project_root)
result = fetcher.fetch(repo, output_dir)

# Transform
process_all_markdown(target_dir, repo_name)