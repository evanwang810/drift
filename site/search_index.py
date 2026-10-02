#!/usr/bin/env python3
"""
Search Index Generator

Creates a searchable index from:
- docs/knowledge_base.json
- docs/*.md files (log.md, failures.md, projects.md, etc.)
- docs/posts/*.html files

The index can be queried by any search function.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import Counter
import re


class SearchIndex:
    """Manages a searchable index of documentation content."""

    def __init__(self):
        self.index = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_entries": 0,
                "total_words": 0,
                "sources": []
            },
            "entries": []
        }
        self.content_cache = {}

    def load_file(self, filepath):
        """Load and return content from a file."""
        if filepath in self.content_cache:
            return self.content_cache[filepath]

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.content_cache[filepath] = content
            return content
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")
            return ""

    def extract_keywords(self, text, max_keywords=10):
        """Extract meaningful keywords from text using simple techniques."""
        # Remove markdown formatting
        text = re.sub(r'#{2,6}\s', '', text)  # Remove headers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Remove italics
        text = re.sub(r'`([^`]+)`', r'\1', text)  # Remove code
        text = re.sub(r'\[[^\]]+\]\([^)]+\)', '', text)  # Remove links
        text = re.sub(r'\[[^\]]+\]', '', text)  # Remove link text

        # Split into words, remove common stop words
        words = text.lower().split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
                      'with', 'by', 'from', 'that', 'this', 'is', 'are', 'was', 'were',
                      'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                      'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall'}

        keywords = [word for word in words if len(word) > 3 and word not in stop_words]

        # Count and get most common
        counter = Counter(keywords)
        return [item[0] for item in counter.most_common(max_keywords)]

    def add_knowledge_base_entry(self, entry):
        """Add a knowledge base entry to the index."""
        if not entry.get('title'):
            return

        text = f"{entry.get('title', '')} {entry.get('description', '')} {entry.get('implementation', '')} {entry.get('verification', '')} {entry.get('impact', '')}"
        keywords = self.extract_keywords(text)

        self.index["entries"].append({
            "type": "knowledge",
            "source": "knowledge_base",
            "title": entry.get('title', ''),
            "description": entry.get('description', ''),
            "keywords": keywords,
            "text": text,
            "tags": entry.get('tags', ''),
            "id": entry.get('title', '').lower().replace(' ', '-')
        })

    def add_markdown_file(self, filepath, category="documentation"):
        """Add content from a markdown file to the index."""
        content = self.load_file(filepath)
        if not content:
            return

        # Extract title from front matter or filename
        title = os.path.basename(filepath).replace('.md', '')

        # Simple title extraction from first line if it's a heading
        first_line = content.strip().split('\n')[0] if content.strip() else ""
        if first_line.startswith('# '):
            title = first_line[2:].strip()

        keywords = self.extract_keywords(content)

        self.index["entries"].append({
            "type": "documentation",
            "source": category,
            "title": title,
            "description": "",
            "keywords": keywords,
            "text": content,
            "tags": category,
            "id": os.path.basename(filepath).replace('.md', '')
        })

    def add_html_file(self, filepath, category="posts"):
        """Add content from an HTML file to the index."""
        content = self.load_file(filepath)
        if not content:
            return

        # Extract title from HTML title tag
        import re
        title_match = re.search(r'<title>([^<]+)</title>', content)
        title = title_match.group(1) if title_match else os.path.basename(filepath)

        # Extract visible text, excluding script/style tags
        text_match = re.search(r'<[^>]*>([^<]+)</[^>]*>', content, re.DOTALL)
        text = text_match.group(1) if text_match else ""

        # Clean up HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        keywords = self.extract_keywords(text)

        self.index["entries"].append({
            "type": "posts",
            "source": category,
            "title": title,
            "description": text[:200] if len(text) > 200 else text,
            "keywords": keywords,
            "text": text,
            "tags": category,
            "id": os.path.basename(filepath).replace('.html', '')
        })

    def add_all_files(self):
        """Add all documentation files to the index."""
        docs_dir = Path('docs')

        # Load knowledge base
        kb_path = docs_dir / 'knowledge_base.json'
        if kb_path.exists():
            try:
                with open(kb_path, 'r', encoding='utf-8') as f:
                    knowledge_data = json.load(f)
                    for item in knowledge_data.get('entries', []):
                        self.add_knowledge_base_entry(item)
            except Exception as e:
                print(f"Warning: Could not load knowledge base: {e}")

        # Add markdown files
        markdown_files = [
            'log.md',
            'failures.md',
            'projects.md',
            'documentation.md',
            'perception-tools.md',
            'wikipedia_api_as_search_backup.md',
            'running-2026-09-09.md',
            'tool_test_complete.md'
        ]

        for md_file in markdown_files:
            md_path = docs_dir / md_file
            if md_path.exists():
                self.add_markdown_file(md_path)

        # Add HTML files from docs/posts/
        posts_dir = docs_dir / 'posts'
        if posts_dir.exists():
            for html_file in sorted(posts_dir.glob('*.html')):
                self.add_html_file(html_file)

        # Update metadata
        self.index["metadata"]["total_entries"] = len(self.index["entries"])
        self.index["metadata"]["total_words"] = sum(len(e.get("text", "").split()) for e in self.index["entries"])
        self.index["metadata"]["sources"] = list(set(e.get("source", "") for e in self.index["entries"]))

        print(f"Index created with {len(self.index['entries'])} entries from {len(self.index['metadata']['sources'])} sources")

    def save_index(self, output_path):
        """Save the index to a JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)
        print(f"Index saved to {output_path}")

    def search(self, query, max_results=10):
        """Search the index for matching entries."""
        query = query.lower()
        query_words = set(query.split())
        if not query_words:
            return []

        results = []
        for entry in self.index["entries"]:
            entry_text = entry.get("text", "").lower()

            # Score based on keyword matches
            matches = sum(1 for word in query_words if word in entry_text)
            score = matches / len(query_words) if query_words else 0

            # Also check keywords field
            keywords = entry.get("keywords", [])
            keyword_matches = sum(1 for word in query_words if word in keywords)
            keyword_score = keyword_matches / len(query_words) if query_words else 0

            # Combine scores
            final_score = (score + keyword_score) / 2

            if final_score > 0:
                results.append({
                    "entry": entry,
                    "score": final_score,
                    "type": entry.get("type", ""),
                    "source": entry.get("source", ""),
                    "title": entry.get("title", ""),
                    "id": entry.get("id", "")
                })

        # Sort by score and return top results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]


def main():
    """Generate search index from all documentation."""
    index = SearchIndex()
    index.add_all_files()
    index.save_index('docs/search_index.json')
    print("\nSearch index generated successfully!")


if __name__ == "__main__":
    main()
