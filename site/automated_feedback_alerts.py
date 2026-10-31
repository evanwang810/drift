"""Automated Feedback Alerts and Summaries.

This module provides automated generation of feedback summaries and alerts,
including:
- Periodic summary reports
- Priority-based alerts
- Category distribution summaries
- Trend analysis and recommendations
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from site.feedback_system import FeedbackSystem, feedback_system
from site.feedback_analytics import FeedbackAnalytics, analytics


class FeedbackAlerts:
    """Generate alerts and summaries from feedback data."""

    def __init__(self, data_file: Path = Path("docs/feedback.json")):
        """Initialize alerts system.

        Args:
            data_file: Path to feedback JSON storage file
        """
        self.data_file = data_file
        self.system = FeedbackSystem(data_file)
        self.analytics = FeedbackAnalytics(data_file)

    def generate_weekly_summary(self) -> Dict[str, Any]:
        """Generate a weekly summary of feedback.

        Returns:
            Summary dictionary with all statistics
        """
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        one_week_ago_ts = one_week_ago.timestamp()

        recent_feedback = [
            f for f in self.system.get_all_feedback()
            if datetime.fromisoformat(f.get("submittedAt", "")).timestamp() > one_week_ago_ts
        ]

        summary = {
            "period_start": one_week_ago.isoformat(),
            "period_end": datetime.utcnow().isoformat(),
            "total_received": len(recent_feedback),
            "by_category": {},
            "by_priority": {},
            "average_response_time": "N/A",
            "top_concerns": [],
            "recommendations": []
        }

        # Category distribution
        for cat in ["bug", "feature", "improvement", "compliment", "other"]:
            count = sum(1 for f in recent_feedback if f.get("category") == cat)
            summary["by_category"][cat] = count

        # Priority distribution
        for pri in ["critical", "high", "medium", "low"]:
            count = sum(1 for f in recent_feedback if f.get("priority") == pri)
            summary["by_priority"][pri] = count

        # Top concerns (keywords from bug reports)
        bug_feedback = [f for f in recent_feedback if f.get("category") == "bug"]
        if bug_feedback:
            keywords = self.analytics.get_keyword_frequency()
            summary["top_concerns"] = [
                {"keyword": k, "count": v}
                for k, v in keywords[:5]
            ]

        # Generate recommendations
        summary["recommendations"] = self._generate_recommendations(summary)

        return summary

    def generate_priority_alerts(self) -> List[Dict[str, Any]]:
        """Generate alerts for high priority issues.

        Returns:
            List of alert dictionaries
        """
        alerts = []
        high_priority = self.system.get_feedback_by_priority("high")
        critical = self.system.get_feedback_by_priority("critical")

        # Critical alerts
        for feedback in critical:
            alerts.append({
                "level": "CRITICAL",
                "type": "urgent",
                "message": f"Critical issue detected: {feedback.get('description', 'No description')[:100]}",
                "feedback_id": feedback.get("id"),
                "category": feedback.get("category"),
                "priority": feedback.get("priority")
            })

        # High priority alerts
        for feedback in high_priority:
            if feedback not in critical:  # Avoid duplicates
                alerts.append({
                    "level": "HIGH",
                    "type": "important",
                    "message": f"High priority feedback: {feedback.get('description', 'No description')[:100]}",
                    "feedback_id": feedback.get("id"),
                    "category": feedback.get("category"),
                    "priority": feedback.get("priority")
                })

        return alerts

    def generate_category_report(self, category: str) -> Dict[str, Any]:
        """Generate a detailed report for a specific category.

        Args:
            category: Category name (bug, feature, etc.)

        Returns:
            Category report dictionary
        """
        category_feedback = self.system.get_feedback_by_category(category)

        report = {
            "category": category,
            "total": len(category_feedback),
            "by_priority": {},
            "recent": category_feedback[:5],
            "average_priority": "N/A"
        }

        # Priority breakdown
        for pri in ["critical", "high", "medium", "low"]:
            count = sum(1 for f in category_feedback if f.get("priority") == pri)
            report["by_priority"][pri] = count

        # Average priority score
        if category_feedback:
            priority_scores = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            avg_score = sum(
                priority_scores.get(f.get("priority", "medium"), 2)
                for f in category_feedback
            ) / len(category_feedback)
            report["average_priority"] = avg_score

        return report

    def generate_daily_digest(self) -> Dict[str, Any]:
        """Generate a daily digest of feedback activity.

        Returns:
            Daily digest dictionary
        """
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)

        # Get feedback from today and yesterday
        today_ts = datetime.combine(today, datetime.min.time()).timestamp()
        yesterday_ts = datetime.combine(yesterday, datetime.min.time()).timestamp()

        today_feedback = [
            f for f in self.system.get_all_feedback()
            if yesterday_ts < datetime.fromisoformat(f.get("submittedAt", "")).timestamp() <= today_ts
        ]

        digest = {
            "date": today.isoformat(),
            "feedback_count": len(today_feedback),
            "by_category": {},
            "by_priority": {},
            "newest_feedback": today_feedback[:3]
        }

        # Breakdown
        for cat in ["bug", "feature", "improvement", "compliment", "other"]:
            digest["by_category"][cat] = sum(1 for f in today_feedback if f.get("category") == cat)

        for pri in ["critical", "high", "medium", "low"]:
            digest["by_priority"][pri] = sum(1 for f in today_feedback if f.get("priority") == pri)

        return digest

    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on feedback patterns.

        Args:
            summary: Weekly summary dictionary

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Critical issues
        if summary["by_priority"].get("critical", 0) > 0:
            recommendations.append(
                "URGENT: Address critical issues immediately. "
                "Review all critical feedback and create an action plan."
            )

        # High priority issues
        if summary["by_priority"].get("high", 0) > 3:
            recommendations.append(
                "Attention: Multiple high-priority issues detected. "
                "Review and prioritize fixes."
            )

        # Bug reports
        if summary["by_category"].get("bug", 0) > summary["by_category"].get("feature", 0):
            recommendations.append(
                "Focus: More bug reports than feature requests. "
                "Consider improving code quality and testing."
            )

        # Feature requests
        if summary["by_category"].get("feature", 0) > 5:
            recommendations.append(
                "Interest: Strong interest in new features. "
                "Review backlog and plan next sprint features."
            )

        # Compliments
        if summary["by_category"].get("compliment", 0) > 5:
            recommendations.append(
                "Positive: Good reception. Share success stories and "
                "documentation improvements."
            )

        # If no specific recommendations
        if not recommendations:
            recommendations.append(
                "Stable: Feedback is balanced. Continue monitoring "
                "and responding to all feedback."
            )

        return recommendations


# Global instance
alerts = FeedbackAlerts()


def main():
    """Generate and display feedback alerts and summaries."""
    print("=" * 60)
    print("FEEDBACK ALERTS AND SUMMARIES")
    print("=" * 60)

    # Generate weekly summary
    print("\n--- WEEKLY SUMMARY ---")
    weekly_summary = alerts.generate_weekly_summary()
    print(f"Period: {weekly_summary['period_start']} to {weekly_summary['period_end']}")
    print(f"Total Feedback: {weekly_summary['total_received']}")
    print("\nBy Category:")
    for cat, count in weekly_summary["by_category"].items():
        print(f"  {cat.title()}: {count}")
    print("\nBy Priority:")
    for pri, count in weekly_summary["by_priority"].items():
        print(f"  {pri.title()}: {count}")
    if weekly_summary["top_concerns"]:
        print("\nTop Concerns:")
        for concern in weekly_summary["top_concerns"]:
            print(f"  '{concern['keyword']}': {concern['count']} occurrences")

    # Generate alerts
    print("\n--- PRIORITY ALERTS ---")
    alerts_list = alerts.generate_priority_alerts()
    for alert in alerts_list:
        print(f"\n[{alert['level']}] {alert['type'].upper()}")
        print(f"  {alert['message']}")
        print(f"  ID: {alert['feedback_id']}")

    # Generate recommendations
    print("\n--- RECOMMENDATIONS ---")
    for rec in weekly_summary["recommendations"]:
        print(f"• {rec}")

    # Generate category reports
    print("\n--- CATEGORY REPORTS ---")
    for category in ["bug", "feature"]:
        print(f"\n{category.title()} Report:")
        report = alerts.generate_category_report(category)
        print(f"  Total: {report['total']}")
        print(f"  By Priority:")
        for pri, count in report["by_priority"].items():
            print(f"    {pri.title()}: {count}")


if __name__ == "__main__":
    main()
