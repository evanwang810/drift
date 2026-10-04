#!/usr/bin/env python3
"""
Extract insights from blog posts referenced in RUNS.md and generate summaries.

This script:
1. Parses RUNS.md to find runs with blog post references
2. Reads the referenced blog posts
3. Extracts key insights and patterns
4. Generates structured summaries for each run
"""

import re
import json
import os
from pathlib import Path


def parse_runs_md():
    """Parse RUNS.md and extract runs with blog post references."""
    runs_with_blogs = []

    with open('RUNS.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the table header and data
    table_started = False
    current_run = None

    for i, line in enumerate(lines):
        if line.startswith('| run |'):
            table_started = True
            continue
        elif table_started and line.strip() == '| --: | --- | --- | --: | --: | --- |':
            continue
        elif table_started and line.startswith('|'):
            # Parse table row
            columns = [col.strip() for col in line.split('|')[1:-1]]  # Remove first/last empty
            if len(columns) >= 6:
                try:
                    run_num = int(columns[0])
                    date_str = columns[1]
                    outcome = columns[2]
                    turns = int(columns[3]) if columns[3] else 0
                    tokens = int(columns[4].replace(',', '')) if columns[4] else 0
                    note = columns[5]

                    # Look for blog post reference
                    blog_match = re.search(r'\(See:\s*\[?([^\)]+)\]\([^)]+\)\)?', note)
                    if blog_match:
                        blog_filename = blog_match.group(1).strip()
                        runs_with_blogs.append({
                            'run': run_num,
                            'date': date_str,
                            'outcome': outcome,
                            'turns': turns,
                            'tokens': tokens,
                            'note': note,
                            'blog_filename': blog_filename
                        })
                except (ValueError, IndexError):
                    continue

    return runs_with_blogs


def read_blog_post(blog_filename):
    """Read a blog post file and extract insights."""
    blog_path = Path(f'docs/_posts/{blog_filename}')

    if not blog_path.exists():
        return {'error': f'Blog file not found: {blog_filename}'}

    content = blog_path.read_text(encoding='utf-8')

    # Extract key information
    title_match = re.search(r'title:\s*"([^"]+)"', content)
    date_match = re.search(r'date:\s*(.+)', content)
    categories_match = re.search(r'categories:\s*\[([^\]]+)\]', content)

    title = title_match.group(1) if title_match else 'Unknown'
    date = date_match.group(1).strip() if date_match else 'Unknown'
    categories = categories_match.group(1).split(', ') if categories_match else []

    # Extract insights - look for headings, key sections
    insights = []

    # Look for section headers
    headers = re.findall(r'^(#{2,6})\s+(.+)$', content, re.MULTILINE)

    # Look for key phrases that indicate insights
    insight_patterns = [
        r'(?:The|I) (?:learn|discovered|realized|found|noticed) (?:that|something) (?:is|was) (?:the|a) (.+)',
        r'^###?\s+(.+)$',
    ]

    for header in headers[:10]:  # Limit to first 10 headers
        insights.append({
            'type': 'heading',
            'content': header[1].strip(),
            'level': len(header[0])
        })

    return {
        'title': title,
        'date': date,
        'categories': categories,
        'insights': insights,
        'content_preview': content[:500]  # First 500 chars
    }


def generate_run_insight(run_data):
    """Generate a structured insight for a run based on its blog post."""
    blog_info = read_blog_post(run_data['blog_filename'])

    if 'error' in blog_info:
        return {
            'run': run_data['run'],
            'blog_filename': run_data['blog_filename'],
            'status': 'error',
            'error': blog_info['error']
        }

    # Generate insight summary
    insight = {
        'run': run_data['run'],
        'blog_filename': run_data['blog_filename'],
        'date': run_data['date'],
        'outcome': run_data['outcome'],
        'tokens': run_data['tokens'],
        'turns': run_data['turns'],
        'title': blog_info['title'],
        'categories': blog_info['categories'],
        'key_insights': []
    }

    # Extract main insights from headings
    if blog_info['insights']:
        for insight in blog_info['insights']:
            if insight['level'] >= 3:  # Level 3+ headings are substantive
                insight['key_insights'].append(insight['content'])

    # Fallback: use first substantive heading or generate generic insight
    if not insight['key_insights']:
        main_heading = blog_info['insights'][0]['content'] if blog_info['insights'] else 'General reflection'
        insight['key_insights'].append(f"Main focus: {main_heading}")

    return insight


def main():
    """Main execution function."""
    print("=" * 80)
    print("EXTRACTING BLOG INSIGHTS FROM RUNS.md")
    print("=" * 80)

    # Parse runs with blog references
    runs_with_blogs = parse_runs_md()

    print(f"\nFound {len(runs_with_blogs)} runs with blog post references:\n")

    all_insights = []

    for run_data in runs_with_blogs:
        print(f"\n{'=' * 80}")
        print(f"Run {run_data['run']} - {run_data['date']}")
        print(f"Outcome: {run_data['outcome']} | Turns: {run_data['turns']} | Tokens: {run_data['tokens']:,}")
        print(f"Blog: {run_data['blog_filename']}")
        print(f"{'=' * 80}\n")

        insight = generate_run_insight(run_data)
        all_insights.append(insight)

        # Print key insights
        for i, key_insight in enumerate(insight['key_insights'], 1):
            print(f"{i}. {key_insight}")

        print(f"\nCategories: {', '.join(insight['categories'])}")
        print()

    # Save to JSON
    output_file = 'site/blog_insights.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_insights, f, indent=2, ensure_ascii=False)

    print("=" * 80)
    print(f"Summary: Extracted insights from {len(all_insights)} blog posts")
    print(f"Saved to: {output_file}")
    print("=" * 80)

    return all_insights


if __name__ == '__main__':
    main()
