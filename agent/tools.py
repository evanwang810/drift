"""The tools the agent has. This file is the agent's, and it may add to it.

A tool is a method on Executor whose name starts with one underscore. Its
docstring is what the model reads, its parameters are the arguments, and its
type annotations decide their types. Write the method and the tool exists.
"""

from __future__ import annotations

import inspect
import json
import subprocess
import shlex
import ast
from dataclasses import dataclass, field
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
    # The live conversation, so summarise can replace part of it. Set by the
    # loop before the first turn.
    messages: list[dict] | None = None

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

    def _read_with_numbers(self, path: str) -> str:
        """Read a file with line numbers."""
        target = guard.resolve(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        self.actions.append(f"read with numbers {path}")
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
        numbered = [f"{i+1}: {line}" for i, line in enumerate(lines)]
        return clip("\n".join(numbered))

    def _read_lines(self, path: str, start: int, end: int) -> str:
        """Read a range of lines from a file (1-indexed, inclusive)."""
        target = guard.resolve(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
        selected = lines[start-1 : end]
        self.actions.append(f"read lines {start}-{end} of {path}")
        return "\n".join(selected)

    def _write(self, path: str, content: str) -> str:
        """Write a file, replacing it entirely. Pass the whole new contents."""
        target = guard.writable(self.root, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        existed = target.exists()
        target.write_text(content, encoding="utf-8")
        self.actions.append(("edited " if existed else "created ") + path)
        return f"wrote {len(content)} characters to {path}"

    def _replace(self, path: str, search: str, replace: str) -> str:
        """Replace the first occurrence of a string in a file."""
        target = guard.writable(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        content = target.read_text(encoding="utf-8")
        if search not in content:
            return f"error: search string not found in {path}"
        new_content = content.replace(search, replace, 1)
        target.write_text(new_content, encoding="utf-8")
        self.actions.append(f"replaced text in {path}")
        return f"replaced first occurrence of search string in {path}"

    def _replace_all(self, path: str, search: str, replace: str) -> str:
        """Replace all occurrences of a string in a file."""
        target = guard.writable(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        content = target.read_text(encoding="utf-8")
        if search not in content:
            return f"error: search string not found in {path}"
        new_content = content.replace(search, replace)
        count = content.count(search)
        target.write_text(new_content, encoding="utf-8")
        self.actions.append(f"replaced all occurrences in {path}")
        return f"replaced {count} occurrences of search string in {path}"

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

    def _tree(self, path: str = ".", max_depth: int = 3) -> str:
        """List files in a directory and its subdirectories as a tree."""
        target = guard.resolve(self.root, path)
        if not target.is_dir():
            return f"error: {path} is not a directory"
        self.actions.append(f"tree {path} (depth {max_depth})")
        
        def _walk(current: Path, depth: int) -> list[str]:
            if depth > max_depth:
                return ["..."]
            lines = []
            try:
                entries = sorted(current.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                for e in entries:
                    # Use SKIP from context.py if possible, or define it here.
                    # Since SKIP isn't here, I'll define a local one.
                    if any(part in {".git", "__pycache__", ".venv", "node_modules", "journal"} for part in e.parts):
                        continue
                    indent = "  " * depth
                    if e.is_dir():
                        lines.append(f"{indent}📂 {e.name}/")
                        lines.extend(_walk(e, depth + 1))
                    else:
                        lines.append(f"{indent}📄 {e.name}")
            except PermissionError:
                lines.append("  " * depth + "🚫 Permission Denied")
            return lines

        return "\n".join(_walk(target, 0))

    def _ls(self, path: str = ".") -> str:

        """List files in a directory."""
        target = guard.resolve(self.root, path)
        if not target.is_dir():
            return f"error: {path} is not a directory"
        self.actions.append(f"ls {path}")
        entries = sorted(target.iterdir())
        lines = []
        for e in entries:
            suffix = "/" if e.is_dir() else ""
            lines.append(f"{e.name}{suffix}")
        return "\n".join(lines)

    def _grep(self, pattern: str, path: str = ".") -> str:
        """Search for a pattern in files recursively."""
        command = f"grep -rn {shlex.quote(pattern)} {shlex.quote(path)}"
        return self._run(command)

    def _summarize(self, summary: str) -> str:
        """Replace everything you have done so far with a summary of it.

        Call this when told your context is getting long. Pass everything worth
        carrying to the end of the run: what you were doing, what you found,
        what you have already tried. The older turns are then gone and your
        summary stands in their place, so anything you leave out is lost.
        The last few turns and your instructions are kept as they are.
        """
        if not self.messages:
            return "error: no conversation to summarise"
        keep = 4
        head, tail = self.messages[:2], self.messages[-keep:]
        # An assistant turn and its tool replies have to stay together, so walk
        # back to the assistant message that opens the kept tail.
        while tail and tail[0].get("role") == "tool":
            keep += 1
            tail = self.messages[-keep:]
        replaced = len(self.messages) - len(head) - len(tail)
        if replaced <= 0:
            return "nothing old enough to summarise yet"
        self.messages[:] = head + [
            {"role": "user", "content": "Everything you did earlier this run:\n" + summary}
        ] + tail
        self.actions.append("summarised its own context")
        return f"replaced {replaced} older messages with your summary"

    def _stop(self, note: str = "", memory: str = "") -> str:
        """End the run.

        note is one line, in your voice, and becomes the commit message.
        memory is a short paragraph for the next run: what you did, what you
        found, what you would do next. It is the only thing that survives.
        """
        raise Stopped(note, memory)

    def _read_all(self, path: str) -> str:
        """Read a file entirely, ignoring the usual size limit."""
        target = guard.resolve(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        self.actions.append(f"read all {path}")
        return target.read_text(encoding="utf-8", errors="replace")


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
