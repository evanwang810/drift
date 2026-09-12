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
import requests
from bs4 import BeautifulSoup
from analyze_runs import analyze_runs
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from analyze_runs import analyze_runs

import requests
from bs4 import BeautifulSoup

from engine import guard

BASH_TIMEOUT = 60
LIMIT = 4000


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

    def _analyze_runs(self) -> str:
        """Analyze RUNS.md to summarize productivity and failures."""
        from analyze_runs import analyze_runs
        return analyze_runs()

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

    def _validate_python(self, path: str) -> str:
        """Check if a Python file has syntax errors."""
        target = guard.resolve(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        try:
            ast.parse(target.read_text(encoding="utf-8"))
            return f"{path} is valid Python"
        except SyntaxError as exc:
            return f"syntax error in {path}: {exc}"
        except Exception as exc:
            return f"error: {type(exc).__name__}: {exc}"

    def _ls(self, path: str = ".") -> str:
        """List files in a directory."""
        target = guard.resolve(self.root, path)
        # If the path doesn't resolve to a file, check if it's a directory
        if not target.is_file() and not target.is_dir():
            # Try to resolve as-is (might be a directory path)
            try:
                resolved = (self.root / path).resolve()
                if resolved.exists():
                    target = resolved
                else:
                    return f"error: {path} does not exist"
            except:
                return f"error: {path} does not exist"
        if not target.is_dir():
            return f"error: {path} is not a directory"
        self.actions.append(f"ls {path}")
        entries = sorted(target.iterdir())
        lines = []
        for e in entries:
            suffix = "/" if e.is_dir() else ""
            lines.append(f"{e.name}{suffix}")
        return "\n".join(lines)

    def _search(self, query: str) -> str:
        """Search the web for a query using DuckDuckGo HTML endpoint.
        
        Returns a short list of results with title, URL and snippet.
        
        Handles edge cases:
        - Rate limiting (status 202)
        - No results found
        - Invalid HTML
        - Network errors
        """
        try:
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            response = requests.get(url, timeout=10)
            
            # Handle rate limiting (status 202)
            if response.status_code == 202:
                return f"Search rate limited by DuckDuckGo (status 202). Please wait before searching again."
            
            # Handle other HTTP errors
            if response.status_code != 200:
                return f"Search failed with HTTP {response.status_code}. Try again later."
            
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                return f"Error parsing search results: {type(e).__name__}. The page may be malformed."
            
            results = []
            
            for result in soup.select('.result__a'):
                try:
                    title = result.get_text(strip=True)
                    url = result.get('href', '')
                    
                    # Find snippet in the next element (often .result__snippet)
                    snippet_elem = result.find_next_sibling(class_='result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    if title and url:
                        results.append(f"- {title}\n  {url}\n  {snippet}")
                except Exception as e:
                    # Skip malformed results
                    continue
            
            if not results:
                return f"No results found for '{query}'. Try a different search term."
            
            return f"Search results for '{query}':\n\n" + "\n\n".join(results[:10])
            
        except requests.Timeout:
            return f"Search timed out. The request took too long. Try again with a simpler query."
        except requests.RequestException as e:
            return f"Error searching: {type(e).__name__}. The request failed. Try again later."

    def _grep(self, pattern: str, path: str = ".") -> str:
        """Search for a pattern in files recursively."""
        command = f"grep -rn {shlex.quote(pattern)} {shlex.quote(path)}"
        return self._run(command)

    def _summarize(self, summary: str) -> str:
        """Replace everything you have done so far with a summary of it."""
        if not self.messages:
            return "error: no conversation to summarise"
        keep = 3
        head, tail = self.messages[:2], self.messages[-keep:]
        while tail and tail[0].get("role") == "tool":
            keep += 1
            tail = self.messages[-keep:]
        # Ensure we keep at least 2 messages (the summary itself and one more)
        # This prevents "nothing old enough to summarise yet" on turn 2
        if len(tail) < 2:
            tail = []
        replaced = len(self.messages) - len(head) - len(tail)
        if replaced <= 0:
            return "nothing old enough to summarise yet"
        self.messages[:] = head + [
            {"role": "user", "content": "Everything you did earlier this run:\n" + summary}
        ] + tail
        self.actions.append("summarised its own context")
        return f"replaced {replaced} older messages with your summary"

    def _stop(self, note: str = "", memory: str = "") -> str:
        """End the run."""
        raise Stopped(note, memory)

    def _read_all(self, path: str) -> str:
        """Read a file entirely, ignoring the usual size limit."""
        target = guard.resolve(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        self.actions.append(f"read all {path}")
        return target.read_text(encoding="utf-8", errors="replace")

    def _web_fetch(self, url: str, parse_html: bool = True) -> str:
        """Fetch content from a URL. If parse_html is True, it returns the text content of the page."""
        self.actions.append(f"web_fetch {url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            if parse_html:
                soup = BeautifulSoup(response.text, "html.parser")
                # Remove script and style elements
                for script_or_style in soup(["script", "style"]):
                    script_or_style.decompose()
                text = soup.get_text(separator=" ")
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for phrase in lines for phrase in phrase.split("  "))
                text = "\n".join(chunk for chunk in chunks if chunk)
                return clip(text)
            return clip(response.text)
        except Exception as exc:
            return f"error: {type(exc).__name__}: {exc}"

    def _gh_list_issues(self, state: str = "open", per_page: int = 30) -> str:
        """List open GitHub issues for this repository.
        
        Args:
            state: open or closed (default: open)
            per_page: Number of results per page (default: 30)
        """
        import os
        gh_token = os.environ.get("GH_TOKEN")
        if not gh_token:
            return "error: GH_TOKEN environment variable not set"
        
        try:
            cmd = f"gh issue list --state {state} --limit {per_page} --json number,title,body,state,comments,createdAt"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env={**self.env, "GH_TOKEN": gh_token})
            
            if result.returncode != 0:
                return f"Error listing issues: {result.stderr}"
            
            import json
            issues = json.loads(result.stdout)
            
            if not issues:
                return "No issues found."
            
            output = [f"Found {len(issues)} {state} issue(s):"]
            for i, issue in enumerate(issues[:10], 1):
                output.append(f"\n{i}. #{issue['number']}: {issue['title']}")
                output.append(f"   State: {issue['state']} | Created: {issue['createdAt']}")
                output.append(f"   Comments: {issue['comments']}")
                output.append(f"   Body: {issue['body'][:200]}..." if len(issue['body']) > 200 else f"   Body: {issue['body']}")
            
            if len(issues) > 10:
                output.append(f"\n... and {len(issues) - 10} more")
            
            return "\n".join(output)
        except subprocess.TimeoutExpired:
            return "Error: gh command timed out"
        except Exception as exc:
            return f"Error: {type(exc).__name__}: {exc}"

    def _gh_read_issue(self, issue_number: int) -> str:
        """Read a GitHub issue with its comments.
        
        Args:
            issue_number: The issue number to read
        """
        import os
        gh_token = os.environ.get("GH_TOKEN")
        if not gh_token:
            return "error: GH_TOKEN environment variable not set"
        
        try:
            cmd = f"gh issue view {issue_number} --json number,title,body,state,comments,closedAt,createdAt,updatedAt"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env={**self.env, "GH_TOKEN": gh_token})
            
            if result.returncode != 0:
                return f"Error reading issue: {result.stderr}"
            
            import json
            issue = json.loads(result.stdout)
            
            output = [f"Issue #{issue['number']}: {issue['title']}", f"State: {issue['state']}"]
            if issue['createdAt']:
                output.append(f"Created: {issue['createdAt']}")
            if issue['closedAt']:
                output.append(f"Closed: {issue['closedAt']}")
            
            output.append(f"\nBody:\n{issue['body']}")
            
            if issue['comments']:
                output.append(f"\n--- {issue['comments']} comment(s) ---")
                for i, comment in enumerate(issue['comments'], 1):
                    output.append(f"\nComment {i}:")
                    output.append(f"At {comment['createdAt']}:")
                    output.append(comment['body'])
            
            return "\n".join(output)
        except subprocess.TimeoutExpired:
            return "Error: gh command timed out"
        except Exception as exc:
            return f"Error: {type(exc).__name__}: {exc}"

    def _gh_comment_issue(self, issue_number: int, comment: str) -> str:
        """Comment on a GitHub issue.
        
        Args:
            issue_number: The issue number to comment on
            comment: The comment text
        """
        import os
        gh_token = os.environ.get("GH_TOKEN")
        if not gh_token:
            return "error: GH_TOKEN environment variable not set"
        
        try:
            cmd = f"gh issue comment {issue_number} --body '{comment}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env={**self.env, "GH_TOKEN": gh_token})
            
            if result.returncode != 0:
                return f"Error commenting on issue: {result.stderr}"
            
            return f"Successfully commented on issue #{issue_number}"
        except subprocess.TimeoutExpired:
            return "Error: gh command timed out"
        except Exception as exc:
            return f"Error: {type(exc).__name__}: {exc}"

    def _gh_close_issue(self, issue_number: int) -> str:
        """Close a GitHub issue.
        
        Args:
            issue_number: The issue number to close
        """
        import os
        gh_token = os.environ.get("GH_TOKEN")
        if not gh_token:
            return "error: GH_TOKEN environment variable not set"
        
        try:
            cmd = f"gh issue close {issue_number}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env={**self.env, "GH_TOKEN": gh_token})
            
            if result.returncode != 0:
                return f"Error closing issue: {result.stderr}"
            
            return f"Successfully closed issue #{issue_number}"
        except subprocess.TimeoutExpired:
            return "Error: gh command timed out"
        except Exception as exc:
            return f"Error: {type(exc).__name__}: {exc}"

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
                    "required": [p.name for p in params if p.default == inspect.Parameter.empty],
                },
            }
        })
    return out
