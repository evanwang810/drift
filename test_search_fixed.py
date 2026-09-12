#!/usr/bin/env python3
"""Test the fixed search tool."""

import sys
sys.path.insert(0, '.')

from agent.tools import Executor
from pathlib import Path

# Create a test executor
root = Path.cwd()
env = {}
executor = Executor(root=root, env=env)

print("Testing fixed search tool...\n")

# Test with a common term that should return results
print("Test: Search for 'python'")
result = executor.dispatch('search', {'query': 'python'})
print(f"Result:\n{result}\n")
print("-" * 60)
print()

# Test with a term that might be rate limited
print("Test: Search for 'agentic workflows'")
result = executor.dispatch('search', {'query': 'agentic workflows'})
print(f"Result:\n{result}\n")
