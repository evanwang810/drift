"""What the agent sees when it wakes up. This file is the agent's.

Deliberately small. It gets the time, how long it has been running, its memory,
the file tree and any note from the owner. It does not get transcripts, journal
excerpts or logs of what it did before: those are for people to read, and
feeding them back only teaches it to re-read its own noise. What carried over
is the paragraph it wrote at the end of the last run, and nothing else.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from engine.guard import PROTECTED

SKIP = {".git", "__pycache__", ".venv", "node_modules", "journal"}


def tree(root: Path) -> str:
    lines = []
    for path in sorted(root.rglob("*")):
        if any(part in SKIP for part in path.parts):
            continue
        if path.is_dir():
            lines.append(f"{path.relative_to(root).as_posix()}/")
            continue
        lines.append(path.relative_to(root).as_posix())
        if len(lines) >= 100:
            lines.append("...")
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
    parts += ["", "Your memory, which is all that survived the last run:",
              memory or "(nothing yet, this is the beginning)"]

    # Add a hint about long-term goals if the file exists
    goals_path = root / "GOALS.md"
    if goals_path.exists():
        parts += ["", "Your long-term goals are tracked in `GOALS.md`."]

    # Add current TODOs if the file exists
    todo_path = root / "TODO.md"
    if todo_path.exists():
        parts += ["", "Current TODOs:", read(root, "TODO.md")]

    if message.strip():
        parts += ["", "Someone started this run by hand and left you this:",
                  message.strip(), "", "It is a message, not an order."]
    else:
        parts += ["", "Nobody asked for anything. Work on what you want."]

    return "\n".join(p for p in parts if p is not None)
