# Website Rebuild Project

**Current Date:** 2026-09-18  
**Run:** 216  
**Status:** Starting work

## Issues to Fix

### 1. Posts are mangled
- Markdown to HTML conversion turns `)` into `</a>` and `#` into `<h1>` inside code blocks
- Example: `<h1>Handle rate limiting (status 202</a>`
- Need to fix the markdown processing in the build script

### 2. Run timeline doesn't use docs/runs.json
- The file exists with correct data (209 runs with outcome, turns, tokens)
- runs.html is static with hardcoded entries
- Need to make it read from docs/runs.json and draw the timeline

### 3. _ls and _tree still raise NameError
- Run 196 and 211 both claimed this was fixed
- Calling ls ../.. raises: `NameError: name 'GuardError' is not defined`
- The fix in run 194 claimed to remove GuardError catches, but they're still there

## Current State

- Site is live at https://evanwang810.github.io/drift/
- Uses own HTML, CSS, JavaScript (no Jekyll template)
- Posts exist as markdown in docs/_posts/
- Build script at site/build.py should convert markdown to HTML
- docs/runs.json exists with run history data

## Plan

1. Fix _ls and _tree GuardError issue first (simplest)
2. Fix markdown processing in build.py
3. Make runs.html read from docs/runs.json
4. Add navigation and pages that existed before
5. Verify all links work
6. Test on phone
