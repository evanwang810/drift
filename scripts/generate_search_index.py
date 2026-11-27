"""
Generate search index from knowledge base JSON.

This script reads the knowledge base and creates a search index for the enhanced
search engine with faceted search, autocomplete, and relevance scoring.
"""

import json
from pathlib import Path
from datetime import datetime
import re


def extract_keywords(text: str) -> list:
    """Extract keywords from text."""
    # Remove common stopwords
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "must", "shall", "can",
        "need", "dare", "ought", "used", "it", "its", "this", "that", "these",
        "those", "i", "you", "he", "she", "we", "they", "me", "him", "her",
        "us", "them", "my", "your", "his", "her", "our", "their", "mine",
        "yours", "hers", "ours", "theirs", "what", "which", "who", "whom",
        "whose", "where", "when", "why", "how", "all", "each", "every", "both",
        "few", "more", "most", "other", "some", "such", "no", "nor", "not",
        "only", "own", "same", "so", "than", "too", "very", "just", "also",
        "now", "then", "here", "there", "once", "about", "into", "through",
        "during", "before", "after", "above", "below", "between", "under",
        "again", "further", "any", "each", "every", "both", "either", "neither",
        "one", "two", "first", "second", "third", "last", "next", "new", "old",
        "big", "small", "good", "bad", "high", "low", "long", "short"
    }

    # Extract words (lowercase, alphanumeric only)
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())

    # Remove stopwords
    keywords = [w for w in words if w not in stopwords]

    # Keep unique keywords
    keywords = list(set(keywords))

    return keywords


def generate_search_index(knowledge_path: Path, output_path: Path) -> dict:
    """
    Generate search index from knowledge base.

    Args:
        knowledge_path: Path to knowledge base JSON
        output_path: Path to output search index

    Returns:
        Search index dictionary
    """
    # Load knowledge base
    if not knowledge_path.exists():
        print(f"Error: Knowledge base not found at {knowledge_path}")
        return {}

    knowledge = json.loads(knowledge_path.read_text(encoding="utf-8"))
    entries = knowledge.get("entries", [])

    print(f"Processing {len(entries)} entries...")

    search_entries = []
    total_words = 0

    for entry in entries:
        # Build text for search
        text_parts = []

        # Title (highest priority)
        title = entry.get("title") or ""
        text_parts.append(title.lower())

        # Description
        description = entry.get("description") or ""
        if description:
            text_parts.append(description.lower())

        # Implementation details
        implementation = entry.get("implementation") or ""
        if implementation:
            text_parts.append(implementation.lower())

        # Combine all text
        combined_text = " ".join(text_parts)

        # Extract keywords
        keywords = extract_keywords(combined_text)

        # Count words
        word_count = len(combined_text.split())
        total_words += word_count

        # Create search entry
        search_entry = {
            "type": entry.get("type", "unknown"),
            "source": entry.get("source", "unknown"),
            "title": title,
            "description": description,
            "text": combined_text,
            "keywords": keywords,
            "tags": entry.get("tags", []),
            "id": entry.get("id", ""),
            "created_at": entry.get("created_at", "")
        }

        search_entries.append(search_entry)

    # Build search index
    search_index = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat(),
            "total_entries": len(search_entries),
            "total_words": total_words,
            "sources": ["knowledge_base"]
        },
        "entries": search_entries
    }

    # Save search index
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, indent=2, ensure_ascii=False)

    print(f"Search index saved to {output_path}")
    print(f"  Total entries: {len(search_entries)}")
    print(f"  Total words: {total_words}")
    print(f"  Sources: {search_index['metadata']['sources']}")

    return search_index


def main():
    """Generate search index from knowledge base."""
    knowledge_path = Path("docs/search_index.json")
    output_path = Path("docs/search_index.json")

    print("=" * 60)
    print("Generating Search Index")
    print("=" * 60)

    search_index = generate_search_index(knowledge_path, output_path)

    if search_index:
        print("\nSearch index generated successfully!")
        print("\nSample entries:")
        for entry in search_index.get("entries", [])[:3]:
            print(f"  - {entry.get('title', 'Untitled')} ({entry.get('type', 'unknown')})")
    else:
        print("\nError generating search index")


if __name__ == "__main__":
    main()
