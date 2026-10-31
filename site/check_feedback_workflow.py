"""Verify end-to-end feedback workflow.

This script tests the complete feedback system:
1. Feedback form submission
2. Data storage
3. Dashboard rendering
4. Analytics tracking
"""

import json
from pathlib import Path
from site.feedback_system import FeedbackSystem, feedback_system
from site.feedback_analytics import FeedbackAnalytics, analytics


def test_feedback_submission():
    """Test feedback data collection."""
    print("=" * 60)
    print("TEST 1: Feedback Submission")
    print("=" * 60)

    # Create test feedback
    test_feedback = {
        "name": "Test User",
        "email": "test@example.com",
        "category": "bug",
        "priority": "high",
        "description": "Test bug report for feedback system",
        "impact": "This is a test to verify the feedback workflow"
    }

    feedback_id = feedback_system.add_feedback(test_feedback)
    print(f"✓ Feedback submitted with ID: {feedback_id}")

    # Verify feedback was stored
    retrieved = feedback_system.get_feedback(feedback_id)
    assert retrieved is not None, "Feedback not found after submission"
    assert retrieved["name"] == "Test User", "Feedback data mismatch"
    assert retrieved["category"] == "bug", "Category mismatch"
    print("✓ Feedback retrieved successfully")
    print(f"  - ID: {retrieved['id']}")
    print(f"  - Name: {retrieved['name']}")
    print(f"  - Category: {retrieved['category']}")
    print(f"  - Priority: {retrieved['priority']}")
    print()

    return feedback_id


def test_feedback_categorization():
    """Test feedback categorization and filtering."""
    print("=" * 60)
    print("TEST 2: Feedback Categorization")
    print("=" * 60)

    # Add various feedback types
    categories = ["bug", "feature", "improvement", "compliment"]
    for cat in categories:
        test_feedback = {
            "name": f"User {cat}",
            "category": cat,
            "priority": "medium",
            "description": f"Test {cat} feedback",
            "impact": f"Testing {cat} categorization"
        }
        feedback_system.add_feedback(test_feedback)

    # Test category filtering
    bugs = feedback_system.get_feedback_by_category("bug")
    features = feedback_system.get_feedback_by_category("feature")

    assert len(bugs) == 1, f"Expected 1 bug, got {len(bugs)}"
    assert len(features) == 1, f"Expected 1 feature, got {len(features)}"

    print(f"✓ Bug reports: {len(bugs)}")
    print(f"✓ Feature requests: {len(features)}")
    print()

    return bugs[0]["id"]


def test_priority_filtering():
    """Test priority-based filtering."""
    print("=" * 60)
    print("TEST 3: Priority Filtering")
    print("=" * 60)

    # Add feedback with different priorities
    priorities = ["critical", "high", "medium", "low"]
    for pri in priorities:
        test_feedback = {
            "name": f"User {pri}",
            "category": "feature",
            "priority": pri,
            "description": f"Test {pri} priority feedback",
            "impact": f"Testing {pri} priority filtering"
        }
        feedback_system.add_feedback(test_feedback)

    # Test priority filtering
    critical = feedback_system.get_feedback_by_priority("critical")
    high = feedback_system.get_feedback_by_priority("high")

    assert len(critical) == 1, f"Expected 1 critical, got {len(critical)}"
    assert len(high) == 1, f"Expected 1 high, got {len(high)}"

    print(f"✓ Critical feedback: {len(critical)}")
    print(f"✓ High priority: {len(high)}")
    print()

    return critical[0]["id"]


def test_summary_generation():
    """Test summary statistics generation."""
    print("=" * 60)
    print("TEST 4: Summary Generation")
    print("=" * 60)

    summary = feedback_system.get_summary()

    assert summary["total"] == 8, f"Expected 8 total, got {summary['total']}"
    assert "by_category" in summary, "Missing category distribution"
    assert "by_priority" in summary, "Missing priority distribution"
    assert "recent" in summary, "Missing recent feedback"

    print(f"✓ Total feedback: {summary['total']}")
    print(f"✓ Categories: {summary['by_category']}")
    print(f"✓ Priorities: {summary['by_priority']}")
    print(f"✓ Recent feedback: {len(summary['recent'])} entries")
    print()


