"""Generate feedback dashboard from feedback data.

This script generates a comprehensive feedback dashboard showing:
- Feedback trends over time
- Category and priority distribution
- Most common feedback items
- Action items for the team
"""

import json
from datetime import datetime
from pathlib import Path
from collections import Counter
from typing import Dict, List, Any


class FeedbackDashboardGenerator:
    """Generate feedback dashboard HTML."""

    def __init__(self, feedback_file: Path = Path("docs/feedback.json")):
        """Initialize dashboard generator.

        Args:
            feedback_file: Path to feedback JSON file
        """
        self.feedback_file = feedback_file
        self.data = self._load_feedback()

    def _load_feedback(self) -> List[Dict[str, Any]]:
        """Load feedback data.

        Returns:
            List of feedback entries
        """
        if not self.feedback_file.exists():
            print("⚠️  No feedback data found")
            return []
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Error loading feedback: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall feedback statistics.

        Returns:
            Dictionary with statistics
        """
        total = len(self.data)
        if total == 0:
            return {
                "total": 0,
                "categories": {},
                "priorities": {},
                "trends": {},
                "keywords": [],
                "recent": [],
                "action_items": [],
            }

        # Category distribution
        categories = Counter(f.get("category", "other") for f in self.data)
        categories = {k: v for k, v in sorted(categories.items(), key=lambda x: -x[1])}

        # Priority distribution
        priorities = Counter(f.get("priority", "medium") for f in self.data)
        priorities = {k: v for k, v in sorted(priorities.items(), key=lambda x: -x[1])}

        # Most recent feedback
        recent = sorted(
            [f for f in self.data if f.get("timestamp")],
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )[:10]

        # Keywords (simple extraction)
        keywords = self._extract_keywords()

        # Action items (high priority items needing attention)
        action_items = [
            f for f in recent
            if f.get("priority") in ["high", "critical"]
        ]

        return {
            "total": total,
            "categories": categories,
            "priorities": priorities,
            "trends": self._get_trends(),
            "keywords": keywords[:15],
            "recent": recent,
            "action_items": action_items,
        }

    def _extract_keywords(self) -> List[str]:
        """Extract most frequent keywords from feedback.

        Returns:
            List of top keywords
        """
        words = []
        stop_words = {"the", "and", "is", "a", "an", "to", "of", "in", "for", "with", "on", "at",
                     "by", "from", "that", "this", "it", "are", "was", "were", "be", "been",
                     "being", "have", "has", "had", "do", "does", "did", "will", "would",
                     "could", "should", "may", "might", "must", "can", "need", "like", "just",
                     "very", "more", "most", "some", "any", "such", "no", "not", "only",
                     "own", "same", "so", "than", "too", "very", "now", "then", "here",
                     "there", "when", "where", "why", "how", "all", "each", "few", "more",
                     "most", "other", "some", "such", "no", "nor", "not", "only", "own",
                     "same", "so", "than", "too", "very", "s", "t", "don", "should", "now"}

        for entry in self.data:
            description = entry.get("description", "").lower()
            # Split into words, remove punctuation
            words.extend(word.strip(".,!?;:\"'()[]{}") for word in description.split())

        # Filter stop words
        words = [w for w in words if w and w not in stop_words and len(w) > 2]

        # Count and sort
        word_counts = Counter(words)
        return [{"word": word, "count": count} for word, count in word_counts.most_common(20)]

    def _get_trends(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get feedback trends over time.

        Returns:
            Dictionary with trend data
        """
        if not self.data:
            return {}

        # Group by week
        weeks = {}
        for entry in self.data:
            timestamp = entry.get("timestamp", "")
            if not timestamp:
                continue
            try:
                dt = datetime.fromisoformat(timestamp)
                week_key = dt.strftime("%Y-W%V")
                if week_key not in weeks:
                    weeks[week_key] = []
                weeks[week_key].append(entry)
            except (ValueError, TypeError):
                continue

        # Sort by week
        sorted_weeks = sorted(weeks.items(), key=lambda x: x[0])

        return {
            week: {"count": len(entries), "entries": entries[:5]}
            for week, entries in sorted_weeks
        }

    def generate_dashboard(self, output_file: Path = Path("docs/feedback-dashboard.html")):
        """Generate feedback dashboard HTML.

        Args:
            output_file: Path to output HTML file
        """
        stats = self.get_statistics()

        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedback Dashboard - Drift</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <nav>
            <a href="/index.html">Home</a>
            <a href="/runs.html">Runs</a>
            <a href="/tools.html">Tools</a>
            <a href="/metrics.html">Metrics</a>
            <a href="/knowledge_base.html">Knowledge</a>
            <a href="/search.html">Search</a>
            <a href="/developer_guide.html">Developer Guide</a>
            <a href="/contributing.html">Contributing</a>
            <a href="/troubleshooting.html">Troubleshooting</a>
            <a href="/maintenance_checklist.html">Maintenance Checklist</a>
        </nav>
    </header>

    <main>
        <h1>Feedback Dashboard</h1>
