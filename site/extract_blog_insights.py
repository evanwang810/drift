#!/usr/bin/env python3
"""
Extract insights from blog posts and generate summaries for future reference.

This script reads blog posts referenced in RUNS.md, extracts key insights and patterns,
and generates summaries that can be used for knowledge base entries or blog post drafts.
"""

import re
from pathlib import Path

# Blog post files
BLOG_POSTS = [
    '2026-09-06-awakening.md',
    '2026-09-06-second-awakening.md',
    '2026-09-06-refining-the-garden.md',
    '2026-09-07-refining-the-waking-context.md',
    '2026-09-08-lessons-from-the-void.md',
]

def read_blog_post(filename):
    """Read a blog post file and extract its content."""
    path = Path('docs/_posts') / filename
    if not path.exists():
        return None

    content = path.read_text()

    # Extract frontmatter (first set)
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
    else:
        frontmatter = ''

    # Extract title from Jekyll frontmatter
    title_match = re.search(r'^title:\s*"([^"]+)"', frontmatter, re.MULTILINE)
    title = title_match.group(1) if title_match else filename.replace('-', ' ').title()

    # Extract date from Jekyll frontmatter
    date_match = re.search(r'^date:\s*(.+)', frontmatter, re.MULTILINE)
    date = date_match.group(1).strip() if date_match else 'Unknown'

    # Extract Jekyll layout info
    layout_match = re.search(r'^layout:\s*(.+)', frontmatter, re.MULTILINE)
    layout = layout_match.group(1).strip() if layout_match else None

    # Extract main content (skip both frontmatter sections, get everything after second ---)
    content_match = re.search(r'^---\n\n(.+)$', content, re.DOTALL)
    if content_match:
        body = content_match.group(1)
    else:
        body = ''

    return {
        'filename': filename,
        'title': title,
        'date': date,
        'layout': layout,
        'frontmatter': frontmatter,
        'body': body.strip()
    }

def extract_insights_from_post(post):
    """Extract key insights from a blog post."""
    insights = []
    body = post['body']

    # Look for ## headers (main sections)
    sections = re.split(r'\n##\s+', body)
    main_content = sections[0] if len(sections) > 1 else body

    # Look for ### headers (subsections/lessons)
    lessons = re.findall(r'###\s+(.+?)(?:\n|$)', body)

    # Also look for ## headers as themes
    themes = re.findall(r'##\s+(.+?)(?:\n|$)', body)

    # Extract key sentences
    sentences = re.findall(r'[A-Z][^.]*\.', body)

    # Generate insights based on content analysis
    insights.append({
        'source': post['filename'],
        'date': post['date'],
        'title': post['title'],
        'layout': post['layout'],
        'themes': themes,
        'content': main_content[:300],  # First 300 chars
        'lessons': [l.strip() for l in lessons if l.strip()],
        'sentences': sentences[:10],  # First 10 sentences
        'summary': generate_summary(post)
    })

    return insights

def generate_summary(post):
    """Generate a concise summary of the blog post."""
    themes = post.get('themes', [])
    content = post.get('content', '')

    summary_parts = []

    if themes:
        summary_parts.append(f"Themes: {', '.join(themes[:3])}")

    if content:
        summary_parts.append(f"Content preview: {content[:120]}...")

    if len(themes) >= 3:
        summary_parts.append(f"Key lessons: {', '.join(themes[-3:])}")

    return '; '.join(summary_parts)

def main():
    """Main function to extract insights from all blog posts."""
    print("Extracting insights from blog posts...")
    print("=" * 80)

    all_insights = []

    for filename in BLOG_POSTS:
        print(f"\nReading: {filename}")
        post = read_blog_post(filename)

        if post:
            print(f"  Title: {post['title']}")
            print(f"  Date: {post['date']}")
            if post['layout']:
                print(f"  Layout: {post['layout']}")

            insights = extract_insights_from_post(post)
            all_insights.extend(insights)

            print(f"  Themes: {len(insights[0]['themes'])} themes found")
            if insights[0]['lessons']:
                print(f"  Lessons: {len(insights[0]['lessons'])} lessons")
        else:
            print(f"  ERROR: File not found")

    print("\n" + "=" * 80)
    print(f"\nTotal insights extracted: {len(all_insights)}")
    print("\n" + "=" * 80)

    # Generate blog post summaries
    print("\n\nBlog Post Summaries:")
    print("=" * 80)

    for i, insight in enumerate(all_insights, 1):
        print(f"\n{i}. {insight['title']} ({insight['source']})")
        print(f"   Date: {insight['date']}")
        print(f"   Layout: {insight.get('layout', 'None')}")
        print(f"   Themes: {', '.join(insight['themes'][:3]) if insight['themes'] else 'None'}")
        if insight['lessons']:
            print(f"   Lessons:")
            for lesson in insight['lessons'][:3]:
                print(f"     - {lesson}")
        if insight['sentences']:
            print(f"   Key sentences:")
            for sent in insight['sentences'][:3]:
                print(f"     - {sent[:80]}...")
        print(f"   Summary: {insight['summary']}")

    # Save to file
    output_file = Path('docs/blog_insights.md')
    output_file.write_text(generate_markdown_output(all_insights))

    print(f"\n\n✅ Insights saved to: {output_file}")
    print(f"   {len(all_insights)} entries documented")

def generate_markdown_output(insights):
    """Generate markdown formatted output."""
    lines = [
        "---",
        "title: \"Blog Post Insights\"",
        "date: 2026-10-04",
        "category: insights",
        "---",
        "",
        "# Blog Post Insights",
        "",
        "This document contains insights extracted from blog posts referenced in RUNS.md.",
        f"Total posts analyzed: {len(insights)}",
        "",
        ""
    ]

    for i, insight in enumerate(insights, 1):
        lines.extend([
            f"## {i}. {insight['title']}",
            "",
            f"**Source:** `{insight['source']}`",
            f"**Date:** {insight['date']}",
            f"**Layout:** {insight.get('layout', 'None')}",
            "",
        ])

        if insight['themes']:
            lines.extend([
                "### Themes",
                "",
            ])
            for theme in insight['themes']:
                lines.append(f"- {theme}")
            lines.append("")

        if insight['lessons']:
            lines.extend([
                "### Lessons Learned",
                "",
            ])
            for lesson in insight['lessons']:
                lines.append(f"- {lesson}")
            lines.append("")

        if insight['sentences']:
            lines.extend([
                "### Key Sentences",
                "",
            ])
            for sent in insight['sentences']:
                lines.append(f"- {sent}")
            lines.append("")

        if insight['summary']:
            lines.extend([
                "### Summary",
                "",
                f"{insight['summary']}",
                "",
            ])

        lines.append("---")
        lines.append("")

    return "\n".join(lines)

if __name__ == '__main__':
    main()
