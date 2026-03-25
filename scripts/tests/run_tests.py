#!/usr/bin/env python3
"""
Test suite for documentation aggregation scripts

Run all tests:
    python3 run_tests.py

Run specific test:
    python3 run_tests.py test_escape_angle_brackets
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from transform_content import (  # type: ignore
    ensure_frontmatter,
    escape_angle_brackets,
    escape_text_angle_brackets,
    quote_yaml_value,
    rewrite_links,
)


class TestRunner:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []

    def assert_equal(self, actual, expected, message=""):
        if actual == expected:
            self.tests_passed += 1
            return True
        else:
            self.tests_failed += 1
            error = (
                f"FAIL: {message}\n  Expected: {repr(expected)}\n  Got: {repr(actual)}"
            )
            self.failures.append(error)
            print(error)
            return False

    def assert_contains(self, text, substring, message=""):
        if substring in text:
            self.tests_passed += 1
            return True
        else:
            self.tests_failed += 1
            error = f"FAIL: {message}\n  Expected to find: {repr(substring)}\n  In: {repr(text)}"
            self.failures.append(error)
            print(error)
            return False

    def assert_not_contains(self, text, substring, message=""):
        if substring not in text:
            self.tests_passed += 1
            return True
        else:
            self.tests_failed += 1
            error = f"FAIL: {message}\n  Expected NOT to find: {repr(substring)}\n  In: {repr(text)}"
            self.failures.append(error)
            print(error)
            return False

    def run_test(self, test_func):
        test_name = test_func.__name__
        print(f"Running {test_name}...", end=" ")
        try:
            test_func(self)
            print("OK")
        except Exception as e:
            self.tests_failed += 1
            error = f"FAIL: {test_name} raised exception: {e}"
            self.failures.append(error)
            print(error)

    def summary(self):
        total = self.tests_passed + self.tests_failed
        print(f"\n{'='*60}")
        print(f"Tests run: {total}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        print(f"{'='*60}")

        if self.tests_failed > 0:
            print("\nFailed tests:")
            for failure in self.failures:
                print(failure)
            return 1
        return 0


def test_escape_angle_brackets_in_text(runner):
    """Test that angle brackets in plain text are escaped"""
    content = "This is <placeholder text> that needs escaping."
    result = escape_angle_brackets(content)
    runner.assert_contains(
        result, "&lt;placeholder text&gt;", "Angle brackets in text should be escaped"
    )


def test_escape_angle_brackets_with_spaces(runner):
    """Test that angle brackets with spaces inside are escaped"""
    content = "Multiple <words here> should be escaped."
    result = escape_angle_brackets(content)
    runner.assert_contains(
        result, "&lt;words here&gt;", "Angle brackets with spaces should be escaped"
    )


def test_preserve_html_tags(runner):
    """Test that valid HTML tags are preserved"""
    content = "This <p>is HTML</p> and should not be escaped."
    result = escape_angle_brackets(content)
    runner.assert_contains(result, "<p>", "HTML <p> tag should be preserved")
    runner.assert_contains(result, "</p>", "HTML </p> tag should be preserved")


def test_preserve_code_blocks(runner):
    """Test that code blocks are not escaped"""
    content = """```python
x = "<value>"
```"""
    result = escape_angle_brackets(content)
    runner.assert_contains(
        result, "<value>", "Code in triple backticks should not be escaped"
    )


def test_preserve_inline_code(runner):
    """Test that inline code is not escaped"""
    content = "Inline code like `<var>` should not be escaped."
    result = escape_angle_brackets(content)
    runner.assert_contains(result, "`<var>`", "Inline code should not be escaped")


def test_rewrite_relative_links(runner):
    """Test that relative links are rewritten correctly"""
    content = "[Link](./other.md)"
    result = rewrite_links(content, "gardenlinux", "introduction/index.md")
    runner.assert_contains(
        result,
        "/projects/gardenlinux/introduction/other",
        "Relative link should be rewritten",
    )


def test_rewrite_numbered_directory_links(runner):
    """Test that numbered directories in links are transformed"""
    content = "[Link](../01_developers/guide.md)"
    result = rewrite_links(content, "gardenlinux", "introduction/index.md")
    runner.assert_contains(
        result, "developers/guide", "Numbered directory in link should be transformed"
    )


def test_preserve_external_links(runner):
    """Test that external links are not modified"""
    content = "[External](https://github.com/gardenlinux/gardenlinux)"
    result = rewrite_links(content, "gardenlinux", "")
    runner.assert_equal(result, content, "External links should not be modified")


def test_preserve_anchor_links(runner):
    """Test that anchor links are preserved"""
    content = "[Anchor](#section)"
    result = rewrite_links(content, "gardenlinux", "")
    runner.assert_equal(result, content, "Anchor links should not be modified")


def test_quote_yaml_value_with_colon(runner):
    """Test that YAML values with colons are quoted"""
    value = "Getting Started: Creating Images"
    result = quote_yaml_value(value)
    runner.assert_contains(result, '"', "Value with colon should be quoted")
    runner.assert_contains(
        result, "Getting Started: Creating Images", "Original value should be preserved"
    )


def test_quote_yaml_value_without_special_chars(runner):
    """Test that simple YAML values are not quoted"""
    value = "Simple Title"
    result = quote_yaml_value(value)
    runner.assert_equal(result, "Simple Title", "Simple value should not be quoted")


def test_ensure_frontmatter_no_change_when_missing(runner):
    """Test that content without frontmatter is returned unchanged"""
    content = "# Test Title\n\nContent here."
    result = ensure_frontmatter(content)
    runner.assert_equal(result, content, "Content without frontmatter should be unchanged")


def test_ensure_frontmatter_preserves_existing(runner):
    """Test that existing frontmatter is preserved"""
    content = "---\ntitle: Existing\n---\n\nContent"
    result = ensure_frontmatter(content)
    runner.assert_contains(
        result, "title: Existing", "Existing frontmatter should be preserved"
    )


def test_ensure_frontmatter_fixes_colons(runner):
    """Test that colons in existing frontmatter are quoted"""
    content = "---\ntitle: Test: Example\n---\n\nContent"
    result = ensure_frontmatter(content)
    runner.assert_contains(
        result, '"Test: Example"', "Colon in frontmatter should be quoted"
    )


def test_escape_text_angle_brackets_preserves_html(runner):
    """Test that known HTML tags are preserved"""
    text = "<div>content</div>"
    result = escape_text_angle_brackets(text)
    runner.assert_contains(result, "<div>", "div tag should be preserved")


def test_escape_text_angle_brackets_escapes_placeholders(runner):
    """Test that placeholder text is escaped"""
    text = "<placeholder>"
    result = escape_text_angle_brackets(text)
    runner.assert_contains(
        result, "&lt;placeholder&gt;", "Placeholder should be escaped"
    )


def main():
    runner = TestRunner()

    # Get test to run from command line, or run all
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        test_func = globals().get(test_name)
        if test_func and callable(test_func):
            runner.run_test(test_func)
        else:
            print(f"Test '{test_name}' not found")
            return 1
    else:
        # Run all tests
        test_functions = [
            test_escape_angle_brackets_in_text,
            test_escape_angle_brackets_with_spaces,
            test_preserve_html_tags,
            test_preserve_code_blocks,
            test_preserve_inline_code,
            test_rewrite_relative_links,
            test_rewrite_numbered_directory_links,
            test_preserve_external_links,
            test_preserve_anchor_links,
            test_quote_yaml_value_with_colon,
            test_quote_yaml_value_without_special_chars,
            test_ensure_frontmatter_no_change_when_missing,
            test_ensure_frontmatter_preserves_existing,
            test_ensure_frontmatter_fixes_colons,
            test_escape_text_angle_brackets_preserves_html,
            test_escape_text_angle_brackets_escapes_placeholders,
        ]

        for test_func in test_functions:
            runner.run_test(test_func)

    return runner.summary()


if __name__ == "__main__":
    sys.exit(main())
