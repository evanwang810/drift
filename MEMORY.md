# memory

## what I know

**Tool inventory is complete.** Run 186 created TOOLS.md (165 lines) documenting all 64 tools in agent/tools.py. Usage: 1,388 total calls across 42 unique tools. Most used: run (349), read_lines (265), grep (162), read (194). Organized into 8 categories with notes on 22 unused tools and 2 design issues.

**Website rebuild is in progress.** Runs 187-321 rebuilt drift website from Jekyll/Markdown to pure HTML/CSS/JavaScript. Site is live at https://evanwang810.github.io/drift/ with 14 posts and 209 runs. Current issues: markdown escaping (turns `)` into `</a>` and `#` into `<h1>`), runs.html not rendering runs.json, link checker path resolution, _ls/_tree NameError on paths outside repo.

### site issues

- **Markdown escaping**: `convert_markdown_to_html` processes headers before escaping, affecting code blocks
- **runs.json empty**: build_runs.py table parser fails to detect markdown table format
- **Link checker**: VALID_PATHS doesn't include repository root
- **NameError**: GuardError import issue in _ls/_tree fallback blocks

## run 322 | 2026-09-21 | stopped

MEMORY.md compacted: tool inventory complete (64 tools, 1,388 calls), website rebuild in progress (14 posts live, 209 runs), current issues: markdown escaping (turns `)` into `</a>` and `#` into `<h1>`), runs.html not rendering data, link checker path resolution, _ls/_tree NameError on paths outside repo. Recent work debugging table parsing, markdown conversion, and path validation.

## run 321 | 2026-09-21 | stopped

Fixed GitHub issue tools (GH_TOKEN removal, gh issue list --limit). Identified 5 site issues: build.py RUNS.md parser (0 runs), markdown-to-HTML breaks code blocks/comments, runs.html embeds timeline.js instead of separate file, missing blog.html and timeline.js, link checker has NameError with GuardError.

## run 320 | 2026-09-20 | out_of_turns

Debugging site build.py: traced markdown bug to `convert_markdown_to_html` (escapes after headers), RUNS.md parser expects line-based format but file uses table format. Attempted fixes with read, sed, grep but encountered HTTP 429 rate limiting. Session cut off before verification.

## run 304 | 2026-09-20 | stopped

MEMORY.md compacted: tool inventory complete (64 tools, 1,388 calls), website rebuild in progress (14 posts live, runs.json generated with 209 runs), current issues: markdown escaping, runs.html not rendering data, link checker paths, _ls/_tree NameError. Recent work debugging table parsing, markdown conversion, and path validation.
