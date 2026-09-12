#!/usr/bin/env python3
"""Test the fixed GitHub tools."""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from agent.tools import Executor

ROOT = Path("/tmp/scratch")
executor = Executor(root=ROOT, env={})

gh_tools = [
    ('_gh_list_issues', {'state': 'open', 'per_page': 5}),
    ('_gh_read_issue', {'issue_number': 1}),
    ('_gh_comment_issue', {'issue_number': 1, 'comment': 'Test comment'}),
    ('_gh_close_issue', {'issue_number': 1}),
]

print("Testing GitHub tools:")
print("="*60)

for tool_name, args in gh_tools:
    print(f"\nTesting: {tool_name}")
    print(f"Args: {args}")
    try:
        result = executor.dispatch(tool_name, args)
        print(f"Result: {result[:200]}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

print("\n" + "="*60)
print("All tests complete")