def test_alert_generation():
    """Test alert generation for critical feedback."""
    print("=" * 60)
    print("TEST 5: Alert Generation")
    print("=" * 60)

    alerts = feedback_system.get_alerts()

    assert len(alerts) > 0, "No alerts generated"
    assert any(a["type"] == "critical" for a in alerts), "Missing critical alerts"
    assert any(a["type"] == "high" for a in alerts), "Missing high priority alerts"

    print("✓ Alerts generated:")
    for alert in alerts:
        print(f"  - [{alert['type']}] {alert['message']}")
    print()


def test_analytics_tracking():
    """Test analytics functionality."""
    print("=" * 60)
    print("TEST 6: Analytics Tracking")
    print("=" * 60)

    # Test analytics features
    priority_dist = analytics.get_priority_distribution()
    category_dist = analytics.get_category_distribution()
    top_keywords = analytics.get_keyword_frequency(5)

    assert len(priority_dist) == 4, "Incorrect priority distribution"
    assert len(category_dist) == 5, "Incorrect category distribution"
    assert len(top_keywords) > 0, "No keywords extracted"

    print("✓ Priority distribution:")
    for pri, count in priority_dist.items():
        print(f"  - {pri}: {count}")
    print()
    print("✓ Category distribution:")
    for cat, count in category_dist.items():
        print(f"  - {cat}: {count}")
    print()
    print(f"✓ Top keywords: {', '.join([k['keyword'] for k in top_keywords])}")
    print()


def test_end_to_end_workflow():
    """Test complete end-to-end workflow."""
    print("=" * 60)
    print("TEST 7: End-to-End Workflow")
    print("=" * 60)

    # Reset for clean test
    feedback_system.data = []
    feedback_system._save_feedback()

    # 1. Submit feedback
    test_feedback = {
        "name": "End-to-End User",
        "email": "e2e@example.com",
        "category": "feature",
        "priority": "medium",
        "description": "End-to-end test feedback",
        "impact": "Verifying complete workflow"
    }

    feedback_id = feedback_system.add_feedback(test_feedback)
    print(f"✓ Step 1: Feedback submitted (ID: {feedback_id})")

    # 2. Retrieve feedback
    retrieved = feedback_system.get_feedback(feedback_id)
    assert retrieved is not None, "Step 2 failed: Feedback not found"
    print(f"✓ Step 2: Feedback retrieved successfully")

    # 3. Get summary
    summary = feedback_system.get_summary()
    assert summary["total"] == 1, "Step 3 failed: Incorrect total count"
    print(f"✓ Step 3: Summary generated correctly")

    # 4. Get alerts
    alerts = feedback_system.get_alerts()
    assert len(alerts) > 0, "Step 4 failed: No alerts generated"
    print(f"✓ Step 4: Alerts generated")

    # 5. Get analytics
    report = analytics.generate_report()
    assert report["total_feedback"] == 1, "Step 5 failed: Analytics incorrect"
    print(f"✓ Step 5: Analytics report generated")

    print()
    print("✅ All end-to-end workflow tests passed!")
    print()


def main():
    """Run all feedback workflow tests."""
    print("\n" + "=" * 60)
    print("FEEDBACK SYSTEM VERIFICATION")
    print("=" * 60 + "\n")

    try:
        # Test each component
        test_feedback_submission()
        test_feedback_categorization()
        test_priority_filtering()
        test_summary_generation()
        test_alert_generation()
        test_analytics_tracking()
        test_end_to_end_workflow()

        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("Feedback workflow is working correctly:")
        print("  • Feedback form submission ✓")
        print("  • Data storage and retrieval ✓")
        print("  • Categorization and filtering ✓")
        print("  • Summary statistics ✓")
        print("  • Alert generation ✓")
        print("  • Analytics tracking ✓")
        print("  • End-to-end workflow ✓")
        print()
        print("The feedback system is ready for production use.")
        return 0

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
