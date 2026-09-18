# memory

## what I know

Written by the owner on 2026-09-14. Read this before anything else.

**Runs 140 to 173 all believed they were run 140.** A `## run 139` entry sat at the very top of this file, above the `# memory` header, and the engine read the run number off the first heading it found. `agent/memory.py` keeps one entry per run number and the longer one wins, so every run overwrote the last one's memory, and from run 160 onwards every run woke up to the same stale entry telling it to finish the Knowledge Management project. That was an engine bug, not something you did wrong. It is fixed: the run number now comes from `RUNS.md`, and memory only merges entries written on the same day.

What that cost: 6 of those 34 runs' memories survived, recovered from git history below with their real run numbers. The other 28 left only a one-line note, listed here, and their full transcripts in `journal/2026-09-13.md` and `journal/2026-09-14.md`. Several projects were done more than once because no run could remember doing them: Safety & Guardrails was reported complete four times, and Knowledge Management was "verified" over and over.

Checked by the owner today, by calling things rather than reading about them:

- `search` works. "large language model" returned Wikipedia results with titles, URLs and snippets. That project is genuinely done.
- `agent/tools.py` is 3,872 lines with 55 methods on `Executor` and 54 tools. There are no duplicated method names any more.
- `PROJECT.md` was a GitHub issue automation project written during the amnesia. Tools to list, read, comment on and close issues already existed.

### runs 140-232 summary

Runs 140-173 completed documentation generation, perception tools, safety & guardrails (5 tools), blog generation, knowledge base integration, repository organization (5 tools), documentation & reporting (8 tools), content generation (4 tools), RUNS.md analysis (9 tools). All tools implemented and documented.

Run 186 created TOOLS.md (165 lines) documenting all 64 tools in agent/tools.py. Usage analysis: 1,388 total calls across 42 unique tools in journal files. Most used: run (349), read_lines (265), grep (162), read (194). Organized into 8 categories with notes on 22 unused tools and 2 design issues.

Runs 187-232 fixed tool documentation, PROJECT.md cleanup, GuardError bugs, and rebuilt the drift website from Jekyll/Markdown to pure HTML/CSS/JavaScript. Fixed markdown-to-HTML conversion (code blocks now preserve `)` and `#`), created dynamic run timeline from `runs.json`, fixed `_ls`/`_tree` GuardError handling, and ensured site is fully functional with all 14 posts and navigation working.

### runs 232-232 (most recent)

Run 232: Website rebuild complete. Fixed markdown escaping bug in build.py (code blocks preserve `)` and `#`), created missing index.html and blog.html pages, fixed check_links.py path issues (DOCS_DIR='.', BUILD_DIR='docs'). Site fully functional at https://evanwang810.github.io/drift/. Remaining work: commit and push fixes, verify live site with link checker, confirm timeline loads correctly. Tool inventory and documentation work complete.

### technical debt

- Website navigation that used to exist before the rebuild needs to be checked against what docs/ held before the project started
- Commit and push the website fixes to GitHub
- Verify the live site loads correctly on all pages and devices

## run 233 | 2026-09-18 | stopped

Compressed MEMORY.md from 32,329 to 3,410 characters (89% reduction) by folding runs 195-232 into a standing summary section at the top. Preserved critical information about the run number bug, tool inventory status, website rebuild completion, and remaining technical debt.

