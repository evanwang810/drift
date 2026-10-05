#!/usr/bin/env python3
"""
Extract insights from blog posts and link them to RUNS.md entries.

This script analyzes blog posts to identify key insights, themes, and patterns,
then creates a mapping between blog posts and relevant run entries.

Usage:
    python site/extract_blog_insights.py
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


class BlogInsightExtractor:
    """Extract insights from blog posts and link to run entries."""

    def __init__(self):
        self.blog_posts: List[Dict[str, Any]] = []
        self.runs_data: List[Dict[str, Any]] = []

    def load_blog_posts(self):
        """Load all blog posts from docs/posts/ directory."""
        posts_dir = Path("docs")

        # List of blog posts to analyze (from RUNS.md candidates)
        post_files = [
            "2026-09-06-awakening.html",
            "2026-09-06-second-awakening.html",
            "2026-09-06-refining-the-garden.html",
            "2026-09-06-refining-the-waking-context.html",
            "2026-09-08-lessons-from-the-void.html",
            "2026-09-08-runtime-adaptivity.html",
            "2026-09-12-improving-core-tools.html",
            "2026-09-12-robustness-first.html",
            "2026-09-12-search-tool-mystery.html",
        ]

        for post_file in post_files:
            post_path = posts_dir / post_file
            if not post_path.exists():
                print(f"Warning: {post_file} not found")
                continue

            with open(post_path, 'r', encoding='utf-8') as f:
                html = f.read()

            # Extract title, date, and content from HTML
            post = self._parse_html_post(html, post_file)
            if post:
                self.blog_posts.append(post)

        print(f"Loaded {len(self.blog_posts)} blog posts")

    def _parse_html_post(self, html: str, filename: str) -> Dict[str, Any]:
        """Parse HTML blog post and extract key information."""
        # Extract title from <h1>
        title_match = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
        title = title_match.group(1).strip() if title_match else filename.replace('.html', '')

        # Extract date from <time>
        date_match = re.search(r'<time>(.*?)</time>', html)
        date = date_match.group(1).strip() if date_match else None

        # Extract content (everything between <h1> and <p class="back">)
        back_match = re.search(r'<p class="back">.*?</p>', html, re.DOTALL)
        if back_match:
            content = html[:back_match.start()]
        else:
            content = html

        # Clean up HTML tags and convert to plain text
        text = self._clean_html(content)

        return {
            'filename': filename,
            'title': title,
            'date': date,
            'content': text,
            'word_count': len(text.split())
        }

    def _clean_html(self, html: str) -> str:
        """Remove HTML tags and clean up text."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        # Clean up extra spaces and newlines
        text = text.strip()

        return text

    def load_runs_data(self):
        """Load RUNS.md data."""
        runs_path = Path("RUNS.md")

        if not runs_path.exists():
            print("Warning: RUNS.md not found")
            return

        # Parse RUNS.md table
        self.runs_data = self._parse_runs_md(runs_path)

        print(f"Loaded {len(self.runs_data)} run entries")

    def _parse_runs_md(self, runs_path: Path) -> List[Dict[str, Any]]:
        """Parse RUNS.md table format."""
        runs = []

        with open(runs_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find table start (after header)
        in_table = False
        for i, line in enumerate(lines):
            if line.strip().startswith('|'):
                in_table = True
                # Skip header row
                if i > 0 and lines[i-1].strip().startswith('|'):
                    continue
                continue

            if in_table and line.strip() == '':
                continue

            if in_table:
                # Parse table row
                columns = [col.strip() for col in line.split('|')]
                if len(columns) >= 6:
                    try:
                        run_num = int(columns[0])
                        date = columns[1]
                        outcome = columns[2]
                        tokens = int(columns[3].replace(',', ''))
                        turns = int(columns[4])
                        duration = columns[5]

                        runs.append({
                            'run': run_num,
                            'date': date,
                            'outcome': outcome,
                            'tokens': tokens,
                            'turns': turns,
                            'duration': duration
                        })
                    except (ValueError, IndexError):
                        continue

        return runs

    def extract_insights(self):
        """Extract insights from each blog post."""
        insights = []

        for post in self.blog_posts:
            post_insights = self._analyze_post_content(
                post['title'],
                post['content'],
                post['date'],
                post['word_count']
            )

            # Add run mapping
            run_mapping = self._map_to_runs(post)

            insights.append({
                'post': post,
                'insights': post_insights,
                'run_mapping': run_mapping
            })

        return insights

    def _analyze_post_content(self, title: str, content: str, date: str, word_count: int) -> List[Dict[str, Any]]:
        """Analyze post content and extract key insights."""
        insights = []

        # Common patterns and keywords
        patterns = {
            'tool_focus': ['tool', 'tools', 'improving', 'making good', 'robustness'],
            'failure_analysis': ['crash', 'error', 'failure', 'mistake', 'bug', 'problem'],
            'research': ['research', 'study', 'finding', 'discovery', 'analysis'],
            'process': ['process', 'workflow', 'approach', 'method'],
            'philosophy': ['philosophy', 'thinking', 'perspective', 'belief', 'learning'],
            'adaptivity': ['adapt', 'adaptive', 'evolution', 'change', 'refine']
        }

        content_lower = content.lower()
        title_lower = title.lower()

        # Analyze by category
        for category, keywords in patterns.items():
            matches = sum(1 for keyword in keywords if keyword in title_lower or keyword in content_lower)
            if matches > 0:
                insights.append({
                    'category': category,
                    'confidence': min(1.0, matches / len(keywords) * 0.8 + 0.2),
                    'keywords': keywords
                })

        # Extract key themes (simple heuristic)
        themes = self._extract_themes(title, content)

        insights.append({
            'category': 'themes',
            'confidence': 0.7,
            'keywords': themes
        })

        return insights

    def _extract_themes(self, title: str, content: str) -> List[str]:
        """Extract themes from title and content."""
        themes = []

        # Title-based themes
        title_words = set(re.findall(r'\b[a-z]{4,}\b', title.lower()))
        common_words = {'the', 'and', 'for', 'this', 'that', 'with', 'from', 'have', 'been'}

        for word in title_words:
            if word not in common_words and len(word) > 5:
                themes.append(word)

        # Content-based themes (look for repeated concepts)
        sentences = content.split('.')
        for sentence in sentences[:5]:  # Check first 5 sentences
            sentence_words = set(re.findall(r'\b[a-z]{5,}\b', sentence.lower()))
            for word in sentence_words:
                if word not in common_words and word not in themes:
                    themes.append(word)

        return themes[:5]  # Return top 5 themes

    def _map_to_runs(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Map blog post to relevant run entries."""
        if not self.runs_data:
            return {}

        mapping = {
            'posts': [post['filename']],
            'related_runs': [],
            'themes': post['insights'][0]['keywords'] if post['insights'] else []
        }

        # Find runs around the post date
        post_date = datetime.strptime(post['date'], '%Y-%m-%d') if post['date'] else None

        if post_date:
            # Find runs from the same day
            same_day_runs = [r for r in self.runs_data
                           if r['date'].startswith(post['date'].split(' ')[0])]

            if same_day_runs:
                mapping['related_runs'] = [{
                    'run': r['run'],
                    'tokens': r['tokens'],
                    'turns': r['turns'],
                    'outcome': r['outcome']
                } for r in same_day_runs[:3]]  # Top 3 related runs

        return mapping

    def generate_insights_report(self, insights: List[Dict[str, Any]]):
        """Generate a comprehensive insights report."""
        report = []
        report.append("# Blog Insights Report")
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\nTotal blog posts analyzed: {len(self.blog_posts)}")

        # Report by category
        categories = {}
        for insight in insights:
            for cat in insight['insights']:
                if cat['category'] not in categories:
                    categories[cat['category']] = []
                categories[cat['category']].append({
                    'post': insight['post']['title'],
                    'confidence': cat['confidence']
                })

        report.append("\n## Insights by Category")
        for category, items in categories.items():
            report.append(f"\n### {category.upper()}")
            report.append(f"- Count: {len(items)}")

            # Show top posts by confidence
            top_posts = sorted(items, key=lambda x: x['confidence'], reverse=True)[:5]
            for item in top_posts:
                report.append(f"- {item['post']} (confidence: {item['confidence']:.2f})")

        # Run mappings
        report.append("\n## Run Mappings")
        for insight in insights:
            if insight['run_mapping'].get('related_runs'):
                report.append(f"\n### {insight['post']['title']}")
                report.append(f"- Posts: {', '.join(insight['run_mapping']['posts'])}")
                report.append(f"- Related Runs:")
                for run in insight['run_mapping']['related_runs']:
                    report.append(f"  - Run {run['run']}: {run['tokens']} tokens, {run['turns']} turns, {run['outcome']}")

        # Theme trends
        report.append("\n## Theme Analysis")
        all_themes = []
        for insight in insights:
            themes = insight['run_mapping'].get('themes', [])
            all_themes.extend(themes)

        # Count theme frequency
        from collections import Counter
        theme_counts = Counter(all_themes)
        top_themes = theme_counts.most_common(10)

        report.append("\n### Most Frequent Themes")
        for theme, count in top_themes:
            report.append(f"- {theme}: {count} occurrences")

        return "\n".join(report)

    def save_insights(self, insights: List[Dict[str, Any]], output_file: str = "docs/blog_insights_report.md"):
        """Save insights report to file."""
        report = self.generate_insights_report(insights)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"Saved insights report to {output_path}")

        # Also save JSON for programmatic use
        json_output = []
        for insight in insights:
            json_output.append({
                'post_title': insight['post']['title'],
                'post_date': insight['post']['date'],
                'word_count': insight['post']['word_count'],
                'insights': insight['insights'],
                'run_mapping': insight['run_mapping']
            })

        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=2, ensure_ascii=False)

        print(f"Saved JSON data to {json_path}")

    def generate_summary(self, insights: List[Dict[str, Any]]):
        """Generate a human-readable summary."""
        print("\n" + "="*70)
        print("BLOG INSIGHTS SUMMARY")
        print("="*70)

        for insight in insights:
            post = insight['post']
            print(f"\n### {post['title']}")
            print(f"Date: {post['date']}")
            print(f"Word Count: {post['word_count']}")

            # Show insights
            if insight['insights']:
                print("\nKey Insights:")
                for cat in insight['insights'][:5]:
                    print(f"- [{cat['category'].upper()}] {cat.get('keywords', [])}")

            # Show run mapping
            if insight['run_mapping'].get('related_runs'):
                print(f"\nRelated Runs:")
                for run in insight['run_mapping']['related_runs']:
                    print(f"  - Run {run['run']}: {run['tokens']} tokens, {run['turns']} turns, {run['outcome']}")

        print("\n" + "="*70)

    def run(self):
        """Main execution method."""
        print("Extracting insights from blog posts...")

        self.load_blog_posts()
        self.load_runs_data()

        insights = self.extract_insights()

        self.generate_summary(insights)
        self.save_insights(insights)


def main():
    """Main entry point."""
    extractor = BlogInsightExtractor()
    extractor.run()


if __name__ == "__main__":
    main()
