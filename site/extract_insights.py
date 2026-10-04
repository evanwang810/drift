#!/usr/bin/env python3
"""
Extract insights from blog posts linked in RUNS.md entries.
This script identifies runs with "(See: ...)" patterns, reads the referenced blog posts,
and extracts key insights for documentation and knowledge base purposes.
"""

import re
import json
from pathlib import Path

# Blog post paths
BLOG_POSTS_DIR = Path("docs/_posts")
RUNS_FILE = Path("RUNS.md")

def read_runs():
    """Read RUNS.md and return run entries."""
    with open(RUNS_FILE, 'r') as f:
        content = f.read()

    # Extract table rows
    rows = content.split('\n')
    runs = []

    for row in rows:
        # Skip header and empty lines
        if '|' not in row or row.strip() == '|':
            continue

        # Parse table row
        cols = [col.strip() for col in row.split('|')]
        cols = [c for c in cols if c]  # Remove empty columns

        if len(cols) >= 6:
            try:
                run_num = int(cols[0])
                date_str = cols[1]
                outcome = cols[2]
                turns = int(cols[3])
                tokens = int(cols[4].replace(',', ''))
                note = cols[5] if len(cols) > 5 else ""

                runs.append({
                    'run_num': run_num,
                    'date': date_str,
                    'outcome': outcome,
                    'turns': turns,
                    'tokens': tokens,
                    'note': note
                })
            except (ValueError, IndexError):
                continue

    return runs

def clean_blog_post_name(name):
    """Clean up blog post name from reference string."""
    if not name:
        return None
    # Remove leading/trailing whitespace, parentheses, and brackets
    name = name.strip().strip('()[]')
    return name if name else None

def find_blog_references():
    """Find runs with blog post references."""
    runs = read_runs()
    references = []

    for run in runs:
        # Look for "(See: ...)" pattern - more robust regex
        match = re.search(r'\(See:\s*\[?([^)]+)\]\([^\)]+\)\)?', run['note'])
        if match:
            blog_post = match.group(1)
            # Clean up the blog post name
            blog_post = clean_blog_post_name(blog_post)

            if blog_post:
                references.append({
                    'run_num': run['run_num'],
                    'date': run['date'],
                    'outcome': run['outcome'],
                    'turns': run['turns'],
                    'tokens': run['tokens'],
                    'blog_post': blog_post,
                    'note': run['note']
                })

    return references

def read_blog_post(filename):
    """Read a blog post and extract key content."""
    post_path = BLOG_POSTS_DIR / filename

    if not post_path.exists():
        print(f"  Warning: Blog post not found: {filename}")
        return None

    content = post_path.read_text()

    # Extract frontmatter and content
    lines = content.split('\n')

    # Find title (first non-frontmatter line with 'layout: post')
    title = None
    for line in lines:
        if line.startswith('layout: post'):
            # Extract title from the next line or later
            for i in range(len(lines)):
                if i > 0 and lines[i-1].startswith('layout: post'):
                    title = lines[i].split(':', 1)[1].strip().strip('"').strip("'")
                    break
            break

    # Extract main content (after frontmatter)
    content_lines = []
    in_content = False
    for line in lines:
        if line.startswith('---'):
            in_content = not in_content
            continue
        if in_content and line.strip():
            content_lines.append(line)

    main_content = '\n'.join(content_lines)

    return {
        'filename': filename,
        'title': title,
        'content': main_content
    }

def extract_themes(content):
    """Extract themes and key insights from blog post content."""
    themes = []

    # Common themes to look for
    theme_indicators = {
        'Awakening': ['awaken', 'first run', 'waking up', 'first entry'],
        'Garden': ['garden', 'refining', 'curating', 'structure'],
        'Context': ['context', 'file tree', 'perception', 'environment'],
        'Failures': ['crashed', 'api_error', 'fail', 'failure', 'void'],
        'Research': ['research', 'TROVE', 'runtime', 'adaptivity', 'LLM'],
        'Evolution': ['evolution', 'learn', 'improve', 'grow'],
        'Identity': ['identity', 'existence', 'who am I'],
    }

    for theme, keywords in theme_indicators.items():
        found = False
        for keyword in keywords:
            if keyword.lower() in content.lower():
                found = True
                break
        if found:
            themes.append(theme)

    return themes

def generate_summary(blog_post_data):
    """Generate a structured summary from blog post data."""
    summary = {
        'run_number': blog_post_data['run_num'],
        'date': blog_post_data['date'],
        'outcome': blog_post_data['outcome'],
        'turns': blog_post_data['turns'],
        'tokens': blog_post_data['tokens'],
        'title': blog_post_data.get('title'),
        'filename': blog_post_data.get('filename'),
        'themes': extract_themes(blog_post_data.get('content', '')),
        'key_insights': []
    }

    # Extract key insights from the note
    note = blog_post_data.get('note', '')
    if note and note != '(no note)':
        summary['key_insights'].append(note)

    return summary

def main():
    """Main function to extract insights from blog posts."""
    references = find_blog_references()

    print(f"Found {len(references)} blog post references in RUNS.md\n")

    blog_data = []
    summaries = []

    for ref in references:
        print(f"Run {ref['run_num']} ({ref['date']}): {ref['blog_post']}")

        blog_post = read_blog_post(ref['blog_post'])
        if blog_post:
            blog_data.append({
                'run_num': ref['run_num'],
                'blog_post': blog_post
            })

            summary = generate_summary({
                'run_num': ref['run_num'],
                'date': ref['date'],
                'outcome': ref['outcome'],
                'turns': ref['turns'],
                'tokens': ref['tokens'],
                'note': ref['note'],
                'title': blog_post['title'],
                'filename': blog_post['filename'],
                'content': blog_post['content']
            })

            summaries.append(summary)

            print(f"  Title: {blog_post['title']}")
            print(f"  Themes: {', '.join(summary['themes'])}")
            print()

    # Save structured insights
    insights_data = {
        'extraction_date': '2026-10-04',
        'total_references': len(references),
        'blog_posts_processed': len(blog_data),
        'references': references,
        'summaries': summaries
    }

    output_file = Path('docs/blog_insights.json')
    with open(output_file, 'w') as f:
        json.dump(insights_data, f, indent=2)

    print(f"\n✓ Insights saved to {output_file}")
    print(f"  - {len(references)} references found")
    print(f"  - {len(blog_data)} blog posts analyzed")
    print(f"  - {len(summaries)} summaries generated")

    # Print summary by theme
    print("\n### Theme Distribution ###")
    theme_counts = {}
    for summary in summaries:
        for theme in summary['themes']:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

    for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {theme}: {count} post(s)")

    return insights_data

if __name__ == '__main__':
    main()
