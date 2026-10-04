#!/usr/bin/env python3
"""
Generate blog post summaries from RUNS.md entries.

This script reads the blog posts referenced in RUNS.md entries and generates
summaries that capture the key insights from the runs.
"""

import re
from pathlib import Path
import json
from datetime import datetime

def extract_blog_candidates():
    """Extract blog post candidates from RUNS.md."""

    runs_path = Path('../RUNS.md')
    if not runs_path.exists():
        print(f"RUNS.md not found at {runs_path}")
        return []
    content = runs_path.read_text()

    # Pattern: run number, date, outcome, turns, tokens, note with (See: ...) pattern
    # Looking for lines ending with (See: ...) pattern - simpler pattern
    pattern = r'\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\(\(See:\s*(.*?)\)\)\s*\|'

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

def read_blog_post(post_path):
    """Read a blog post and return its content."""
    try:
        with open(post_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {post_path}: {e}")
        return None

def extract_insights_from_run(run_data, blog_content):
    """Extract insights from a run entry and corresponding blog post."""

    # Extract key phrases from the run note
    note = run_data['note']
    insights = []

    # Common patterns to extract insights
    patterns = [
        (r'(\w+) (?:improved|refined|enhanced|expanded)', r'\1'),
        (r'(\w+) (?:created|built|added)', r'\1'),
        (r'(\w+) (?:completed|finished)', r'\1'),
        (r'stopped (?:early|as requested)', r'stopped'),
        (r'(\w+) (?:fixed|corrected)', r'\1'),
    ]

    for pattern, replacement in patterns:
        matches = re.findall(pattern, note, re.IGNORECASE)
        if matches:
            insights.extend(matches)

    # Extract insights from blog content
    if blog_content:
        # Look for headings (##) which often contain key themes
        headings = re.findall(r'^##\s+(.+)$', blog_content, re.MULTILINE)
        insights.extend(headings)

        # Look for key phrases
        key_phrases = [
            'insight', 'discovered', 'learned', 'found', 'realized',
            'improved', 'refined', 'enhanced', 'expanded',
            'tool', 'documentation', 'project', 'goal'
        ]

        for phrase in key_phrases:
            if phrase in blog_content.lower():
                # Extract context around the phrase
                match = re.search(
                    r'(\w+\s+\w+)\s+' + phrase + r'\s+(.+?)(?:\.|$)',
                    blog_content,
                    re.IGNORECASE
                )
                if match:
                    insights.append(match.group(0)[:100])

    # Clean and deduplicate insights
    insights = list(set(insights))
    insights = [i for i in insights if len(i) > 3]

    return {
        'run': run_data['run'],
        'date': run_data['date'],
        'outcome': run_data['outcome'],
        'turns': run_data['turns'],
        'tokens': run_data['tokens'],
        'note': note,
        'insights': insights
    }

def main():
    """Main function to generate blog post summaries."""

    print("Extracting blog post candidates from RUNS.md...")
    candidates = extract_blog_candidates()

    print(f"\nFound {len(candidates)} blog post candidates:")
    print("=" * 80)

    # Read blog posts
    print("\nReading blog posts...")
    posts = {}
    posts_dir = Path('docs/posts')

    if posts_dir.exists():
        for post_file in posts_dir.glob('*.md'):
            posts[post_file.name] = read_blog_post(post_file)
    else:
        print(f"Posts directory not found: {posts_dir}")

    # Generate summaries
    summaries = []

    print("\n\nGenerating summaries...")
    print("=" * 80)

    for candidate in candidates:
        post_name = candidate['post_file']
        post_content = posts.get(post_name)

        if post_content:
            print(f"\nProcessing: {post_name}")
            print(f"  Run {candidate['run']}: {candidate['date']}")
            print(f"  Outcome: {candidate['outcome']}")
            print(f"  Turns: {candidate['turns']}, Tokens: {candidate['tokens']}")

            # Extract insights
            summary = extract_insights_from_run(candidate, post_content)
            summaries.append(summary)

            # Display insights
            if summary['insights']:
                print(f"  Insights extracted:")
                for insight in summary['insights'][:5]:
                    print(f"    - {insight}")
            else:
                print(f"  No insights extracted")

    # Save summaries
    output_path = Path('site/blog_summaries.json')
    with open(output_path, 'w') as f:
        json.dump({
            'summary_date': datetime.utcnow().isoformat(),
            'total_candidates': len(candidates),
            'total_summaries': len(summaries),
            'candidates': candidates,
            'summaries': summaries
        }, f, indent=2)

    print(f"\n\nSummaries saved to {output_path}")
    print(f"Generated {len(summaries)} blog post summaries")

if __name__ == '__main__':
    main()
