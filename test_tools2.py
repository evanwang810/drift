#!/usr/bin/env python3
"""Test all tools and record what they return."""

from agent.tools import Executor
from pathlib import Path
import inspect

root = Path(".")
executor = Executor(root=root, env={})

# List all methods that start with underscore
tools = [name for name in dir(executor) if name.startswith('_') and not name.startswith('__')]
print("All tools (callable methods):")
for tool in sorted(tools):
    print(f"  {tool}")

print("\n" + "="*60 + "\n")

# Test each tool
results = {}

for tool_name in tools:
    try:
        print(f"Testing {tool_name}...")
        # Get the method
        method = getattr(executor, tool_name)

        # Get the signature (skip self)
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())
        if params and params[0] == 'self':
            params = params[1:]

        # Build args
        args = {}
        for param in params:
            param_type = sig.parameters[param].annotation
            default = sig.parameters[param].default

            # Try to find a reasonable default value based on type
            if param_type == int:
                args[param] = 1
            elif param_type == str:
                args[param] = "test"
            elif param_type == bool:
                args[param] = False
            elif param_type == list:
                args[param] = []
            elif param_type == dict:
                args[param] = {}
            elif default != inspect.Parameter.empty:
                args[param] = default
            else:
                # No sensible default, skip this param
                continue

        result = method(**args)
        results[tool_name] = result

        # Print result
        print(f"  Result: {result[:200]}..." if len(str(result)) > 200 else f"  Result: {result}")

    except Exception as e:
        results[tool_name] = f"ERROR: {type(e).__name__}: {e}"
        print(f"  ERROR: {type(e).__name__}: {e}")

    print()

print("\n" + "="*60)
print("Summary:")
print(f"Total tools: {len(tools)}")
print(f"Successfully called: {sum(1 for r in results.values() if not r.startswith('ERROR'))}")
print(f"Errors: {sum(1 for r in results.values() if r.startswith('ERROR'))}")

# Save results
with open("tool_test_results.txt", "w") as f:
    for tool_name, result in results.items():
        f.write(f"{tool_name}: {result}\n")

print("\nFull results saved to tool_test_results.txt")
