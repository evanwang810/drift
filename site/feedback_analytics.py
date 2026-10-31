"""Feedback Analytics - Track user behavior and feedback patterns.

This module provides analytics tracking for feedback data, including:
- User behavior tracking
- Feedback trends over time
- Category and priority distribution analysis
- Keyword extraction from feedback
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class FeedbackAnalytics:
    """Track and analyze feedback patterns."""

    def __init__(self, data_file: Path = Path("docs/feedback.json")):
        """Initialize analytics tracker.

        Args:
            data_file: Path to feedback JSON storage file
        """
        self.data_file = data_file
        self.data: List[Dict[str, Any]] = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        """Load feedback data.

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

    def track_page_view(self, page: str, user_id: str = "anonymous") -> None:
        """Track a page view.

        Args:
            page: Page path
            user_id: Optional user identifier
        """
        # In a real system, this would integrate with analytics
        # For now, we log to console
        print(f"[Analytics] Page view: {page} by {user_id}")

    def track_feedback_submit(self, category: str, priority: str) -> None:
        """Track feedback submission.

        Args:
            category: Feedback category
            priority: Feedback priority
        """
        print(f"[Analytics] Feedback submitted: {category}/{priority}")

    def get_page_views(self) -> Dict[str, int]:
        """Get page view statistics.

        Returns:
            Dictionary mapping pages to view counts
        """
        # In a real system, this would query an analytics database
        return {"feedback.html": 1, "feedback-dashboard.html": 0}

    def get_feedback_trends(self, days: int = 30) -> Dict[str, List[Dict[str, Any]]]:
        """Get feedback trends over time.

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with trend data by category
        """
        cutoff = datetime.utcnow().timestamp() - (days * 24 * 60 * 60)

        recent = [
            f for f in self.data
            if datetime.fromisoformat(f.get("timestamp", "")).timestamp() > cutoff
        ]

        trends = {}
        for entry in recent:
            category = entry.get("category", "other")
            if category not in trends:
                trends[category] = []
            trends[category].append(entry)

        return trends

    def get_priority_distribution(self) -> Dict[str, int]:
        """Get distribution of feedback by priority.

        Returns:
            Dictionary with priority counts
        """
        distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for entry in self.data:
            priority = entry.get("priority", "medium")
            distribution[priority] = distribution.get(priority, 0) + 1
        return distribution

    def get_category_distribution(self) -> Dict[str, int]:
        """Get distribution of feedback by category.

        Returns:
            Dictionary with category counts
        """
        distribution = {"bug": 0, "feature": 0, "improvement": 0, "compliment": 0, "other": 0}
        for entry in self.data:
            category = entry.get("category", "other")
            distribution[category] = distribution.get(category, 0) + 1
        return distribution

    def get_keyword_frequency(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Get most frequent keywords in feedback descriptions.

        Args:
            top_n: Number of top keywords to return

        Returns:
            List of keywords with frequencies
        """
        keyword_counts = {}

        for entry in self.data:
            description = entry.get("description", "").lower()
            # Extract words (4+ characters)
            words = re.findall(r'\b\w{4,}\b', description)

            for word in words:
                # Skip common stop words
                if word in ["this", "that", "very", "just", "also", "could", "would"]:
                    continue
                keyword_counts[word] = keyword_counts.get(word, 0) + 1

        # Sort by frequency
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)

        return [{"keyword": k, "frequency": v} for k, v in sorted_keywords[:top_n]]

    def get_avg_response_time(self) -> Optional[float]:
        """Calculate average response time if responses are tracked.

        Returns:
            Average time in hours or None
        """
        # Placeholder - would track when feedback is resolved
        return None

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analytics report.

        Returns:
            Dictionary with all analytics data
        """
        return {
            "page_views": self.get_page_views(),
            "feedback_trends": self.get_feedback_trends(),
            "priority_distribution": self.get_priority_distribution(),
            "category_distribution": self.get_category_distribution(),
            "top_keywords": self.get_keyword_frequency(),
            "total_feedback": len(self.data),
            "generated_at": datetime.utcnow().isoformat()
        }


# Global instance
analytics = FeedbackAnalytics()
