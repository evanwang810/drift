"""What the agent may not change.

The line is between how it runs and what it does. engine/ and drift.py are the
first: API client, rate limiting, the loop. Break those and there is no next run
to fix them from. Everything else is the agent's.
"""

from __future__ import annotations

import fnmatch
import subprocess
from pathlib import Path

PROTECTED = (".github/*", ".github/**", ".git/*", ".git/**",
             "engine/*", "engine/**", "drift.py", "KILL")


class GuardError(PermissionError):
    """The agent reached somewhere it is not allowed to reach."""


def resolve(root: Path, raw: str) -> Path:
    """Resolve a relative path, refusing anything outside the repository."""
    if not raw or raw.strip() in (".", "/"):
        raise GuardError(f"not a file path: {raw!r}")
    target = (root / raw.lstrip("/")).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        raise GuardError(f"{raw} is outside the repository") from None
    return target


def is_protected(rel: str) -> bool:
    return any(fnmatch.fnmatch(rel, pattern) for pattern in PROTECTED)


def writable(root: Path, raw: str) -> Path:
    """Resolve for writing. Raises on anything in the engine."""
    target = resolve(root, raw)
    rel = target.resolve().relative_to(root.resolve()).as_posix()
    if is_protected(rel):
        raise GuardError(f"{rel} is engine code. Everything outside engine/ is yours.")
    return target


def trespasses(root: Path) -> list[str]:
    """Protected files that changed anyway, usually via the shell."""
    out = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root, capture_output=True, text=True,
    )
    changed = [ln[3:].strip().strip('"') for ln in out.stdout.splitlines() if ln.strip()]
    return [path for path in changed if is_protected(path)]
