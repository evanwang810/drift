#!/usr/bin/env python3
"""Debug RUNS.md parsing."""

with open('RUNS.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print("\nFirst 30 lines:")
for i, line in enumerate(lines[:30]):
    print(f"{i}: {line.rstrip()}")
