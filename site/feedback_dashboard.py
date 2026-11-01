"""Feedback Dashboard Generator.

This module generates a feedback dashboard from the feedback.json file,
showing trends, distributions, and summaries.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from feedback_analytics import FeedbackAnalytics


def generate_dashboard(output_file: Path = Path("docs/feedback-dashboard.html")) -> None:
    """Generate a feedback dashboard HTML file.

    Args:
        output_file: Path to output HTML file
    """
    analytics = FeedbackAnalytics()
    data = analytics.data

    # Calculate time ranges
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    three_months_ago = now - timedelta(days=90)

    # Filter data by time ranges
    recent_week = [f for f in data
                   if datetime.fromisoformat(f.get("timestamp", now.isoformat())) >= week_ago]
    recent_month = [f for f in data
                    if datetime.fromisoformat(f.get("timestamp", now.isoformat())) >= month_ago]
    recent_quarter = [f for f in data
                      if datetime.fromisoformat(f.get("timestamp", now.isoformat())) >= three_months_ago]

    # Generate metrics
    total_feedback = len(data)
    total_week = len(recent_week)
    total_month = len(recent_month)
    total_quarter = len(recent_quarter)

    # Priority distribution
    priority_dist = analytics.get_priority_distribution()

    # Category distribution
    category_dist = analytics.get_category_distribution()

    # Top keywords
    top_keywords = analytics.get_keyword_frequency(top_n=10)

    # Recent feedback (last 10)
    recent = sorted(data, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]

    # Calculate trends
    week_to_month = ((total_month - total_week) / total_week * 100) if total_week > 0 else 0
    month_to_quarter = ((total_quarter - total_month) / total_month * 100) if total_month > 0 else 0

    # HTML template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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

<div class="dashboard-grid">
    <!-- Time Range Metrics -->
    <div class="metric-card">
        <h3>Total Feedback</h3>
        <div class="metric-value">{total_feedback}</div>
        <div class="metric-subtext">All time</div>
    </div>

    <div class="metric-card">
        <h3>Feedback This Week</h3>
        <div class="metric-value">{total_week}</div>
        <div class="metric-subtext">Last 7 days</div>
    </div>

    <div class="metric-card">
        <h3>Feedback This Month</h3>
        <div class="metric-value">{total_month}</div>
        <div class="metric-subtext">Last 30 days</div>
    </div>

    <div class="metric-card">
        <h3>Feedback This Quarter</h3>
        <div class="metric-value">{total_quarter}</div>
        <div class="metric-subtext">Last 90 days</div>
    </div>
</div>

<div class="dashboard-grid">
    <!-- Priority Distribution -->
    <div class="card">
        <h2>Priority Distribution</h2>
        <div class="distribution-chart">
            <div class="bar-container">
                <div class="bar-label">Critical</div>
                <div class="bar-fill critical" style="width: {priority_dist.get('critical', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{priority_dist.get('critical', 0)}</div>
            </div>
            <div class="bar-container">
                <div class="bar-label">High</div>
                <div class="bar-fill high" style="width: {priority_dist.get('high', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{priority_dist.get('high', 0)}</div>
            </div>
            <div class="bar-container">
                <div class="bar-label">Medium</div>
                <div class="bar-fill medium" style="width: {priority_dist.get('medium', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{priority_dist.get('medium', 0)}</div>
            </div>
            <div class="bar-container">
                <div class="bar-label">Low</div>
                <div class="bar-fill low" style="width: {priority_dist.get('low', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{priority_dist.get('low', 0)}</div>
            </div>
        </div>
    </div>

    <!-- Category Distribution -->
    <div class="card">
        <h2>Category Distribution</h2>
        <div class="distribution-chart">
            <div class="bar-container">
                <div class="bar-label">Bug</div>
                <div class="bar-fill bug" style="width: {category_dist.get('bug', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{category_dist.get('bug', 0)}</div>
            </div>
            <div class="bar-container">
                <div class="bar-label">Feature</div>
                <div class="bar-fill feature" style="width: {category_dist.get('feature', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{category_dist.get('feature', 0)}</div>
            </div>
            <div class="bar-container">
                <div class="bar-label">Improvement</div>
                <div class="bar-fill improvement" style="width: {category_dist.get('improvement', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{category_dist.get('improvement', 0)}</div>
            </div>
            <div class="bar-container">
                <div class="bar-label">Compliment</div>
                <div class="bar-fill compliment" style="width: {category_dist.get('compliment', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{category_dist.get('compliment', 0)}</div>
            </div>
            <div class="bar-container">
                <div class="bar-label">Other</div>
                <div class="bar-fill other" style="width: {category_dist.get('other', 0) / max(total_feedback, 1) * 100}%"></div>
                <div class="bar-value">{category_dist.get('other', 0)}</div>
            </div>
        </div>
    </div>
</div>

<div class="dashboard-grid">
    <!-- Top Keywords -->
    <div class="card">
        <h2>Top Keywords</h2>
        <ul class="keyword-list">
"""
    for kw in top_keywords:
        html += f'            <li class="keyword-item"><span class="keyword-count">{kw["frequency"]}</span> {kw["keyword"]}</li>\n'
    html += """        </ul>
    </div>

    <!-- Recent Feedback -->
    <div class="card">
        <h2>Recent Feedback</h2>
        <ul class="feedback-list">
"""
    for item in recent:
        feedback_id = item.get("id", "N/A")
        category = item.get("category", "other").capitalize()
        priority = item.get("priority", "medium").capitalize()
        timestamp = datetime.fromisoformat(item.get("timestamp", "")).strftime("%Y-%m-%d %H:%M")
        description = item.get("description", "")[:100] + ("..." if len(item.get("description", "")) > 100 else "")
        html += f"""            <li class="feedback-item">
                <div class="feedback-header">
                    <span class="feedback-id">#{feedback_id}</span>
                    <span class="feedback-category {category}">{category}</span>
                    <span class="feedback-priority {priority}">{priority}</span>
                </div>
                <div class="feedback-timestamp">{timestamp}</div>
                <div class="feedback-description">{description}</div>
            </li>
"""
    html += """        </ul>
    </div>
</div>

<div class="dashboard-grid">
    <!-- Trends -->
    <div class="card">
        <h2>Trends</h2>
        <div class="trend-cards">
            <div class="trend-card">
                <div class="trend-label">Week to Month</div>
                <div class="trend-value {f'up' if week_to_month >= 0 else 'down'}">{abs(week_to_month):.1f}%</div>
                <div class="trend-direction">{week_to_month >= 0 and '↑' or '↓'}</div>
            </div>
            <div class="trend-card">
                <div class="trend-label">Month to Quarter</div>
                <div class="trend-value {f'up' if month_to_quarter >= 0 else 'down'}">{abs(month_to_quarter):.1f}%</div>
                <div class="trend-direction">{month_to_quarter >= 0 and '↑' or '↓'}</div>
            </div>
        </div>
    </div>

    <!-- Summary -->
    <div class="card">
        <h2>Summary</h2>
        <div class="summary-text">
"""
    # Generate summary text
    if total_week > 0:
        html += f"• <strong>This week:</strong> {total_week} feedback items received\n"
    if total_month > 0:
        html += f"• <strong>This month:</strong> {total_month} feedback items received\n"
    if total_feedback > 0:
        critical_count = priority_dist.get("critical", 0)
        if critical_count > 0:
            html += f"• <strong>Critical priority:</strong> {critical_count} items requiring immediate attention\n"
        bug_count = category_dist.get("bug", 0)
        if bug_count > 0:
            html += f"• <strong>Bug reports:</strong> {bug_count} items\n"
        feature_count = category_dist.get("feature", 0)
        if feature_count > 0:
            html += f"• <strong>Feature requests:</strong> {feature_count} items\n"
    html += """
        </div>
        <div class="summary-footer">
            <p>Generated on {}</p>
            <a href="/feedback.html" class="btn-secondary">View Feedback Form</a>
        </div>
    </div>
</div>

</main>
</body>
</html>
""".format(now.strftime("%Y-%m-%d %H:%M:%S UTC"))

    output_file.write_text(html, encoding="utf-8")
    print(f"Feedback dashboard generated: {output_file}")


if __name__ == "__main__":
    generate_dashboard()
