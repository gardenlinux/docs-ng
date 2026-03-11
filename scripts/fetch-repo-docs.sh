#!/bin/bash
# Script to fetch documentation from remote repositories using sparse checkout
# Usage: ./fetch-repo-docs.sh <repo_url> <branch> <docs_path> <output_dir>

set -e

REPO_URL="$1"
BRANCH="${2:-main}"
DOCS_PATH="${3:-docs}"
OUTPUT_DIR="$4"
TEMP_DIR=$(mktemp -d)

if [ -z "$REPO_URL" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <repo_url> <branch> <docs_path> <output_dir>"
    echo "Example: $0 https://github.com/gardenlinux/gardenlinux.git main docs /tmp/output"
    exit 1
fi

echo "Fetching docs from: $REPO_URL"
echo "   Branch: $BRANCH"
echo "   Docs path: $DOCS_PATH"
echo "   Output: $OUTPUT_DIR"

# Initialize sparse checkout
cd "$TEMP_DIR"
git init
git remote add origin "$REPO_URL"
git config core.sparseCheckout true

echo "$DOCS_PATH/*" >> .git/info/sparse-checkout

echo "Cloning (sparse checkout)..."
git fetch --depth=1 origin "$BRANCH"
git checkout "$BRANCH"

if [ -d "$DOCS_PATH" ]; then
    echo "Copying docs to $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
    cp -r "$DOCS_PATH"/* "$OUTPUT_DIR/" 2>/dev/null || true
    # Handle hidden directories for media
    shopt -s dotglob
    for item in "$DOCS_PATH"/.*; do
        if [ -e "$item" ] && [ "$(basename "$item")" != "." ] && [ "$(basename "$item")" != ".." ]; then
            cp -r "$item" "$OUTPUT_DIR/" 2>/dev/null || true
        fi
    done
    shopt -u dotglob
    echo "Fetch complete!"
else
    echo "Warning: $DOCS_PATH directory not found in repository"
fi

# Cleanup
cd - > /dev/null
rm -rf "$TEMP_DIR"
