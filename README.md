# docs-ng

Master repo for public facing Garden Linux documentation.

## Quick Start

```bash
# Run development server
make run

# Run tests
make test

# Aggregate documentation from repos
make aggregate
```

## Testing

Run the test suite to verify scripts work correctly:

```bash
make test              # Run all tests
make test-unit         # Run unit tests only
make test-integration  # Run integration tests only
```

See `scripts/tests/README.md` for more details.

## Documentation Aggregation

See `scripts/README.md` for documentation aggregation details.

## GitHub Pages Deployment

The documentation site is automatically deployed to GitHub Pages:

- **Production**: Automatically deployed when changes are merged to `main`
  - URL: https://gardenlinux.github.io/docs-ng/
- **PR Previews**: Each pull request gets its own preview deployment
  - URL: https://gardenlinux.github.io/docs-ng/pr-{PR_NUMBER}/
  - Automatically updated with each commit
  - Cleaned up when PR is closed

The workflow is configured in `.github/workflows/deploy-pages.yml`.

For detailed information about the deployment system, see the [GitHub Pages Deployment Guide](docs/contributing/github-pages-deployment.md).

## Commands

Run `make help` for all available commands.

