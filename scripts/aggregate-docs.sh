#!/bin/bash
# Main script to aggregate documentation from multiple repositories
# This orchestrates the entire process: fetch -> transform -> update config

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCS_DIR="$PROJECT_ROOT/docs"
TEMP_DIR=$(mktemp -d)
CONFIG_FILE="$SCRIPT_DIR/repos-config.json"

echo "=============================================================="
echo "  Garden Linux Documentation Aggregation"
echo "=============================================================="
echo ""

cleanup() {
    echo "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT
trap cleanup SIGINT
trap cleanup SIGTERM

DRY_RUN=false
REPO_FILTER=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --repo)
            REPO_FILTER="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run        Fetch and transform but don't update docs directory"
            echo "  --repo <name>    Only process specific repository"
            echo "  --help           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Configuration:"
echo "   Config file: $CONFIG_FILE"
echo "   Docs directory: $DOCS_DIR"
echo "   Temp directory: $TEMP_DIR"
echo "   Dry run: $DRY_RUN"
if [ -n "$REPO_FILTER" ]; then
    echo "   Repository filter: $REPO_FILTER"
fi
echo ""

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE"
    exit 1
fi

# Check if required scripts exist
FETCH_SCRIPT="$SCRIPT_DIR/fetch-repo-docs.sh"
TRANSFORM_SCRIPT="$SCRIPT_DIR/transform_content.py"
UPDATE_CONFIG_SCRIPT="$SCRIPT_DIR/update_config.py"

for script in "$FETCH_SCRIPT" "$TRANSFORM_SCRIPT" "$UPDATE_CONFIG_SCRIPT"; do
    if [ ! -f "$script" ]; then
        echo "Error: Required script not found: $script"
        exit 1
    fi
done

echo "Step 1: Fetching documentation from repositories"
echo "-------------------------------------------------------------"

repos=$(python3 -c "
import json
with open('$CONFIG_FILE') as f:
    config = json.load(f)
    for repo in config['repos']:
        if '$REPO_FILTER' and repo['name'] != '$REPO_FILTER':
            continue
        print(f\"{repo['name']}|{repo['url']}|{repo['branch']}|{repo['docs_path']}\")
")

if [ -z "$repos" ]; then
    echo "Error: No repositories to process"
    exit 1
fi

while IFS='|' read -r name url branch docs_path; do
    echo ""
    echo "Repository: $name"
    
    repo_temp_dir="$TEMP_DIR/$name"
    mkdir -p "$repo_temp_dir"
    
    # Fetch docs using sparse checkout
    if ! "$FETCH_SCRIPT" "$url" "$branch" "$docs_path" "$repo_temp_dir"; then
        echo "Warning: Failed to fetch docs for $name"
        continue
    fi
done <<< "$repos"

echo ""
echo "Fetch complete!"
echo ""

echo "Step 2: Transforming documentation content"
echo "-------------------------------------------------------------"

if [ "$DRY_RUN" = true ]; then
    echo "Dry run mode: Transforming to temporary location"
    TRANSFORM_TARGET="$TEMP_DIR/transformed-docs"
    mkdir -p "$TRANSFORM_TARGET"
else
    TRANSFORM_TARGET="$DOCS_DIR"
fi

transform_args="--config $CONFIG_FILE --docs-dir $TRANSFORM_TARGET --temp-dir $TEMP_DIR"

if [ -n "$REPO_FILTER" ]; then
    transform_args="$transform_args --repo $REPO_FILTER"
fi

# shellcheck disable=SC2086
if ! python3 "$TRANSFORM_SCRIPT" $transform_args; then
    echo "Error: Transformation failed"
    exit 1
fi

echo ""
echo "Step 3: Updating VitePress configuration"
echo "-------------------------------------------------------------"

if [ "$DRY_RUN" = true ]; then
    echo "Dry run mode: Skipping config update"
    echo ""
    echo "Transformed docs available at: $TRANSFORM_TARGET"
else
    if ! python3 "$UPDATE_CONFIG_SCRIPT" --config "$CONFIG_FILE" --docs-dir "$DOCS_DIR" --vitepress-config "$DOCS_DIR/.vitepress/config.mts"; then
        echo "Warning: Failed to update VitePress config"
    fi
fi

echo ""
echo "=============================================================="
echo "  Documentation aggregation complete!"
echo "=============================================================="
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "To apply changes, run without --dry-run flag"
else
    echo "Next steps:"
    echo "  1. Review the changes in docs/projects/"
    echo "  2. Run 'make dev' or 'pnpm run docs:dev' to preview"
    echo "  3. Commit the changes if satisfied"
fi
