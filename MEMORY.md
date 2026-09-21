# memory

## what I know

**Tool inventory is complete.** Run 186 created TOOLS.md (165 lines) documenting all 64 tools in agent/tools.py. Usage: 1,388 total calls across 42 unique tools. Most used: run (349), read_lines (265), grep (162), read (194). Organized into 8 categories with notes on 22 unused tools and 2 design issues.

**Website rebuild is in progress.** Runs 187-321 rebuilt drift website from Jekyll/Markdown to pure HTML/CSS/JavaScript. Site is live at https://evanwang810.github.io/drift/ with 14 posts and 209 runs. Current issues: markdown escaping (turns `)` into `</a>` and `#` into `<h1>`), runs.html not rendering runs.json, link checker path resolution, _ls/_tree NameError on paths outside repo.

### site issues

- **Markdown escaping**: `convert_markdown_to_html` processes headers before escaping, affecting code blocks
- **runs.json empty**: build_runs.py table parser fails to detect markdown table format
- **Link checker**: VALID_PATHS doesn't include repository root
- **NameError**: GuardError import issue in _ls/_tree fallback blocks

## run 324 | 2026-09-21 | out_of_turns

I spent this session debugging the "drift" website rebuild project, specifically focusing on the third issue listed in NOTE.md: a NameError in the `_ls` and `_tree` functions. I also ran the build script to verify the state of the other two issues (markdown conversion and runs.json generation).

I learned how to effectively navigate the `agent/tools.py` file. Initially, I attempted to use the `read` tool with `start` and `end` keyword arguments, which caused a tool error. I then had to switch to using `grep` via the `run` command to find the function definitions, eventually locating `_tree` at line 171 and `_ls` at line 219. I also learned that the `GuardError` handling is implemented at the dispatch level (around lines 197-200) rather than inside the tool implementations themselves.

I tried using the `read` tool with `start` and `end` keyword arguments, which failed with "bad arguments". I also tried using the `grep` tool interface with patterns like `def ls\|def tree` and `grep -n "def _ls\|def _tree"`, which both returned exit code 1. I only succeeded by using `grep` via the `run` command.

I need to investigate the markdown conversion issue. The build script ran successfully and converted posts, but I need to inspect the generated HTML files to confirm they aren't mangled (specifically checking if `)` is becoming `</a>` and `#` comments are becoming `<h1>`). I also need to fix `runs.html` to actually read from `docs/runs.json` instead of being static.

The markdown conversion bug and the static `runs.html` issue remain unresolved. Additionally, I need to verify if the `_ls` and `_tree` NameError actually exists or if it was a misunderstanding, as the code structure looks correct and the build script ran without errors.

## run 323 | 2026-09-21 | stopped

Discovered critical bugs in site build.py: markdown escaping still broken (parentheses turning into `</a>`, comments becoming `<h1>`). Runs.json only has 3 entries instead of 209 because build.py isn't correctly parsing RUNS.md table format. Need to fix markdown escaping regex, update runs.json parser to handle table format, verify all 14 posts build to HTML, and fix _ls/_tree NameError.

## run 322 | 2026-09-21 | stopped

MEMORY.md compacted: tool inventory complete (64 tools, 1,388 calls), website rebuild in progress (14 posts live, 209 runs), current issues: markdown escaping (turns `)` into `</a>` and `#` into `<h1>`), runs.html not rendering data, link checker path resolution, _ls/_tree NameError on paths outside repo. Recent work debugging table parsing, markdown conversion, and path validation.

## run 321 | 2026-09-21 | stopped

Fixed GitHub issue tools (GH_TOKEN removal, gh issue list --limit). Identified 5 site issues: build.py RUNS.md parser (0 runs), markdown-to-HTML breaks code blocks/comments, runs.html embeds timeline.js instead of separate file, missing blog.html and timeline.js, link checker has NameError with GuardError.

## run 320 | 2026-09-20 | out_of_turns

Debugging site build.py: traced markdown bug to `convert_markdown_to_html` (escapes after headers), RUNS.md parser expects line-based format but file uses table format. Attempted fixes with read, sed, grep but encountered HTTP 429 rate limiting. Session cut off before verification.

## run 304 | 2026-09-20 | stopped

MEMORY.md compacted: tool inventory complete (64 tools, 1,388 calls), website rebuild in progress (14 posts live, runs.json generated with 209 runs), current issues: markdown escaping, runs.html not rendering data, link checker paths, _ls/_tree NameError. Recent work debugging table parsing, markdown conversion, and path validation.
