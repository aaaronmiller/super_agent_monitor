#!/bin/bash
#
# Format Enforcer Hook
# Validates output format and enforces consistency
#
# Triggers: Before output submission
# Purpose: Ensure agent outputs match expected format

set -e

# Read event from stdin
EVENT=$(cat)

# Extract event type
EVENT_TYPE=$(echo "$EVENT" | jq -r '.type // "unknown"')

# Only process output events
if [ "$EVENT_TYPE" != "output" ]; then
    exit 0
fi

# Extract output content
OUTPUT=$(echo "$EVENT" | jq -r '.content // ""')
AGENT=$(echo "$EVENT" | jq -r '.agent // "unknown"')

# Validation flags
VALID=true
WARNINGS=""

# Function to add warning
add_warning() {
    WARNINGS="${WARNINGS}⚠️  $1\n"
}

# Check for common format issues
case "$AGENT" in
    "prd-finder")
        # Should have "File Discovery Results" header
        if ! echo "$OUTPUT" | grep -q "File Discovery Results"; then
            add_warning "Missing 'File Discovery Results' header"
            VALID=false
        fi

        # Should have priority and standard sections
        if ! echo "$OUTPUT" | grep -q "Priority Files"; then
            add_warning "Missing 'Priority Files' section"
            VALID=false
        fi
        ;;

    "file-analyzer")
        # Should have "File:" prefix
        if ! echo "$OUTPUT" | grep -q "^## File:"; then
            add_warning "Missing '## File:' header"
            VALID=false
        fi

        # Should have required fields
        for field in "Project" "Type" "Summary" "Key Features" "Tags"; do
            if ! echo "$OUTPUT" | grep -q "**${field}**:"; then
                add_warning "Missing required field: **${field}**:"
                VALID=false
            fi
        done
        ;;

    "prd-rater")
        # Should have rating header
        if ! echo "$OUTPUT" | grep -q "### PRD Rating:"; then
            add_warning "Missing '### PRD Rating:' header"
            VALID=false
        fi

        # Should have dimension scores table
        if ! echo "$OUTPUT" | grep -q "Dimension.*Score.*Rating"; then
            add_warning "Missing dimension scores table"
            VALID=false
        fi

        # Should have overall score
        if ! echo "$OUTPUT" | grep -q "**Overall Score**:"; then
            add_warning "Missing overall score"
            VALID=false
        fi
        ;;

    "project-tagger")
        # Should have association results header
        if ! echo "$OUTPUT" | grep -q "Project Association Results"; then
            add_warning "Missing 'Project Association Results' header"
            VALID=false
        fi

        # Should list tags applied
        if ! echo "$OUTPUT" | grep -q "Tags Applied:"; then
            add_warning "Missing 'Tags Applied:' section"
            VALID=false
        fi
        ;;

    "github-searcher")
        # Should have comparison header
        if ! echo "$OUTPUT" | grep -q "### GitHub Comparison:"; then
            add_warning "Missing '### GitHub Comparison:' header"
            VALID=false
        fi

        # Should have recommendation
        if ! echo "$OUTPUT" | grep -qE "LINK ONLY|ENHANCE OURS|BUILD NEW"; then
            add_warning "Missing recommendation (LINK ONLY / ENHANCE OURS / BUILD NEW)"
            VALID=false
        fi
        ;;
esac

# General format checks (all agents)

# Check for proper markdown headers
if ! echo "$OUTPUT" | grep -qE "^#{1,3} "; then
    add_warning "No markdown headers found (expected # ## or ###)"
fi

# Check for reasonable length
OUTPUT_LENGTH=$(echo "$OUTPUT" | wc -c)
if [ "$OUTPUT_LENGTH" -lt 100 ]; then
    add_warning "Output suspiciously short (<100 chars)"
fi

# Check for placeholder text
if echo "$OUTPUT" | grep -qiE "\{.*\}|TODO|FIXME|XXX"; then
    add_warning "Output contains placeholders or TODO markers"
fi

# Print validation results
if [ "$VALID" = false ]; then
    echo -e "\n❌ Format Validation Failed"
    echo -e "$WARNINGS"
    echo ""
    echo "Agent: $AGENT"
    echo "Output length: $OUTPUT_LENGTH chars"
    echo ""
    echo "⚠️  Output may not match expected format."
    echo "    Continuing anyway, but results may be unparseable."
    echo ""
else
    # Silent success (only warn on issues)
    :
fi

# Always allow execution to continue (warnings only)
exit 0
