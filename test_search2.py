#!/usr/bin/env python3
"""Test search with different queries."""

from bs4 import BeautifulSoup
import requests
import requests.utils

queries = [
    "python",
    "test",
    "hello world",
    "example",
    "agent",
]

for query in queries:
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"

    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")

    response = requests.get(url, timeout=10)

    print(f"Status code: {response.status_code}")
    print(f"Response length: {len(response.text)} chars")

    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select('.result__a')

    print(f"Found {len(results)} .result__a elements")

    if results:
        print("\nFirst result:")
        result = results[0]
        print(f"  Title: {result.get_text(strip=True)[:100]}")
        url_elem = result.select_one('.result__url')
        print(f"  URL: {url_elem.get_text(strip=True) if url_elem else 'None'}")
        snippet_elem = result.select_one('.result__snippet')
        print(f"  Snippet: {snippet_elem.get_text(strip=True)[:100] if snippet_elem else 'None'}")
    else:
        print("\nNo results found. Checking HTML structure...")

        # Show what elements are there
        all_links = soup.find_all('a', href=True)
        print(f"Total <a> tags with href: {len(all_links)}")

        # Look for any links that might be search results
        for i, link in enumerate(all_links[:20]):
            href = link.get('href', '')
            text = link.get_text(strip=True)[:50]
            if 'duckduckgo' in href or text:
                print(f"  {i}: {text} -> {href[:100]}")

        # Check if there's a "No results" message
        no_results = soup.find(string=lambda t: t and 'no results' in t.lower())
        if no_results:
            print(f"Found 'no results' text: {no_results.strip()[:100]}")
