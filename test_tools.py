#!/usr/bin/env python3
"""Test all tools in agent/tools.py to see which actually work."""

import sys
sys.path.insert(0, '.')

from agent.tools import Executor
from pathlib import Path

# Create a test executor
root = Path.cwd()
env = {}
executor = Executor(root=root, env=env)

results = []

# Test each tool
tools_to_test = [
    ('analyze_runs', {}, 'Analyze RUNS.md'),
    ('read', {'path': 'agent/tools.py'}, 'Read tools.py'),
    ('read_with_numbers', {'path': 'agent/tools.py'}, 'Read tools.py with numbers'),
    ('read_lines', {'path': 'agent/tools.py', 'start': 1, 'end': 10}, 'Read first 10 lines of tools.py'),
    ('read_all', {'path': 'agent/tools.py'}, 'Read all of tools.py'),
    ('write', {'path': 'test_output.txt', 'content': 'Test content'}, 'Write test file'),
    ('replace', {'path': 'test_output.txt', 'search': 'Test', 'replace': 'Replaced'}, 'Replace in test file'),
    ('replace_all', {'path': 'test_output.txt', 'search': 'Replaced', 'replace': 'Again replaced'}, 'Replace all in test file'),
    ('delete', {'path': 'test_output.txt'}, 'Delete test file'),
    ('run', {'command': 'echo "hello"'}, 'Run echo command'),
    ('tree', {'path': '.', 'max_depth': 2}, 'List directory tree'),
    ('validate_python', {'path': 'agent/tools.py'}, 'Validate Python syntax'),
    ('ls', {'path': '.'}, 'List directory'),
    ('grep', {'pattern': 'def ', 'path': '.'}, 'Grep for function definitions'),
    ('summarize', {'summary': 'Test summary'}, 'Summarize context'),
    ('stop', {'note': 'Test stop'}, 'Stop run'),
    ('search', {'query': 'agentic workflows'}, 'Search the web'),
    ('web_fetch', {'url': 'https://example.com', 'parse_html': True}, 'Fetch web page'),
]

print("Testing tools...\n")
for tool_name, args, description in tools_to_test:
    try:
        result = executor.dispatch(tool_name, args)
        results.append({
            'tool': tool_name,
            'description': description,
            'status': 'SUCCESS',
            'result': result[:200] if isinstance(result, str) else str(result)[:200]
        })
        print(f"✓ {description} ({tool_name})")
    except Exception as e:
        results.append({
            'tool': tool_name,
            'description': description,
            'status': 'ERROR',
            'error': str(e)
        })
        print(f"✗ {description} ({tool_name}): {e}")

print("\n\n" + "="*60)
print("SUMMARY:")
print("="*60)

success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
error_count = sum(1 for r in results if r['status'] == 'ERROR')

print(f"Successful: {success_count}/{len(results)}")
print(f"Errors: {error_count}/{len(results)}")

print("\nFailed tools:")
for r in results:
    if r['status'] == 'ERROR':
        print(f"  - {r['tool']}: {r['error']}")
