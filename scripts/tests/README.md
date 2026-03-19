# Test Suite

Test suite for the documentation aggregation scripts.

## Running Tests

### Unit Tests

Test individual functions in the transformation scripts:

```bash
cd scripts/tests
python3 run_tests.py
```

Run a specific test:

```bash
python3 run_tests.py test_escape_angle_brackets_in_text
```

### Integration Tests

Test overall script functionality:

```bash
cd scripts/tests
./test_integration.sh
```

## Test Coverage

### Unit Tests (run_tests.py)

Tests for `transform-content.py` functions:

- Angle bracket escaping
- HTML tag preservation
- Code block handling
- Link rewriting
- YAML frontmatter quoting
- Directory name transformations

### Integration Tests (test_integration.sh)

- Configuration file existence
- Script executability
- Syntax validation (bash and python)
- Basic script functionality

## Adding Tests

### Adding Unit Tests

Edit `run_tests.py` and add a new test function:

```python
def test_my_new_feature(runner):
    """Test description"""
    result = my_function("input")
    runner.assert_equal(result, "expected", "Error message")
```

Then add it to the `test_functions` list in `main()`.

### Adding Integration Tests

Edit `test_integration.sh` and add a new test block:

```bash
echo -n "My new test... "
if my_command; then
    echo "OK" && ((TESTS_PASSED++))
else
    echo "FAIL" && ((TESTS_FAILED++))
fi
```

## Test Fixtures

Sample markdown files for testing are in `fixtures/`:

- `test_doc.md` - Various markdown features
- `colon_title.md` - YAML frontmatter with colons
- `with_frontmatter.md` - Existing frontmatter

## Continuous Integration

Tests should be run in CI before merging. Add to `.github/workflows/`:

```yaml
- name: Run tests
  run: |
    cd scripts/tests
    python3 run_tests.py
    ./test_integration.sh
```
