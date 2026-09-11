#!/usr/bin/env python3
"""Count tokens in the waking message and tool schema."""

from pathlib import Path
from datetime import datetime
import re

root = Path.cwd()

# Read system prompt
system = (root / "agent/prompt.md").read_text()
print(f"System prompt: {len(system.split())} words ≈ {len(system) // 4} tokens")

# Read waking message
waking = (
    f"It is {datetime(2026, 9, 11, 13, 41):%A %Y-%m-%d %H:%M} UTC. This is run 94.\n"
    f"You have been running for 1 days.\n"
    f"Last run ended: api_error.\n"
    f"You have up to 40 turns.\n"
    f"\n"
    f"Fixed, and not yours to change:\n"
    f"  .github/*  .github/**  .git/*  .git/**  engine/*  engine/**  drift.py  KILL\n"
    f"Everything else is yours, agent/ included. Change it when it helps.\n"
    f"\n"
    f"WAKE says 30 minutes until you wake again. You may change that.\n"
    f"\n"
    f"Files:\n"
    f".git/\n"
    f".github/\n"
    f".gitignore\n"
    f"ANSWER.md\n"
    f"GOALS.md\n"
    f"KILL\n"
    f"MEMORY.md\n"
    f"NOTE.md\n"
    f"\n"
    f"Your memory (last 3 runs):\n"
    f"## run 93 | 2026-09-11 | api_error\n"
    f"\n"
    f"I was attempting to initiate the first turn of a 4...\n"
    f"\n"
    f"I learned that the external service provider is cu...\n"
    f"\n"
    f"Sending the request five times in rapid succession...\n"
    f"\n"
    f"Long-term goals in GOALS.md.\n"
    f"\n"
    f"Nobody asked for anything. Work on what you want."
)
print(f"Waking message: {len(waking.split())} words ≈ {len(waking) // 4} tokens")

# Read tools.py and generate the actual schema
tools_file = (root / "agent/tools.py").read_text()
import inspect
import json

# Simulate the schema function
from agent import tools

schema_list = tools.schema()
schema_json = json.dumps(schema_list, indent=2)
print(f"\nTool schema (JSON): {len(schema_json.split())} words ≈ {len(schema_json) // 4} tokens")

# Count each tool
print(f"\nIndividual tool sizes:")
for i, tool in enumerate(schema_list):
    tool_str = json.dumps(tool, indent=2)
    print(f"  Tool {i+1}: {len(tool_str.split())} words ≈ {len(tool_str) // 4} tokens")

# Total
total = len(system.split()) + len(waking.split()) + len(schema_json.split())
print(f"\nTotal: {total} tokens")
