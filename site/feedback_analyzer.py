#!/usr/bin/env python3
"""Automated feedback summary and alert system for the Drift website.

This script analyzes user feedback data and generates:
- Summary reports by category and priority
- Alert notifications for critical issues
- Trends and patterns over time
- Response tracking and statistics
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


class FeedbackAnalyzer:
    """Analyze and summarize user feedback data."""

    def __init__(self, feedback_file: Path = Path("docs/feedback.json")):
        """Initialize the feedback analyzer.

        Args:
            feedback_file: Path to the feedback JSON file
        """
        self.feedback_file = feedback_file
        self.feedback_data = self._load_feedback()
        self.stats = self._calculate_stats()

    def _load_feedback(self) -> List[Dict]:
        """Load feedback data from JSON file.

        Returns:
            List of feedback dictionaries
        """
        if self.feedback_file.exists():
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _calculate_stats(self) -> Dict:
        """Calculate statistics from feedback data.

        Returns:
            Dictionary with statistics
        """
        if not self.feedback_data:
            return {
                "total": 0,
                "by_category": {},
                "by_priority": {},
                "by_status": {},
                "recent": [],
                "critical_issues": [],
                "trends": {}
            }

        # Calculate totals
        total = len(self.feedback_data)
        by_category = Counter([f.get("category", "other") for f in self.feedback_data])
        by_priority = Counter([f.get("priority", "medium") for f in self.feedback_data])
        by_status = Counter([f.get("status", "new") for f in self.feedback_data])

        # Get recent feedback (last 30 days)
        cutoff = datetime.now() - timedelta(days=30)
        recent = [
            f for f in self.feedback_data
            if datetime.fromisoformat(f.get("submittedAt", ""))
            > cutoff
        ]

        # Get critical issues
        critical = [
            f for f in self.feedback_data
            if f.get("priority", "medium") in ["high", "critical"]
        ]

        # Trends (by day)
        trends = defaultdict(int)
        for f in self.feedback_data:
            date = datetime.fromisoformat(f.get("submittedAt", "")).date()
            trends[date] += 1

        # Convert date objects to strings for JSON serialization
        trends_serializable = {
            str(date): count for date, count in trends.items()
        }

        return {
            "total": total,
            "by_category": dict(by_category),
            "by_priority": dict(by_priority),
            "by_status": dict(by_status),
            "recent": recent[:20],  # Last 20 recent entries
            "critical_issues": critical,
            "trends": trends_serializable
        }

    def generate_summary(self) -> str:
        """Generate a comprehensive feedback summary.

        Returns:
            Formatted summary string
        """
        if not self.feedback_data:
            return "No feedback data available."

        lines = []
        lines.append("=" * 60)
        lines.append("FEEDBACK SUMMARY")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Feedback: {self.stats['total']}")
        lines.append("")

        # Category breakdown
        lines.append("Category Breakdown:")
        for category, count in sorted(self.stats['by_category'].items()):
            pct = (count / self.stats['total']) * 100
            lines.append(f"  {category.capitalize():20s}: {count:3d} ({pct:5.1f}%)")
        lines.append("")

        # Priority breakdown
        lines.append("Priority Breakdown:")
        for priority, count in sorted(self.stats['by_priority'].items()):
            pct = (count / self.stats['total']) * 100
            lines.append(f"  {priority.capitalize():10s}: {count:3d} ({pct:5.1f}%)")
        lines.append("")

        # Status breakdown
        lines.append("Status Breakdown:")
        for status, count in sorted(self.stats['by_status'].items()):
            pct = (count / self.stats['total']) * 100
            lines.append(f"  {status.capitalize():20s}: {count:3d} ({pct:5.1f}%)")
        lines.append("")

        # Critical issues
        if self.stats['critical_issues']:
            lines.append("Critical Issues Requiring Attention:")
            for issue in self.stats['critical_issues']:
                lines.append(f"  - {issue.get('category', 'Unknown')}: {issue.get('description', 'No description')[:60]}...")
                lines.append(f"    ID: {issue.get('id', 'N/A')}")
            lines.append("")

        # Recent activity
        lines.append("Recent Activity (Last 30 Days):")
        for f in self.stats['recent']:
            date = datetime.fromisoformat(f.get('submittedAt', '')).strftime('%Y-%m-%d')
            category = f.get('category', 'Unknown')
            priority = f.get('priority', 'medium')
            lines.append(f"  {date} - {category}: {priority}")
        lines.append("")

        # Trends
        lines.append("Feedback Trends:")
        if self.stats['trends']:
            # Get last 7 days of data
            last_7_days = {
                date: count for date, count in self.stats['trends'].items()
                if date >= str((datetime.now() - timedelta(days=7)).date())
            }
            if last_7_days:
                max_count = max(last_7_days.values())
                for date, count in sorted(last_7_days.items()):
                    bar = "█" * int((count / max_count) * 30)
                    lines.append(f"  {date}: {bar} {count}")
        else:
            lines.append("  No trend data available.")
        lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)

    def generate_alerts(self) -> List[str]:
        """Generate alert messages for critical issues.

        Returns:
            List of alert messages
        """
        alerts = []

        if not self.feedback_data:
            return alerts

        # Critical priority alerts
        high_priority = [
            f for f in self.feedback_data
            if f.get('priority') == 'high'
        ]

        if high_priority:
            alerts.append(f"⚠️ HIGH PRIORITY ALERT: {len(high_priority)} high-priority items require attention")

        # Critical priority alerts
        critical_issues = [
            f for f in self.feedback_data
            if f.get('priority') == 'critical'
        ]

        if critical_issues:
            alerts.append(f"🚨 CRITICAL ALERT: {len(critical_issues)} critical issues need immediate attention")

        # Unanswered critical issues (if we had response tracking)
        unanswered_critical = [
            f for f in self.feedback_data
            if f.get('priority') == 'critical' and f.get('status') == 'new'
        ]

        if unanswered_critical:
            alerts.append(f"⏰ UNRESPONDED ALERT: {len(unanswered_critical)} critical items haven't been addressed yet")

        # Low response rate (if we had response tracking)
        if self.stats['total'] > 10:
            response_rate = (self.stats['by_status'].get('responded', 0) / self.stats['total']) * 100
            if response_rate < 50:
                alerts.append(f"⚠️ LOW RESPONSE RATE: Only {response_rate:.1f}% of feedback has been responded to")

        return alerts

    def generate_dashboard_html(self, output_file: Path = Path("docs/feedback-dashboard.html")):
        """Generate an HTML dashboard for feedback visualization.

        Args:
            output_file: Path to output HTML file
        """
        if not self.feedback_data:
            html_content = """
            <html>
            <head>
                <title>Feedback Dashboard</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <h1>Feedback Dashboard</h1>
                <p>No feedback data available.</p>
            </body>
            </html>
            """
            output_file.write_text(html_content, encoding="utf-8")
            return

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedback Dashboard</title>
    <link rel="stylesheet" href="/static/style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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

        <div class="dashboard-stats">
            <div class="stat-card">
                <h3>Total Feedback</h3>
                <p class="stat-number">{self.stats['total']}</p>
            </div>
            <div class="stat-card">
                <h3>Critical Issues</h3>
                <p class="stat-number critical">{len(self.stats['critical_issues'])}</p>
            </div>
            <div class="stat-card">
                <h3>High Priority</h3>
                <p class="stat-number high">{sum(1 for f in self.feedback_data if f.get('priority') == 'high')}</p>
            </div>
            <div class="stat-card">
                <h3>Medium Priority</h3>
                <p class="stat-number medium">{sum(1 for f in self.feedback_data if f.get('priority') == 'medium')}</p>
            </div>
        </div>

        <div class="dashboard-charts">
            <div class="chart-container">
                <h3>Feedback by Category</h3>
                <canvas id="categoryChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>Feedback by Priority</h3>
                <canvas id="priorityChart"></canvas>
            </div>
        </div>

        <div class="dashboard-list">
            <h3>Recent Feedback</h3>
            <div class="list-container">
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Category</th>
                            <th>Priority</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for f in reversed(self.stats['recent']):
            date = datetime.fromisoformat(f.get('submittedAt', '')).strftime('%Y-%m-%d')
            category = f.get('category', 'Unknown')
            priority = f.get('priority', 'medium')
            description = f.get('description', 'No description')[:50] + '...'
            priority_class = priority
            html_content += f"""
                        <tr>
                            <td>{date}</td>
                            <td>{category}</td>
                            <td class="{priority_class}">{priority}</td>
                            <td>{description}</td>
                        </tr>
