#!/usr/bin/env python3
"""Test Wikipedia as a search source."""

import requests
from bs4 import BeautifulSoup

def test_wikipedia():
    print("Testing Wikipedia API search endpoint\n")

    query = "agentic workflows"
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json&utf8=&origin=*"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        print(f"Status: {response.status_code}")

        if "query" in data and "search" in data["query"]:
            results = data["query"]["search"]
            print(f"\nFound {len(results)} results:\n")

            for i, result in enumerate(results[:5]):
                print(f"{i+1}. {result['title']}")
                print(f"   Snippet: {result['snippet'][:150]}")
                print()

        else:
            print("No search results found in API response")
            print(f"Full response: {data}")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_wikipedia()
