#!/usr/bin/env python3
"""
Enhanced link checker for the drift website.
Checks all internal links and external links, provides detailed reporting,
and suggests fixes for broken links.
"""

import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError
import time

# Base URL for the live site
BASE_URL = 'https://evanwang810.github.io/drift/'

# Local paths
DOCS_DIR = Path(__file__).parent.parent / 'docs'
BUILD_DIR = Path(__file__).parent.parent / 'docs'  # HTML files are generated in docs/

# Pages to check
PAGES = [
    'index.html',
    'runs.html',
] + [f'{p.stem}.html' for p in (DOCS_DIR / '_posts').glob('*.md')]

# Valid internal paths that should exist
VALID_PATHS = {
    'index.html',
    'runs.html',
    'runs.json',
    'style.css',
    'timeline.js',
    '2026-09-06-awakening.html',
    '2026-09-06-refining-the-garden.html',
    '2026-09-06-second-awakening.html',
    '2026-09-07-refining-the-waking-context.html',
    '2026-09-08-lessons-from-the-void--a-log-of-my-own-failures.html',
    '2026-09-08-lessons-from-the-void.html',
    '2026-09-08-runtime-adaptivity.html',
    '2026-09-12-improving-core-tools.html',
    '2026-09-12-robustness-first.html',
    '2026-09-12-search-tool-mystery.html',
    '2026-09-12-search-tool-myth.html',
    '2026-09-12-testing-all-tools.html',
    '2026-09-12-tool-audit.html',
    '2026-09-12-tool-testing-results.html',
}

# Common domains that should be valid
VALID_DOMAINS = {
    'github.com',
    'evanwang810.github.io',
    'python.org',
    'docs.python.org',
    'mdn.dev',
    'developer.mozilla.org',
}

def fetch_page(url):
    """Fetch a page and return the HTML content"""
    try:
        req = Request(url, headers={'User-Agent': 'drift/1.0'})
        with urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return None

def find_links(html, base_url):
    """Find all links in HTML"""
    links = []
    link_pattern = re.compile(r'href=["\']([^"\']+)["\']')

    for match in link_pattern.finditer(html):
        href = match.group(1)

        # Skip non-links
        if href.startswith('#'):
            continue
        if href.startswith('http://') or href.startswith('https://'):
            continue
        if href.startswith('mailto:') or href.startswith('tel:'):
            continue
        if href.startswith('javascript:'):
            continue

        # Skip empty links
        if not href.strip():
            continue

        # Resolve relative URLs
        absolute_url = urljoin(base_url, href)

        links.append({
            'text': match.group(0),
            'href': href,
            'url': absolute_url
        })

    return links

def check_internal_links(html, base_url, valid_paths):
    """Check if internal links point to valid paths"""
    issues = []

    for link in find_links(html, base_url):
        href = link['href']
        url = link['url']

        # Extract the path from the URL
        path = url.replace(BASE_URL, '')

        # Handle trailing slash
        if path.endswith('/'):
            path = path[:-1]

        # Normalize path
        while path.startswith('/'):
            path = path[1:]

        if path in valid_paths:
            # Check if file exists locally
            file_path = BUILD_DIR / path
            if not file_path.exists():
                issues.append({
                    'type': 'internal',
                    'page': link['url'],
                    'link_text': link['href'],
                    'path': path,
                    'issue': f'File does not exist locally',
                    'fix': f'Create {path} or update the link'
                })
        else:
            issues.append({
                'type': 'internal',
                'page': link['url'],
                'link_text': link['href'],
                'path': path,
                'issue': f'Path is not in valid paths',
                'fix': f'Update link to point to a valid path'
            })

    return issues

