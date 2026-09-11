#!/usr/bin/env python3
"""Test GitHub tools exist and can be called."""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.tools import Executor

def test_gh_tools():
    root = Path(".")
    env = os.environ.copy()
    executor = Executor(root=root, env=env)

    tools = ["_gh_list_issues", "_gh_read_issue", "_gh_comment_issue", "_gh_close_issue"]
    
    results = []
    for tool_name in tools:
        has_it = hasattr(executor, tool_name)
        results.append((tool_name, "YES" if has_it else "NO"))
        
        if has_it:
            try:
                method = getattr(executor, tool_name)
                result = method("open", 5)
                results.append((tool_name, result[:200]))
            except Exception as e:
                results.append((tool_name, f"ERROR: {type(e).__name__}: {e}"))
        else:
            results.append((tool_name, "Method does not exist"))

    return results

if __name__ == "__main__":
    results = test_gh_tools()
    for name, result in results:
        print(f"{name}: {result}")
