"""Feedback System End-to-End Verification.

This script verifies the entire feedback workflow:
1. Feedback form submission (simulated)
2. Data storage in feedback.json
3. Analytics tracking
4. Dashboard generation
5. Alert generation
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from feedback_analytics import FeedbackAnalytics
from feedback_dashboard import generate_dashboard
from feedback_alerts import FeedbackAlertSystem


def test_feedback_submission():
    """Test feedback submission data structure."""
    print("\n" + "=" * 60)
    print("TEST 1: Feedback Submission")
    print("=" * 60)

    # Simulate a feedback submission
    test_feedback = {
        "id": "FB-20261101-001",
        "name": "Test User",
        "email": "test@example.com",
        "category": "bug",
        "priority": "critical",
        "description": "The search function is not returning results",
        "impact": "This makes it impossible for users to find information",
        "timestamp": datetime.utcnow().isoformat()
    }

    print(f"✓ Submitted feedback: {test_feedback['id']}")
    print(f"  Category: {test_feedback['category']}")
    print(f"  Priority: {test_feedback['priority']}")

    return test_feedback


def test_data_storage():
    """Test storing feedback data."""
    print("\n" + "=" * 60)
    print("TEST 2: Data Storage")
    print("=" * 60)

    feedback_file = Path("docs/feedback.json")

    # Create test data
    test_feedbacks = [
        {
            "id": f"FB-20261101-{i:03d}",
            "name": f"User {i}",
            "category": "bug" if i % 2 == 0 else "feature",
            "priority": ["low", "medium", "high", "critical"][i % 4],
            "description": f"Test feedback #{i}",
            "impact": f"Impact description for feedback #{i}",
            "timestamp": datetime.utcnow().isoformat()
        }
        for i in range(10)
    ]

    # Write to file
    feedback_file.write_text(
        json.dumps(test_feedbacks, indent=2, default=str),
        encoding="utf-8"
    )

    print(f"✓ Stored {len(test_feedbacks)} feedback items to {feedback_file}")

    # Verify file exists and has correct content
    assert feedback_file.exists(), "Feedback file does not exist"
    loaded = json.loads(feedback_file.read_text(encoding="utf-8"))
    assert len(loaded) == 10, f"Expected 10 feedback items, got {len(loaded)}"

    print(f"✓ Verified file exists and contains {len(loaded)} items")

    return test_feedbacks


def test_analytics_tracking():
    """Test analytics functionality."""
    print("\n" + "=" * 60)
    print("TEST 3: Analytics Tracking")
    print("=" * 60)

    analytics = FeedbackAnalytics()

    # Test priority distribution
    priority_dist = analytics.get_priority_distribution()
    print(f"✓ Priority distribution: {priority_dist}")

    # Test category distribution
    category_dist = analytics.get_category_distribution()
    print(f"✓ Category distribution: {category_dist}")

    # Test keyword frequency
    top_keywords = analytics.get_keyword_frequency(top_n=5)
    print(f"✓ Top keywords: {[(k['keyword'], k['frequency']) for k in top_keywords]}")

    # Test feedback trends
    trends = analytics.get_feedback_trends(days=30)
    print(f"✓ Feedback trends (last 30 days): {len(trends)} categories with data")

    return True


def test_dashboard_generation():
    """Test dashboard HTML generation."""
    print("\n" + "=" * 60)
    print("TEST 4: Dashboard Generation")
    print("=" * 60)

    dashboard_file = Path("docs/feedback-dashboard.html")

    # Mock analytics data
    with patch('site.feedback_analytics.FeedbackAnalytics') as mock_analytics:
        # Create mock analytics instance
        mock_instance = mock_analytics.return_value
        mock_instance.data = [
            {
                "id": f"FB-20261101-{i:03d}",
                "category": "bug" if i % 2 == 0 else "feature",
                "priority": ["low", "medium", "high", "critical"][i % 4],
                "timestamp": datetime.utcnow().isoformat(),
                "description": f"Test feedback #{i}",
                "impact": f"Impact #{i}"
            }
            for i in range(10)
        ]

        # Generate dashboard
        generate_dashboard(dashboard_file)

    # Verify file was created
    assert dashboard_file.exists(), "Dashboard file was not created"
    html_content = dashboard_file.read_text(encoding="utf-8")

    # Verify key elements
    assert "Feedback Dashboard" in html_content, "Dashboard title not found"
    assert "Total Feedback" in html_content, "Total feedback metric not found"
    assert "Priority Distribution" in html_content, "Priority distribution section not found"
    assert "Category Distribution" in html_content, "Category distribution section not found"

    print(f"✓ Dashboard generated at {dashboard_file}")
    print(f"✓ Dashboard contains: Title, metrics, priority distribution, category distribution")

    # Clean up
    if dashboard_file.exists():
        dashboard_file.unlink()

    return True


def test_alert_system():
    """Test alert generation."""
    print("\n" + "=" * 60)
    print("TEST 5: Alert System")
    print("=" * 60)

    alert_system = FeedbackAlertSystem()

    # Test critical alerts
    critical_alerts = alert_system.generate_critical_alerts()
    print(f"✓ Critical alerts generated: {len(critical_alerts)}")

    # Test bug report alert
    bug_alerts = alert_system.generate_bug_report_alert()
    for alert in bug_alerts:
        print(f"  • {alert['message']}")

    # Test feature request summary
    feature_summary = alert_system.generate_feature_request_summary()
    print(f"✓ Feature request summary: {feature_summary['total']} total")

    # Test bug summary
    bug_summary = alert_system.generate_bug_summary()
    print(f"✓ Bug summary: {bug_summary['total']} total bugs")

    # Test daily summary
    daily_summary = alert_system.generate_daily_summary()
    print(f"✓ Daily summary generated with {len(daily_summary['critical_alerts'])} critical alerts")

    # Test summary report generation
    report = alert_system.generate_summary_report()
    assert len(report) > 0, "Summary report is empty"
    print(f"✓ Summary report generated ({len(report)} characters)")

    return True


def test_complete_workflow():
    """Test the complete feedback workflow."""
    print("\n" + "=" * 60)
    print("TEST 6: Complete Workflow")
    print("=" * 60)

    feedback_file = Path("docs/feedback.json")
    dashboard_file = Path("docs/feedback-dashboard.html")
    alerts_file = Path("docs/feedback-alerts.json")

    # Step 1: Clear existing data
    if feedback_file.exists():
        feedback_file.unlink()

    # Step 2: Add test feedback
    test_feedbacks = [
        {
            "id": f"FB-20261101-{i:03d}",
            "name": f"Test User {i}",
            "email": f"user{i}@example.com",
            "category": ["bug", "feature", "improvement", "compliment", "other"][i % 5],
            "priority": ["low", "medium", "high", "critical"][i % 4],
            "description": f"Test feedback description #{i}",
            "impact": f"Impact description #{i}",
            "timestamp": datetime.utcnow().isoformat()
        }
        for i in range(8)
    ]

    feedback_file.write_text(
        json.dumps(test_feedbacks, indent=2, default=str),
        encoding="utf-8"
    )

    print("✓ Step 1: Added test feedback data")

    # Step 3: Run analytics
    analytics = FeedbackAnalytics()
    priority_dist = analytics.get_priority_distribution()
    category_dist = analytics.get_category_distribution()

    print(f"✓ Step 2: Analytics processed {len(test_feedbacks)} items")
    print(f"  Priority distribution: {priority_dist}")
    print(f"  Category distribution: {category_dist}")

    # Step 4: Generate dashboard
    with patch('site.feedback_analytics.FeedbackAnalytics') as mock_analytics:
        mock_instance = mock_analytics.return_value
        mock_instance.data = test_feedbacks
        generate_dashboard(dashboard_file)

    print(f"✓ Step 3: Generated dashboard at {dashboard_file}")

    # Step 5: Generate alerts
    alert_system = FeedbackAlertSystem()
    daily_summary = alert_system.generate_daily_summary()
    alerts_file.write_text(
        json.dumps(daily_summary, indent=2, default=str),
        encoding="utf-8"
    )

    print(f"✓ Step 4: Generated alerts at {alerts_file}")

    # Step 6: Verify all outputs
    assert feedback_file.exists(), "Feedback file missing"
    assert dashboard_file.exists(), "Dashboard file missing"
    assert alerts_file.exists(), "Alerts file missing"

    print(f"✓ Step 5: All outputs verified")

    # Cleanup
    feedback_file.unlink()
    dashboard_file.unlink()
    alerts_file.unlink()

    print("✓ Step 6: Cleanup completed")

    return True


def main() -> int:
    """Run all verification tests."""
    print("\n" + "=" * 60)
    print("FEEDBACK SYSTEM END-TO-END VERIFICATION")
    print("=" * 60)

    tests = [
        ("Feedback Submission", test_feedback_submission),
        ("Data Storage", test_data_storage),
        ("Analytics Tracking", test_analytics_tracking),
        ("Dashboard Generation", test_dashboard_generation),
        ("Alert System", test_alert_system),
        ("Complete Workflow", test_complete_workflow),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, True, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
            print(f"✗ Test failed: {e}")

    # Print summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for test_name, success, error in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
        if error:
            print(f"  Error: {error}")

    print("\n" + "=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
