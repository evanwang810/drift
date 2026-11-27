"""
Search result visualization for the knowledge base.

Provides visual representations of search results including:
- Related tags and categories
- Result summaries with scores
- Date-based grouping
- Type distribution charts
"""

from typing import List, Dict, Any
from datetime import datetime
import json


class SearchVisualization:
    """Generate visualizations for search results."""

    def __init__(self):
        pass

    def create_result_summary(self, results: List[Dict[str, Any]]) -> str:
        """Create a visual summary of search results."""
        if not results:
            return "<div class='search-visualization'><h3>No Results Found</h3></div>"

        output = f"""
        <div class='search-visualization'>
            <div class='search-header'>
                <h3>Search Results</h3>
                <span class='result-count'>{len(results)} result(s)</span>
            </div>
            <div class='results-list'>
        """

        for i, result in enumerate(results[:10], 1):
            title = result.get('title', 'Untitled')
            entry_type = result.get('type', 'other')
            score = result.get('score', 0)
            date = result.get('created_at', 'N/A')
            description = result.get('description', '')[:150]

            output += f"""
            <div class='result-item' style='border-left: 4px solid hsl({score}, 70%, 50%); margin-bottom: 10px; padding-left: 10px;'>
                <div class='result-header'>
                    <span class='result-title'>{title}</span>
                    <span class='result-score' style='background: hsl({score}, 70%, 50%);'>{score}% relevance</span>
                </div>
                <div class='result-meta'>
                    <span class='result-type'>{entry_type}</span>
                    <span class='result-date'>{date}</span>
                </div>
                <div class='result-description'>{description}...</div>
            </div>
            """

        if len(results) > 10:
            output += f"""
            <div class='more-results'>
                ...and {len(results) - 10} more results
            </div>
            """

        output += """
            </div>
        </div>
        """

        return output

    def create_facet_viz(self, facets: Dict[str, Any], query: str = None) -> str:
        """Create visual representation of facets."""
        output = '<div class="facet-viz">'

        # Type distribution
        if facets.get('types'):
            output += self._create_bar_chart('By Type', facets['types'])

        # Tag cloud
        if facets.get('tags'):
            output += self._create_tag_cloud(facets['tags'])

        # Date distribution
        if facets.get('date_ranges'):
            output += self._create_date_distribution(facets['date_ranges'])

        output += '</div>'
        return output

    def _create_bar_chart(self, title: str, data: Dict[str, int]) -> str:
        """Create a simple bar chart visualization."""
        max_count = max(data.values()) if data else 1

        output = f"""
        <div class="bar-chart">
            <h4>{title}</h4>
        """

        for label, count in sorted(data.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / max_count) * 100
            output += f"""
            <div class="bar-row">
                <span class="bar-label">{label}</span>
                <div class="bar-container">
                    <div class="bar-fill" style="width: {percentage}%"></div>
                </div>
                <span class="bar-value">{count}</span>
            </div>
            """

        output += '</div>'
        return output

    def _create_tag_cloud(self, tags: Dict[str, int]) -> str:
        """Create a tag cloud visualization."""
        output = '<div class="tag-cloud">'
        output += '<h4>Popular Tags</h4>'
        output += '<div class="tags">'

        for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:15]:
            size = min(20, 8 + (count * 0.5))
            output += f"""
            <span class="tag" style="font-size: {size}px; background: hsl(210, 60%, 45%); color: white; padding: 4px 8px; margin: 2px; border-radius: 4px;">
                {tag} ({count})
            </span>
            """

        output += '</div></div>'
        return output

    def _create_date_distribution(self, data: Dict[str, int]) -> str:
        """Create a date range distribution visualization."""
        output = '<div class="date-distribution">'
        output += '<h4>Date Distribution</h4>'

        for range_name, count in data.items():
            percentage = (count / sum(data.values())) * 100 if data.values() else 0
            color_map = {
                'this_week': '#4CAF50',
                'this_month': '#2196F3',
                'this_year': '#FF9800',
                'older': '#9E9E9E'
            }

            output += f"""
            <div class="date-item">
                <span class="date-label">{range_name}</span>
                <div class="date-bar-container">
                    <div class="date-bar-fill" style="width: {percentage}%; background: {color_map.get(range_name, '#666')}"></div>
                </div>
                <span class="date-value">{count}</span>
            </div>
            """

        output += '</div>'
        return output

    def create_suggestion_viz(self, suggestions: List[str]) -> str:
        """Create visualization for query suggestions."""
        if not suggestions:
            return '<div class="suggestion-viz"><p>No suggestions available.</p></div>'

        output = '<div class="suggestion-viz">'
        output += '<h4>Query Suggestions</h4>'
        output += '<ul class="suggestion-list">'

        for i, suggestion in enumerate(suggestions, 1):
            output += f"""
            <li class="suggestion-item">
                <span class="suggestion-number">{i}.</span>
                <span class="suggestion-text">{suggestion}</span>
            </li>
            """

        output += '</ul></div>'
        return output

    def create_dashboard(self, results: List[Dict[str, Any]], facets: Dict[str, Any], suggestions: List[str] = None) -> str:
        """Create a complete search dashboard visualization."""
        output = '<div class="search-dashboard">'

        # Main results
        output += self.create_result_summary(results)

        # Facets
        if facets:
            output += self.create_facet_viz(facets)

        # Suggestions
        if suggestions:
            output += self.create_suggestion_viz(suggestions)

        output += '</div>'
        return output

    def generate_json_summary(self, results: List[Dict[str, Any]]) -> str:
        """Generate JSON summary of search results for API use."""
        summary = {
            'total_results': len(results),
            'results': [
                {
                    'title': r.get('title'),
                    'type': r.get('type'),
                    'score': r.get('score'),
                    'created_at': r.get('created_at'),
                    'description': r.get('description')
                }
                for r in results[:10]
            ]
        }
        return json.dumps(summary, indent=2)

    def get_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics about search results."""
        if not results:
            return {
                'total': 0,
                'by_type': {},
                'avg_score': 0,
                'date_range': None
            }

        # Count by type
        by_type = {}
        for r in results:
            entry_type = r.get('type', 'other')
            by_type[entry_type] = by_type.get(entry_type, 0) + 1

        # Average score
        scores = [r.get('score', 0) for r in results]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Date range
        dates = [r.get('created_at') for r in results if r.get('created_at')]
        if dates:
            try:
                date_range = {
                    'earliest': min(dates),
                    'latest': max(dates)
                }
            except (ValueError, TypeError):
                date_range = None
        else:
            date_range = None

        return {
            'total': len(results),
            'by_type': by_type,
            'avg_score': round(avg_score, 2),
            'date_range': date_range
        }


def main():
    """Test the visualization module."""
    from enhanced_search import EnhancedSearchEngine

    ROOT = Path(__file__).resolve().parent.parent
    engine = EnhancedSearchEngine(
        ROOT / "scripts" / "knowledge_base.json",
        ROOT / "docs",
        ROOT / "docs" / "_posts"
    )

    viz = SearchVisualization()

    # Test search
    results = engine.search("Python", max_results=20)

    # Generate dashboard
    print("=== Search Dashboard ===")
    print(viz.create_dashboard(results, engine.get_facets()))

    # Generate JSON summary
    print("\n=== JSON Summary ===")
    print(viz.generate_json_summary(results))

    # Get statistics
    stats = viz.get_stats(results)
    print("\n=== Statistics ===")
    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()
