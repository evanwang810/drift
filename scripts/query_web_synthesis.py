#!/usr/bin/env python3
"""
Web Synthesis Query Interface

Query and retrieve synthesized web content from the knowledge store.
"""

import argparse
import json
from pathlib import Path
from web_synthesis_store import WebSynthesisStore


class WebSynthesisQueryInterface:
    """Query interface for web synthesis knowledge store."""

    def __init__(self, store_dir='data/web_synthesis'):
        self.store = WebSynthesisStore(store_dir)

    def search(self, query, limit=10):
        """Search entries by query string."""
        results = self.store.search(query, limit)
        return results

    def search_by_tag(self, tag, limit=10):
        """Get entries by tag."""
        results = self.store.get_by_tag(tag, limit)
        return results

    def search_all_tags(self, limit=20):
        """Get all unique tags."""
        tags = set()
        for entry in self.store.get_all(limit=None):
            tags.update(entry['tags'])
        return sorted(list(tags))[:limit]

    def get_entry(self, entry_id):
        """Get a specific entry."""
        return self.store.get_entry(entry_id)

    def display_results(self, results, format='human'):
        """Display query results."""
        if format == 'human':
            print(f"\n{'='*60}")
            print(f"Found {len(results)} result(s)\n")
            print('='*60 + '\n')

            for i, entry in enumerate(results, 1):
                print(f"{i}. {entry['title']}")
                print(f"   URL: {entry['url']}")
                print(f"   Tags: {', '.join(entry['tags'])}")
                print(f"   Summary: {entry['summary']}")
                print(f"   Source: {entry['source_type']}")
                print(f"   Created: {entry['created_at']}\n")

        elif format == 'json':
            print(json.dumps(results, indent=2, ensure_ascii=False))

    def get_statistics(self):
        """Get store statistics."""
        return self.store.get_stats()

    def export_all(self, output_file='data/web_synthesis/query_results.json'):
        """Export all entries to JSON."""
        results = self.store.get_all(limit=None)
        output_path = Path(output_file)

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"Exported {len(results)} entries to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Query web synthesis knowledge store'
    )
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--tag', help='Filter by tag')
    parser.add_argument('--limit', type=int, default=10,
                       help='Maximum results to return')
    parser.add_argument('--format', choices=['human', 'json'],
                       default='human', help='Output format')
    parser.add_argument('--export', '-e', help='Export results to JSON file')
    parser.add_argument('--stats', action='store_true',
                       help='Show store statistics')
    parser.add_argument('--tags', action='store_true',
                       help='List all available tags')

    args = parser.parse_args()

    interface = WebSynthesisQueryInterface()

    if args.stats:
        stats = interface.get_statistics()
        print(f"Total entries: {stats['total_entries']}")
        print(f"Last updated: {stats['last_updated']}")
        print(f"Sources: {stats['sources']}")

    elif args.tags:
        tags = interface.search_all_tags()
        print("Available tags:")
        for tag in tags:
            print(f"  - {tag}")

    elif args.tag:
        results = interface.search_by_tag(args.tag, args.limit)
        interface.display_results(results, args.format)

    elif args.query:
        results = interface.search(args.query, args.limit)
        interface.display_results(results, args.format)

    elif args.export:
        interface.export_all(args.export)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
