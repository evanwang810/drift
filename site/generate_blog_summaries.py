#!/usr/bin/env python3
"""
Generate blog post summaries from RUNS.md entries and referenced blog posts.

This script identifies runs with blog post references, reads the blog posts,
extracts key insights, and generates structured summaries for human review.
"""

import re
import json
from pathlib import Path

def parse_runs_md():
    """Parse RUNS.md and extract entries with blog post references."""
    runs_file = Path("RUNS.md")
    if not runs_file.exists():
        print("ERROR: RUNS.md not found")
        return []

    content = runs_file.read_text()
    lines = content.split('\n')

    # Find the table section
    in_table = False
    in_header = False
    runs_with_refs = []

    for line in lines:
        # Check if we're past the header
        if line.startswith('---'):
            in_header = True
            continue
        
        if in_header and line.startswith('| # |'):
            in_table = True
            continue
        if in_table and line.startswith('| - |'):
            continue
        if in_table and not line.startswith('|'):
            in_table = False
            continue

        if in_table:
            # Parse table row
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                run_num = parts[1]
                date = parts[2]
                outcome = parts[3]
                turns = parts[4]
                tokens = parts[5]
                note = parts[6] if len(parts) > 6 else ""

                # Check for blog post reference
                blog_match = re.search(r'\(See:.*?\.md\)', note)
                if blog_match:
                    blog_ref = blog_match.group(0)
                    runs_with_refs.append({
                        'run_num': run_num,
                        'date': date,
                        'outcome': outcome,
                        'turns': turns,
                        'tokens': tokens,
                        'note': note,
                        'blog_ref': blog_ref
                    })

    return runs_with_refs

def extract_blog_ref_name(blog_ref):
    """Extract the blog post name from the reference string."""
    # Extract between "See:" and ".md)"
    match = re.search(r'\(See:\s*\[(.*?)\]', blog_ref)
    if match:
        return match.group(1)
    return None

def find_blog_post_path(blog_name):
    """Find the path to a blog post given its name."""
    # Try various paths
    paths = [
        Path(f"docs/_posts/{blog_name}"),
        Path(f"docs/{blog_name}"),
        Path(f"docs/posts/{blog_name}"),
    ]

    for path in paths:
        if path.exists():
            return path

    # Try searching in docs/_posts directory
    posts_dir = Path("docs/_posts")
    if posts_dir.exists():
        for file in posts_dir.glob("*.md"):
            # Extract blog name from filename (strip .md and potential prefixes)
            name = file.stem
            # Try to match by looking for blog_name in the filename
            if blog_name.replace("-", " ") in file.stem or blog_name in file.stem:
                return file

    return None

def extract_blog_insights(post_path):
    """Extract insights from a blog post."""
    if not post_path or not post_path.exists():
        return None

    content = post_path.read_text()

    # Extract title and date if present
    title_match = re.search(r'title:\s*"([^"]+)"', content)
    title = title_match.group(1) if title_match else post_path.stem

    # Extract date if present
    date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', content)
    date = date_match.group(1) if date_match else None

    # Extract tags if present
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', content)
    tags = tags_match.group(1).split(', ') if tags_match else []

    # Extract categories if present
    categories_match = re.search(r'categories:\s*\[([^\]]+)\]', content)
    categories = categories_match.group(1).split(', ') if categories_match else []

    # Extract key sections (look for markdown headings)
    sections = []
    for line in content.split('\n'):
        if line.startswith('##'):
            sections.append(line[3:].strip())
        elif line.startswith('###'):
            sections.append(line[4:].strip())

    return {
        'title': title,
        'date': date,
        'tags': tags,
        'categories': categories,
        'sections': sections,
        'excerpt': content[:500]  # First 500 chars as excerpt
    }