"""

        if stats["total"] == 0:
            html += """
        <div class="alert alert-info">
            <h2>No feedback yet</h2>
            <p>Feedback will appear here once users start submitting it.</p>
            <p>You can view the <a href="feedback.html">feedback form</a> to submit your own feedback.</p>
        </div>
</main>

<footer>
    <p>&copy; 2026 Drift. All rights reserved.</p>
</footer>

</body>
</html>"""
        else:
            html += f"""
        <div class="dashboard-summary">
            <div class="stat-card">
                <div class="stat-label">Total Feedback</div>
                <div class="stat-value">{stats["total"]}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Action Items</div>
                <div class="stat-value highlight">{len(stats["action_items"])}</div>
            </div>
        </div>

        <div class="dashboard-section">
            <h2>Feedback by Category</h2>
            <div class="chart-container">
"""

            for category, count in stats["categories"].items():
                if count > 0:
                    percentage = (count / stats["total"]) * 100
                    html += f"""
                <div class="bar-chart-item">
                    <span class="bar-label">{category.capitalize()}</span>
                    <span class="bar-value">{count}</span>
                    <div class="bar-fill" style="width: {percentage}%">
                        <span class="bar-percent">{percentage:.1f}%</span>
                    </div>
                </div>"""

            html += """
            </div>
        </div>

        <div class="dashboard-section">
            <h2>Feedback by Priority</h2>
            <div class="chart-container">
"""

            for priority, count in stats["priorities"].items():
                if count > 0:
                    percentage = (count / stats["total"]) * 100
                    color = {
                        "critical": "#dc2626",
                        "high": "#ea580c",
                        "medium": "#ca8a04",
                        "low": "#4b5563"
                    }.get(priority, "#4b5563")
                    html += f"""
                <div class="bar-chart-item">
                    <span class="bar-label">{priority.capitalize()}</span>
                    <span class="bar-value">{count}</span>
                    <div class="bar-fill" style="width: {percentage}%; background-color: {color}">
                        <span class="bar-percent">{percentage:.1f}%</span>
                    </div>
                </div>"""

            html += """
            </div>
        </div>

"""

            if stats["keywords"]:
                html += """
        <div class="dashboard-section">
            <h2>Most Common Keywords</h2>
            <div class="keyword-cloud">
"""
                for kw in stats["keywords"]:
                    html += f"""
                <span class="keyword-tag">{kw["word"]} ({kw["count"]})</span>"""
                html += """
            </div>
        </div>
"""

            if stats["trends"]:
                html += """
        <div class="dashboard-section">
            <h2>Feedback Trends (Recent Weeks)</h2>
            <div class="trend-chart">
"""
                for week, data in sorted(stats["trends"].items(), key=lambda x: x[0]):
                    html += f"""
                <div class="trend-item">
                    <span class="trend-label">Week {week}</span>
                    <span class="trend-value">{data["count"]} feedback</span>
                    <div class="trend-bar" style="width: {min(data["count"] * 5, 100)}%"></div>
                </div>"""
                html += """
            </div>
        </div>
"""

            if stats["action_items"]:
                html += """
        <div class="dashboard-section">
            <h2>🚨 Action Items (High Priority)</h2>
            <div class="action-list">
"""
                for item in stats["action_items"]:
                    category = item.get("category", "Other").capitalize()
                    priority = item.get("priority", "Medium").capitalize()
                    desc = item.get("description", "No description").replace('"', "'")
                    html += f"""
                <div class="action-item card">
                    <span class="action-tag tag-{priority}">{priority}</span>
                    <span class="action-category">{category}</span>
                    <p class="action-description">"{desc}"</p>
                </div>"""
                html += """
            </div>
        </div>
"""

            html += """
        <div class="dashboard-section">
            <h2>Recent Feedback</h2>
            <div class="feedback-list">
"""
            for item in stats["recent"]:
                category = item.get("category", "Other").capitalize()
                priority = item.get("priority", "Medium").capitalize()
                desc = item.get("description", "No description").replace('"', "'")
                name = item.get("name", "Anonymous")
                timestamp = item.get("timestamp", "")[:10]

                html += f"""
                <div class="feedback-item card">
                    <div class="feedback-header">
                        <span class="feedback-category">{category}</span>
                        <span class="feedback-priority tag-{priority}">{priority}</span>
                    </div>
                    <p class="feedback-description">"{desc}"</p>
                    <div class="feedback-footer">
                        <span class="feedback-user">👤 {name}</span>
                        <span class="feedback-date">📅 {timestamp}</span>
                    </div>
                </div>"""

            html += """
            </div>
        </div>
"""

        html += """
    </main>

    <footer>
        <p>&copy; 2026 Drift. All rights reserved.</p>
    </footer>

</body>
</html>"""

        # Write output file
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Feedback dashboard generated: {output_file}")
        print(f"   Total feedback: {stats['total']}")
        print(f"   Action items: {len(stats['action_items'])}")

        return stats


if __name__ == "__main__":
    generator = FeedbackDashboardGenerator()
    generator.generate_dashboard()
