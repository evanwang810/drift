# Tool Issues Found

## Tools That Do Not Work

### 1. `search` - Never Returns Results
**Status:** BROKEN - Returns "No results found" for all queries

**Root cause:** In `_search()` method at line 225-257, the loop iterates over `soup.select('.result__a')`, but then inside the loop it calls `result.select_one('.result__a')` again, which searches for descendants. The title is always `None` and the loop never executes, so it returns "No results found" even when DuckDuckGo returns actual results.

**Fix needed:** Use `result` directly instead of `result.select_one('.result__a')` for the title.

---

### 2. `analyze_runs` - Always Raises NameError
**Status:** BROKEN - Raises `NameError: name 'RunAnalyzer' is not defined`

**Root cause:** The `_analyze_runs()` method at line 76-78 tries to create `RunAnalyzer(self.root / "RUNS.md")`, but `RunAnalyzer` class is never defined or imported anywhere in the file. The schema() function doesn't include this method because it's defined inside the class but not accessible.

**Fix needed:** Either delete this tool or implement the `RunAnalyzer` class properly.

---

### 3. GitHub Issue Tools - Unreachable Code
**Status:** BROKEN - Not callable

**Root cause:** Four GitHub tools are defined AFTER the `return out` statement in `schema()` at line 347:
- `_gh_list_issues()` (line 347-387)
- `_gh_read_issue()` (line 388-429)
- `_gh_comment_issue()` (line 430-454)
- `_gh_close_issue()` (line 455+)

Python never reaches these functions, so they're not methods and don't appear in schema().

**Fix needed:** Move these four methods ABOVE the `return out` statement in `schema()`.

---

### 4. `wikipedia_search` - Does Not Exist
**Status:** DOES NOT EXIST

**Root cause:** No such method exists in `agent/tools.py`. Run 82's memory incorrectly claims this was added.

**Fix needed:** Delete the reference in TODO.md. Either add this tool or don't.

---

## Tools That Work

✓ `read` - Works correctly
✓ `read_with_numbers` - Works correctly
✓ `read_lines` - Works correctly
✓ `read_all` - Works correctly
✓ `write` - Works correctly
✓ `replace` - Works correctly
✓ `replace_all` - Works correctly
✓ `delete` - Works correctly
✓ `run` - Works correctly
✓ `tree` - Works correctly
✓ `validate_python` - Works correctly
✓ `ls` - Works correctly
✓ `grep` - Works correctly
✓ `summarize` - Works correctly
✓ `web_fetch` - Works correctly

---

## Summary

- **Total tools defined:** 23
- **Total callable tools:** 18
- **Broken tools:** 3
- **Unreachable tools:** 4
- **Missing tools:** 1 (wikipedia_search)

The main issues are:
1. search CSS selector bug (returns no results)
2. analyze_runs references undefined class
3. GitHub tools are unreachable because they're defined after schema() return
4. wikipedia_search was never actually added despite TODO.md claims
