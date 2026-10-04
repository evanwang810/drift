#!/usr/bin/env python3
"""
Extract insights from blog posts that are linked in RUNS.md.
This creates a bridge between technical run logs and reflective blog posts.
"""

import re
import json
from pathlib import Path

def extract_insights_from_html(html_path):
    """Extract insights and key themes from an HTML blog post."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Unknown"

    # Extract body text
    body_match = re.search(r'<main>\s*<article>(.*?)</article>\s*</main>', content, re.DOTALL)
    if body_match:
        body_html = body_match.group(1)
    else:
        body_html = content

    # Remove HTML tags and clean text
    text = re.sub(r'<[^>]+>', '\n', body_html)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()

    # Extract key sections (h2, h3 headings)
    sections = re.findall(r'<h[23]>(.*?)</h[23]>', body_html, re.DOTALL)
    section_titles = [s.strip() for s in sections]

    # Count paragraphs
    paragraphs = re.findall(r'<p>(.*?)</p>', body_html, re.DOTALL)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Extract date
    date_match = re.search(r'<time>(.*?)</time>', content)
    date = date_match.group(1).strip() if date_match else "Unknown"

    return {
        'title': title,
        'date': date,
        'text': text,
        'paragraphs': paragraphs,
        'section_titles': section_titles,
        'word_count': len(text.split())
    }

def extract_run_blog_connections(runs_path, blog_posts):
    """Extract connections between runs and blog posts from RUNS.md."""
    with open(runs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all (See: ...) patterns
    patterns = re.findall(r'\(See: \((.*?)\)\)', content)

    connections = []
    for pattern in patterns:
        # Extract run number and blog post link
        run_match = re.search(r'(\d+)\s*\|', content, re.DOTALL)
        if run_match:
            run_num = run_match.group(1)

            # Find the blog post in our list
            for post in blog_posts:
                if post['filename'] in pattern:
                    connections.append({
                        'run': run_num,
                        'blog_post': post
                    })
                    break

    return connections

def main():
    runs_path = Path('RUNS.md')
    blog_dir = Path('docs')

    # Find blog post HTML files
    blog_files = list(blog_dir.glob('2026-09-*.html'))

    blog_posts = []
    for html_file in blog_files:
        try:
            insights = extract_insights_from_html(html_file)
            blog_posts.append({
                'filename': html_file.name,
                'html_path': str(html_file),
                'insights': insights
            })
        except Exception as e:
            print(f"Error reading {html_file.name}: {e}")

    print(f"Found {len(blog_posts)} blog posts")
    for post in blog_posts:
        print(f"  - {post['filename']}: {post['insights']['title']}")

    # Extract connections from RUNS.md
    connections = extract_run_blog_connections(runs_path, blog_posts)

    print(f"\nFound {len(connections)} run-blog connections:")
    for conn in connections:
        print(f"  Run {conn['run']} -> {conn['blog_post']['filename']}")

    # Save insights
    output = {
        'blog_posts': [dict(post) for post in blog_posts],
        'connections': connections
    }

    output_path = Path('docs/blog_insights.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved insights to {output_path}")
    print(f"Total blog posts: {len(blog_posts)}")
    print(f"Total connections: {len(connections)}")

if __name__ == '__main__':
    main()
