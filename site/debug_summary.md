# Debug Summary for Run 333

## Files Read

### site/build.py
- Markdown to HTML conversion script
- Has escaping logic that turns `)` into `</a>` and `#` comments into `<h1>`
- Escaping happens BEFORE code block handling (incorrect order)
- Code has placeholder system for code blocks
- Logic for `#` comments only triggers for single `#` (not `##` or `###`)

### agent/tools.py
- `_ls` and `_tree` tools catch `guard.GuardError` but import is missing
- `guard` imported as `from engine import guard` - should work
- Issue: NameError when branch runs (path outside repo)

### runs.html
- File does not exist yet - needs to be created
- Should read from docs/runs.json and display run timeline

### docs/runs.json
- Contains only 3 runs (50, 88, 120)
- Owner says 209 runs exist - may need to regenerate from RUNS.md

## Issues to Fix

1. **GuardError import in _ls/_tree** - verify import exists
2. **Markdown escaping in build.py** - fix order of escaping and code block handling
3. **runs.html** - create new file to read runs.json
4. **runs.json** - may need to regenerate from RUNS.md (209 runs vs 3)
5. **Missing pages** - need to check docs/ before rebuild

## Next Steps

1. Fix guard import issue
2. Fix markdown escaping bug
3. Create runs.html that reads runs.json
4. Regenerate runs.json if needed (209 runs)
5. Restore missing pages from docs/
