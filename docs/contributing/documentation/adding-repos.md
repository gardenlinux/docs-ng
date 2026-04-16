---
title: "Adding Repositories to Documentation Aggregation"
description: "Guide for adding new repositories to the documentation aggregation system"
related_topics:
  - /contributing/documentation/documentation_workflow.md
  - /contributing/documentation/writing_good_docs.md
  - /contributing/documentation/aggregation-architecture.md
  - /contributing/documentation/adding-repos.md
  - /contributing/documentation/working-locally.md
  - /contributing/documentation/technical.md
  - /contributing/documentation/testing.md
  - /contributing/documentation/vitepress-features.md
---

# Adding Repositories to Documentation Aggregation

This guide explains how to add a new repository to the documentation aggregation
system.

> **Source Repository:**
> [gardenlinux/docs-ng](https://github.com/gardenlinux/docs-ng)

## Prerequisites

- Access to the repository you want to add
- Understanding of the repository's documentation structure
- Edit access to `repos-config.json`

## Step 1: Add Repository Configuration

Edit `repos-config.json` and add a new entry to the `repos` array:

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

### Required Fields

- **`name`**: Unique identifier for the repository
- **`url`**: Git URL or `file://` path for local development
- **`docs_path`**: Path to docs directory within the repository
- **`target_path`**: Where to place mirrored docs (usually `projects/<name>`)
- **`ref`**: Git branch or tag to fetch from

### Optional Fields

- **`commit`**: Lock to a specific commit hash for reproducibility
- **`root_files`**: List of root-level files to copy (e.g.,
  `["README.md", "CONTRIBUTING.md"]`)
- **`structure`**: Directory mapping strategy (see below)
- **`media_directories`**: List of media directories to copy (e.g.,
  `[".media", "_static", "assets"]`)

## Step 2: Choose a Structure Strategy

### Flat Structure

Copy all files as-is without reorganization:

```json
"structure": "flat"
```

### Sphinx Structure

For Sphinx-generated documentation:

```json
"structure": "sphinx"
```

### Custom Mapping

Map source directories to Diataxis categories:

```json
"structure": {
  "tutorials": "tutorials",
  "guides": "how-to",
  "concepts": "explanation",
  "api": "reference"
}
```

## Step 3: Configure Targeted Documentation

To have files automatically placed into the main Diataxis structure, add
`github_target_path` front-matter to markdown files in the source repository:

```markdown
---
title: "Example Guide"
github_target_path: "docs/how-to/example-guide.md"
---

# Example Guide

Content here...
```

Files with `github_target_path` will be copied to that exact location, not to
`projects/<repo-name>/`.

## Step 4: Test with Local Configuration

Create or edit `repos-config.local.json` for local testing:

```json
{
  "repos": [
    {
      "name": "new-repo",
      "url": "file://../new-repo",
      "docs_path": "docs",
      "target_path": "projects/new-repo",
      "structure": "flat"
    }
  ]
}
```

Then test aggregation:

```bash
make aggregate-local
```

## Step 5: Verify the Output

Check that files are in the correct locations:

```bash
ls -la docs/projects/new-repo/
```

If using `github_target_path`, verify targeted files:

```bash
ls -la docs/tutorials/
ls -la docs/how-to/
```

## Step 6: Lock the Commit (Production)

For production, lock to a specific commit:

```bash
# This fetches the latest and updates repos-config.json
make aggregate-update-repo REPO=new-repo
```

Or manually add the commit hash:

```json
{
  "name": "new-repo",
  "url": "https://github.com/gardenlinux/new-repo",
  "docs_path": "docs",
  "target_path": "projects/new-repo",
  "ref": "main",
  "commit": "abc123def456...",
  "structure": "flat"
}
```

## Advanced Configuration

### Media Directories

Automatically copy media directories alongside documentation:

```json
{
  "name": "new-repo",
  "media_directories": [".media", "assets", "_static"]
}
```

The system will:

- Find all instances of these directories recursively
- Copy nested media dirs (e.g., `tutorials/assets/`) to the same relative path
- Copy root-level media dirs (e.g., `_static/`) to the common ancestor of
  targeted files

### Root Files

Copy root-level files (like README.md or CONTRIBUTING.md):

```json
{
  "name": "new-repo",
  "root_files": ["README.md", "CONTRIBUTING.md", "LICENSE"]
}
```

These files can also have `github_target_path` front-matter for targeted
placement.

### Special Files

Handle non-standard files:

```json
{
  "name": "new-repo",
  "special_files": {
    "GUIDE.md": "how-to",
    "CONCEPTS.md": "explanation"
  }
}
```

## Complete Example

Here's a complete configuration:

```json
{
  "name": "example-tool",
  "url": "https://github.com/gardenlinux/example-tool",
  "docs_path": "documentation",
  "target_path": "projects/example-tool",
  "ref": "docs-ng",
  "commit": "1234567890abcdef",
  "root_files": ["README.md"],
  "structure": {
    "getting-started": "tutorials",
    "guides": "how-to",
    "concepts": "explanation",
    "api-reference": "reference"
  },
  "media_directories": [".media", "images"],
  "special_files": {
    "CHANGELOG.md": "reference"
  }
}
```

## Troubleshooting

### Files Not Appearing

- Verify `docs_path` points to the correct directory
- Check that the repository has a `docs-ng` branch or adjust `ref`
- Ensure `github_target_path` front-matter is correct

### Media Not Copied

- Add media directory names to `media_directories`
- Check that media dirs exist in the source repository

### Links Broken

- The transformer attempts to rewrite links automatically
- Check that relative links in source docs are correct
- Review `src/aggregation/transformer.py` for link rewriting logic

## Related Topics

<RelatedTopics />
