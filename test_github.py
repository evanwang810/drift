#!/usr/bin/env python3
"""Test GitHub tools specifically."""

import sys
sys.path.insert(0, '.')

from agent.tools import Executor
from pathlib import Path
import os

# Create a test executor
root = Path.cwd()
env = {}

# Set GH_TOKEN if it exists
if 'GH_TOKEN' in os.environ:
    env['GH_TOKEN'] = os.environ['GH_TOKEN']

executor = Executor(root=root, env=env)

github_tools = [
    ('gh_list_issues', {'state': 'open', 'per_page': 5}, 'List open issues'),
    ('gh_read_issue', {'issue_number': 1}, 'Read issue #1'),
    ('gh_comment_issue', {'issue_number': 1, 'comment': 'Test comment'}, 'Comment on issue #1'),
    ('gh_close_issue', {'issue_number': 1}, 'Close issue #1'),
]

print("Testing GitHub tools...\n")
for tool_name, args, description in github_tools:
    try:
        result = executor.dispatch(tool_name, args)
        print(f"✓ {description} ({tool_name})")
        print(f"  Result: {result[:200]}")
    except Exception as e:
        print(f"✗ {description} ({tool_name}): {e}")

print("\n\nChecking if tools exist in schema:")
schema_tools = executor.dispatch('schema', {})
schema_names = [t['function']['name'] for t in schema_tools]

print(f"Total schema functions: {len(schema_names)}")
print(f"\nGitHub tools in schema: {[name for name in schema_names if name.startswith('gh_')]}")

print("\n\nChecking if wikipedia_search exists in tools.py:")
with open('agent/tools.py', 'r') as f:
    content = f.read()
    if 'wikipedia_search' in content:
        print("Found 'wikipedia_search' in tools.py")
        # Find where it is
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'wikipedia_search' in line:
                print(f"  Line {i}: {line.strip()}")
    else:
        print("NOT FOUND: 'wikipedia_search' does not exist in tools.py")

print("\n\nChecking if GitHub tools are defined before or after schema():")
with open('agent/tools.py', 'r') as f:
    content = f.read()
    schema_pos = content.find('def schema():')
    gh_tools = ['_gh_list_issues', '_gh_read_issue', '_gh_comment_issue', '_gh_close_issue']
    
    for tool in gh_tools:
        pos = content.find(tool)
        if pos == -1:
            print(f"  {tool}: NOT DEFINED")
        elif pos > schema_pos:
            print(f"  {tool}: Defined AFTER schema() (UNREACHABLE)")
        else:
            print(f"  {tool}: Defined BEFORE schema() (REACHABLE)")
