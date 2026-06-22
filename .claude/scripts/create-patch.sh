#!/bin/bash
set -e

# Configuration
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DISLER_DIR="$PROJECT_ROOT/external/disler"
PATCHES_DIR="$PROJECT_ROOT/patches"

if [ -z "$1" ]; then
    echo "Usage: ./create-patch.sh \"patch_name\""
    exit 1
fi

NAME=$(echo "$1" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
TIMESTAMP=$(date +%Y%m%d)
NEXT_NUM=$(find "$PATCHES_DIR" -maxdepth 1 -name "*.patch" | wc -l | xargs -I{} echo "{}" | awk '{printf "%03d", $1+1}')
FILENAME="${NEXT_NUM}-${NAME}.patch"

echo "📝 Creating patch $FILENAME from external/disler..."

cd "$DISLER_DIR"
git diff > "$PATCHES_DIR/$FILENAME"

if [ -s "$PATCHES_DIR/$FILENAME" ]; then
    echo "✅ Patch created at patches/$FILENAME"
    echo "   Size: $(wc -c < "$PATCHES_DIR/$FILENAME") bytes"
else
    rm "$PATCHES_DIR/$FILENAME"
    echo "❌ No changes detected in external/disler. Patch empty."
fi
