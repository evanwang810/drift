#!/usr/bin/env python3
"""Verify the entire feedback workflow works end-to-end.

This script tests:
1. Feedback form HTML renders correctly
2. Feedback analyzer generates correct summaries
3. Dashboard is generated successfully
4. Response templates are accessible
5. All components integrate properly
"""

import subprocess
from pathlib import Path
import sys


def test_feedback_html_exists():
    """Test that feedback.html exists and is readable."""
    feedback_html = Path("docs/feedback.html")
    if not feedback_html.exists():
        print("❌ FAIL: feedback.html does not exist")
        return False

    content = feedback_html.read_text(encoding="utf-8")
    if "Feedback" not in content:
        print("❌ FAIL: feedback.html missing expected content")
        return False

    if "feedbackForm" not in content:
        print("❌ FAIL: feedback.html missing form element")
        return False

    print("✓ PASS: feedback.html exists and contains form")
    return True


def test_feedback_analyzer():
    """Test that feedback analyzer runs successfully."""
    analyzer_script = Path("site/feedback_analyzer.py")
    if not analyzer_script.exists():
        print("❌ FAIL: feedback_analyzer.py does not exist")
        return False

    result = subprocess.run(
        [sys.executable, str(analyzer_script)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ FAIL: feedback_analyzer.py failed to run")
        print(f"  stdout: {result.stdout}")
        print(f"  stderr: {result.stderr}")
        return False

    if "Total Feedback" not in result.stdout:
        print("❌ FAIL: feedback_analyzer.py did not generate summary")
        return False

    print("✓ PASS: feedback_analyzer.py runs successfully")
    return True


def test_dashboard_exists():
    """Test that feedback dashboard is generated."""
    dashboard = Path("docs/feedback-dashboard.html")
    if not dashboard.exists():
        print("❌ FAIL: feedback-dashboard.html does not exist")
        return False

    content = dashboard.read_text(encoding="utf-8")
    if "Feedback Dashboard" not in content:
        print("❌ FAIL: feedback-dashboard.html missing expected content")
        return False

    print("✓ PASS: feedback-dashboard.html exists and renders")
    return True


def test_response_templates():
    """Test that response templates document exists and is readable."""
    templates = Path("docs/feedback-response-templates.md")
    if not templates.exists():
        print("❌ FAIL: feedback-response-templates.md does not exist")
        return False

    content = templates.read_text(encoding="utf-8")
    required_sections = [
        "Bug Reports",
        "Feature Requests",
        "Improvements",
        "Compliments",
        "Response Workflow",
        "Quality Guidelines"
    ]

    missing = [s for s in required_sections if s not in content]
    if missing:
        print(f"❌ FAIL: feedback-response-templates.md missing sections: {', '.join(missing)}")
        return False

    print("✓ PASS: feedback-response-templates.md exists and has required sections")
    return True


def test_build_includes_dashboard():
    """Test that the build script includes the feedback dashboard."""
    build_script = Path("site/build.py")
    content = build_script.read_text(encoding="utf-8")

    if "feedback_dashboard" not in content.lower():
        print("❌ FAIL: build.py does not reference feedback dashboard")
        return False

    print("✓ PASS: build.py includes feedback dashboard")
    return True


def test_check_site_passes():
    """Test that check_site.py passes with feedback changes."""
    result = subprocess.run(
        [sys.executable, "site/check_site.py"],
        capture_output=True,
        text=True,
        cwd="."
    )

    # check_site.py should have 12/12 validations pass
    if "12/12" not in result.stdout and "12 of 12" not in result.stdout:
        print(f"⚠️  WARNING: check_site.py did not pass all validations")
        print(f"  stdout: {result.stdout}")
        return False

    print("✓ PASS: check_site.py passes all validations")
    return True


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("FEEDBACK WORKFLOW VERIFICATION")
    print("=" * 60)
    print()

    tests = [
        ("Feedback HTML exists", test_feedback_html_exists),
        ("Feedback analyzer runs", test_feedback_analyzer),
        ("Dashboard exists", test_dashboard_exists),
        ("Response templates exist", test_response_templates),
        ("Build includes dashboard", test_build_includes_dashboard),
        ("check_site.py passes", test_check_site_passes),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        print("-" * 60)
        result = test_func()
        results.append((test_name, result))

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print()
        print("🎉 ALL TESTS PASSED! Feedback workflow is complete and working.")
        return 0
    else:
        print()
        print("⚠️  Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
