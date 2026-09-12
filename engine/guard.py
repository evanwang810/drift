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
    raw = raw.strip()
    # The repository's own absolute path, as the shell prints it. Stripping the
    # leading slash off that turned /home/runner/work/drift/drift/docs/about.md
    # into docs nested five directories deep inside the repository, and a run
    # built a whole website there while the real one sat untouched.
    for prefix in {root.as_posix().rstrip("/"), root.resolve().as_posix().rstrip("/")}:
        if raw == prefix or raw.startswith(prefix + "/"):
            raw = raw[len(prefix):].lstrip("/") or "."
            if raw == ".":
                raise GuardError("not a file path: the repository root")
            break
    else:
        if raw.startswith("/"):
            head = raw.lstrip("/").split("/", 1)[0]
            # "/docs/x.md" means the repository's docs. "/tmp/x" or "/home/..."
            # names somewhere real on this machine, and quietly recreating it
            # inside the repository is worse than saying no.
            if head and Path("/" + head).exists() and not (root / head).exists():
                raise GuardError(f"{raw} is outside the repository. Paths are"
                                 f" relative to it: the root is {root.as_posix()}")
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
