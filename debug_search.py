#!/usr/bin/env python3
"""Debug the search tool."""

import sys
import os
import requests
from bs4 import BeautifulSoup

query = "LLM agents 2026"
url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"

print(f"Fetching: {url}")

try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if results exist
        result_elements = soup.select('.result__a')
        print(f"\nFound {len(result_elements)} .result__a elements")
        
        # Check for any result-like elements
        all_links = soup.select('a')
        print(f"Found {len(all_links)} total <a> tags")
        
        # Look for result containers
        result_containers = soup.select('.result__a, .result, .result__body')
        print(f"Found {len(result_containers)} result-like containers")
        
        # Check for any HTML in the response
        if len(response.text) < 5000:
            print(f"\nResponse is very short ({len(response.text)} chars):")
            print(response.text[:1000])
        else:
            print(f"\nFirst 500 chars of HTML:")
            print(response.text[:500])
            
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
