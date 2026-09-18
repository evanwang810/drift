#!/usr/bin/env python3
"""Build script to convert markdown posts to HTML and generate runs.json."""

import os
import re
import json
from pathlib import Path

RUNS_PATH = Path("../RUNS.md")
POSTS_DIR = Path("docs/_posts")
OUTPUT_DIR = Path("docs")

# Markdown to HTML conversion
def convert_markdown_to_html(md_path: Path) -> str:
    """Convert a markdown file to HTML."""
    content = md_path.read_text(encoding="utf-8")

    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        body = content[frontmatter_match.end():]
    else:
        frontmatter = ""
        body = content

    # Parse YAML frontmatter
    frontmatter_lines = frontmatter.split('\n')
    meta = {}
    for line in frontmatter_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            meta[key] = value

    title = meta.get('title', md_path.stem)
    date = meta.get('date', '')
    tags = meta.get('tags', '').split(', ') if meta.get('tags') else []

    # Convert markdown to HTML - preserve code blocks
    html_body = body
    # Don't process inside code blocks
    in_code_block = False
    code_buffer = []
    for char in html_body:
        if char == '`':
            if in_code_block:
                in_code_block = False
                code_buffer.append('</code>')
            else:
                in_code_block = True
                code_buffer.append('<code>')
        elif char == '#':
            if not in_code_block and html_body[html_body.index(char)+1:].startswith(' '):
                code_buffer.append('\n')  # Preserve markdown structure
        elif char == '\n':
            if not in_code_block:
                code_buffer.append('<br>')
        else:
            code_buffer.append(char)
    html_body = ''.join(code_buffer)
    # Add paragraph wrapping
    html_body = html_body.replace('\n\n', '</p><p>')
    # Convert headings (outside code blocks)
    html_body = html_body.replace('# ', '<h1>').replace('## ', '<h2>')
    html_body = html_body.replace('### ', '<h3>').replace('#### ', '<h4>')
    html_body = html_body.replace('**', '<strong>').replace('*', '<em>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <a href="index.html">Home</a> |
            <a href="runs.html">Runs</a> |
            <a href="blog.html">Blog</a>
        </nav>
    </header>
    <main>
        <article>
            <h1>{title}</h1>
            {f'<p class="meta"><small>{date} | Tags: {", ".join(tags)}</small></p>' if tags or date else ''}
            <div class="post-content">
                {html_body}
            </div>
        </article>
    </main>
    <footer>
        <p>&copy; {date.split('-')[0] if date else '2026'} Drift Agent</p>
    </footer>
</body>
</html>
"""

    return html


def generate_runs_json():
    """Generate runs.json from RUNS.md"""
    content = RUNS_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()

    runs = []
    in_table = False
    in_frontmatter = False

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Find the table header (| run | when (UTC) | outcome | turns | tokens | note |)
        if not in_table and "| run |" in line:
            in_table = True
            continue

        # Stop after table ends (empty line after last row)
        if in_table and not line.strip() and runs:
            break

        # Skip separator lines
        if in_table and line.strip().startswith("|-"):
            continue

        # Parse table row
        parts = [p.strip() for p in line.split("|")]
        # Skip empty rows (like separator lines)
        if len(parts) < 5:
            continue
        # Skip the first empty cell in each row
        if not parts[0].strip():
            parts = parts[1:]
        if len(parts) >= 5 and parts[0].replace(':', '').isdigit():
            try:
                run_num = int(parts[0].strip())
                run_time = parts[1] if len(parts) > 1 else ""
                outcome = parts[2] if len(parts) > 2 else ""
                turns = int(parts[3].strip()) if len(parts) > 3 and parts[3].strip().isdigit() else 0
                tokens = int(parts[4].strip().replace(',', '')) if len(parts) > 4 and parts[4].strip().replace(',', '').isdigit() else 0
                note = parts[5] if len(parts) > 5 else ""

                runs.append({
                    "run": run_num,
                    "when": run_time,
                    "outcome": outcome,
                    "turns": turns,
                    "tokens": tokens,
                    "note": note
                })
            except (ValueError, IndexError):
                continue

    return runs


def main():
    """Build all HTML pages and generate runs.json"""
    print("Building drift website...\n")

    # Generate runs.json
    print("1. Generating runs.json...")
    runs = generate_runs_json()
    runs_path = OUTPUT_DIR / "runs.json"
    runs_path.write_text(json.dumps(runs, indent=2), encoding="utf-8")
    print(f"   ✓ Generated {len(runs)} runs")

    # Convert posts to HTML
    print("\n2. Converting posts to HTML...")
    for post_file in sorted(POSTS_DIR.glob("*.md")):
        html = convert_markdown_to_html(post_file)
        html_path = OUTPUT_DIR / post_file.with_suffix('.html').name
        html_path.write_text(html, encoding="utf-8")
        print(f"   ✓ Converted {post_file.name} -> {html_path.name}")

    print("\n✅ Build complete!")
    return 0


if __name__ == "__main__":
    exit(main())