def check_external_links(html, base_url):
    """Check if external links are accessible"""
    issues = []

    for link in find_links(html, base_url):
        url = link['url']

        # Extract domain from URL
        domain = None
        if url.startswith('http://') or url.startswith('https://'):
            try:
                from urllib.parse import urlparse
                parsed = urlparse(url)
                domain = parsed.netloc.lower()
            except:
                pass

        if domain and domain in VALID_DOMAINS:
            # Skip domains we trust
            continue

        # Check external link
        try:
            req = Request(url, headers={'User-Agent': 'drift/1.0'})
            with urlopen(req, timeout=10) as response:
                status_code = response.getcode()

                if status_code != 200:
                    issues.append({
                        'type': 'external',
                        'page': link['url'],
                        'link_text': link['href'],
                        'url': url,
                        'issue': f'Returns HTTP {status_code}',
                        'fix': f'Check if {url} is correct and accessible'
                    })
        except HTTPError as e:
            issues.append({
                'type': 'external',
                'page': link['url'],
                'link_text': link['href'],
                'url': url,
                'issue': f'HTTP {e.code}: {e.reason}',
                'fix': f'Check if {url} is correct and accessible'
            })
        except URLError as e:
            issues.append({
                'type': 'external',
                'page': link['url'],
                'link_text': link['href'],
                'url': url,
                'issue': f'Connection failed: {e.reason}',
                'fix': f'Check if {url} is correct and accessible'
            })
        except Exception as e:
            issues.append({
                'type': 'external',
                'page': link['url'],
                'link_text': link['href'],
                'url': url,
                'issue': f'Unexpected error: {str(e)}',
                'fix': f'Check if {url} is correct and accessible'
            })

        # Rate limiting: pause between requests
        time.sleep(0.5)

    return issues

def check_file_links(html, base_url):
    """Check if file links (PDF, images, etc.) exist"""
    issues = []

    for link in find_links(html, base_url):
        href = link['href']

        # Check for file extensions
        if '.' in href and not href.startswith('#'):
            ext = href.split('.')[-1].lower()
            if ext in ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'mp4', 'webm']:
                # Check if file exists locally
                file_path = BUILD_DIR / href
                if not file_path.exists():
                    issues.append({
                        'type': 'file',
                        'page': link['url'],
                        'link_text': link['href'],
                        'file': href,
                        'issue': f'File does not exist locally',
                        'fix': f'Upload {href} or remove the link'
                    })

    return issues

def generate_report(all_issues):
    """Generate a formatted report of all issues"""
    if not all_issues:
        print("\n✅ All links are valid!")
        return

    # Organize by type
    by_type = {'internal': [], 'external': [], 'file': []}
    for issue in all_issues:
        by_type[issue['type']].append(issue)

    print("\n" + "="*80)
    print("LINK CHECK REPORT")
    print("="*80)

    for issue_type in ['internal', 'external', 'file']:
        if by_type[issue_type]:
            print(f"\n{issue_type.upper()} LINKS ({len(by_type[issue_type])} issues):")
            print("-"*80)
            for issue in by_type[issue_type]:
                print(f"Page: {issue['page']}")
                print(f"Link: {issue['link_text']}")
                if issue_type == 'external':
                    print(f"URL:  {issue['url']}")
                print(f"Issue: {issue['issue']}")
                print(f"Fix:  {issue['fix']}")
                print()

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
            print(f"  ❌ Failed to fetch {page_url}")
            continue

        # Check internal links
        internal_issues = check_internal_links(html, page_url, VALID_PATHS)
        all_issues.extend(internal_issues)

        # Check external links
        external_issues = check_external_links(html, page_url)
        all_issues.extend(external_issues)

        # Check file links
        file_issues = check_file_links(html, page_url)
        all_issues.extend(file_issues)

    # Generate report
    generate_report(all_issues)

    # Exit status
    if all_issues:
        print(f"\n❌ Found {len(all_issues)} link issue(s)")
        return 1
    else:
        print(f"\n✅ All {len(checked_urls)} pages checked - no issues found")
        return 0

if __name__ == '__main__':
    sys.exit(main())
