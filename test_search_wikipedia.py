#!/usr/bin/env python3
"""Test Wikipedia fallback for search."""

import sys
sys.path.insert(0, '/home/runner/work/drift/drift')

import agent.tools

_search_wikipedia = agent.tools._search_wikipedia

if _search_wikipedia is None:
    print("_search_wikipedia not found in tools module")
    exit(1)

print("Testing Wikipedia fallback...")
query = "LLM"
print(f"Query: {query}")

results = _search_wikipedia(query)
print(f"Results: {results[:200]}")
