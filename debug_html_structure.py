#!/usr/bin/env python3
"""Debug the HTML structure of DuckDuckGo search results."""

import requests
from bs4 import BeautifulSoup

def debug_html():
    url = "https://html.duckduckgo.com/html/?q=agentic%20workflows"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    print("Checking for common result classes in DuckDuckGo HTML:\n")

    # Try various CSS selectors
    selectors = [
        '.result__a',
        '.result__a',  # The buggy one
        '.result__a',  # Should be the same
        '.result',
        '.result__body',
        '.result__snippet',
        'h3.result__a',
        'a.result__a',
        'a[href*="duckduckgo"]',
        'a[href*="html.duckduckgo"]',
        'div.result',
        'div.result__a',
    ]

    for selector in selectors:
        results = list(soup.select(selector))
        print(f"{selector:30} → {len(results)} results")

    # Look for any result-like elements
    print("\n\nLooking for all links in the document:")
    all_links = list(soup.select('a'))
    print(f"Total links: {len(all_links)}")

    # Show first 10 links
    for i, link in enumerate(all_links[:10]):
        print(f"  {i+1}. {link.get('href', 'NO HREF')[:80]}")

    # Check if there's any result-like content
    print("\n\nSearching for 'result' in class names:")
    for tag in soup.find_all():
        if tag.get('class') and 'result' in tag.get('class'):
            print(f"  Found tag: <{tag.name}> class={tag.get('class')}")

if __name__ == "__main__":
    debug_html()
