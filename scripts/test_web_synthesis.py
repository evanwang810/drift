#!/usr/bin/env python3
"""
Test script for Web Information Retrieval and Synthesis System.

Tests the system with 3-5 different web sources and verifies extraction quality.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from web_synthesis_orchestrator import WebSynthesisSystem


def test_system():
    """Test the web synthesis system with various sources."""
    system = WebSynthesisSystem()

    print("Testing Web Information Retrieval and Synthesis System")
    print("=" * 60)

    # Test URLs - diverse sources to test extraction quality
    test_urls = [
        {
            'url': 'https://example.com',
            'tags': ['test', 'example', 'basic'],
            'description': 'Basic example page for testing'
        },
        {
            'url': 'https://www.python.org',
            'tags': ['programming', 'python', 'language'],
            'description': 'Official Python website'
        },
        {
            'url': 'https://wikipedia.org',
            'tags': ['wikipedia', 'reference', 'encyclopedia'],
            'description': 'Wikipedia main page'
        }
    ]

    print("\nProcessing test URLs:")
    print("-" * 60)

    processed = []
    for i, test in enumerate(test_urls, 1):
        print(f"\n{i}. Testing: {test['url']}")
        print(f"   Description: {test['description']}")
        print(f"   Expected tags: {', '.join(test['tags'])}")

        entry_id = system.process_single_url(
            test['url'],
            tags=test['tags']
        )

        if entry_id:
            entry = system.store.get_entry(entry_id)
            if entry:
                print(f"   ✓ Title: {entry['title']}")
                print(f"   ✓ Tags: {', '.join(entry['tags'])}")
                print(f"   ✓ Summary length: {len(entry['summary'])} chars")
                processed.append(entry_id)

    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)

    # Verify extraction quality
    print(f"\n✓ Successfully processed {len(processed)}/{len(test_urls)} URLs")

    if processed:
        # Test query functionality
        print("\n" + "-" * 60)
        print("Testing Query Functionality:")
        print("-" * 60)

        queries = [
            ('python', 'Python programming language'),
            ('example', 'Example pages'),
            ('wikipedia', 'Wikipedia reference')
        ]

        for query, expected in queries:
            results = system.run_query(query, limit=5)
            if results:
                print(f"  ✓ Query '{query}': Found {len(results)} result(s)")
                print(f"    (Expected: {expected})")
            else:
                print(f"  ✗ Query '{query}': No results found")

        # Test statistics
        print("\n" + "-" * 60)
        print("System Statistics:")
        print("-" * 60)

        stats = system.display_stats()

        # Test tag listing
        print("\n" + "-" * 60)
        print("Available Tags:")
        print("-" * 60)

        tags = system.interface.search_all_tags()
        for tag in tags:
            count = len(system.store.get_by_tag(tag))
            print(f"  - {tag}: {count} entry(s)")

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

    # Return success if we processed at least 2 URLs
    return len(processed) >= 2


def run_quality_check():
    """Run quality checks on extracted content."""
    system = WebSynthesisSystem()

    print("\nRunning Quality Checks")
    print("=" * 60)

    checks_passed = 0
    checks_total = 4

    # Check 1: All entries have titles
    entries = system.store.get_all(limit=None)
    if entries:
        title_count = sum(1 for e in entries if e['title'])
        if title_count == len(entries):
            print(f"✓ Check 1: All entries have titles ({len(entries)}/{len(entries)})")
            checks_passed += 1
        else:
            print(f"✗ Check 1: Missing titles ({title_count}/{len(entries)})")
    else:
        print("✗ Check 1: No entries in store")

    # Check 2: Entries have summaries
    if entries:
        summary_count = sum(1 for e in entries if e['summary'])
        if summary_count == len(entries):
            print(f"✓ Check 2: All entries have summaries ({len(entries)}/{len(entries)})")
            checks_passed += 1
        else:
            print(f"✗ Check 2: Missing summaries ({summary_count}/{len(entries)})")
    else:
        print("✗ Check 2: No entries in store")

    # Check 3: Entries have URLs
    if entries:
        url_count = sum(1 for e in entries if e['url'])
        if url_count == len(entries):
            print(f"✓ Check 3: All entries have URLs ({len(entries)}/{len(entries)})")
            checks_passed += 1
        else:
            print(f"✗ Check 3: Missing URLs ({url_count}/{len(entries)})")
    else:
        print("✗ Check 3: No entries in store")

    # Check 4: Store index is up to date
    stats = system.store.get_stats()
    if stats['total_entries'] == len(entries):
        print(f"✓ Check 4: Index matches data ({stats['total_entries']}/{stats['total_entries']})")
        checks_passed += 1
    else:
        print(f"✗ Check 4: Index mismatch ({stats['total_entries']} vs {len(entries)})")

    print("\n" + "=" * 60)
    print(f"Quality Checks: {checks_passed}/{checks_total} passed")
    print("=" * 60)

    return checks_passed == checks_total


if __name__ == '__main__':
    success = test_system()

    print("\n" + "=" * 60)
    print("End-to-End Test Results")
    print("=" * 60)

    quality_passed = run_quality_check()

    if success and quality_passed:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed")
        sys.exit(1)