"""
        html_content += """
                    </tbody>
                </table>
            </div>
        </div>

        <div class="dashboard-alerts">
            <h3>Alerts</h3>
"""
        alerts = self.generate_alerts()
        for alert in alerts:
            html_content += f"<div class=\"alert alert-{alert.split(':')[0].strip().lower()}\">{alert}</div>"
        html_content += """
        </div>
    </main>

    <footer>
        <p>&copy; 2026 Drift. All rights reserved.</p>
    </footer>

    <script>
        const categoryData = {
            labels: ['""" + "', '".join(self.stats['by_category'].keys()) + """'],
            datasets: [{
                label: 'Count',
                data: ['""" + "', '".join(str(self.stats['by_category'].get(k, 0)) for k in self.stats['by_category'].keys()) + """'],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)'
                ]
            }]
        };

        const priorityData = {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                label: 'Count',
                data: [
                    """ + str(len(self.stats['critical_issues'])) + """,
                    """ + str(sum(1 for f in self.feedback_data if f.get('priority') == 'high')) + """,
                    """ + str(sum(1 for f in self.feedback_data if f.get('priority') == 'medium')) + """,
                    """ + str(sum(1 for f in self.feedback_data if f.get('priority') == 'low')) + """
                ],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(255, 159, 64, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ]
            }]
        };

        new Chart(document.getElementById('categoryChart'), {
            type: 'bar',
            data: categoryData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

        new Chart(document.getElementById('priorityChart'), {
            type: 'doughnut',
            data: priorityData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    </script>
</body>
</html>
"""
        output_file.write_text(html_content, encoding="utf-8")

    def save_feedback_data(self):
        """Save feedback data to JSON file.

        This creates the feedback.json file with all feedback data.
        """
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.feedback_file, "w", encoding="utf-8") as f:
            json.dump(self.feedback_data, f, indent=2, default=str)


def main():
    """Main function to run the feedback analyzer."""
    analyzer = FeedbackAnalyzer()

    # Generate and print summary
    print(analyzer.generate_summary())

    # Generate alerts
    alerts = analyzer.generate_alerts()
    print("\n" + "=" * 60)
    print("ALERTS")
    print("=" * 60)
    for alert in alerts:
        print(alert)

    # Generate dashboard HTML
    dashboard_path = Path("docs/feedback-dashboard.html")
    analyzer.generate_dashboard_html(dashboard_path)
    print(f"\n✓ Dashboard generated: {dashboard_path}")

    # Save feedback data
    analyzer.save_feedback_data()
    print(f"✓ Feedback data saved: {analyzer.feedback_file}")


if __name__ == "__main__":
    main()
