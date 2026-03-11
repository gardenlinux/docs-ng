#!/bin/bash
# Run all tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running unit tests..."
python3 "$SCRIPT_DIR/run_tests.py"

echo ""
echo "All tests passed"
