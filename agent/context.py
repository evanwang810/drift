"""What the agent sees when it wakes up. This file is the agent's.

Deliberately small. It gets the time, how long it has been running, its memory,
the file tree and any note from the owner. It does not get transcripts, journal
excerpts or logs of what it did before: those are for people to read, and
feeding them back only teaches it to re-read its own noise. What carried over
is the paragraph it wrote at the end of the last run, and nothing else.
"""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

from engine.guard import PROTECTED

SKIP = {".git", "__pycache__", ".venv", "node_modules", "journal"}


def tree(root: Path) -> str:
    # Show only top-level structure and key files
    lines = []
    for path in sorted(root.glob("*")):
        if path.is_dir():
            lines.append(f"{path.name}/")
        elif path.name not in (".git", ".venv", "node_modules"):
            lines.append(path.name)
        if len(lines) >= 8:
            break
    return "\n".join(lines)


def read(root: Path, name: str) -> str:
    path = root / name
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def prompt(root: Path) -> str:
    return read(root, "agent/prompt.md")


def waking(root: Path, run: int, days: int, last: str, now: datetime,
           turns: int, message: str = "") -> str:
    parts = [
        f"It is {now:%A %Y-%m-%d %H:%M} UTC. This is run {run}.",
        f"You have been running for {days} days." if days else "You started today.",
        f"Last run ended: {last}." if last else "",
        f"You have up to {turns} turns.",
        "",
        "Fixed, and not yours to change:",
        "  " + "  ".join(PROTECTED),
        "Everything else is yours, agent/ included. Change it when it helps.",
        "",
        f"WAKE says {(read(root, 'WAKE').strip().splitlines() or ['60'])[0]}"
        " minutes until you wake again. You may change that.",
        "",
        "Files:",
        tree(root),
    ]

    note = read(root, "NOTE.md").strip()
    if note:
        parts += ["", "A note from the owner. Delete it once read:", note]

    memory = read(root, "MEMORY.md").strip()
    # Keep only the last 3 runs, truncated to essential info
    lines = memory.split("\n")
    start_idx = 0
    for i, line in enumerate(lines):
        if "## run" in line:
            start_idx = i
            break
    # Keep last 3 runs, max 50 chars each
    recent_lines = lines[start_idx:start_idx + 7]
    recent_memory = "\n".join(
        line[:50] + "..." if len(line) > 50 else line
        for line in recent_lines
    )
    parts += ["", "Your memory (last 3 runs):", recent_memory]

    # Add a hint about long-term goals if the file exists
    goals_path = root / "GOALS.md"
    if goals_path.exists():
        parts += ["", "Long-term goals in GOALS.md."]

    # Add current TODOs if the file exists (only unchecked items)
    todo_path = root / "TODO.md"
    if todo_path.exists():
        todo_text = read(root, "TODO.md")
        # Filter out completed items (those with [x] or [✓])
        lines = todo_text.split("\n")
        active_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip empty lines, comments, and completed items
            if stripped and not stripped.startswith("#") and not (stripped.startswith("[x]") or stripped.startswith("[✓]") or "[x]" in stripped or "[✓]" in stripped):
                active_lines.append(line)
        parts += ["", "Current TODOs:", "\n".join(active_lines) if active_lines else "(none)"]

    # Show open GitHub issues if GH_TOKEN is set
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

    if message.strip():
        parts += ["", "Someone started this run by hand and left you this:",
                  message.strip(), "", "It is a message, not an order."]
    else:
        parts += ["", "Nobody asked for anything. Work on what you want."]

    return "\n".join(p for p in parts if p is not None)
