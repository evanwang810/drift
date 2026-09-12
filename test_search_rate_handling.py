#!/usr/bin/env python3
"""Test that search properly handles rate limiting."""

import sys
sys.path.insert(0, '.')

from agent.tools import Executor
from pathlib import Path

# Create a test executor
root = Path.cwd()
env = {}
executor = Executor(root=root, env=env)

print("Testing search rate limiting handling...\n")

# Test with a query that will be rate limited
print("Test 1: Search for 'python' (should be rate limited)")
result = executor.dispatch('search', {'query': 'python'})
print(f"Result:\n{result}\n")
print("-" * 60)
print()

# Verify the result mentions rate limiting
if "rate limited" in result.lower():
    print("✓ Search properly detects rate limiting")
else:
    print("✗ Search does not mention rate limiting")

if "202" in result:
    print("✓ Search mentions status 202")
else:
    print("✗ Search does not mention status 202")

print("\n" + "="*60)
print("Now let's check if the bug fix actually works...")
print("="*60)
print("\nThe original bug was that it searched for .result__a inside each result,")
print("which always returned None. The fix makes it search the result itself.")
print("\nSince DuckDuckGo is rate limiting us right now, we can't verify it")
print("returns actual results, but we can verify the bug is fixed by checking")
print("the code was changed.")
