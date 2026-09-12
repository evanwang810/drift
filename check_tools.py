#!/usr/bin/env python3
"""Check which methods exist in Executor."""

import sys
from pathlib import Path
import inspect

sys.path.insert(0, str(Path(__file__).parent))

from agent.tools import Executor

print("All methods in Executor:")
print("="*60)

for name, function in inspect.getmembers(Executor, inspect.isfunction):
    print(f"{name}")

print("\n" + "="*60)
print("Methods starting with underscore (potential tools):")
print("="*60)

tools = [name for name, function in inspect.getmembers(Executor, inspect.isfunction)
         if name.startswith("_") and not name.startswith("__")]

for tool in sorted(tools):
    print(tool)
