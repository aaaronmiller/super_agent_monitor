#!/usr/bin/env python3
"""
Fetch URL Script
Downloads content from a URL with smart content extraction

Usage: fetch-url.py <url> [--format=text|markdown|json]
"""

import argparse
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

USER_AGENT = "Mozilla/5.0 (compatible; SuperAgentMonitor/1.0; +https://github.com/super-agent-monitor)"

def fetch_url(url: str, format: str = "text", timeout: int = 10) -> str:
    """
    Fetch content from URL and format it

    Args:
        url: URL to fetch
        format: Output format (text, markdown, json)
        timeout: Request timeout in seconds

    Returns:
        Formatted content
    """
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme in ["http", "https"]:
        raise ValueError("URL must start with http:// or https://")

    # Fetch content
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
        allow_redirects=True
    )
    response.raise_for_status()

    # Check content type
    content_type = response.headers.get("Content-Type", "").lower()

    # JSON responses
    if "application/json" in content_type:
        if format == "json":
            return response.text
        else:
            data = response.json()
            return json.dumps(data, indent=2)

    # HTML responses
    if "text/html" in content_type:
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script, style, and nav elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        if format == "markdown":
            return html_to_markdown(soup)
        elif format == "json":
            return json.dumps({
                "title": soup.title.string if soup.title else "",
                "text": soup.get_text(separator="\n", strip=True),
                "links": [a.get("href") for a in soup.find_all("a", href=True)]
            }, indent=2)
        else:  # text
            return soup.get_text(separator="\n", strip=True)

    # Plain text responses
    if "text/plain" in content_type or "text/markdown" in content_type:
        return response.text

    # Default: return raw content
    return response.text

def html_to_markdown(soup: BeautifulSoup) -> str:
    """Convert HTML to markdown (simple conversion)"""
    lines = []

    # Title
    if soup.title:
        lines.append(f"# {soup.title.string}\n")

    # Find main content (try common containers)
    main_content = (
        soup.find("main") or
        soup.find("article") or
        soup.find("div", class_=["content", "main-content", "post-content"]) or
        soup.find("body")
    )

    if not main_content:
        main_content = soup

    # Convert headings
    for i in range(1, 7):
        for heading in main_content.find_all(f"h{i}"):
            lines.append(f"{'#' * i} {heading.get_text(strip=True)}\n")

    # Convert paragraphs
    for p in main_content.find_all("p"):
        text = p.get_text(strip=True)
        if text:
            lines.append(f"{text}\n")

    # Convert lists
    for ul in main_content.find_all("ul"):
        for li in ul.find_all("li", recursive=False):
            lines.append(f"- {li.get_text(strip=True)}")
        lines.append("")

    for ol in main_content.find_all("ol"):
        for i, li in enumerate(ol.find_all("li", recursive=False), 1):
            lines.append(f"{i}. {li.get_text(strip=True)}")
        lines.append("")

    # Convert code blocks
    for pre in main_content.find_all("pre"):
        code = pre.find("code")
        if code:
            lines.append(f"```\n{code.get_text()}\n```\n")
        else:
            lines.append(f"```\n{pre.get_text()}\n```\n")

    # Convert links
    for a in main_content.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a.get("href")
        if text and href:
            lines.append(f"[{text}]({href})")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch content from URL and format it"
    )
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument(
        "--format",
        choices=["text", "markdown", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )

    args = parser.parse_args()

    try:
        content = fetch_url(args.url, format=args.format, timeout=args.timeout)
        print(content)
        sys.exit(0)
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {args.timeout}s", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
