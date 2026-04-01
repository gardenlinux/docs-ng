---
title: "docs-ng Documentation Hub"
description: "Documentation aggregation system for Garden Linux - combines docs from multiple repositories into a unified VitePress site"
github_org: gardenlinux
github_repo: docs-ng
github_source_path: docs/reference/supporting_tools/docs-ng/overview/index.md
---

# docs-ng: Garden Linux Documentation Hub

Build unified documentation from multiple Garden Linux repositories.

> **Source Repository:** [gardenlinux/docs-ng](https://github.com/gardenlinux/docs-ng)

## Overview

docs-ng is the documentation aggregation system that powers the unified Garden Linux documentation site. It aggregates content from multiple source repositories (gardenlinux, builder, python-gardenlinux-lib) into a cohesive VitePress site.

### Key Features

- **Targeted Documentation**: Files with `github_target_path` frontmatter are automatically placed into the correct Diataxis categories
- **Project Mirroring**: Complete repository documentation mirrored under `docs/projects/<repo-name>/`
- **Commit Locking**: Reproducible builds with locked commit hashes
- **Media Handling**: Automatic discovery and copying of media directories
- **Link Rewriting**: Automatic link transformation for cross-repository references

### Documentation Paths

The system supports two complementary documentation paths:

1. **Targeted Documentation** — Files with `github_target_path` frontmatter → `docs/tutorials/`, `docs/how-to/`, etc.
2. **Project Mirror** — All repo docs mirrored under `docs/projects/<repo-name>/`

## Quick Start

```bash
# Aggregate documentation from repos
make aggregate

# Run development server
make dev

# Build production site
make build
```

## Architecture Overview

```
Source Repos → Fetch (git/local) → Transform → docs/ → VitePress
```

The aggregation pipeline consists of four main stages:

1. **Fetch** — `src/aggregation/fetcher.py` pulls docs via git sparse checkout or local copy
2. **Transform** — `src/aggregation/transformer.py` rewrites links, fixes frontmatter
3. **Structure** — `src/aggregation/structure.py` reorganizes directories and copies media
4. **Output** — VitePress builds the site

## Project Structure

```
docs-ng/
├── repos-config.json         # Repository configuration
├── repos-config.local.json   # Local development config
├── src/                      # Source code
│   ├── aggregate.py          # CLI entry point
│   └── aggregation/          # Core package
├── tests/                    # Test suite
└── docs/                     # Generated documentation
    ├── projects/             # Mirrored repository docs
    ├── tutorials/            # Aggregated tutorials
    ├── how-to/               # Aggregated guides
    ├── explanation/          # Aggregated explanations
    └── reference/            # Aggregated reference docs
```

## Further Reading

- [Getting Started Tutorial](/reference/supporting_tools/docs-ng/tutorials/getting_started) — Step-by-step guide to using docs-ng
- [Adding Repositories](/reference/supporting_tools/docs-ng/how-to/adding-repos) — How to add new repositories to the aggregation
- [Technical Reference](/reference/supporting_tools/docs-ng/reference/technical) — Source code and API documentation
- [Configuration Reference](/reference/supporting_tools/docs-ng/reference/configuration) — Complete configuration options
- [Architecture Explanation](/reference/supporting_tools/docs-ng/explanation/architecture) — Deep dive into how docs-ng works

## Contributing

See the [docs-ng repository](https://github.com/gardenlinux/docs-ng) for contribution guidelines.
