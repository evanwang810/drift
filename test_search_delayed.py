#!/usr/bin/env python3
"""Test search with delayed requests."""

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
                print("No .result__a elements found")
                print(f"Checking for alternative result classes...")
                all_results = soup.find_all(class_=lambda x: x and 'result' in x.lower())
                print(f"Elements with 'result' in class name: {len(all_results)}")
        elif response.status_code == 202:
            print("Rate limited (202 status)")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

# Query 1: Try a specific simple query
print("Query 1: 'LLM agents'")
test_ddg_request("LLM agents")
time.sleep(10)

# Query 2: Try another query
print("\nQuery 2: 'agentic workflows'")
test_ddg_request("agentic workflows")
time.sleep(10)

# Query 3: Try something very simple
print("\nQuery 3: 'hello world'")
test_ddg_request("hello world")
time.sleep(10)
