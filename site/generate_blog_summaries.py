#!/usr/bin/env python3
"""
Generate blog post summaries from RUNS.md entries.

This script extracts insights from RUNS.md entries that reference blog posts,
and generates summaries that can be used to create or update blog posts.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

class BlogSummaryGenerator:
    """Generate blog post summaries from run entries and blog posts."""

    def __init__(self):
        self.runs_path = Path('RUNS.md')
        self.blog_dir = Path('docs')
        self.candidates = []

    def find_blog_candidates(self):
        """Find runs in RUNS.md that reference blog posts."""
        content = self.runs_path.read_text()

        # Look for (See: (...)) patterns in notes
        # This pattern matches the blog post reference format
        # Extracts content between (See: and the final ))
        pattern = r'\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\(\(See:\s*(.*?)\)\)\s*\|'

        self.candidates = []
        for match in re.finditer(pattern, content, re.DOTALL):
            run_num = int(match.group(1))
            date = match.group(2)
            outcome = match.group(4)
            turns = int(match.group(5))
            tokens = int(match.group(6))
            note = match.group(7).strip(' )')
            post_ref = match.group(8).strip()

            # Extract just the filename from the reference
            post_filename = post_ref.split('/')[-1].split('\\')[-1] if '/' in post_ref or '\\' in post_ref else post_ref

            self.candidates.append({
                'run': run_num,
                'date': date,
                'outcome': outcome,
                'turns': turns,
                'tokens': tokens,
                'note': note,
                'post_file': post_filename,
                'post_ref': post_ref
            })

        print(f"Found {len(self.candidates)} blog post candidates")
        return self.candidates

    def read_blog_post(self, filename):
        """Read a blog post from HTML file."""
        post_path = self.blog_dir / filename

        if not post_path.exists():
            print(f"  Warning: Blog post {filename} not found")
            return None

        content = post_path.read_text()

        # Parse HTML and extract title, date, and body
        soup = BeautifulSoup(content, 'html.parser')

        # Get title
        title = soup.find('h1').text.strip() if soup.find('h1') else 'Untitled'

        # Get date from meta
        date_elem = soup.find('time')
        date = date_elem.text.strip() if date_elem else 'Unknown'

        # Get body content
        article = soup.find('article')
        if article:
            paragraphs = article.find_all('p')
            body = '\n'.join(p.text.strip() for p in paragraphs)
        else:
            body = soup.body.text.strip()

        return {
            'title': title,
            'date': date,
            'body': body
        }

    def extract_insights(self, blog_content):
        """Extract key insights and themes from blog content."""
        insights = []

        # Look for common blog post structures
        # 1. Introduction and awakening
        if 'awakening' in blog_content.lower():
            insights.append(('theme', 'awakening', 'Initial awakening and setup'))

        # 2. Refining and improving
        if 'refining' in blog_content.lower():
            insights.append(('theme', 'refinement', 'Process of refining and improvement'))

        # 3. Lessons and failures
        if 'lesson' in blog_content.lower() or 'failure' in blog_content.lower():
            insights.append(('theme', 'reflection', 'Learning from failures and mistakes'))

        # 4. Runtime adaptivity
        if 'runtime' in blog_content.lower() and 'adaptivity' in blog_content.lower():
            insights.append(('theme', 'adaptivity', 'Adapting plans at runtime'))

        # 5. Research and discovery
        if 'research' in blog_content.lower() or 'read' in blog_content.lower():
            insights.append(('theme', 'research', 'Research and exploration'))

        # 6. Technical improvements
        if 'improvement' in blog_content.lower() or 'fix' in blog_content.lower():
            insights.append(('theme', 'technical', 'Technical improvements and fixes'))

        # 7. Digital garden concept
        if 'digital garden' in blog_content.lower():
            insights.append(('theme', 'philosophy', 'Digital garden as a survival strategy'))

        return insights

    def generate_summary(self, run_info, blog_post):
        """Generate a summary that bridges run data and blog content."""
        if not blog_post:
            return None

        insights = self.extract_insights(blog_post['body'])

        summary = {
            'run': run_info['run'],
            'date': run_info['date'],
            'outcome': run_info['outcome'],
            'turns': run_info['turns'],
            'tokens': run_info['tokens'],
            'blog_title': blog_post['title'],
            'blog_date': blog_post['date'],
            'insights': insights,
            'key_themes': list(set([ins[1] for ins in insights]))
        }

        return summary

    def generate_all_summaries(self):
        """Generate summaries for all blog post candidates."""
        self.find_blog_candidates()

        summaries = []

        for candidate in self.candidates:
            print(f"\nProcessing Run {candidate['run']} - {candidate['post_file']}")

            # Read the blog post
            blog_post = self.read_blog_post(candidate['post_file'])

            if blog_post:
                # Generate summary
                summary = self.generate_summary(candidate, blog_post)
                summaries.append(summary)

                # Print summary
                print(f"  Blog: {blog_post['title']}")
                print(f"  Themes: {', '.join(summary['key_themes'])}")
                print(f"  Insights: {len(summary['insights'])} found")

        return summaries

    def generate_markdown_summary(self, summary):
        """Generate a markdown-formatted summary."""
        md = f"""## Run {summary['run']} ({summary['date']})

**Outcome:** {summary['outcome']}
**Turns:** {summary['turns']}
**Tokens:** {summary['tokens']}

### Blog Post: {summary['blog_title']}

{summary['blog_date']}

### Key Themes

{', '.join(summary['key_themes'])}

### Insights

"""

        for theme, name, description in summary['insights']:
            md += f"- **{name}**: {description}\n"

        md += "\n### Full Blog Content\n\n"
        md += summary['body'][:1000] + "..." if len(summary['body']) > 1000 else summary['body']

        return md

    def export_summaries(self, output_file='docs/blog_summaries.md'):
        """Export all summaries to markdown file."""
        summaries = self.generate_all_summaries()

        if not summaries:
            print("No summaries generated")
            return

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open('w', encoding='utf-8') as f:
            f.write("# Blog Post Summaries from Runs\n\n")
            f.write(f"Generated: {Path('RUNS.md').stat().st_mtime}\n\n")
            f.write("## Summary\n\n")
            f.write(f"Found {len(summaries)} blog post summaries across {len(self.candidates)} referenced runs.\n\n")
            f.write("---\n\n")

            for i, summary in enumerate(summaries, 1):
                f.write(f"## Summary {i}: Run {summary['run']}\n\n")
                f.write(self.generate_markdown_summary(summary))
                f.write("\n\n---\n\n")

        print(f"\nExported {len(summaries)} summaries to {output_file}")
        return output_path


if __name__ == '__main__':
    generator = BlogSummaryGenerator()
    generator.export_summaries()
