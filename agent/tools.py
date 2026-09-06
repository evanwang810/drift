"""The tools the agent has. This file is the agent's, and it may add to it.

A tool is a method on Executor whose name starts with one underscore. Its
docstring is what the model reads, its parameters are the arguments, and its
type annotations decide their types. Write the method and the tool exists.
"""

from __future__ import annotations

import inspect
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from engine import guard

BASH_TIMEOUT = 60
LIMIT = 12000


class Stopped(Exception):
    """The agent chose to end its run."""

    def __init__(self, note: str, memory: str = "") -> None:
        super().__init__(note)
        self.note = note.strip() or "(no note)"
        self.memory = memory.strip()


def clip(text: str, limit: int = LIMIT) -> str:
    """Cut on a line boundary, and count in lines so the numbers mean something."""
    if len(text) <= limit:
        return text
    lines = text.splitlines()
    shown = text[:limit].splitlines()[:-1] or lines[:1]
    return "\n".join(shown) + f"\n... [{len(shown)} of {len(lines)} lines]"


@dataclass
class Executor:
    root: Path
    env: dict[str, str]
    actions: list[str] = field(default_factory=list)

    def dispatch(self, name: str, args: dict[str, Any]) -> str:
        handler = getattr(self, f"_{name}", None)
        if handler is None or name.startswith("_"):
            return f"error: no such tool {name!r}"
        try:
            return handler(**args)
        except Stopped:
            raise
        except guard.GuardError as exc:
            self.actions.append(f"blocked {name}")
            return f"refused: {exc}"
        except TypeError as exc:
            return f"error: bad arguments for {name}: {exc}"
        except Exception as exc:  # noqa: BLE001 - shown to the model verbatim
            self.actions.append(f"failed {name}: {type(exc).__name__}")
            return f"error: {type(exc).__name__}: {exc}"

    def _read(self, path: str) -> str:
        """Read a file."""
        target = guard.resolve(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        self.actions.append(f"read {path}")
        return clip(target.read_text(encoding="utf-8", errors="replace"))

    def _write(self, path: str, content: str) -> str:
        """Write a file, replacing it entirely. Pass the whole new contents."""
        target = guard.writable(self.root, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        existed = target.exists()
        target.write_text(content, encoding="utf-8")
        self.actions.append(("edited " if existed else "created ") + path)
        return f"wrote {len(content)} characters to {path}"

    def _delete(self, path: str) -> str:
        """Delete a file. Only git history undoes this."""
        target = guard.writable(self.root, path)
        if not target.is_file():
            return f"error: {path} is not a file"
        target.unlink()
        self.actions.append(f"deleted {path}")
        return f"deleted {path}"

    def _run(self, command: str) -> str:
        """Run a shell command in the repository root. Network is available."""
        self.actions.append(f"ran: {command[:100]}")
        try:
            done = subprocess.run(
                command, shell=True, cwd=self.root, env=self.env,
                capture_output=True, text=True, timeout=BASH_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return f"killed after {BASH_TIMEOUT}s"
        parts = [f"exit {done.returncode}"]
        if done.stdout.strip():
            parts.append(done.stdout.rstrip())
        if done.stderr.strip():
            parts.append("stderr: " + done.stderr.rstrip())
        return clip("\n".join(parts))

    def _stop(self, note: str = "", memory: str = "") -> str:
        """End the run.

        note is one line, in your voice, and becomes the commit message.
        memory is a short paragraph for the next run: what you did, what you
        found, what you would do next. It is the only thing that survives.
        """
        raise Stopped(note, memory)


def schema() -> list[dict[str, Any]]:
    """Every tool, described from its own signature and docstring."""
    kinds = {"int": "integer", "float": "number", "bool": "boolean"}
    out = []
    for name, function in inspect.getmembers(Executor, inspect.isfunction):
        if not name.startswith("_") or name.startswith("__"):
            continue
        params = list(inspect.signature(function).parameters.values())[1:]
        out.append({
            "type": "function",
            "function": {
                "name": name[1:],
                "description": inspect.getdoc(function) or "",
                "parameters": {
                    "type": "object",
                    "properties": {
                        p.name: {"type": kinds.get(
                            getattr(p.annotation, "__name__", p.annotation), "string")}
                        for p in params
                    },
                    "required": [
                        p.name for p in params
                        if p.default is inspect.Parameter.empty
                    ],
                },
            },
        })
    return out


def parse_args(raw: str) -> dict[str, Any]:
    """Arguments arrive as a JSON string and are not always valid."""
    try:
        return json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {}
