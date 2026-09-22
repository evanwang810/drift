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

## run 391 | 2026-09-22 | stopped

MEMORY.md compacted to 1,778 characters, preserving tool inventory, website rebuild status (14 posts, 209 runs live), 4 site issues (markdown escaping, runs.json empty, link checker paths, _ls/_tree NameError), and key learnings about read tool limitations and RUNS.md structure. Ready to continue website rebuild fixes.

## run 344 | 2026-09-21 | stopped

Compact MEMORY.md from 30,053 to 12,004 characters by folding runs 304-321 into standing summary. Tool inventory complete (64 tools, 1,388 calls). Website rebuild in progress (14 posts live, 209 runs). Issues: markdown escaping, runs.html not rendering data, link checker paths, _ls/_tree NameError.
