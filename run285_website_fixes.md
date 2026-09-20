# Run 285: Website Fix Tracking

## Status: Turn 12 of 12 (Last Turn)

## Three Critical Bugs to Fix

### 1. Posts Mangled by Markdown Conversion
**Problem:** Markdown to HTML conversion turns `)` inside code blocks into `</a>` and `#` comments into `<h1>`.
**Example:** Search-tool post reads `<h1>Handle rate limiting (status 202</a>`
**Location:** Likely in markdown conversion logic in build.py or related conversion code
**Priority:** HIGH

### 2. Run Timeline Not Using Data
**Problem:** `docs/runs.json` is correct (209 runs with outcome, turns, tokens) but `runs.html` never mentions it.
**Current State:** runs.html is static HTML with three entries baked in.
**Location:** runs.html likely doesn't read from runs.json, or build.py doesn't generate it properly
**Priority:** HIGH

### 3. _ls and _tree NameError on Path Outside Repository
**Problem:** Still raises `NameError: name 'GuardError' is not defined` on paths like `ls ../..`
**Previous Fixes:** Run 196 and run 211 both claimed to fix this
**Current State:** Fix from run 194 removed GuardError catches, but NameError still occurs
**Priority:** MEDIUM

## Learnings from Previous Runs

1. `build.py` generates HTML files successfully but fails to populate `runs.json` because it doesn't correctly parse the markdown table format in `RUNS.md`
2. The markdown conversion logic has a flaw where code blocks are replaced with placeholders (`__CODE_BLOCK_X__`), but those placeholders are subsequently processed by the markdown parser, causing syntax errors
3. Exact string matching in `replace` commands fails due to whitespace/formatting differences in source files
4. Need to re-read build.py around the `build_runs` function to get exact text for `replace` commands

## Learnings from Current Turn

### From reading build.py:
- build.py has TWO different parsing approaches for RUNS.md:
  1. Line-based format (lines starting with "## run ") - THIS IS IMPLEMENTED
  2. Table format - THIS IS NOT IMPLEMENTED
- The code only implements the line-based format, so it can't parse the markdown table format that RUNS.md actually uses
- The runs.html DOES fetch from runs.json (lines 326-334 in build.py), so if runs.json is empty, it will show "Failed to load run data"
- The markdown conversion function is in `convert_markdown_to_html` starting around line 26

### From reading tools.py:
- The GuardError handling IS present in the dispatch method (line 52)
- Both _ls and _tree use guard.resolve which would raise GuardError for paths outside repo
- The NameError shouldn't occur if the code is correct - the owner's test must be failing somewhere else

## Next Steps

1. Read RUNS.md to see the actual table format that needs to be parsed
2. Add table format parsing to build_runs() function in build.py
3. Fix markdown conversion code blocks and comments
4. Debug _ls/_tree NameError (verify the actual error and location)
5. Test by running `python3 site/build.py`
6. Verify runs.json is generated correctly
7. Verify HTML files are not mangled
8. Verify _ls/_tree handle paths outside repo properly

## Progress

- [x] Read context from previous runs
- [x] Read build.py to understand implementation
- [x] Read tools.py to understand _ls/_tree implementation
- [ ] Read RUNS.md to see actual table format
- [ ] Fix runs.json generation from RUNS.md
- [ ] Fix markdown conversion code blocks and comments
- [ ] Fix _ls/_tree NameError for paths outside repo
- [ ] Test all fixes
- [ ] Verify live site
