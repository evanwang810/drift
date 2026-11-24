#!/usr/bin/env python3
"""
Web Information Retrieval and Synthesis System

Main orchestrator for the web synthesis system. Fetches content, extracts
and synthesizes information, and stores it in a structured knowledge base.
"""

import argparse
import json
import sys
from pathlib import Path

from fetch_web_content import WebContentFetcher
from web_synthesis_store import WebSynthesisStore
from query_web_synthesis import WebSynthesisQueryInterface


class WebSynthesisSystem:
    """Main orchestrator for web synthesis system."""

    def __init__(self, store_dir='data/web_synthesis'):
        self.fetcher = WebContentFetcher()
        self.store = WebSynthesisStore(store_dir)
        self.interface = WebSynthesisQueryInterface(store_dir)

    def process_single_url(self, url, tags=None, max_length=500):
        """Process a single URL."""
        print(f"Fetching: {url}")

        result = self.fetcher.fetch_and_process(url)

        if result['status'] == 'success':
            print(f"  ✓ Title: {result['metadata']['title']}")
            print(f"  ✓ Summary: {result['summary'][:100]}...")

            entry_id = self.store.add_entry(
                url=result['metadata']['url'],
                title=result['metadata']['title'],
                summary=result['summary'],
                source_type='web',
                tags=tags or [],
                metadata=result['metadata'],
                content=result['text']
            )

            print(f"  ✓ Stored as: {entry_id}")
            return entry_id
        else:
            print(f"  ✗ Error: {result['error']}")
            return None

    def process_multiple_urls(self, urls, tags=None, max_length=500):
        """Process multiple URLs."""
        results = []
        for url in urls:
            entry_id = self.process_single_url(url, tags, max_length)
            if entry_id:
                results.append(entry_id)
        return results

    def run_query(self, query, limit=10):
        """Run a query against the knowledge base."""
        print(f"\nQuery: '{query}'")
        results = self.interface.search(query, limit)
        self.interface.display_results(results)

    def display_stats(self):
        """Display system statistics."""
        stats = self.interface.get_statistics()
        print("\n" + "="*60)
        print("Web Synthesis System Statistics")
        print("="*60)
        print(f"Total entries: {stats['total_entries']}")
        print(f"Last updated: {stats['last_updated']}")
        print("="*60 + "\n")

    def export_index(self, output_file='data/web_synthesis/index.json'):
        """Export the entire knowledge base index."""
        self.store.export_to_markdown(output_file)


def main():
    parser = argparse.ArgumentParser(
        description='Web Information Retrieval and Synthesis System'
    )
    parser.add_argument('urls', nargs='*', help='One or more URLs to process')
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--tag', help='Filter by tag')
    parser.add_argument('--limit', type=int, default=10,
                       help='Maximum results for query')
    parser.add_argument('--tags', action='store_true',
                       help='List all available tags')
    parser.add_argument('--stats', action='store_true',
                       help='Show system statistics')
    parser.add_argument('--export', '-e', help='Export to JSON file')
    parser.add_argument('--store-dir', default='data/web_synthesis',
                       help='Knowledge store directory')
    parser.add_argument('--max-length', type=int, default=500,
                       help='Maximum summary length in characters')

    args = parser.parse_args()

    system = WebSynthesisSystem(args.store_dir)

    if args.stats:
        system.display_stats()
    elif args.tags:
        tags = system.interface.search_all_tags()
        print("Available tags:")
        for tag in tags:
            print(f"  - {tag}")
    elif args.query:
        system.run_query(args.query, args.limit)
    elif args.export:
        system.export_index(args.export)
    elif args.urls:
        results = system.process_multiple_urls(
            args.urls,
            max_length=args.max_length
        )
        print(f"\nProcessed {len(results)} URLs successfully")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
