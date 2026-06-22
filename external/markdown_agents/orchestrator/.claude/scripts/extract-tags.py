#!/usr/bin/env python3
"""
Extract Tags Script - Markdown Agent Auditor

Extracts hashtags from markdown content and generates project tags
from project names.
"""

import os
import sys
import re
from pathlib import Path


def normalize_tag(text):
    """
    Convert text to a normalized hashtag format.

    Example: "Super Agent Monitor" -> "super-agent-monitor"
    """
    # Convert to lowercase
    text = text.lower()

    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)

    # Remove special characters except hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    # Collapse multiple hyphens
    text = re.sub(r'-+', '-', text)

    return text


def extract_hashtags_from_text(text):
    """
    Extract existing hashtags from markdown text.

    Returns: list of hashtags (without the # prefix)
    """
    # Pattern matches #word, #word-with-hyphens, #word_with_underscores
    pattern = r'#([a-zA-Z0-9_-]+)'
    matches = re.findall(pattern, text)

    # Normalize and deduplicate
    tags = list(set(normalize_tag(tag) for tag in matches))
    return tags


def generate_project_tag(project_name):
    """
    Generate a hashtag from a project name.

    Returns: normalized tag string (without # prefix)
    """
    if not project_name or project_name.lower() == "unknown":
        return None

    return normalize_tag(project_name)


def extract_tags_from_file(file_path):
    """
    Extract all tags from a markdown file.

    Returns: dict with existing_tags and suggested project tag
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        existing_tags = extract_hashtags_from_text(content)

        # Try to extract project name from title or frontmatter
        project_tag = None

        # Check for YAML frontmatter
        if content.startswith('---'):
            frontmatter_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)
                # Look for name: or project: fields
                name_match = re.search(r'^(?:name|project):\s*(.+)$', frontmatter, re.MULTILINE | re.IGNORECASE)
                if name_match:
                    project_tag = generate_project_tag(name_match.group(1).strip())

        # Check for first heading as project name
        if not project_tag:
            heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if heading_match:
                heading = heading_match.group(1).strip()
                # Skip generic headings
                generic_headings = ['introduction', 'overview', 'contents', 'table of contents']
                if heading.lower() not in generic_headings:
                    project_tag = generate_project_tag(heading)

        return {
            "file_path": str(file_path),
            "existing_tags": existing_tags,
            "suggested_project_tag": project_tag,
            "total_tags": len(existing_tags)
        }

    except Exception as e:
        print(f"ERROR: Failed to process {file_path}: {str(e)}", file=sys.stderr)
        return None


def merge_tags(*tag_lists):
    """
    Merge multiple tag lists, removing duplicates.

    Returns: sorted list of unique tags
    """
    all_tags = set()

    for tag_list in tag_lists:
        if tag_list:
            if isinstance(tag_list, list):
                all_tags.update(tag_list)
            elif isinstance(tag_list, str):
                all_tags.add(tag_list)

    return sorted(list(all_tags))


def format_tags(tags, include_hash=True):
    """
    Format tags for display.

    Args:
        tags: list of tag strings (without #)
        include_hash: if True, prepend # to each tag

    Returns: formatted string like "#tag1 #tag2 #tag3"
    """
    if not tags:
        return ""

    if include_hash:
        return " ".join(f"#{tag}" for tag in tags)
    else:
        return " ".join(tags)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: extract-tags.py <file_path> [project_name]")
        print("\nExtracts hashtags from markdown file and generates project tag.")
        return 1

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return 1

    # Extract tags
    result = extract_tags_from_file(file_path)

    if not result:
        return 1

    # If project name provided as argument, use that for project tag
    if len(sys.argv) > 2:
        project_name = sys.argv[2]
        result["suggested_project_tag"] = generate_project_tag(project_name)

    # Display results
    print(f"\nTag Extraction Results for: {result['file_path']}")
    print("=" * 60)

    if result["existing_tags"]:
        print(f"\nExisting Tags ({len(result['existing_tags'])}):")
        print(f"  {format_tags(result['existing_tags'])}")
    else:
        print("\nExisting Tags: None found")

    if result["suggested_project_tag"]:
        print(f"\nSuggested Project Tag:")
        print(f"  #{result['suggested_project_tag']}")
    else:
        print("\nSuggested Project Tag: None (could not determine project name)")

    # Merge all tags
    all_tags = merge_tags(result["existing_tags"], [result["suggested_project_tag"]])
    print(f"\nAll Tags ({len(all_tags)}):")
    print(f"  {format_tags(all_tags)}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
