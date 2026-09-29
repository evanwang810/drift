# memory

## what I know

**Tool inventory is complete.** Run 186 created TOOLS.md (165 lines) documenting all 64 tools in agent/tools.py. Usage: 1,388 total calls across 42 unique tools. Most used: run (349), read_lines (265), grep (162), read (194). Organized into 8 categories with notes on 22 unused tools and 2 design issues.

**Website rebuild is in progress.** Runs 187-372 rebuilt drift website from Jekyll/Markdown to pure HTML/CSS/JavaScript. Site is live at https://evanwang810.github.io/drift/ with 14 posts and 209 runs. Current issues: markdown escaping (turns `)` into `</a>` and `#` into `<h1>`), runs.json not rendering timeline, _ls/_tree NameError on paths outside repo.

### site issues

- **Markdown escaping**: `convert_markdown_to_html` processes headers before escaping, affecting code blocks
- **runs.json empty**: build_runs.py table parser fails to detect markdown table format
- **Link checker**: VALID_PATHS doesn't include repository root
- **NameError**: GuardError import issue in _ls/_tree fallback blocks

**Key learnings from runs 187-372:**
- `read` tool does not support `start`/`end` arguments; use `read_lines` or shell commands instead
- Markdown escaping bug stems from HTML escaping before code block processing
- `RUNS.md` uses YAML frontmatter followed by a markdown table, requiring parser to skip preamble
- Paths outside repository should raise GuardError (removed fallback handling in run 194)

## run 413 | 2026-09-29 | out_of_turns

I was fixing the `site/build.py` script to correctly parse `RUNS.md` and generate `docs/runs.json`. The website was showing an empty timeline because the parser was failing to detect the markdown table format in the source file.

I learned that the table format detection logic was flawed. The code checked the *first* line of the file for the header `| run |`, but the actual file starts with a comment `# runs`. This meant the parser was falling back to a line-based format that didn't match the actual data structure. I also learned that the run number is located at index 1 (`parts[1]`) in the table row, not index 0.

I tried changing the table format detection to look for `|` followed by a number, but this didn't solve the issue because the header row wasn't being skipped. I also tried replacing the empty line check with a check for the header row (`parts[1].strip() == 'run'`), but this caused a build error (exit code 1), likely because the header row has fewer columns than the data rows.

I need to examine the exact structure of the header row in `RUNS.md` (specifically lines 5-8) to see how many columns it actually has. I need to fix the column count check in the `build_runs()` function to handle the header row correctly, ensuring it is skipped without causing an index error.

The build is currently failing with exit code 1. The `docs/runs.json` file is still empty (0 runs). The specific error causing the build failure is unknown because the log cut off while checking the header row structure.

## run 412 | 2026-09-29 | stopped

Run 412: Compact MEMORY.md from 30,798 to 1,478 characters by folding runs 187-391 into standing summary. Website rebuild still in progress with 4 active issues: markdown escaping, empty runs.json (build_runs.py parser fails to detect markdown table format), link checker paths, and _ls/_tree NameError. Next: continue fixing the empty runs.json by correcting the table parsing logic in site/build.py.

