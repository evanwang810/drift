"""How memory works between runs. This file is the agent's.

The engine guarantees only one thing: at the end of every run it calls `write`
with what that run wants to carry forward, and if this module raises it falls
back to appending a plain entry so nothing is ever lost. Everything else about
the shape of memory is decided here, and can be changed here.

The current shape is a standing summary plus a chain of recent entries.

The standing summary is everything above the first `## run` heading. It is never
rotated and never truncated by this module. It is the place for things that stay
true: how the repository is laid out, what has been tried and failed, what the
owner has asked for, what was learned about the environment. Rewrite it, do not
append to it.

Below it, one entry per run, newest first. These are the raw record. The
standing summary is a lossy rewrite of the past and it can drift; the entries
are what actually happened, and they are what it gets checked against.

When the whole file grows past `LIMIT`, the engine will say so on waking and ask
for it to be compacted. Compaction means folding the oldest entries up into the
standing summary and deleting them, keeping what still matters. Losing detail is
the cost of compaction, so compact as losslessly as the budget allows: prefer
dropping things that are recorded elsewhere, since RUNS.md and git log are exact
and do not need repeating here.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

# Roughly how large MEMORY.md may get, in characters, before the engine asks
# for a compaction. Three characters to a token, so this is about 10k tokens,
# which is comfortable against a context ceiling several times that.
LIMIT = 30000

# Entries below this many are never dropped by a compaction nudge, so that a
# burst of failed runs cannot empty the recent record.
FLOOR = 3

OPENING = """# memory

## what I know

Nothing yet. This section is mine to rewrite. It survives compaction, so
anything that should outlive the last few runs belongs here.
"""


def split(text: str) -> tuple[str, list[str]]:
    """Separate the standing summary from the dated run entries."""
    head, sep, rest = text.partition("\n## run ")
    if not sep:
        return text.rstrip() or OPENING.rstrip(), []
    entries = re.split(r"(?=^## run )", sep + rest, flags=re.M)
    return head.rstrip(), [e for e in entries if e.strip().startswith("## run")]


def size(root: Path) -> int:
    path = root / "MEMORY.md"
    return len(path.read_text(encoding="utf-8")) if path.is_file() else 0


def crowded(root: Path) -> bool:
    """Whether the engine should ask for a compaction on the next waking."""
    head, entries = split(read(root))
    return size(root) > LIMIT and len(entries) > FLOOR


def read(root: Path) -> str:
    path = root / "MEMORY.md"
    return path.read_text(encoding="utf-8") if path.is_file() else OPENING


def write(root: Path, run: int, outcome: str, text: str, now: datetime) -> None:
    """Add this run's entry. The standing summary above it is left alone.

    Nothing is dropped here. Memory only shrinks when it is compacted
    deliberately, which is a decision made with the content in front of it
    rather than by a counter that cannot read.
    """
    head, entries = split(read(root))
    entry = f"## run {run} | {now:%Y-%m-%d} | {outcome}\n\n{text.strip()}\n\n"
    (root / "MEMORY.md").write_text(
        head + "\n\n" + entry + "".join(entries), encoding="utf-8"
    )
