"""
Analytics dashboard generator for the repository website.
Creates visualizations of user behavior and engagement metrics.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import math


class AnalyticsDashboardGenerator:
    """Generate analytics dashboard HTML page."""

    def __init__(self, data_file="docs/analytics.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()

    def _load_data(self):
        """Load analytics data from JSON file."""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {
            "page_views": [],
            "search_queries": [],
            "page_visits": {},
            "page_views_by_day": {},
            "total_visitors": 0,
            "first_visit": None
        }

    def _get_page_views(self, page_path=None):
        """Get page view statistics."""
        if page_path:
            return self.data["page_visits"].get(page_path, {
                "total_views": 0,
                "unique_visitors": set(),
                "last_visit": None
            })
        return self.data["page_visits"]

    def _get_top_pages(self, limit=10):
        """Get the most visited pages."""
        page_stats = [
            (path, data["total_views"], len(data["unique_visitors"]))
            for path, data in self.data["page_visits"].items()
        ]
        page_stats.sort(key=lambda x: x[1], reverse=True)
        return page_stats[:limit]

    def _get_search_stats(self):
        """Get search query statistics."""
        queries = [q["query"] for q in self.data["search_queries"]]
        top_queries = Counter(queries).most_common(10)
        return {
            "total_queries": len(self.data["search_queries"]),
            "top_queries": [{"query": q, "count": c} for q, c in top_queries],
            "unique_queries": len(set(queries))
        }

    def _get_daily_stats(self, days=30):
        """Get daily page view statistics for the last N days."""
        today = datetime.now()
        daily_stats = []

        for i in range(days):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            views = self.data["page_views_by_day"].get(date, 0)
            daily_stats.append({"date": date, "views": views})

        return daily_stats

    def _get_engagement_metrics(self):
        """Calculate engagement metrics."""
        total_views = len(self.data["page_views"])
        total_visitors = self.data["total_visitors"]

        # Calculate bounce rate (simplified - pages per visit ratio)
        avg_views_per_visitor = total_views / total_visitors if total_visitors > 0 else 0
        bounce_rate = min(1.0, (total_visitors / total_views) if total_views > 0 else 0)

        # Calculate time on page (simulated - random between 30s and 300s)
        avg_time_on_page = 30 + int(math.sqrt(total_views)) * 10

        return {
            "avg_time_on_page": avg_time_on_page,
            "bounce_rate": bounce_rate * 100,  # Convert to percentage
            "avg_views_per_visitor": avg_views_per_visitor
        }

    def generate_dashboard(self):
        """Generate the complete analytics dashboard HTML."""
        dashboard = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard - Repository</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #bdc3c7;
            font-size: 1.1em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            font-size: 0.9em;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }}
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .stat-card .subtext {{
            font-size: 0.9em;
            color: #95a5a6;
            margin-top: 5px;
        }}
        .section {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .section h2 {{
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }}
        .chart {{
            margin: 20px 0;
        }}
        .bar-chart {{
            display: flex;
            align-items: flex-end;
            height: 300px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            gap: 10px;
        }}
        .bar {{
            flex: 1;
            background: #3498db;
            border-radius: 4px 4px 0 0;
            position: relative;
            transition: all 0.3s;
        }}
        .bar:hover {{
            background: #2980b9;
        }}
        .bar-label {{
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.8em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
        }}
        .bar-value {{
            position: absolute;
            top: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.8em;
            font-weight: bold;
        }}
        .page-list {{
            list-style: none;
        }}
        .page-item {{
            display: flex;
            justify-content: space-between;
            padding: 12px 15px;
            background: #f9f9f9;
            margin-bottom: 8px;
            border-radius: 4px;
        }}
        .page-item:hover {{
            background: #f0f0f0;
        }}
        .page-item .page-name {{
            font-weight: 500;
        }}
        .page-item .page-views {{
            font-weight: bold;
            color: #3498db;
        }}
        .search-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}
        .search-tag {{
            background: #e8f4f8;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        .search-tag .count {{
            font-weight: bold;
            color: #3498db;
        }}
        footer {{
            text-align: center;
            padding: 30px;
            color: #7f8c8d;
        }}
        .date-range {{
            color: #bdc3c7;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Analytics Dashboard</h1>
            <p class="subtitle">Repository Website Analytics</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Page Views</h3>
                <div class="value">{len(self.data['page_views'])}</div>
                <div class="subtext">All time</div>
            </div>
            <div class="stat-card">
                <h3>Unique Visitors</h3>
                <div class="value">{self.data['total_visitors']}</div>
                <div class="subtext">All time</div>
            </div>
            <div class="stat-card">
                <h3>Current Visitors</h3>
                <div class="value">{self.data.get('current_visitors', 0)}</div>
                <div class="subtext">Now viewing</div>
            </div>
            <div class="stat-card">
                <h3>Search Queries</h3>
                <div class="value">{len(self.data['search_queries'])}</div>
                <div class="subtext">All time</div>
            </div>
        </div>

        <div class="section">
            <h2>📈 Page Views Over Time</h2>
            <div class="chart">
                <div class="bar-chart">
"""
        # Add bars for the last 30 days
        daily_stats = self._get_daily_stats(30)
        max_views = max((stat["views"] for stat in daily_stats), default=1)

        for stat in daily_stats:
            height = (stat["views"] / max_views) * 100 if max_views > 0 else 0
            dashboard += f"""                    <div class="bar" style="height: {height}%;">
                        <div class="bar-value">{stat["views"]}</div>
                        <div class="bar-label">{stat["date"]}</div>
                    </div>
"""

        dashboard += """                </div>
            </div>
            <p class="date-range">Last 30 days</p>
        </div>

        <div class="section">
            <h2>🏆 Top Pages</h2>
            <ul class="page-list">
"""
        top_pages = self._get_top_pages(10)
        for i, (page, views, unique) in enumerate(top_pages, 1):
            dashboard += f"""                <li class="page-item">
                    <span class="page-name">{i}. {page}</span>
                    <span class="page-views">{views} views</span>
                </li>
"""

        dashboard += """            </ul>
        </div>

        <div class="section">
            <h2>🔍 Search Queries</h2>
            <p>Total searches: <strong>{len(self.data['search_queries'])}</strong></p>
            <p>Unique queries: <strong>{len(set(q['query'] for q in self.data['search_queries']))}</strong></p>
            <div class="search-list">
"""

        search_stats = self._get_search_stats()
        for item in search_stats['top_queries']:
            dashboard += f"""                <span class="search-tag">
                    "{item['query']}" <span class="count">{item['count']}</span>
                </span>
"""

        dashboard += """            </div>
        </div>

        <div class="section">
            <h2>💡 Engagement Metrics</h2>
            <ul>
                <li><strong>Average Time on Page:</strong> {avg_time}s</li>
                <li><strong>Bounce Rate:</strong> {bounce_rate}%</li>
                <li><strong>Average Views per Visitor:</strong> {avg_views:.2f}</li>
            </ul>
        </div>

        <footer>
            <p>Analytics data updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>
"""

        return dashboard

    def generate_dashboard_file(self, output_file="docs/analytics-dashboard.html"):
        """Generate the dashboard HTML file."""
        dashboard = self.generate_dashboard()
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(dashboard, encoding='utf-8')
        return output_path


def main():
    """Run analytics dashboard generator demo."""
    generator = AnalyticsDashboardGenerator()
    dashboard = generator.generate_dashboard()

    print("=== ANALYTICS DASHBOARD GENERATED ===")
    print("\n" + dashboard)
    print("\nDashboard HTML generated successfully.")

    # Generate file
    output_file = generator.generate_dashboard_file()
    print(f"\nDashboard saved to: {output_file}")
    print(f"File size: {output_file.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
