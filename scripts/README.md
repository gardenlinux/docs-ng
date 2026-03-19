# Documentation Aggregation Scripts

This directory contains scripts for aggregating documentation from multiple
Garden Linux repositories into this centralized documentation hub.

## Overview

The aggregation system fetches documentation from source repositories,
transforms them to work with VitePress, and integrates them into the docs hub.

## Architecture

```
Source Repos                    docs-ng (this repo)
┌─────────────┐                ┌──────────────────┐
│ gardenlinux │                │                  │
│   /docs/    │───┐            │  docs/projects/  │
└─────────────┘   │            │  ├─ gardenlinux/ │
                  │            │  ├─ builder/     │
┌─────────────┐   │  Fetch &   │  └─ python-lib/  │
│   builder   │   ├─ Transform │                  │
│   /docs/    │───┤  ─────────>│  VitePress Site  │
└─────────────┘   │            │                  │
                  │            └──────────────────┘
┌─────────────┐   │
│  python-lib │   │
│   /docs/    │───┘
└─────────────┘
```

## Configuration

### repos-config.json

Repository configuration with the following parameters:

- `name`: Repository name
- `url`: Git repository URL
- `docs_path`: Path to docs within the repository
- `target_path`: Where to place docs in this project (relative to docs/)
- `branch`: Git branch to fetch from
- `structure`: Directory structure mapping or copy mode
  - Object with mappings like `{"00_introduction": "introduction"}` for
    structured repos
  - `"flat"` to copy all files as-is
  - `"sphinx"` for Sphinx documentation
- `special_files` (optional): Map of files/directories to move to specific
  locations
  - Example: `{"boot_modes.md": "introduction", "architecture": "introduction"}`
  - Files are moved during transformation, useful for organizing root-level
    content
- `media_directories` (optional): List of directories to copy (including hidden
  directories)
  - Example: `[".media"]`
  - These directories are copied as-is to preserve media assets

### Example Configuration

```json
{
  "name": "gardenlinux",
  "url": "https://github.com/gardenlinux/gardenlinux",
  "docs_path": "docs",
  "target_path": "projects/gardenlinux",
  "branch": "main",
  "structure": {
    "00_introduction": "introduction",
    "01_developers": "developers",
    "02_operators": "operators"
  },
  "special_files": {
    "boot_modes.md": "introduction",
    "architecture": "introduction"
  },
  "media_directories": [".media"]
}
```

## Scripts

### `repos-config.json`

Configuration file defining which repositories to aggregate from.

It also maps the apparent structure of the docs file into their own sections.
This is an example for the docs located in the main Gardenlinux repository.

**Structure:**

```json
{
  "repos": [
    {
      "name": "gardenlinux",
      "url": "https://github.com/gardenlinux/gardenlinux.git",
      "docs_path": "docs",
      "target_path": "projects/gardenlinux",
      "branch": "main",
      "structure": {
        "00_introduction": "introduction",
        "01_developers": "developers",
        "02_operators": "operators"
      }
    }
  ]
}
```

### `fetch-repo-docs.sh`

Fetches documentation from a repository using git sparse checkout.

**Usage:**

```bash
./fetch-repo-docs.sh <repo_url> <branch> <docs_path> <output_dir>
```

**Example:**

```bash
./fetch-repo-docs.sh https://github.com/gardenlinux/gardenlinux.git main docs /tmp/gl-docs
```

### `transform_content.py`

Transforms documentation content to work with VitePress:

- Renames numbered directories (e.g., `00_introduction` → `introduction`)
- Rewrites internal links to work with new structure
- Adds/fixes frontmatter
- Handles different documentation structures

**Usage:**

```bash
./transform_content.py --config repos-config.json \
                       --docs-dir ../docs \
                       --temp-dir /tmp/fetched-docs
```

### `update_config.py`

Generates VitePress sidebar configuration based on aggregated documentation
structure.

