#!/usr/bin/env python3
"""Test all tools and record what they return."""

from agent.tools import Executor
from pathlib import Path

root = Path(".")
executor = Executor(root=root, env={})

results = {}

# Test _read
print("Testing _read...")
try:
    result = executor._read("agent/tools.py")
    results["_read"] = result
    print(f"  Result length: {len(result)} chars")
except Exception as e:
    results["_read"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _search
print("Testing _search...")
try:
    result = executor._search("agentic workflows")
    results["_search"] = result
    print(f"  Result: {result[:200]}..." if len(str(result)) > 200 else f"  Result: {result}")
except Exception as e:
    results["_search"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _web_fetch
print("Testing _web_fetch...")
try:
    result = executor._web_fetch("https://example.com")
    results["_web_fetch"] = result
    print(f"  Result length: {len(result)} chars")
except Exception as e:
    results["_web_fetch"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _ls
print("Testing _ls...")
try:
    result = executor._ls(".")
    results["_ls"] = result
    print(f"  Files listed: {len(result.splitlines())}")
except Exception as e:
    results["_ls"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _grep
print("Testing _grep...")
try:
    result = executor._grep("def _")
    results["_grep"] = result
    print(f"  Matches: {len(result.splitlines())}")
except Exception as e:
    results["_grep"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _write
print("Testing _write...")
try:
    result = executor._write("test_output.txt", "Test content")
    results["_write"] = result
    print(f"  Result: {result}")
except Exception as e:
    results["_write"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _delete
print("Testing _delete...")
try:
    result = executor._delete("test_output.txt")
    results["_delete"] = result
    print(f"  Result: {result}")
except Exception as e:
    results["_delete"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Save results
with open("tool_test_results.txt", "w") as f:
    f.write("Tool Test Results:\n")
    f.write("="*60 + "\n\n")
    for tool_name, result in results.items():
        f.write(f"{tool_name}:\n{result}\n\n")

print("Full results saved to tool_test_results.txt")
