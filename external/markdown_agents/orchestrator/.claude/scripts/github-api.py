#!/usr/bin/env python3
"""
GitHub API Helper Script - Markdown Agent Auditor

Helper functions for constructing GitHub search queries and parsing results.
Note: This script provides utilities but does NOT make direct API calls.
The actual searching should be done via WebSearch tool by the agent.
"""

import sys
import re
from urllib.parse import quote


def construct_search_query(project_name, features=None, technologies=None):
    """
    Construct optimized GitHub search queries from project information.

    Args:
        project_name: Name of the project
        features: List of key features (optional)
        technologies: List of technologies used (optional)

    Returns: List of search query strings
    """
    queries = []

    # Clean project name (remove generic terms)
    generic_terms = [
        'system', 'platform', 'tool', 'application', 'app', 'project',
        'service', 'framework', 'library', 'solution'
    ]

    cleaned_name = project_name.lower()
    for term in generic_terms:
        cleaned_name = re.sub(r'\b' + term + r'\b', '', cleaned_name)
    cleaned_name = ' '.join(cleaned_name.split()).strip()

    # Query 1: Project name + site:github.com
    if cleaned_name:
        queries.append(f"{cleaned_name} site:github.com")

    # Query 2: Core features combination
    if features and len(features) >= 2:
        # Take top 2-3 most distinctive features
        feature_terms = []
        for feature in features[:3]:
            # Extract key terms from feature description
            words = re.findall(r'\b\w{4,}\b', feature.lower())
            feature_terms.extend(words[:2])  # Take first 2 significant words

        if feature_terms:
            feature_query = ' '.join(feature_terms[:4])  # Max 4 terms
            queries.append(f"{feature_query} site:github.com")

    # Query 3: Technology stack + domain
    if technologies and cleaned_name:
        # Take most distinctive technology
        distinctive_techs = []
        common_techs = ['python', 'javascript', 'java', 'node', 'react', 'vue']

        for tech in technologies:
            tech_lower = tech.lower()
            # Prioritize less common technologies
            if tech_lower not in common_techs:
                distinctive_techs.append(tech_lower)

        if distinctive_techs:
            tech_query = f"{cleaned_name} {distinctive_techs[0]} site:github.com"
            queries.append(tech_query)

    # Ensure we have at least one query
    if not queries:
        queries.append(f"{project_name} site:github.com")

    return queries


def parse_github_url(url):
    """
    Parse a GitHub repository URL and extract owner and repo name.

    Args:
        url: GitHub repository URL

    Returns: dict with owner and repo, or None if invalid
    """
    # Pattern matches: github.com/owner/repo or github.com/owner/repo/...
    pattern = r'github\.com/([^/]+)/([^/]+)'
    match = re.search(pattern, url)

    if match:
        owner = match.group(1)
        repo = match.group(2).rstrip('/')  # Remove trailing slash if any
        return {
            "owner": owner,
            "repo": repo,
            "full_name": f"{owner}/{repo}",
            "url": f"https://github.com/{owner}/{repo}"
        }

    return None


def extract_repo_info_from_text(text):
    """
    Extract repository information from text (e.g., search results).

    Args:
        text: Text containing GitHub repository mentions

    Returns: list of repo info dicts
    """
    # Find all GitHub URLs in text
    pattern = r'https?://github\.com/[^/\s]+/[^/\s]+'
    urls = re.findall(pattern, text)

    repos = []
    seen = set()

    for url in urls:
        repo_info = parse_github_url(url)
        if repo_info and repo_info['full_name'] not in seen:
            repos.append(repo_info)
            seen.add(repo_info['full_name'])

    return repos


def calculate_overlap_percentage(prd_features, repo_features):
    """
    Calculate feature overlap between PRD and repository.

    Args:
        prd_features: List of features from PRD
        repo_features: List of features from repository

    Returns: dict with overlap statistics
    """
    if not prd_features:
        return {
            "overlap_pct": 0,
            "shared_count": 0,
            "prd_unique_count": 0,
            "repo_unique_count": len(repo_features) if repo_features else 0
        }

    # Normalize features for comparison (lowercase, remove punctuation)
    def normalize(feature_list):
        return [
            re.sub(r'[^\w\s]', '', f.lower()).strip()
            for f in feature_list
        ]

    prd_normalized = normalize(prd_features)
    repo_normalized = normalize(repo_features)

    # Find shared features (exact match or high keyword overlap)
    shared = 0
    for prd_feature in prd_normalized:
        for repo_feature in repo_normalized:
            # Calculate word overlap
            prd_words = set(prd_feature.split())
            repo_words = set(repo_feature.split())

            if prd_words and repo_words:
                overlap = len(prd_words & repo_words) / len(prd_words | repo_words)
                if overlap > 0.5:  # >50% word overlap
                    shared += 1
                    break

    overlap_pct = (shared / len(prd_features)) * 100

    return {
        "overlap_pct": round(overlap_pct, 1),
        "shared_count": shared,
        "prd_unique_count": len(prd_features) - shared,
        "repo_unique_count": len(repo_features) - shared if repo_features else 0
    }