**Usage:**

```bash
./update_config.py --config repos-config.json \
                   --docs-dir ../docs \
                   --vitepress-config ../docs/.vitepress/config.mts
```

**Output:** Creates `config.generated.json` with sidebar structure that can be
integrated into VitePress config.

### `aggregate-docs.sh`

Main orchestration script that runs the entire aggregation pipeline.

**Usage:**

```bash
# Aggregate all repositories
./aggregate-docs.sh

# Dry run (don't modify docs directory)
./aggregate-docs.sh --dry-run

# Aggregate specific repository
./aggregate-docs.sh --repo gardenlinux
```

## Makefile Targets

For convenience, use these Makefile targets:

```bash
# Test aggregation without modifying docs/
make aggregate-dry

# Aggregate all repositories
make aggregate

# Aggregate specific repository
make aggregate-repo REPO=gardenlinux

# Clean aggregated docs
make clean-projects
```

## Workflow

1. **Fetch**: Use sparse checkout to clone only the `docs/` directory from
   source repos
2. **Transform**:
   - Restructure directories according to `structure` mapping
   - Rewrite internal links to work with new paths
   - Add frontmatter to markdown files
3. **Update Config**: Generate sidebar configuration for VitePress
4. **Build**: VitePress builds the unified documentation site

## Testing Locally

```bash
# 1. Run dry-run to test without modifying docs/
make aggregate-dry

# 2. If successful, run actual aggregation
make aggregate

# 3. Preview the documentation
make run

# 4. Visit http://localhost:5173 to see aggregated docs
```

## CI/CD Integration

The aggregation runs automatically via GitHub Actions:

- **Schedule**: Daily at 2 AM UTC
- **Manual**: Via workflow dispatch in GitHub UI
- **Webhook**: Can be triggered by source repositories

See `.github/workflows/aggregate-docs.yml` for details.

## Adding New Repositories

1. Add repository configuration to `repos-config.json`:

```json
{
  "name": "new-repo",
  "url": "https://github.com/gardenlinux/new-repo.git",
  "docs_path": "docs",
  "target_path": "projects/new-repo",
  "branch": "main",
  "structure": "flat"
}
```

> [!IMPORTANT]
> When the `docs/` directory contains subdirectories, mirror this structure in
> the `repos-config.json`.

```json
{
  "name": "new-repo",
  "url": "https://github.com/gardenlinux/new-repo.git",
  "docs_path": "docs",
  "target_path": "projects/new-repo",
  "branch": "main",
  "structure": {
    "00_introduction": "introduction",
    "01_developers": "developers",
    "02_operators": "operators"
  }
}
```

2. Test aggregation:

```bash
make aggregate-repo REPO=new-repo
```

3. Verify in development server:

```bash
make run
```

## Testsuite

Run the test suite before making changes:

```bash
cd scripts/tests
./run_all.sh
```

See `tests/README.md` for more details.

## Troubleshooting

### Links are broken after aggregation

- Check the `rewrite_links()` function in `transform-content.py`
- Verify link patterns in source documentation
- Test with: `make aggregate-dry`

### Directory structure not matching

- Review `structure` configuration in `repos-config.json`
- Check `transform_directory_structure()` in `transform-content.py`

### Sidebar not generating correctly

- Check output in `docs/.vitepress/config.generated.json`
- Verify markdown files have proper titles/frontmatter
- Review `scan_directory_structure()` in `update-config.py`

### Fetch failing

- Verify repository URL and branch in `repos-config.json`
- Check network connectivity
- Ensure sparse checkout is working: `git config core.sparseCheckout true`

## Notes

- **Local repos**: If testing with local repos, you can use `file://` URLs in
  config
- **Authentication**: For private repos, ensure GitHub token has appropriate
  permissions
- **Large docs**: To keep fetching sizes small, the sparse checkout only fetches
  `docs/`. Any additional documentation should be comitted here directly.
