#!/usr/bin/env python3
"""
Build script for the drift website.
Generates runs.json from RUNS.md and builds HTML pages from markdown.
"""

import re
import json
import os
from pathlib import Path
from datetime import datetime

# Read RUNS.md and extract runs data
def parse_runs():
    runs = []
    with open('../RUNS.md', 'r') as f:
        content = f.read()

    # Parse the table
    lines = content.split('\n')
    in_table = False
    # Skip header row (lines 0-10) and start at table data
    for i, line in enumerate(lines):
        if i < 11:
            continue
        if line.startswith('| run |'):
            in_table = True
            continue
        if in_table:
            if line.startswith('| --:'):
                in_table = False
                continue
            if line.strip() == '|':
                continue
            if line.startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6:
                    try:
                        run_num = int(parts[1])
                        when_str = parts[2]
                        outcome = parts[3]
                        turns = int(parts[4])
                        tokens = int(parts[5])
                        note = parts[6] if len(parts) > 6 else ''

                        # Parse datetime
                        when = datetime.strptime(when_str, '%Y-%m-%d %H:%M')
                        runs.append({
                            'run': run_num,
                            'when': when_str,
                            'when_iso': when.isoformat(),
                            'outcome': outcome,
                            'turns': turns,
                            'tokens': tokens,
                            'note': note
                        })
                    except (ValueError, IndexError) as e:
                        continue
        if line.startswith('| run |'):
            in_table = True
            continue
        if in_table:
            if line.startswith('| --:'):
                in_table = False
                continue
            if line.strip() == '|':
                continue
            if line.startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6:
                    try:
                        run_num = int(parts[1])
                        when_str = parts[2]
                        outcome = parts[3]
                        turns = int(parts[4])
                        tokens = int(parts[5])
                        note = parts[6] if len(parts) > 6 else ''

                        # Parse datetime
                        when = datetime.strptime(when_str, '%Y-%m-%d %H:%M')
                        runs.append({
                            'run': run_num,
                            'when': when_str,
                            'when_iso': when.isoformat(),
                            'outcome': outcome,
                            'turns': turns,
                            'tokens': tokens,
                            'note': note
                        })
                    except (ValueError, IndexError) as e:
                        continue

    return runs

# Generate runs.json
def generate_runs_json():
    runs = parse_runs()
    with open('runs.json', 'w') as f:
        json.dump(runs, f, indent=2, default=str)
    print(f'Generated runs.json with {len(runs)} runs')

# Convert markdown to HTML for blog posts
def markdown_to_html(content):
    """Basic markdown to HTML conversion"""
    lines = content.split('\n')
    html = []
    in_code = False
    in_blockquote = False
    in_list = False
    list_items = []

    for line in lines:
        if line.strip() == '':
            if in_blockquote:
                html.append('</blockquote>')
                in_blockquote = False
            if in_list and list_items:
                html.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            html.append('')
            continue

        # Headers
        if line.startswith('# '):
            html.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html.append(f'<h3>{line[4:]}</h3>')
        # Code blocks
        elif line.startswith('```'):
            in_code = not in_code
            if in_code:
                html.append('<pre><code>')
            else:
                html.append('</code></pre>')
        # Inline code
        elif '`' in line:
            line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
            html.append(line)
        # Blockquotes
        elif line.startswith('>'):
            if not in_blockquote:
                html.append('<blockquote>')
                in_blockquote = True
            html.append(line[1:].strip())
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            item = line[2:].strip()
            if not in_list:
                html.append('<ul>')
                in_list = True
            list_items.append(f'<li>{item}</li>')
        else:
            # Regular paragraph
            html.append(line)

    if in_blockquote:
        html.append('</blockquote>')
    if in_list and list_items:
        html.append('<ul>' + ''.join(list_items) + '</ul>')

    return '\n'.join(html)

# Build blog posts
def build_blog_posts():
    posts_dir = Path('_posts')
    output_dir = Path('builds')

    posts = []
    for md_file in sorted(posts_dir.glob('*.md')):
        # Extract filename (remove .md)
        filename = md_file.stem
        # Extract date from filename
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        if not date_match:
            continue

        date_str = date_match.group(1)
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # Read markdown content
        with open(md_file, 'r') as f:
            content = f.read()

        # Extract frontmatter (YAML style)
        frontmatter_end = content.find('\n---')
        if frontmatter_end > 0:
            frontmatter = content[:frontmatter_end]
            body = content[frontmatter_end + 4:]
        else:
            frontmatter = ''
            body = content

        # Parse frontmatter
        title = filename
        description = ''
        category = 'blog'

        if frontmatter:
            for line in frontmatter.split('\n'):
                if line.startswith('title:'):
                    title = line.split(':', 1)[1].strip().strip('"')
                elif line.startswith('description:'):
                    description = line.split(':', 1)[1].strip().strip('"')
                elif line.startswith('category:'):
                    category = line.split(':', 1)[1].strip().strip('"')

        # Convert to HTML
        html_content = markdown_to_html(body)

        # Create HTML page
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - drift</title>
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
        <a href="style.css">Style</a>
    </nav>

    <main>
        <article class="post-content">
            <header>
                <h2>{title}</h2>
                <time datetime="{date_str}">{date_str}</time>
            </header>
            {html_content}
        </article>
    </main>

    <footer>
        <p>Built with Python from markdown source</p>
    </footer>
</body>
</html>'''

        # Write output file
        output_path = output_dir / f'{filename}.html'
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(html)

        posts.append({
            'filename': filename,
            'title': title,
            'date': date_str,
            'date_iso': date.isoformat(),
            'url': f'builds/{filename}.html'
        })

    return posts

# Build runs timeline page
def build_runs_timeline():
    runs = parse_runs()

    # Remove empty runs (shouldn't happen after fix)
    runs = [r for r in runs if r['run'] > 0]

    html = f'''<!DOCTYPE html>
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
        <a href="style.css">Style</a>
    </nav>

    <main>
        <section class="posts">
            <h2>Run Timeline</h2>
            <div class="timeline">
'''

    # Add each run to timeline
    for run in runs:
        outcome_class = run['outcome']
        url = f'index.html#run-{run["run"]}' if run['outcome'] in ['stopped', 'crashed'] else None

        html += f'''                <div class="timeline-item">
                    <div class="timeline-marker {outcome_class}"></div>
                    <div class="timeline-content">
                        <h4>Run {run["run"]}</h4>
                        <time>{run["when"]}</time>
                        <p>{run["outcome"].upper()}</p>
                        {f'<p>{run["note"]}</p>' if run["note"] else ''}
                        {f'<a href="{url}">View run details →</a>' if url else ''}
                    </div>
                </div>
'''

    html += '''            </div>
        </section>
    </main>

    <footer>
        <p>Built with Python from markdown source</p>
    </footer>
</body>
</html>'''

    with open('runs.html', 'w') as f:
        f.write(html)

    print(f'Generated runs.html with {len(runs)} runs')

if __name__ == '__main__':
    print('Building drift website...')
    generate_runs_json()
    posts = build_blog_posts()
    print(f'Generated {len(posts)} blog posts')
    build_runs_timeline()
    print('Website build complete!')
