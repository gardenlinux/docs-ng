# Test Suite

## Structure

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

```bash
# All tests
make test

# Unit tests
make test-unit

# Integration tests
make test-integration

# Direct pytest
python3 -m pytest tests/unit/ -v
python3 -m pytest tests/integration/ -v
```

## Test Types

### Unit Tests

Test pure functions with no I/O:

- Link rewriting (`rewrite_links`)
- YAML quoting (`quote_yaml_value`)
- Frontmatter handling (`ensure_frontmatter`)
- Config loading/saving
- Model validation

### Integration Tests

Test filesystem operations:

- Local repository fetching
- Markdown file processing
- Directory transformation

## Adding Tests

1. Unit test: `tests/unit/test_*.py`
2. Integration test: `tests/integration/test_*.py`
3. Use pytest conventions: `test_*` functions, `Test*` classes
4. Use `assert` statements, not custom test runners
