#!/usr/bin/env python3
"""Test different queries to find one that returns results."""

import requests
from bs4 import BeautifulSoup

queries = [
    "python",
    "javascript",
    "html",
    "web development",
    "api",
    "github",
    "openai",
]

print("Testing various queries to find one that returns results:\n")

for query in queries:
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    response = requests.get(url, timeout=10)
    
    print(f"\nQuery: '{query}'")
    print(f"  Status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select('.result__a')
        print(f"  Results found: {len(results)}")
        
        if results:
            print(f"  First result: {results[0].get_text(strip=True)[:80]}")
            print(f"  First href: {results[0].get('href', 'N/A')[:80]}")
            break
    elif response.status_code == 202:
        print(f"  Rate limited (status 202)")
    else:
        print(f"  Error: {response.status_code}")
