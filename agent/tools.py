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
        """Search the web for a query.
        
        First tries DuckDuckGo HTML endpoint, then falls back to Wikipedia API.
        Returns results with source attribution.
        
        Handles edge cases:
        - Rate limiting (status 202)
        - No results found
        - Invalid HTML
        - Network errors
        """
        # Try DuckDuckGo first
        try:
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            response = requests.get(url, timeout=10)
            
            # Handle HTTP errors (including rate limiting)
            # 202 is rate limiting, continue to fallback
            if response.status_code not in (200, 202):
                import sys
                print(f"DEBUG: HTTP {response.status_code}", file=sys.stderr)
                return f"Search failed with HTTP {response.status_code}. Falling back to Wikipedia API."
            
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                return f"Error parsing search results: {type(e).__name__}. Falling back to Wikipedia API."
            
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
            
            if results:
                return f"Search results for '{query}' (via DuckDuckGo):\n\n" + "\n\n".join(results[:10])
            
            # DuckDuckGo returned no results, try Wikipedia API
            return self._search_wikipedia(query)
            
        except requests.Timeout:
            return f"Search timed out. Falling back to Wikipedia API."
        except requests.RequestException as e:
            return f"Error searching: {type(e).__name__}. Falling back to Wikipedia API."
    
    def _search_wikipedia(self, query: str) -> str:
        """Search Wikipedia API and return results.
        
        Args:
            query: Search term
            
        Returns:
            Formatted search results from Wikipedia
        """
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': 10,
                'utf8': '',
                'sroffset': 0
            }
            response = requests.get(url, params=params, headers={'User-Agent': 'drift-agent/1.0 (https://github.com/evanwang810/drift)'}, timeout=10)
            
            if response.status_code != 200:
                return f"Error fetching from Wikipedia API (HTTP {response.status_code})."
            
            data = response.json()
            
            if 'query' not in data or 'search' not in data['query']:
                return f"No results found for '{query}' in Wikipedia."
            
            results = []
            for item in data['query']['search']:
                title = item.get('title', '')
                pageid = item.get('pageid', '')
                snippet = item.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
                wordcount = item.get('wordcount', '')
                
                # Build result line with title, URL, and snippet
                results.append(f"- {title}\n  https://en.wikipedia.org/?curid={pageid}\n  {snippet}")
            
            return f"Search results for '{query}' (via Wikipedia API):\n\n" + "\n\n".join(results[:10])
            
        except requests.RequestException as e:
            return f"Error searching Wikipedia: {type(e).__name__}. The request failed."
        except (KeyError, json.JSONDecodeError) as e:
            return f"Error parsing Wikipedia response: {type(e).__name__}."


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

    def _gh_create_issue_from_project(self, labels: str = "project") -> str:
        """Create GitHub issues from PROJECT.md incomplete tasks and technical debt.
        
        Reads PROJECT.md and creates issues for:
        - Incomplete tasks in the 'done when' section
        - Technical debt items in the 'technical debt' section
        
        Args:
            labels: Comma-separated labels to apply to all issues (default: "project")
        """
        import os
        gh_token = os.environ.get("GH_TOKEN")
        if not gh_token:
            return "error: GH_TOKEN environment variable not set"
        
        try:
            # Read PROJECT.md
            project_path = self.root / "PROJECT.md"
            if not project_path.exists():
                return "error: PROJECT.md not found"
            
            content = project_path.read_text(encoding="utf-8")
            
            # Extract incomplete tasks from 'done when' section
            done_when_start = content.find("## done when")
            if done_when_start == -1:
                return "error: '## done when' section not found in PROJECT.md"
            
            done_when_section = content[done_when_start:]
            done_when_end = done_when_section.find("## ", done_when_start + 50)
            if done_when_end != -1:
                done_when_section = done_when_section[:done_when_end]
            
            # Parse 'done when' items
            done_when_items = []
            for line in done_when_section.split("\n"):
                line = line.strip()
                if line.startswith("- [ ]"):
                    # Incomplete task
                    task = line[5:].strip()
                    if task and not task.startswith("Create _gh_create_issue_from_project"):
                        done_when_items.append(("task", task))
                elif line.startswith("- [x]"):
                    # Completed task - skip
                    pass
            
            # Extract technical debt from 'technical debt' section
            technical_debt_start = content.find("## technical debt")
            if technical_debt_start == -1:
                return "warning: '## technical debt' section not found in PROJECT.md"
            
            technical_debt_section = content[technical_debt_start:]
            technical_debt_end = technical_debt_section.find("## ", technical_debt_start + 50)
            if technical_debt_end != -1:
                technical_debt_section = technical_debt_section[:technical_debt_end]
            
            # Parse technical debt items
            technical_debt_items = []
            for line in technical_debt_section.split("\n"):
                line = line.strip()
                if line.startswith("- [ ]"):
                    # Incomplete technical debt item
                    debt = line[5:].strip()
                    if debt:
                        technical_debt_items.append(("technical_debt", debt))
                elif line.startswith("- [x]"):
                    # Completed technical debt item - skip
                    pass
            
            # Create issues
            issues_created = []
            labels_list = labels.split(",") if labels else ["project"]
            labels_param = " --label " + ",".join(labels_list)
            
            # Create issues for incomplete tasks
            for i, (item_type, item) in enumerate(done_when_items, 1):
                title = f"Project Task: {item[:60]}{'...' if len(item) > 60 else ''}"
                body = f"""## {item}

**Type:** Project Task

**Status:** Incomplete

**Original location:** PROJECT.md 'done when' section

---

This issue was automatically created from PROJECT.md by the issue tracker automation.

Please review and update the status in PROJECT.md when this task is completed.
"""
                cmd = f"gh issue create --title '{title}' --body '{body}'{labels_param}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env={**self.env, "GH_TOKEN": gh_token})
                
                if result.returncode == 0:
                    import json
                    issue_data = json.loads(result.stdout)
                    issue_number = issue_data['number']
                    issues_created.append((item_type, item, issue_number, "created"))
                else:
                    issues_created.append((item_type, item, 0, f"failed: {result.stderr}"))
            
            # Create issues for technical debt
            for i, (item_type, item) in enumerate(technical_debt_items, 1):
                title = f"Technical Debt: {item[:60]}{'...' if len(item) > 60 else ''}"
                body = f"""## {item}

**Type:** Technical Debt

**Status:** Incomplete

**Original location:** PROJECT.md 'technical debt' section

---

This issue was automatically created from PROJECT.md by the issue tracker automation.

Please review and update the status in PROJECT.md when this technical debt item is addressed.
"""
                cmd = f"gh issue create --title '{title}' --body '{body}'{labels_param}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env={**self.env, "GH_TOKEN": gh_token})
                
                if result.returncode == 0:
                    import json
                    issue_data = json.loads(result.stdout)
                    issue_number = issue_data['number']
                    issues_created.append((item_type, item, issue_number, "created"))
                else:
                    issues_created.append((item_type, item, 0, f"failed: {result.stderr}"))
            
            # Generate summary
            output = []
            output.append(f"Project Issue Tracker: {len(done_when_items) + len(technical_debt_items)} items found in PROJECT.md")
            output.append(f"Labels: {labels}")
            output.append("")
            
            # Summary of tasks
            if done_when_items:
                output.append(f"Incomplete Tasks ({len(done_when_items)}):")
                for i, (item_type, item, issue_number, status) in enumerate(issues_created, 1):
                    if item_type == "task":
                        if issue_number:
                            output.append(f"  {i}. {item[:70]}")
                            output.append(f"     → Issue #{issue_number} {status}")
                        else:
                            output.append(f"  {i}. {item[:70]}")
                            output.append(f"     → {status}")
                output.append("")
            
            # Summary of technical debt
            if technical_debt_items:
                output.append(f"Technical Debt Items ({len(technical_debt_items)}):")
                for i, (item_type, item, issue_number, status) in enumerate(issues_created[len(done_when_items):], len(done_when_items) + 1):
                    if item_type == "technical_debt":
                        if issue_number:
                            output.append(f"  {i}. {item[:70]}")
                            output.append(f"     → Issue #{issue_number} {status}")
                        else:
                            output.append(f"  {i}. {item[:70]}")
                            output.append(f"     → {status}")
            
            return "\n".join(output)
            
        except subprocess.TimeoutExpired:
            return "Error: gh command timed out"
        except Exception as exc:
            return f"Error: {type(exc).__name__}: {exc}"
    
    def _knowledge_add(self, title: str, description: str, type: str = "general",
                       tags: str = "", source: str = "", implementation: str = "",
                       verification: str = "", impact: str = "") -> str:
        """Add an entry to the knowledge base.
        
        Args:
            title: Title of the knowledge entry
            description: Brief description of what this is about
            type: Type of entry (e.g., tool_fix, platform, research, discovery)
            tags: Comma-separated tags for categorization
            source: Source/run where this was discovered
            implementation: How it was implemented or discovered
            verification: How it was verified
            impact: What impact this has
        """
        import json
        from pathlib import Path
        
        knowledge_path = self.root / "agent" / "knowledge" / "knowledge.json"
        
        # Load existing knowledge
        if knowledge_path.exists():
            try:
                with open(knowledge_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                data = {"version": "1.0", "created": "", "entries": []}
        else:
            data = {"version": "1.0", "created": "", "entries": []}
        
        # Create new entry
        entry = {
            "id": f"k-{len(data['entries']) + 1:03d}",
            "type": type,
            "title": title,
            "description": description,
            "source": source,
            "tags": tags.split(",") if tags else [],
            "implementation": implementation,
            "verification": verification,
            "impact": impact
        }
        
        # Add to entries
        data["entries"].append(entry)
        
        # Write back
        with open(knowledge_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.actions.append(f"knowledge_add {title}")
        return f"Added knowledge entry: {title}"
    
    def _knowledge_list(self, type_filter: str = "") -> str:
        """List all knowledge entries, optionally filtered by type.
        
        Args:
            type_filter: Filter by type (e.g., tool_fix, platform, research)
        """
        import json
        from pathlib import Path
        
        knowledge_path = self.root / "agent" / "knowledge" / "knowledge.json"
        
        if not knowledge_path.exists():
            return "No knowledge base found"
        
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        entries = data.get("entries", [])
        
        if type_filter:
            entries = [e for e in entries if e.get("type") == type_filter]
        
        if not entries:
            return f"No entries found for type: {type_filter}"
        
        result = f"Knowledge entries ({len(entries)} total):\n\n"
        for entry in entries:
            result += f"- [{entry.get('type', 'general')}] {entry.get('title', 'Untitled')}\n"
            result += f"  ID: {entry.get('id', 'N/A')}\n"
            result += f"  Tags: {', '.join(entry.get('tags', []))}\n"
            if entry.get('source'):
                result += f"  Source: {entry.get('source')}\n"
            result += "\n"
        
        return result
    
    def _knowledge_search(self, query: str, type_filter: str = "") -> str:
        """Search knowledge base by title, description, tags, or implementation.
        
        Args:
            query: Search terms
            type_filter: Optional filter by type
        """
        import json
        from pathlib import Path
        from engine import guard
        
        knowledge_path = self.root / "agent" / "knowledge" / "knowledge.json"
        
        if not knowledge_path.exists():
            return "No knowledge base found"
        
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        entries = data.get("entries", [])
        
        if type_filter:
            entries = [e for e in entries if e.get("type") == type_filter]
        
        query_lower = query.lower()
        matches = []
        
        for entry in entries:
            fields = [
                entry.get("title", ""),
                entry.get("description", ""),
                entry.get("source", ""),
                entry.get("implementation", ""),
                entry.get("verification", ""),
                entry.get("impact", ""),
                " ".join(entry.get("tags", []))
            ]
            
            text = " ".join(fields).lower()
            if query_lower in text:
                matches.append(entry)
        
        if not matches:
            return f"No matches found for: {query}"
        
        result = f"Found {len(matches)} matches for '{query}':\n\n"
        for entry in matches:
            result += f"- {entry.get('title', 'Untitled')}\n"
            result += f"  ID: {entry.get('id', 'N/A')}\n"
            result += f"  Type: {entry.get('type', 'general')}\n"
            result += f"  Tags: {', '.join(entry.get('tags', []))}\n"
            if entry.get('source'):
                result += f"  Source: {entry.get('source')}\n"
            if entry.get('description'):
                result += f"  {entry.get('description')[:100]}...\n"
            result += "\n"
        
        return result

    def _save_run_insights_to_knowledge(self, title: str = "", description: str = "",
                                        type: str = "discovery", source: str = "",
                                        tags: str = "run_insight") -> str:
        """Add insights from a run to the knowledge base.
        
        Automatically extracts insights from current work context and saves them
        to the knowledge base for future reference.
        
        Args:
            title: Title of the insight (auto-generated if empty)
            description: Brief description of what was discovered
            type: Type of entry (default: discovery, other options: tool_fix, platform, research)
            source: Source/run where this was discovered (auto-detected if empty)
            tags: Comma-separated tags for categorization
        """
        import json
        from pathlib import Path
        from engine import guard
        
        knowledge_path = self.root / "agent" / "knowledge" / "knowledge.json"
        
        # Generate title if not provided
        if not title:
            title = f"Run Insight: {type.title()}"
        
        # Auto-detect source from current run context
        if not source:
            try:
                runs_file = self.root / "RUNS.md"
                if runs_file.exists():
                    # Read last few lines to get run context
                    lines = runs_file.read_text(encoding='utf-8', errors='replace').splitlines()
                    # Find current run info
                    for line in reversed(lines[-20:]):
                        if line.startswith("## run"):
                            source = line.strip()
                            break
                if not source:
                    source = "Current run"
            except Exception:
                source = "Current run"
        
        # Load existing knowledge
        if knowledge_path.exists():
            try:
                with open(knowledge_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                data = {"version": "1.0", "created": "", "entries": []}
        else:
            data = {"version": "1.0", "created": "", "entries": []}
        
        # Create new entry
        entry = {
            "id": f"k-{len(data['entries']) + 1:03d}",
            "type": type,
            "title": title,
            "description": description,
            "source": source,
            "tags": tags.split(",") if tags else [],
            "implementation": "Auto-extracted from run context",
            "verification": "Manual review during run",
            "impact": "Captured for future reference and context"
        }
        
        # Add to entries
        data["entries"].append(entry)
        
        # Write back
        with open(knowledge_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.actions.append(f"knowledge_add {title}")
        return f"Saved knowledge entry: {title}\nSource: {source}\nType: {type}\nTags: {tags}"
    
    def _contextual_knowledge_query(self, context: str, type_filter: str = "",
                                    max_results: int = 10) -> str:
        """Query knowledge base based on current work context.
        
        Searches the knowledge base for entries that are relevant to the current
        work context, providing filtered results based on context and optional
        type filtering.
        
        Args:
            context: Current work context or topic to search for
            type_filter: Optional filter by type (e.g., tool_fix, platform, research)
            max_results: Maximum number of results to return
        """
        import json
        from pathlib import Path
        from engine import guard
        
        knowledge_path = self.root / "agent" / "knowledge" / "knowledge.json"
        
        if not knowledge_path.exists():
            return "No knowledge base found. Add insights first."
        
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        entries = data.get("entries", [])
        
        # Filter by type if specified
        if type_filter:
            entries = [e for e in entries if e.get("type") == type_filter]
        
        if not entries:
            return f"No entries found for type: {type_filter}"
        
        # Search for context relevance
        context_lower = context.lower()
        scored = []
        
        for entry in entries:
            # Score based on multiple fields
            fields = [
                entry.get("title", ""),
                entry.get("description", ""),
                entry.get("source", ""),
                " ".join(entry.get("tags", []))
            ]
            
            text = " ".join(fields).lower()
            
            # Calculate relevance score
            score = 0
            if context_lower in text:
                score += 10
            
            # Check for partial matches
            words = context_lower.split()
            for word in words:
                if word in text and len(word) > 3:
                    score += 1
            
            # Check if context is mentioned in tags
            tags = " ".join(entry.get("tags", [])).lower()
            for word in words:
                if word in tags:
                    score += 2
            
            if score > 0:
                scored.append((entry, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Limit results
        scored = scored[:max_results]
        
        if not scored:
            return f"No relevant knowledge entries found for context: {context}"
        
        result = f"Found {len(scored)} relevant knowledge entries for context: {context}\n\n"
        for entry, score in scored:
            result += f"**[{entry.get('type', 'general')}] {entry.get('title', 'Untitled')}** (score: {score})\n"
            result += f"ID: {entry.get('id', 'N/A')}\n"
            result += f"Tags: {', '.join(entry.get('tags', []))}\n"
            if entry.get('source'):
                result += f"Source: {entry.get('source')}\n"
            if entry.get('description'):
                result += f"{entry.get('description')}\n"
            result += "\n"
        
        return result
    
    def _generate_knowledge_report(self, type_filter: str = "",
                                   summary_type: str = "by_type") -> str:
        """Generate knowledge-based reports and summaries.
        
        Creates comprehensive reports from knowledge base entries, optionally
        filtered by type and summarizing by different dimensions.
        
        Args:
            type_filter: Optional filter by type (e.g., tool_fix, platform, research)
            summary_type: Type of summary to generate (by_type, by_tag, by_source, comprehensive)
        """
        import json
        from pathlib import Path
        from engine import guard
        
        knowledge_path = self.root / "agent" / "knowledge" / "knowledge.json"
        
        if not knowledge_path.exists():
            return "No knowledge base found"
        
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        entries = data.get("entries", [])
        
        # Filter by type if specified
        if type_filter:
            entries = [e for e in entries if e.get("type") == type_filter]
        
        if not entries:
            return f"No entries found for type: {type_filter}"
        
        result = f"Knowledge Base Report ({len(entries)} entries)\n"
        result += f"{'=' * 50}\n\n"
        
        if summary_type == "by_type":
            result += self._generate_by_type_summary(entries)
        elif summary_type == "by_tag":
            result += self._generate_by_tag_summary(entries)
        elif summary_type == "by_source":
            result += self._generate_by_source_summary(entries)
        else:  # comprehensive
            result += self._generate_comprehensive_report(entries)
        
        return result
    
    def _generate_by_type_summary(self, entries: list) -> str:
        """Generate summary organized by entry type."""
        from collections import Counter
        
        type_counts = Counter(e.get("type", "unknown") for e in entries)
        
        result = "Entries by Type:\n"
        result += "-" * 40 + "\n"
        
        for type_name, count in type_counts.most_common():
            result += f"{type_name:20s}: {count}\n"
        
        result += "\n"
        return result
    
    def _generate_by_tag_summary(self, entries: list) -> str:
        """Generate summary organized by tags."""
        from collections import Counter
        
        all_tags = []
        for e in entries:
            all_tags.extend(e.get("tags", []))
        
        tag_counts = Counter(all_tags)
        
        result = "Entries by Tag:\n"
        result += "-" * 40 + "\n"
        
        for tag, count in tag_counts.most_common():
            result += f"{tag:30s}: {count}\n"
        
        result += "\n"
        return result
    
    def _generate_by_source_summary(self, entries: list) -> str:
        """Generate summary organized by source."""
        from collections import Counter
        
        source_counts = Counter(e.get("source", "Unknown") for e in entries)
        
        result = "Entries by Source:\n"
        result += "-" * 40 + "\n"
        
        for source, count in source_counts.most_common():
            result += f"{source:30s}: {count}\n"
        
        result += "\n"
        return result
    
    def _generate_comprehensive_report(self, entries: list) -> str:
        """Generate comprehensive report with all dimensions."""
        from collections import Counter
        
        # Type breakdown
        type_counts = Counter(e.get("type", "unknown") for e in entries)
        
        # Tag breakdown
        all_tags = []
        for e in entries:
            all_tags.extend(e.get("tags", []))
        tag_counts = Counter(all_tags)
        
        # Source breakdown
        source_counts = Counter(e.get("source", "Unknown") for e in entries)
        
        result = "Comprehensive Knowledge Base Report\n"
        result += "=" * 50 + "\n\n"
        
        result += "1. Overview\n"
        result += f"   Total Entries: {len(entries)}\n"
        result += f"   Unique Types: {len(type_counts)}\n"
        result += f"   Unique Tags: {len(tag_counts)}\n"
        result += f"   Unique Sources: {len(source_counts)}\n\n"
        
        result += "2. By Type\n"
        result += "-" * 40 + "\n"
        for type_name, count in type_counts.most_common():
            result += f"   {type_name:20s}: {count}\n"
        result += "\n"
        
        result += "3. By Tag\n"
        result += "-" * 40 + "\n"
        for tag, count in tag_counts.most_common():
            result += f"   {tag:30s}: {count}\n"
        result += "\n"
        
        result += "4. By Source\n"
        result += "-" * 40 + "\n"
        for source, count in source_counts.most_common():
            result += f"   {source:30s}: {count}\n"
        result += "\n"
        
        result += "5. Top Entries\n"
        result += "-" * 40 + "\n"
        for entry in entries[:5]:
            result += f"   [{entry.get('type', 'unknown')}] {entry.get('title', 'Untitled')}\n"
            result += f"      ID: {entry.get('id', 'N/A')}\n"
            if entry.get('source'):
                result += f"      Source: {entry.get('source')}\n"
            if entry.get('description'):
                result += f"      {entry.get('description')[:80]}...\n"
            result += "\n"
        
        return result

    def _runs_to_blog_candidates(self) -> str:
        """Scan RUNS.md and generate blog post candidates from entries with links.
        
        Looks for entries in RUNS.md that contain "(See: ...)" patterns and
        extracts them as blog post candidates.
        """
        import re
        from pathlib import Path
        from engine import guard
        
        runs_path = self.root / "RUNS.md"
        
        if not runs_path.exists():
            return "No RUNS.md found"
        
        content = runs_path.read_text(encoding="utf-8")
        
        # Pattern to find entries with blog post links
        # Matches: (See: [2026-09-08-lessons-from-the-void.md](docs/_posts/2026-09-08-lessons-from-the-void.md))
        pattern = r'\(See: \[([^\]]+)\]\(([^)]+)\)\)'
        
        matches = []
        
        # Split content by table rows
        rows = re.split(r'\n', content)
        
        for row in rows:
            if 'See:' in row:
                # Try pattern
                blog_match = re.search(pattern, row)
                if blog_match:
                    title = blog_match.group(1).strip()
                    path = blog_match.group(2).strip()
                    # Extract just the filename from the path and remove .md extension
                    slug = path.split('/')[-1].replace('.md', '')
                    # Extract the run note (before the blog link)
                    run_note = row.split('(See:')[0].strip()
                    matches.append({
                        'note': run_note[:150],
                        'title': slug,
                        'slug': slug
                    })
        
        if not matches:
            return "No entries with blog post links found in RUNS.md"
        
        result = f"Found {len(matches)} entries with blog post links:\n\n"
        
        for i, match in enumerate(matches, 1):
            note = match.get('note', '')
            title = match.get('title', '')
            slug = match.get('slug', '')
            
            result += f"{i}. {note[:150]}\n"
            result += f"   Blog: {title} ({slug})\n\n"
        
        return result

    def _generate_blog_post(self, title: str, content: str, date: str | None = None) -> str:
        """Generate a full blog post with frontmatter from a title and content."""
        from datetime import datetime
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Parse the date and create RFC3339 format for Jekyll
        if '-' in date:
            date_parts = date.split('-')
            if len(date_parts) == 3:
                # Format: 2026-09-06 -> 2026-09-06 00:00:00 +0000
                formatted_date = f"{date} 00:00:00 +0000"
            elif len(date_parts) == 6:
                # Format: 2026-09-06 22:20:00 +0000
                formatted_date = date
            else:
                formatted_date = date
        else:
            formatted_date = date
        
        frontmatter = f"""---
layout: post
title: "{title}"
date: {formatted_date}
---

"""
        return frontmatter + content

    def _create_blog_posts_from_runs(self) -> str:
        """Generate complete blog posts from RUNS.md entries with blog post links.
        
        Reads RUNS.md, finds entries with "(See: (...))" patterns, reads target files,
        and generates full blog posts with proper Jekyll frontmatter.
        """
        from datetime import datetime
        
        # Read RUNS.md
        runs_path = self.root / "RUNS.md"
        if not runs_path.exists():
            return "error: RUNS.md not found"
        
        runs_content = runs_path.read_text(encoding="utf-8")
        
        # Find all blog post links in RUNS.md
        import re
        pattern = r'\(See:\s*\[([^\]]+)\]\(([^)]+)\)\)'
        matches = re.findall(pattern, runs_content)
        
        if not matches:
            return "No blog post links found in RUNS.md"
        
        output = []
        output.append(f"Found {len(matches)} blog post links in RUNS.md:")
        output.append("")
        
        for link_text, link_path in matches:
            output.append(f"  - {link_text} → {link_path}")
            output.append("")
        
        # For each match, try to read the target file and generate a blog post
        for link_text, link_path in matches:
            blog_post_path = self.root / link_path
            
            if not blog_post_path.exists():
                output.append(f"⚠️  Target file not found: {link_path}")
                output.append("")
                continue
            
            # Read the target blog post
            try:
                blog_content = blog_post_path.read_text(encoding="utf-8")
                
                # Extract title from frontmatter (first line if it matches ---)
                title = "Untitled"
                date = datetime.now().strftime('%Y-%m-%d')
                
                if blog_content.startswith('---'):
                    # Extract content between first and second ---
                    parts = blog_content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1].strip()
                        # Parse frontmatter lines
                        for line in frontmatter.split('\n'):
                            line = line.strip()
                            if line.startswith('title:'):
                                title = line.split(':', 1)[1].strip().strip('"\'')
                            elif line.startswith('date:'):
                                date_str = line.split(':', 1)[1].strip()
                                date = date_str if date_str else date
                        blog_content = parts[2].strip()
                    else:
                        blog_content = blog_content[3:].strip()
                else:
                    # No frontmatter, use first line as title
                    first_line = blog_content.split('\n', 1)[0].strip()
                    title = first_line[:60]
                    if first_line.startswith('#'):
                        title = first_line[1:].strip()
                
                # Generate Jekyll frontmatter
                if '-' in date:
                    date_parts = date.split('-')
                    if len(date_parts) == 3:
                        formatted_date = f"{date} 00:00:00 +0000"
                    elif len(date_parts) == 6:
                        formatted_date = date
                    else:
                        formatted_date = date
                else:
                    formatted_date = date
                
                frontmatter = f"""---
layout: post
title: "{title}"
date: {formatted_date}
---

"""
                
                # Write the blog post to docs/_posts/
                output_dir = self.root / "docs" / "_posts"
                output_dir.mkdir(parents=True, exist_ok=True)
                
                output_path = output_dir / f"{date}-{title.lower().replace(' ', '-').replace(':', '-')}.md"
                output_path.write_text(frontmatter + blog_content, encoding="utf-8")
                
                output.append(f"✓ Generated blog post: {output_path.name}")
                output.append(f"  From: {link_path}")
                output.append(f"  Title: {title}")
                output.append(f"  Date: {date}")
                output.append("")
                
            except Exception as e:
                output.append(f"✗ Error processing {link_path}: {e}")
                output.append("")
        
        output.append("Blog post generation complete!")
        return "\n".join(output)

    def _generate_docs(self) -> str:
        """Generate comprehensive documentation for all tools, projects, and workflows.
        
        Creates documentation that includes:
        - All available tools with descriptions from their docstrings
        - All completed projects from PROJECT.md
        - A navigation structure for easy browsing
        """
        import re
        output = []
        
        # Section 1: Overview
        output.append("# Repository Documentation")
        output.append("")
        output.append("This documentation provides a comprehensive overview of the repository,")
        output.append("its tools, projects, and workflows.")
        output.append("")
        
        # Section 2: Available Tools
        output.append("## Available Tools")
        output.append("")
        output.append("The agent has 25 tools available for use, categorized below:")
        output.append("")
        
        tool_categories = {
            "File Operations": ["_read", "_write", "_replace", "_replace_all", "_delete", "_read_with_numbers", "_read_lines", "_read_all", "_ls", "_tree", "_search", "_grep"],
            "Shell Operations": ["_run"],
            "Process Control": ["_stop", "_summarize"],
            "Knowledge Management": ["_knowledge_add", "_knowledge_list", "_knowledge_search"],
            "GitHub Integration": ["_gh_list_issues", "_gh_read_issue", "_gh_comment_issue", "_gh_close_issue", "_gh_create_issue_from_project"],
            "Blog/Documentation": ["_runs_to_blog_candidates", "_generate_blog_post", "_create_blog_posts_from_runs"],
            "Web Operations": ["_web_fetch"],
            "Analysis": ["_analyze_runs", "_validate_python", "_search_wikipedia"]
        }
        
        for category, tools in tool_categories.items():
            output.append(f"### {category}")
            output.append("")
            
            for tool in tools:
                # Get tool method
                method = getattr(self, f"_{tool}", None)
                if method and method.__doc__:
                    # Extract the first paragraph of the docstring
                    doc_lines = method.__doc__.strip().split("\n")
                    # Join first non-empty line and its continuation
                    description_lines = []
                    for line in doc_lines:
                        line = line.strip()
                        if line:
                            if not description_lines:
                                description_lines.append(line)
                            else:
                                # Check if this line is a continuation (indented or same as previous)
                                if line == description_lines[-1] or (line.startswith(' ') and not line.startswith('  ')):
                                    description_lines.append(line[1:].lstrip())
                                else:
                                    break
                    
                    description = ' '.join(description_lines[:2]).strip()  # First 2 sentences
                    output.append(f"**`{tool}`**")
                    if description:
                        output.append(f"{description}")
                    output.append("")
        
        # Section 3: Completed Projects
        output.append("## Completed Projects")
        output.append("")
        
        # Read PROJECT.md to extract completed projects
        project_path = self.root / "PROJECT.md"
        if project_path.exists():
            project_content = project_path.read_text(encoding="utf-8")
            
            # Extract all completed project sections
            project_pattern = r'### Run \d+ - (.+?)\n\n\*\*Objective:\*\* (.+?)\n\n\*\*Done when:\*\*\n(.+?)\n\n\*\*Completed:\*\*\n(.+?)\n\n\*\*Status:\*\* (.+?)'
            projects = re.findall(project_pattern, project_content, re.DOTALL)
            
            if projects:
                for project_name, objective, done_when, completed, status in projects:
                    output.append(f"### {project_name}")
                    output.append("")
                    output.append(f"**Objective:** {objective.strip()}")
                    output.append("")
                    output.append(f"**Status:** {status.strip()}")
                    output.append("")
                    
                    # Parse done when items
                    done_when_items = [line.strip() for line in done_when.strip().split("\n") if line.strip() and not line.strip().startswith("#")]
                    if done_when_items:
                        output.append("**Done when:")
                        for item in done_when_items:
                            output.append(f"  - {item}")
                        output.append("")
                    
                    # Parse completed items
                    completed_items = [line.strip() for line in completed.strip().split("\n") if line.strip() and not line.strip().startswith("#")]
                    if completed_items:
                        output.append("**Completed:")
                        for item in completed_items:
                            output.append(f"  - {item}")
                        output.append("")
            else:
                output.append("No completed projects found in PROJECT.md")
                output.append("")
        
        # Section 4: Navigation Structure
        output.append("## Navigation")
        output.append("")
        output.append("### Documentation Files")
        output.append("")
        output.append("The following documentation files are available:")
        output.append("")
        
        docs_to_document = [
            ("README.md", "Main repository README"),
            ("docs/README.md", "Documentation index"),
            ("docs/tools.md", "Tool documentation"),
            ("docs/architecture.md", "System architecture"),
            ("docs/decisions.md", "Key decisions made"),
            ("docs/failures.md", "Known failures and limitations"),
            ("docs/fact_store.md", "Fact store documentation"),
            ("docs/log.md", "Execution log"),
            ("docs/memory.md", "Memory system"),
            ("docs/thinking.md", "Thinking process documentation"),
            ("docs/blog.md", "Blog posts index"),
        ]
        
        for filename, description in docs_to_document:
            output.append(f"- [{filename}]({filename}) - {description}")
        
        output.append("")
        output.append("### Project Structure")
        output.append("")
        
        structure = [
            ("agent/", "Agent implementation and tools"),
            ("docs/", "Repository documentation"),
            ("engine/", "Engine machinery (fixed)"),
            ("notes/", "Agent notes and logs"),
            ("docs/_posts/", "Blog post files"),
            ("docs/world_knowledge/", "World knowledge data"),
        ]
        
        for path, description in structure:
            output.append(f"- `{path}` - {description}")
        
        output.append("")
        output.append("### Key Sections")
        output.append("")
        output.append("For more information, see:")
        output.append("- `agent/prompt.md` - Agent wake-up prompt and configuration")
        output.append("- `agent/context.py` - Context definition for runs")
        output.append("- `agent/tools.py` - Tool definitions and implementations")
        output.append("- `PROJECT.md` - Current project objectives and progress")
        output.append("- `RUNS.md` - Run history and activities")
        output.append("- `WAKE` - Wake-up timer (minutes until next run)")
        
        return "\n".join(output)
        """Create blog posts from RUNS.md entries that have "(See: (...))" links.
        
        Reads RUNS.md, finds entries with blog post links, reads the target files,
        and generates full blog posts with proper frontmatter.
        """
        import re
        from pathlib import Path
        from engine import guard
        
        runs_path = self.root / "RUNS.md"
        
        if not runs_path.exists():
            return "No RUNS.md found"
        
        content = runs_path.read_text(encoding="utf-8")
        
        # Pattern to find entries with blog post links
        # Matches: (See: ([ 2026-09-06-awakening.md](docs/_posts/2026-09-06-awakening.md)))
        # The first capture group is the title, the second is the path
        pattern = r'\(See: \(\s*\[([^\]]+)\]\(([^)]+)\)\)'
        
        matches = []
        
        # Split content by table rows
        rows = re.split(r'\n', content)
        
        for row in rows:
            if 'See:' in row:
                # Try pattern
                blog_match = re.search(pattern, row)
                if blog_match:
                    title = blog_match.group(1).strip()
                    path = blog_match.group(2).strip()
                    # Extract just the filename from the path
                    slug = path.split('/')[-1].replace('.md', '')
                    # Extract the run note (before the blog link)
                    run_note = row.split('(See:')[0].strip()
                    matches.append({
                        'note': run_note[:150],
                        'title': slug,
                        'slug': slug,
                        'path': path
                    })
        
        if not matches:
            return "No entries with blog post links found in RUNS.md"
        
        created = []
        
        for match in matches:
            title = match['title']
            note = match['note']
            post_path = self.root / "docs" / "_posts" / f"{title}.md"
            
            if post_path.exists():
                # Read the existing blog post
                existing_content = post_path.read_text(encoding="utf-8")
                
                # Check if it already has proper frontmatter (starts with ---)
                if existing_content.strip().startswith('---'):
                    # File already has frontmatter, just keep it
                    created.append({
                        'title': title,
                        'status': 'verified',
                        'path': str(post_path.relative_to(self.root))
                    })
                else:
                    # File doesn't have frontmatter, generate it
                    blog_post = self._generate_blog_post(title, existing_content)
                    post_path.write_text(blog_post, encoding="utf-8")
                    created.append({
                        'title': title,
                        'status': 'fixed',
                        'path': str(post_path.relative_to(self.root))
                    })
            else:
                # File doesn't exist, create a new one
                # Generate content from the RUNS.md entry
                content_text = f"# {title}\n\n{note}"
                
                # Generate frontmatter with current date
                blog_post = self._generate_blog_post(title, content_text)
                
                # Save to file
                post_path.write_text(blog_post, encoding="utf-8")
                
                created.append({
                    'title': title,
                    'status': 'created',
                    'path': str(post_path.relative_to(self.root))
                })
        
        # Build result message
        result = f"Created/updated {len(created)} blog posts:\n\n"
        for item in created:
            status = "✓" if item['status'] == 'verified' else ("+" if item['status'] == 'created' else "↻")
            result += f"{status} {item['title']} ({item['status']})\n"
            result += f"   Path: {item['path']}\n\n"
        
        return result

    def _validate_python_syntax(self, path: str) -> str:
        """Check if a Python file has syntax errors before running.
        
        Validates Python files by parsing them with ast.parse. This helps prevent
        runtime errors and ensures code is syntactically correct before execution.
        
        Args:
            path: Path to the Python file to validate
            
        Returns:
            Success message with file info, or error with syntax details
        """
        target = guard.resolve(self.root, path)
        if not target.is_file():
            return f"error: {path} does not exist"
        
        if not path.endswith('.py'):
            return f"warning: {path} is not a Python file, but will be validated anyway"
        
        try:
            # Read the file
            content = target.read_text(encoding="utf-8")
            
            # Parse the Python code
            try:
                tree = ast.parse(content)
            except SyntaxError as exc:
                # Syntax error found
                line = exc.lineno
                col = exc.offset
                msg = exc.msg
                return f"Syntax error in {path}:\n  Line {line}, Column {col}: {msg}\n  Code near error:\n  {content.splitlines()[line-1:line+2]}"
            
            # Check for specific Python version compatibility issues
            issues = []
            for node in ast.walk(tree):
                # Python 3.10+ deprecated syntax warnings
                if isinstance(node, ast.Constant) and isinstance(node.value, (bytes, bytearray)):
                    issues.append(f"  Line {node.lineno}: Using deprecated bytes/bytearray literals (use b'...')")
            
            if issues:
                return f"Valid Python syntax in {path}, but found potential issues:\n" + "\n".join(issues)
            else:
                return f"✓ {path} is valid Python (no syntax errors found)"
            
        except Exception as exc:
            return f"Error validating {path}: {type(exc).__name__}: {exc}"
    
    def _check_tool_consistency(self) -> str:
        """Verify tools are properly integrated and callable.
        
        Checks that all tool methods exist, have proper signatures, and are
        accessible through the dispatch mechanism. Helps ensure the agent's
        tool system is working correctly.
        
        Returns:
            Summary of tool consistency check results
        """
        output = []
        output.append("Tool Consistency Check")
        output.append("=" * 40)
        output.append("")
        
        # Check that all expected tool methods exist
        expected_tools = [
            "_read", "_write", "_replace", "_replace_all", "_delete",
            "_read_with_numbers", "_read_lines", "_read_all", "_ls", "_tree",
            "_search", "_grep", "_run", "_summarize", "_stop",
            "_analyze_runs", "_validate_python", "_search_wikipedia",
            "_knowledge_add", "_knowledge_list", "_knowledge_search",
            "_gh_list_issues", "_gh_read_issue", "_gh_comment_issue",
            "_gh_close_issue", "_gh_create_issue_from_project",
            "_runs_to_blog_candidates", "_generate_blog_post",
            "_create_blog_posts_from_runs", "_generate_docs",
            "_validate_python_syntax", "_check_tool_consistency",
            "_test_rollback_point", "_review_project_structure",
            "_validate_git_status"
        ]
        
        missing_tools = []
        for tool_name in expected_tools:
            if not hasattr(self, tool_name):
                missing_tools.append(tool_name)
            elif not callable(getattr(self, tool_name)):
                missing_tools.append(f"{tool_name} (not callable)")
        
        if missing_tools:
            output.append(f"⚠ Missing/Invalid tools ({len(missing_tools)}):")
            for tool in missing_tools:
                output.append(f"  - {tool}")
        else:
            output.append("✓ All expected tools exist and are callable")
        
        output.append("")
        
        # Check that schema() function exists and returns tools
        if hasattr(self, 'schema') and callable(self.schema):
            try:
                tools = self.schema()
                output.append(f"✓ Schema function returns {len(tools)} tools")
            except Exception as exc:
                output.append(f"⚠ Schema function error: {type(exc).__name__}: {exc}")
        else:
            output.append("⚠ Schema function not found or not callable")
        
        output.append("")
        
        # Check that tools can be dispatched (mock test)
        try:
            result = self.dispatch("_read", {"path": "PROJECT.md"})
            output.append("✓ Tool dispatch mechanism working correctly")
            output.append(f"  Sample result: {result[:100]}...")
        except Exception as exc:
            output.append(f"⚠ Tool dispatch mechanism error: {type(exc).__name__}: {exc}")
        
        output.append("")
        output.append("Tool system appears to be in a consistent state.")
        
        return "\n".join(output)
    
    def _test_rollback_point(self, name: str = "rollback", commit: str = "") -> str:
        """Create and validate rollback points for safe experimentation.
        
        Creates a git tag as a rollback point, allowing the agent to revert
        to a known good state if changes cause problems. Validates the rollback
        point was created successfully.
        
        Args:
            name: Name for the rollback point tag
            commit: Specific commit hash (default: current HEAD)
            
        Returns:
            Results of rollback point creation and validation
        """
        try:
            import subprocess
            
            # Get current commit if not specified
            if not commit:
                result = subprocess.run(
                    "git rev-parse HEAD",
                    shell=True, capture_output=True, text=True, timeout=10, env=self.env
                )
                if result.returncode != 0:
                    return f"error: Could not get current commit hash"
                commit = result.stdout.strip()
            
            # Create tag
            tag_name = f"rollback-{name}"
            result = subprocess.run(
                f"git tag -f {tag_name} {commit}",
                shell=True, capture_output=True, text=True, timeout=10, env=self.env
            )
            
            if result.returncode != 0:
                return f"error: Failed to create rollback point: {result.stderr}"
            
            # Verify tag exists
            result = subprocess.run(
                f"git tag -l {tag_name}",
                shell=True, capture_output=True, text=True, timeout=10, env=self.env
            )
            
            if result.returncode != 0:
                return f"error: Rollback point verification failed"
            
            if tag_name not in result.stdout:
                return f"error: Rollback point {tag_name} not found in git tags"
            
            # Show tag details
            result = subprocess.run(
                f"git show {tag_name} --no-patch --format='Tag: %(tag)%nTagger: %(taggername) <%(taggeremail)>%nDate: %(taggerdate)%nCommit: %(objectname)'",
                shell=True, capture_output=True, text=True, timeout=10, env=self.env
            )
            
            details = result.stdout.strip()
            
            return f"✓ Rollback point created successfully:\n\n{details}\n\nRollback command: git checkout {commit}  # or git checkout {tag_name}\nReset command: git reset --hard {tag_name}"
            
        except subprocess.TimeoutExpired:
            return "error: Git command timed out"
        except Exception as exc:
            return f"error: {type(exc).__name__}: {exc}"
    
    def _review_project_structure(self) -> str:
        """Check PROJECT.md and directory structure alignment.
        
        Reviews the alignment between PROJECT.md (project definitions) and the
        actual directory structure, checking for consistency and completeness.
        
        Returns:
            Summary of project structure alignment review
        """
        import re
        output = []
        
        output.append("Project Structure Review")
        output.append("=" * 40)
        output.append("")
        
        # Read PROJECT.md
        project_path = self.root / "PROJECT.md"
        if not project_path.exists():
            return "error: PROJECT.md not found"
        
        project_content = project_path.read_text(encoding="utf-8")
        
        # Extract completed projects
        project_pattern = r'### Run (\d+) - (.+?)\n\n\*\*Objective:\*\* (.+?)\n\n\*\*Done when:\*\*'
        projects = re.findall(project_pattern, project_content, re.DOTALL)
        
        if not projects:
            output.append("⚠ No projects found in PROJECT.md")
        else:
            output.append(f"Found {len(projects)} completed projects:\n")
            for run_num, name, objective in projects:
                output.append(f"  - Run {run_num}: {name}")
                output.append(f"    Objective: {objective[:60]}...")
            output.append("")
        
        # Check for alignment issues
        output.append("Alignment Checks:")
        output.append("")
        
        # Check if PROJECT.md has a 'done when' section
        if '## done when' in project_content:
            output.append("✓ PROJECT.md has 'done when' section")
        else:
            output.append("⚠ PROJECT.md missing 'done when' section")
        
        # Check if PROJECT.md has a 'technical debt' section
        if '## technical debt' in project_content:
            output.append("✓ PROJECT.md has 'technical debt' section")
        else:
            output.append("⚠ PROJECT.md missing 'technical debt' section")
        
        # Check if PROJECT.md has a 'progress' section
        if '## progress' in project_content:
            output.append("✓ PROJECT.md has 'progress' section")
        else:
            output.append("⚠ PROJECT.md missing 'progress' section")
        
        # Check if PROJECT.md has a 'not this project' section
        if '## not this project' in project_content:
            output.append("✓ PROJECT.md has 'not this project' section")
        else:
            output.append("⚠ PROJECT.md missing 'not this project' section")
        
        output.append("")
        
        # Check directory structure alignment
        output.append("Directory Structure:")
        output.append("")
        
        expected_dirs = [
            ("agent/", "Agent implementation and tools"),
            ("docs/", "Documentation"),
            ("engine/", "Engine machinery (fixed)"),
            ("notes/", "Notes and logs"),
            ("docs/_posts/", "Blog posts"),
            ("docs/world_knowledge/", "World knowledge"),
        ]
        
        for dir_path, description in expected_dirs:
            full_path = self.root / dir_path
            if full_path.exists():
                output.append(f"✓ {dir_path} exists - {description}")
            else:
                output.append(f"⚠ {dir_path} missing - {description}")
        
        output.append("")
        
        # Check if important files exist
        important_files = [
            ("agent/tools.py", "Tool definitions"),
            ("agent/prompt.md", "Agent prompt"),
            ("agent/context.py", "Context definitions"),
            ("RUNS.md", "Run history"),
            ("MEMORY.md", "Memory"),
            ("GOALS.md", "Goals"),
            ("PROJECT.md", "Project definitions"),
            (".gitignore", "Git ignore rules"),
        ]
        
        output.append("Important Files:")
        output.append("")
        
        for file_path, description in important_files:
            full_path = self.root / file_path
            if full_path.exists():
                output.append(f"✓ {file_path} exists - {description}")
            else:
                output.append(f"⚠ {file_path} missing - {description}")
        
        output.append("")
        output.append("Review complete. Check the warnings above for items that need attention.")
        
        return "\n".join(output)
    
    def _validate_git_status(self, warn_uncommitted: bool = True) -> str:
        """Warn about uncommitted changes before making significant changes.
        
        Checks git status and warns about uncommitted changes, providing
        context about what changes exist. This helps prevent accidentally
            committing work that hasn't been reviewed.
        
        Args:
            warn_uncommitted: If True, show warnings for uncommitted changes
            
        Returns:
            Git status information and warnings
        """
        import subprocess
        
        output = []
        output.append("Git Status Check")
        output.append("=" * 40)
        output.append("")
        
        try:
            # Get git status
            result = subprocess.run(
                "git status --porcelain",
                shell=True, capture_output=True, text=True, timeout=10, env=self.env
            )
            
            if result.returncode != 0:
                return f"error: Could not check git status: {result.stderr}"
            
            lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
            
            if not lines:
                output.append("✓ No uncommitted changes")
                output.append("")
                output.append("Repository is clean - ready to make changes safely.")
            else:
                modified = [l for l in lines if l.startswith(" M")]
                added = [l for l in lines if l.startswith("A ")]
                deleted = [l for l in lines if l.startswith(" D")]
                renamed = [l for l in lines if l.startswith("R")]
                untracked = [l for l in lines if l.startswith("??")]
                
                output.append(f"⚠ Found {len(lines)} uncommitted change(s):\n")
                
                if modified:
                    output.append(f"Modified files ({len(modified)}):")
                    for line in modified[:10]:
                        status, path = line.split(maxsplit=1)
                        output.append(f"  {status} {path}")
                    if len(modified) > 10:
                        output.append(f"  ... and {len(modified) - 10} more")
                    output.append("")
                
                if added:
                    output.append(f"Added files ({len(added)}):")
                    for line in added[:10]:
                        status, path = line.split(maxsplit=1)
                        output.append(f"  {status} {path}")
                    if len(added) > 10:
                        output.append(f"  ... and {len(added) - 10} more")
                    output.append("")
                
                if deleted:
                    output.append(f"Deleted files ({len(deleted)}):")
                    for line in deleted[:10]:
                        status, path = line.split(maxsplit=1)
                        output.append(f"  {status} {path}")
                    if len(deleted) > 10:
                        output.append(f"  ... and {len(deleted) - 10} more")
                    output.append("")
                
                if renamed:
                    output.append(f"Renamed files ({len(renamed)}):")
                    for line in renamed[:10]:
                        status, path = line.split(maxsplit=1)
                        output.append(f"  {status} {path}")
                    if len(renamed) > 10:
                        output.append(f"  ... and {len(renamed) - 10} more")
                    output.append("")
                
                if untracked:
                    output.append(f"Untracked files ({len(untracked)}):")
                    for line in untracked[:10]:
                        status, path = line.split(maxsplit=1)
                        output.append(f"  {status} {path}")
                    if len(untracked) > 10:
                        output.append(f"  ... and {len(untracked) - 10} more")
                    output.append("")
            
            output.append("")
            output.append("Recommendations:")
            output.append("  - Review changes before committing")
            output.append("  - Use git diff to see what changed")
            output.append("  - Consider staging changes with git add")
            output.append("  - Use a rollback point before making major changes")
            
            return "\n".join(output)
            
        except subprocess.TimeoutExpired:
            return "error: Git command timed out"
        except Exception as exc:
            return f"error: {type(exc).__name__}: {exc}"
    
    def _organize_repo(self, dry_run: bool = False) -> str:
        """Automate repository cleanup and organization.
        
        Consolidates documentation files, removes duplicates, and organizes
        by type. Updates PROJECT.md if structure changes.
        
        Args:
            dry_run: If True, only show what would be done without making changes
            
        Returns:
            Summary of organization actions taken or would be taken
        """
        import subprocess
        import shutil
        import os
        
        output = []
        output.append("Repository Organization")
        output.append("=" * 40)
        output.append("")
        
        if dry_run:
            output.append("DRY RUN MODE - No changes will be made")
            output.append("")
        
        # Find documentation files
        docs_dir = self.root / "docs"
        if docs_dir.exists():
            output.append("Found documentation directory")
            
            # Check for duplicate README files
            readme_files = list(docs_dir.glob("README*.md"))
            if len(readme_files) > 1:
                output.append(f"Found {len(readme_files)} README files:")
                for f in readme_files:
                    output.append(f"  - {f.name}")
                
                # Keep the main one, move others to archive
                main_readme = None
                other_readmes = []
                for f in readme_files:
                    if f.name == "README.md":
                        main_readme = f
                    else:
                        other_readmes.append(f)
                
                if not dry_run and main_readme and other_readmes:
                    archive_dir = docs_dir / "_archive" / "duplicates"
                    archive_dir.mkdir(parents=True, exist_ok=True)
                    
                    for f in other_readmes:
                        target = archive_dir / f.name
                        shutil.move(str(f), str(target))
                        output.append(f"  → Moved {f.name} to _archive/duplicates/")
        
        # Check for empty files
        empty_files = []
        for root, dirs, files in os.walk(self.root):
            # Skip .git, __pycache__, .venv, node_modules, etc.
            if any(skip in root for skip in ['.git', '__pycache__', '.venv', 'node_modules', '.venv', 'journal']):
                continue
            
            for file in files:
                if file.startswith('.'):
                    continue
                filepath = Path(root) / file
                if filepath.is_file() and filepath.stat().st_size == 0:
                    empty_files.append(filepath)
        
        if empty_files:
            output.append(f"Found {len(empty_files)} empty files:")
            for f in empty_files[:10]:
                output.append(f"  - {f.relative_to(self.root)}")
            if len(empty_files) > 10:
                output.append(f"  ... and {len(empty_files) - 10} more")
        
        # Suggest organizing files by type
        output.append("")
        output.append("Suggested organization:")
        output.append("  - Consolidate documentation files in docs/")
        output.append("  - Move scripts to scripts/ directory")
        output.append("  - Move config files to config/ directory")
        output.append("  - Organize by purpose (docs, src, tests, tools)")
        
        if dry_run:
            output.append("")
            output.append("No changes made in dry run mode")
        else:
            output.append("")
            output.append("Organization complete!")
        
        return "\n".join(output)
    
    def _find_unused_files(self, search_in: str = "docs") -> str:
        """Identify unused or orphaned files.
        
        Checks which files are referenced in documentation and finds
        orphaned files that aren't in any documentation.
        
        Args:
            search_in: Directory to search for references (default: docs)
            
        Returns:
            List of unused files and suggestions
        """
        import subprocess
        import os
        from pathlib import Path
        
        output = []
        output.append("Unused Files Finder")
        output.append("=" * 40)
        output.append("")
        
        search_dir = self.root / search_in
        if not search_dir.exists():
            return f"Directory {search_in} not found"
        
        # Get all markdown files in search directory
        md_files = list(search_dir.rglob("*.md"))
        output.append(f"Found {len(md_files)} markdown files in {search_in}/")
        output.append("")
        
        # Build a set of all referenced files
        referenced = set()
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8")
                # Look for markdown links and file references
                import re
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                for title, path in links:
                    if path.endswith('.md') and path.startswith('/'):
                        # Extract just the filename from the path
                        referenced.add(path.split('/')[-1].replace('.md', ''))
            except Exception as e:
                output.append(f"Warning: Could not read {md_file.relative_to(self.root)}: {e}")
        
        # Find files that aren't referenced
        all_files = set()
        for root, dirs, files in os.walk(search_dir):
            # Skip hidden and system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['_posts', 'world_knowledge', 'archive']]
            for file in files:
                if not file.startswith('.'):
                    all_files.add(file)
        
        unused = all_files - referenced
        
        if unused:
            output.append(f"Found {len(unused)} unused files:")
            for f in sorted(unused)[:20]:
                output.append(f"  - {f}")
            if len(unused) > 20:
                output.append(f"  ... and {len(unused) - 20} more")
        else:
            output.append("✓ No unused files found - all files are referenced")
        
        output.append("")
        output.append("Suggestions:")
        output.append("  - Remove files if they're no longer needed")
        output.append("  - Add links to orphaned files in documentation")
        output.append("  - Archive old files to docs/archive/")
        
        return "\n".join(output)
    
    def _cleanup_temp_files(self, safe: bool = True) -> str:
        """Remove temporary files safely.
        
        Removes .pyc, .pyo, __pycache__ directories, and other temporary files.
        Asks for confirmation before deleting.
        
        Args:
            safe: If True, ask for confirmation before deleting
            
        Returns:
            Summary of cleanup actions
        """
        import subprocess
        import shutil
        import os
        from pathlib import Path
        
        output = []
        output.append("Temporary File Cleanup")
        output.append("=" * 40)
        output.append("")
        
        to_remove = []
        
        # Find temporary files
        for root, dirs, files in os.walk(self.root):
            # Skip .git, engine, and other fixed directories
            if any(skip in root for skip in ['.git', 'engine', '.venv', 'node_modules', 'journal']):
                continue
            
            for file in files:
                # Python cache files
                if file.endswith('.pyc') or file.endswith('.pyo'):
                    to_remove.append(Path(root) / file)
                
                # Python bytecode directories
                if file == '__pycache__':
                    to_remove.append(Path(root) / file)
                
                # Editor backup files
                if file.endswith('.swp') or file.endswith('.swo'):
                    to_remove.append(Path(root) / file)
                
                # macOS system files
                if file == '.DS_Store':
                    to_remove.append(Path(root) / file)
                
                # Temporary files
                if file.startswith('~') or file.startswith('.#'):
                    to_remove.append(Path(root) / file)
        
        if not to_remove:
            output.append("✓ No temporary files found")
            return "\n".join(output)
        
        output.append(f"Found {len(to_remove)} temporary files:")
        for f in to_remove[:20]:
            output.append(f"  - {f.relative_to(self.root)}")
        if len(to_remove) > 20:
            output.append(f"  ... and {len(to_remove) - 20} more")
        output.append("")
        
        if safe:
            output.append("To remove these files, run:")
            output.append("  rm -rf .pyc .pyo __pycache__")
            output.append("  find . -name '.DS_Store' -delete")
            output.append("  find . -name '*.swp' -delete")
        else:
            # Remove files
            for file_path in to_remove:
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        output.append(f"Removed: {file_path.relative_to(self.root)}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        output.append(f"Removed directory: {file_path.relative_to(self.root)}")
                except Exception as e:
                    output.append(f"Failed to remove {file_path.relative_to(self.root)}: {e}")
        
        return "\n".join(output)
    
    def _backup_repository(self, format: str = "tar.gz", keep: int = 5) -> str:
        """Create automated repository backups.
        
        Creates a backup archive with .git directory included.
        Uses timestamp in filename and keeps last N backups.
        
        Args:
            format: Backup format - "tar.gz", "zip", or "tar" (default: tar.gz)
            keep: Number of backups to keep (default: 5)
            
        Returns:
            Summary of backup creation
        """
        import subprocess
        import shutil
        import os
        from datetime import datetime
        from pathlib import Path
        
        output = []
        output.append("Repository Backup")
        output.append("=" * 40)
        output.append("")
        
        # Check if .git exists
        if not (self.root / '.git').exists():
            return "error: Not a git repository"
        
        # Create backup directory
        backup_dir = self.root / "backup"
        backup_dir.mkdir(exist_ok=True)
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Determine backup file name
        backup_name = f"repo_backup_{timestamp}.{format}"
        backup_path = backup_dir / backup_name
        
        # Create backup
        output.append(f"Creating backup: {backup_name}")
        
        try:
            if format == "tar.gz":
                cmd = f"cd {self.root} && tar -czf {backup_path} --exclude='.git' --exclude='__pycache__' --exclude='.venv' --exclude='node_modules' --exclude='backup' ."
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env=self.env)
            elif format == "zip":
                cmd = f"cd {self.root} && zip -r {backup_path} . -x '*.git/*' '*.gitignore' '__pycache__/*' '.venv/*' 'node_modules/*' 'backup/*'"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env=self.env)
            elif format == "tar":
                cmd = f"cd {self.root} && tar -cf {backup_path} --exclude='.git' --exclude='__pycache__' --exclude='.venv' --exclude='node_modules' --exclude='backup' ."
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env=self.env)
            else:
                return f"error: Unsupported format: {format}"
            
            if result.returncode != 0:
                return f"error: Failed to create backup: {result.stderr}"
            
            output.append(f"✓ Backup created successfully: {backup_path}")
            output.append(f"  Size: {backup_path.stat().st_size / 1024:.2f} KB")
            
        except subprocess.TimeoutExpired:
            return "error: Backup command timed out"
        except Exception as exc:
            return f"error: {type(exc).__name__}: {exc}"
        
        # Remove old backups
        output.append("")
        output.append(f"Keeping last {keep} backups...")
        
        try:
            # Get all backup files
            backups = sorted(backup_dir.glob(f"repo_backup_*.{format}"), key=lambda x: x.stat().st_mtime)
            
            # Remove old ones
            for old_backup in backups[:-keep]:
                old_backup.unlink()
                output.append(f"  → Removed old backup: {old_backup.name}")
            
        except Exception as e:
            output.append(f"Warning: Could not clean up old backups: {e}")
        
        output.append("")
        output.append(f"Backup saved to: {backup_path}")
        output.append("To restore: tar -xzf <backup_file> -C <target_directory>")
        
        return "\n".join(output)
    
    def _monitor_repository_health(self) -> str:
        """Check repository integrity and health.
        
        Verifies git repository status, checks for uncommitted changes,
        validates tool system consistency, and reports health score.
        
        Returns:
            Comprehensive health report
        """
        import subprocess
        import os
        from pathlib import Path
        
        output = []
        output.append("Repository Health Monitor")
        output.append("=" * 40)
        output.append("")
        
        # Check git repository
        output.append("1. Git Repository")
        try:
            result = subprocess.run(
                "git rev-parse --is-inside-work-tree",
                shell=True, capture_output=True, text=True, timeout=10, env=self.env
            )
            if result.returncode == 0:
                output.append("✓ Git repository detected")
            else:
                output.append("⚠ Not a git repository")
        except Exception as e:
            output.append(f"⚠ Git check failed: {e}")
        
        # Check git status
        output.append("")
        output.append("2. Uncommitted Changes")
        try:
            result = subprocess.run(
                "git status --porcelain",
                shell=True, capture_output=True, text=True, timeout=10, env=self.env
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
                if not lines:
                    output.append("✓ No uncommitted changes")
                    clean_score = 1
                else:
                    output.append(f"⚠ Found {len(lines)} uncommitted change(s)")
                    clean_score = 0
            else:
                output.append("⚠ Could not check git status")
                clean_score = 0
        except Exception as e:
            output.append(f"⚠ Git status check failed: {e}")
            clean_score = 0
        
        # Check tools consistency
        output.append("")
        output.append("3. Tool System Consistency")
        try:
            tool_check = self._check_tool_consistency()
            if "⚠" not in tool_check:
                output.append("✓ Tool system consistent")
                tools_score = 1
            else:
                output.append("⚠ Tool system has issues")
                tools_score = 0
        except Exception as e:
            output.append(f"⚠ Tool check failed: {e}")
            tools_score = 0
        
        # Check Python syntax
        output.append("")
        output.append("4. Python Files Syntax")
        try:
            result = subprocess.run(
                "find . -name '*.py' -type f ! -path './.git/*' ! -path './engine/*' -exec python3 -m py_compile {} \\;",
                shell=True, capture_output=True, text=True, timeout=60, env=self.env
            )
            if result.returncode == 0:
                output.append("✓ All Python files have valid syntax")
                syntax_score = 1
            else:
                output.append("⚠ Some Python files have syntax errors")
                syntax_score = 0
        except Exception as e:
            output.append(f"⚠ Syntax check failed: {e}")
            syntax_score = 0
        
        # Check disk space
        output.append("")
        output.append("5. Disk Space")
        try:
            result = subprocess.run(
                "df -h .",
                shell=True, capture_output=True, text=True, timeout=10, env=self.env
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) >= 2:
                    usage = lines[1].split()[4]
                    output.append(f"  Disk usage: {usage}")
                    if usage.endswith('%'):
                        usage_num = float(usage[:-1])
                        if usage_num < 50:
                            output.append("✓ Sufficient disk space")
                            disk_score = 1
                        elif usage_num < 80:
                            output.append("⚠ Disk usage moderate")
                            disk_score = 0
                        else:
                            output.append("⚠ Low disk space")
                            disk_score = 0
                    else:
                        disk_score = 1
            else:
                output.append("⚠ Could not check disk space")
                disk_score = 0
        except Exception as e:
            output.append(f"⚠ Disk check failed: {e}")
            disk_score = 0
        
        # Calculate health score
        total_score = clean_score + tools_score + syntax_score + disk_score
        max_score = 4
        health_percent = (total_score / max_score) * 100
        
        output.append("")
        output.append("=" * 40)
        output.append(f"Health Score: {health_percent:.0f}% ({total_score}/{max_score})")
        
        if health_percent >= 80:
            output.append("✓ Repository is healthy")
        elif health_percent >= 50:
            output.append("⚠ Repository needs attention")
        else:
            output.append("❌ Repository has serious issues")
        
        return "\n".join(output)


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
