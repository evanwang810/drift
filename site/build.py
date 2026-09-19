#!/usr/bin/env python3
"""Build script to convert markdown posts to HTML and generate runs.json."""

import os
import re
import json
from pathlib import Path

RUNS_PATH = Path("/home/runner/work/drift/drift/RUNS.md")
POSTS_DIR = Path("/home/runner/work/drift/drift/docs/_posts")
OUTPUT_DIR = Path("/home/runner/work/drift/drift/docs")

def convert_markdown_to_html(md_path: Path) -> str:
    """Convert a markdown file to HTML using proper escaping."""
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

    # Properly escape HTML in the body first
    body = body.replace('&', '&amp;')
    body = body.replace('<', '&lt;')
    body = body.replace('>', '&gt;')

    # Handle code blocks by replacing them with placeholders first
    code_blocks = []

    # Multi-line code blocks (triple backticks)
    lines = body.split('\n')
    processed_lines = []
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                code_blocks.append('')
            else:
                code_blocks[-1] = code_blocks[-1].rstrip('\n')
        elif in_code_block:
            code_blocks[-1] += '\n' + line
        else:
            processed_lines.append(line)

    # Replace multi-line code blocks with placeholders
    for i, code in enumerate(code_blocks):
        placeholder = f'__CODE_BLOCK_{i}__'
        body = body.replace(f'```{code}```', placeholder)

    # Handle inline code blocks (single backticks) - replace after multi-line
    for i, code in enumerate(code_blocks):
        placeholder = f'__CODE_BLOCK_{i}__'
        body = body.replace(f'`{code}`', placeholder)

    # Process markdown elements (but not inside code blocks)
    lines = body.split('\n')
    processed_lines = []
    in_code_block = False
    for line in lines:
        # Check for code block placeholders
        if '__CODE_BLOCK_' in line:
            processed_lines.append(line)
            continue

        # Check for code block markers
        if '```' in line:
            in_code_block = not in_code_block

        # Only process # comments if NOT inside a code block
        if not in_code_block and line.strip().startswith('#'):
            line = f"<!-- {line.strip()} -->"

        # Convert headers
        line = re.sub(r'^# ', '<h1>', line)
        line = re.sub(r'^## ', '<h2>', line)
        line = re.sub(r'^### ', '<h3>', line)
        line = re.sub(r'^#### ', '<h4>', line)

        # Convert bold and italic
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)

        # Convert lists
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            line = '<li>' + line[2:] + '</li>'

        processed_lines.append(line)

    body = '\n'.join(processed_lines)

    # Convert double newlines to paragraph tags
    body = re.sub(r'\n\n', '</p>\n\n<p>', body)

    # Wrap in paragraph if needed
    if body and not body.startswith('<'):
        body = '<p>' + body + '</p>'

    # Restore code blocks (after all other processing)
    for i, code in enumerate(code_blocks):
        if code:
            # Multi-line code block with proper escaping
            code_escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            body = body.replace(f'__CODE_BLOCK_{i}__', f'<pre><code>{code_escaped}</code></pre>')
        else:
            # Inline code block
            body = body.replace(f'__CODE_BLOCK_{i}__', '<code></code>')

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
                {body}
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

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Find the table header (| run | when (UTC) | outcome | turns | tokens | note |)