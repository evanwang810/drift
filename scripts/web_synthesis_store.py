#!/usr/bin/env python3
"""
Web Synthesis Knowledge Store

Store and retrieve synthesized web content in a structured knowledge base.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class WebSynthesisStore:
    """Store and manage synthesized web content."""

    def __init__(self, store_dir='data/web_synthesis'):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)

        self.index_file = self.store_dir / 'index.json'
        self.data_file = self.store_dir / 'entries.json'

        self._load_index()

    def _load_index(self):
        """Load the index of stored entries."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {
                'total': 0,
                'last_updated': None,
                'entries': {}
            }

    def _save_index(self):
        """Save the index."""
        self.index['last_updated'] = datetime.now().isoformat()
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def add_entry(self, url, title, summary, source_type='web', tags=None,
                  metadata=None, content=None):
        """Add a new synthesized entry."""
        if tags is None:
            tags = []

        entry_id = f"{source_type}:{hash(url) % 1000000:06d}"

        entry = {
            'id': entry_id,
            'url': url,
            'title': title,
            'summary': summary,
            'source_type': source_type,
            'tags': tags,
            'metadata': metadata or {},
            'content': content or '',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        self.index['entries'][entry_id] = entry
        self.index['total'] += 1
        self._save_index()

        # Save individual entry
        entry_file = self.store_dir / f'{entry_id}.json'
        with open(entry_file, 'w') as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)

        return entry_id

    def search(self, query, limit=10):
        """Search entries by query."""
        query = query.lower()
        results = []

        for entry_id, entry in self.index['entries'].items():
            text = f"{entry['title']} {entry['summary']} {entry['content']}".lower()
            tags = ' '.join(entry['tags']).lower()

            # Calculate relevance score
            relevance = 0
            if query in text:
                relevance += 10
            if query in tags:
                relevance += 5

            # Check tag matches
            for tag in entry['tags']:
                if query in tag.lower():
                    relevance += 3

            if relevance > 0:
                results.append({
                    'entry': entry,
                    'relevance': relevance
                })

        # Sort by relevance and return top results
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return [r['entry'] for r in results[:limit]]

    def get_by_tag(self, tag, limit=10):
        """Get entries by tag."""
        results = []
        for entry in self.index['entries'].values():
            if tag in entry['tags']:
                results.append(entry)
        return results[:limit]

    def get_all(self, limit=100):
        """Get all entries."""
        return list(self.index['entries'].values())[:limit]

    def get_entry(self, entry_id):
        """Get a specific entry."""
        return self.index['entries'].get(entry_id)

    def delete_entry(self, entry_id):
        """Delete an entry."""
        if entry_id in self.index['entries']:
            del self.index['entries'][entry_id]
            self.index['total'] -= 1

            # Delete the file
            entry_file = self.store_dir / f'{entry_id}.json'
            if entry_file.exists():
                entry_file.unlink()

            self._save_index()
            return True
        return False

    def export_to_markdown(self, output_file='data/web_synthesis/index.md'):
        """Export all entries to a markdown file."""
        entries = self.get_all(limit=None)

        with open(output_file, 'w') as f:
            f.write("# Web Synthesis Knowledge Base\n\n")
            f.write(f"Total entries: {len(entries)}\n\n")
            f.write("---\n\n")

            for entry in entries:
                f.write(f"# {entry['title']}\n\n")
                f.write(f"**URL:** {entry['url']}\n\n")
                f.write(f"**Tags:** {', '.join(entry['tags'])}\n\n")
                f.write(f"**Source Type:** {entry['source_type']}\n\n")
                f.write(f"**Created:** {entry['created_at']}\n\n")
                f.write(f"## Summary\n\n")
                f.write(f"{entry['summary']}\n\n")
                f.write("---\n\n")

    def get_stats(self):
        """Get store statistics."""
        stats = {
            'total_entries': self.index['total'],
            'last_updated': self.index['last_updated'],
            'sources': {}
        }

        for entry in self.index['entries'].values():
            source = entry['source_type']
            stats['sources'][source] = stats['sources'].get(source, 0) + 1

        return stats


def main():
    """Test the store."""
    store = WebSynthesisStore()

    # Add test entry
    entry_id = store.add_entry(
        url='https://example.com',
        title='Example Domain',
        summary='This is a simple example page for testing the web synthesis system.',
        source_type='test',
        tags=['example', 'test']
    )

    print(f"Added entry: {entry_id}")

    # Search
    results = store.search('example')
    print(f"Search results: {len(results)}")

    # Get stats
    stats = store.get_stats()
    print(f"Stats: {stats}")

    # Export
    store.export_to_markdown()
    print("Exported to markdown")


if __name__ == '__main__':
    main()
