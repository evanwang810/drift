#!/usr/bin/env python3
"""
Extract insights from RUNS.md and blog posts to create a bridge between
technical run logs and reflective blog posts.
"""

import re
import json
from pathlib import Path


class RUNSMDParser:
    """Parse RUNS.md and extract blog post references."""

    def __init__(self, runs_md_path="RUNS.md"):
        self.runs_md_path = Path(runs_md_path)
        self.runs = []

    def parse(self):
        """Parse RUNS.md and extract all runs and blog references."""
        content = self.runs_md_path.read_text()

        # Find all table rows
        table_pattern = r'\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|'
        rows = re.findall(table_pattern, content)

        # Remove header row (first row that contains "run")
        if rows and "run" in rows[0].lower():
            rows = rows[1:]

        for row in rows:
            # Parse the table row
            cols = [col.strip() for col in row.split('|')[1:-1]]

            if len(cols) >= 6:
                try:
                    run_num = int(cols[0])
                    date_str = cols[1]
                    outcome = cols[2]
                    turns = int(cols[3].replace(',', ''))
                    tokens = int(cols[4].replace(',', ''))

                    # Extract blog reference
                    blog_ref = None
                    note = cols[5]

                    # Look for (See: ... ) pattern
                    see_pattern = r'\(See:\s*\((.*?)\)\)'
                    matches = re.findall(see_pattern, note)

                    if matches:
                        blog_ref = matches[0]

                    self.runs.append({
                        'run': run_num,
                        'date': date_str,
                        'outcome': outcome,
                        'turns': turns,
                        'tokens': tokens,
                        'note': note,
                        'blog_ref': blog_ref
                    })
                except (ValueError, IndexError) as e:
                    print(f"Error parsing row: {row[:50]}... Error: {e}")

        return self.runs

    def get_blog_candidates(self):
        """Get all runs that have blog post references."""
        return [run for run in self.runs if run['blog_ref']]


class BlogPostReader:
    """Read and analyze blog posts."""

    def __init__(self, posts_dir="docs/_posts"):
        self.posts_dir = Path(posts_dir)

    def read_post(self, post_name):
        """Read a blog post by name."""
        post_path = self.posts_dir / post_name

        if not post_path.exists():
            print(f"Warning: {post_name} not found")
            return None

        content = post_path.read_text()
        return content

    def extract_insights(self, content):
        """Extract key insights from blog post content."""
        insights = []

        # Look for structured sections (headers, bold text, etc.)
        lines = content.split('\n')

        current_section = None
        for line in lines:
            # Check for Jekyll frontmatter
            if line.startswith('---'):
                continue

            # Check for markdown headers
            if line.startswith('# '):
                current_section = line[2:].strip()
                continue

            # Extract key insights
            if line.strip() and line.strip()[0] in ['-', '*', '+']:
                insight = line[1:].strip()
                if insight:
                    insights.append({
                        'section': current_section,
                        'insight': insight
                    })

        return insights


class InsightBridge:
    """Create a bridge between RUNS.md entries and blog posts."""

    def __init__(self, runs_parser, blog_reader):
        self.runs_parser = runs_parser
        self.blog_reader = blog_reader

    def generate_insights(self):
        """Generate insights bridging runs and blog posts."""
        runs = self.runs_parser.runs
        blog_candidates = self.runs_parser.get_blog_candidates()

        insights = []

        for run in runs:
            if run['blog_ref']:
                # Find the corresponding blog post
                blog_name = run['blog_ref']
                content = self.blog_reader.read_post(blog_name)

                if content:
                    # Extract insights from the blog post
                    blog_insights = self.blog_reader.extract_insights(content)

                    insights.append({
                        'run': run['run'],
                        'run_date': run['date'],
                        'run_outcome': run['outcome'],
                        'run_tokens': run['tokens'],
                        'run_turns': run['turns'],
                        'blog_post': blog_name,
                        'insights': blog_insights,
                        'note': run['note']
                    })

        return insights

    def generate_summary(self, insights):
        """Generate a human-readable summary."""
        output = []

        output.append("# Insights Bridge: RUNS.md → Blog Posts\n")
        output.append(f"Generated {len(insights)} blog post summaries from {len(insights) * 5} runs (on average)\n\n")

        for entry in insights:
            output.append(f"## Run {entry['run']}: {entry['blog_post']}")
            output.append(f"**Date:** {entry['run_date']}")
            output.append(f"**Outcome:** {entry['run_outcome']}")
            output.append(f"**Tokens:** {entry['run_tokens']:,}")
            output.append(f"**Turns:** {entry['run_turns']}\n")

            output.append(f"**Blog Post:** {entry['blog_post']}")
            output.append(f"**Note:** {entry['note']}\n")

            if entry['insights']:
                output.append("### Key Insights\n")
                for insight in entry['insights']:
                    section = insight['section'] or 'General'
                    text = insight['insight']
                    output.append(f"**{section}:** {text}")
                output.append("")

            output.append("---\n")

        return '\n'.join(output)


def main():
    """Main function to run the insight extraction."""
    print("Extracting insights from RUNS.md and blog posts...")

    # Parse RUNS.md
    runs_parser = RUNSMDParser()
    runs = runs_parser.parse()
    print(f"Parsed {len(runs)} runs from RUNS.md")

    # Get blog candidates
    blog_candidates = runs_parser.get_blog_candidates()
    print(f"Found {len(blog_candidates)} blog post references")

    # Read blog posts
    blog_reader = BlogPostReader()
    print(f"Scanning blog posts in docs/_posts/")

    # Create insight bridge
    bridge = InsightBridge(runs_parser, blog_reader)
    insights = bridge.generate_insights()
    print(f"Extracted insights from {len(insights)} blog posts")

    # Generate summary
    summary = bridge.generate_summary(insights)

    # Save to file
    output_path = "docs/INSIGHTS_BRIDGE.md"
    with open(output_path, 'w') as f:
        f.write(summary)

    print(f"\nSaved insights to {output_path}")
    print(f"\nSummary of insights:")
    print(f"- Total runs analyzed: {len(runs)}")
    print(f"- Blog post references: {len(blog_candidates)}")
    print(f"- Insights extracted: {len(insights)}")
    print(f"- Average insights per blog post: {len(insights) * 5 / len(blog_candidates):.1f}")

    # Also save as JSON for programmatic use
    json_path = "docs/insights_bridge.json"
    with open(json_path, 'w') as f:
        json.dump(insights, f, indent=2)

    print(f"Saved JSON data to {json_path}")

    return insights, summary


if __name__ == "__main__":
    main()
