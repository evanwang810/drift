#!/usr/bin/env python3
"""Test search with a long delay to avoid rate limiting."""

import requests
from bs4 import BeautifulSoup
import time

def test_ddg_request(query):
    """Test the actual HTTP request to DuckDuckGo."""
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"

    print(f"Requesting: {url}")

    try:
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response length: {len(response.text)} bytes")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.select('.result__a')
            print(f"Number of .result__a elements found: {len(results)}")

            if results:
                print("\nFirst 3 results:")
                for i, result in enumerate(results[:3], 1):
                    title = result.get_text(strip=True)
                    url = result.get('href', '')
                    print(f"  {i}. {title[:80]}")
                    print(f"     {url[:80]}")
            else:
                print("No .result__a elements found - checking if results are there...")
                print(f"Body preview (first 1000 chars):")
                print(response.text[:1000])
        elif response.status_code == 202:
            print("Rate limited (202 status)")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

# Try with a long delay
print("Waiting 30 seconds before first request...")
time.sleep(30)

queries = ["LLM agents", "agentic workflows", "Python programming"]

for i, query in enumerate(queries, 1):
    print(f"\n{'='*60}")
    print(f"Query {i}/{len(queries)}: {query}")
    print('='*60)
    test_ddg_request(query)

    if i < len(queries):
        print("\nWaiting 15 seconds before next query...")
        time.sleep(15)
