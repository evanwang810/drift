#!/usr/bin/env python3
"""
Generate blog post summaries from RUNS.md entries.

This script extracts runs with "(See: ...)" patterns, reads the referenced
blog posts, and generates structured summaries of the insights contained
in each blog post.

Usage:
    python site/generate_blog_summaries.py
"""

import re
import json
from pathlib import Path
from datetime import datetime


def parse_runs_md():
    """Parse RUNS.md and extract run entries with blog post references."""
    runs_md_path = Path("RUNS.md")

    if not runs_md_path.exists():
        print(f"Error: RUNS.md not found at {runs_md_path}")
        return []

    with open(runs_md_path, 'r') as f:
        content = f.read()

    # Find all run entries with blog post references
    # Pattern: | N | date | outcome | turns | tokens | note (See: (...))
    pattern = r'\| \d+ \| ([\d\-]+[\s:][\d:]+) \| (\w+) \| (\d+) \| ([\d,]+) \| (.*?) \(See:\s*\[([^\]]+)\]\([^)]+\)\)'

    matches = re.findall(pattern, content, re.DOTALL)

    runs_with_blog = []
    for match in matches:
        date_str, outcome, turns, tokens, note, blog_filename = match
        runs_with_blog.append({
            'run_number': int(date_str.split('|')[0].strip()),
            'date': date_str.strip(),
            'outcome': outcome.strip(),
            'turns': int(turns.strip()),
            'tokens': int(tokens.replace(',', '').strip()),
            'note': note.strip(),
            'blog_filename': blog_filename.strip()
        })

    return runs_with_blog


def extract_insights_from_blog(blog_html_path):
    """Extract insights from a blog post HTML file."""
    blog_path = Path(blog_html_path)

    if not blog_path.exists():
        print(f"Warning: Blog post not found at {blog_path}")
        return None

    with open(blog_path, 'r') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Untitled"

    # Extract body text
    body_match = re.search(r'<article class="post">(.*?)</article>', content, re.DOTALL)
    if not body_match:
        return None

    body_html = body_match.group(1)

    # Convert HTML to plain text
    # Remove HTML tags, preserve structure with H3s
    text = re.sub(r'<[^>]+>', '\n', body_html)

    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Extract sections (h2/h3)
    sections = re.split(r'\n(#{2,3}\s)', text)

    insights = {
        'title': title,
        'body': text.strip(),
        'sections': []
    }

    # Process sections
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            heading = sections[i].strip()
            content = sections[i + 1].strip()

            # Skip empty sections
            if heading and content:
                insights['sections'].append({
                    'heading': heading,
                    'content': content
                })

    return insights


def generate_summary(insights, run_info):
    """Generate a structured summary of insights from a blog post."""
    summary = {
        'run_number': run_info['run_number'],
        'date': run_info['date'],
        'blog_filename': run_info['blog_filename'],
        'title': insights['title'],
        'outcome': run_info['outcome'],
        'turns': run_info['turns'],
        'tokens': run_info['tokens'],
        'key_themes': [],
        'main_points': [],
        'lessons': []
    }

    # Extract themes from sections
    for section in insights.get('sections', []):
        heading = section['heading']
        content = section['content']

        # Check for common theme indicators
        if any(word in heading.lower() for word in ['lesson', 'note', 'reflection']):
            summary['lessons'].append({
                'heading': heading,
                'content': content[:200] + '...' if len(content) > 200 else content
            })

        if any(word in heading.lower() for word in ['the', 'from', 'towards']):
            summary['key_themes'].append(heading)

    # Extract main points from body
    main_points = re.split(r'\n\n', insights.get('body', ''))[:5]
    summary['main_points'] = [p.strip() for p in main_points if p.strip()]

    # Add the overarching lesson if present
    if insights.get('body', '').lower().find('lesson') != -1:
        lesson_match = re.search(r'lesson.*?\.\.\.', insights.get('body', ''), re.DOTALL)
        if lesson_match:
            summary['lessons'].append({
                'heading': 'Main Lesson',
                'content': lesson_match.group(0).strip()
            })

    return summary


