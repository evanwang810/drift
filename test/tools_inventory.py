#!/usr/bin/env python3
"""Extract tool names from agent/tools.py"""

import re

with open("agent/tools.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find all methods that start with _ (excluding the Stopped exception class)
pattern = r'def _(.*?)(?:\(|$)'
matches = re.findall(pattern, content)

print(f"Found {len(matches)} tool methods:")
for tool in sorted(set(matches)):
    print(f"  - {tool}")
