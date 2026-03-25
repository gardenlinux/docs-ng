# "Edit this page on GitHub" Feature Implementation

This document describes the implementation of the "Edit this page on GitHub" feature for the docs-ng documentation site.

## Overview

The feature allows users to click an "Edit this page on GitHub" link on any documentation page, which takes them directly to the source file in the appropriate GitHub repository for editing.

## Challenge

Since docs-ng aggregates documentation from multiple repositories (gardenlinux, builder, python-gardenlinux-lib), each page needs to know which repository and path it came from to generate the correct GitHub edit URL.

## Solution

The implementation adds GitHub metadata to each aggregated page's frontmatter during the transformation process, which VitePress then uses to construct the correct edit URL.

## Implementation Details

### 1. Source File Metadata (`gardenlinux/docs/*.md`)

GitHub metadata has been added directly to the frontmatter of all markdown files in the gardenlinux repository:

```yaml
---
title: "First Boot on Azure"
github_org: gardenlinux
github_repo: gardenlinux
github_source_path: docs/tutorials/first-boot-azure.md
---
```

A script (`scripts/add_github_frontmatter.py`) was created to add this metadata to all 116 markdown files in the gardenlinux/docs directory. The metadata includes:
- `github_org`: Organization name (always "gardenlinux")
- `github_repo`: Repository name (always "gardenlinux")
- `github_source_path`: File path relative to repository root (e.g., "docs/tutorials/first-boot-azure.md")

### 2. Repository Configuration (`scripts/repos-config.json`)

Added GitHub metadata fields to repository configurations (for potential use with other repos):

```json
{
  "name": "gardenlinux",
  "github_org": "gardenlinux",
  "github_repo": "gardenlinux",
  "branch": "docs-ng",
  ...
}
```

### 3. VitePress Configuration (`docs/.vitepress/config.mts`)

Added `editLink` configuration with a dynamic pattern function:

```typescript
editLink: {
  pattern: ({ filePath, frontmatter }) => {
    // If page has GitHub metadata from aggregated content, use it
    if (frontmatter.github_org && frontmatter.github_repo && frontmatter.github_source_path) {
      const branch = frontmatter.github_branch || 'main';
      return `https://github.com/${frontmatter.github_org}/${frontmatter.github_repo}/edit/${branch}/${frontmatter.github_source_path}`;
    }
    // Fallback for pages native to docs-ng (no GitHub metadata)
    return `https://github.com/gardenlinux/docs-ng/edit/main/docs/${filePath}`;
  },
  text: 'Edit this page on GitHub'
}
```

## How It Works

1. **During Aggregation**: When docs are fetched and transformed from source repositories:
   - The transform script reads the repo configuration (org, repo, branch, docs_path)
   - For each markdown file, it calculates the original source path
   - It injects GitHub metadata into the file's frontmatter

2. **At Runtime**: When VitePress renders a page:
   - It reads the frontmatter metadata
   - The `editLink.pattern` function constructs the appropriate GitHub edit URL
   - If metadata exists, it links to the source repository
   - If metadata is missing (native docs-ng pages), it links to the docs-ng repository

## Example

For a file originally from `gardenlinux/docs/tutorials/first-boot-azure.md`:

**Frontmatter added:**
```yaml
---
title: "First Boot on Azure"
github_org: gardenlinux
github_repo: gardenlinux
github_branch: docs-ng
github_source_path: docs/tutorials/first-boot-azure.md
---
```

**Generated URL:**
```
https://github.com/gardenlinux/gardenlinux/edit/docs-ng/docs/tutorials/first-boot-azure.md
```

## Testing

To test the implementation:

1. Run the aggregation: `make aggregate`
2. Start the dev server: `make run`
3. Navigate to any aggregated page
4. Verify the "Edit this page on GitHub" link appears
5. Click it to ensure it goes to the correct file in the correct repository

## Benefits

- **Accurate Attribution**: Each page links to its actual source repository
- **Easy Contribution**: Users can quickly find where to edit a page
- **Multi-repo Support**: Works seamlessly across all aggregated repositories
- **Fallback Support**: Native docs-ng pages still work correctly