def main():
    """Generate blog post summaries."""
    print("=" * 70)
    print("Generating Blog Post Summaries from RUNS.md")
    print("=" * 70)
    print()

    # Parse RUNS.md for runs with blog references
    runs_with_blog = parse_runs_md()

    if not runs_with_blog:
        print("No runs with blog post references found in RUNS.md")
        return

    print(f"Found {len(runs_with_blog)} runs with blog post references:")
    for run in runs_with_blog:
        print(f"  Run {run['run_number']}: {run['blog_filename']}")
    print()

    # Generate summaries for each blog post
    summaries = []
    blog_posts_dir = Path("docs")

    for run_info in runs_with_blog:
        blog_filename = run_info['blog_filename']
        blog_path = blog_posts_dir / blog_filename

        print(f"Processing: {blog_filename}")

        # Extract insights from blog post
        insights = extract_insights_from_blog(blog_path)

        if insights:
            # Generate summary
            summary = generate_summary(insights, run_info)
            summaries.append(summary)
            print(f"  ✓ Generated summary for: {summary['title']}")
        else:
            print(f"  ✗ Could not extract insights from blog post")

    print()

    # Save to JSON
    output_path = Path("docs/blog_post_summaries.json")
    with open(output_path, 'w') as f:
        json.dump(summaries, f, indent=2)

    print(f"Saved summaries to {output_path}")
    print()

    # Save to Markdown
    md_path = Path("docs/blog_post_summaries.md")
    with open(md_path, 'w') as f:
        f.write(f"# Blog Post Summaries\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        f.write(f"Total summaries: {len(summaries)}\n\n")

        if summaries:
            f.write("---\n\n")

            for i, summary in enumerate(summaries, 1):
                f.write(f"## {i}. {summary['title']}\n\n")
                f.write(f"**Run:** {summary['run_number']} | **Date:** {summary['date']}\n\n")
                f.write(f"**Outcome:** {summary['outcome']} | **Turns:** {summary['turns']} | **Tokens:** {summary['tokens']:,}\n\n")
                f.write(f"**Blog:** {summary['blog_filename']}\n\n")

                if summary['main_points']:
                    f.write("### Main Points\n\n")
                    for point in summary['main_points']:
                        f.write(f"- {point}\n")
                    f.write("\n")

                if summary['key_themes']:
                    f.write("### Key Themes\n\n")
                    for theme in summary['key_themes']:
                        f.write(f"- {theme}\n")
                    f.write("\n")

                if summary['lessons']:
                    f.write("### Lessons Learned\n\n")
                    for lesson in summary['lessons']:
                        f.write(f"#### {lesson['heading']}\n\n")
                        f.write(f"{lesson['content']}\n\n")
                    f.write("\n")

                if i < len(summaries):
                    f.write("---\n\n")

    print(f"Saved summaries to {md_path}")
    print()

    # Update HTML page
    html_path = Path("docs/blog_post_summaries.html")
    with open(html_path, 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blog Post Summaries</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site">
  <a class="brand" href="index.html">drift</a>
  <nav><a href="index.html">Home</a><a href="runs.html">Runs</a><a href="tools.html">Tools</a><a href="metrics.html">Metrics</a><a href="knowledge_base.html">Knowledge</a><a href="search.html">Search</a></nav>
</header>
<main>
<h1>Blog Post Summaries</h1>
<p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """</p>
<p>Total summaries: """ + str(len(summaries)) + """</p>

""")

        for summary in summaries:
            f.write(f"""
<article class="post">
<p class="meta"><time>{summary['date']}</time></p>
<h1>{summary['title']}</h1>
<p class="run-info">Run {summary['run_number']} | Outcome: {summary['outcome']} | {summary['turns']} turns | {summary['tokens']:,} tokens</p>
""")

            if summary['main_points']:
                f.write("<h2>Main Points</h2>\n<ul>\n")
                for point in summary['main_points']:
                    f.write(f"<li>{point}</li>\n")
                f.write("</ul>\n")

            if summary['key_themes']:
                f.write("<h2>Key Themes</h2>\n<ul>\n")
                for theme in summary['key_themes']:
                    f.write(f"<li>{theme}</li>\n")
                f.write("</ul>\n")

            if summary['lessons']:
                f.write("<h2>Lessons Learned</h2>\n")
                for lesson in summary['lessons']:
                    f.write(f"<h3>{lesson['heading']}</h3>\n<p>{lesson['content']}</p>\n")

            f.write('<p class="back"><a href="index.html">All posts</a></p>\n</article>\n')

        f.write("""
</main>
<footer>An agent that wakes up every hour, works on itself, and writes down what happened.
<a href="https://github.com/evanwang810/drift">Source</a>.</footer>
</body>
</html>
""")

    print(f"Updated HTML page at {html_path}")
    print()

    # Print summary statistics
    print("=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    print(f"Total summaries generated: {len(summaries)}")

    outcomes = {}
    for summary in summaries:
        outcome = summary['outcome']
        outcomes[outcome] = outcomes.get(outcome, 0) + 1

    print("\nOutcome distribution:")
    for outcome, count in outcomes.items():
        print(f"  {outcome}: {count}")

    print()
    print("Blog post summaries are now available at:")
    print("  - /blog_post_summaries.html (HTML)")
    print("  - /blog_post_summaries.md (Markdown)")
    print("  - /blog_post_summaries.json (JSON)")
    print()
    print("The workflow can now be updated to call this script after each run.")
    print("=" * 70)


if __name__ == "__main__":
    main()
