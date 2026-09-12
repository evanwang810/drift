#!/usr/bin/env python3
"""Test search with more realistic queries and check if rate limiting is the issue."""

from bs4 import BeautifulSoup
import requests
import requests.utils
import time

queries = [
    "LLM agents",
    "agentic AI",
    "python programming",
    "web scraping",
    "beautiful soup",
]

for query in queries:
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"

    print(f"\nQuery: {query}")

    response = requests.get(url, timeout=10)

    print(f"  Status: {response.status_code}")

    if response.status_code == 202:
        print(f"  Rate limited - empty HTML")
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select('.result__a')
        print(f"  Results found: {len(results)}")
        if results:
            for r in results[:2]:
                print(f"    - {r.get_text(strip=True)[:60]}")
    elif response.status_code == 200:
        print(f"  Success!")
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select('.result__a')
        print(f"  Results found: {len(results)}")
        if results:
            for i, r in enumerate(results[:3], 1):
                title = r.get_text(strip=True)
                print(f"    {i}. {title[:60]}")
    else:
        print(f"  Unexpected status")

    time.sleep(1)  # Be polite
