"""Feedback System - Automated feedback collection, analysis, and alerting.

This module handles:
- Feedback data collection and storage
- Automated feedback summaries and categorization
- Priority-based alerts for critical feedback
- Analytics tracking of feedback trends
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class FeedbackSystem:
    """Manage feedback collection, analysis, and alerting."""

    def __init__(self, data_file: Path = Path("docs/feedback.json")):
        """Initialize feedback system.

        Args:
            data_file: Path to feedback JSON storage file
        """
        self.data_file = data_file
        self.data: List[Dict[str, Any]] = self._load_feedback()

    def _load_feedback(self) -> List[Dict[str, Any]]:
        """Load feedback data from file.

        Returns:
            List of feedback entries
        """
        if not self.data_file.exists():
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_feedback(self) -> None:
        """Save feedback data to file."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def add_feedback(self, feedback_data: Dict[str, Any]) -> str:
        """Add a new feedback entry.

        Args:
            feedback_data: Feedback entry data

        Returns:
            Feedback ID for the new entry
        """
        feedback_id = self._generate_feedback_id()

        entry = {
            "id": feedback_id,
            "timestamp": datetime.utcnow().isoformat(),
            **feedback_data
        }

        self.data.insert(0, entry)  # Add to beginning
        self._save_feedback()

        return feedback_id

    def _generate_feedback_id(self) -> str:
        """Generate unique feedback ID.

        Returns:
            Unique feedback ID (FB-YYYYMMDD-XXXXX)
        """
        date_str = datetime.utcnow().strftime("%Y%m%d")
        random_part = f"{random.randint(10000, 99999)}"
        return f"FB-{date_str}-{random_part}"

    def get_feedback(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        """Get feedback by ID.

        Args:
            feedback_id: Feedback ID to retrieve

        Returns:
            Feedback entry or None if not found
        """
        for entry in self.data:
            if entry.get("id") == feedback_id:
                return entry
        return None

    def get_all_feedback(self) -> List[Dict[str, Any]]:
        """Get all feedback entries.

        Returns:
            List of all feedback entries
        """
        return self.data.copy()

    def get_feedback_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get feedback by category.

        Args:
            category: Category to filter by

        Returns:
            List of feedback entries in that category
        """
        return [f for f in self.data if f.get("category") == category]

    def get_feedback_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Get feedback by priority level.

        Args:
            priority: Priority level (low, medium, high, critical)

        Returns:
            List of feedback entries with that priority
        """
        return [f for f in self.data if f.get("priority") == priority]

    def get_summary(self) -> Dict[str, Any]:
        """Generate feedback summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        total = len(self.data)
        if total == 0:
            return {
                "total": 0,
                "by_category": {},
                "by_priority": {},
                "recent": []
            }

        by_category = {}
        by_priority = {}

        for entry in self.data:
            category = entry.get("category", "other")
            priority = entry.get("priority", "medium")

            by_category[category] = by_category.get(category, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1

        # Recent feedback (last 10)
        recent = self.data[:10]

        return {
            "total": total,
            "by_category": by_category,
            "by_priority": by_priority,
            "recent": recent,
            "last_updated": datetime.utcnow().isoformat()
        }

    def get_alerts(self) -> List[Dict[str, Any]]:
        """Generate alerts for critical feedback.

        Returns:
            List of alert messages for critical/high priority items
        """
        alerts = []

        # Check for critical feedback
        critical = self.get_feedback_by_priority("critical")
        if critical:
            alerts.append({
                "type": "critical",
                "count": len(critical),
                "message": f"⚠️ {len(critical)} critical feedback items require immediate attention"
            })

        # Check for high priority feedback
        high = self.get_feedback_by_priority("high")
        if high:
            alerts.append({
                "type": "high",
                "count": len(high),
                "message": f"⚠️ {len(high)} high priority feedback items need review"
            })

        # Check for bug reports
        bugs = self.get_feedback_by_category("bug")
        if bugs:
            alerts.append({
                "type": "bugs",
                "count": len(bugs),
                "message": f"🔍 {len(bugs)} bug reports need investigation"
            })

        # Check for feature requests
        features = self.get_feedback_by_category("feature")
        if features:
            alerts.append({
                "type": "features",
                "count": len(features),
                "message": f"💡 {len(features)} feature requests pending review"
            })

        return alerts

    def get_trending_topics(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get trending topics based on recent feedback.

        Args:
            days: Number of days to look back

        Returns:
            List of trending topics with counts
        """
        cutoff = datetime.utcnow().timestamp() - (days * 24 * 60 * 60)

        recent_feedback = [
            f for f in self.data
            if datetime.fromisoformat(f.get("timestamp", "")).timestamp() > cutoff
        ]

        if not recent_feedback:
            return []

        # Extract keywords from descriptions
        keywords = {}
        for entry in recent_feedback:
            description = entry.get("description", "").lower()
            # Simple keyword extraction
            words = re.findall(r'\b\w{4,}\b', description)
            for word in words:
                keywords[word] = keywords.get(word, 0) + 1

        # Sort by frequency
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)

        return [
            {"keyword": k, "count": v}
            for k, v in sorted_keywords[:10]
        ]


# Global instance
feedback_system = FeedbackSystem()
