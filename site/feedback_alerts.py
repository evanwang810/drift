"""Feedback Alerts and Summary System.

This module generates automated feedback summaries and alerts based on
priority and category patterns.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from feedback_analytics import FeedbackAnalytics


class FeedbackAlertSystem:
    """Generate alerts and summaries for feedback data."""

    def __init__(self, data_file: Path = Path("docs/feedback.json")):
        """Initialize alert system.

        Args:
            data_file: Path to feedback JSON storage file
        """
        self.analytics = FeedbackAnalytics(data_file)

    def generate_critical_alerts(self) -> List[Dict[str, Any]]:
        """Generate alerts for critical priority feedback.

        Returns:
            List of critical alerts with details
        """
        critical_feedback = [
            f for f in self.analytics.data
            if f.get("priority") == "critical"
        ]

        alerts = []

        if critical_feedback:
            alerts.append({
                "level": "critical",
                "message": f"Critical priority feedback received: {len(critical_feedback)} items",
                "details": critical_feedback,
                "timestamp": datetime.utcnow().isoformat()
            })

        return alerts

    def generate_bug_report_alert(self) -> List[Dict[str, Any]]:
        """Generate alert if bug reports are trending up.

        Returns:
            List of bug-related alerts
        """
        week_ago = datetime.utcnow() - timedelta(days=7)
        month_ago = datetime.utcnow() - timedelta(days=30)

        week_bugs = len([
            f for f in self.analytics.data
            if f.get("category") == "bug"
            and datetime.fromisoformat(f.get("timestamp", "")) >= week_ago
        ])

        month_bugs = len([
            f for f in self.analytics.data
            if f.get("category") == "bug"
            and datetime.fromisoformat(f.get("timestamp", "")) >= month_ago
        ])

        alerts = []

        if week_bugs > 0 and month_bugs > 0:
            growth = ((week_bugs - month_bugs) / month_bugs * 100)
            if growth > 0:
                alerts.append({
                    "level": "warning",
                    "message": f"Bug reports are increasing: {growth:.1f}% growth this month",
                    "details": {
                        "month_bugs": month_bugs,
                        "week_bugs": week_bugs,
                        "growth": growth
                    },
                    "timestamp": datetime.utcnow().isoformat()
                })

        return alerts

    def generate_feature_request_summary(self) -> Dict[str, Any]:
        """Generate summary of feature requests.

        Returns:
            Dictionary with feature request summary
        """
        feature_requests = [
            f for f in self.analytics.data
            if f.get("category") == "feature"
        ]

        # Group by priority
        high_features = len([f for f in feature_requests if f.get("priority") == "high"])
        medium_features = len([f for f in feature_requests if f.get("priority") == "medium"])
        low_features = len([f for f in feature_requests if f.get("priority") == "low"])

        # Group by keywords
        keywords = {}
        for f in feature_requests:
            description = f.get("description", "").lower()
            # Simple keyword extraction
            words = description.split()[:5]  # First 5 words
            for word in words:
                if len(word) > 4:  # Only words longer than 4 chars
                    keywords[word] = keywords.get(word, 0) + 1

        top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total": len(feature_requests),
            "high_priority": high_features,
            "medium_priority": medium_features,
            "low_priority": low_features,
            "top_keywords": [{"keyword": k, "count": v} for k, v in top_keywords],
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_bug_summary(self) -> Dict[str, Any]:
        """Generate summary of bug reports.

        Returns:
            Dictionary with bug report summary
        """
        bug_reports = [
            f for f in self.analytics.data
            if f.get("category") == "bug"
        ]

        # Group by priority
        critical_bugs = len([f for f in bug_reports if f.get("priority") == "critical"])
        high_bugs = len([f for f in bug_reports if f.get("priority") == "high"])
        medium_bugs = len([f for f in bug_reports if f.get("priority") == "medium"])
        low_bugs = len([f for f in bug_reports if f.get("priority") == "low"])

        # Get recent bugs
        recent = sorted(bug_reports, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]

        return {
            "total": len(bug_reports),
            "critical": critical_bugs,
            "high": high_bugs,
            "medium": medium_bugs,
            "low": low_bugs,
            "recent": recent,
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_improvement_summary(self) -> Dict[str, Any]:
        """Generate summary of improvement suggestions.

        Returns:
            Dictionary with improvement summary
        """
        improvements = [
            f for f in self.analytics.data
            if f.get("category") == "improvement"
        ]

        return {
            "total": len(improvements),
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_compliment_summary(self) -> Dict[str, Any]:
        """Generate summary of compliments.

        Returns:
            Dictionary with compliment summary
        """
        compliments = [
            f for f in self.analytics.data
            if f.get("category") == "compliment"
        ]

        return {
            "total": len(compliments),
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_daily_summary(self) -> Dict[str, Any]:
        """Generate comprehensive daily summary.

        Returns:
            Dictionary with all summary data
        """
        return {
            "critical_alerts": self.generate_critical_alerts(),
            "bug_report_alert": self.generate_bug_report_alert(),
            "feature_requests": self.generate_feature_request_summary(),
            "bug_reports": self.generate_bug_summary(),
            "improvements": self.generate_improvement_summary(),
            "compliments": self.generate_compliment_summary(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report.

        Returns:
            Formatted summary report string
        """
        summary = self.generate_daily_summary()

        report = []
        report.append("=" * 60)
        report.append("FEEDBACK DAILY SUMMARY REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {summary['timestamp']}")
        report.append("")

        # Critical alerts
        if summary["critical_alerts"]:
            report.append("⚠️ CRITICAL ALERTS")
            report.append("-" * 60)
            for alert in summary["critical_alerts"]:
                report.append(f"[{alert['timestamp']}] {alert['message']}")
            report.append("")

        # Bug report alerts
        bug_alerts = summary["bug_report_alert"]
        if bug_alerts:
            report.append("🛠️ BUG TRENDS")
            report.append("-" * 60)
            for alert in bug_alerts:
                report.append(f"[{alert['timestamp']}] {alert['message']}")
            report.append("")

        # Feature requests
        features = summary["feature_requests"]
        report.append("💡 FEATURE REQUESTS")
        report.append("-" * 60)
        report.append(f"Total: {features['total']}")
        report.append(f"High Priority: {features['high_priority']}")
        report.append(f"Medium Priority: {features['medium_priority']}")
        report.append(f"Low Priority: {features['low_priority']}")
        report.append("Top Keywords:")
        for kw in features["top_keywords"][:5]:
            report.append(f"  • {kw['keyword']}: {kw['count']} times")
        report.append("")

        # Bug reports
        bugs = summary["bug_reports"]
        report.append("🐛 BUG REPORTS")
        report.append("-" * 60)
        report.append(f"Total: {bugs['total']}")
        report.append(f"Critical: {bugs['critical']}")
        report.append(f"High: {bugs['high']}")
        report.append(f"Medium: {bugs['medium']}")
        report.append(f"Low: {bugs['low']}")
        report.append("")

        # Improvements
        improvements = summary["improvements"]
        report.append("✨ IMPROVEMENTS")
        report.append("-" * 60)
        report.append(f"Total: {improvements['total']}")
        report.append("")

        # Compliments
        compliments = summary["compliments"]
        report.append("🌟 COMPLIMENTS")
        report.append("-" * 60)
        report.append(f"Total: {compliments['total']}")
        report.append("")

        report.append("=" * 60)
        report.append("END OF SUMMARY")
        report.append("=" * 60)

        return "\n".join(report)

    def save_alerts_to_file(self, alerts_file: Path = Path("docs/feedback-alerts.json")) -> None:
        """Save alerts and summaries to a JSON file.

        Args:
            alerts_file: Path to output JSON file
        """
        summary = self.generate_daily_summary()
        alerts_file.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
        print(f"Alerts saved to: {alerts_file}")


if __name__ == "__main__":
    alert_system = FeedbackAlertSystem()

    # Generate and print daily summary
    print(alert_system.generate_summary_report())

    # Save to file
    alert_system.save_alerts_to_file()
