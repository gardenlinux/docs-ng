---
title: "Contributing to the Garden Linux Documentation"
description: "Learn how to contribute to Garden Linux documentation — working with the aggregation system locally"
---

# Contributing to the Garden Linux Documentation

Garden Linux documentation is published at
**https://gardenlinux-docs.netlify.app/** and combines content from multiple
repositories into a unified documentation site.

> **Source Repository:**
> [gardenlinux/docs-ng](https://github.com/gardenlinux/docs-ng)

## Working with the Documentation System Locally

For more substantial changes — like adding new pages, restructuring content, or
working on the aggregation system itself — you'll want to set up the
documentation system locally.

### Prerequisites

- Python 3.x
- pnpm (for VitePress)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/gardenlinux/docs-ng.git
cd docs-ng
```

### Step 2: Install Dependencies

```bash
pnpm install
```

This installs VitePress and other Node.js dependencies needed to build the
documentation site.

### Step 3: Aggregate Documentation

#### From Remote Repositories (Production)

Aggregate from locked commits in `repos-config.json`:

```bash
make aggregate
```

This fetches documentation from the configured repositories at their locked
commit hashes.

#### From Local Repositories (Development)

For local development, use `repos-config.local.json` with `file://` URLs:

```bash
make aggregate-local
```

This copies documentation from local repositories without using git.

### Step 4: Start the Development Server

```bash
make dev
```

The documentation site will be available at `http://localhost:5173`.

### Step 5: Make Changes

As you work on documentation in source repositories:

1. Make changes to markdown files in source repos
2. Run `make aggregate-local` to update the aggregated docs
3. The dev server will hot-reload automatically

### Step 6: Build for Production

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

- Learn how to [add new repositories](adding-repos.md)
- Understand the [architecture](./aggregation-architecture.md)
- Review the [configuration reference](./configuration.md)

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

Check that `repos-config.json` or `repos-config.local.json` is properly
configured. See the [configuration reference](./configuration.md) for details.

## See Also

- [Documentation Workflow](./documentation_workflow.md)
- [Documentation Quality Markers](./writing_good_docs.md)
- [Documentation Aggregator Architecture](./aggregation-architecture.md)
- [How to Documentation - Adding Repos to Aggregate](./adding-repos.md)
- [How to Documentation - Working With the Aggregator Locally](./working-locally.md)
- [Documentation Aggregator Technical Reference](./technical.md)
- [Documentation Aggregator Local Testing Guide](./testing.md)
- [Working with the Documentation Hub on Your Machine](./working-locally.md)
