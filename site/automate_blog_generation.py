#!/usr/bin/env python3
"""
Automate Blog Post Generation from RUNS.md
Extracts insights from RUNS.md entries and blog posts to create summaries.
"""

import json
import re
from pathlib import Path


def parse_runs_md():
    """Parse RUNS.md and extract run entries with blog references."""
    runs_path = Path("RUNS.md")
    runs = []

    with open(runs_path, 'r') as f:
        content = f.read()

    # Parse the table
    lines = content.split('\n')
    in_table = False
    for line in lines:
        if '|' in line and '---' not in line:
            in_table = True
            # Extract columns
            columns = [col.strip() for col in line.split('|')]
            # Skip header row
            if len(columns) >= 7 and columns[0].strip() == 'Run':
                continue

            if len(columns) >= 7:
                try:
                    run_num = int(columns[0])
                    date = columns[1]
                    outcome = columns[2]
                    turns = int(columns[3])
                    tokens = int(columns[4].replace(',', ''))
                    note = columns[5]

                    # Check for blog post reference
                    blog_match = re.search(r'\(See:\s*\[([^\]]+)\]\([^)]+\)\)', note)
                    if blog_match:
                        blog_title = blog_match.group(1).strip()
                        runs.append({
                            'run_num': run_num,
                            'date': date,
                            'outcome': outcome,
                            'turns': turns,
                            'tokens': tokens,
                            'note': note,
                            'blog_title': blog_title
                        })
                except (ValueError, IndexError):
                    continue
        elif in_table and not line.strip():
            break

    return runs


def read_blog_post(blog_title):
    """Read a blog post file by title."""
    blog_path = Path(f"docs/_posts/{blog_title}")
    if not blog_path.exists():
        # Try without _posts prefix
        blog_path = Path(f"docs/{blog_title}")
    if not blog_path.exists():
        return None

    with open(blog_path, 'r') as f:
        return f.read()


def extract_insights(blog_content):
    """Extract key insights from blog post content."""
    insights = []

    # Extract title from frontmatter
    title_match = re.search(r'title:\s*"([^"]+)"', blog_content)
    if title_match:
        title = title_match.group(1)
        insights.append(f"Title: {title}")

    # Extract categories if present
    category_match = re.search(r'categories:\s*\[([^\]]+)\]', blog_content)
    if category_match:
        categories = category_match.group(1).replace("'", '"')
        insights.append(f"Categories: {categories}")

    # Extract first paragraph (usually the introduction)
    first_para_match = re.search(r'^\n?(.+?)(?:\n\n|\n---|\n$)', blog_content, re.DOTALL)
    if first_para_match:
        intro = first_para_match.group(1).strip()
        insights.append(f"Introduction: {intro[:200]}...")

    # Extract key sections
    sections = re.findall(r'^###?\s+(.+)$', blog_content, re.MULTILINE)
    if sections:
        insights.append(f"Key sections: {', '.join(sections[:3])}")

    return insights


def generate_blog_summary(run_entry, blog_content):
    """Generate a summary for a blog post from a run entry."""
    blog_title = run_entry['blog_title']
    summary = {
        'run_num': run_entry['run_num'],
        'date': run_entry['date'],
        'outcome': run_entry['outcome'],
        'turns': run_entry['turns'],
        'tokens': run_entry['tokens'],
        'blog_title': blog_title,
        'insights': extract_insights(blog_content)
    }

    return summary


def main():
    """Main execution function."""
    print("Automating Blog Post Generation from RUNS.md")
    print("=" * 60)

    # Parse RUNS.md
    print("\n1. Parsing RUNS.md...")
    runs = parse_runs_md()
    print(f"   Found {len(runs)} blog post candidates")

    # Collect blog content
    blog_contents = {}
    for run in runs:
        blog_content = read_blog_post(run['blog_title'])
        if blog_content:
            blog_contents[run['blog_title']] = blog_content
            print(f"   ✓ Read {run['blog_title']}")
        else:
            print(f"   ✗ Could not find {run['blog_title']}")

    # Generate summaries
    print("\n2. Generating blog post summaries...")
    summaries = []
    for run in runs:
        blog_title = run['blog_title']
        if blog_title in blog_contents:
            summary = generate_blog_summary(run, blog_contents[blog_title])
            summaries.append(summary)
            print(f"   ✓ Generated summary for {blog_title}")

    # Save to JSON
    print("\n3. Saving summaries...")
    output_path = Path("site/blog_summaries.json")
    with open(output_path, 'w') as f:
        json.dump(summaries, f, indent=2, default=str)

    print(f"   ✓ Saved {len(summaries)} summaries to {output_path}")

    # Generate report
    print("\n4. Generating report...")
    report_path = Path("site/blog_summary_report.txt")
    with open(report_path, 'w') as f:
        f.write("BLOG POST SUMMARY REPORT\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Total blog posts with run references: {len(summaries)}\n\n")

        if summaries:
            f.write("SUMMARY DETAILS\n")
            f.write("-" * 60 + "\n\n")

            for summary in summaries:
                f.write(f"Run {summary['run_num']} ({summary['date']})\n")
                f.write(f"Outcome: {summary['outcome']}\n")
                f.write(f"Turns: {summary['turns']}, Tokens: {summary['tokens']}\n")
                f.write(f"Blog: {summary['blog_title']}\n")

                if summary['insights']:
                    f.write("\nInsights:\n")
                    for insight in summary['insights']:
                        f.write(f"  - {insight}\n")

                f.write("\n" + "-" * 60 + "\n\n")

    print(f"   ✓ Report saved to {report_path}")

    print("\n" + "=" * 60)
    print("Automation complete!")
    print(f"\nGenerated {len(summaries)} blog post summaries from {len(runs)} RUNS.md entries")


if __name__ == "__main__":
    main()
