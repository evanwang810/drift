#!/usr/bin/env python3
"""
Clean and fix knowledge base data.

Fixes:
- Duplicate entry IDs
- Malformed tags (spaces, long phrases)
- Duplicate entries
- Inconsistent categories
"""

import json
import re
from collections import Counter
from datetime import datetime

def clean_tag(tag):
    """Clean a tag: remove spaces, truncate if too long, convert to lowercase."""
    if not tag:
        return "uncategorized"

    # Remove leading/trailing spaces
    tag = tag.strip()

    # If tag is empty after stripping, return uncategorized
    if not tag:
        return "uncategorized"

    # Replace spaces with hyphens
    tag = re.sub(r'\s+', '-', tag)

    # Truncate if too long (max 50 chars)
    if len(tag) > 50:
        tag = tag[:47] + '...'

    # Convert to lowercase
    tag = tag.lower()

    return tag

def extract_keywords(text):
    """Extract main keywords from text (first few words)."""
    words = re.split(r'\s+', text.strip())
    # Take first 3 words if available
    keywords = words[:3]
    return '-'.join(keywords)

def determine_category(entry):
    """Determine appropriate category for an entry based on type and title."""
    entry_type = entry.get('type', '').lower()
    title = entry.get('title', '').lower()

    # Platform entries
    if 'platform' in title or entry_type == 'platform':
        return 'Platform'

    # Tool fixes and improvements
    if entry_type in ['tool_fix', 'tool_improvement', 'tool_limitation']:
        return 'Tools'

    # Research
    if entry_type == 'research':
        return 'Research'

    # Discoveries
    if entry_type == 'discovery':
        return 'Discoveries'

    # Workflows
    if entry_type == 'workflow':
        return 'Workflows'

    # Default based on title keywords
    if 'documentation' in title:
        return 'Documentation'

    return 'General'

def clean_entry(entry, index):
    """Clean a single entry."""
    title = entry.get('title', '')

    # Remove "Tool/Feature:" prefix from titles if present
    if title.startswith('Tool/Feature:'):
        title = title[len('Tool/Feature:'):]

    # Clean tags
    tags = entry.get('tags', [])
    cleaned_tags = [clean_tag(tag) for tag in tags]
    # Remove duplicates from tags
    cleaned_tags = list(dict.fromkeys(cleaned_tags))  # Preserve order, remove duplicates

    # Determine category
    category = determine_category(entry)

    # Create cleaned entry
    cleaned = {
        'id': f'k-{index:03d}',
        'title': title.strip(),
        'description': entry.get('description', ''),
        'type': entry.get('type', 'general'),
        'tags': cleaned_tags,
        'source': entry.get('source', ''),
        'implementation': entry.get('implementation', ''),
        'verification': entry.get('verification', ''),
        'impact': entry.get('impact', ''),
        'category': category,
        'related_tags': entry.get('related_tags', []),
        'popularity_score': entry.get('popularity_score', 0)
    }

    return cleaned

def deduplicate_entries(entries):
    """Remove duplicate entries."""
    seen = set()
    unique_entries = []

    for entry in entries:
        # Create a fingerprint for deduplication
        title = entry.get('title', '').lower()
        description = entry.get('description', '').lower()
        type_ = entry.get('type', '')

        fingerprint = f"{title}|{description}|{type_}"

        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_entries.append(entry)

    return unique_entries

def main():
    """Main function to clean knowledge base."""
    # Read the knowledge base
    with open('docs/knowledge_base.json', 'r', encoding='utf-8') as f:
        entries = json.load(f)

    print(f"Original entries: {len(entries)}")

    # Deduplicate
    entries = deduplicate_entries(entries)
    print(f"After deduplication: {len(entries)}")

    # Clean each entry
    cleaned_entries = []
    for i, entry in enumerate(entries):
        cleaned = clean_entry(entry, i)
        cleaned_entries.append(cleaned)

    # Write cleaned entries
    with open('docs/knowledge_base.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_entries, f, indent=2, ensure_ascii=False)

    print(f"Cleaned entries: {len(cleaned_entries)}")
    print("Knowledge base cleaned and saved.")

    # Show some statistics
    categories = Counter(entry.get('category', 'uncategorized') for entry in cleaned_entries)
    types = Counter(entry.get('type', 'uncategorized') for entry in cleaned_entries)

    print("\nCategories:")
    for cat, count in categories.most_common():
        print(f"  {cat}: {count}")

    print("\nTypes:")
    for typ, count in types.most_common():
        print(f"  {typ}: {count}")

if __name__ == '__main__':
    main()
