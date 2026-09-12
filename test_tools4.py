#!/usr/bin/env python3
"""Test remaining tools that may have issues."""

from agent.tools import Executor
from pathlib import Path

root = Path(".")
executor = Executor(root=root, env={})

results = {}

# Test _analyze_runs
print("Testing _analyze_runs...")
try:
    result = executor._analyze_runs()
    results["_analyze_runs"] = result
    print(f"  Result length: {len(result)} chars")
    print(f"  Result preview:\n{result[:500]}")
except Exception as e:
    results["_analyze_runs"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _gh_list_issues (should fail if GH_TOKEN not set, but should be callable)
print("Testing _gh_list_issues...")
try:
    result = executor._gh_list_issues()
    results["_gh_list_issues"] = result
    print(f"  Result: {result}")
except Exception as e:
    results["_gh_list_issues"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _gh_read_issue
print("Testing _gh_read_issue...")
try:
    result = executor._gh_read_issue(1)
    results["_gh_read_issue"] = result
    print(f"  Result: {result}")
except Exception as e:
    results["_gh_read_issue"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _gh_comment_issue
print("Testing _gh_comment_issue...")
try:
    result = executor._gh_comment_issue(1, "test comment")
    results["_gh_comment_issue"] = result
    print(f"  Result: {result}")
except Exception as e:
    results["_gh_comment_issue"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _gh_close_issue
print("Testing _gh_close_issue...")
try:
    result = executor._gh_close_issue(1)
    results["_gh_close_issue"] = result
    print(f"  Result: {result}")
except Exception as e:
    results["_gh_close_issue"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _read_all
print("Testing _read_all...")
try:
    result = executor._read_all("agent/tools.py")
    results["_read_all"] = result
    print(f"  Result length: {len(result)} chars")
except Exception as e:
    results["_read_all"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _read_with_numbers
print("Testing _read_with_numbers...")
try:
    result = executor._read_with_numbers("agent/tools.py")
    results["_read_with_numbers"] = result
    print(f"  Result length: {len(result)} chars")
except Exception as e:
    results["_read_with_numbers"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Test _read_lines
print("Testing _read_lines...")
try:
    result = executor._read_lines("agent/tools.py", 1, 10)
    results["_read_lines"] = result
    print(f"  Result length: {len(result)} chars")
except Exception as e:
    results["_read_lines"] = f"ERROR: {type(e).__name__}: {e}"
    print(f"  ERROR: {e}")

print()

# Save results
with open("tool_test_results.txt", "a") as f:
    f.write("\n" + "="*60 + "\n")
    f.write("Additional Tool Tests:\n")
    f.write("="*60 + "\n\n")
    for tool_name, result in results.items():
        f.write(f"{tool_name}:\n{result}\n\n")

print("Full results saved to tool_test_results.txt")
