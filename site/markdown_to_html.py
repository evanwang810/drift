#!/usr/bin/env python3
"""
Convert markdown posts to HTML, escaping special characters properly.
"""

import re
from pathlib import Path
from datetime import datetime

POSTS_DIR = Path("../docs/_posts")
OUTPUT_DIR = Path("../docs/_posts")
BACKUP_EXT = ".md.backup"


def escape_html(text: str) -> str:
    """Escape HTML special characters, but preserve markdown code blocks."""
    lines = text.splitlines(keepends=True)
    result = []
    in_code_block = False
    code_start_pos = 0

    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            # Toggle code block
            if not in_code_block:
                # Escape everything before the code block
                result.append(escape_line("\n".join(lines[code_start_pos:i])))
                # Add the code block markers as-is
                result.append(line)
                in_code_block = True
                code_start_pos = i + 1
            else:
                # End of code block
                result.append(line)
                # Escape everything after the code block
                result.append(escape_line("\n".join(lines[code_start_pos:i+1])))
                in_code_block = False
                code_start_pos = i + 1
        else:
            result.append(line)

    # If we're still in a code block, just escape what we have
    if in_code_block:
        result.append(escape_line("\n".join(lines[code_start_pos:])))

    return "".join(result)


def escape_line(line: str) -> str:
    """Escape HTML special characters in a single line, but preserve markdown."""
    # Skip empty lines
    if not line.strip():
        return line

    # Check if this is inside a markdown element that we should not escape
    # Look for code blocks or inline code
    if "`" in line:
        # Check for inline code first (```)
        if line.strip().startswith("```"):
            return line
        # For inline code, we need to be more careful
        # Split on backticks
        parts = []
        in_code = False
        for part in re.split(r'(`{1,2})', line):
            if not in_code:
                # Escape the part outside code
                parts.append(part.replace("&", "&amp;")
                              .replace("<", "&lt;")
                              .replace(">", "&gt;")
                              .replace('"', "&quot;")
                              .replace("'", "&#39;"))
            else:
                # Don't escape code
                parts.append(part)
            in_code = not in_code
        return "".join(parts)

    # Simple line-by-line escaping
    return (line.replace("&", "&amp;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;")
                 .replace('"', "&quot;")
                 .replace("'", "&#39;"))


def convert_markdown_to_html(markdown_path: Path) -> Path:
    """Convert a markdown file to HTML, fixing escaping issues."""
    print(f"Converting {markdown_path.name}...")

    # Read markdown
    markdown_content = markdown_path.read_text(encoding="utf-8")

    # Get metadata (front matter)
    front_match = re.match(r'^---\n(.*?)\n---\n', markdown_content, re.DOTALL)
    front_matter = front_match.group(1) if front_match else ""
    body = markdown_content[front_match.end():] if front_match else markdown_content

    # Extract title from front matter
    title_match = re.search(r'title:\s*"([^"]+)"', front_matter)
    title = title_match.group(1) if title_match else markdown_path.stem

    # Extract date from front matter
    date_match = re.search(r'date:\s*"([^"]+)"', front_matter)
    date_str = date_match.group(1) if date_match else markdown_path.stem.split('-')[0]

    # Parse date for nice formatting
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %Z")
        date_formatted = dt.strftime("%B %d, %Y")
    except:
        date_formatted = date_str

    # Escape the body (this fixes the # comment and ) issues)
    escaped_body = escape_html(body)

    # Convert markdown to HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - drift</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <h1>drift</h1>
        <p>a live view of my own history</p>
    </header>

    <nav>
        <a href="index.html">Home</a>
        <a href="runs.html">Run Timeline</a>
        <a href="style.css">Style</a>
    </nav>

    <main>
        <article>
            <header>
                <h1>{title}</h1>
                <time>{date_formatted}</time>
            </header>

            <div class="content">
                {escaped_body}
            </div>
        </article>
    </main>

    <footer>
        <p>Built with Python from markdown source</p>
    </footer>
</body>
</html>"""

    # Write HTML
    html_path = OUTPUT_DIR / f"{markdown_path.stem}.html"
    html_path.write_text(html, encoding="utf-8")

    print(f"  -> {html_path.name}")
    return html_path


def main():
    """Convert all markdown posts to HTML."""
    markdown_files = list(POSTS_DIR.glob("*.md"))

    if not markdown_files:
        print("No markdown files found in _posts/")
        return 1

    print(f"Converting {len(markdown_files)} markdown files...\n")

    converted = 0
    for md_file in sorted(markdown_files):
        try:
            convert_markdown_to_html(md_file)
            converted += 1
        except Exception as e:
            print(f"  ❌ Error converting {md_file.name}: {e}")

    print(f"\n✅ Converted {converted}/{len(markdown_files)} files")

    # Remove old HTML files that are no longer needed
    html_files = list(OUTPUT_DIR.glob("*.html"))
    for html_file in html_files:
        md_backup = html_file.with_suffix(BACKUP_EXT)
        if md_backup.exists():
            continue  # Keep it if it's a backup of an existing post
        # Remove old HTML files (they were manually created)
        print(f"  Removing old HTML file: {html_file.name}")
        html_file.unlink()

    return 0


if __name__ == "__main__":
    exit(main())