def recommend_action(overlap_pct, repo_quality_score):
    """
    Recommend action based on overlap and quality.

    Args:
        overlap_pct: Feature overlap percentage (0-100)
        repo_quality_score: Repository quality score (0-10)

    Returns: "link_only", "enhance_ours", or "build_new"
    """
    if overlap_pct >= 85 and repo_quality_score >= 7:
        return "link_only"
    elif overlap_pct >= 40:
        return "enhance_ours"
    else:
        return "build_new"


def format_search_queries_for_display(queries):
    """Format search queries for display in markdown."""
    output = "**Search Queries Used**:\n"
    for i, query in enumerate(queries, 1):
        output += f"{i}. \"{query}\"\n"
    return output


def main():
    """Main entry point for testing/demonstration."""
    if len(sys.argv) < 2:
        print("GitHub API Helper - Usage Examples:\n")
        print("1. Generate search queries:")
        print("   python github-api.py query 'Multi-Agent Monitor' 'workflow management,agent coordination' 'Vue,PostgreSQL'\n")
        print("2. Parse GitHub URL:")
        print("   python github-api.py parse 'https://github.com/owner/repo'\n")
        print("3. Calculate overlap:")
        print("   python github-api.py overlap 'feat1,feat2,feat3' 'feat1,feat4,feat5'\n")
        return 1

    command = sys.argv[1]

    if command == "query":
        if len(sys.argv) < 3:
            print("ERROR: Project name required", file=sys.stderr)
            return 1

        project_name = sys.argv[2]
        features = sys.argv[3].split(',') if len(sys.argv) > 3 else None
        technologies = sys.argv[4].split(',') if len(sys.argv) > 4 else None

        queries = construct_search_query(project_name, features, technologies)

        print("\nGenerated Search Queries:")
        print("=" * 60)
        for i, q in enumerate(queries, 1):
            print(f"{i}. {q}")
        print()

    elif command == "parse":
        if len(sys.argv) < 3:
            print("ERROR: URL required", file=sys.stderr)
            return 1

        url = sys.argv[2]
        repo_info = parse_github_url(url)

        if repo_info:
            print("\nParsed Repository Info:")
            print("=" * 60)
            print(f"Owner: {repo_info['owner']}")
            print(f"Repo: {repo_info['repo']}")
            print(f"Full Name: {repo_info['full_name']}")
            print(f"URL: {repo_info['url']}")
            print()
        else:
            print("ERROR: Invalid GitHub URL", file=sys.stderr)
            return 1

    elif command == "overlap":
        if len(sys.argv) < 4:
            print("ERROR: Two feature lists required (comma-separated)", file=sys.stderr)
            return 1

        prd_features = sys.argv[2].split(',')
        repo_features = sys.argv[3].split(',')

        overlap = calculate_overlap_percentage(prd_features, repo_features)

        print("\nFeature Overlap Analysis:")
        print("=" * 60)
        print(f"PRD Features: {len(prd_features)}")
        print(f"Repo Features: {len(repo_features)}")
        print(f"Shared Features: {overlap['shared_count']}")
        print(f"Overlap Percentage: {overlap['overlap_pct']}%")
        print(f"PRD Unique: {overlap['prd_unique_count']}")
        print(f"Repo Unique: {overlap['repo_unique_count']}")

        # Recommendation
        recommendation = recommend_action(overlap['overlap_pct'], 8)  # Assume quality 8 for demo
        print(f"\nRecommendation: {recommendation.upper().replace('_', ' ')}")
        print()

    else:
        print(f"ERROR: Unknown command '{command}'", file=sys.stderr)
        print("Valid commands: query, parse, overlap", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
