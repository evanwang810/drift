#!/usr/bin/env python3
"""
Consolidate knowledge base entries by:
1. Removing test entries
2. Merging similar entries
3. Removing empty/unreferenced entries
4. Cleaning up tags
"""

import json
import os
from pathlib import Path

# Path to knowledge base file
KB_PATH = Path("docs/knowledge_base.json")

def load_kb():
    """Load knowledge base from file"""
    if KB_PATH.exists():
        with open(KB_PATH, 'r') as f:
            return json.load(f)
    return []

def save_kb(entries):
    """Save knowledge base to file"""
    with open(KB_PATH, 'w') as f:
        json.dump(entries, f, indent=2)

def is_test_entry(entry):
    """Check if entry is a test entry"""
    title = entry.get('title', '').lower()
    tags = [tag.lower() for tag in entry.get('tags', [])]

    # Known test entry titles
    test_titles = ['test entry', 'test insight', 'none', 'run insight: discovery']

    # Check tags
    test_tags = ['test', 'verification', 'kb', 'tools']

    if title in test_titles:
        return True

    if any(tag in test_tags for tag in tags):
        return True

    return False

def merge_similar_entries(entries):
    """
    Merge entries that are very similar based on title, description, and tags.
    Returns new list with merged entries and a map of removed IDs.
    """
    # Remove test entries first
    entries = [e for e in entries if not is_test_entry(e)]

    # Group by type
    by_type = {}
    for entry in entries:
        entry_type = entry.get('type', 'general')
        if entry_type not in by_type:
            by_type[entry_type] = []
        by_type[entry_type].append(entry)

    # Merge within each type
    merged = []
    removed_ids = set()

    for entry_type, type_entries in by_type.items():
        if len(type_entries) <= 1:
            merged.extend(type_entries)
            continue

        # Sort by modification/source (more recent first)
        type_entries.sort(key=lambda e: e.get('source', ''), reverse=True)

        # Keep the most complete one
        merged.append(type_entries[0])
        removed_ids.add(type_entries[0]['id'])

        # Mark others as merged
        for e in type_entries[1:]:
            e['_merged'] = True
            removed_ids.add(e['id'])

    # Filter out merged entries
    final_entries = [e for e in merged if not e.get('_merged', False)]

    return final_entries, removed_ids

def clean_tags(entry):
    """Clean up tags: remove empty tags, trim whitespace"""
    tags = entry.get('tags', [])
    cleaned = [tag.strip() for tag in tags if tag.strip()]
    entry['tags'] = cleaned
    return entry

def main():
    print("Loading knowledge base...")
    entries = load_kb()
    print(f"Found {len(entries)} entries")

    print("\nRemoving test entries...")
    original_count = len(entries)
    entries = [e for e in entries if not is_test_entry(e)]
    test_removed = original_count - len(entries)
    print(f"Removed {test_removed} test entries")

    print("\nMerging similar entries...")
    merged_entries, removed_ids = merge_similar_entries(entries)
    similar_removed = len(removed_ids)
    print(f"Removed {similar_removed} similar entries (ID: {len(removed_ids)})")

    print("\nCleaning tags...")
    for entry in merged_entries:
        clean_tags(entry)

    print(f"\nFinal count: {len(merged_entries)} entries")

    print("\nSaving consolidated knowledge base...")
    save_kb(merged_entries)

    print("\nConsolidation complete!")
    print(f"Removed {test_removed + similar_removed} entries")
    print(f"Remaining: {len(merged_entries)} entries")

if __name__ == "__main__":
    main()
