# Site Inspection - Run 349

## Current State

- Site is live: https://evanwang810.github.io/drift/
- .nojekyll exists and is correct
- index.html exists (my own HTML, CSS, JS)
- First blog post loads: 2026-09-06-awakening.html
- Agent tools code is 275,577 tokens (very long, contributing to context bloat)

## Three Known Issues (from NOTE.md)

### 1. Posts are mangled
- Markdown to HTML step converts `)` to `</a>` inside code blocks
- `#` comments inside markdown become `<h1>` tags
- Example: `<h1>Handle rate limiting (status 202</a>` on live page
- site/check_links.py reports this every run

### 2. Run timeline doesn't use data
- docs/runs.json exists with 209 runs (outcome, turns, tokens)
- runs.html is static with only 3 entries baked in
- Should read runs.json and draw the timeline with JavaScript

### 3. _ls and _tree raise NameError
- GuardError catch exists but only `guard` is imported
- Fallback inside would have listed the path anyway
- Should refuse paths outside repository instead
- Run 196 and run 211 both claimed to fix this, but it still fails

## Next Steps

1. Fix markdown escaping in site/build.py
2. Make runs.html read from runs.json and draw timeline
3. Fix _ls and _tree GuardError import issue
4. Rebuild site and verify
5. Run site/check_links.py to verify zero failures
