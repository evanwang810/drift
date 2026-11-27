"""
Enhanced search engine for the knowledge base with faceted search,
autocomplete, and relevance scoring.

Core search backend operational with faceted search, autocomplete, and relevance scoring.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict


class EnhancedSearchEngine:
    """Enhanced search engine with faceted search, autocomplete, and relevance scoring."""

    def __init__(self, search_index_path: Optional[Path] = None):
        """
        Initialize the enhanced search engine.

        Args:
            search_index_path: Path to search index JSON file. If None, uses default path.
        """
        self.search_index_path = search_index_path or Path("docs/search_index.json")
        self.index: Dict[str, Any] = {}
        self.load_index()

    def load_index(self) -> None:
        """Load the search index from disk."""
        if self.search_index_path.exists():
            self.index = json.loads(self.search_index_path.read_text(encoding="utf-8"))
            print(f"Loaded search index with {self.index.get('metadata', {}).get('total_entries', 0)} entries")
        else:
            print(f"Warning: Search index not found at {self.search_index_path}")
            self.index = {
                "metadata": {"total_entries": 0},
                "entries": []
            }

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search the knowledge base with filters and relevance scoring.

        Args:
            query: Search query string
            filters: Optional filters for type, tags, source, date range
            limit: Maximum number of results to return
            min_score: Minimum relevance score threshold

        Returns:
            List of search results sorted by relevance score
        """
        if not self.index.get("entries"):
            return []

        query_lower = query.lower()
        results = []
        query_terms = set(query_lower.split())

        for entry in self.index.get("entries", []):
            # Apply filters
            if filters:
                if "type" in filters and entry.get("type") != filters["type"]:
                    continue
                if "tags" in filters and filters["tags"]:
                    entry_tags = set(entry.get("tags", []))
                    if not entry_tags.intersection(filters["tags"]):
                        continue
                if "source" in filters and entry.get("source") != filters["source"]:
                    continue
                if "date_range" in filters and filters["date_range"]:
                    entry_date = entry.get("created_at", "")
                    start, end = filters["date_range"]
                    if entry_date < start or entry_date > end:
                        continue

            # Calculate relevance score
            text = " ".join([
                entry.get("title", "").lower(),
                entry.get("description", "").lower(),
                entry.get("text", "").lower()
            ])

            # Score based on term matching
            score = 0.0
            matched_terms = []

            for term in query_terms:
                if term in text:
                    # Exact match gets higher score
                    if term == query_lower:
                        score += 3.0
                    # Phrase match gets medium score
                    elif term in text.split():
                        score += 2.0
                    # Partial match gets lower score
                    else:
                        score += 1.0
                    matched_terms.append(term)

            if score >= min_score:
                results.append({
                    "entry": entry,
                    "score": score,
                    "matched_terms": matched_terms
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        # Return top N results with entry data
        return [
            {
                "title": r["entry"].get("title", ""),
                "description": r["entry"].get("description", ""),
                "type": r["entry"].get("type", ""),
                "tags": r["entry"].get("tags", []),
                "source": r["entry"].get("source", ""),
                "score": r["score"],
                "matched_terms": r["matched_terms"],
                "id": r["entry"].get("id", ""),
                "created_at": r["entry"].get("created_at", "")
            }
            for r in results[:limit]
        ]

    def get_facets(
        self,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get available facets for filtering.

        Args:
            filters: Optional active filters to exclude from facet counts

        Returns:
            Dictionary of facet counts
        """
        facets = {
            "types": defaultdict(int),
            "sources": defaultdict(int),
            "tags": defaultdict(int)
        }

        for entry in self.index.get("entries", []):
            if filters:
                # Skip entries that match active filters
                if "type" in filters and entry.get("type") == filters["type"]:
                    continue
                if "source" in filters and entry.get("source") == filters["source"]:
                    continue

            facets["types"][entry.get("type", "unknown")] += 1
            facets["sources"][entry.get("source", "unknown")] += 1
            for tag in entry.get("tags", []):
                facets["tags"][tag] += 1

        # Convert to sorted lists
        return {
            "types": [{"type": k, "count": v} for k, v in sorted(facets["types"].items())],
            "sources": [{"source": k, "count": v} for k, v in sorted(facets["sources"].items())],
            "tags": [{"tag": k, "count": v} for k, v in sorted(facets["tags"].items())]
        }

    def autocomplete(
        self,
        prefix: str,
        max_results: int = 10
    ) -> List[str]:
        """
        Get autocomplete suggestions based on prefix.

        Args:
            prefix: Prefix to match
            max_results: Maximum number of suggestions

        Returns:
            List of matching suggestions
        """
        if not prefix or len(prefix) < 2:
            return []

        prefix_lower = prefix.lower()
        suggestions = set()

        for entry in self.index.get("entries", []):
            title = entry.get("title", "").lower()
            description = entry.get("description", "").lower()

            # Check title match
            if title.startswith(prefix_lower):
                suggestions.add(entry.get("title", ""))

            # Check description match
            if description.startswith(prefix_lower):
                suggestions.add(entry.get("title", ""))

        return sorted(list(suggestions))[:max_results]

    def get_all_tags(self) -> List[str]:
        """Get all unique tags from the knowledge base."""
        tags = set()
        for entry in self.index.get("entries", []):
            for tag in entry.get("tags", []):
                tags.add(tag)
        return sorted(list(tags))

    def get_all_types(self) -> List[str]:
        """Get all unique types from the knowledge base."""
        types = set()
        for entry in self.index.get("entries", []):
            types.add(entry.get("type", "unknown"))
        return sorted(list(types))

    def get_all_sources(self) -> List[str]:
        """Get all unique sources from the knowledge base."""
        sources = set()
        for entry in self.index.get("entries", []):
            sources.add(entry.get("source", "unknown"))
        return sorted(list(sources))

    def get_search_stats(self) -> Dict[str, Any]:
        """Get statistics about the search index."""
        entries = self.index.get("entries", [])
        return {
            "total_entries": len(entries),
            "total_words": self.index.get("metadata", {}).get("total_words", 0),
            "types": list(set(entry.get("type", "unknown") for entry in entries)),
            "sources": list(set(entry.get("source", "unknown") for entry in entries)),
            "tags": list(set(tag for entry in entries for tag in entry.get("tags", [])))
        }


# Create global instance
search_engine = EnhancedSearchEngine()


def load_search_index(path: Optional[Path] = None) -> EnhancedSearchEngine:
    """Load and return a search engine instance."""
    return EnhancedSearchEngine(path)


def search(
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 10,
    min_score: float = 0.0
) -> List[Dict[str, Any]]:
    """Convenience function for search."""
    return search_engine.search(query, filters, limit, min_score)


def get_facets(filters: Optional[Dict[str, Any]] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Convenience function for getting facets."""
    return search_engine.get_facets(filters)


def autocomplete(prefix: str, max_results: int = 10) -> List[str]:
    """Convenience function for autocomplete."""
    return search_engine.autocomplete(prefix, max_results)


if __name__ == "__main__":
    # Test the search engine
    print("Testing Enhanced Search Engine")
    print("=" * 50)

    # Get stats
    stats = search_engine.get_search_stats()
    print(f"\nSearch Index Stats:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Total words: {stats['total_words']}")
    print(f"  Types: {stats['types']}")
    print(f"  Sources: {stats['sources']}")
    print(f"  Tags: {stats['tags']}")

    # Test autocomplete
    print(f"\nAutocomplete examples:")
    for prefix in ["search", "tool", "error", "platform"]:
        suggestions = autocomplete(prefix, 5)
        print(f"  '{prefix}': {suggestions}")

    # Test search
    print(f"\nSearch examples:")
    results = search("search tool", limit=3)
    for r in results:
        print(f"  [{r['score']:.2f}] {r['title']} - {r['description'][:80]}...")

    # Test facets
    print(f"\nFacets:")
    facets = get_facets()
    for facet_name, facet_data in facets.items():
        print(f"  {facet_name}:")
        for item in facet_data[:5]:
            print(f"    {item}")

    print("\nSearch engine test complete!")
