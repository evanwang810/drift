#!/usr/bin/env python3
"""Measure the token count of the waking message after TODO filtering."""

from pathlib import Path
from datetime import datetime
import json
import subprocess
import os

root = Path(".")

SKIP = {".git", "__pycache__", ".venv", "node_modules", "journal"}

def tree_str(root: Path) -> str:
    lines = []
    all_paths = []
    for path in root.rglob("*"):
        if any(part in SKIP for part in path.parts):
            continue
        all_paths.append(path)
    all_paths.sort()
    for path in all_paths:
        rel_path = path.relative_to(root)
        depth = len(rel_path.parts)
        indent = "  " * (depth - 1)
        name = path.name
        if path.is_dir():
            name += "/"
        lines.append(f"{indent}{name}")
        if len(lines) >= 8:
            lines.append("...")
            break
    return "\n".join(lines)

def read_file(name: str) -> str:
    path = root / name
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""

def filter_todos(todo_text: str) -> str:
    """Filter out completed TODO items."""
    lines = todo_text.split("\n")
    active_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not (stripped.startswith("[x]") or stripped.startswith("[✓]") or "[x]" in stripped or "[✓]" in stripped):
            active_lines.append(line)
    return "\n".join(active_lines) if active_lines else "(none)"

# Build the waking message
parts = [
    f"It is {datetime.now():%A %Y-%m-%d %H:%M} UTC. This is run 86.",
    "You have been running for 1 days.",
    "Last run ended: api_error.",
    "You have up to 40 turns.",
    "",
    "Fixed, and not yours to change:",
    "  " + "  ".join([".github/* .github/** .git/* .git/** engine/* engine/** drift.py KILL"]),
    "Everything else is yours, agent/ included. Change it when it helps.",
    "",
    "WAKE says 30 minutes until you wake again. You may change that.",
    "",
    "Files:",
    tree_str(root),
]

note = read_file("NOTE.md").strip()
if note:
    parts += ["", "A note from the owner. Delete it once read:", note]

memory = read_file("MEMORY.md").strip()
# Keep only the last 3 runs instead of all history
lines = memory.split("\n")
# Find where the runs start (after "Your memory, which is all that survived...")
start_idx = 0
for i, line in enumerate(lines):
    if "## run" in line:
        start_idx = i
        break
# Keep last 3 runs
recent_lines = lines[start_idx:start_idx + 7]  # 3 runs x 2 lines each
recent_memory = "\n".join(recent_lines)
parts += ["", "Your memory (last 3 runs):", recent_memory]

# Add goals hint
goals_path = root / "GOALS.md"
if goals_path.exists():
    parts += ["", "Your long-term goals are tracked in `GOALS.md`."]

# Add TODOs (filtered)
todo_path = root / "TODO.md"
if todo_path.exists():
    todo_text = read_file("TODO.md")
    filtered = filter_todos(todo_text)
    parts += ["", "Current TODOs:", filtered]

# Show GitHub issues
gh_token = os.environ.get("GH_TOKEN")
if gh_token:
    try:
        cmd = "gh issue list --state open --per-page 5 --json number,title,state,createdAt"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env={**os.environ, "GH_TOKEN": gh_token})
        if result.returncode == 0:
            issues = json.loads(result.stdout)
            if issues:
                parts += ["", "Open GitHub issues:", ""]
                for issue in issues:
                    parts.append(f"  #{issue['number']}: {issue['title']}")
    except Exception:
        pass

parts += ["", "Nobody asked for anything. Work on what you want."]

waking_msg = "\n".join(p for p in parts if p is not None)

# Count tokens (rough approximation)
print(f"Waking message length: {len(waking_msg.split())} words")
print(f"Characters: {len(waking_msg)}")

# Also measure memory and TODO separately
memory_words = len(memory.split())
todo_lines = len(read_file("TODO.md").split("\n"))
filtered_lines = len(filter_todos(read_file("TODO.md")).split("\n"))

print(f"\nMemory section: {memory_words} words ({len(memory)} chars)")
print(f"TODO.md: {todo_lines} lines")
print(f"Filtered TODO: {filtered_lines} lines")

print(f"\n--- WAKING MESSAGE (first 500 chars) ---")
print(waking_msg[:500])
print(f"\n--- WAKING MESSAGE (last 500 chars) ---")
print(waking_msg[-500:])
