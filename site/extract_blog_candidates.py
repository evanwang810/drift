#!/usr/bin/env python3
"""
Extract blog post candidates from RUNS.md entries.

This script identifies runs that have "(See: ...)" patterns referencing blog posts,
and extracts the relevant information for potential blog post generation.
"""

import re
from pathlib import Path

def extract_blog_candidates():
    """Extract blog post candidates from RUNS.md."""

    # Read RUNS.md
    runs_path = Path('RUNS.md')
    content = runs_path.read_text()

    # Pattern: run number, date, outcome, turns, tokens, note with (See: ...)
    # Looking for lines that end with "(See: ([filename](path)))" pattern
    # The pattern: | run | date | outcome | turns | tokens | note (See: (filename)) |
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

if __name__ == '__main__':
    candidates = extract_blog_candidates()

    print(f"Found {len(candidates)} blog post candidates:")
    print("=" * 80)

    for c in candidates:
        print(f"\nRun {c['run']}: {c['date']}")
        print(f"  Outcome: {c['outcome']}")
        print(f"  Turns: {c['turns']}, Tokens: {c['tokens']}")
        print(f"  Post: {c['post_file']}")
        print(f"  Note: {c['note'][:80]}..." if len(c['note']) > 80 else f"  Note: {c['note']}")
