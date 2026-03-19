#!/usr/bin/env bash
# Convenience script for testing aggregation with local repositories
# This uses repos-config.local.json which points to local file:// paths

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Testing aggregation with local repositories..."
echo ""

# Check if local repos exist
REPOS=(
    "/home/$USER/*/gardenlinux/gardenlinux"
    "/home/$USER/*/gardenlinux/builder"
    "/home/$USER/*/gardenlinux/python-gardenlinux-lib"
)

for repo in "${REPOS[@]}"; do
    if [ ! -d "$repo" ]; then
        echo "Error: Local repo not found: $repo"
        exit 1
    fi
done

echo "All local repositories found"
echo ""

# Backup original config
if [ -f "$SCRIPT_DIR/repos-config.json" ]; then
    cp "$SCRIPT_DIR/repos-config.json" "$SCRIPT_DIR/repos-config.json.bak"
    echo "Backed up repos-config.json to repos-config.json.bak"
fi

cp "$SCRIPT_DIR/repos-config.local.json" "$SCRIPT_DIR/repos-config.json"
echo "Using local configuration"
echo ""

"$SCRIPT_DIR/aggregate-docs.sh" "$@"

# Restore original config
if [ -f "$SCRIPT_DIR/repos-config.json.bak" ]; then
    mv "$SCRIPT_DIR/repos-config.json.bak" "$SCRIPT_DIR/repos-config.json"
    echo ""
    echo "Restored original repos-config.json"
fi
