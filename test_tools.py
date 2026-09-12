#!/usr/bin/env python3
"""Test each tool in agent/tools.py to see which ones actually work."""

import inspect
from pathlib import Path
from agent.tools import Executor
import os

def test_tools():
    """Test each tool by attempting to call it with minimal arguments."""

    tools = [name for name, func in inspect.getmembers(Executor, inspect.isfunction)
             if name.startswith('_') and not name.startswith('__')]

    print(f"Total tools defined: {len(tools)}\n")

    results = {}
    for tool_name in tools:
        tool_func = getattr(Executor, tool_name)

        # Get line number
        try:
            line_no = inspect.getsourcelines(tool_func)[1]
        except:
            line_no = "unknown"

        # Try to get docstring
        docstring = inspect.getdoc(tool_func) or "(no docstring)"

        # Determine if it's callable by trying to call it
        result = "NOT CALLED"
        error = None

        try:
            # Create executor instance
            root = Path('.')
            env = os.environ.copy()
            executor = Executor(root, env)

            # Try to call with appropriate args
            if tool_name == "_read" or tool_name == "_read_with_numbers" or tool_name == "_read_lines":
                result = executor._read("README.md")  # Try to read a real file
            elif tool_name == "_write":
                result = executor._write("test_tool_output.txt", "test")
            elif tool_name == "_delete":
                result = executor._delete("test_tool_output.txt")
            elif tool_name == "_replace" or tool_name == "_replace_all":
                result = executor._replace("test_tool_output.txt", "test", "new")
            elif tool_name == "_run":
                result = executor._run("echo 'test'")
            elif tool_name == "_tree":
                result = executor._tree(".", max_depth=1)
            elif tool_name == "_validate_python":
                result = executor._validate_python("test_tools.py")
            elif tool_name == "_ls":
                result = executor._ls(".")
            elif tool_name == "_search":
                result = executor._search("test query")
            elif tool_name == "_grep":
                result = executor._grep("test", ".")
            elif tool_name == "_summarize":
                result = executor._summarize("test summary")
            elif tool_name == "_stop":
                result = "STOP called (raises Stopped exception)"
            elif tool_name == "_read_all":
                result = executor._read_all("test_tools.py")
            elif tool_name == "_web_fetch":
                result = executor._web_fetch("https://example.com", parse_html=True)
            elif tool_name == "_gh_list_issues":
                result = executor._gh_list_issues()
            elif tool_name == "_gh_read_issue":
                result = executor._gh_read_issue(1)
            elif tool_name == "_gh_comment_issue":
                result = executor._gh_comment_issue(1, "test comment")
            elif tool_name == "_gh_close_issue":
                result = executor._gh_close_issue(1)
            elif tool_name == "_analyze_runs":
                result = executor._analyze_runs()
            else:
                result = f"Cannot determine test args for {tool_name}"

        except Exception as e:
            error = f"{type(e).__name__}: {e}"

        results[tool_name] = {
            "line_no": line_no,
            "docstring": docstring[:100],
            "result": result if error is None else f"ERROR: {error}",
            "has_error": error is not None
        }

        print(f"{tool_name} (line {line_no}):")
        print(f"  {result[:150]}")
        if error:
            print(f"  ERROR: {error}")
        print()

    return results

if __name__ == "__main__":
    test_tools()
