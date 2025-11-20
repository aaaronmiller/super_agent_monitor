#!/usr/bin/env python3
"""
Parse PDF Script
Extracts text and metadata from PDF files

Usage: parse-pdf.py <pdf_file> [--format=text|markdown|json]
"""

import argparse
import sys
import json
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 not installed. Run: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)

def extract_pdf_text(pdf_path: str) -> tuple[str, dict]:
    """
    Extract text and metadata from PDF

    Returns:
        (text_content, metadata)
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not path.suffix.lower() == ".pdf":
        raise ValueError(f"Not a PDF file: {pdf_path}")

    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)

        # Extract metadata
        metadata = {
            "title": reader.metadata.get("/Title", "") if reader.metadata else "",
            "author": reader.metadata.get("/Author", "") if reader.metadata else "",
            "subject": reader.metadata.get("/Subject", "") if reader.metadata else "",
            "creator": reader.metadata.get("/Creator", "") if reader.metadata else "",
            "producer": reader.metadata.get("/Producer", "") if reader.metadata else "",
            "pages": len(reader.pages),
        }

        # Extract text from all pages
        text_parts = []
        for page_num, page in enumerate(reader.pages, 1):
            try:
                page_text = page.extract_text()
                if page_text.strip():
                    text_parts.append(f"--- Page {page_num} ---\n{page_text}")
            except Exception as e:
                text_parts.append(f"--- Page {page_num} ---\n[Error extracting text: {e}]")

        full_text = "\n\n".join(text_parts)

    return full_text, metadata

def format_as_markdown(text: str, metadata: dict) -> str:
    """Format PDF content as markdown"""
    lines = []

    # Add metadata header
    if metadata.get("title"):
        lines.append(f"# {metadata['title']}\n")
    else:
        lines.append("# PDF Document\n")

    if metadata.get("author"):
        lines.append(f"**Author**: {metadata['author']}")
    if metadata.get("subject"):
        lines.append(f"**Subject**: {metadata['subject']}")
    if metadata.get("pages"):
        lines.append(f"**Pages**: {metadata['pages']}")

    lines.append("\n---\n")

    # Add content
    lines.append(text)

    return "\n".join(lines)

def format_as_json(text: str, metadata: dict) -> str:
    """Format PDF content as JSON"""
    return json.dumps({
        "metadata": metadata,
        "text": text,
        "length": len(text)
    }, indent=2)

def main():
    parser = argparse.ArgumentParser(
        description="Extract text and metadata from PDF files"
    )
    parser.add_argument("pdf_file", help="Path to PDF file")
    parser.add_argument(
        "--format",
        choices=["text", "markdown", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=None,
        help="Maximum output length in characters (truncate if exceeded)"
    )

    args = parser.parse_args()

    try:
        # Extract PDF content
        text, metadata = extract_pdf_text(args.pdf_file)

        # Truncate if needed
        if args.max_length and len(text) > args.max_length:
            text = text[:args.max_length] + f"\n\n[... truncated at {args.max_length} chars ...]"

        # Format output
        if args.format == "markdown":
            output = format_as_markdown(text, metadata)
        elif args.format == "json":
            output = format_as_json(text, metadata)
        else:  # text
            output = text

        print(output)
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error parsing PDF: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
