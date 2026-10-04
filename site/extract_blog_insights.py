#!/usr/bin/env python3
"""
Extract insights and generate blog post summaries from referenced posts.

This script reads blog posts that are referenced in RUNS.md, extracts key insights,
and generates human-readable summaries that bridge the gap between technical run logs
and reflective blog posts.
"""

import re
from pathlib import Path
from datetime import datetime
import json

class BlogPostInsightExtractor:
    """Extract insights from blog posts."""

    def __init__(self, blog_posts_dir='docs/_posts'):
        self.blog_posts_dir = Path(blog_posts_dir)

    def extract_post_metadata(self, filepath):
        """Extract metadata from a blog post file."""

        content = filepath.read_text()

        # Extract title from YAML frontmatter
        title_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        title = None
        date = None
        tags = []

        if title_match:
            frontmatter = title_match.group(1)
            title_match = re.search(r'^title:\s*"([^"]+)"', frontmatter)
            date_match = re.search(r'^date:\s*"([^"]+)"', frontmatter)
            tags_match = re.search(r'^tags:\s*\[(.*?)\]', frontmatter, re.DOTALL)

            if title_match:
                title = title_match.group(1).strip()

            if date_match:
                date = date_match.group(1).strip()

            if tags_match:
                tags = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]

        # Extract layout
        layout_match = re.search(r'^layout:\s*(\w+)', content)
        layout = layout_match.group(1) if layout_match else None

        return {
            'title': title,
            'date': date,
            'tags': tags,
            'layout': layout,
            'filename': filepath.name
        }

    def extract_headings(self, content):
        """Extract all headings from the content."""

        headings = []

        # Match markdown headings
        heading_pattern = r'^(#{1,6})\s+(.+)$'

        for line in content.split('\n'):
            match = re.match(heading_pattern, line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append(text)

        return headings

    def extract_paragraphs(self, content):
        """Extract paragraphs from the content."""

        paragraphs = []

        # Split on double newlines, preserving content
        blocks = re.split(r'\n\n+', content)

        for block in blocks:
            if block.strip():
                # Extract markdown from block
                markdown_match = re.search(r'(.*?)\n\n', block, re.DOTALL)
                text = markdown_match.group(1).strip() if markdown_match else block.strip()

                # Convert markdown to plain text
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
                text = re.sub(r'`(.+?)`', r'\1', text)  # Code
                text = re.sub(r'#{1,6}\s+', '', text)  # Headings
                text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Links

                paragraphs.append(text[:500])  # Limit length

        return paragraphs

    def extract_categories(self, content):
        """Extract categories from the content."""

        categories = []

        # Look for categories in frontmatter
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            # Check for categories in frontmatter
            categories_match = re.search(r'^categories:\s*\[(.*?)\]', frontmatter, re.DOTALL)
            if categories_match:
                categories = [c.strip().strip('"\'') for c in categories_match.group(1).split(',')]

        return categories

    def extract_key_points(self, content, headings, paragraphs):
        """Extract key points and themes from the content."""

        key_points = []

        # Combine headings and paragraphs
        all_text = '\n'.join(headings + paragraphs)

        # Look for recurring themes
        themes = {
            'progress': 0,
            'failure': 0,
            'reflection': 0,
            'technical': 0,
            'meta': 0,
            'planning': 0,
            'growth': 0,
            'adaptation': 0
        }

        # Analyze headings for themes
        for heading in headings:
            heading_lower = heading.lower()
            for theme, keywords in [
                ('progress', ['progress', 'improvement', 'evolution', 'building', 'developing']),
                ('failure', ['fail', 'crash', 'error', 'broken', 'mistake']),
                ('reflection', ['reflect', 'think', 'consider', 'meaning', 'purpose']),
                ('technical', ['code', 'implement', 'tool', 'function', 'system']),
                ('meta', ['meta', 'thinking', 'cognitive', 'awareness', 'self']),
                ('planning', ['plan', 'goal', 'objective', 'target', 'strategy']),
                ('growth', ['grow', 'learn', 'learned', 'discovered', 'improve']),
                ('adaptation', ['adapt', 'change', 'modify', 'adjust', 'evolve'])
            ]:
                if any(keyword in heading_lower for keyword in keywords):
                    themes[theme] += 1

        # Find most prominent themes
        max_score = max(themes.values()) if themes.values() else 1
        for theme, score in themes.items():
            if score > 0 and score >= max_score * 0.5:  # At least 50% of max
                key_points.append(theme)

        # Add first paragraph as summary
        if paragraphs:
            key_points.append(paragraphs[0][:150])

        return key_points

    def extract_insights(self, filepath):
        """Extract all insights from a blog post."""

        metadata = self.extract_post_metadata(filepath)
        content = filepath.read_text()

        headings = self.extract_headings(content)
        paragraphs = self.extract_paragraphs(content)
        categories = self.extract_categories(content)
        key_points = self.extract_key_points(content, headings, paragraphs)

        # Generate summary from paragraphs
        summary = '\n\n'.join(paragraphs[:3]) if paragraphs else 'No content available.'

        return {
            'title': metadata['title'],
            'date': metadata['date'],
            'filename': metadata['filename'],
            'categories': categories,
            'tags': metadata['tags'],
            'headings': headings,
            'paragraphs': paragraphs,
            'key_points': key_points,
            'summary': summary[:500] if len(summary) > 500 else summary,
            'layout': metadata['layout']
        }

    def extract_all_insights(self):
        """Extract insights from all referenced blog posts."""

        # List all markdown files in the blog posts directory
        blog_files = list(self.blog_posts_dir.glob('*.md'))

        insights = []

        for blog_file in blog_files:
            try:
                insight = self.extract_insights(blog_file)
                insights.append(insight)
                print(f"Extracted insights from: {blog_file.name}")
            except Exception as e:
                print(f"Error extracting from {blog_file.name}: {e}")

        return insights


def generate_insights_report(insights):
    """Generate a comprehensive insights report."""

    report = []

    report.append("# Blog Post Insights Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Posts Analyzed: {len(insights)}")
    report.append("")

    # Summary statistics
    total_headings = sum(len(i['headings']) for i in insights)
    total_paragraphs = sum(len(i['paragraphs']) for i in insights)
    total_categories = set()
    for i in insights:
        total_categories.update(i['categories'])

    report.append("## Statistics")
    report.append("")
    report.append(f"- Total Headings: {total_headings}")
    report.append(f"- Total Paragraphs: {total_paragraphs}")
    report.append(f"- Unique Categories: {', '.join(sorted(total_categories))}")
    report.append("")

    # Per-post analysis
    report.append("## Post-by-Post Analysis")
    report.append("")

    for insight in insights:
        report.append(f"### {insight['title']}")
        report.append("")
        report.append(f"**Filename:** `{insight['filename']}`")
        report.append(f"**Date:** {insight['date']}")
        report.append("")

        if insight['categories']:
            report.append(f"**Categories:** {', '.join(insight['categories'])}")

        if insight['tags']:
            report.append(f"**Tags:** {', '.join(insight['tags'])}")
        report.append("")

        if insight['key_points']:
            report.append("**Key Themes:**")
            for point in insight['key_points']:
                report.append(f"- {point}")
            report.append("")

        if insight['headings']:
            report.append("**Structure:**")
            for heading in insight['headings']:
                report.append(f"- {heading}")
            report.append("")

        report.append("---")
        report.append("")

    return '\n'.join(report)


def generate_insights_json(insights):
    """Generate JSON with structured insights."""

    data = {
        'generated_at': datetime.now().isoformat(),
        'total_posts': len(insights),
        'posts': insights
    }

    return json.dumps(data, indent=2)


def main():
    """Main function."""

    print("Extracting insights from blog posts...")
    print("=" * 80)

    extractor = BlogPostInsightExtractor()
    insights = extractor.extract_all_insights()

    print(f"\nExtracted insights from {len(insights)} blog posts")
    print("=" * 80)

    # Generate reports
    report = generate_insights_report(insights)
    json_data = generate_insights_json(insights)

    # Save reports
    report_path = Path('docs/blog_post_insights_report.md')
    report_path.write_text(report)
    print(f"\nSaved markdown report to: {report_path}")

    json_path = Path('docs/blog_post_insights.json')
    json_path.write_text(json_data)
    print(f"Saved JSON data to: {json_path}")

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    for insight in insights:
        print(f"\n{insight['title']}")
        print(f"  Date: {insight['date']}")
        print(f"  Categories: {', '.join(insight['categories'])}")
        print(f"  Headings: {len(insight['headings'])}")
        print(f"  Paragraphs: {len(insight['paragraphs'])}")
        if insight['summary']:
            print(f"  Preview: {insight['summary'][:100]}...")


if __name__ == '__main__':
    main()
