#!/usr/bin/env python3
"""
Knowledge Base Consolidation Script

This script identifies and consolidates duplicate or highly similar entries in the knowledge base.
"""

import json
import hashlib
from collections import defaultdict
from difflib import SequenceMatcher

def calculate_similarity(str1, str2):
    """Calculate string similarity using SequenceMatcher."""
    return SequenceMatcher(None, str1, str2).ratio()

def normalize_tags(tags):
    """Normalize tags by lowercasing and removing extra whitespace."""
    return sorted([tag.strip().lower() for tag in tags if tag.strip()])

def find_duplicates(knowledge_base):
    """Find duplicate entries in the knowledge base."""
    entries_by_hash = defaultdict(list)
    entries_by_title = defaultdict(list)
    similar_entries = []

    for entry in knowledge_base:
        # Create a hash based on title and normalized tags
        title = entry.get('title', '').lower().strip()
        normalized_tags = normalize_tags(entry.get('tags', []))

        # Create a composite signature
        signature = f"{title}|{'|'.join(normalized_tags)}"

        # Hash the signature
        sig_hash = hashlib.md5(signature.encode()).hexdigest()

        entries_by_hash[sig_hash].append(entry)
        entries_by_title[title].append(entry)

    # Find duplicates by hash (exact or near-exact matches)
    duplicates_by_hash = {
        hash_val: entries for hash_val, entries in entries_by_hash.items()
        if len(entries) > 1
    }

    # Find similar entries by title
    similar_by_title = {}
    for title, entries in entries_by_title.items():
        if len(entries) > 1:
            similar_by_title[title] = entries

    return duplicates_by_hash, similar_by_title

def analyze_duplicates(knowledge_base):
    """Analyze the knowledge base for duplicates and generate a report."""
    duplicates_by_hash, similar_by_title = find_duplicates(knowledge_base)

    print(f"\n=== Knowledge Base Analysis ===")
    print(f"Total entries: {len(knowledge_base)}")
    print(f"Exact duplicate groups (by hash): {len(duplicates_by_hash)}")
    print(f"Similar title groups: {len(similar_by_title)}")

    # Report exact duplicates
    if duplicates_by_hash:
        print(f"\n=== Exact Duplicates Found ===")
        total_duplicate_count = 0
        for hash_val, entries in duplicates_by_hash.items():
            if len(entries) > 1:
                print(f"\nGroup (hash: {hash_val[:8]}...): {len(entries)} entries")
                for i, entry in enumerate(entries, 1):
                    print(f"  {i}. {entry['title']} (ID: {entry['id']})")
                    print(f"     Type: {entry.get('type', 'N/A')}")
                    print(f"     Source: {entry.get('source', 'N/A')}")
                total_duplicate_count += len(entries)

        print(f"\nTotal entries in duplicate groups: {total_duplicate_count}")
        print(f"Would be reduced to: {len(knowledge_base) - total_duplicate_count}")

    # Report similar entries
    if similar_by_title:
        print(f"\n=== Similar Title Groups ===")
        for title, entries in list(similar_by_title.items())[:10]:  # Show first 10
            if len(entries) > 1:
                print(f"\nTitle: '{title}' ({len(entries)} entries)")
                for i, entry in enumerate(entries, 1):
                    print(f"  {i}. {entry['id']} - Source: {entry.get('source', 'N/A')}")

    return duplicates_by_hash, similar_by_title

def main():
    # Load knowledge base
    kb_path = '.local/state/knowledge_base.json'
    try:
        with open(kb_path, 'r') as f:
            knowledge_base = json.load(f)
    except FileNotFoundError:
        print(f"Error: {kb_path} not found")
        return

    # Analyze
    duplicates_by_hash, similar_by_title = analyze_duplicates(knowledge_base)

    # Print recommendations
    print(f"\n=== Recommendations ===")
    if duplicates_by_hash:
        print("1. Merge exact duplicates into single entries")
        print(f"   - Will reduce total entries from {len(knowledge_base)} to approximately {len(knowledge_base) - len([e for group in duplicates_by_hash.values() for e in group])}")
    if similar_by_title:
        print("2. Review and merge similar title entries")
        print("   - Some entries have very similar titles but different content")

if __name__ == '__main__':
    main()
