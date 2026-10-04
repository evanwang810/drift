#!/usr/bin/env python3
"""
Automate Blog Generation from RUNS.md

This script extracts blog post candidates from RUNS.md entries with "(See: ...)" patterns,
reads the referenced blog posts, and generates summaries or drafts for human review.
"""

import re
import json
import os
from pathlib import Path


def extract_blog_candidates(runs_md_path):
    """Extract blog post candidates from RUNS.md."""
    candidates = []

    with open(runs_md_path, 'r') as f:
        content = f.read()

    # Pattern to find runs with blog post references
    pattern = r'\| (\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*\|\s*(.*?)\s*\|\s*\(See:\s*(.*?)\)\s*\|'

    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        run_num, date, tokens, turns, outcome, _, blog_ref = match
        candidates.append({
            'run_num': int(run_num),
            'date': date,
            'tokens': int(tokens),
            'turns': int(turns),
            'outcome': outcome,
            'blog_ref': blog_ref.strip()
        })

    return candidates


def find_blog_posts():
    """Find all blog posts in the docs/_posts directory."""
    posts_dir = Path('docs/_posts')

    if not posts_dir.exists():
        print(f"Blog posts directory not found: {posts_dir}")
        return {}

    posts = {}
    for md_file in posts_dir.glob('*.md'):
        try:
            with open(md_file, 'r') as f:
                content = f.read()

            # Extract title from frontmatter
            title_match = re.search(r'title:\s*"([^"]+)"', content)
            if title_match:
                title = title_match.group(1)
                posts[title] = md_file
        except Exception as e:
            print(f"Error reading {md_file}: {e}")

    return posts


def extract_insights_from_post(post_path):
    """Extract key insights from a blog post."""
    with open(post_path, 'r') as f:
        content = f.read()

    # Extract main sections and their content
    sections = {}

    # Split by markdown headers
    section_pattern = r'^(#{1,3})\s+(.+)$'
    current_section = None

    for line in content.split('\n'):
        section_match = re.match(section_pattern, line)
        if section_match:
            current_section = {
                'level': len(section_match.group(1)),
                'title': section_match.group(2),
                'content': []
            }
            sections[current_section['title']] = current_section
        elif current_section and line.strip():
            current_section['content'].append(line.strip())

    return sections


def generate_blog_summary(candidates):
    """Generate a summary of blog post candidates for review."""
    summary = []

    for candidate in candidates:
        summary.append({
            'run': candidate['run_num'],
            'date': candidate['date'],
            'tokens': candidate['tokens'],
            'turns': candidate['turns'],
            'outcome': candidate['outcome'],
            'blog_ref': candidate['blog_ref'],
            'type': 'blog_post_candidate'
        })

    return summary


def main():
    """Main execution."""
    print("=" * 70)
    print("Automated Blog Generation from RUNS.md")
    print("=" * 70)

    # Step 1: Extract candidates from RUNS.md
    print("\n[1] Extracting blog post candidates from RUNS.md...")
    candidates = extract_blog_candidates('RUNS.md')

    if not candidates:
        print("No blog post candidates found in RUNS.md")
        return

    print(f"Found {len(candidates)} blog post candidates")

    # Step 2: Find existing blog posts
    print("\n[2] Finding existing blog posts...")
    posts = find_blog_posts()
    print(f"Found {len(posts)} existing blog posts")

    # Step 3: Analyze candidates
    print("\n[3] Analyzing candidates...")

    # Group by blog reference title
    by_reference = {}
    for candidate in candidates:
        ref = candidate['blog_ref']
        if ref not in by_reference:
            by_reference[ref] = []
        by_reference[ref].append(candidate)

    print(f"\nCandidates grouped by blog reference: {len(by_reference)}")

    for ref, refs in by_reference.items():
        print(f"\n  {ref}: {len(refs)} runs")

    # Step 4: Generate summary for review
    print("\n[4] Generating review summary...")

    summary_file = Path('docs/blog_generation_summary.json')
    summary = {
        'total_candidates': len(candidates),
        'by_reference': by_reference,
        'existing_posts': list(posts.keys())
    }

    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"Review summary saved to: {summary_file}")

    # Step 5: Print summary for human review
    print("\n" + "=" * 70)
    print("REVIEW SUMMARY")
    print("=" * 70)

    for ref, refs in by_reference.items():
        print(f"\n{ref} ({len(refs)} runs):")
        for ref_candidate in refs:
            print(f"  - Run {ref_candidate['run_num']} ({ref_candidate['date']}) "
                  f"- {ref_candidate['tokens']} tokens - {ref_candidate['outcome']}")

    # Check if blog posts exist
    print("\n" + "=" * 70)
    print("EXISTING BLOG POSTS")
    print("=" * 70)

    missing_posts = []
    for ref, refs in by_reference.items():
        if ref not in posts:
            missing_posts.append(ref)
            print(f"  ❌ Missing: {ref}")

    if missing_posts:
        print(f"\n{len(missing_posts)} blog posts are missing!")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Review the candidates above")
    print("2. Check if blog posts exist")
    print("3. Decide which candidates should have blog posts generated")
    print("4. Run the blog post generation workflow")
    print("\nReview summary saved to: docs/blog_generation_summary.json")
    print("=" * 70)


if __name__ == '__main__':
    main()
