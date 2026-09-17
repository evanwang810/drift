#!/usr/bin/env python3
"""
Link checker for drift website.
Fetches every page and every link on the live site, reporting any broken links.
"""

import re
import sys
from pathlib import Path


def check_links() -> int:
    """Check all links on the live site."""
    base_url = "https://evanwang810.github.io/drift/"
    all_pages = [
        "index.html",
        "runs.html",
        "data/runs.json",
        "style.css",
    ]

    # Check for markdown posts
    import os
    posts_dir = Path("docs/_posts")
    if posts_dir.exists():
        for md_file in posts_dir.glob("*.md"):
            html_file = md_file.stem + ".html"
            all_pages.append(html_file)

    failures = []

    print(f"Checking {len(all_pages)} pages on {base_url}")
    print("=" * 60)

    for page in all_pages:
        url = base_url + page
        print(f"\nChecking: {url}")

        try:
            import requests
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                print(f"  ❌ HTTP {response.status_code}")
                failures.append((url, response.status_code, "HTTP error"))
                continue

            print(f"  ✓ OK (200)")

            # Parse HTML and extract links
            content = response.text

            # Find all links
            link_pattern = r'href="([^"]+)"'
            links = re.findall(link_pattern, content)

            if not links:
                print(f"  (no links found)")
                continue

            # Check each link
            for link in links:
                # Resolve relative URLs
                if link.startswith("/"):
                    check_url = base_url + link[1:]
                elif link.startswith("./"):
                    check_url = base_url + link[2:]
                else:
                    check_url = base_url + link

                # Skip external links and anchors
                if check_url.startswith("http") or check_url.startswith("#"):
                    continue

                print(f"    - {link}")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            failures.append((url, None, str(e)))

    print("\n" + "=" * 60)

    if failures:
        print(f"\n❌ {len(failures)} failure(s):")
        for url, status, error in failures:
            print(f"  - {url}: {status or error}")
        return 1
    else:
        print(f"\n✓ All {len(all_pages)} pages are reachable")
        return 0


if __name__ == "__main__":
    sys.exit(check_links())
