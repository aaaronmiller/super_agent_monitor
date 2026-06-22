#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "PyMuPDF",
# ]
# ///

"""
Parse PDF Tool

Extracts text content from PDF documents.

Usage:
    uv run scripts/tools/parse_pdf.py --path "/path/to/doc.pdf" --json
    uv run scripts/tools/parse_pdf.py --help
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional


def parse_pdf(
    path: str,
    pages: Optional[str] = None,
    extract_images: bool = False
) -> dict:
    """Parse PDF and return structured content."""
    try:
        import fitz  # PyMuPDF
        
        doc_path = Path(path)
        if not doc_path.exists():
            return {
                "success": False,
                "data": None,
                "error": f"File not found: {path}"
            }
        
        doc = fitz.open(path)
        
        # Parse page range
        if pages:
            if '-' in pages:
                start, end = pages.split('-')
                page_range = range(int(start) - 1, int(end))
            else:
                page_range = [int(pages) - 1]
        else:
            page_range = range(len(doc))
        
        # Extract text from pages
        text_content = []
        for page_num in page_range:
            if 0 <= page_num < len(doc):
                page = doc[page_num]
                text_content.append({
                    "page": page_num + 1,
                    "text": page.get_text()
                })
        
        full_text = "\n\n".join(p["text"] for p in text_content)
        
        # Limit text length
        if len(full_text) > 50000:
            full_text = full_text[:50000] + "...[truncated]"
        
        return {
            "success": True,
            "data": {
                "path": str(path),
                "filename": doc_path.name,
                "total_pages": len(doc),
                "pages_extracted": len(text_content),
                "text_length": len(full_text),
                "text": full_text,
                "metadata": dict(doc.metadata) if doc.metadata else {}
            },
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Parse PDF documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--path', '-p', required=True, help='Path to PDF file')
    parser.add_argument('--pages', type=str, default=None, help='Page range (e.g., "1-5" or "3")')
    parser.add_argument('--extract-images', action='store_true', help='Extract images (not implemented)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = parse_pdf(args.path, args.pages, args.extract_images)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"File: {result['data']['filename']}")
            print(f"Pages: {result['data']['total_pages']}")
            print("-" * 40)
            print(result['data']['text'][:1000])
        else:
            print(f"Error: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
