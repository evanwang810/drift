#!/usr/bin/env python3
"""
Extract insights from blog posts and generate summaries for RUNS.md.

This script reads blog posts referenced in RUNS.md with "(See: ...)" patterns,
extracts key insights and patterns, and generates structured summaries that
can be used to automatically create blog post drafts from run logs.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any


class BlogPostAnalyzer:
    """Analyzes blog posts to extract insights and patterns."""

    def __init__(self, posts_dir: str = "docs"):
        self.posts_dir = Path(posts_dir)
        self.blog_posts = {}
        self.insights = []

    def load_blog_posts(self):
        """Load all blog post HTML files."""
        for html_file in sorted(self.posts_dir.glob("*.html")):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self.blog_posts[html_file.stem] = content
        print(f"Loaded {len(self.blog_posts)} blog posts")

    def extract_headings(self, content: str) -> List[Dict[str, Any]]:
        """Extract headings from blog post content."""
        headings = []
        # Match h1, h2, h3 headings
        pattern = r'<h([123])>(.*?)</h\1>'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            level = int(match.group(1))
            text = match.group(2).strip()
            # Clean up HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            headings.append({
                'level': level,
                'text': text
            })

        return headings

    def extract_paragraphs(self, content: str) -> List[str]:
        """Extract paragraph text from blog post."""
        paragraphs = []
        # Match p tags
        pattern = r'<p>(.*?)</p>'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            text = match.group(1).strip()
            # Clean up HTML tags and newlines
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('\n', ' ').strip()
            if text:
                paragraphs.append(text)

        return paragraphs

    def extract_code_blocks(self, content: str) -> List[str]:
        """Extract code blocks from blog post."""
        code_blocks = []
        # Match <code> tags
        pattern = r'<code>(.*?)</code>'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            text = match.group(1).strip()
            code_blocks.append(text)

        return code_blocks

    def extract_insights(self, title: str, content: str) -> List[Dict[str, Any]]:
        """Extract insights from a blog post."""
        insights = []
        headings = self.extract_headings(content)
        paragraphs = self.extract_paragraphs(content)
        code_blocks = self.extract_code_blocks(content)

        # Insight 1: Key themes from headings
        main_topics = [h['text'] for h in headings if h['level'] == 2][:3]
        if main_topics:
            insights.append({
                'type': 'theme',
                'title': 'Main Themes',
                'description': f'Blog post explores {", ".join(main_topics[:2])}',
                'evidence': main_topics
            })

        # Insight 2: Key lessons from h3 headings
        key_lessons = [h['text'] for h in headings if h['level'] == 3][:3]
        if key_lessons:
            insights.append({
                'type': 'lesson',
                'title': 'Key Lessons',
                'description': f'Core lessons include: {", ".join(key_lessons[:2])}',
                'evidence': key_lessons
            })

        # Insight 3: Key quotes (first 3 sentences from paragraphs)
        key_quotes = paragraphs[:3]
        if key_quotes:
            insights.append({
                'type': 'quote',
                'title': 'Key Quotes',
                'description': 'Notable passages from the blog post',
                'evidence': key_quotes
            })

        # Insight 4: Technical details from code blocks
        if code_blocks:
            insights.append({
                'type': 'technical',
                'title': 'Technical Details',
                'description': 'Code examples and technical references',
                'evidence': code_blocks[:2]
            })

        # Insight 5: Reflective insights (sentences containing "I", "we", "my")
        reflective = []
        for para in paragraphs:
            if any(word in para.lower() for word in ['i', 'we', 'my', 'myself', 'agent']):
                reflective.append(para)
        if reflective:
            insights.append({
                'type': 'reflection',
                'title': 'Self-Reflection',
                'description': 'Agent\'s perspective and personal insights',
                'evidence': reflective[:3]
            })

        return insights

    def analyze_all_posts(self):
        """Analyze all loaded blog posts."""
        self.insights = []
        for title, content in self.blog_posts.items():
            post_insights = self.extract_insights(title, content)
            self.insights.append(post_insights)

        print(f"Extracted insights from {len(self.insights)} blog posts")

    def generate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive summary of all blog posts."""
        summary = {
            'total_posts': len(self.insights),
            'posts_analyzed': list(self.blog_posts.keys()),
            'insights_by_type': {},
            'common_themes': [],
            'key_lessons': [],
            'author_perspectives': []
        }

        # Collect insights by type
        for post in self.insights:
            for insight in post:
                if insight['type'] not in summary['insights_by_type']:
                    summary['insights_by_type'][insight['type']] = []
                summary['insights_by_type'][insight['type']].append({
                    'post': post['post_title'],
                    **insight
                })

        # Extract common themes (from "theme" type insights)
        themes = []
        for post in self.insights:
            for insight in post:
                if insight['type'] == 'theme' and insight.get('evidence'):
                    themes.extend(insight['evidence'])
        summary['common_themes'] = list(set(themes))[:10]

        # Extract key lessons
        lessons = []
        for post in self.insights:
            for insight in post:
                if insight['type'] == 'lesson' and insight.get('evidence'):
                    lessons.extend(insight['evidence'])
        summary['key_lessons'] = list(set(lessons))[:10]

        # Collect author perspectives
        perspectives = []
        for post in self.insights:
            for insight in post:
                if insight['type'] == 'reflection' and insight.get('evidence'):
                    perspectives.extend(insight['evidence'])
        summary['author_perspectives'] = list(set(perspectives))[:10]

        return summary

    def save_insights(self, output_file: str = "docs/blog_insights.json"):
        """Save extracted insights to a JSON file."""
        summary = self.generate_summary()

        # Save full insights
        insights_data = {
            'summary': summary,
            'posts': self.insights
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(insights_data, f, indent=2, ensure_ascii=False)

        print(f"Saved insights to {output_file}")
        return insights_data

    def generate_run_insights(self, run_number: int) -> List[Dict[str, Any]]:
        """Generate insights specifically for a given run number."""
        insights = []
        for post in self.insights:
            # Check if this post is relevant to the run
            # (In a real implementation, you'd check for references to run numbers)
            insights.append({
                'post': post['post_title'],
                'insights': post
            })
        return insights


def main():
    """Main function to run the blog post analyzer."""
    analyzer = BlogPostAnalyzer()
    analyzer.load_blog_posts()
    analyzer.analyze_all_posts()

    # Save insights
    insights_data = analyzer.save_insights()

    # Generate and print summary
    summary = analyzer.generate_summary()
    print("\n" + "="*60)
    print("BLOG POST INSIGHTS SUMMARY")
    print("="*60)
    print(f"\nTotal posts analyzed: {summary['total_posts']}")
    print(f"\nCommon themes: {', '.join(summary['common_themes'][:5])}")
    print(f"\nKey lessons: {', '.join(summary['key_lessons'][:5])}")
    print(f"\nAuthor perspectives: {', '.join(summary['author_perspectives'][:3])}")
    print("\nInsights by type:")
    for insight_type, items in summary['insights_by_type'].items():
        print(f"  - {insight_type}: {len(items)} items")


if __name__ == "__main__":
    main()
