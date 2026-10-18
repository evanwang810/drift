# Troubleshooting Guide

This guide helps diagnose and resolve common issues in the Drift Agent project.

## Table of Contents

1. [Agent Issues](#agent-issues)
2. [Site Build Issues](#site-build-issues)
3. [Tool Issues](#tool-issues)
4. [Documentation Issues](#documentation-issues)
5. [Environment Issues](#environment-issues)
6. [Debugging Tips](#debugging-tips)

---

## Agent Issues

### Agent Won't Start

**Symptom**: Running `python drift.py` fails with an error.

**Possible Causes**:

1. **Import Errors**
   ```bash
   # Check Python version
   python --version  # Should be 3.10+

   # Check for missing dependencies
   pip install -r requirements.txt
   ```

2. **Environment Variables Not Set**
   ```bash
   # Verify GH_TOKEN is set (optional, for GitHub tools)
   echo $GH_TOKEN
   ```

3. **File Permission Issues**
   ```bash
   # Check permissions on key files
   ls -la drift.py
   ls -la agent/
   ```

**Solution**: Check the error message, ensure dependencies are installed, and verify Python version.

---

### Agent Gets Stuck in Infinite Loop

**Symptom**: The agent keeps making the same changes or never stops.

**Possible Causes**:

1. **Incomplete Project Definition**
   - The project in `PROJECT.md` has no clear "Done when" criteria
   - The agent cannot determine when to stop

2. **Insufficient Memory Constraints**
   - The agent is running out of context and makes poor decisions

3. **Tool Errors**
   - A tool is failing silently and returning invalid data

**Solution**:

1. Read `PROJECT.md` and ensure it has clear, verifiable completion criteria
2. Monitor the agent's progress by checking `RUNS.md` and `MEMORY.md`
3. Check for tool errors in the agent's output
4. If stuck for too long, press `Ctrl+C` and manually call `summarize`

---

### Agent Makes Repeated Changes

**Symptom**: The agent keeps making the same edits without progress.

**Possible Causes**:

1. **Edit Overlap**
   - The agent is editing files that get overwritten by subsequent edits

2. **Inconsistent State**
   - The agent is reading outdated information

3. **Lack of Verification**
   - The agent isn't checking if its changes are correct

**Solution**:

1. Check if multiple files are being edited simultaneously
2. Verify the agent is reading up-to-date files
3. Add validation steps between edits
4. Use `validate_git_status` to check for uncommitted changes

---

## Site Build Issues

### Site Build Fails

**Symptom**: `python site/build.py` fails with an error.

**Common Causes**:

1. **Missing Dependencies**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Python Syntax Errors**
   ```bash
   # Check for syntax errors
   python -m py_compile site/build.py
   ```

3. **File Not Found**
   - Check that required source files exist in `docs/`

4. **Markdown Parsing Errors**
   - Check for malformed markdown in `docs/*.md` files

**Solution**: Check the error message and ensure all dependencies are installed and source files exist.

---

### Site Validation Fails

**Symptom**: `python site/check_site.py` reports failures.

**Common Issues**:

1. **Missing HTML Files**
   - Run `python site/build.py` to regenerate HTML
   - Check that markdown files exist in `docs/`

2. **Broken Links**
   - Check `docs/_config.yml` for incorrect navigation links
   - Verify all markdown files exist and have correct extensions

3. **File Naming Issues**
   - Blog posts should follow pattern: `YYYY-MM-DD-words-with-dashes.md`
   - Check that all markdown files have corresponding HTML files

4. **Duplicate Posts**
   - Check `docs/_posts/` for duplicate markdown files

**Solution**: Fix the specific issue mentioned in the validation output.

---

### Live Site Has Issues

**Symptom**: `python site/check_site.py --live` reports failures on the published site.

**Common Causes**:

1. **Build Not Published**
   - You need to commit and push your changes
   - GitHub Pages may take 1-2 minutes to update

2. **Caching Issues**
   - Clear browser cache
   - Wait a few minutes for GitHub Pages to propagate

3. **Missing Build Artifacts**
   - Ensure all required files exist locally before committing
   - Run `python site/build.py` locally first

**Solution**:

1. Verify your local build works: `python site/check_site.py`
2. Commit and push changes: `git add . && git commit -m "..." && git push`
3. Wait for GitHub Pages to update
4. Check the live site again

---

## Tool Issues

### Tool Returns Unexpected Results

**Symptom**: A tool (e.g., `read`, `write`, `run`) doesn't work as expected.

**Common Issues**:

1. **Wrong Arguments**
   - Check the tool's docstring for correct argument syntax
   - Use `_run("python -c 'help(YourTool)'"` to see docstrings

2. **File Path Issues**
   - Use absolute paths or paths relative to repository root
   - Check that files exist with `ls`

3. **Permission Denied**
   - Check file permissions with `ls -la`
   - Ensure you have write access

4. **Network Issues**
   - Tools that use network (e.g., `search`, `web_fetch`) may fail if offline

**Solution**: Read the tool's docstring, check arguments, verify file paths, and check permissions.

---

### Tool Fails Silently

**Symptom**: A tool appears to do nothing or returns empty results.

**Common Causes**:

1. **Error in Tool Implementation**
   - Check `agent/tools.py` for syntax errors
   - Run `python -m py_compile agent/tools.py`

2. **Invalid Input**
   - Check that input data is correct
   - Use simpler inputs to isolate the issue

3. **Environment Issues**
   - Check that required tools/dependencies are installed

**Solution**: Read the tool's implementation, check for errors, and test with simpler inputs.

---

### GitHub Tools Not Working

**Symptom**: GitHub tools (`gh_list_issues`, `gh_read_issue`, etc.) fail.

**Common Causes**:

1. **GH_TOKEN Not Set**
   ```bash
   # Set the token
   export GH_TOKEN=your_token_here
   ```

2. **Invalid Token**
   - Ensure the token has `repo` scope
   - Verify the token is valid by testing manually

3. **Rate Limiting**
   - GitHub API has rate limits (5000 requests/hour for unauthenticated)

**Solution**: Set `GH_TOKEN` environment variable with a valid token.

---

## Documentation Issues

### Documentation Not Updating

**Symptom**: Changes to `docs/*.md` files don't appear on the website.

**Common Causes**:

1. **Not Building**
   - Run `python site/build.py` to regenerate HTML
   - HTML files are generated from markdown files

2. **Not Committed**
   - Changes only affect local files
   - Commit and push to trigger rebuild

3. **Wrong File Location**
   - Documentation must be in `docs/`
   - Build script only processes files in that directory

**Solution**: Build, commit, and push changes.

---

### Broken Links in Documentation

**Symptom**: Links in `docs/*.md` files are broken.

**Common Causes**:

1. **Typo in Link**
   - Check the link syntax: `[text](url)`
   - Verify the URL is correct

2. **Missing Target File**
   - Check that the referenced file exists
   - Use `ls docs/` to list files

3. **Wrong Extension**
   - Links to markdown files should use `.md` extension
   - Example: `[Tools](tools.md)` not `[Tools](tools.html)`

**Solution**: Fix the link syntax and verify the target file exists.

---

## Environment Issues

### Python Dependencies Not Installed

**Symptom**: Import errors when running Python files.

**Common Causes**:

1. **Virtual Environment Not Activated**
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Wrong Python Version**
   ```bash
   # Check Python version
   python --version  # Should be 3.10+

   # Use correct Python
   python3 --version
   ```

3. **Incomplete Requirements**
   ```bash
   # Install all dependencies
   pip install -r requirements.txt
   ```

**Solution**: Activate virtual environment, check Python version, and install dependencies.

---

### Git Issues

**Symptom**: Git commands fail or behave unexpectedly.

**Common Causes**:

1. **Git Not Configured**
   ```bash
   # Configure git user
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **Repository Not Clean**
   ```bash
   # Check git status
   git status

   # Commit or stash changes
   git add .
   git commit -m "message"
   ```

3. **Permission Issues**
   - Check that you have write access to the repository

**Solution**: Configure git, check status, and commit changes as needed.

---

## Debugging Tips

### Enable Verbose Logging

If you need to see detailed information:

```bash
# Set environment variable
export DRIFT_DEBUG=1

# Run the agent
python drift.py
```

### Check Agent Memory

After each run, read `MEMORY.md` to see what the agent accomplished:

```bash
cat MEMORY.md
```

### Review Agent Decisions

Read `RUNS.md` to see all the agent's actions:

```bash
head -n 50 RUNS.md
```

### Test Tools Individually

Test tools in isolation to diagnose issues:

```bash
# Test read tool
python -c "from agent.tools import read; print(read('README.md'))"

# Test write tool
python -c "from agent.tools import write; write('test.txt', 'hello')"
```

### Check for Syntax Errors

```bash
# Check Python files for syntax errors
python -m py_compile agent/tools.py
python -m py_compile site/build.py
python -m py_compile site/check_site.py
```

### Validate Git Status

Before making significant changes:

```bash
python agent/tools.py validate_git_status --warn_uncommitted
```

---

## Getting Help

If you've tried these solutions and still have issues:

1. **Check the documentation** in `docs/` and `README.md`
2. **Review RUNS.md** to see if others have encountered the same issue
3. **Open a GitHub Issue** with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected behavior vs. actual behavior
   - Error messages or logs
   - Environment details (Python version, OS, etc.)

---

## Common Quick Fixes

### Site won't build

```bash
pip install -r requirements.txt
python site/build.py
```

### Agent not working

```bash
python -m py_compile agent/tools.py
python -m py_compile drift.py
```

### GitHub tools not working

```bash
export GH_TOKEN=your_token_here
```

### Dependencies not installed

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Git not configured

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

For more information, see the [Developer Guide](DEVELOPER_GUIDE.md).
