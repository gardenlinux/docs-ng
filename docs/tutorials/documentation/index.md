---
title: "Contributing to the Garden Linux Documentation"
description: "Learn how to contribute to Garden Linux documentation — from quick edits to working with the aggregation system locally"
---

# Contributing to the Garden Linux Documentation

Garden Linux documentation is published at **https://gardenlinux-docs.netlify.app/** and combines content from multiple repositories into a unified documentation site.

> **Source Repository:** [gardenlinux/docs-ng](https://github.com/gardenlinux/docs-ng)

## Quick Edits — The Easy Way

The easiest way to improve the documentation is directly from the published site:

1. **Navigate to any page** on https://gardenlinux-docs.netlify.app/
2. **Scroll to the bottom** of the page
3. **Click "Edit this page on GitHub"** — this opens the source file in the correct repository
4. **Make your edits** using GitHub's web editor
5. **Submit a pull request** — the changes will be automatically aggregated into the documentation site

### Why This Works

The "Edit this page on GitHub" button is intelligent and takes you to the correct source location:

- For content from the **main gardenlinux repository**, it links to `gardenlinux/gardenlinux/docs/...`
- For content from the **builder repository**, it links to `gardenlinux/builder/docs/...`
- For content from the **python-gardenlinux-lib repository**, it links to `gardenlinux/python-gardenlinux-lib/docs/...`
- For documentation-specific pages, it links to `gardenlinux/docs-ng/docs/...`

**You don't need to understand the aggregation system to contribute!** The system automatically detects changes in source repositories and rebuilds the unified documentation site.

This works because the VitePress configuration uses frontmatter metadata (`github_org`, `github_repo`, `github_source_path`, `github_branch`) embedded in each page to resolve the correct source location.

This approach is perfect for:

- Fixing typos
- Clarifying explanations
- Adding missing information
- Updating outdated content

## Documentation Aggregation System

The documentation aggregation system powers the unified Garden Linux documentation site. It aggregates content from multiple source repositories (gardenlinux, builder, python-gardenlinux-lib) into a cohesive VitePress site.

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

### Architecture Overview

```
Source Repos → Fetch (git/local) → Transform → docs/ → VitePress
```

The aggregation pipeline consists of four main stages:

1. **Fetch** — `src/aggregation/fetcher.py` pulls docs via git sparse checkout or local copy
2. **Transform** — `src/aggregation/transformer.py` rewrites links, fixes frontmatter
3. **Structure** — `src/aggregation/structure.py` reorganizes directories and copies media
4. **Output** — VitePress builds the site

### Working with the Documentation System Locally

For more substantial changes — like adding new pages, restructuring content, or working on the aggregation system itself — you'll want to set up the documentation system locally.

#### Prerequisites

- Python 3.x
- pnpm (for VitePress)
- Git

#### Step 1: Clone the Repository

```bash
git clone https://github.com/gardenlinux/docs-ng.git
cd docs-ng
```

#### Step 2: Install Dependencies

```bash
pnpm install
```

This installs VitePress and other Node.js dependencies needed to build the documentation site.

#### Step 3: Aggregate Documentation

##### From Remote Repositories (Production)

Aggregate from locked commits in `repos-config.json`:

```bash
make aggregate
```

This fetches documentation from the configured repositories at their locked commit hashes.

##### From Local Repositories (Development)

For local development, use `repos-config.local.json` with `file://` URLs:

```bash
make aggregate-local
```

This copies documentation from local repositories without using git.

#### Step 4: Start the Development Server

```bash
make dev
```

The documentation site will be available at `http://localhost:5173`.

#### Step 5: Make Changes

As you work on documentation in source repositories:

1. Make changes to markdown files in source repos
2. Run `make aggregate-local` to update the aggregated docs
3. The dev server will hot-reload automatically

#### Step 6: Build for Production

When ready to deploy:

```bash
make build
```

This creates a production build in `docs/.vitepress/dist/`.

### Common Workflows

#### Updating a Single Repository

```bash
make aggregate-repo REPO=gardenlinux
```

#### Updating Lock Files

To fetch the latest commits and update `repos-config.json`:

```bash
make aggregate-update
```

#### Running Tests

```bash
make test
```

### Project Structure

#### Repository Structure (docs-ng)

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

#### After Aggregation

After running the aggregation, your docs directory will look like:

```
docs/
├── projects/              # Mirrored repository docs
│   ├── gardenlinux/
│   ├── builder/
│   └── python-gardenlinux-lib/
├── tutorials/             # Aggregated tutorials
├── how-to/                # Aggregated guides
├── explanation/           # Aggregated explanations
├── reference/             # Aggregated reference
└── contributing/          # Aggregated contributing docs
```

### Troubleshooting

#### Clean Build

If you encounter issues, try a clean build:

```bash
make clean
make aggregate
make dev
```

#### Check Dependencies

Ensure all dependencies are installed:

```bash
pnpm install
python3 --version  # Should be 3.x
```

#### Verify Configuration

Check that `repos-config.json` or `repos-config.local.json` is properly configured. See the [configuration reference](../../reference/documentation/configuration.md) for details.

## Next Steps

- [Adding Repositories](../../how-to/documentation/adding-repos.md) — How to add new repositories to the aggregation
- [Technical Reference](../../reference/documentation/technical.md) — Source code and API documentation
- [Configuration Reference](../../reference/documentation/configuration.md) — Complete configuration options
- [Architecture Explanation](../../explanation/documentation/aggregation-architecture.md) — Deep dive into how the documentation aggregation system works
