"""Check for duplicate tool definitions in agent/tools.py."""

import re
from pathlib import Path

# Read the tools.py file
tools_file = Path("agent/tools.py")
content = tools_file.read_text()

# Find all methods starting with _
methods = re.findall(r'^\s+def _(\w+)\(', content, re.MULTILINE)

print(f"Total methods starting with _: {len(methods)}")
print("\nAll methods:")
for i, method in enumerate(methods, 1):
    print(f"{i:3}. {method}")

# Check for duplicates
method_counts = {}
for method in methods:
    method_counts[method] = method_counts.get(method, 0) + 1

duplicates = {method: count for method, count in method_counts.items() if count > 1}
if duplicates:
    print(f"\n⚠️  DUPLICATES FOUND ({sum(duplicates.values())} total occurrences):")
    for method, count in duplicates.items():
        print(f"  {method}: {count} times")
else:
    print("\n✅ No duplicates found")

# Write to a file for comparison
with open("agent/methods.txt", "w") as f:
    f.write("Methods in agent/tools.py:\n")
    for method in methods:
        f.write(f"  {method}\n")

print("\nMethods list written to agent/methods.txt")
