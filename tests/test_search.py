#!/usr/bin/env python3
"""
Test suite for basic site functionality.
Tests that core site features exist and function correctly.
"""

import os
import sys


def test_site_check():
    """Test that check_site.py passes all validations."""
    print("Testing check_site.py...")
    result = os.system('python site/check_site.py --live > /dev/null 2>&1')
    if result == 0:
        print("  ✓ All check_site.py validations pass")
        return True
    else:
        print("  ✗ Some check_site.py validations fail")
        return False


def test_runs_json():
    """Test that runs.json exists and has correct data."""
    print("\nTesting runs.json...")
    try:
        with open('site/runs.json', 'r') as f:
            runs = json.load(f)
        print(f"  ✓ runs.json exists with {len(runs)} runs")

        # Check for required fields
        if runs and isinstance(runs, list):
            required_fields = ['number', 'date', 'output']
            first_run = runs[0]
            has_fields = all(field in first_run for field in required_fields)
            if has_fields:
                print(f"  ✓ All runs have required fields")
                return True
            else:
                print(f"  ✗ Some runs missing required fields")
                return False
        else:
            print(f"  ✗ runs.json is empty or not a list")
            return False
    except FileNotFoundError:
        print(f"  ✗ runs.json not found")
        return False
    except json.JSONDecodeError:
        print(f"  ✗ runs.json is not valid JSON")
        return False


def test_posts_directory():
    """Test that _posts directory exists and has correct structure."""
    print("\nTesting _posts directory...")
    posts_dir = 'docs/_posts'
    if not os.path.exists(posts_dir):
        print(f"  ✗ _posts directory not found")
        return False

    posts = os.listdir(posts_dir)
    print(f"  ✓ _posts directory exists with {len(posts)} posts")

    # Check naming pattern
    for post in posts:
        has_date = '-' in post and post.count('-') >= 2
        has_extension = post.endswith('.md')
        if not (has_date and has_extension):
            print(f"  ✗ Invalid post name: {post}")
            return False

    print(f"  ✓ All posts have correct naming pattern")
    return True


def main():
    """Run all basic functionality tests."""
    print("=" * 60)
    print("BASIC SITE FUNCTIONALITY TESTING")
    print("=" * 60)

    results = {
        'Site Check': test_site_check(),
        'Runs JSON': test_runs_json(),
        'Posts Directory': test_posts_directory(),
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = '✓ PASS' if passed else '✗ FAIL'
        print(f"{test_name:.<40} {status}")

    all_pass = all(results.values())
    if all_pass:
        print("\n✓ ALL TESTS PASSED")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
