#!/usr/bin/env python3
"""
Blog Insights Extractor

This script extracts key insights from blog posts referenced in RUNS.md
and generates structured summaries for human review.

Usage:
    python site/extract_blog_insights.py
"""

import json
import os
from pathlib import Path
from datetime import datetime


class BlogInsightsExtractor:
    """Extracts insights from blog posts and generates summaries."""

    def __init__(self, posts_dir="docs/_posts", output_file="docs/blog_post_insights.json"):
        self.posts_dir = Path(posts_dir)
        self.output_file = Path(output_file)
        self.blog_posts = []

    def load_all_posts(self):
        """Load all markdown blog posts."""
        print(f"Loading blog posts from {self.posts_dir}...")

        for post_file in sorted(self.posts_dir.glob("*.md")):
            if post_file.name.startswith("2026-09"):
                try:
                    content = post_file.read_text()
                    post_info = self._parse_post_metadata(content, post_file.name)
                    self.blog_posts.append(post_info)
                    print(f"  ✓ Loaded: {post_file.name}")
                except Exception as e:
                    print(f"  ✗ Error loading {post_file.name}: {e}")

        print(f"\nLoaded {len(self.blog_posts)} blog posts")
        return self.blog_posts

    def _parse_post_metadata(self, content, filename):
        """Parse frontmatter and extract post metadata."""
        # Handle both string and list inputs
        if isinstance(content, list):
            content = '\n'.join(content)
        lines = content.split('\n')

        # Find frontmatter boundaries
        if lines[0].startswith('---'):
            frontmatter_end = 1
            while frontmatter_end < len(lines) and not lines[frontmatter_end].startswith('---'):
                frontmatter_end += 1

            # Parse frontmatter
            frontmatter = {}
            for line in lines[1:frontmatter_end]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    frontmatter[key] = value

            # Extract body content
            body_start = frontmatter_end + 1
            body = '\n'.join(lines[body_start:])

            return {
                'filename': filename,
                'title': frontmatter.get('title', filename),
                'date': frontmatter.get('date', ''),
                'tags': frontmatter.get('tags', '').split(','),
                'categories': frontmatter.get('categories', []).split(','),
                'body': body,
                'word_count': len(body.split())
            }
        else:
            # No frontmatter, treat entire file as body
            return {
                'filename': filename,
                'title': filename.replace('.md', ''),
                'date': '',
                'tags': [],
                'categories': [],
                'body': content,
                'word_count': len(content.split())
            }

    def extract_key_themes(self, post):
        """Extract key themes and insights from a post."""
        body = post['body'].lower()

        themes = {
            'architecture': [],
            'meta_reflection': [],
            'process': [],
            'research': [],
            'discovery': [],
            'failure': [],
            'growth': []
        }

        # Look for common patterns
        if 'architecture' in body or 'context' in body:
            themes['architecture'] = ['system design', 'perception', 'environment']

        if 'reflection' in body or 'meta' in body:
            themes['meta_reflection'] = ['self-awareness', 'introspection']

        if 'fail' in body or 'crash' in body:
            themes['failure'] = ['error handling', 'resilience', 'recovery']

        if 'ground' in body or 'verify' in body:
            themes['growth'] = ['validation', 'reliability', 'grounding']

        if 'research' in body or 'framework' in body:
            themes['research'] = ['knowledge', 'adaptation']

        return themes

    def generate_summary(self, post):
        """Generate a human-readable summary of a post."""
        themes = self.extract_key_themes(post)

        summary_parts = []
        summary_parts.append(f"**{post['title']}** ({post['date']})")

        if themes['architecture']:
            summary_parts.append(f"- Architecture focus: {', '.join(themes['architecture'])}")

        if themes['meta_reflection']:
            summary_parts.append(f"- Meta-reflection: {', '.join(themes['meta_reflection'])}")

        if themes['failure']:
            summary_parts.append(f"- Lessons on failure: {', '.join(themes['failure'])}")

        if themes['growth']:
            summary_parts.append(f"- Growth focus: {', '.join(themes['growth'])}")

        summary_parts.append(f"- Word count: {post['word_count']}")

        return '\n'.join(summary_parts)

    def extract_insights(self):
        """Extract insights from all posts and structure them."""
        print("\nExtracting insights from blog posts...")

        all_insights = []
        total_words = 0

        for post in self.blog_posts:
            themes = self.extract_key_themes(post)
            summary = self.generate_summary(post)

            insight = {
                'post': post,
                'themes': themes,
                'summary': summary,
                'extracted_at': datetime.now().isoformat()
            }

            all_insights.append(insight)
            total_words += post['word_count']

            print(f"\n{post['title']} ({post['date']})")
            print(f"  Themes: {list(themes.keys())}")
            print(f"  Word count: {post['word_count']}")

        print(f"\nTotal insights extracted: {len(all_insights)}")
        print(f"Total word count: {total_words}")

        return all_insights

    def save_results(self, insights):
        """Save extracted insights to JSON file."""
        print(f"\nSaving results to {self.output_file}...")

        output = {
            'extraction_metadata': {
                'extraction_date': datetime.now().isoformat(),
                'total_posts_analyzed': len(self.blog_posts),
                'total_insights': len(insights),
                'total_word_count': sum(post['word_count'] for post in self.blog_posts)
            },
            'insights': insights
        }

        self.output_file.write_text(json.dumps(output, indent=2))

        print(f"  ✓ Results saved")
        return output

    def generate_report(self, insights):
        """Generate a human-readable report."""
        print("\n" + "="*70)
        print("BLOG INSIGHTS EXTRACTION REPORT")
        print("="*70)

        # Summary by theme
        print("\n### Summary by Theme")
        print("-" * 70)

        theme_counts = {}
        for insight in insights:
            for theme in insight['themes'].keys():
                theme_counts[theme] = theme_counts.get(theme, 0) + 1

        for theme, count in sorted(theme_counts.items(), key=lambda x: -x[1]):
            print(f"- {theme}: {count} posts")

        # Recent posts
        print("\n### Recent Posts")
        print("-" * 70)

        recent_posts = sorted(self.blog_posts, key=lambda x: x['date'], reverse=True)[:5]
        for post in recent_posts:
            print(f"- {post['date']}: {post['title']}")

        # Statistics
        print("\n### Statistics")
        print("-" * 70)
        print(f"Total posts analyzed: {len(self.blog_posts)}")
        print(f"Total word count: {sum(post['word_count'] for post in self.blog_posts):,}")
        print(f"Average word count per post: {sum(post['word_count'] for post in self.blog_posts) // len(self.blog_posts):,}")

    def run(self):
        """Run the complete extraction pipeline."""
        print("Blog Insights Extractor")
        print("=" * 70)

        self.load_all_posts()
        insights = self.extract_insights()
        output = self.save_results(insights)
        self.generate_report(insights)

        print("\n" + "="*70)
        print("Extraction complete!")
        print("="*70)

        return output


if __name__ == "__main__":
    extractor = BlogInsightsExtractor()
    extractor.run()
