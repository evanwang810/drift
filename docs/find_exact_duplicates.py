#!/usr/bin/env python3
"""
Find exact duplicate entries in knowledge base.
"""

import json
from collections import defaultdict

def load_knowledge_base():
    """Load knowledge_base.json"""
    with open('docs/knowledge_base.json', 'r') as f:
        return json.load(f)

def normalize_entry(entry):
    """Normalize entry for comparison"""
    return {
        'title': entry['title'].lower().strip(),
        'tags': normalize_tags(entry['tags']),
        'description': entry['description'].lower().strip(),
        'type': entry['type'].lower(),
        'source': entry['source'].lower()
    }

def find_exact_duplicates(entries):
    """Find entries with identical normalized content"""
    normalized = {}
    duplicates = []

    for entry in entries:
        norm = normalize_entry(entry)

        # Create a key from title and tags
        key = (norm['title'], tuple(norm['tags']), norm['type'], norm['description'])

        if key in normalized:
            # Found a duplicate
            duplicates.append((normalized[key], entry))
        else:
            normalized[key] = entry

    return duplicates

def main():
    entries = load_knowledge_base()
    print(f"Total entries: {len(entries)}")

    duplicates = find_exact_duplicates(entries)

    print(f"\nFound {len(duplicates)} exact duplicate pairs")

    for i, (entry1, entry2) in enumerate(duplicates, 1):
        print(f"\nDuplicate #{i}:")
        print(f"  Title: {entry1['title']}")
        print(f"  ID 1: {entry1['id']}, ID 2: {entry2['id']}")
        print(f"  Type: {entry1['type']}")
        print(f"  Tags: {', '.join(entry1['tags'])}")
        print(f"  Source 1: {entry1['source']}, Source 2: {entry2['source']}")

if __name__ == '__main__':
    main()
