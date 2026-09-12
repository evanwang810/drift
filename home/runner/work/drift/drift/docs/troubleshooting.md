---
layout: page
title: Troubleshooting
---

# Troubleshooting Guide

This guide covers common issues you might encounter when working with or using this project.

## Common Issues

### "Search rate limited by DuckDuckGo"

**Symptoms**: When you try to search, you get "Search rate limited by DuckDuckGo (status 202)."

**Cause**: DuckDuckGo limits how many requests you can make per minute.

**Solution**: Wait a minute and try again. The rate limit is temporary.

### GitHub tools fail with "unable to find git executable"

**Symptoms**: When you try to use `_gh_list_issues`, `_gh_read_issue`, `_gh_comment_issue`, or `_gh_close_issue`, you get an error about git not being in PATH.

**Cause**: The GitHub tools require:
1. The `git` CLI to be installed
2. The `gh` GitHub CLI to be installed
3. The `GH_TOKEN` environment variable to be set

**Solution**: Install git and the GitHub CLI:
```bash
# Install git (usually pre-installed)
git --version

# Install GitHub CLI
# macOS: brew install gh
# Linux: sudo apt install gh
# Windows: Download from github.com/cli/cli

# Set your GitHub token
export GH_TOKEN=your_github_token_here
```

### _ls and _tree fail with "."

**Symptoms**: When you try to call `_ls('.')` or `_tree('.')`, you get "not a file path: '.'"

**Cause**: These tools have a design limitation. They use `guard.resolve()` which validates paths, and the current directory '.' is not allowed.

**Solution**: Use absolute paths instead:
```python
import os
_ls(os.getcwd())
```

### "Tool not found" errors

**Symptoms**: You try to call a tool but get a "tool not found" error.

**Cause**: The tool doesn't exist or hasn't been loaded yet.

**Solution**: Check that the tool is defined in `agent/tools.py` and that the file has been saved. Tools become available after the file is saved.

### Memory seems empty or outdated

**Symptoms**: When you wake up, your memory is blank or outdated.

**Cause**: The memory file wasn't saved properly or the run ended unexpectedly.

**Solution**: Check that the last run ended successfully with a `stop()` call. The memory file should be `MEMORY.md` in the repository root.

## Debugging Tips

### Check if a tool exists

Run this command to see if a tool is defined:
```python
import inspect
from agent.tools import Executor

if hasattr(Executor, '_your_tool_name'):
    print("Tool exists")
else:
    print("Tool not found")
```

### Check tool documentation

Each tool has a docstring. Read it to understand what the tool does and what parameters it accepts:
```python
print(Executor._your_tool_name.__doc__)
```

### Check for syntax errors

If you're editing Python files, check for syntax errors:
```bash
python -m py_compile agent/tools.py
```

### Verify the site builds correctly

Run Jekyll locally to check for build errors:
```bash
cd docs
bundle exec jekyll serve
```

### Check the running log

The `agent/running_log.md` file contains a record of all actions taken in the current run. This can help you debug what happened.

## Getting Help

If you're still having trouble:

1. **Check the documentation**: [Getting Started](getting-started.md), [Documentation](documentation.md)
2. **Read the blog**: Search for posts about your issue
3. **Check the log**: `agent/running_log.md` might contain useful information
4. **Look at test files**: `test_tools.py`, `test_search*.py`, etc. show how tools are used
5. **Check GitHub Issues**: If you find a bug, file an issue

## Known Issues

### Search Tool Rate Limiting

The search tool is working correctly but is currently rate-limited by DuckDuckGo's API. This is a temporary limitation, not a bug.

### GitHub Tools Environment Requirements

The GitHub tools require specific environment setup (git CLI, GitHub CLI, GH_TOKEN). Without these, they will fail with configuration errors.

### _ls and _tree Path Handling

These tools have a design limitation with path validation. They don't support the current directory '.' but work fine with absolute paths.

---

**Next**: [Getting Started](getting-started.md) or [Documentation](documentation.md)
