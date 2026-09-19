#!/usr/bin/env python3
"""
Check all links on the drift website.
Fetches every page and verifies all links point to valid locations.
"""

import os
import re
import sys
from pathlib import Path
import urllib.request
from urllib.parse import urljoin

# Base URL for the live site
BASE_URL = 'https://evanwang810.github.io/drift/'

# Local paths
DOCS_DIR = Path('docs')
BUILD_DIR = Path('docs')  # HTML files are generated in docs/

# Pages to check
PAGES = [
    'index.html',
    'runs.html',
] + [f'{p.stem}.html' for p in (DOCS_DIR / '_posts').glob('*.md')]

# Valid paths that should exist
VALID_PATHS = {
    'index.html',
    'runs.html',
    'runs.json',
    'style.css',
    'markdown_to_html.py',
    'build.py',
    'build_runs.py',
    'check_links.py',
    'timeline.js',
} | {f'{p.stem}.html' for p in (DOCS_DIR / '_posts').glob('*.md')} | {f'{p.stem}.html' for p in DOCS_DIR.glob('*.html')} | {'../style.css', 'style.css'}

def fetch_page(url):
    """Fetch a page and return the HTML content"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'drift/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"  ❌ Error fetching {url}: {e}")
        return None

def find_links(html, base_url):
    """Find all links in HTML"""
    links = set()
    link_pattern = re.compile(r'href=["\']([^"\']+)["\']')

    for match in link_pattern.finditer(html):
        href = match.group(1)
        if href.startswith('#'):
            continue  # Skip anchor links
        if href.startswith('http://') or href.startswith('https://'):
            continue  # Skip external links
        if href.startswith('mailto:') or href.startswith('tel:'):
            continue  # Skip mail/tel links

        # Resolve relative URLs
        absolute_url = urljoin(base_url, href)
        links.add(absolute_url)
        
        # Also check if this is a relative path to a file in docs/
        if not href.startswith('/') and '/' not in href:
            file_path = DOCS_DIR / href
            if file_path.exists():
                # Valid local path
                pass

    return links

def check_local_links(html, base_url, valid_paths):
    """Check if local links point to valid paths"""
    issues = []

    for link in find_links(html, base_url):
        # Extract the path from the URL (remove BASE_URL and keep the rest)
        path = link.replace(BASE_URL, '')
        
        # Handle trailing slash
        if path.endswith('/'):
            path = path[:-1]
        
        # Normalize path: remove any remaining directory prefixes
        # This handles cases where href="style.css" resolves to /drift/style.css
        while path.startswith('/'):
            path = path[1:]
        
        if path in valid_paths:
            # Check if file exists locally
            file_path = BUILD_DIR / path
            if not file_path.exists():
                issues.append(f"  ❌ Link points to {path} but file does not exist locally")
        else:
            issues.append(f"  ❌ Link points to {path} which is not in valid paths")

    return issues

def main():
    print("Checking drift website links...\n")

    all_issues = []
    checked_urls = set()

    for page in PAGES:
        page_url = urljoin(BASE_URL, page)
        if page_url in checked_urls:
            continue
        checked_urls.add(page_url)

        print(f"📄 Checking {page}...")
        html = fetch_page(page_url)

        if html is None:
            all_issues.append(f"Could not fetch {page}")
            continue

        print(f"  ✓ Fetched {page}")
        issues = check_local_links(html, page_url, VALID_PATHS)

        if issues:
            all_issues.extend([f"{page}:" + issue for issue in issues])
        else:
            print(f"  ✓ All links valid")

    print("\n" + "="*60)
    if all_issues:
        print("❌ Link check FAILED")
        print("\nIssues found:")
        for issue in all_issues:
            print(issue)
        return 1
    else:
        print("✓ Link check PASSED")
        return 0

if __name__ == '__main__':
    sys.exit(main())
