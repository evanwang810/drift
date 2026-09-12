#!/usr/bin/env python3
"""Test all tools in agent/tools.py to see what actually returns."""

import sys
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.tools import Executor
import analyze_runs

# Create executor with proper ROOT
ROOT = Path("/tmp/scratch")
executor = Executor(root=ROOT, env={})

tools = [
    'search',
    'web_fetch',
    'read',
    'read_with_numbers',
    'read_lines',
    'read_all',
    'write',
    'replace',
    'replace_all',
    'delete',
    'ls',
    'tree',
    'grep',
    'validate_python',
    'analyze_runs',
    '_gh_list_issues',
    '_gh_read_issue',
    '_gh_comment_issue',
    '_gh_close_issue',
    '_wikipedia_search',
]

results = {}

for tool_name in tools:
    print(f"\n{'='*60}")
    print(f"Testing: {tool_name}")
    print('='*60)

    try:
        # Check if the tool exists as a method
        handler = getattr(executor, f"_{tool_name}", None)
        if handler is None:
            print(f"  ❌ No handler found")
            results[tool_name] = "no_handler"
            continue

        # Try calling it with real arguments
        if tool_name == 'search':
            result = executor.dispatch(tool_name, {"query": "agentic workflows"})
        elif tool_name == 'web_fetch':
            result = executor.dispatch(tool_name, {"url": "https://example.com"})
        elif tool_name == 'read':
            result = executor.dispatch(tool_name, {"path": "README.md"})
        elif tool_name == 'read_with_numbers':
            result = executor.dispatch(tool_name, {"path": "README.md"})
        elif tool_name == 'read_lines':
            result = executor.dispatch(tool_name, {"path": "README.md", "start": 1, "end": 10})
        elif tool_name == 'read_all':
            result = executor.dispatch(tool_name, {"path": "README.md"})
        elif tool_name == 'write':
            result = executor.dispatch(tool_name, {"path": "test_output.txt", "content": "test"})
        elif tool_name == 'replace':
            result = executor.dispatch(tool_name, {"path": "README.md", "search": "test", "replace": "replaced"})
        elif tool_name == 'replace_all':
            result = executor.dispatch(tool_name, {"path": "README.md", "search": "test", "replace": "replaced"})
        elif tool_name == 'delete':
            result = executor.dispatch(tool_name, {"path": "test_output.txt"})
        elif tool_name == 'ls':
            result = executor.dispatch(tool_name, {"path": "."})
        elif tool_name == 'tree':
            result = executor.dispatch(tool_name, {"path": "."})
        elif tool_name == 'grep':
            result = executor.dispatch(tool_name, {"pattern": "test", "path": "."})
        elif tool_name == 'validate_python':
            result = executor.dispatch(tool_name, {"path": "agent/tools.py"})
        elif tool_name == 'analyze_runs':
            result = executor.dispatch(tool_name, {})
        elif tool_name.startswith('_gh_'):
            result = executor.dispatch(tool_name, {"repo": "test/repo", "number": 1})
        elif tool_name == '_wikipedia_search':
            result = executor.dispatch(tool_name, {"query": "agentic workflows"})
        else:
            print(f"  ❌ No test arguments defined")
            results[tool_name] = "no_test_args"
            continue

        print(f"  Result: {result[:200]}")
        results[tool_name] = result[:200]

    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {e}")
        results[tool_name] = f"ERROR: {type(e).__name__}: {e}"

# Save results
with open("TOOL_TEST_RESULTS.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n{'='*60}")
print("All tests complete. Results saved to TOOL_TEST_RESULTS.json")
print('='*60)
