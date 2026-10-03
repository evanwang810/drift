"""Generate a search index from knowledge base and blog posts.

Run it from anywhere:   python site/generate_search_index.py
"""

import json
import re
from pathlib import Path
from markdown import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
POSTS = DOCS / "_posts"
EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


def front_matter(text: str) -> tuple[dict, str]:
    """Extract front matter and body from markdown."""
    meta: dict = {}
    while True:
        match = re.match(r"\s*---\n(.*?)\n---\n", text, re.S)
        if not match:
            return meta, text
        for line in match.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep and value.strip():
                meta.setdefault(key.strip(), []).append(value.strip().strip('"'))
        text = text[match.end():]
    return meta, text


def read_posts() -> list[dict]:
    """Read all blog posts and extract searchable content."""
    posts = []
    for post_path in sorted(POSTS.glob("*.md"), reverse=True):
        text = post_path.read_text(encoding="utf-8")
        meta, body = front_matter(text)

        # Extract title and content for search
        title = meta.get("title", [post_path.stem])[0] if meta.get("title") else post_path.stem[11:].replace("-", " ")
        heading = re.search(r"^#\s+(.+)$", body, re.M)
        if heading:
            body = body[heading.end():]

        # Clean text for indexing
        clean_text = re.sub(r"[#*`>\[\]()_]|^\d{4}-\d{2}-\d{2}\s*[:.-]?\s*", " ", body)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        # Convert to HTML for search highlighting
        html_content = markdown(body, extensions=EXTENSIONS)

        posts.append({
            "id": post_path.stem,
            "date": post_path.stem[:10],
            "title": title,
            "url": f"{post_path.stem}.html",
            "content": clean_text,
            "html_content": html_content,
            "excerpt": clean_text[:180] + ("..." if len(clean_text) > 180 else "")
        })
    return posts


def read_knowledge_base() -> list[dict]:
    """Read knowledge base entries."""
    try:
        kb = json.loads((DOCS / "knowledge_base.json").read_text(encoding="utf-8"))
        return kb
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def generate_search_index() -> dict:
    """Generate complete search index."""
    posts = read_posts()
    knowledge = read_knowledge_base()

    # Combine all searchable content
    entries = []

    # Add blog posts
    for post in posts:
        entries.append({
            "type": "post",
            "id": post["id"],
            "title": post["title"],
            "url": post["url"],
            "date": post["date"],
            "content": post["content"],
            "html_content": post["html_content"],
            "excerpt": post["excerpt"]
        })

    # Add knowledge base entries
    for entry in knowledge:
        tags = " ".join(entry.get("tags", []))
        entries.append({
            "type": "knowledge",
            "id": entry.get("id", ""),
            "title": entry.get("title", ""),
            "url": f"knowledge_base.html#{entry.get('id', '')}",
            "date": entry.get("source", "")[:10] if entry.get("source") else "",
            "content": f"{entry.get('description', '')} {tags} {entry.get('implementation', '')} {entry.get('impact', '')}",
            "html_content": "",  # Knowledge base is displayed differently
            "excerpt": (entry.get('description', '')[:200] + "...") if entry.get('description') else ""
        })

    return {
        "total": len(entries),
        "generated_at": Path(__file__).stat().st_mtime,
        "entries": entries
    }


def main():
    """Generate and save search index."""
    index = generate_search_index()
    output_path = DOCS / "search_index.json"
    output_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Search index generated: {output_path}")
    print(f"  - {index['total']} total entries")
    print(f"  - {len([e for e in index['entries'] if e['type'] == 'post'])} posts")
    print(f"  - {len([e for e in index['entries'] if e['type'] == 'knowledge'])} knowledge entries")


if __name__ == "__main__":
    main()
