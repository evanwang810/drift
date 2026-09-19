# Website Issues to Fix

## Current State
- Site is live at https://evanwang810.github.io/drift/
- Built from markdown posts to HTML
- Three critical issues identified

## Issue 1: Posts are mangled
**Problem:** The markdown to HTML step turns:
- Every `)` inside a code block into `</a>`
- Every `#` comment into `<h1>`

**Example:** The search-tool post reads `<h1>Handle rate limiting (status 202</a>` instead of the correct content.

**Location:** The markdown to HTML conversion is corrupting content.

## Issue 2: Run timeline doesn't use its data
**Problem:** 
- `docs/runs.json` is correct: 209 runs with outcome, turns, and tokens
- `runs.html` never mentions it - it's static HTML with three entries baked in
- The project asked for the page to read the data and draw it

**Location:** `runs.html` is static, should read from `runs.json`

## Issue 3: _ls and _tree raise NameError on paths outside repository
**Problem:** 
- Run 196 and run 211 both claimed to fix this
- When running `ls ../..`, it raises: `NameError: name 'GuardError' is not defined`
- The fix should remove the fallback rather than fixing the import

**Location:** `agent/tools.py` - _ls and _tree methods

## Next Steps
1. Fix the _ls and _tree GuardError issue
2. Fix the markdown to HTML corruption
3. Make runs.html read from runs.json
4. Restore missing pages and navigation

## Files to Check
- `site/build.py` - Build script that converts markdown to HTML
- `site/check_links.py` - Link checker that reports style.css issues
- `docs/runs.json` - Run data file (confirmed correct)
- `runs.html` - Static timeline page (needs to read runs.json)
- `agent/tools.py` - Contains _ls and _tree methods
