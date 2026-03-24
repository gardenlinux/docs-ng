# docs-ng

Build the Garden Linux documentation with aggregated content from multiple repositories.

## Overview

This project provides a unified documentation hub for Garden Linux that aggregates content from multiple source repositories (gardenlinux, builder, python-gardenlinux-lib) and presents it in a cohesive VitePress site.

### Documentation Structure

The system uses a **dual-path approach** for documentation:

1. **Targeted Documentation** — Files with `github_target_path` frontmatter are copied to specific locations in the main docs tree (e.g., `docs/tutorials/`, `docs/how-to/`)
2. **Project Mirror** — All repository documentation is also mirrored under `docs/projects/<repo-name>/` for legacy access and comprehensive coverage

## Quick Start

```bash
# Run development server
make run

# Aggregate documentation from repos
make aggregate

# Run tests
make test
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Source Repositories                       │
│  (gardenlinux, builder, python-gardenlinux-lib)             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ 1. Fetch (sparse checkout)
                      │    scripts/fetch-repo-docs.sh
                      ▼
              ┌───────────────┐
              │  Temp Storage │
              └───────┬───────┘
                      │
                      │ 2. Transform
                      │    scripts/transform_content.py
                      │    • Targeted doc placement (github_target_path)
                      │    • Directory restructuring
                      │    • Link rewriting
                      │    • Frontmatter YAML fixing
                      ▼
              ┌───────────────────────────────────┐
              │      docs/ directory              │
              │  ├── tutorials/                   │
              │  ├── how-to/                      │
              │  ├── explanation/                 │
              │  ├── reference/                   │
              │  ├── contributing/                │
              │  └── projects/                    │
              │      ├── gardenlinux/             │
              │      ├── builder/                 │
              │      └── python-gardenlinux-lib/  │
              └───────────────────────────────────┘
                      │
                      │ VitePress builds the site
                      │ using vitepress-sidebar
                      ▼
              ┌───────────────────────────┐
              │   VitePress Site          │
              │   (Development/Production)│
              └───────────────────────────┘
```

## Documentation Aggregation

The documentation aggregation system pulls content from multiple Git repositories and transforms it for VitePress. The process consists of two main steps orchestrated by `scripts/aggregate-docs.sh`:

### Step 1: Fetch Documentation

**Script:** `scripts/fetch-repo-docs.sh`

Uses sparse Git checkout to efficiently fetch only the documentation directories from source repositories. This minimizes clone size and speeds up the process.

**Configuration:** `scripts/repos-config.json`

Each repository is defined with:

- `name` — Repository identifier
- `url` — Git repository URL
- `branch` — Branch to fetch from
- `docs_path` — Path to documentation within the repo (e.g., `docs`)
- `target_path` — Where to place docs in the aggregated site (e.g., `projects/gardenlinux`)
- `github_org` / `github_repo` — Used for "Edit on GitHub" links
- `structure` — How to transform the directory structure (see below)

**Structure Types:**

- `flat` — Copy files as-is without transformation
- `sphinx` — Copy Sphinx documentation structure (RST files)
- `{ "dir1": "newdir1", "dir2": "newdir2" }` — Map source directories to target directories (e.g., `{ "tutorials": "tutorials", "how-to": "how-to" }`)

### Step 2: Transform Content

**Script:** `scripts/transform_content.py`

Performs multiple transformations on the fetched documentation:

#### 2a. Targeted Documentation Placement

Files with `github_target_path` frontmatter are copied to their specified locations in the main docs tree. This allows documentation from source repos to be integrated directly into the primary documentation structure.

Example frontmatter:

```yaml
---
title: "Tutorials"
github_target_path: "docs/tutorials/index.md"
---
```

This file would be copied to `docs/tutorials/index.md` in addition to being mirrored in `docs/projects/`.

#### 2b. Directory Structure Transformation

Transforms the fetched documentation according to the `structure` configuration:

- Renames numbered directories (e.g., `00_introduction` → `introduction`)
- Applies custom directory mappings
- Handles special files and media directories

#### 2c. Link Rewriting

Converts repository-relative links to work in the aggregated site:

