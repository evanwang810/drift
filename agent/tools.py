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
