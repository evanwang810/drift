#!/usr/bin/env python3
"""
Extract blog post candidates from RUNS.md entries.

This script identifies runs that have "(See: ...)" patterns referencing blog posts,
and extracts the relevant information for potential blog post generation.
"""

import re
from pathlib import Path
import json

def extract_blog_candidates():
    """Extract blog post candidates from RUNS.md."""

    # Read RUNS.md
    runs_path = Path('RUNS.md')
    content = runs_path.read_text()

    # Pattern: run number, date, outcome, turns, tokens, note with (See: ...) pattern
    # Looking for lines that end with "(See: ...)" pattern
    # The pattern: | run | date | outcome | turns | tokens | note (See: ...)
    # Note: (See: ) can have double/single parens around the entire link, and can have variations
    pattern = r'\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\(See:\s*(.*?)\)\s*\|'

    candidates = []
    for match in re.finditer(pattern, content, re.DOTALL):
        run_num = match.group(1)
        date = match.group(2)
        outcome = match.group(4)
        turns = match.group(5)
        tokens = match.group(6)
        note = match.group(7).strip(' )')
        post_ref = match.group(8).strip(' ]"\'')

        # Extract just the filename from the reference
        post_filename = post_ref.split('/')[-1].split('\\')[-1] if '/' in post_ref or '\\' in post_ref else post_ref

        candidates.append({
            'run': run_num,
            'date': date,
            'outcome': outcome,
            'turns': turns,
            'tokens': tokens,
            'note': note,
            'post_file': post_filename,
            'post_ref': post_ref
        })

    return candidates

def read_blog_posts(posts_dir='docs/posts'):
    """Read all blog posts and return their content."""
    posts = {}
    posts_path = Path(posts_dir)

    if not posts_path.exists():
        print(f"Posts directory not found: {posts_path}")
        return posts

    for post_file in posts_path.glob('*.md'):
        try:
            content = post_file.read_text()
            posts[post_file.name] = {
                'path': str(post_file),
                'content': content
            }
        except Exception as e:
            print(f"Error reading {post_file}: {e}")

    return posts

def main():
    """Main function to extract candidates and read blog posts."""

    print("Extracting blog post candidates from RUNS.md...")
    candidates = extract_blog_candidates()

    print(f"\nFound {len(candidates)} blog post candidates:")
    print("=" * 80)

    for c in candidates:
        print(f"\nRun {c['run']}: {c['date']}")
        print(f"  Outcome: {c['outcome']}")
        print(f"  Turns: {c['turns']}, Tokens: {c['tokens']}")
        print(f"  Post: {c['post_file']}")
        print(f"  Note: {c['note'][:80]}..." if len(c['note']) > 80 else f"  Note: {c['note']}")

    # Read blog posts
    print("\n\nReading blog posts...")
    posts = read_blog_posts()

    print(f"\nFound {len(posts)} blog posts:")
    print("=" * 80)

    for post_name, post_data in posts.items():
        print(f"\n{post_name}")
        print(f"  Path: {post_data['path']}")
        print(f"  Content preview (first 200 chars):")
        print(f"  {post_data['content'][:200]}...")

    # Save candidates to JSON for reference
    output_path = Path('site/blog_candidates.json')
    with open(output_path, 'w') as f:
        json.dump({
            'candidates': candidates,
            'posts': {name: {'path': data['path']} for name, data in posts.items()}
        }, f, indent=2)

    print(f"\n\nCandidates saved to {output_path}")

if __name__ == '__main__':
    main()
