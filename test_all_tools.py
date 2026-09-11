"""Test all tools in agent/tools.py"""
import sys
sys.path.insert(0, '.')
from agent.tools import Executor
from pathlib import Path
import json

# Create an executor instance
executor = Executor(root=Path('.'), env={})

# List of all callable tools
tools_to_test = [
    '_analyze_runs',
    '_delete',
    '_grep',
    '_ls',
    '_read',
    '_read_all',
    '_read_lines',
    '_read_with_numbers',
    '_replace',
    '_replace_all',
    '_run',
    '_search',
    '_summarize',
    '_tree',
    '_validate_python',
    '_web_fetch',
    '_write',
]

print("=" * 80)
print("TOOL TESTING RESULTS")
print("=" * 80)

results = {}

for tool_name in tools_to_test:
    print(f"\nTesting: {tool_name}")
    tool = getattr(executor, tool_name, None)

    # Build appropriate args for each tool
    args = {}

    if tool_name == '_analyze_runs':
        pass  # No args needed
    elif tool_name == '_delete':
        args = {'path': 'test_temp_file.txt'}
    elif tool_name == '_grep':
        args = {'pattern': 'agent', 'path': '.'}
    elif tool_name == '_ls':
        args = {'path': '.'}
    elif tool_name == '_read':
        args = {'path': 'PROJECT.md'}
    elif tool_name == '_read_all':
        args = {'path': 'PROJECT.md'}
    elif tool_name == '_read_lines':
        args = {'path': 'PROJECT.md', 'start': 1, 'end': 10}
    elif tool_name == '_read_with_numbers':
        args = {'path': 'PROJECT.md'}
    elif tool_name == '_replace':
        args = {'path': 'PROJECT.md', 'search': 'PROJECT', 'replace': 'PROJECT.md'}
    elif tool_name == '_replace_all':
        args = {'path': 'PROJECT.md', 'search': 'PROJECT', 'replace': 'PROJECT.md'}
    elif tool_name == '_run':
        args = {'command': 'echo "hello"'}
    elif tool_name == '_search':
        args = {'query': 'agentic workflows'}
    elif tool_name == '_summarize':
        # This requires messages to be set
        args = {'summary': 'Test summary'}
    elif tool_name == '_tree':
        args = {'path': '.', 'max_depth': 2}
    elif tool_name == '_validate_python':
        args = {'path': 'test_tools.py'}
    elif tool_name == '_web_fetch':
        args = {'url': 'https://example.com', 'parse_html': True}
    elif tool_name == '_write':
        args = {'path': 'test_temp_file.txt', 'content': 'test content'}

    try:
        result = tool(**args)
        results[tool_name] = result
        print(f"  ✓ SUCCESS")
        print(f"  Output (first 200 chars): {str(result)[:200]}")
    except NameError as e:
        results[tool_name] = f"NameError: {e}"
        print(f"  ✗ NameError: {e}")
    except Exception as e:
        results[tool_name] = f"{type(e).__name__}: {e}"
        print(f"  ✗ {type(e).__name__}: {e}")

# Test _stop (should raise Stopped)
print(f"\nTesting: _stop")
try:
    executor._stop("test stop", "test memory")
    results['_stop'] = "ERROR: Should have raised Stopped"
    print(f"  ✗ Should have raised Stopped")
except Exception as e:
    if "Stopped" in str(type(e)):
        results['_stop'] = "✓ Correctly raises Stopped"
        print(f"  ✓ Correctly raises Stopped")
    else:
        results['_stop'] = f"{type(e).__name__}: {e}"
        print(f"  ✗ {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\nTotal tools tested: {len(tools_to_test) + 1}")
print(f"Successful: {sum(1 for r in results.values() if '✓' in str(r))}")
print(f"Failed: {sum(1 for r in results.values() if '✗' in str(r))}")

print("\nAll results:")
for name, result in sorted(results.items()):
    print(f"  {name}: {result}")
