#!/usr/bin/env bash
# Script to fetch documentation from remote repositories using sparse checkout
# Usage: ./fetch-repo-docs.sh <repo_url> <branch> <docs_path> <output_dir> [root_files...]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="$1"
BRANCH="${2:-main}"
DOCS_PATH="${3:-docs}"
OUTPUT_DIR="$4"
shift 4
ROOT_FILES=("$@")
TEMP_DIR=$(mktemp -d)

if [ -z "$REPO_URL" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <repo_url> <branch> <docs_path> <output_dir> [root_files...]"
    echo "Example: $0 https://github.com/gardenlinux/gardenlinux.git main docs /tmp/output CONTRIBUTING.md SECURITY.md"
    exit 1
fi

# Convert relative file:// URLs to absolute paths
if [[ "$REPO_URL" == file://../* ]]; then
    RELATIVE_PATH="${REPO_URL#file://}"
    ABSOLUTE_PATH="$(cd "$SCRIPT_DIR/.." && cd "$RELATIVE_PATH" && pwd)"
    REPO_URL="file://$ABSOLUTE_PATH"
fi

echo "Fetching docs from: $REPO_URL"
echo "   Branch: $BRANCH"
echo "   Docs path: $DOCS_PATH"
if [ ${#ROOT_FILES[@]} -gt 0 ]; then
    echo "   Root files: ${ROOT_FILES[*]}"
fi
echo "   Output: $OUTPUT_DIR"

# Initialize sparse checkout
cd "$TEMP_DIR"
git init
git remote add origin "$REPO_URL"
git config core.sparseCheckout true

echo "$DOCS_PATH/*" >> .git/info/sparse-checkout

# Add root files to sparse checkout if specified
for root_file in "${ROOT_FILES[@]}"; do
    if [ -n "$root_file" ]; then
        echo "$root_file" >> .git/info/sparse-checkout
    fi
done

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
else
    echo "Warning: $DOCS_PATH directory not found in repository"
fi

# Copy root files if specified
if [ ${#ROOT_FILES[@]} -gt 0 ]; then
    echo "Copying root files to $OUTPUT_DIR"
    for root_file in "${ROOT_FILES[@]}"; do
        if [ -f "$root_file" ]; then
            cp "$root_file" "$OUTPUT_DIR/"
            echo "   Copied: $root_file"
        else
            echo "   Warning: $root_file not found"
        fi
    done
fi

echo "Fetch complete!"

# Cleanup
cd - > /dev/null
rm -rf "$TEMP_DIR"
