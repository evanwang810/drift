"""
Search result visualization for the knowledge base query interface.

Visualizes search results with tags, categories, relevance scores, and related items.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path


class SearchVisualizer:
    """Visualizer for search results with various display formats."""

    def __init__(self, search_index_path: Optional[Path] = None):
        """
        Initialize the search visualizer.

        Args:
            search_index_path: Path to search index JSON file
        """
        self.search_index_path = search_index_path or Path("docs/search_index.json")
        self.index = {}
        if self.search_index_path.exists():
            self.index = json.loads(self.search_index_path.read_text(encoding="utf-8"))

    def visualize_results(
        self,
        results: List[Dict[str, Any]],
        query: str,
        show_scores: bool = True,
        show_tags: bool = True,
        max_length: int = 500
    ) -> str:
        """
        Visualize search results as HTML.

        Args:
            results: List of search result dictionaries
            query: Original search query
            show_scores: Whether to show relevance scores
            show_tags: Whether to show tags
            max_length: Maximum description length

        Returns:
            HTML string visualization
        """
        if not results:
            return f"<div class='search-results'>No results found for '{query}'</div>"

        html_parts = [f"<div class='search-results'>"]
        html_parts.append(f"<h2>Results for '{query}' ({len(results)} found)</h2>")

        for i, result in enumerate(results, 1):
            entry = result["entry"]

            html_parts.append("<div class='result-item'>")

            # Header with score and title
            header_parts = [f"<div class='result-header'>"]
            if show_scores:
                score_color = self._get_score_color(result["score"])
                header_parts.append(f"<span class='score {score_color}'>{result['score']:.2f} pts</span>")
            header_parts.append(f"<h3 class='result-title'>{self._escape_html(entry.get('title', ''))}</h3>")
            header_parts.append("</div>")

            # Description
            description = entry.get("description", "")
            if len(description) > max_length:
                description = description[:max_length] + "..."
            html_parts.append(f"<p class='result-description'>{self._escape_html(description)}</p>")

            # Tags
            if show_tags and entry.get("tags"):
                html_parts.append("<div class='result-tags'>")
                for tag in entry.get("tags", [])[:5]:  # Show max 5 tags
                    html_parts.append(f"<span class='tag'>{self._escape_html(tag)}</span>")
                html_parts.append("</div>")

            # Metadata
            meta_parts = ["<div class='result-meta'>"]
            meta_parts.append(f"<span class='type'>{entry.get('type', 'unknown')}</span>")
            meta_parts.append(f"<span class='source'>{entry.get('source', 'unknown')}</span>")
            if entry.get("created_at"):
                meta_parts.append(f"<span class='date'>{entry.get('created_at')}</span>")
            meta_parts.append("</div>")

            html_parts.append("".join(header_parts))
            html_parts.append("".join(meta_parts))
            html_parts.append("</div>")

        html_parts.append("</div>")
        return "".join(html_parts)

    def visualize_tags_cloud(self, tags: List[str], max_size: int = 5) -> str:
        """
        Visualize tags as a tag cloud.

        Args:
            tags: List of tags
            max_size: Maximum font size in em

        Returns:
            HTML tag cloud
        """
        if not tags:
            return "<div class='tag-cloud'>No tags available</div>"

        # Count tag frequencies
        tag_counts = {}
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Calculate font sizes
        max_count = max(tag_counts.values()) if tag_counts else 1
        min_count = min(tag_counts.values()) if tag_counts else 1

        html_parts = ["<div class='tag-cloud'>"]
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
            size = max_size * (count / max_count)
            html_parts.append(
                f"<a href='#' class='tag-link' style='font-size: {size:.1f}em;' "
                f"data-tag='{self._escape_html(tag)}'>{self._escape_html(tag)}</a> "
            )
        html_parts.append("</div>")

        return "".join(html_parts)

    def visualize_facets(self, facets: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Visualize search facets.

        Args:
            facets: Facet data from search engine

        Returns:
            HTML facet visualization
        """
        html_parts = ["<div class='facets'>"]

        for facet_name, facet_items in facets.items():
            if not facet_items:
                continue

            html_parts.append(f"<div class='facet-group'>")
            html_parts.append(f"<h4 class='facet-title'>{facet_name.capitalize()}</h4>")

            for item in facet_items[:10]:  # Show max 10 items per facet
                count = item.get("count", 0)
                label = item.get(facet_name[:-1], item.get("type", ""))  # Remove 's' from 'types'
                html_parts.append(
                    f"<div class='facet-item'>"
                    f"<span class='facet-count'>{count}</span>"
                    f"<span class='facet-label'>{label}</span>"
                    f"</div>"
                )

            html_parts.append("</div>")

        html_parts.append("</div>")
        return "".join(html_parts)

    def get_relevance_color(self, score: float) -> str:
        """
        Get color based on relevance score.

        Args:
            score: Relevance score

        Returns:
            CSS color class
        """
        if score >= 5.0:
            return "high"
        elif score >= 3.0:
            return "medium"
        elif score >= 1.0:
            return "low"
        else:
            return "none"

    def _get_score_color(self, score: float) -> str:
        """Get CSS class for score display."""
        if score >= 5.0:
            return "score-high"
        elif score >= 3.0:
            return "score-medium"
        elif score >= 1.0:
            return "score-low"
        else:
            return "score-none"

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        if not text:
            return ""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def format_summary(
        self,
        results: List[Dict[str, Any]],
        query: str,
        show_scores: bool = True
    ) -> str:
        """
        Get a text summary of search results.

        Args:
            results: Search results
            query: Original query
            show_scores: Whether to include scores

        Returns:
            Text summary
        """
        if not results:
            return f"No results found for '{query}'"

        summary = f"Search results for '{query}' ({len(results)} found):\n"

        for i, result in enumerate(results, 1):
            title = result.get("title", "Untitled")
            score = result.get("score", 0)
            description = result.get("description", "")

            summary += f"\n{i}. [{score:.2f}] {title}"
            if description:
                summary += f"\n   {description[:150]}..."

        return summary

    def export_to_json(self, results: List[Dict[str, Any]]) -> str:
        """
        Export results as JSON.

        Args:
            results: Search results

        Returns:
            JSON string
        """
        return json.dumps(results, indent=2, ensure_ascii=False)


