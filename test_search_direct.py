#!/usr/bin/env python3
"""Test search directly."""

from bs4 import BeautifulSoup
import requests
import requests.utils

query = "agentic workflows"
url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"

print(f"Querying: {url}\n")

response = requests.get(url, timeout=10)
print(f"Status code: {response.status_code}")
print(f"Response length: {len(response.text)} chars")
print(f"Response preview (first 500 chars):\n{response.text[:500]}\n")

soup = BeautifulSoup(response.text, 'html.parser')
print(f"Found {len(soup.select('.result__a'))} .result__a elements")

for i, result in enumerate(soup.select('.result__a')[:5], 1):
    print(f"\nResult {i}:")
    print(f"  Title element: {result}")
    print(f"  Title text: {result.get_text(strip=True)[:100]}")
    print(f"  URL element: {result.select_one('.result__url')}")
    print(f"  URL text: {result.select_one('.result__url').get_text(strip=True) if result.select_one('.result__url') else 'None'}")
    print(f"  Snippet element: {result.select_one('.result__snippet')}")
    snippet = result.select_one('.result__snippet')
    print(f"  Snippet text: {snippet.get_text(strip=True)[:100] if snippet else 'None'}")
