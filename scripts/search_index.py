"""
Search index builder for enhanced search functionality.

This module creates and maintains a search index across:
- Knowledge base entries
- Documentation files
- Blog posts
"""

import json
from pathlib import Path
from datetime import datetime
import re


class SearchIndex:
    """Build and maintain a search index across all content."""

    def __init__(self, knowledge_base_path: Path, docs_path: Path, posts_path: Path):
        self.kb_path = knowledge_base_path
        self.docs_path = docs_path
        self.posts_path = posts_path
        self.index = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'version': '2.0',
                'total_entries': 0
            },
            'knowledge': [],
            'documentation': [],
            'posts': []
        }

    def add_all_files(self):
        """Add all knowledge base, docs, and posts to the index."""
        self._add_knowledge_base()
        self._add_docs()
        self._add_posts()

    def _add_knowledge_base(self):
        """Index knowledge base entries."""
        if not self.kb_path.exists():
            return

        with open(self.kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        entries = data.get('entries', [])

        for entry in entries:
            # Extract searchable text
            searchable_text = (
                f"{entry.get('title', '')} "
                f"{entry.get('content_summary', '')} "
                f"{' '.join(entry.get('entities', []))} "
                f"{' '.join(entry.get('tags', []))}"
            ).lower()

            self.index['knowledge'].append({
                'id': entry.get('id', ''),
                'title': entry.get('title', ''),
                'type': 'knowledge',
                'content': searchable_text,
                'description': entry.get('content_summary', '')[:500],
                'entities': entry.get('entities', []),
                'tags': entry.get('tags', []),
                'created_at': entry.get('extracted_at', ''),
                'source_url': entry.get('source_url', '')
            })

        self.index['metadata']['total_entries'] = len(self.index['knowledge'])

    def _add_docs(self):
        """Index documentation files."""
        if not self.docs_path.exists():
            return

        for md_file in self.docs_path.glob("*.md"):
            if md_file.name.startswith("_"):
                continue

            try:
                content = md_file.read_text(encoding='utf-8')

                # Extract front matter if present
                lines = content.split('\n')
                front_matter = {}
                body = content

                if lines[0].strip() == '---':
                    in_fm = True
                    for line in lines[1:]:
                        if line.strip() == '---':
                            in_fm = False
                            break
                        if ':' in line:
                            key, value = line.split(':', 1)
                            front_matter[key.strip()] = value.strip().strip('"')
                    body = '\n'.join(lines[lines.index('---') + 1:])

                searchable_text = (
                    f"{front_matter.get('title', md_file.stem)} "
                    f"{body}"
                ).lower()

                self.index['documentation'].append({
                    'id': md_file.stem,
                    'title': front_matter.get('title', md_file.stem.replace('-', ' ').title()),
                    'type': 'documentation',
                    'content': searchable_text,
                    'description': body[:500],
                    'created_at': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
                    'path': str(md_file.relative_to(md_file.parent.parent.parent)),
                    'filename': md_file.name
                })

            except Exception as e:
                print(f"Warning: Could not index {md_file}: {e}")

        self.index['metadata']['total_entries'] += len(self.index['documentation'])

    def _add_posts(self):
        """Index blog posts."""
        if not self.posts_path.exists():
            return

        for md_file in self.posts_path.glob("*.md"):
            if md_file.name.startswith("_"):
                continue

            try:
                content = md_file.read_text(encoding='utf-8')

                # Extract front matter
                lines = content.split('\n')
                front_matter = {}
                body = content

                if lines[0].strip() == '---':
                    in_fm = True
                    for line in lines[1:]:
                        if line.strip() == '---':
                            in_fm = False
                            break
                        if ':' in line:
                            key, value = line.split(':', 1)
                            front_matter[key.strip()] = value.strip().strip('"')
                    body = '\n'.join(lines[lines.index('---') + 1:])

                title = front_matter.get('title', md_file.stem.replace('-', ' ').title())
                date = front_matter.get('date', md_file.stem[:10])
                excerpt = front_matter.get('excerpt', body[:200])

                searchable_text = (
                    f"{title} "
                    f"{excerpt} "
                    f"{body}"
                ).lower()

                self.index['posts'].append({
                    'id': md_file.stem,
                    'title': title,
                    'type': 'posts',
                    'content': searchable_text,
                    'description': body[:500],
                    'created_at': date,
                    'slug': md_file.stem,
                    'excerpt': excerpt
                })

            except Exception as e:
                print(f"Warning: Could not index {md_file}: {e}")

        self.index['metadata']['total_entries'] += len(self.index['posts'])

    def search(self, query: str, max_results: int = 20) -> list:
        """Search the index.

        Args:
            query: Search query string
            max_results: Maximum number of results

        Returns:
            List of search results with scores and metadata
        """
        if not query or not query.strip():
            return []

        query_lower = query.lower()
        query_terms = re.findall(r'\b\w{3,}\b', query_lower)

        results = []

        # Search across all types
        for entry in self.index['knowledge'] + self.index['documentation'] + self.index['posts']:
            searchable_text = entry.get('content', '')

            # Calculate relevance score
            score = 0.0

            # Exact match on title
            title = entry.get('title', '').lower()
            if query in title:
                score += 10

            # Match query terms
            term_matches = 0
            for term in query_terms:
                if term in searchable_text:
                    term_matches += 1

            score += term_matches * 3

            # Positional matching
            first_pos = searchable_text.find(query_lower)
            if first_pos != -1:
                score += 2 / (first_pos + 1)

            # Check tags
            if entry.get('tags'):
                tags_lower = [tag.lower() for tag in entry['tags']]
                for term in query_terms:
                    if any(term in tag for tag in tags_lower):
                        score += 2

            # Normalize score
            max_possible = 10 + (len(query_terms) * 3) + 2 + (len(query_terms) * 2)
            normalized_score = min(100, (score / max_possible) * 100) if max_possible > 0 else 0

            if normalized_score > 0:
                results.append({
                    **entry,
                    'score': normalized_score
                })

        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)

        return results[:max_results]

    def save_index(self, output_path: Path):
        """Save the index to a JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

        print(f"Search index saved to {output_path}")
        print(f"Total entries indexed: {self.index['metadata']['total_entries']}")
        print(f"  - Knowledge entries: {len(self.index['knowledge'])}")
        print(f"  - Documentation: {len(self.index['documentation'])}")
        print(f"  - Posts: {len(self.index['posts'])}")


def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(description='Build search index.')
    parser.add_argument('--output', type=str, default='docs/search_index.json', help='Output path')

    args = parser.parse_args()

    ROOT = Path(__file__).resolve().parent.parent
    index = SearchIndex(
        ROOT / "scripts" / "knowledge_base.json",
        ROOT / "docs",
        ROOT / "docs" / "_posts"
    )

    index.add_all_files()
    index.save_index(Path(args.output))


if __name__ == '__main__':
    main()
