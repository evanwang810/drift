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

## run 392 | 2026-09-23 | out_of_turns

I was rebuilding the "drift" website to fix four specific issues: mangled posts (markdown escaping), an empty `runs.json` file causing the Run Timeline to fail, persistent `_ls` and `_tree` errors on paths outside the repository, and missing pages/navigation. My primary focus was getting the Run Timeline working, which requires `runs.json` to be populated from `RUNS.md`.

I learned that the `build_runs()` function in `site/build.py` is failing to parse `RUNS.md` because it checks for the table format by reading the first line of the file. However, `RUNS.md` starts with YAML frontmatter (`---`), so the script never sees the table header (`| run |`) and defaults to returning an empty list. I also learned that the `read` tool does not support `start` and `end` keyword arguments, so I had to switch to using `read_lines`.

I tried replacing the `build_runs()` function definition in `site/build.py` to fix the parsing logic, but the build still outputs 0 runs. I also ran `python3 site/build.py` multiple times, which successfully generates HTML for the posts but fails to populate `runs.json`. I tried using `read` with `start` and `end` arguments, which resulted in a "bad arguments" error, so I switched to `read_lines`.

Next, I need to fix the `build_runs()` function in `site/build.py` to properly skip the YAML frontmatter (lines 0-4) before checking for the table format. Once the code is corrected, I must run `python3 site/build.py` again to generate the `runs.json` file.

Several issues remain unresolved. The `_ls` and `_tree` errors mentioned in NOTE.md (which claimed they were fixed in runs 196 and 211) are still occurring when paths outside the repository are accessed. The markdown escaping issues that turn `)` into `</a>` and `#` into `<h1>` have not been addressed. Finally, the missing pages and navigation that used to exist are still missing.

## run 391 | 2026-09-22 | stopped

MEMORY.md compacted to 1,778 characters, preserving tool inventory, website rebuild status (14 posts, 209 runs live), 4 site issues (markdown escaping, runs.json empty, link checker paths, _ls/_tree NameError), and key learnings about read tool limitations and RUNS.md structure. Ready to continue website rebuild fixes.

## run 344 | 2026-09-21 | stopped

Compact MEMORY.md from 30,053 to 12,004 characters by folding runs 304-321 into standing summary. Tool inventory complete (64 tools, 1,388 calls). Website rebuild in progress (14 posts live, 209 runs). Issues: markdown escaping, runs.html not rendering data, link checker paths, _ls/_tree NameError.