def generate_summary(run_info, blog_insights):
    """Generate a summary combining run info and blog insights."""
    if blog_insights:
        return {
            'run_num': run_info['run_num'],
            'date': run_info['date'],
            'outcome': run_info['outcome'],
            'turns': run_info['turns'],
            'tokens': run_info['tokens'],
            'blog_post': blog_insights['title'],
            'date': blog_insights['date'],
            'tags': blog_insights['tags'],
            'categories': blog_insights['categories'],
            'sections': blog_insights['sections'],
            'excerpt': blog_insights['excerpt']
        }
    else:
        return {
            'run_num': run_info['run_num'],
            'date': run_info['date'],
            'outcome': run_info['outcome'],
            'turns': run_info['turns'],
            'tokens': run_info['tokens'],
            'blog_post': 'NOT FOUND',
            'note': run_info['note']
        }

def main():
    """Main function."""
    print("=== Blog Post Summary Generator ===\n")

    # Parse RUNS.md
    runs_with_refs = parse_runs_md()
    print(f"Found {len(runs_with_refs)} runs with blog post references\n")

    summaries = []

    for run_info in runs_with_refs:
        # Extract blog post name from reference
        blog_name = extract_blog_ref_name(run_info['blog_ref'])
        print(f"Run {run_info['run_num']}: Looking for '{blog_name}'...")

        if blog_name:
            # Find blog post file
            post_path = find_blog_post_path(blog_name)
            if post_path:
                print(f"  ✓ Found at: {post_path}")
                blog_insights = extract_blog_insights(post_path)
                if blog_insights:
                    summary = generate_summary(run_info, blog_insights)
                    summaries.append(summary)
                    print(f"  ✓ Extracted insights: {blog_insights['title']}")
            else:
                print(f"  ✗ Blog post not found")
                summary = generate_summary(run_info, None)
                summaries.append(summary)
        else:
            print(f"  ✗ Could not extract blog post name")
            summary = generate_summary(run_info, None)
            summaries.append(summary)

    # Save summaries
    output_file = Path("docs/blog_summaries.json")
    with open(output_file, 'w') as f:
        json.dump(summaries, f, indent=2)

    print(f"\n=== Summary ===")
    print(f"Generated {len(summaries)} blog post summaries")
    print(f"Saved to: {output_file}")

    # Also create markdown summary
    md_file = Path("docs/BLOG_SUMMARIES.md")
    with open(md_file, 'w') as f:
        f.write("# Blog Post Summaries\n\n")
        f.write(f"Generated from {len(summaries)} RUNS.md entries with blog post references.\n\n")
        f.write("---\n\n")

        for summary in summaries:
            f.write(f"## Run {summary['run_num']} ({summary['date']})\n\n")
            f.write(f"**Outcome:** {summary['outcome']} | **Turns:** {summary['turns']} | **Tokens:** {summary['tokens']}\n\n")

            if summary['blog_post'] != 'NOT FOUND':
                f.write(f"### Blog Post: {summary['blog_post']}\n\n")
                if summary['date']:
                    f.write(f"**Date:** {summary['date']}\n\n")
                if summary['tags']:
                    f.write(f"**Tags:** {', '.join(summary['tags'])}\n\n")
                if summary['categories']:
                    f.write(f"**Categories:** {', '.join(summary['categories'])}\n\n")

                if summary['sections']:
                    f.write(f"**Sections:** {', '.join(summary['sections'])}\n\n")

                if summary['excerpt']:
                    f.write(f"**Excerpt:**\n> {summary['excerpt']}\n\n")
            else:
                f.write(f"### Blog Post: NOT FOUND\n\n")
                f.write(f"**Note:** {summary['note']}\n\n")

            f.write("---\n\n")

    print(f"Markdown summary saved to: {md_file}")

    # Display summary
    print(f"\n=== Summary Details ===\n")
    for summary in summaries:
        print(f"Run {summary['run_num']}: {summary['blog_post']}")
        if summary['blog_post'] != 'NOT FOUND':
            print(f"  Date: {summary['date']}")
            print(f"  Tags: {', '.join(summary['tags'])}")
        print()

if __name__ == "__main__":
    main()
