#!/usr/bin/env python3
"""Detailed test of search tool."""

import sys
sys.path.insert(0, '.')

from agent.tools import Executor
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Create a test executor
root = Path.cwd()
env = {}
executor = Executor(root=root, env=env)

print("Testing search tool in detail...\n")

# Test 1: Search for "agentic workflows"
print("Test 1: Search for 'agentic workflows'")
result = executor.dispatch('search', {'query': 'agentic workflows'})
print(f"Result:\n{result}")
print()

# Test 2: Use requests directly to see what DuckDuckGo returns
print("Test 2: Direct request to DuckDuckGo")
url = "https://html.duckduckgo.com/html/?q=agentic+workflows"
response = requests.get(url, timeout=10)
print(f"Status code: {response.status_code}")
print(f"First 500 chars of response:\n{response.text[:500]}")

# Check if there are result__a elements
soup = BeautifulSoup(response.text, 'html.parser')
results = soup.select('.result__a')
print(f"\nNumber of .result__a elements found: {len(results)}")

if results:
    for i, result in enumerate(results[:3], 1):
        title_elem = result.select_one('.result__a')
        url_elem = result.select_one('.result__url')
        snippet_elem = result.select_one('.result__snippet')
        print(f"\nResult {i}:")
        print(f"  Title element: {title_elem.get_text(strip=True) if title_elem else 'None'}")
        print(f"  URL element: {url_elem.get_text(strip=True) if url_elem else 'None'}")
        print(f"  Snippet element: {snippet_elem.get_text(strip=True) if snippet_elem else 'None'}")
else:
    print("No results found - this is the bug!")

print("\n\n" + "="*60)
print("Testing analyze_runs...")
print("="*60)
result = executor.dispatch('analyze_runs', {})
print(f"Result:\n{result}")