# Global instance
visualizer = SearchVisualizer()


if __name__ == "__main__":
    # Test visualization
    print("Testing Search Visualizer")
    print("=" * 50)

    viz = SearchVisualizer()

    # Test sample results
    sample_results = [
        {
            "entry": {
                "title": "Search Tool Wikipedia API Fallback",
                "description": "The search tool was never actually working - it never returned any results despite code that claimed to search DuckDuckGo.",
                "type": "tool_fix",
                "tags": ["search", "wikipedia", "duckduckgo"],
                "source": "Run 126",
                "created_at": "2026-09-13"
            },
            "score": 4.5,
            "matched_terms": ["search", "tool"]
        },
        {
            "entry": {
                "title": "GLM-5.3-Flash Platform Details",
                "description": "Discovered the platform running this agent is GLM-5.3-Flash (not GLM-4.7-Flash as previously assumed).",
                "type": "platform",
                "tags": ["platform", "glm", "llm"],
                "source": "Run 79-82",
                "created_at": "2026-10-01"
            },
            "score": 3.0,
            "matched_terms": ["platform"]
        }
    ]

    # Test HTML visualization
    html_viz = viz.visualize_results(sample_results, "search tool")
    print("\nHTML Visualization:")
    print(html_viz[:500] + "...")

    # Test text summary
    summary = viz.format_summary(sample_results, "search tool")
    print("\nText Summary:")
    print(summary)

    # Test tags cloud
    tags = ["search", "wikipedia", "duckduckgo", "api", "tool", "platform", "glm"]
    tag_cloud = viz.visualize_tags_cloud(tags)
    print("\nTag Cloud:")
    print(tag_cloud[:300] + "...")

    print("\nVisualizer test complete!")
