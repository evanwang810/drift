"""
Enhanced search interface for the knowledge base and documentation.

Provides advanced search functionality with:
- Multi-field search across knowledge base entries, docs, and posts
- Filters by type (knowledge, documentation, posts)
- Tag-based filtering
- Date range filtering
- Relevance scoring
- Query suggestions and autocomplete
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class EnhancedSearchEngine:
    """Advanced search engine with filtering and relevance scoring."""

    def __init__(self, knowledge_base_path: Path, docs_path: Path, posts_path: Path):
        self.kb_path = knowledge_base_path
        self.docs_path = docs_path
        self.posts_path = posts_path
        self.knowledge_base = self._load_knowledge_base()
        self.docs = self._load_docs()
        self.posts = self._load_posts()

    def _load_knowledge_base(self) -> List[Dict[str, Any]]:
        """Load knowledge base entries."""
        if not self.kb_path.exists():
            return []

        with open(self.kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data.get('entries', [])

    def _load_docs(self) -> List[Dict[str, Any]]:
        """Load documentation files."""
        docs = []
        if not self.docs_path.exists():
            return docs

        for md_file in self.docs_path.glob("*.md"):
            if md_file.name.startswith("_"):
                continue
            try:
                content = md_file.read_text(encoding='utf-8')
                title = md_file.stem.replace('-', ' ').replace('_', ' ').title()
                docs.append({
                    'type': 'documentation',
                    'id': md_file.stem,
                    'title': title,
                    'path': str(md_file),
                    'content': content,
                    'description': content[:500],
                    'created_at': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
                })
            except Exception as e:
                print(f"Warning: Could not load {md_file}: {e}")

        return docs

    def _load_posts(self) -> List[Dict[str, Any]]:
        """Load blog posts."""
        posts = []
        if not self.posts_path.exists():
            return posts

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

                posts.append({
                    'type': 'posts',
                    'id': md_file.stem,
                    'title': title,
                    'path': str(md_file),
                    'content': body,
                    'description': body[:500],
                    'created_at': date,
                    'slug': md_file.stem
                })
            except Exception as e:
                print(f"Warning: Could not load {md_file}: {e}")

        return posts

    def search(
        self,
        query: str,
        max_results: int = 20,
        filter_type: Optional[str] = None,
        filter_tags: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort_by: str = 'relevance'
    ) -> List[Dict[str, Any]]:
        """
        Search across knowledge base, docs, and posts.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            filter_type: Filter by type (knowledge, documentation, posts)
            filter_tags: Filter by tags (list of tags)
            start_date: Filter by start date (YYYY-MM-DD)
            end_date: Filter by end date (YYYY-MM-DD)
            sort_by: Sort by relevance, date, or title

        Returns:
            List of search results with scores and metadata
        """
        if not query or not query.strip():
            return []

        # Combine all content
        all_entries = []

        # Add knowledge base entries
        for entry in self.knowledge_base:
            all_entries.append({
                **entry,
                'type': 'knowledge',
                'searchable_text': f"{entry.get('title', '')} {entry.get('content_summary', '')} {' '.join(entry.get('entities', []))}".lower()
            })

        # Add documentation
        for doc in self.docs:
            all_entries.append({
                **doc,
                'searchable_text': f"{doc['title']} {doc['description']}".lower()
            })

        # Add posts
        for post in self.posts:
            all_entries.append({
                **post,
                'searchable_text': f"{post['title']} {post.get('excerpt', '')}".lower()
            })

        # Apply filters
        filtered_entries = self._apply_filters(all_entries, filter_type, filter_tags, start_date, end_date)

        # Calculate relevance scores
        scored_results = self._calculate_relevance(filtered_entries, query)

        # Sort results
        scored_results.sort(
            key=lambda x: (
                x['score'] if sort_by == 'relevance' else (
                    x.get('created_at', '') if sort_by == 'date' else x.get('title', '').lower()
                )
            ),
            reverse=sort_by in ['relevance', 'date']
        )

        # Return top results with entry metadata
        return scored_results[:max_results]

    def _apply_filters(
        self,
        entries: List[Dict[str, Any]],
        filter_type: Optional[str],
        filter_tags: Optional[List[str]],
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Apply filters to search results."""
        filtered = entries

        if filter_type:
            filtered = [e for e in filtered if e.get('type') == filter_type]

        if filter_tags:
            filtered = [
                e for e in filtered
                if e.get('tags') and any(tag in e.get('tags', []) for tag in filter_tags)
            ]

        if start_date:
            filtered = [
                e for e in filtered
                if e.get('created_at') and e['created_at'] >= start_date
            ]

        if end_date:
            filtered = [
                e for e in filtered
                if e.get('created_at') and e['created_at'] <= end_date
            ]

        return filtered

    def _calculate_relevance(self, entries: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Calculate relevance scores for entries."""
        query_lower = query.lower()
        query_terms = re.findall(r'\b\w{3,}\b', query_lower)

        scored_results = []

        for entry in entries:
            # Get searchable text
            searchable_text = entry.get('searchable_text', '')

            # Calculate base score
            score = 0.0

            # Exact match on title
            title = entry.get('title', '').lower()
            if query in title:
                score += 10

            # Match query terms in searchable text
            term_matches = 0
            for term in query_terms:
                if term in searchable_text:
                    term_matches += 1

            score += term_matches * 3

            # Positional matching (first occurrence)
            first_pos = searchable_text.find(query_lower)
            if first_pos != -1:
                score += 2 / (first_pos + 1)

            # Check tags for partial matches
            if entry.get('tags'):
                tags_lower = [tag.lower() for tag in entry['tags']]
                for term in query_terms:
                    if any(term in tag for tag in tags_lower):
                        score += 2

            # Bonus for exact entity matches in knowledge base
            if entry.get('type') == 'knowledge' and entry.get('entities'):
                entities_lower = [e.lower() for e in entry['entities']]
                for term in query_terms:
                    if any(term in entity for entity in entities_lower):
                        score += 3

            # Normalize score (0-100 range)
            max_possible = 10 + (len(query_terms) * 3) + 2 + (len(query_terms) * 2) + 3
            normalized_score = min(100, (score / max_possible) * 100) if max_possible > 0 else 0

            if normalized_score > 0:
                scored_results.append({
                    **entry,
                    'score': normalized_score,
                    'query': query
                })

        return scored_results

    def get_suggestions(self, query: str, max_suggestions: int = 10) -> List[str]:
        """Get query suggestions based on common searches and tags."""
        if not query or not query.strip():
            return []

        suggestions = set()

        # Extract terms from query
        query_terms = re.findall(r'\b\w{3,}\b', query.lower())

        # Add related terms from knowledge base
        for entry in self.knowledge_base[:100]:
            title = entry.get('title', '').lower()
            entities = entry.get('entities', [])

            # Add entities that contain query terms
            for term in query_terms:
                for entity in entities:
                    if term in entity.lower() and len(entity) > 5:
                        suggestions.add(entity)

        # Add common search terms from knowledge base tags
        all_tags = set()
        for entry in self.knowledge_base:
            all_tags.update(entry.get('tags', []))

        for tag in all_tags:
            if any(term in tag.lower() for term in query_terms):
                suggestions.add(tag)

        return sorted(list(suggestions))[:max_suggestions]

    def get_facets(self, query: Optional[str] = None) -> Dict[str, Any]:
        """Get facet counts for filtering."""
        # Combine all content
        all_entries = []
        all_entries.extend(self.knowledge_base)
        all_entries.extend(self.docs)
        all_entries.extend(self.posts)

        # Filter if query provided
        if query:
            all_entries = self._apply_filters(all_entries, None, None, None, None)

        # Count by type
        type_counts = {}
        for entry in all_entries:
            entry_type = entry.get('type', 'other')
            type_counts[entry_type] = type_counts.get(entry_type, 0) + 1

        # Count by tags (knowledge base only)
        tag_counts = {}
        for entry in all_entries:
            if entry.get('type') == 'knowledge' and entry.get('tags'):
                for tag in entry['tags']:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Count by date range
        date_counts = {
            'this_week': 0,
            'this_month': 0,
            'this_year': 0,
            'older': 0
        }

        today = datetime.now()

        for entry in all_entries:
            if entry.get('created_at'):
                # Fix: created_at may be in '2026-09-12 13:07:00 UTC' format, not ISO format
                created_date = datetime.strptime(entry['created_at'], '%Y-%m-%d %H:%M:%S %Z')

                if (today - created_date).days < 7:
                    date_counts['this_week'] += 1
                elif (today - created_date).days < 30:
                    date_counts['this_month'] += 1
                elif (today - created_date).days < 365:
                    date_counts['this_year'] += 1
                else:
                    date_counts['older'] += 1

        return {
            'types': type_counts,
            'tags': dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]),
            'date_ranges': date_counts
        }

    def generate_summary(self, results: List[Dict[str, Any]]) -> str:
        """Generate a human-readable summary of search results."""
        if not results:
            return "No results found."

        summary = f"<h2>Search Results</h2><p>{len(results)} result(s) found for '{results[0].get('query', '')}'</p>"
        summary += "<ul>"

        for result in results[:5]:
            title = result.get('title', 'Untitled')
            type_label = result.get('type', 'other')
            score = result.get('score', 0)
            date = result.get('created_at', 'N/A')

            summary += f"""
            <li>
              <strong>{title}</strong> ({type_label}, {score}% relevance)
              <small>{date}</small>
            </li>
            """

        if len(results) > 5:
            summary += f"<li>...and {len(results) - 5} more results</li>"

        summary += "</ul>"
        return summary


def main():
    """Command-line interface for enhanced search."""
    import argparse

    parser = argparse.ArgumentParser(description='Enhanced search for knowledge base and documentation.')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--max-results', type=int, default=20, help='Maximum number of results')
    parser.add_argument('--type', help='Filter by type (knowledge, documentation, posts)')
    parser.add_argument('--tags', nargs='+', help='Filter by tags')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--sort', choices=['relevance', 'date', 'title'], default='relevance', help='Sort by field')
    parser.add_argument('--suggestions', action='store_true', help='Show query suggestions')
    parser.add_argument('--facets', action='store_true', help='Show available facets')
    parser.add_argument('--summary', action='store_true', help='Generate summary')

    args = parser.parse_args()

    ROOT = Path(__file__).resolve().parent.parent
    engine = EnhancedSearchEngine(
        ROOT / "scripts" / "knowledge_base.json",
        ROOT / "docs",
        ROOT / "docs" / "_posts"
    )

    if args.suggestions:
        suggestions = engine.get_suggestions(args.query)
        print(f"Query suggestions for '{args.query}':")
        for suggestion in suggestions:
            print(f"  - {suggestion}")
        return

    if args.facets:
        facets = engine.get_facets(args.query)
        print("\nFacet Counts:")
        print("\nBy Type:")
        for type_name, count in facets['types'].items():
            print(f"  {type_name}: {count}")

        print("\nBy Tags:")
        for tag, count in facets['tags'].items():
            print(f"  {tag}: {count}")

        print("\nBy Date Range:")
        for range_name, count in facets['date_ranges'].items():
            print(f"  {range_name}: {count}")
        return

    results = engine.search(
        query=args.query,
        max_results=args.max_results,
        filter_type=args.type,
        filter_tags=args.tags,
        start_date=args.start_date,
        end_date=args.end_date,
        sort_by=args.sort
    )

    if args.summary:
        print(engine.generate_summary(results))
    else:
        print(f"\nSearch Results for '{args.query}':\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('title', 'Untitled')} ({result.get('type', 'other')})")
            print(f"   Score: {result.get('score', 0):.1f}%")
            if result.get('description'):
                print(f"   Description: {result['description'][:100]}...")
            print()


if __name__ == '__main__':
    main()
