#!/usr/bin/env python3
"""Debug DuckDuckGo response structure."""

import requests
from bs4 import BeautifulSoup

print("Checking DuckDuckGo response structure...\n")

# Test with a simple query
query = "python programming language"
url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
response = requests.get(url, timeout=10)

print(f"Status code: {response.status_code}")
print(f"Content length: {len(response.text)}")
print(f"First 1000 chars:\n{response.text[:1000]}")
print("\n" + "="*60 + "\n")

# Try different selectors
soup = BeautifulSoup(response.text, 'html.parser')

selectors = [
    '.result__a',
    '.result__body',
    '.result',
    'a.result__a',
    '.result__title',
    '.result__url',
]

print("Testing various selectors:")
for selector in selectors:
    elements = soup.select(selector)
    print(f"  {selector}: {len(elements)} elements")

print("\n" + "="*60 + "\n")

# Print first result elements
print("First result elements found:")
for i, result in enumerate(soup.select('.result__a')[:3], 1):
    print(f"\nResult {i}:")
    print(f"  Tag: {result.name}")
    print(f"  Class: {result.get('class')}")
    print(f"  Text: {result.get_text(strip=True)[:100]}")
    print(f"  Href: {result.get('href', 'N/A')[:100]}")