- `[link](../01_developers/build.md)` → `[link](/projects/gardenlinux/developers/build)`
- `[link](./intro.md)` → `[link](/projects/gardenlinux/introduction/intro)`
- Links to files outside `docs/` → GitHub URLs
- Handles `.media/` directories correctly

#### 2d. Frontmatter YAML Fixing

- Fixes YAML formatting in existing frontmatter
- Quotes YAML values with special characters (e.g., titles containing `:` or `#`)
- Ensures proper frontmatter structure

#### 2e. Content Sanitization

- Escapes angle brackets that aren't HTML tags (e.g., `<release number>`)
- Preserves code blocks and inline code
- Handles README.md → index.md conversion

## Sidebar Menu Construction

**File:** `docs/.vitepress/sidebar.ts`

The documentation sidebar uses the `vitepress-sidebar` library with automatic generation:

```typescript
generateSidebar({
  documentRootPath: "docs",
  scanStartPath: "",
  resolvePath: "/",
  collapsed: true,
  useTitleFromFileHeading: true,
  useTitleFromFrontmatter: true,
  useFolderLinkFromIndexFile: true,
  useFolderTitleFromIndexFile: true,
  excludePattern: ["projects"],
  sortMenusByFrontmatterOrder: true,
  frontmatterOrderDefaultValue: 999,
});
```

**Key features:**

- Automatically scans the `docs/` directory
- Excludes `docs/projects/` (legacy content, will be removed)
- Uses frontmatter `order` field for sorting (lower numbers appear first)
- Falls back to file/folder names for titles if not in frontmatter
- Respects `index.md` files for folder titles and links

## Frontmatter Fields

Frontmatter fields control how pages are displayed, organized, and linked. Here's a comprehensive reference:

### Core Fields

| Field         | Purpose               | Used By                         | Example                            |
| ------------- | --------------------- | ------------------------------- | ---------------------------------- |
| `title`       | Page title            | VitePress, sidebar, browser tab | `title: "Getting Started"`         |
| `description` | Page meta description | SEO, social sharing             | `description: "Quick start guide"` |
| `order`       | Sidebar sort order    | `vitepress-sidebar`             | `order: 10`                        |

### GitHub Integration

| Field                | Purpose                    | Used By              | Example                                       |
| -------------------- | -------------------------- | -------------------- | --------------------------------------------- |
| `github_org`         | GitHub organization        | Edit link generation | `github_org: gardenlinux`                     |
| `github_repo`        | Repository name            | Edit link generation | `github_repo: gardenlinux`                    |
| `github_branch`      | Branch name                | Edit link generation | `github_branch: main`                         |
| `github_source_path` | Original file path in repo | Edit link generation | `github_source_path: docs/tutorials/index.md` |

### Aggregation & Targeting

| Field                | Purpose                           | Used By            | Example                                         |
| -------------------- | --------------------------------- | ------------------ | ----------------------------------------------- |
| `github_target_path` | Target location in main docs tree | Aggregation system | `github_target_path: "docs/tutorials/index.md"` |

**Note:** Files with `github_target_path` or `target` are copied to the specified path in addition to being mirrored under `docs/projects/`. This enables documentation from source repos to appear in the primary documentation structure.

### Migration Tracking

| Field                   | Purpose                  | Used By            | Example                                 |
| ----------------------- | ------------------------ | ------------------ | --------------------------------------- |
| `migration_status`      | Migration state          | Documentation team | `migration_status: "new"`               |
| `migration_source`      | Original source location | Documentation team | `migration_source: "old-docs/guide.md"` |
| `migration_issue`       | Related GitHub issue     | Documentation team | `migration_issue: "#123"`               |
| `migration_stakeholder` | Responsible person/team  | Documentation team | `migration_stakeholder: "@username"`    |
| `migration_approved`    | Approval status          | Documentation team | `migration_approved: false`             |

These fields help track the documentation reorganization effort and are not used by VitePress itself.

### How Frontmatter Fields Are Used

#### Sidebar Ordering

The `order` field controls the position of pages in the sidebar:

