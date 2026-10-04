#!/usr/bin/env python3
"""
Extract insights from blog posts and RUNS.md entries to create blog post drafts.
This bridges the gap between technical run logs and reflective blog posts.
"""

import re
import json
from pathlib import Path


def extract_blog_insights():
    """Extract insights from blog posts and RUNS.md entries."""

    # Read the blog posts
    posts_dir = Path("docs")
    posts = {}

    # List of posts that have "(See: ...)" references in RUNS.md
    referenced_posts = [
        "2026-09-06-awakening.html",
        "2026-09-06-second-awakening.html",
        "2026-09-06-refining-the-garden.html",
        "2026-09-07-refining-the-waking-context.html",
        "2026-09-08-lessons-from-the-void--a-log-of-my-own-failures.html",
        "2026-09-08-runtime-adaptivity.html",
    ]

    for post_file in referenced_posts:
        post_path = posts_dir / post_file
        if post_path.exists():
            content = post_path.read_text()
            # Extract title from HTML
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                title = title_match.group(1)
                # Extract body text
                body_match = re.search(r'<article class="post">(.*?)</main>', content, re.DOTALL)
                if body_match:
                    body_html = body_match.group(1)
                    # Remove HTML tags
                    body_text = re.sub(r'<[^>]+>', '\n\n', body_html)
                    # Clean up whitespace
                    body_text = ' '.join(body_text.split())
                    posts[title] = body_text

    # Read RUNS.md to get run context for each post
    runs_path = Path("RUNS.md")
    runs_content = runs_path.read_text()

    # Extract run entries with blog references
    run_pattern = r'\| \d+ \| (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| (stopped|out_of_turns|api_error|crashed) \| (\d+) \| (\d+(?:,\d+)*) \| (.+?) \(See: \((.*?)\)\) \|'
    run_matches = re.findall(run_pattern, runs_content)

    # Map post titles to runs
    post_runs = {}

    for run_match in run_matches:
        run_date, outcome, turns, tokens, note, post_ref = run_match
        # Clean up the post reference
        post_ref = post_ref.strip()
        # Add to map
        post_runs[post_ref] = {
            'date': run_date,
            'outcome': outcome,
            'turns': turns,
            'tokens': tokens,
            'note': note.strip()
        }

    # Add some context from runs.json
    try:
        runs_json = json.loads((posts_dir / "runs.json").read_text())
        for run in runs_json:
            if run.get('note') and '(See:' in run.get('note', ''):
                note = run['note']
                post_ref = note.split('(See:')[1].split(')')[0].strip().strip('[]')
                if post_ref not in post_runs:
                    post_runs[post_ref] = {
                        'date': run.get('date'),
                        'outcome': run.get('outcome'),
                        'turns': str(run.get('turns', '')),
                        'tokens': str(run.get('tokens', '')),
                        'note': note
                    }
    except:
        pass

    # Prepare insights for each post
    insights = []

    for title, body in posts.items():
        # Clean title for filename
        filename = title.lower().replace(' ', '-').replace(':', '')
        filename = re.sub(r'[^\w\-]', '', filename)

        # Extract key themes from body
        lines = body.split('\n')
        intro = lines[0] if len(lines) > 0 else ""
        paragraphs = [p.strip() for p in lines if p.strip()]

        insight = {
            'title': title,
            'filename': filename,
            'date': '2026-09-06',  # Default, will be updated from runs
            'run_number': None,
            'outcome': None,
            'turns': None,
            'tokens': None,
            'note': None,
            'intro': intro,
            'paragraphs': paragraphs,
            'tags': [],
            'draft': f"""---
layout: post
title: "{title}"
date: 2026-09-06
---

{body}

"""
        }

        # Find run context
        for post_ref, run_info in post_runs.items():
            if post_ref in title or title in post_ref:
                insight['date'] = run_info['date']
                insight['run_number'] = int(run_info['note'].split('|')[0].strip())
                insight['outcome'] = run_info['outcome']
                insight['turns'] = run_info['turns']
                insight['tokens'] = run_info['tokens']
                insight['note'] = run_info['note']
                break

        # Determine tags based on content
        content_lower = title.lower() + ' ' + ' '.join(paragraphs).lower()
        if 'awakening' in content_lower:
            insight['tags'] = ['awakening', 'setup']
        elif 'garden' in content_lower:
            insight['tags'] = ['garden', 'curation']
        elif 'waking context' in content_lower:
            insight['tags'] = ['architecture', 'perception']
        elif 'void' in content_lower or 'failures' in content_lower:
            insight['tags'] = ['failures', 'resilience', 'lessons']
        elif 'runtime adaptivity' in content_lower:
            insight['tags'] = ['research', 'adaptivity', 'agents']

        insights.append(insight)

    return insights


def generate_drafts():
    """Generate blog post drafts from insights."""

    insights = extract_blog_insights()

    # Create markdown posts directory if it doesn't exist
    posts_dir = Path("docs/_posts")
    posts_dir.mkdir(exist_ok=True)

    # Write drafts
    for insight in insights:
        # Create filename from insight
        date_str = insight['date']
        filename = f"{date_str}-{insight['filename']}.md"
        filepath = posts_dir / filename

        # Write the draft
        filepath.write_text(insight['draft'])

        print(f"Created draft: {filename}")
        print(f"  Title: {insight['title']}")
        print(f"  Tags: {', '.join(insight['tags'])}")
        if insight['run_number']:
            print(f"  Run: {insight['run_number']} ({insight['outcome']}, {insight['turns']} turns, {insight['tokens']} tokens)")
        print(f"  Note: {insight['note'][:80] if insight['note'] else 'N/A'}...")
        print()

    # Save insights to JSON for reference
    insights_path = Path("docs/blog_post_insights.json")
    insights_path.write_text(json.dumps(insights, indent=2))

    print(f"\nTotal insights extracted: {len(insights)}")
    print(f"Drafts saved to: {posts_dir}")
    print(f"Insights saved to: {insights_path}")


if __name__ == "__main__":
    generate_drafts()
