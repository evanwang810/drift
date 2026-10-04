#!/usr/bin/env python3
"""
Generate blog post drafts by combining RUNS.md entries with blog post insights.

This script takes RUNS.md entries with "(See: ...)" patterns and combines them
with insights from the referenced blog posts to generate draft blog posts.
"""

import re
from pathlib import Path
from datetime import datetime
import json

class BlogDraftGenerator:
    """Generate blog post drafts from RUNS.md entries."""

    def __init__(self, runs_path='RUNS.md', blog_insights_path='docs/blog_post_insights.json'):
        self.runs_path = Path(runs_path)
        self.blog_insights_path = Path(blog_insights_path)

    def extract_run_candidates(self):
        """Extract runs with blog post references from RUNS.md."""

        content = self.runs_path.read_text()

        # Pattern for runs with (See: ...) pattern
        # Looking for: | run | date | outcome | turns | tokens | note (See: ...))
        # The pattern matches: "Attempted to enable GitHub Pages; blocked by permissions. (See: ([ 2026-09-06-awakening.md](docs/_posts/2026-09-06-awakening.md)))"
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
            # Pattern: ([ 2026-09-06-awakening.md](docs/_posts/2026-09-06-awakening.md))
            # We want to extract just the filename
            filename_match = re.search(r'\]\(([^)]+)\)', post_ref)
            if filename_match:
                post_path = filename_match.group(1)
                post_filename = post_path.split('/')[-1] if '/' in post_path else post_path.split('\\')[-1]
            else:
                post_filename = post_ref

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

    def load_blog_insights(self):
        """Load blog post insights from JSON."""

        with open(self.blog_insights_path) as f:
            data = json.load(f)
            return data.get('posts', [])

    def find_insight_for_post(self, insights, post_file):
        """Find the insight object for a given blog post file."""

        for insight in insights:
            if insight['filename'] == post_file:
                return insight
        return None

    def generate_draft(self, run_entry, insight):
        """Generate a blog post draft from a run entry and insight."""

        draft_lines = [
            "---",
            f"title: \"{run_entry['note'][:60]}...\"",
            f"date: {run_entry['date']}",
            "layout: post",
            "categories: [Reflection, Run Log]",
            ""
        ]

        if insight and insight['categories']:
            draft_lines.append("categories:")
            for cat in insight['categories']:
                draft_lines.append(f"  - {cat}")
            draft_lines.append("")

        draft_lines.extend([
            run_entry['note'],
            "",
            "---",
            "",
        ])

        # Add insights if available
        if insight:
            draft_lines.append("## Insights")
            draft_lines.append("")

            if insight['key_points']:
                draft_lines.append("### Key Themes")
                draft_lines.append("")
                for point in insight['key_points']:
                    draft_lines.append(f"- {point}")
                draft_lines.append("")

            if insight['headings']:
                draft_lines.append("### Structure")
                draft_lines.append("")
                for heading in insight['headings']:
                    draft_lines.append(f"- {heading}")
                draft_lines.append("")

        draft_lines.extend([
            "## Run Details",
            "",
            f"- **Run:** {run_entry['run']}",
            f"- **Date:** {run_entry['date']} {run_entry['date'].split(' ')[1] if ' ' in run_entry['date'] else '00:00'}",
            f"- **Outcome:** {run_entry['outcome']}",
            f"- **Turns:** {run_entry['turns']}",
            f"- **Tokens:** {run_entry['tokens']}",
            ""
        ])

        # Add note about the original post
        draft_lines.extend([
            "## Related Post",
            "",
            f"This run referenced the original blog post: **{insight['title'] if insight else 'Not Found'}**",
            f"File: `{run_entry['post_file']}`",
            ""
        ])

        return '\n'.join(draft_lines)

    def generate_all_drafts(self):
        """Generate all blog post drafts."""

        # Extract run candidates
        run_candidates = self.extract_run_candidates()
        print(f"Found {len(run_candidates)} run candidates with blog post references")

        # Load insights
        insights = self.load_blog_insights()
        print(f"Loaded insights from {len(insights)} blog posts")

        # Match candidates with insights
        drafts = []
        for run_entry in run_candidates:
            insight = self.find_insight_for_post(insights, run_entry['post_file'])

            draft = self.generate_draft(run_entry, insight)
            drafts.append({
                'run': run_entry,
                'insight': insight,
                'draft': draft
            })

        return drafts

    def save_drafts(self, drafts):
        """Save all drafts to markdown files."""

        drafts_dir = Path('docs/blog_drafts')
        drafts_dir.mkdir(exist_ok=True)

        for draft_info in drafts:
            run = draft_info['run']
            insight = draft_info['insight']
            draft = draft_info['draft']

            # Create filename from run note (sanitized)
            safe_title = re.sub(r'[^\w\s-]', '', run['note'][:50]).strip()
            safe_title = re.sub(r'[-\s]+', '-', safe_title) or f'run-{run["run"]}'
            filename = f"run-{run['run']}-{safe_title}.md"

            filepath = drafts_dir / filename
            filepath.write_text(draft)

            print(f"Saved draft: {filename}")

        print(f"\nSaved {len(drafts)} drafts to {drafts_dir}/")

    def generate_summary(self, drafts):
        """Generate a summary of all drafts."""

        summary_lines = [
            "# Blog Post Drafts Summary",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Drafts: {len(drafts)}",
            ""
        ]

        for draft_info in drafts:
            run = draft_info['run']
            insight = draft_info['insight']

            summary_lines.extend([
                "## Draft",
                "",
                f"**Run:** {run['run']}",
                f"**Date:** {run['date']}",
                f"**Outcome:** {run['outcome']}",
                f"**Tokens:** {run['tokens']}",
                f"**Note:** {run['note'][:100]}...",
                ""
            ])

            if insight:
                summary_lines.extend([
                    "**Insight:**",
                    f"- Title: {insight['title']}",
                    f"- Filename: {insight['filename']}",
                    f"- Categories: {', '.join(insight['categories'])}",
                    f"- Headings: {len(insight['headings'])}",
                    f"- Paragraphs: {len(insight['paragraphs'])}",
                    ""
                ])
            else:
                summary_lines.extend([
                    "**No insight available for this post.**",
                    ""
                ])

            summary_lines.extend([
                "---",
                ""
            ])

        return '\n'.join(summary_lines)


def main():
    """Main function."""

    print("Generating blog post drafts...")
    print("=" * 80)

    generator = BlogDraftGenerator()
    drafts = generator.generate_all_drafts()

    print(f"\nGenerated {len(drafts)} drafts")
    print("=" * 80)

    # Save drafts
    generator.save_drafts(drafts)

    # Generate summary
    summary = generator.generate_summary(drafts)
    summary_path = Path('docs/BLOG_DRAFTS_SUMMARY.md')
    summary_path.write_text(summary)
    print(f"Saved summary to: {summary_path}")

    # Print overview
    print("\n" + "=" * 80)
    print("OVERVIEW")
    print("=" * 80)

    for draft_info in drafts[:3]:  # Show first 3
        run = draft_info['run']
        insight = draft_info['insight']

        print(f"\nDraft for Run {run['run']}: {run['date']}")
        print(f"  Outcome: {run['outcome']}, Tokens: {run['tokens']}")
        print(f"  Note: {run['note'][:80]}...")
        print(f"  Related post: {run['post_file']}")
        if insight:
            print(f"  Insight: {insight['title'][:60]}...")


if __name__ == '__main__':
    main()
