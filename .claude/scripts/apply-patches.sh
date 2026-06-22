#!/bin/bash
set -e

# Configuration
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DISLER_DIR="$PROJECT_ROOT/external/disler"
PATCHES_DIR="$PROJECT_ROOT/patches"

echo "🔧 Applying patches to external/disler..."

if [ ! -d "$DISLER_DIR" ]; then
    echo "❌ Error: external/disler directory not found."
    exit 1
fi

cd "$DISLER_DIR"

# Reset to clean state (optional, but recommended to avoid duplicate patches)
# git reset --hard HEAD
# git clean -fd

# Iterate through patches
count=0
for patch in "$PATCHES_DIR"/*.patch; do
    if [ -f "$patch" ]; then
        echo "   📄 Applying $(basename "$patch")..."
        # Try adjusting p-level if standard p1 fails
        if git apply --check "$patch" 2>/dev/null; then
             git apply "$patch"
        elif git apply -p1 --check "$patch" 2>/dev/null; then
             git apply -p1 "$patch"
        elif git apply -p2 --check "$patch" 2>/dev/null; then
             git apply -p2 "$patch"
        else
             echo "❌ Failed to apply $(basename "$patch")"
             exit 1
        fi
        ((count++))
    fi
done

if [ "$count" -eq 0 ]; then
    echo "ℹ️  No patches found."
else
    echo "✅ Successfully applied $count patches."
fi
