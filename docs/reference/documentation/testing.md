---
title: "Documentation Aggregation Testing Guide"
description: "Test suite for documentation - unit tests, integration tests, and testing best practices"
---

# Documentation Aggregation Testing Guide

Test suite documentation for the documentation aggregation system.

> **Source Repository:** [gardenlinux/docs-ng](https://github.com/gardenlinux/docs-ng) > **Source File:** [tests/README.md](https://github.com/gardenlinux/docs-ng/blob/main/tests/README.md)

## Test Structure

```
tests/
├── conftest.py           # pytest configuration
├── fixtures/             # Test data
├── unit/                 # Unit tests (pure functions)
│   ├── test_config.py
│   ├── test_models.py
│   └── test_transformer.py
└── integration/          # Integration tests (filesystem)
    └── test_aggregation.py
```

## Running Tests

### All Tests

```bash
make test
```

### Unit Tests Only

```bash
make test-unit
```

### Integration Tests Only

```bash
make test-integration
```

### Direct pytest

For more control, use pytest directly:

```bash
# Run specific test file
python3 -m pytest tests/unit/test_transformer.py -v

# Run specific test function
python3 -m pytest tests/unit/test_transformer.py::test_rewrite_links -v

# Run with coverage
python3 -m pytest tests/ --cov=src/aggregation --cov-report=html
```

## Test Types

### Unit Tests

Test pure functions with no I/O side effects:

- **Link rewriting** (`rewrite_links`) — Transform markdown links
- **YAML quoting** (`quote_yaml_value`) — Safely quote YAML values
- **Frontmatter handling** (`ensure_frontmatter`, `parse_frontmatter`) — Parse and manipulate frontmatter
- **Config loading/saving** — Parse and write configuration files
- **Model validation** — Data class validation and serialization

Unit tests are fast, isolated, and don't touch the filesystem.

### Integration Tests

Test filesystem operations and the full aggregation workflow:

- **Local repository fetching** — Copy docs from local repos
- **Markdown file processing** — Transform files in place
- **Directory transformation** — Restructure directory trees
- **End-to-end aggregation** — Complete workflow testing

Integration tests are slower and require temporary directories.

## Test Fixtures

Located in `tests/fixtures/`, these provide:

- Sample markdown files
- Example frontmatter configurations
- Mock repository structures
- Configuration file examples

## Adding Tests

### Adding a Unit Test

1. Create or update a test file in `tests/unit/`
2. Use pytest conventions (`test_*` functions, `Test*` classes)
3. Use `assert` statements for validation

Example:

```python
def test_rewrite_links():
    """Test that links are properly rewritten."""
    content = "[link](../other/file.md)"
    result = rewrite_links(content, "repo-name", "path/to/file.md")
    assert "[link](/projects/repo-name/other/file.md)" in result
```

### Adding an Integration Test

1. Create or update a test file in `tests/integration/`
2. Use pytest fixtures for temporary directories
3. Clean up resources in teardown

Example:

```python
def test_fetch_local(tmp_path):
    """Test fetching from local repository."""
    source = tmp_path / "source"
    source.mkdir()
    (source / "docs").mkdir()
    (source / "docs" / "test.md").write_text("# Test")

    fetcher = DocsFetcher(tmp_path)
    result = fetcher.fetch(config, tmp_path / "output")

    assert result.success
    assert (tmp_path / "output" / "test.md").exists()
```

## Test Coverage

Check test coverage with:

```bash
python3 -m pytest tests/ --cov=src/aggregation --cov-report=term-missing
```

Target coverage levels:

- **Unit tests**: >90% coverage of pure functions
- **Integration tests**: Key workflows covered
- **Overall**: >80% code coverage

## Best Practices

### Do

- Test one thing per test function
- Use descriptive test names that explain what is being tested
- Use fixtures for common setup
- Keep tests fast and isolated
- Use parametrize for testing multiple inputs
- Assert specific outcomes, not just absence of errors

### Don't

- Test implementation details
- Make tests dependent on each other
- Use time-based assertions (use mocks instead)
- Leave temporary files after tests
- Test third-party library behavior

## Continuous Integration

Tests run automatically on:

- Pull requests
- Pushes to main/docs-ng branches
- Scheduled nightly builds

## Debugging Tests

### Run with verbose output

```bash
python3 -m pytest tests/ -vv
```

### Stop on first failure

```bash
python3 -m pytest tests/ -x
```

### Run failed tests only

```bash
python3 -m pytest tests/ --lf
```

### Use pdb debugger

```bash
python3 -m pytest tests/ --pdb
```

## Common Issues

### ImportError

Ensure you're in the project root and Python can find the `src` directory:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Fixture Not Found

Check that `conftest.py` is in the correct location and properly defines fixtures.

### Integration Tests Failing

Integration tests may fail if:

- Insufficient disk space
- Permission issues with temp directories
- Git not available in PATH

## See Also

- [Getting Started Tutorial](../../tutorials/documentation/index.md) — Step-by-step guide to contributing documentation
- [Adding Repositories](../../how-to/documentation/adding-repos.md) — How to add new repositories to the aggregation
- [Technical Reference](../../reference/documentation/technical.md) — Source code and API documentation
- [Configuration Reference](../../reference/documentation/configuration.md) — Complete configuration options
- [Architecture Explanation](../../explanation/documentation/aggregation-architecture.md) — Deep dive into how the documentation aggregation system works
