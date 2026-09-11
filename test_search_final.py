#!/usr/bin/env python3
"""Test if search now returns actual results."""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.tools import Executor

def test_search():
    root = Path(".")
    env = os.environ.copy()
    executor = Executor(root=root, env=env)

    try:
        result = executor._search("LLM agents 2026")
        print(f"Search result:\n{result}")
        return result
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return None

if __name__ == "__main__":
    result = test_search()
    if result and "No results found" not in result:
        print("\n✓ Search returned actual results!")
    elif result:
        print("\n✗ Search still returns 'No results found'")
