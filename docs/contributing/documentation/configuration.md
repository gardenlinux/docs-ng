---
title: "Documentation Aggregation Configuration Reference"
description: "Complete reference for repos-config.json and repos-config.local.json configuration options"
---

# Documentation Aggregation Configuration Reference

Complete reference for configuring the documentation aggregation system.

> **Source Repository:**
> [gardenlinux/docs-ng](https://github.com/gardenlinux/docs-ng)

## Configuration Files

### `repos-config.json`

Main configuration file for production aggregation. Uses git URLs and commit
locks.

**Location:** Project root

### `repos-config.local.json`

Development configuration file for local testing. Uses `file://` URLs to avoid
git operations.

**Location:** Project root

## Configuration Structure

```json
{
  "repos": [
    {
      "name": "repository-name",
      "url": "https://github.com/org/repo",
      "docs_path": "docs",
      "target_path": "projects/repository-name",
      "ref": "main",
      "commit": "abc123...",
      "root_files": ["README.md"],
      "structure": "flat",
      "media_directories": [".media", "assets"],
      "special_files": {
        "GUIDE.md": "how-to"
      }
    }
  ]
}
```

## Field Reference

### Required Fields

#### `name`

- **Type:** String
- **Description:** Unique identifier for the repository
- **Example:** `"gardenlinux"`, `"builder"`, `"python-gardenlinux-lib"`
- **Notes:** Used in generated paths and logging

#### `url`

- **Type:** String (URL or file path)
- **Description:** Repository location
- **Examples:**
  - Git: `"https://github.com/gardenlinux/gardenlinux"`
  - Local: `"file://../gardenlinux"`
- **Notes:** For local development, use `file://` URLs in
  `repos-config.local.json`

#### `docs_path`

- **Type:** String
- **Description:** Path to documentation directory within the repository
- **Examples:** `"docs"`, `"documentation"`, `"."` (for root)
- **Notes:** Relative to repository root; content of this directory is copied

#### `target_path`

- **Type:** String
- **Description:** Destination path in the docs directory
- **Example:** `"projects/gardenlinux"`
- **Notes:** Usually `projects/<name>` for project mirrors

#### `ref`

- **Type:** String
- **Description:** Git reference to fetch (branch, tag, or commit)
- **Examples:** `"main"`, `"docs-ng"`, `"v1.0.0"`
- **Notes:** Required for git URLs; ignored for `file://` URLs

### Optional Fields

#### `commit`

- **Type:** String (commit hash)
- **Description:** Lock to a specific commit for reproducible builds
- **Example:** `"abc123def456..."`
- **Default:** Not used (fetches from `ref`)
- **Notes:** Generated automatically with `make aggregate-update`

#### `root_files`

- **Type:** Array of strings
- **Description:** Root-level files to copy (e.g., README.md, CONTRIBUTING.md)
- **Example:** `["README.md", "CONTRIBUTING.md", "LICENSE"]`
- **Default:** `[]` (no root files copied)
- **Notes:** Files can have `github_target_path` front-matter for targeted
  placement

#### `structure`

- **Type:** String or Object
- **Description:** How to reorganize directory structure
- **Options:**
  - `"flat"` — Copy all files as-is
  - `"sphinx"` — Sphinx documentation structure
  - Object — Custom directory mapping (see below)
- **Default:** `"flat"`

**Custom Structure Example:**

```json
"structure": {
  "tutorials": "tutorials",
  "guides": "how-to",
  "concepts": "explanation",
  "api-reference": "reference"
}
```

This maps source directories to Diataxis categories.

#### `media_directories`

- **Type:** Array of strings
- **Description:** Directory names to treat as media/assets
- **Example:** `[".media", "assets", "_static", "images"]`
- **Default:** `[]`
- **Notes:**
  - Searched recursively in source repository
  - Nested media dirs (e.g., `tutorials/assets/`) copied to same relative path
  - Root-level media dirs (e.g., `_static/`) copied to common ancestor of
    targeted files

#### `special_files`

- **Type:** Object (filename → category mapping)
- **Description:** Map non-standard files to Diataxis categories
- **Example:**
  ```json
  {
    "GUIDE.md": "how-to",
    "CONCEPTS.md": "explanation",
    "CHANGELOG.md": "reference"
  }
  ```
- **Default:** `{}`
- **Notes:** Used when files don't follow standard naming conventions

## Complete Example

```json
{
  "repos": [
    {
      "name": "gardenlinux",
      "url": "https://github.com/gardenlinux/gardenlinux",
      "docs_path": "docs",
      "target_path": "projects/gardenlinux",
      "ref": "docs-ng",
      "commit": "c4b1d8d7f878fcb3e779315d28e35fcb19ae4dfb",
      "root_files": ["CONTRIBUTING.md", "SECURITY.md"],
      "structure": {
        "tutorials": "tutorials",
        "how-to": "how-to",
        "explanation": "explanation",
        "reference": "reference",
        "contributing": "contributing"
      },
      "media_directories": [".media", "assets", "_static"]
    },
    {
      "name": "builder",
      "url": "https://github.com/gardenlinux/builder",
      "docs_path": "docs",
      "target_path": "projects/builder",
      "ref": "docs-ng",
      "commit": "b10476ad8c46130f310e36daa42c6e2c14fb51a9",
      "structure": "flat",
      "media_directories": [".media", "assets", "_static"]
    },
    {
      "name": "python-gardenlinux-lib",
      "url": "https://github.com/gardenlinux/python-gardenlinux-lib",
      "docs_path": "docs",
      "target_path": "projects/python-gardenlinux-lib",
      "ref": "docs-ng",
      "commit": "9142fccc3d83ab51759db7d328fa19166bc1df63",
      "structure": "sphinx",
      "media_directories": [".media", "assets", "_static"]
    }
  ]
}
```

## Environment-Specific Configuration

### Production (`repos-config.json`)

- Use HTTPS git URLs
- Include `commit` locks for reproducibility
- Use `docs-ng` or stable branches for `ref`

### Development (`repos-config.local.json`)

- Use `file://` URLs for local repos
- Omit `commit` field (not used for local)
- Omit `ref` field (not needed for file://)
- Keep structure and other settings consistent with production

**Example local config:**

```json
{
  "repos": [
    {
      "name": "gardenlinux",
      "url": "file://../gardenlinux",
      "docs_path": "docs",
      "target_path": "projects/gardenlinux",
      "root_files": ["CONTRIBUTING.md", "SECURITY.md"],
      "structure": {
        "tutorials": "tutorials",
        "how-to": "how-to",
        "explanation": "explanation",
        "reference": "reference"
      },
      "media_directories": [".media", "assets"]
    }
  ]
}
```

## Common Configuration Patterns

### Minimal Configuration

Simplest configuration for a flat repository:

```json
{
  "name": "my-repo",
  "url": "https://github.com/org/my-repo",
  "docs_path": "docs",
  "target_path": "projects/my-repo",
  "ref": "main",
  "structure": "flat"
}
```

### With Targeted Documentation

Repository using `github_target_path` front-matter:

```json
{
  "name": "my-repo",
  "url": "https://github.com/org/my-repo",
  "docs_path": "docs",
  "target_path": "projects/my-repo",
  "ref": "main",
  "structure": "flat",
  "media_directories": ["assets", "_static"]
}
```

Then in your markdown files:

```yaml
---
title: "My Tutorial"
github_target_path: "docs/tutorials/my-tutorial.md"
---
```

## Front-Matter Fields

When using `github_target_path`, you can include additional metadata:

- **`github_org`**: Organization name (e.g., `"gardenlinux"`)
- **`github_repo`**: Repository name (e.g., `"docs-ng"`)
- **`github_source_path`**: Original file path in source repo (e.g.,
  `"docs/tutorial.md"`)

These help create source links in the documentation.

### Page Display Fields

- **`description`**: A short summary of the page. Used as the `<meta>`
  description by VitePress and shown in section index listings when
  `overviewDescriptions` is enabled on the parent page.
- **`overviewDescriptions`**: Boolean controlling whether the `<SectionIndex />`
  component displays child page descriptions. Defaults to `true`. Set to `false`
  on an index page to hide descriptions for its listing.
- **`order`**: Numeric value for controlling sort order in the sidebar and
  section listings. Lower values appear first.
- **`migration_status`**: Status for content migration (e.g., `"new"`,
  `"adapt"`, `"aggregate"`).

## See Also

- [Documentation Workflow](./documentation_workflow.md)
- [Documentation Quality Markers](./writing_good_docs.md)
- [Documentation Aggregator Architecture](./aggregation-architecture.md)
- [How to Documentation - Adding Repos to Aggregate](./adding-repos.md)
- [How to Documentation - Working With the Aggregator Locally](./working-locally.md)
- [Documentation Aggregator Technical Reference](./technical.md)
- [Documentation Aggregator Local Testing Guide](./testing.md)
- [Working with the Documentation Hub on Your Machine](./working-locally.md)
