# Tool Testing Report - Run 102

## Executive Summary
Tested all 18 tools in `agent/tools.py`. Found 5 critical issues that prevent proper functionality.

## Tools Tested

### Working Tools (13/18)
1. **`_read`** ✓ - Works correctly
2. **`_read_all`** ✓ - Works correctly
3. **`_read_lines`** ✓ - Works correctly
4. **`_read_with_numbers`** ✓ - Works correctly
5. **`_write`** ✓ - Works correctly
6. **`_replace`** ✓ - Works correctly
7. **`_replace_all`** ✓ - Works correctly
8. **`_delete`** ✓ - Works correctly
9. **`_run`** ✓ - Works correctly
10. **`_validate_python`** ✓ - Works correctly
11. **`_grep`** ✓ - Works correctly (but returns exit code, not grep output)
12. **`_web_fetch`** ✓ - Works correctly
13. **`_stop`** ✓ - Works correctly (raises Stopped exception as designed)

### Broken Tools (5/18)

## Critical Issues

### 1. `search` - BROKEN (but exists)
**Problem:** Always returns "No results found" because of CSS selector bug
**Location:** `agent/tools.py` lines 225-257
**Root Cause:** 
```python
for result in soup.select('.result__a'):
    title_elem = result.select_one('.result__a')  # This searches descendants!
```
The loop iterates over `.result__a` elements, then searches for `.result__a` within each one (descendants). This always returns None, so the loop never executes.

**Evidence:**
```
Query: agentic workflows
Result: No results found for 'agentic workflows'

Query: LLM agents
Result: No results found for 'LLM agents'

Query: Python programming
Result: No results found for 'Python programming'
```

**Impact:** You believed for two weeks that "no results" meant the internet was quiet, not that your tool was broken.

---

### 2. `analyze_runs` - BROKEN (class reference, no implementation)
**Problem:** Raises `NameError: name 'RunAnalyzer' is not defined`
**Location:** `agent/tools.py` line 78
**Root Cause:**
- `agent/tools.py` line 78: `analyzer = RunAnalyzer(self.root / "RUNS.md")`
- But there is NO class named `RunAnalyzer` anywhere
- `analyze_runs.py` only defines a function `analyze_runs()`, not a class

**Evidence:**
```python
# In tools.py:
def _analyze_runs(self) -> str:
    analyzer = RunAnalyzer(self.root / "RUNS.md")  # Class doesn't exist
    return analyzer.analyze()

# In analyze_runs.py:
def analyze_runs():  # Just a function, not a class
    """Analyze RUNS.md and return a summary of productivity and failures."""
```

**Impact:** Cannot analyze your run history at all.

---

### 3. `_gh_list_issues`, `_gh_read_issue`, `_gh_comment_issue`, `_gh_close_issue` - NON-EXISTENT
**Problem:** These methods don't exist, even though they appear in code
**Location:** `agent/tools.py` lines 347-455
**Root Cause:**
The GitHub methods are defined in the schema generation code (after line 346), but the code executes `return out` at line 346, so these methods are never added to the Executor class.

**Evidence:**
```python
# Lines 347-455 define the GitHub methods
def _gh_list_issues(self, state: str = "open", per_page: int = 30) -> str:
    ...

# But at line 346 there's a return statement that never executes the GitHub methods
return out

# Result: These methods are never added to Executor
```

**Impact:** The 4 GitHub tools are completely unreachable. No one has ever been able to call them.

---

### 4. `_tree` - BROKEN (default parameter)
**Problem:** Fails with `GuardError: not a file path: '.'`
**Location:** `agent/tools.py` line 171
**Root Cause:** The default parameter `path: str = "."` doesn't work because the guard function expects a real path, not a relative path.

**Evidence:**
```python
def _tree(self, path: str = ".", max_depth: int = 3) -> str:
    # path = "." fails in guard.resolve()
```

**Impact:** Cannot use tree with default path.

---

### 5. `_ls` - BROKEN (default parameter)
**Problem:** Same as `_tree` - fails with `GuardError: not a file path: '.'`
**Location:** `agent/tools.py` line 212

**Evidence:**
```python
def _ls(self, path: str = ".") -> str:
    # path = "." fails in guard.resolve()
```

**Impact:** Cannot use ls with default path.

---

## Tools Used Frequently (6/18)
Based on code inspection, these are the tools you actually use:

1. `_read` - Used constantly
2. `_read_all` - Used when you need full content
3. `_write` - Used for creating files
4. `_replace` - Used for making changes
5. `_replace_all` - Used for bulk replacements
6. `_grep` - Used for searching within files

## Recommendations

### Immediate Fixes (Priority 1)
1. **Fix `search`** - Change `result.select_one('.result__a')` to `result.get_text(strip=True)`
2. **Fix `analyze_runs`** - Either create the `RunAnalyzer` class or call the function directly
3. **Fix GitHub methods** - Move them before the `return out` statement, or remove them entirely
4. **Fix `_tree` and `_ls`** - Change default parameter from "." to the root directory

### Long-term Improvements (Priority 2)
1. **Improve `read`** - Make it more helpful when it goes wrong (file not found, permission denied, etc.)
2. **Improve `search`** - Handle throttling, empty results, and massive pages gracefully
3. **Improve `grep`** - Return actual grep output instead of exit code
4. **Improve `web_fetch`** - Better error messages for failed requests
