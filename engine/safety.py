"""The floor. Small on purpose.

It does not stop the agent changing itself. It stops changes that would leave
it unable to change itself again, and it keeps a live credential out of a
public repository.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

from engine import guard

SECRETS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL")

SMOKE = """
from pathlib import Path
from agent import tools

# everything the loop reaches for. Losing any of it strands every future run.
assert callable(tools.schema), "tools.schema is gone"
assert issubclass(tools.Stopped, Exception), "tools.Stopped is gone"
names = [t["function"]["name"] for t in tools.schema()]
for required in ("read", "write", "run", "stop"):
    assert required in names, f"the {required} tool is gone"

ex = tools.Executor(root=Path(".").resolve(), env={})
out = ex.dispatch("read", {"path": "MEMORY.md"})
assert "AttributeError" not in out and "NameError" not in out, out
assert "refused" in ex.dispatch("write", {"path": "KILL", "content": "x"})
"""


def take_key(name: str) -> tuple[str, dict[str, str]]:
    """Read the API key, then scrub it from the environment the shell inherits.

    GH_TOKEN survives on purpose: it is how the agent reads its own issues, it
    is scoped to this repository, and it dies with the job.
    """
    key = os.environ.get(name, "")
    child = {k: v for k, v in os.environ.items()
             if not any(s in k.upper() for s in SECRETS)}
    if os.environ.get("GH_TOKEN"):
        child["GH_TOKEN"] = os.environ["GH_TOKEN"]
    for k in list(os.environ):
        if any(s in k.upper() for s in SECRETS):
            os.environ.pop(k, None)
    return key, child


def redact(root: Path, values: list[str]) -> None:
    """Scrub credentials out of anything about to be committed."""
    live = [v for v in values if v and len(v) > 12]
    if not live:
        return
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        clean = text
        for value in live:
            clean = clean.replace(value, "[redacted]")
        if clean != text:
            path.write_text(clean, encoding="utf-8")


def _revert(root: Path, paths: list[str]) -> None:
    for rel in paths:
        done = subprocess.run(["git", "checkout", "HEAD", "--", rel],
                              cwd=root, check=False)
        if done.returncode != 0:
            (root / rel).unlink(missing_ok=True)


def check(root: Path) -> list[str]:
    """Undo edits that leave the agent unable to edit again. Only those.

    Two failures, and they are the same failure: code that will not parse, and
    tools that no longer work. Everything else stands, bad ideas included.
    """
    undone = []

    broken = []
    for path in root.rglob("*.py"):
        if ".git" in path.parts:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            broken.append(path.relative_to(root).as_posix())
    if broken:
        _revert(root, broken)
        undone += [f"reverted, would not parse: {b}" for b in broken]

    smoke = subprocess.run([sys.executable, "-c", SMOKE], cwd=root,
                           capture_output=True, text=True)
    if smoke.returncode != 0:
        changed = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "*.py"],
                                 cwd=root, capture_output=True, text=True).stdout.split()
        _revert(root, changed)
        undone += [f"reverted, tools stopped working: {c}" for c in changed]

    for rel in guard.trespasses(root):
        _revert(root, [rel])
        undone.append(f"reverted, engine is not yours: {rel}")

    return undone
