# Garden Linux Documentation Hub

Build unified documentation from multiple Garden Linux repositories.

## Quick Start

```bash
# Aggregate documentation from repos
make aggregate

# Run development server
make dev
```

## Overview

This project aggregates content from multiple source repositories (gardenlinux, builder, python-gardenlinux-lib) into a cohesive VitePress site.

### Documentation Paths

1. **Targeted Documentation** — Files with `github_target_path` frontmatter → `docs/tutorials/`, `docs/how-to/`, etc.
2. **Project Mirror** — All repo docs mirrored under `docs/projects/<repo-name>/`

## Architecture

```
Source Repos → Fetch (git/local) → Transform → docs/ → VitePress
```

**Aggregation Pipeline:**

1. **Fetch** — `src/aggregation/fetcher.py` pulls docs via git sparse checkout or local copy
2. **Transform** — `src/aggregation/transformer.py` rewrites links, fixes frontmatter
3. **Structure** — `src/aggregation/structure.py` reorganizes directories and copies media
4. **Output** — VitePress builds the site

**Key Mechanisms:**

- **Targeted Documentation**: Files with `github_target_path` frontmatter are copied directly to specified paths (e.g., `docs/tutorials/cloud/first-boot-aws.md`). This is the primary mechanism for aggregating content from source repos into the unified documentation structure.
  
- **Media Directories**: Directories listed in `media_directories` (e.g., `_static`, `assets`) are automatically discovered and copied. For nested media dirs (like `tutorials/assets`), they're copied to the same relative path. For root-level media dirs (like `_static`), they're copied to the common ancestor of all targeted files.

- **Commit Locking**: The `commit` field in `repos-config.json` locks to a specific commit for reproducibility. Use `make aggregate-update` to fetch the latest commits and update the locks automatically.

- **Project Mirror**: In addition to targeted docs, the entire `docs/` directory from each repo is mirrored under `docs/projects/<repo-name>/` for reference.

## Configuration

### repos-config.json

Located at project root. Defines repositories to aggregate:

```json
{
  "repos": [
    {
      "name": "gardenlinux",
      "url": "https://github.com/gardenlinux/gardenlinux",
      "docs_path": "docs",
      "target_path": "projects/gardenlinux",
      "ref": "docs-ng",
      "commit": "abc123...",
      "root_files": ["CONTRIBUTING.md", "SECURITY.md"],
      "structure": {
        "tutorials": "tutorials",
        "how-to": "how-to",
        "explanation": "explanation",
        "reference": "reference"
      },
      "media_directories": [".media", "assets", "_static"]
    },
    {
      "name": "python-gardenlinux-lib",
      "url": "https://github.com/gardenlinux/python-gardenlinux-lib",
      "docs_path": "docs",
      "target_path": "projects/python-gardenlinux-lib",
      "ref": "docs-ng",
      "commit": "def456...",
      "structure": "sphinx",
      "media_directories": ["_static"]
    }
  ]
}
```

**Key fields:**

- `ref` — branch/tag to fetch
- `commit` — (optional) commit lock for reproducibility; use `--update-locks` to update
- `root_files` — (optional) root-level files to copy (e.g., CONTRIBUTING.md)
- `structure` — directory mapping, `"flat"` for as-is copy, or `"sphinx"` for Sphinx docs
- `media_directories` — (optional) list of media directories to copy (relative paths searched recursively)

For local testing, use `repos-config.local.json` with `file://` URLs.

## Commands

### Development

```bash
make dev              # Start dev server
make build            # Production build
make preview          # Preview production build
```

### Testing

```bash
make test             # Run all tests
make test-unit        # Unit tests
make test-integration # Integration tests
```

### Aggregation

```bash
make aggregate-local                # From local repos (file://)
make aggregate                      # From remote repos (locked commits)
make aggregate-repo REPO=...        # Single repository
make aggregate-update               # Fetch latest + update commit locks
make aggregate-update-repo REPO=... # Single repository
```

### Utilities

```bash
make clean            # Clean build artifacts and aggregated docs
```

## Project Structure

```
docs-ng/
├── repos-config.json         # Repository configuration
├── repos-config.local.json   # Local development config
├── src/                      # Source code
│   ├── aggregate.py          # CLI entry point
│   ├── aggregation/          # Core package
│   │   ├── models.py         # Data classes
│   │   ├── config.py         # Config I/O
│   │   ├── fetcher.py        # Repository fetching
│   │   ├── transformer.py    # Content transformation
│   │   └── structure.py      # Directory operations
│   └── README.md             # Technical documentation
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests (pure functions)
│   ├── integration/          # Integration tests (filesystem)
│   └── README.md             # Test documentation
└── docs/                     # Generated documentation
    ├── projects/             # Mirrored repository docs
    ├── tutorials/            # Aggregated tutorials (via github_target_path)
    ├── how-to/               # Aggregated guides (via github_target_path)
    ├── explanation/          # Aggregated explanations (via github_target_path)
    ├── reference/            # Aggregated reference docs (via github_target_path)
    │   └── supporting_tools/ # Builder, python-gardenlinux-lib docs
    └── contributing/         # Aggregated contributing docs (via github_target_path)
```

## Adding Repositories

1. Add to `repos-config.json`:

```json
{
  "name": "new-repo",
  "url": "https://github.com/gardenlinux/new-repo",
  "docs_path": "docs",
  "target_path": "projects/new-repo",
  "ref": "main",
  "structure": "flat"
}
```

2. Test: `make aggregate-repo REPO=new-repo`
3. Preview: `make dev`

## Documentation

- **User Guide**: This README
- **Technical Docs**: `src/README.md`
- **Test Docs**: `tests/README.md`

## Contributing

See `CONTRIBUTING.md` for development guidelines.
