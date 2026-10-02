"""Generate a search index from knowledge base entries and blog posts.

The index contains searchable text from all sources, with metadata for filtering.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
POSTS = DOCS / "_posts"
KNOWLEDGE_BASE = DOCS / "knowledge_base.json"
INDEX_OUTPUT = DOCS / "search_index.json"


def read_markdown_posts() -> list[dict]:
    """Read all blog posts and extract searchable content."""
    entries = []
    for post_path in sorted(POSTS.glob("*.md")):
        text = post_path.read_text(encoding="utf-8")
        # Extract front matter
        meta_match = re.match(r"^\s*---\n(.*?)\n---\n", text, re.S)
        if not meta_match:
            continue

        meta = {}
        for line in meta_match.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep and value.strip():
                meta.setdefault(key.strip(), []).append(value.strip().strip('"'))

        # Extract body text (after front matter)
        body = text[meta_match.end():]

        # Get title from front matter, or extract from heading
        titles = [t for t in meta.get("title", []) if t != post_path.stem]
        heading = re.search(r"^#\s+(.+)$", body, re.M)
        title = (titles[0] if titles else heading.group(1).strip() if heading
                 else post_path.stem[11:].replace("-", " ").capitalize())

        # Extract excerpt if not in front matter
        if "excerpt" not in meta:
            excerpt_match = re.search(r"^#\s+.+$", body, re.M)
            excerpt = excerpt_match.group(0).strip() if excerpt_match else ""
            excerpt = re.sub(r"\s+", " ", excerpt)[:200]
        else:
            excerpt = " ".join(meta.get("excerpt", []))

        # Get date
        date = meta.get("date", [post_path.stem[:10]])[0]

        entries.append({
            "id": f"post-{post_path.stem}",
            "type": "post",
            "title": title,
            "date": date,
            "excerpt": excerpt,
            "body": body,
            "slug": post_path.stem
        })

    return entries


def read_knowledge_base() -> list[dict]:
    """Read knowledge base entries and extract searchable content."""
    data = json.loads(KNOWLEDGE_BASE.read_text(encoding="utf-8"))
    entries = []

    for item in data:
        # Extract searchable fields
        title = item.get("title", "")
        description = item.get("description", "")
        implementation = item.get("implementation", "")
        verification = item.get("verification", "")
        source = item.get("source", "")
        tags = item.get("tags", [])

        # Combine all text fields
        text = " ".join([
            title, description, implementation, verification,
            source, " ".join(tags)
        ])

        entries.append({
            "id": item.get("id", ""),
            "type": "knowledge",
            "title": title,
            "description": description,
            "tags": tags,
            "type_field": item.get("type", ""),
            "source": source,
            "text": text
        })

    return entries


def build_search_index() -> dict:
    """Build the search index from all sources."""
    print("Reading blog posts...")
    posts = read_markdown_posts()
    print(f"  Found {len(posts)} posts")

    print("Reading knowledge base...")
    knowledge = read_knowledge_base()
    print(f"  Found {len(knowledge)} knowledge entries")

    # Combine all entries
    all_entries = posts + knowledge

    # Create inverted index
    index = {
        "total": len(all_entries),
        "entries": all_entries,
        "last_updated": datetime.now().isoformat()
    }

    # Save index
    INDEX_OUTPUT.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Search index saved to {INDEX_OUTPUT}")

    return index


if __name__ == "__main__":
    build_search_index()
