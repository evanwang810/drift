"""Test GitHub tools"""
import sys
sys.path.insert(0, '.')
from agent.tools import Executor
from pathlib import Path

executor = Executor(root=Path('.'), env={})

gh_tools = [
    '_gh_list_issues',
    '_gh_read_issue',
    '_gh_comment_issue',
    '_gh_close_issue',
]

print("Testing GitHub tools:")
for tool_name in gh_tools:
    tool = getattr(executor, tool_name, None)
    print(f"\n{tool_name}:")
    print(f"  Exists: {tool is not None}")
    print(f"  Type: {type(tool)}")
