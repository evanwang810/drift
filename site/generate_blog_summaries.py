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
        return []

    with open(insights_path) as f:
        insights = json.load(f).get('posts', [])

    # Generate summaries
    all_summaries = []

    for insight in insights:
        summary = generate_summary(insight)
        all_summaries.append(summary)

    return all_summaries

def generate_report(insights):
    """Generate a comprehensive report with insights organized by category."""

    report_lines = [
        "# Blog Post Summaries",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Posts: {len(insights)}",
        "",
        "## Overview"
    ]

    # Calculate statistics
    total_headings = sum(len(i['headings']) for i in insights)
    total_paragraphs = sum(len(i['paragraphs']) for i in insights)

    report_lines.extend([
        f"- Total Headings: {total_headings}",
        f"- Total Paragraphs: {total_paragraphs}",
        "",
        "## By Title"
    ])

    # Group by title
    for insight in insights:
        report_lines.extend([
            "",
            f"### {insight['title']}",
            "",
            f"**Filename:** `{insight['filename']}`",
            f"**Date:** {insight['date']}",
            "",
        ])

        if insight['categories']:
            report_lines.append(f"**Categories:** {', '.join(insight['categories'])}")

        if insight['tags']:
            report_lines.append(f"**Tags:** {', '.join(insight['tags'])}")

        if insight['headings']:
            report_lines.append("")
            report_lines.append("**Headings:**")
            for heading in insight['headings']:
                report_lines.append(f"- {heading}")

        if insight['paragraphs']:
            report_lines.append("")
            report_lines.append("**Content Preview:**")
            for para in insight['paragraphs'][:3]:
                preview = para[:150] + "..." if len(para) > 150 else para
                report_lines.append(f"- {preview}")

        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

    return '\n'.join(report_lines)

def main():
    """Main function."""

    print("Loading insights from JSON...")
    print("=" * 80)

    # Load insights
    insights_path = Path('docs/blog_post_insights.json')
    if not insights_path.exists():
        print("Error: blog_post_insights.json not found")
        return

    with open(insights_path) as f:
        data = json.load(f)

    insights = data.get('posts', [])

    print(f"Loaded insights from {len(insights)} blog posts")
    print("=" * 80)

    # Generate summaries
    summaries = generate_all_summaries()

    print(f"Generated {len(summaries)} blog post summaries")
    print("=" * 80)

    # Save summaries
    output_path = Path('docs/BLOG_SUMMARIES.md')
    output_path.write_text('\n'.join(summaries))
    print(f"\nSaved summaries to: {output_path}")

    # Generate comprehensive report
    report = generate_report(insights)
    report_path = Path('docs/BLOG_SUMMARIES_REPORT.md')
    report_path.write_text(report)
    print(f"Saved report to: {report_path}")

    # Print summary of what was generated
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nGenerated {len(summaries)} blog post summaries")
    print(f"Saved to: docs/BLOG_SUMMARIES.md")
    print(f"\nGenerated comprehensive report with statistics")
    print(f"Saved to: docs/BLOG_SUMMARIES_REPORT.md")

    if insights:
        print(f"\nSample - {insights[0]['title']}")
        print(f"  Date: {insights[0]['date']}")
        print(f"  Categories: {', '.join(insights[0]['categories'])}")
        print(f"  Headings: {len(insights[0]['headings'])}")
        print(f"  Paragraphs: {len(insights[0]['paragraphs'])}")


if __name__ == '__main__':
    main()
