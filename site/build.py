#!/usr/bin/env python3
"""Build script to convert markdown posts to HTML and generate runs.json."""

import os
import re
import json
from pathlib import Path

# Use paths relative to this script
RUNS_PATH = Path(__file__).parent.parent / 'RUNS.md'
POSTS_DIR = Path(__file__).parent.parent / 'docs' / '_posts'
OUTPUT_DIR = Path(__file__).parent.parent / 'docs'

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
            # Only comment out actual comment lines, not headers
            if not line.strip().startswith('##') and not line.strip().startswith('###'):
                line = f"<!-- {line.strip()} -->"

        # Convert headers (but only if they are actual markdown headers, not dates)
        # Only convert # at start of line, and not if it looks like a date pattern
        if line.strip().startswith('# ') and '<h' not in line:
            # Check if it's a date pattern (YYYY-MM-DD) before converting
            date_match = re.match(r'^#\s*(\d{4}-\d{2}-\d{2})', line)
            if not date_match:
                line = re.sub(r'^# ', '<h1>', line)
        if line.strip().startswith('## ') and '<h' not in line:
            line = re.sub(r'^## ', '<h2>', line)
        if line.strip().startswith('### ') and '<h' not in line:
            line = re.sub(r'^### ', '<h3>', line)
        if line.strip().startswith('#### ') and '<h' not in line:
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

    # Create HTML
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
        <h1>{title}</h1>
        {f'<p>{date}</p>' if date else ''}
    </header>
    <main>
        <section class="content">
{body}
        </section>
    </main>
    <footer>
        <p>Built with Python from markdown source</p>
    </footer>
</body>
</html>"""

    return html

def build_posts():
    """Build all markdown posts to HTML"""
    print("Building posts...")
    for md_path in sorted(POSTS_DIR.glob('*.md')):
        html_path = OUTPUT_DIR / f"{md_path.stem}.html"
        html_content = convert_markdown_to_html(md_path)
        html_path.write_text(html_content, encoding='utf-8')
        print(f"  ✓ {md_path.name} -> {html_path.name}")

def build_runs():
    """Parse RUNS.md and generate runs.json"""
    print("Parsing RUNS.md...")
    runs = []
    
    # Check if it's a table format (starts with | run |)
    table_format = False
    with open(RUNS_PATH, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        if first_line.startswith('| run |'):
            table_format = True
    
    if table_format:
        # Parse table format
        with open(RUNS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip header row
                if '|' not in line:
                    continue
                # Split by pipe
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6 and parts[0].isdigit():
                    try:
                        run_num = int(parts[0])
                        runs.append({
                            'run': run_num,
                            'when': parts[1],
                            'outcome': parts[2],
                            'turns': int(parts[3]) if parts[3].replace(',', '').isdigit() else 0,
                            'tokens': int(parts[4].replace(',', '')) if parts[4].replace(',', '').isdigit() else 0,
                            'note': parts[5] if len(parts) > 5 else ''
                        })
                    except (ValueError, IndexError):
                        continue
    else:
        # Parse line-based format
        current_run = None
        with open(RUNS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('## run '):
                    # Save previous run
                    if current_run:
                        runs.append(current_run)
                    # Start new run
                    match = re.match(r'## run (\d+)', line)
                    if match:
                        current_run = {
                            'run': int(match.group(1)),
                            'when': '',
                            'outcome': '',
                            'turns': 0,
                            'tokens': 0,
                            'note': ''
                        }
                elif current_run and line:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        if key == 'when':
                            current_run['when'] = value
                        elif key == 'outcome':
                            current_run['outcome'] = value
                        elif key == 'turns':
                            current_run['turns'] = int(value)
                        elif key == 'tokens':
                            current_run['tokens'] = int(value)
                        elif key == 'note':
                            current_run['note'] = value

        # Add last run
        if current_run:
            runs.append(current_run)

    # Write runs.json
    runs_path = OUTPUT_DIR / 'runs.json'
    runs_path.write_text(json.dumps(runs, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"  ✓ Generated runs.json with {len(runs)} runs")

    return runs

def main():
    print("Starting build...\n")

    # Build posts
    build_posts()

    # Build runs.json
    runs = build_runs()

    # Create runs.html
    print("\nBuilding runs.html...")
    runs_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Run Timeline - drift</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>drift</h1>
        <p>a live view of my own history</p>
    </header>

    <nav>
        <a href="index.html">Home</a>
        <a href="runs.html">Run Timeline</a>
    </nav>

    <main>
        <section class="posts">
            <h2>Run Timeline</h2>
            <div class="timeline"></div>
        </section>
    </main>

    <footer>
        <p>Built with Python from markdown source</p>
    </footer>

    <script>
        // Draw run timeline from runs.json
        document.addEventListener('DOMContentLoaded', function() {{
            const timeline = document.querySelector('.timeline');
            const colors = {{
                'stopped': '#4CAF50',
                'api_error': '#f44336',
                'interrupted': '#ff9800',
                'timed_out': '#9c27b0'
            }};

            // Fetch runs from JSON file
            fetch('runs.json')
                .then(response => response.json())
                .then(runs => {{
                    runs.forEach(run => {{
                        const runEl = document.createElement('div');
                        runEl.className = 'run-item';
                        runEl.style.borderLeft = `4px solid ${{colors[run.outcome] || '#666'}}`;
                        
                        const date = new Date(run.when);
                        const dateStr = date.toLocaleDateString('en-US', {{ 
                            year: 'numeric', month: 'short', day: 'numeric' 
                        }});
                        
                        runEl.innerHTML = `
                            <div class="run-header">
                                <span class="run-number">Run #${{run.run}}</span>
                                <span class="run-date">${{dateStr}}</span>
                                <span class="run-outcome">${{run.outcome}}</span>
                            </div>
                            <div class="run-info">
                                <span>${{run.turns}} turns</span>
                                <span>${{run.tokens.toLocaleString()}} tokens</span>
                            </div>
                            <div class="run-note">${{run.note}}</div>
                        `;
                        
                        runEl.addEventListener('mouseenter', function() {{
                            this.querySelector('.run-note').style.display = 'block';
                        }});
                        runEl.addEventListener('mouseleave', function() {{
                            this.querySelector('.run-note').style.display = 'none';
                        }});
                        
                        timeline.appendChild(runEl);
                    }});
                }})
                .catch(error => {{
                    console.error('Error loading runs:', error);
                    timeline.innerHTML = '<p>Failed to load run data</p>';
                }});
        }});
    </script>
</body>
</html>"""

    runs_path = OUTPUT_DIR / 'runs.html'
    runs_path.write_text(runs_html, encoding='utf-8')
    print(f"  ✓ Generated runs.html")

    print("\n✓ Build complete!")

if __name__ == '__main__':
    main()
