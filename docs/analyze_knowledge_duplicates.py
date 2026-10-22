#!/usr/bin/env python3
"""
Script to analyze knowledge base for duplicate entries.
Identifies entries with identical titles, tags, and content.
"""

import json
from collections import defaultdict
from difflib import SequenceMatcher

def load_knowledge_base():
    """Load knowledge_base.json"""
    with open('docs/knowledge_base.json', 'r') as f:
        return json.load(f)

def normalize_tags(tags):
    """Normalize tags: lowercase, strip whitespace"""
    return sorted([str(tag).lower().strip() for tag in tags if tag])

def calculate_similarity(entry1, entry2):
    """Calculate similarity between two entries based on title, tags, and description"""
    title_sim = SequenceMatcher(None, entry1['title'].lower(), entry2['title'].lower()).ratio()
    tags_sim = SequenceMatcher(None, ' '.join(normalize_tags(entry1['tags'])),
                              ' '.join(normalize_tags(entry2['tags']))).ratio()
    desc_sim = SequenceMatcher(None, entry1['description'].lower(), entry2['description'].lower()).ratio()

    return (title_sim + tags_sim + desc_sim) / 3

def find_duplicates(entries, threshold=0.85):
    """Find duplicate entries based on similarity"""
    duplicates = []
    used = set()

    for i, entry1 in enumerate(entries):
        if i in used:
            continue

        entry_group = [entry1]
        entry1_id = entry1['id']

        for j, entry2 in enumerate(entries):
            if i >= j or j in used:
                continue

            sim = calculate_similarity(entry1, entry2)
            if sim >= threshold:
                entry_group.append(entry2)
                used.add(j)

        if len(entry_group) > 1:
            duplicates.append(entry_group)

    return duplicates

def analyze_by_title(entries):
    """Group entries by title to find near-duplicates"""
    title_groups = defaultdict(list)

    for entry in entries:
        title_groups[entry['title']].append(entry)

    # Find groups with multiple entries
    duplicates = [group for group in title_groups.values() if len(group) > 1]

    return duplicates

def main():
    entries = load_knowledge_base()
    print(f"Total entries: {len(entries)}")

    # Analyze by title
    print("\n=== Duplicate Titles ===")
    title_duplicates = analyze_by_title(entries)
    for group in title_duplicates[:10]:  # Show first 10
        print(f"\n{group[0]['title']} ({len(group)} entries):")
        for entry in group:
            print(f"  - ID: {entry['id']}, Type: {entry['type']}, Source: {entry['source']}")

    # Find similar entries
    print("\n=== Highly Similar Entries (similarity > 0.9) ===")
    similar_entries = []
    for i, entry1 in enumerate(entries):
        for j, entry2 in enumerate(entries):
            if i >= j:
                continue

            sim = calculate_similarity(entry1, entry2)
            if sim > 0.9:
                similar_entries.append((entry1, entry2, sim))

    for entry1, entry2, sim in sorted(similar_entries, key=lambda x: x[2], reverse=True)[:20]:
        print(f"\nSimilarity: {sim:.2f}")
        print(f"  {entry1['title']} (ID: {entry1['id']})")
        print(f"  {entry2['title']} (ID: {entry2['id']})")

    print(f"\nFound {len(title_duplicates)} duplicate title groups")
    print(f"Found {len(similar_entries)} pairs with similarity > 0.9")

if __name__ == '__main__':
    main()
