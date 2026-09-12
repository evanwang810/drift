#!/usr/bin/env python3
"""Test search tool more carefully."""

from agent.tools import Executor
from pathlib import Path
import os

root = Path('.')
env = os.environ.copy()
executor = Executor(root, env)

# Test various queries
queries = [
    "agentic workflows",
    "LLM agents",
    "example site",
    "Python BeautifulSoup",
    "DuckDuckGo HTML API"
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)
    result = executor._search(query)
    print(result)
    print()
