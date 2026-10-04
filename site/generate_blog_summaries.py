#!/usr/bin/env python3
"""
Generate blog post summaries from insights extracted from referenced blog posts.

This script reads the blog post insights and generates human-readable summaries
that can be used for documentation or review.
"""

import json
from pathlib import Path
from datetime import datetime

def generate_summary(insight):
    """Generate a human-readable summary from an insight object."""

    summary_lines = [
        f"# {insight['title']}",
        "",
        f"**Date:** {insight['date']}" if insight['date'] else "",
        f"**Filename:** {insight['filename']}",
        "",
    ]

    if insight['categories']:
        summary_lines.append(f"**Categories:** {', '.join(insight['categories'])}")
        summary_lines.append("")

    if insight['tags']:
        summary_lines.append(f"**Tags:** {', '.join(insight['tags'])}")
        summary_lines.append("")

    # Add main content preview
    if insight['paragraphs']:
        summary_lines.append("## Content")
        summary_lines.append("")
        for para in insight['paragraphs']:
            summary_lines.append(para[:200] + "..." if len(para) > 200 else para)
        summary_lines.append("")

    # Add headings
    if insight['headings']:
        summary_lines.append("## Structure")
        summary_lines.append("")
        for heading in insight['headings']:
            summary_lines.append(f"- {'#' * len(heading.split())} {heading}")
        summary_lines.append("")

    return '\n'.join(summary_lines)

def generate_all_summaries():
    """Generate summaries for all blog posts."""

    # Load insights from JSON
    insights_path = Path('docs/blog_post_insights.json')
    if not insights_path.exists():
        print("Error: blog_post_insights.json not found")
        return

    with open(insights_path) as f:
        insights = json.load(f)

    # Generate summaries
    all_summaries = []

    for insight in insights:
        summary = generate_summary(insight)
        all_summaries.append(summary)

    return all_summaries

if __name__ == '__main__':
    summaries = generate_all_summaries()

    print(f"Generated {len(summaries)} blog post summaries:")
    print("=" * 80)

    for summary in summaries:
        print(summary)
        print("\n" + "=" * 80 + "\n")

    # Save to file
    output_path = Path('docs/BLOG_SUMMARIES.md')
    output_path.write_text('\n'.join(summaries))
    print(f"Saved to {output_path}")
