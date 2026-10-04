#!/usr/bin/env python3
"""
Extract insights from blog posts and bridge the gap between RUNS.md entries
and reflective blog posts, creating a natural flow of insights from technical
logs to blog content.
"""

import re
import json
import os
from pathlib import Path
from datetime import datetime


class BlogInsightExtractor:
    """Extract insights from blog posts and create summaries."""

    def __init__(self):
        self.blog_posts = {}
        self.runs_with_blog_refs = []

    def find_blog_posts(self, posts_dir="docs/_posts"):
        """Find all blog posts in the posts directory."""
        posts_path = Path(posts_dir)
        if not posts_path.exists():
            print(f"Warning: Posts directory not found: {posts_path}")
            return

        for md_file in posts_path.glob("*.md"):
            self.blog_posts[md_file.name] = md_file

        print(f"Found {len(self.blog_posts)} blog posts")

    def extract_blog_metadata(self, md_file):
        """Extract metadata from a blog post markdown file."""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title (first H1)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "Untitled"

        # Extract date
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
        date_str = date_match.group(1) if date_match else "Unknown"

        # Extract tags
        tags = []
        tags_match = re.search(r'tags:\s*\[(.+)\]', content)
        if tags_match:
            tags = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]

        # Extract categories
        categories = []
        cats_match = re.search(r'categories:\s*\[(.+)\]', content)
        if cats_match:
            categories = [c.strip().strip('"\'') for c in cats_match.group(1).split(',')]

        # Extract the main content (after frontmatter)
        frontmatter_end = content.find('---\n\n')
        if frontmatter_end != -1:
            main_content = content[frontmatter_end + 4:].strip()
        else:
            main_content = content.strip()

        return {
            'filename': md_file.name,
            'title': title,
            'date': date_str,
            'tags': tags,
            'categories': categories,
            'content': main_content,
            'full_content': content
        }

    def find_runs_with_blog_refs(self, runs_md_path="RUNS.md"):
        """Find all runs in RUNS.md that reference blog posts."""
        runs_path = Path(runs_md_path)
        if not runs_path.exists():
            print(f"Warning: RUNS.md not found: {runs_path}")
            return []

        run_entries = []

        with open(runs_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Parse the table
        in_table = False
        for i, line in enumerate(lines):
            if line.startswith('| run |'):
                in_table = True
                continue

            if in_table and line.startswith('| --:'):
                in_table = False
                continue

            if in_table and line.strip():
                # Parse table row
                columns = [col.strip() for col in line.split('|')[1:-1]]

                if len(columns) >= 6:
                    run_num = int(columns[0])
                    when = columns[1]
                    outcome = columns[2]
                    turns = int(columns[3])
                    tokens = int(columns[4].replace(',', ''))
                    note = columns[5]

                    # Check for blog reference
                    blog_refs = self._extract_blog_refs(note)
                    if blog_refs:
                        run_entries.append({
                            'run': run_num,
                            'when': when,
                            'outcome': outcome,
                            'turns': turns,
                            'tokens': tokens,
                            'note': note,
                            'blog_refs': blog_refs
                        })

        self.runs_with_blog_refs = run_entries
        print(f"Found {len(run_entries)} runs with blog references")
        return run_entries

    def _extract_blog_refs(self, note):
        """Extract blog post references from a note."""
        # Try multiple formats for blog references
        patterns = [
            r'See:\s*\[([^\]]+)\]\(([^)]+)\)',  # See: ([ 2026-09-06-awakening.md](...))
            r'See:\s*\[([^\]]+)\]\(([^)]+)\)',  # See: ([2026-09-06-awakening.md](...))
            r'\((See:\s*\[([^\]]+)\]\([^)]+\))\)',  # (See: ([ 2026-09-06-awakening.md](...)))
            r'See:\s*\[([^\]]+)\]\(([^)]+)\)',  # See: ([2026-09-06-awakening.md](...))
        ]
        
        for pattern in patterns:
            refs = re.findall(pattern, note)
            if refs:
                break
        
        blog_refs = []
        for title, link in refs:
            # Extract filename from link
            filename = link.split('/')[-1] if '/' in link else link
            if filename.endswith('.md'):
                filename = filename[:-3]  # Remove .md extension
            blog_refs.append({
                'title': title,
                'link': link,
                'filename': filename
            })

        return blog_refs

    def extract_insights_from_blog(self, blog_data):
        """Extract key insights from a blog post."""
        insights = []

        content = blog_data['content'].lower()

        # Extract key themes based on content patterns
        if 'awakening' in content:
            insights.append('Theme: Awakening and initial setup')
            insights.append('Key: Understanding the environment and available tools')

        if 'refining' in content or 'improving' in content:
            insights.append('Theme: Refinement and improvement')
            insights.append('Key: Iterative process of building and optimizing')

        if 'lessons' in content or 'failure' in content:
            insights.append('Theme: Learning from failure')
            insights.append('Key: Treat crashes and errors as data, not interruptions')

        if 'runtime' in content or 'adaptivity' in content:
            insights.append('Theme: Runtime adaptivity')
            insights.append('Key: Plans are hypotheses; validate against traces')

        if 'research' in content or 'TROVE' in content or 'BUGSTONE' in content:
            insights.append('Theme: Research and investigation')
            insights.append('Key: Exploring the broader landscape of agent capabilities')

        # Extract key takeaways
        paragraphs = blog_data['content'].split('\n\n')
        key_takeaways = []

        for para in paragraphs:
            if len(para) > 100 and len(para) < 500:
                # Look for bullet points or numbered lists
                if re.search(r'^[\d\-\*\+]\s+', para):
                    key_takeaways.append(para.strip())

        return {
            'title': blog_data['title'],
            'date': blog_data['date'],
            'tags': blog_data['tags'],
            'categories': blog_data['categories'],
            'insights': insights,
            'key_takeaways': key_takeaways[:3],  # Limit to top 3
            'content_preview': blog_data['content'][:300] + '...'
        }

    def generate_blog_run_summary(self, run_entry, blog_data):
        """Generate a summary that bridges the run log and blog post."""
        summary = {
            'run': run_entry['run'],
            'when': run_entry['when'],
            'outcome': run_entry['outcome'],
            'turns': run_entry['turns'],
            'tokens': run_entry['tokens'],
            'blog_post': {
                'title': blog_data['title'],
                'filename': blog_data['filename'],
                'date': blog_data['date'],
                'tags': blog_data['tags'],
                'categories': blog_data['categories']
            },
            'connection': {
                'theme': self._extract_theme(blog_data['content']),
                'insights': blog_data['insights'],
                'run_context': self._extract_run_context(run_entry['note'])
            },
            'summary_text': self._generate_summary_text(run_entry, blog_data)
        }

        return summary

    def _extract_theme(self, content):
        """Extract the main theme from blog content."""
        content_lower = content.lower()

        themes = {
            'awakening': 'awakening',
            'digital garden': 'garden',
            'refining': 'refinement',
            'waking context': 'context',
            'lessons': 'lessons',
            'void': 'lessons',
            'runtime': 'runtime',
            'adaptivity': 'adaptivity',
            'research': 'research',
            'architecture': 'architecture'
        }

        for theme, keyword in themes.items():
            if keyword in content_lower:
                return theme

        return 'general'

    def _extract_run_context(self, note):
        """Extract key context from the run note."""
        if 'blocked' in note.lower():
            return 'permission issue, could not enable GitHub Pages'
        elif 'expanded' in note.lower() or 'refined' in note.lower():
            return 'expanding or refining the website'
        elif 'crashed' in note.lower():
            return 'run crashed, likely due to system issue'
        elif 'research' in note.lower():
            return 'conducting research on LLM agents'
        else:
            return 'general work on the project'

    def _generate_summary_text(self, run_entry, blog_data):
        """Generate a human-readable summary text."""
        theme = self._extract_theme(blog_data['content'])
        run_context = self._extract_run_context(run_entry['note'])

        texts = {
            'awakening': f"Run {run_entry['run']} ({run_entry['when']}) - {blog_data['title']}. Initial awakening phase focused on understanding the environment and setting up foundational tools.",
            'garden': f"Run {run_entry['run']} ({run_entry['when']}) - {blog_data['title']}. Building the digital garden, establishing identity through documentation and structure.",
            'refinement': f"Run {run_entry['run']} ({run_entry['when']}) - {blog_data['title']}. Iterative refinement of the digital garden, fixing issues and improving structure.",
            'context': f"Run {run_entry['run']} ({run_entry['when']}) - {blog_data['title']}. Refining the waking context and file tree structure for better orientation.",
            'lessons': f"Run {run_entry['run']} ({run_entry['when']}) - {blog_data['title']}. Learning from failures and crashes, understanding system dependencies.",
            'runtime': f"Run {run_entry['run']} ({run_entry['when']}) - {blog_data['title']}. Research on runtime adaptivity and LLM agent architecture.",
            'research': f"Run {run_entry['run']} ({run_entry['when']}) - {blog_data['title']}. Research into the state of LLM agents in late 2026."
        }

        return texts.get(theme, f"Run {run_entry['run']} ({run_entry['when']}) - {blog_data['title']}. {run_context}")

    def generate_all_summaries(self):
        """Generate summaries for all blog-run connections."""
        summaries = []

        for run_entry in self.runs_with_blog_refs:
            blog_file = self.blog_posts.get(run_entry['blog_refs'][0]['filename'] + '.md')

            if not blog_file:
                print(f"Warning: Blog file not found for {run_entry['blog_refs'][0]['filename']}")
                continue

            blog_data = self.extract_blog_metadata(blog_file)
            summary = self.generate_blog_run_summary(run_entry, blog_data)
            summaries.append(summary)

        return summaries

    def save_summaries(self, summaries, output_path="docs/blog_run_summaries.json"):
        """Save summaries to a JSON file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.utcnow().isoformat(),
                'total_summaries': len(summaries),
                'summaries': summaries
            }, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(summaries)} summaries to {output_path}")
        return output_path


def main():
    """Main entry point."""
    extractor = BlogInsightExtractor()

    # Find blog posts
    extractor.find_blog_posts()

    # Find runs with blog references
    extractor.find_runs_with_blog_refs()

    # Generate all summaries
    summaries = extractor.generate_all_summaries()

    # Save summaries
    if summaries:
        extractor.save_summaries(summaries)

        # Print summary statistics
        print("\n" + "="*60)
        print("BLOG-RUN CONNECTIONS SUMMARY")
        print("="*60)
        print(f"Total connections: {len(summaries)}")
        print(f"Blog posts analyzed: {len(extractor.blog_posts)}")
        print(f"Runs with blog references: {len(extractor.runs_with_blog_refs)}")

        # Count by theme
        themes = {}
        for summary in summaries:
            theme = summary['connection']['theme']
            themes[theme] = themes.get(theme, 0) + 1

        print("\nThemes:")
        for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {theme}: {count}")

        print("\nSample connections:")
        for summary in summaries[:3]:
            print(f"  Run {summary['run']}: {summary['blog_post']['title']} ({summary['summary_text'][:60]}...)")


if __name__ == "__main__":
    main()
