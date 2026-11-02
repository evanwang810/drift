"""
Analytics tracking module for the repository website.
Tracks page views, search queries, and user engagement metrics.
"""

import json
import os
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path


class AnalyticsTracker:
    """Track user behavior and engagement metrics."""

    def __init__(self, data_dir="docs"):
        self.data_dir = Path(data_dir)
        self.analytics_file = self.data_dir / "analytics.json"
        self.data = self._load_data()

    def _load_data(self):
        """Load existing analytics data or create empty structure."""
        if self.analytics_file.exists():
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        return {
            "page_views": [],
            "search_queries": [],
            "page_visits": defaultdict(lambda: {"total_views": 0, "unique_visitors": set(), "last_visit": None}),
            "page_views_by_day": defaultdict(lambda: 0),
            "total_visitors": 0,
            "first_visit": None,
            "engagement": {
                "avg_time_on_page": 0,
                "bounce_rate": 0,
                "return_visitors": 0
            }
        }

    def _save_data(self):
        """Save analytics data to file."""
        with open(self.analytics_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_page_view(self, page_path, user_id=None):
        """Record a page view event."""
        if self.data["first_visit"] is None:
            self.data["first_visit"] = datetime.now().isoformat()

        today = datetime.now().strftime("%Y-%m-%d")
        self.data["page_views_by_day"][today] += 1

        visitor_data = self.data["page_visits"][page_path]
        visitor_data["total_views"] += 1

        if user_id and user_id not in visitor_data["unique_visitors"]:
            visitor_data["unique_visitors"].add(user_id)

        visitor_data["last_visit"] = datetime.now().isoformat()

        self.data["page_views"].append({
            "page": page_path,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id
        })

        self.data["total_visitors"] = len(self.data["page_visits"][page_path]["unique_visitors"])
        self._save_data()

    def record_search_query(self, query, filters=None):
        """Record a search query event."""
        self.data["search_queries"].append({
            "query": query,
            "filters": filters or {},
            "timestamp": datetime.now().isoformat()
        })
        self._save_data()

    def get_page_views(self, page_path=None):
        """Get page view statistics."""
        if page_path:
            return self.data["page_visits"].get(page_path, {})
        return self.data["page_visits"]

    def get_search_stats(self):
        """Get search query statistics."""
        queries = [q["query"] for q in self.data["search_queries"]]
        top_queries = Counter(queries).most_common(10)
        return {
            "total_queries": len(self.data["search_queries"]),
            "top_queries": [{"query": q, "count": c} for q, c in top_queries],
            "unique_queries": len(set(queries))
        }

    def get_daily_stats(self):
        """Get daily page view statistics."""
        return dict(self.data["page_views_by_day"])

    def get_overall_stats(self):
        """Get overall analytics statistics."""
        return {
            "total_page_views": len(self.data["page_views"]),
            "total_visitors": self.data["total_visitors"],
            "first_visit": self.data["first_visit"],
            "current_visitors": sum(len(v["unique_visitors"]) for v in self.data["page_visits"].values())
        }

    def generate_summary(self):
        """Generate a text summary of analytics."""
        summary = []
        summary.append("=== ANALYTICS SUMMARY ===\n")

        overall = self.get_overall_stats()
        summary.append(f"Total Page Views: {overall['total_page_views']}")
        summary.append(f"Unique Visitors: {overall['total_visitors']}")
        summary.append(f"Current Visitors: {overall['current_visitors']}")
        summary.append(f"First Visit: {overall['first_visit']}")

        search_stats = self.get_search_stats()
        summary.append(f"\nSearch Queries: {search_stats['total_queries']}")
        summary.append(f"Unique Queries: {search_stats['unique_queries']}")
        summary.append("\nTop Search Queries:")
        for item in search_stats['top_queries']:
            summary.append(f"  - '{item['query']}': {item['count']} times")

        return "\n".join(summary)


def main():
    """Run analytics tracking demo."""
    tracker = AnalyticsTracker()

    # Record some sample page views
    print("Recording page views...")
    tracker.record_page_view("/index.html", user_id="user1")
    tracker.record_page_view("/knowledge-base.html", user_id="user1")
    tracker.record_page_view("/knowledge-base.html", user_id="user2")
    tracker.record_page_view("/blog/2026-10-01-first-post.html", user_id="user1")
    tracker.record_page_view("/metrics.html", user_id="user3")
    tracker.record_page_view("/index.html", user_id="user1")

    # Record some search queries
    print("\nRecording search queries...")
    tracker.record_search_query("tools", {"type": "tool_fix"})
    tracker.record_search_query("knowledge base", {"category": "discovery"})
    tracker.record_search_query("analytics")
    tracker.record_search_query("knowledge base", {"category": "discovery"})
    tracker.record_search_query("github")

    # Display summaries
    print("\n" + tracker.generate_summary())

    print("\nAnalytics data saved to docs/analytics.json")


if __name__ == "__main__":
    main()
