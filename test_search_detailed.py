#!/usr/bin/env python3
"""Detailed test of the search bug."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agent.tools import Executor
import requests
from bs4 import BeautifulSoup

def test_search_bug():
    """Test the actual search bug with a real query."""
    print("Testing search bug with query: 'agentic workflows'\n")

    # First, test what the search function actually does
    url = "https://html.duckduckgo.com/html/?q=agentic%20workflows"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    results = list(soup.select('.result__a'))
    print(f"1. Number of '.result__a' elements found: {len(results)}")

    if results:
        first = results[0]
        title_from_result = first.get_text(strip=True)[:100]
        print(f"   First result title (from element itself): '{title_from_result}'")

        # The bug: searching descendants
        title_from_descendant = first.select_one('.result__a')
        if title_from_descendant:
            title_from_descendant_text = title_from_descendant.get_text(strip=True)[:100]
            print(f"   First result title (from descendant): '{title_from_descendant_text}'")
            print(f"   They are the same: {title_from_result == title_from_descendant_text}")
        else:
            print("   No descendant found - but there should be!")

    # Test the actual tool
    print("\n2. Calling _search tool:")
    root = Path(__file__).parent
    env = {"PATH": str(Path("/usr/bin"))}
    executor = Executor(root=root, env=env)

    result = executor._search("agentic workflows")
    print(f"Result: {result[:200]}")

    # Count how many results were found in the result string
    if "No results found" in result:
        print("\n3. ❌ BUG CONFIRMED: Search returned 'No results found' even though there are results on the page")
    else:
        print("\n3. ✓ Search returned actual results")

if __name__ == "__main__":
    test_search_bug()
