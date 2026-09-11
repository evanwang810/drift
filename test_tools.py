#!/usr/bin/env python3
"""Test every tool in agent/tools.py and record what happens."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from agent.tools import Executor

# Create an executor instance
root = Path.cwd()
env = {}

executor = Executor(root=root, env=env)

tools_to_test = [
    ("_search", {"query": "agentic workflows"}),
    ("_grep", {"pattern": "test", "path": "."}),
    ("_analyze_runs", {}),
    ("_read", {"path": "agent/tools.py"}),
    ("_read_with_numbers", {"path": "agent/tools.py"}),
    ("_read_lines", {"path": "agent/tools.py", "start": 1, "end": 10}),
    ("_write", {"path": "test_output.txt", "content": "test"}),
    ("_replace", {"path": "test_output.txt", "search": "test", "replace": "REPLACED"}),
    ("_replace_all", {"path": "test_output.txt", "search": "REPLACED", "replace": "DONE"}),
    ("_delete", {"path": "test_output.txt"}),
    ("_summarize", {"summary": "test summary"}),
    ("_stop", {"note": "test stop"}),
    ("_read_all", {"path": "agent/tools.py"}),
    ("_web_fetch", {"url": "https://example.com", "parse_html": True}),
    ("_gh_list_issues", {"state": "open", "per_page": 5}),
    ("_gh_read_issue", {"issue_number": 1}),
    ("_gh_comment_issue", {"issue_number": 1, "comment": "test comment"}),
    ("_gh_close_issue", {"issue_number": 1}),
]

results = []

for tool_name, args in tools_to_test:
    try:
        result = executor.dispatch(tool_name, args)
        results.append(f"{tool_name}: SUCCESS\n  Args: {args}\n  Result: {result[:200] if len(result) > 200 else result}\n")
    except Exception as e:
        results.append(f"{tool_name}: ERROR\n  Args: {args}\n  Error: {type(e).__name__}: {e}\n")
    print(f"\n{'='*60}")
    print(f"Tool: {tool_name}")
    print(f"{'='*60}")
    print(f"Result: {result[:500] if len(result) > 500 else result}")

# Write results to file
with open("tool_test_results.md", "w") as f:
    f.write("# Tool Test Results\n\n")
    f.write(f"Total tools tested: {len(tools_to_test)}\n\n")
    for result in results:
        f.write(result)
        f.write("\n" + "="*60 + "\n\n")

print("\n\nResults written to tool_test_results.md")
