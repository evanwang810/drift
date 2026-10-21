#!/usr/bin/env python3
"""
Test suite for main website pages.
Tests that all main pages exist and have expected content.
"""

import os
import sys


def test_main_pages():
    """Test that all main pages exist and load correctly."""
    pages = [
        'index.html',
        'runs.html',
        'tools.html',
        'metrics.html',
        'knowledge.html',
        'search.html',
        'documentation.html',
    ]

    print("Testing main pages load...")
    results = {}
    for page in pages:
        results[page] = os.path.exists(f'docs/{page}')
        print(f"  {'✓' if results[page] else '✗'} {page}")

    all_pass = all(results.values())
    if all_pass:
        print("\n✓ All main pages load correctly")
    else:
        print("\n✗ Some pages failed to load")
    return all_pass


def test_posts():
    """Test that all posts exist and have correct names."""
    posts_dir = 'docs/_posts'
    posts = os.listdir(posts_dir)

    print(f"\nTesting blog posts ({len(posts)} posts)...")
    results = {}

    for post in posts:
        # Check naming pattern: YYYY-MM-DD-words-with-dashes.md
        has_date = '-' in post and post.count('-') >= 2
        has_extension = post.endswith('.md')
        results[post] = has_date and has_extension
        print(f"  {'✓' if results[post] else '✗'} {post}")

    all_pass = all(results.values())
    if all_pass:
        print("\n✓ All posts have correct naming pattern")
    else:
        print("\n✗ Some posts have incorrect naming")
    return all_pass


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


def main():
    """Run all main page tests."""
    print("=" * 60)
    print("COMPREHENSIVE SITE TESTING")
    print("=" * 60)

    results = {
        'Main Pages': test_main_pages(),
        'Blog Posts': test_posts(),
        'Runs JSON': test_runs_json(),
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
