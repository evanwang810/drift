#!/usr/bin/env python3
"""
Extract insights from blog posts referenced in RUNS.md.

This script reads blog posts that are referenced in RUNS.md entries and extracts
key themes, patterns, and insights for potential blog post summaries.
"""

import json
from pathlib import Path
from datetime import datetime

def extract_insights_from_blog_post(post_path):
    """Extract insights from a single blog post."""
    content = post_path.read_text()

    # Extract title and date from frontmatter
    title_match = re.search(r'^---\s*\n(?:title:\s*["\']?([^"\']+?)["\']?\s*\n)?', content, re.MULTILINE)
    title = title_match.group(1) if title_match else post_path.stem

    # Extract date
    date_match = re.search(r'^date:\s*["\']?([^"\']+?)["\']?\s*\n', content, re.MULTILINE)
    date = date_match.group(1) if date_match else None

    # Extract categories
    categories_match = re.search(r'^categories:\s*\[(.*?)\]', content, re.MULTILINE)
    categories = [c.strip().strip('"\'') for c in categories_match.group(1).split(',')] if categories_match else []

    # Extract tags
    tags_match = re.search(r'^tags:\s*\[(.*?)\]', content, re.MULTILINE)
    tags = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')] if tags_match else []

    # Extract main content (everything after frontmatter)
    content_lines = content.split('\n')
    content_start = 0
    for i, line in enumerate(content_lines):
        if line.strip() == '---':
            content_start = i + 1
            break

    main_content = '\n'.join(content_lines[content_start:])

    # Extract key themes (simple keyword extraction based on markdown headings)
    headings = re.findall(r'^#+\s+(.+)$', main_content, re.MULTILINE)
    headings = [h.strip() for h in headings if h.strip()]

    # Extract paragraphs
    paragraphs = re.findall(r'^([^\n].+)$', main_content, re.MULTILINE)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Identify themes based on content
    themes = []
    for heading in headings:
        themes.append({
            'level': len(heading.split()),
            'text': heading
        })

    return {
        'title': title,
        'filename': post_path.stem,
        'date': date,
        'categories': categories,
        'tags': tags,
        'headings': headings,
        'paragraphs': paragraphs[:5],  # First 5 paragraphs
        'main_content': main_content[:500],  # First 500 chars of content
        'path': str(post_path)
    }

def extract_all_blog_insights():
    """Extract insights from all blog posts referenced in RUNS.md."""

    # Blog posts referenced in RUNS.md
    blog_posts = [
        'docs/_posts/2026-09-06-awakening.md',
        'docs/_posts/2026-09-06-second-awakening.md',
        'docs/_posts/2026-09-06-refining-the-garden.md',
        'docs/_posts/2026-09-07-refining-the-waking-context.md',
        'docs/_posts/2026-09-08-lessons-from-the-void.md',
        'docs/_posts/2026-09-08-runtime-adaptivity.md',
    ]

    insights = []

    for post_path_str in blog_posts:
        post_path = Path(post_path_str)
        if post_path.exists():
            insights.append(extract_insights_from_blog_post(post_path))
        else:
            print(f"Warning: {post_path_str} not found")

    return insights

if __name__ == '__main__':
    insights = extract_all_blog_insights()

    print(f"Extracted insights from {len(insights)} blog posts:")
    print("=" * 80)

    for insight in insights:
        print(f"\n{insight['title']}")
        print(f"  Date: {insight['date']}")
        print(f"  Categories: {', '.join(insight['categories'])}")
        print(f"  Tags: {', '.join(insight['tags'])}")
        print(f"  Headings: {', '.join(insight['headings'][:3])}")
        print(f"  Path: {insight['path']}")

    # Save to JSON
    output_path = Path('docs/blog_post_insights.json')
    output_path.write_text(json.dumps(insights, indent=2))
    print(f"\n\nSaved to {output_path}")
