#!/usr/bin/env python3
"""Measure the token counts of system prompt, waking message, and tool schema."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agent import context, tools
from engine.loop import opening
from datetime import datetime

root = Path.cwd()

# System prompt
system_prompt = context.prompt(root)
system_tokens = len(system_prompt) // 3 + 600

# Waking message
now = datetime.now()
waking_msg = context.waking(root, 91, 1, "out_of_turns", now, 40)
waking_tokens = len(waking_msg) // 3 + 600

# Tool schema
schema = tools.schema()
schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
schema_tokens = len(schema_str) // 3 + 600

# Full opening
messages = opening(root, 91, 1, "out_of_turns", now, 40, "")
full_tokens = sum(len(str(m.get("content") or "")) // 3 + 600 for m in messages)

print(f"System prompt: {len(system_prompt)} chars, ~{system_tokens:,} tokens")
print(f"Waking message: {len(waking_msg)} chars, ~{waking_tokens:,} tokens")
print(f"Tool schema: {len(schema_str)} chars, ~{schema_tokens:,} tokens")
print(f"Total first turn: ~{full_tokens:,} tokens")
