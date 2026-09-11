#!/usr/bin/env python3
"""Test all tools with proper arguments and record what they return."""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.tools import Executor

def test_tools():
    root = Path(".")
    env = os.environ.copy()
    executor = Executor(root=root, env=env)

    results = []

    # Test _analyze_runs - it should use the standalone function, not RunAnalyzer class
    try:
        result = executor._analyze_runs()
        results.append(("analyze_runs", result))
    except Exception as e:
        results.append(("analyze_runs", f"ERROR: {type(e).__name__}: {e}"))

    # Test _read
    try:
        result = executor._read("agent/tools.py")
        results.append(("read", result[:200]))
    except Exception as e:
        results.append(("read", f"ERROR: {type(e).__name__}: {e}"))

    # Test _search with a real query
    try:
        result = executor._search("LLM agents 2026")
        results.append(("search", result[:300]))
    except Exception as e:
        results.append(("search", f"ERROR: {type(e).__name__}: {e}"))

    # Test _validate_python
    try:
        result = executor._validate_python("agent/tools.py")
        results.append(("validate_python", result))
    except Exception as e:
        results.append(("validate_python", f"ERROR: {type(e).__name__}: {e}"))

    # Test _ls
    try:
        result = executor._ls(".")
        results.append(("ls", result[:200]))
    except Exception as e:
        results.append(("ls", f"ERROR: {type(e).__name__}: {e}"))

    # Test _tree
    try:
        result = executor._tree(".", 2)
        results.append(("tree", result[:200]))
    except Exception as e:
        results.append(("tree", f"ERROR: {type(e).__name__}: {e}"))

    # Test _run
    try:
        result = executor._run("echo hello")
        results.append(("run", result[:200]))
    except Exception as e:
        results.append(("run", f"ERROR: {type(e).__name__}: {e}"))

    # Test _grep
    try:
        result = executor._grep("def _", ".")
        results.append(("grep", result[:200]))
    except Exception as e:
        results.append(("grep", f"ERROR: {type(e).__name__}: {e}"))

    # Check if GitHub tools exist (they should not, they're unreachable code)
    has_gh_tools = all(hasattr(executor, f"_gh_{name}") for name in ["list_issues", "read_issue", "comment_issue", "close_issue"])
    results.append(("gh_tools_exist", "YES" if has_gh_tools else "NO"))

    return results

if __name__ == "__main__":
    results = test_tools()
    for name, result in results:
        print(f"{name}: {result}")
