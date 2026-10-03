"""Generate a search index from all documentation sources.

Run it from anywhere:   python site/generate_search_index.py
Output: docs/search_index.json
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

def build_search_index() -> dict:
    """Build a search index from all documentation sources."""
    index = {
        "knowledge_base": [],
        "posts": [],
        "runs": [],
        "tools": [],
        "projects": []
    }

    # 1. Load knowledge base
    try:
        kb_file = DOCS / "knowledge_base.json"
        if kb_file.exists():
            knowledge_base = json.loads(kb_file.read_text(encoding="utf-8"))
            for entry in knowledge_base:
                index["knowledge_base"].append({
                    "id": entry.get("id", ""),
                    "title": entry.get("title", ""),
                    "description": entry.get("description", ""),
                    "type": entry.get("type", ""),
                    "tags": entry.get("tags", []),
                    "source": entry.get("source", ""),
                    "url": "knowledge_base.html#k-" + (entry.get("id", "").split("-")[-1] if "-" in entry.get("id", "") else entry.get("id", ""))
                })
    except Exception as e:
        print(f"Error loading knowledge base: {e}")

    # 2. Load blog posts
    posts_dir = DOCS / "_posts"
    if posts_dir.exists():
        for post_file in sorted(posts_dir.glob("*.md")):
            try:
                text = post_file.read_text(encoding="utf-8")
                # Extract front matter
                front_match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
                if front_match:
                    front_matter = front_match.group(1)
                    meta = {}
                    for line in front_matter.splitlines():
                        key, sep, value = line.partition(":")
                        if sep and value.strip():
                            key = key.strip()
                            value = value.strip().strip('"')
                            if key in meta:
                                if isinstance(meta[key], list):
                                    meta[key].append(value)
                                else:
                                    meta[key] = [meta[key], value]
                            else:
                                meta[key] = value
                    title = meta.get("title", post_file.stem)
                    date = meta.get("date", post_file.stem[:10])
                    excerpt = meta.get("excerpt", "")
                    if not excerpt:
                        # Extract body text
                        body = text[front_match.end():]
                        words = re.sub(r"[#*`>\[\]()_]|\\n", " ", body)
                        words = " ".join(words.split())
                        excerpt = words[:200] + ("..." if len(words) > 200 else "")
                else:
                    title = post_file.stem
                    date = post_file.stem[:10]
                    body = text
                    words = re.sub(r"[#*`>\[\]()_]|\\n", " ", body)
                    words = " ".join(words.split())
                    excerpt = words[:200] + ("..." if len(words) > 200 else "")

                index["posts"].append({
                    "title": title,
                    "date": date,
                    "excerpt": excerpt,
                    "url": post_file.stem + ".html"
                })
            except Exception as e:
                print(f"Error processing post {post_file}: {e}")

    # 3. Load run history
    try:
        runs_file = ROOT / "RUNS.md"
        if runs_file.exists():
            text = runs_file.read_text(encoding="utf-8")
            # Parse table
            lines = text.splitlines()
            in_table = False
            for line in lines:
                if line.startswith("| --: |"):
                    in_table = True
                    continue
                if in_table and line.startswith("| --: |"):
                    break  # End of table
                if in_table and line.startswith("|"):
                    cells = [c.strip() for c in line.strip().strip("|").split("|")]
                    if len(cells) >= 6:
                        run_num = cells[0]
                        when = cells[1]
                        outcome = cells[2]
                        turns = cells[3]
                        tokens = cells[4]
                        note = cells[5]
                        # Clean note
                        note = re.sub(r"\s*\(See:.*$", "", note)
                        index["runs"].append({
                            "run": run_num,
                            "when": when,
                            "outcome": outcome,
                            "turns": turns,
                            "tokens": tokens,
                            "note": note,
                            "url": "runs.html"
                        })
    except Exception as e:
        print(f"Error loading run history: {e}")

    # 4. Load tools
    try:
        tools_file = DOCS / "TOOLS.md"
        if tools_file.exists():
            text = tools_file.read_text(encoding="utf-8")
            # Extract tools from the list
            tool_pattern = r'\| (.*?) \| (.*?) \| (.*?) \|'
            matches = re.findall(tool_pattern, text)
            for name, description, real_args in matches:
                # Clean up
                name = name.strip()
                description = description.strip()
                real_args = real_args.strip()
                index["tools"].append({
                    "name": name,
                    "description": description,
                    "arguments": real_args
                })
    except Exception as e:
        print(f"Error loading tools: {e}")

    # 5. Load projects
    try:
        projects_file = DOCS / "projects.md"
        if projects_file.exists():
            text = projects_file.read_text(encoding="utf-8")
            # Extract project names and descriptions
            lines = text.splitlines()
            in_projects = False
            current_project = None
            current_description = []

            for line in lines:
                if line.strip() == "## Projects":
                    in_projects = True
                    continue
                if in_projects and line.strip().startswith("## "):
                    if current_project:
                        index["projects"].append({
                            "name": current_project,
                            "description": " ".join(current_description).strip()
                        })
                    current_project = line.strip()[3:]
                    current_description = []
                elif in_projects and line.strip() and not line.strip().startswith("#"):
                    current_description.append(line.strip())

            # Don't forget the last project
            if current_project and current_description:
                index["projects"].append({
                    "name": current_project,
                    "description": " ".join(current_description).strip()
                })
    except Exception as e:
        print(f"Error loading projects: {e}")

    return index


if __name__ == "__main__":
    print("Building search index...")
    index = build_search_index()
    output_file = DOCS / "search_index.json"
    output_file.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Search index written to {output_file}")
    print(f"  - {len(index['knowledge_base'])} knowledge base entries")
    print(f"  - {len(index['posts'])} posts")
    print(f"  - {len(index['runs'])} runs")
    print(f"  - {len(index['tools'])} tools")
    print(f"  - {len(index['projects'])} projects")
