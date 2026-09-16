#!/usr/bin/env python3
"""Test all 54 tools in agent/tools.py systematically."""

import sys
from pathlib import Path
from agent.tools import Executor

# Create a mock executor instance
mock_env = {}
exec = Executor(root=Path('.'), env=mock_env)

# Get all tools
tools = [m for m in dir(exec) if m.startswith('_') and not m.startswith('__')]

print(f"Testing {len(tools)} tools...\n")

results = {}

for tool_name in tools:
    try:
        # Get the method
        method = getattr(exec, tool_name)

        # Try to get signature
        import inspect
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())
        defaults = {k: v.default for k, v in sig.parameters.items() if v.default is not inspect.Parameter.empty}

        # Try to call with no args
        result = method(**{k: defaults.get(k, None) for k in params})

        results[tool_name] = {
            'status': 'ok',
            'result': str(result)[:200] if result else 'None',
            'error': None
        }
        print(f"✓ {tool_name}")

    except Exception as e:
        results[tool_name] = {
            'status': 'error',
            'result': None,
            'error': str(e)[:100]
        }
        print(f"✗ {tool_name}: {e}")

# Save results
import json
with open('tools_test_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to tools_test_results.json")
print(f"Passed: {sum(1 for r in results.values() if r['status'] == 'ok')}/{len(tools)}")
print(f"Failed: {sum(1 for r in results.values() if r['status'] == 'error')}/{len(tools)}")
