# Quick Start: Documentation Aggregation

This guide will help you test the documentation aggregation system locally.

## Prerequisites

- Python 3.11+
- Git
- Bash
- Local clones of source repositories (for testing)

## Testing Locally (Recommended First Steps)

### 1. Test with Dry Run

This will fetch and transform docs but won't modify your `docs/` directory:

```bash
make test-aggregate
```

This uses local file:// paths to your existing repo clones, so it's fast and
safe.

### 2. Review the Output

The dry run will create a temporary directory with transformed docs. Check the
output to see:

- Which repos were fetched successfully
- Any transformation warnings
- Generated sidebar configuration

### 3. Run Actual Aggregation

Once you're satisfied with the dry run:

```bash
make aggregate
```

This will:

1. Fetch docs from all configured repos
2. Transform content (rename dirs, rewrite links, add frontmatter)
3. Copy to `docs/projects/`
4. Generate sidebar configuration

### 4. Preview the Documentation

```bash
make dev
```

Visit http://localhost:5173 to see the aggregated documentation.

### 5. Navigate to Projects

The aggregated docs will be available at:

- `/projects/gardenlinux/` - Main Garden Linux documentation
- `/projects/builder/` - Builder documentation
- `/projects/python-gardenlinux-lib/` - Python library docs

## Testing Specific Repository

To test with just one repo:

```bash
make aggregate-repo REPO=gardenlinux
```

## Configuration

### Local Testing Configuration

For local testing, the system uses `scripts/repos-config.local.json` which
points to local repositories:

```json
{
  "repos": [
    {
      "name": "gardenlinux",
      "url": "file:///home/$USER/gardenlinux/gardenlinux",
      ...
    }
  ]
}
```

### Production Configuration

For CI/CD, use `scripts/repos-config.json` with remote URLs:

```json
{
  "repos": [
    {
      "name": "gardenlinux",
      "url": "https://github.com/gardenlinux/gardenlinux.git",
      ...
    }
  ]
}
```

## What Gets Aggregated?

### gardenlinux repo

- `docs/00_introduction/` → `docs/projects/gardenlinux/introduction/`
- `docs/01_developers/` → `docs/projects/gardenlinux/developers/`
- `docs/02_operators/` → `docs/projects/gardenlinux/operators/`

### builder repo

- `docs/*.md` → `docs/projects/builder/` (flat structure)

### python-gardenlinux-lib repo

- `docs/*.rst` → `docs/projects/python-gardenlinux-lib/` (Sphinx structure)

## Content Transformations

The system automatically:

1. **Renames directories**: `00_introduction` → `introduction`
2. **Rewrites links**: `[link](../01_developers/build.md)` →
   `[link](/projects/gardenlinux/developers/build)`
3. **Adds frontmatter**: Ensures all markdown files have proper YAML frontmatter
4. **Preserves structure**: Maintains subdirectories and file hierarchy

## Cleaning Up

To remove aggregated docs:

```bash
make clean-projects
```

To clean everything (including build artifacts):

```bash
make clean
```

## Troubleshooting

### "Config file not found"

Make sure you're in the docs-ng root directory when running make commands.

### "Local repo not found"

Check that the paths in `repos-config.local.json` match your local repository
locations.

### "No changes detected"

This is normal if you've already run aggregation and the source docs haven't
changed.

### Links are broken

- Check browser console for 404 errors
- Review the generated sidebar in `docs/.vitepress/config.generated.json`
- Verify link transformations in `scripts/transform-content.py`

## Next Steps

1. Test aggregation locally ✓
2. Review transformed content ✓
3. Update VitePress config.mts with generated sidebars
4. Add navigation dropdown for project docs
5. Push to GitHub and let CI run the aggregation
6. Set up scheduled runs (daily at 2 AM UTC)

## Manual Integration with VitePress Config

The system generates `docs/.vitepress/config.generated.json` with sidebar
structure. You'll need to manually integrate this into `config.mts`:

```typescript
// config.mts
sidebar: {
  // Your existing sidebars
  '/quickstart': [...],
  '/usage/': [...],
  
  // Add generated project sidebars
  '/projects/gardenlinux/': [...], // Copy from config.generated.json
  '/projects/builder/': [...],
  '/projects/python-gardenlinux-lib/': [...],
}
```
