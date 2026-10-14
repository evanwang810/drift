#!/usr/bin/env python3
"""
Test suite for search functionality.
Tests that search works correctly on the website.
"""

import os
import sys

# Add site directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'site'))


def test_search_index_exists():
    """Test that search index exists."""
    print("Testing search index exists...")
    search_index_path = 'site/search_index.json'

    if os.path.exists(search_index_path):
        print(f"  ✓ Search index exists at {search_index_path}")
        return True
    else:
        print(f"  ✗ Search index not found at {search_index_path}")
        return False


def test_search_page_exists():
    """Test that search page exists."""
    print("\nTesting search page exists...")
    search_page_path = 'html/search.html'

    if os.path.exists(search_page_path):
        print(f"  ✓ Search page exists at {search_page_path}")
        return True
    else:
        print(f"  ✗ Search page not found at {search_page_path}")
        return False


def test_search_page_has_search_interface():
    """Test that search page has search interface."""
    print("\nTesting search page has search interface...")

    search_page_path = 'html/search.html'
    if not os.path.exists(search_page_path):
        print(f"  ✗ Search page not found")
        return False

    with open(search_page_path, 'r') as f:
        content = f.read()

    checks = [
        ('search box', '<input'),
        ('search button', 'Search'),
        ('search results area', 'results'),
        ('JavaScript search', 'searchIndex'),
    ]

    results = []
    for check_name, check_str in checks:
        has_check = check_str in content
        results.append((check_name, has_check))
        print(f"  {'✓' if has_check else '✗'} {check_name}")

    return all(result[1] for result in results)


def test_knowledge_base_filtering():
    """Test that knowledge base has filtering functionality."""
    print("\nTesting knowledge base filtering...")

    kb_path = 'html/knowledge.html'
    if not os.path.exists(kb_path):
        print(f"  ✗ Knowledge base page not found")
        return False

    with open(kb_path, 'r') as f:
        content = f.read()

    checks = [
        ('Type filter buttons', 'type-btn'),
        ('Tag checkboxes', 'tag-checkbox'),
        ('Search input', 'filter-input'),
        ('Sort dropdown', 'sort-select'),
        ('Statistics display', 'stats'),
    ]

    results = []
    for check_name, check_str in checks:
        has_check = check_str in content
        results.append((check_name, has_check))
        print(f"  {'✓' if has_check else '✗'} {check_name}")

    return all(result[1] for result in results)


def test_metrics_dashboard():
    """Test that metrics dashboard exists and has visualizations."""
    print("\nTesting metrics dashboard...")

    metrics_path = 'html/metrics.html'
    if not os.path.exists(metrics_path):
        print(f"  ✗ Metrics page not found")
        return False

    with open(metrics_path, 'r') as f:
        content = f.read()

    checks = [
        ('Overview stats', 'overview'),
        ('Token trends', 'token'),
        ('Success rate', 'success'),
        ('Completion tracking', 'completion'),
        ('Charts or graphs', 'chart') or ('visualizations', 'visual'),
    ]

    results = []
    for check_name, check_str in checks:
        has_check = check_str in content
        results.append((check_name, has_check))
        print(f"  {'✓' if has_check else '✗'} {check_name}")

    return all(result[1] for result in results)


def main():
    """Run all search and functionality tests."""
    print("=" * 60)
    print("SEARCH AND FUNCTIONALITY TESTING")
    print("=" * 60)

    results = {
        'Search Index': test_search_index_exists(),
        'Search Page': test_search_page_exists(),
        'Search Interface': test_search_page_has_search_interface(),
        'Knowledge Base Filtering': test_knowledge_base_filtering(),
        'Metrics Dashboard': test_metrics_dashboard(),
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
