---
title: "Getting Started with docs-ng"
description: "Step-by-step tutorial for setting up and using the docs-ng documentation aggregation system"
github_org: gardenlinux
github_repo: docs-ng
github_source_path: docs/reference/supporting_tools/docs-ng/tutorials/getting_started.md
---

# Getting Started with docs-ng

This tutorial will walk you through setting up and using docs-ng to aggregate documentation from multiple repositories.

> **Source Repository:** [gardenlinux/docs-ng](https://github.com/gardenlinux/docs-ng)

## Prerequisites

- Python 3.x
- pnpm (for VitePress)
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/gardenlinux/docs-ng.git
cd docs-ng
```

## Step 2: Install Dependencies

```bash
pnpm install
```

This installs VitePress and other Node.js dependencies needed to build the documentation site.

## Step 3: Aggregate Documentation

### From Remote Repositories (Production)

Aggregate from locked commits in `repos-config.json`:

```bash
make aggregate
```

This fetches documentation from the configured repositories at their locked commit hashes.

### From Local Repositories (Development)

For local development, use `repos-config.local.json` with `file://` URLs:

```bash
make aggregate-local
```

This copies documentation from local repositories without using git.

## Step 4: Start the Development Server

```bash
make dev
```

The documentation site will be available at `http://localhost:5173`.

## Step 5: Make Changes

As you work on documentation in source repositories:

1. Make changes to markdown files in source repos
2. Run `make aggregate-local` to update the aggregated docs
3. The dev server will hot-reload automatically

## Step 6: Build for Production

When ready to deploy:

```bash
make build
```

This creates a production build in `docs/.vitepress/dist/`.

## Common Workflows

### Updating a Single Repository

```bash
make aggregate-repo REPO=gardenlinux
```

### Updating Lock Files

To fetch the latest commits and update `repos-config.json`:

```bash
make aggregate-update
```

### Running Tests

```bash
make test
```

## Project Structure

After aggregation, your docs directory will look like:

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

## Next Steps

- Learn how to [add new repositories](/reference/supporting_tools/docs-ng/how-to/adding-repos)
- Understand the [architecture](/reference/supporting_tools/docs-ng/explanation/architecture)
- Review the [configuration reference](/reference/supporting_tools/docs-ng/reference/configuration)

## Troubleshooting

### Clean Build

If you encounter issues, try a clean build:

```bash
make clean
make aggregate
make dev
```

### Check Dependencies

Ensure all dependencies are installed:

```bash
pnpm install
python3 --version  # Should be 3.x
```

### Verify Configuration

Check that `repos-config.json` or `repos-config.local.json` is properly configured. See the [configuration reference](/reference/supporting_tools/docs-ng/reference/configuration) for details.
