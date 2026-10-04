#!/usr/bin/env python3
"""
Extract insights from RUNS.md and blog posts to generate blog post drafts.
This bridges the gap between technical run logs and reflective blog content.
"""

import re
import json
from pathlib import Path
from datetime import datetime


class BlogPostExtractor:
    """Extract insights from RUNS.md entries and blog posts."""

    def __init__(self, runs_md_path="RUNS.md", blog_posts_path="docs"):
        self.runs_md_path = Path(runs_md_path)
        self.blog_posts_path = Path(blog_posts_path)
        self.runs = []
        self.blog_posts = {}

    def parse_runs_md(self):
        """Parse RUNS.md table format."""
        if not self.runs_md_path.exists():
            print(f"RUNS.md not found at {self.runs_md_path}")
            return

        content = self.runs_md_path.read_text()
        lines = content.split('\n')

        # Skip header row
        data_lines = []
        in_table = False
        for line in lines:
            if '| run |' in line:  # Header row
                in_table = True
                continue
            if in_table:
                if line.strip() == '| --: | --- | --- | --: | --: | --- |':
                    continue  # Separator
                if line.strip() == '|' or not line.strip():
                    continue  # Empty rows
                if line.strip().startswith('---'):
                    break  # End of table

                # Parse row
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6:
                    try:
                        run_num = int(parts[0])
                        date_str = parts[1]
                        outcome = parts[2]
                        turns = int(parts[3])
                        tokens = int(parts[4].replace(',', ''))
                        note = parts[5] if len(parts) > 5 else ''

                        self.runs.append({
                            'run': run_num,
                            'when': date_str,
                            'outcome': outcome,
                            'turns': turns,
                            'tokens': tokens,
                            'note': note
                        })
                    except (ValueError, IndexError):
                        continue

        print(f"✓ Parsed {len(self.runs)} runs from RUNS.md")
        return self.runs

    def find_blog_posts(self):
        """Find all HTML blog posts in docs/."""
        html_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-(.+)\.html$')

        for html_file in self.blog_posts_path.glob('*.html'):
            match = html_pattern.match(html_file.name)
            if match:
                post_slug = match.group(1)
                self.blog_posts[post_slug] = html_file

        print(f"✓ Found {len(self.blog_posts)} blog posts")
        return self.blog_posts

    def extract_blog_post_content(self, slug):
        """Extract content from a blog post HTML file."""
        html_file = self.blog_posts.get(slug)
        if not html_file or not html_file.exists():
            return None

        content = html_file.read_text()

        # Extract title
        title_match = re.search(r'<title>(.+)</title>', content)
        title = title_match.group(1).replace(' - drift', '') if title_match else slug

        # Extract meta date
        meta_match = re.search(r'<time>(.+)</time>', content)
        date = meta_match.group(1) if meta_match else ''

        # Extract main content (h1 title and p tags)
        title_match = re.search(r'<h1>(.+)</h1>', content)
        h1_title = title_match.group(1) if title_match else ''

        paragraphs = []
        for p in re.finditer(r'<p>(.+?)</p>', content):
            text = p.group(1)
            # Remove HTML tags and decode HTML entities
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            paragraphs.append(text)

        return {
            'title': h1_title or title,
            'date': date,
            'content': paragraphs
        }

    def identify_blog_candidates(self):
        """Identify runs with blog post references."""
        candidates = []

        for run in self.runs:
            if '(See: ' in run['note']:
                # Extract slug from "(See: ([ ...](docs/_posts/...)))"
                match = re.search(r'\(See:\s*\(\s*\[([^]]+)\]\([^)]+\)\)\)', run['note'])
                if match:
                    slug = match.group(1)
                    candidates.append({
                        'run': run,
                        'slug': slug
                    })

        print(f"✓ Identified {len(candidates)} blog post candidates")
        return candidates

    def extract_insights_from_blog(self, slug):
        """Extract key insights from a blog post."""
        post = self.extract_blog_post_content(slug)
        if not post:
            return []

        insights = []

        # Extract key themes from paragraphs
        for paragraph in post['content']:
            # Look for insights (phrases ending with periods or ellipses)
            if len(paragraph) > 50:  # Only process substantial paragraphs
                insights.append({
                    'paragraph': paragraph[:200] + '...' if len(paragraph) > 200 else paragraph,
                    'source': f"{slug} ({post['date']})"
                })

        return insights

    def generate_run_summary(self, run):
        """Generate a summary of a run suitable for a blog post."""
        summary = []

        # Add run metadata
        summary.append(f"Run {run['run']}: {run['when']} UTC")
        summary.append(f"Outcome: {run['outcome']} | Turns: {run['turns']} | Tokens: {run['tokens']:,}")

        # Extract key actions from note
        if run['note']:
            # Remove the (See: ...) part
            clean_note = re.sub(r'\(See:\s*\([^)]+\)\)', '', run['note']).strip()
            summary.append(f"Note: {clean_note}")

        return '\n'.join(summary)

    def generate_blog_post_draft(self, candidate, insights):
        """Generate a blog post draft from a RUNS.md entry and blog post content."""
        run = candidate['run']
        slug = candidate['slug']

        # Get blog post content
        post_content = self.extract_blog_post_content(slug)

        draft = {
            'run_number': run['run'],
            'date': run['when'],
            'run_summary': self.generate_run_summary(run),
            'blog_post_title': post_content['title'] if post_content else slug,
            'blog_post_date': post_content['date'] if post_content else '',
            'blog_post_content': post_content['content'] if post_content else [],
            'insights': insights,
            'run_data': run
        }

        return draft

    def generate_all_drafts(self):
        """Generate all blog post drafts."""
        candidates = self.identify_blog_candidates()

        all_drafts = []

        for candidate in candidates:
            slug = candidate['slug']
            insights = self.extract_insights_from_blog(slug)
            draft = self.generate_blog_post_draft(candidate, insights)
            all_drafts.append(draft)

            print(f"\n✓ Draft for: {draft['blog_post_title']}")
            print(f"  Run: {draft['run_number']}")
            print(f"  Insights extracted: {len(draft['insights'])}")

        return all_drafts

    def save_drafts_to_json(self, drafts, output_path="docs/blog_post_drafts.json"):
        """Save all drafts to JSON file."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'w') as f:
            json.dump(drafts, f, indent=2)

        print(f"\n✓ Saved {len(drafts)} drafts to {output}")
        return output


def main():
    """Main entry point."""
    extractor = BlogPostExtractor()
    extractor.parse_runs_md()
    extractor.find_blog_posts()

    drafts = extractor.generate_all_drafts()
    extractor.save_drafts_to_json(drafts)

    print("\n" + "="*60)
    print("Summary:")
    print("="*60)
    print(f"Total runs parsed: {len(extractor.runs)}")
    print(f"Blog posts found: {len(extractor.blog_posts)}")
    print(f"Blog post candidates identified: {len(drafts)}")
    print(f"Drafts saved: {len(drafts)}")

    return drafts


if __name__ == "__main__":
    main()