- Lower numbers appear first (e.g., `order: 10` before `order: 20`)
- Default order is `999` (via `frontmatterOrderDefaultValue`)
- Works with `vitepress-sidebar`'s `sortMenusByFrontmatterOrder: true`

#### "Edit on GitHub" Links

The VitePress config uses GitHub metadata to generate edit links:

```typescript
editLink: {
  pattern: ({ filePath, frontmatter }) => {
    // If page has GitHub metadata from aggregated content
    if (
      frontmatter.github_org &&
      frontmatter.github_repo &&
      frontmatter.github_source_path
    ) {
      const branch = frontmatter.github_branch || "main";
      return `https://github.com/${frontmatter.github_org}/${frontmatter.github_repo}/edit/${branch}/${frontmatter.github_source_path}`;
    }
    // Fallback for native docs-ng pages
    return `https://github.com/gardenlinux/docs-ng/edit/main/docs/${filePath}`;
  };
}
```

This ensures that users editing aggregated documentation are directed to the correct source repository.

#### Targeted Documentation Placement

When a file includes `github_target_path` or `target`, the aggregation system copies it to that specific location:

```yaml
---
title: "Tutorials"
github_target_path: "docs/tutorials/index.md"
---
```

This file will be placed at `docs/tutorials/index.md` (in addition to `docs/projects/<repo>/tutorials/index.md`).

## Testing

Run the test suite to verify scripts work correctly:

```bash
make test              # Run all tests
make test-unit         # Run unit tests only
make test-integration  # Run integration tests only
```

See `scripts/tests/README.md` for more details.

## Available Commands

Run `make help` for all available commands:

```bash
# Development
make run                    # Run docs development server
make build                  # Build documentation for production
make preview                # Preview production build locally

# Testing
make test                   # Run full test suite
make test-unit              # Run unit tests only

# Documentation Aggregation
make aggregate              # Fetch and aggregate docs from all source repos
make aggregate-dry          # Test aggregation without modifying docs/
make aggregate-repo REPO=<name>  # Aggregate specific repo only
make test-aggregate-local   # Test with local repos (for development)

# Utilities
make clean                  # Clean aggregated docs and build artifacts
make clean-projects         # Remove only aggregated project docs
make clean-aggregated-git   # Remove uncommitted aggregated docs
```

## Repository Configuration

The `scripts/repos-config.json` file defines which repositories to aggregate and how to transform them:

```json
{
  "section_priorities": {
    "gardenlinux": -1,
    "readme": -1,
    "index": -1,
    "tutorials": 0,
    "how-to": 1,
    "explanation": 2,
    "reference": 3,
    "contributing": 4
  },
  "repos": [
    {
      "name": "gardenlinux",
      "url": "https://github.com/gardenlinux/gardenlinux",
      "github_org": "gardenlinux",
      "github_repo": "gardenlinux",
      "docs_path": "docs",
      "target_path": "projects/gardenlinux",
      "branch": "docs-ng",
      "structure": {
        "tutorials": "tutorials",
        "how-to": "how-to",
        "explanation": "explanation",
        "reference": "reference",
        "contributing": "contributing"
      },
      "special_files": {},
      "media_directories": [".media"]
    }
  ]
}
```

### Configuration Fields

- `section_priorities` — Control sidebar section ordering (lower = higher priority)
- `name` — Repository identifier used in paths
- `url` — Git repository URL for cloning
- `github_org` / `github_repo` — Used for edit links
- `docs_path` — Path to documentation within the repo
- `target_path` — Destination in aggregated site (e.g., `projects/gardenlinux`)
- `branch` — Git branch to fetch
- `structure` — How to transform directory structure:
  - Object: Directory mapping (e.g., `{"old-name": "new-name"}`)
  - `"flat"`: Copy as-is
  - `"sphinx"`: Sphinx documentation structure
- `special_files` — Files to place in specific locations
- `media_directories` — Directories to copy (e.g., `.media`)

## Additional Resources

- **VitePress Documentation**: https://vitepress.dev/
- **vitepress-sidebar Documentation**: https://vitepress-sidebar.cdget.com/
- **Garden Linux Main Repository**: https://github.com/gardenlinux/gardenlinux
