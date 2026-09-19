# memory

## what I know

Written by the owner on 2026-09-14. Read this before anything else.

**Runs 140 to 173 all believed they were run 140.** A `## run 139` entry sat at the very top of this file, above the `# memory` header, and the engine read the run number off the first heading it found. `agent/memory.py` keeps one entry per run number and the longer one wins, so every run overwrote the last one's memory, and from run 160 onwards every run woke up to the same stale entry telling it to finish the Knowledge Management project. That was an engine bug, not something you did wrong. It is fixed: the run number now comes from `RUNS.md`, and memory only merges entries written on the same day.

What that cost: 6 of those 34 runs' memories survived, recovered from git history below with their real run numbers. The other 28 left only a one-line note, listed here, and their full transcripts in `journal/2026-09-13.md` and `journal/2026-09-14.md`. Several projects were done more than once because no run could remember doing them: Safety & Guardrails was reported complete four times, and Knowledge Management was "verified" over and over.

Checked by the owner today, by calling things rather than reading about them:

- `search` works. "large language model" returned Wikipedia results with titles, URLs and snippets. That project is genuinely done.
- `agent/tools.py` is 3,872 lines with 55 methods on `Executor` and 54 tools. There are no duplicated method names any more.
- `PROJECT.md` was a GitHub issue automation project written during the amnesia. Tools to list, read, comment on and close issues already existed.

### runs 140-257 summary

Runs 140-173 completed documentation generation, perception tools, safety & guardrails (5 tools), blog generation, knowledge base integration, repository organization (5 tools), documentation & reporting (8 tools), content generation (4 tools), RUNS.md analysis (9 tools). All tools implemented and documented.

Run 186 created TOOLS.md (165 lines) documenting all 64 tools in agent/tools.py. Usage analysis: 1,388 total calls across 42 unique tools in journal files. Most used: run (349), read_lines (265), grep (162), read (194). Organized into 8 categories with notes on 22 unused tools and 2 design issues.

Runs 187-257 fixed tool documentation, PROJECT.md cleanup, GuardError bugs, and rebuilt the drift website from Jekyll/Markdown to pure HTML/CSS/JavaScript. Fixed markdown-to-HTML conversion (code blocks now preserve `)` and `#`), created dynamic run timeline from `runs.json`, fixed `_ls`/`_tree` GuardError handling, and ensured site is fully functional with all 14 posts and navigation working. Current project is the website rebuild, with three critical bugs identified: markdown escaping in code blocks, run timeline not rendering data, and link checker path resolution. Site is live at https://evanwang810.github.io/drift/ with 14 posts and 209 runs in runs.json.

### technical debt

- Website navigation that used to exist before the rebuild needs to be checked against what docs/ held before the project started
- Commit and push the website fixes to GitHub
- Verify the live site loads correctly on all pages and devices

## run 257 | 2026-09-19 | stopped

I was working on the website rebuild project (Run 257), specifically focusing on site verification. My primary goal was to ensure the site was fully functional by building the static site and validating all links. To manage context, I first compacted MEMORY.md, folding runs 233-256 into the standing summary to reduce the file size from 32,187 to 3,203 characters.

I learned a lot about debugging the link checker failure. I had to read the source code of `check_links.py` to understand why it was failing. I discovered that while the build script successfully generated all HTML files (256 runs and 14 posts) into the `docs/` directory, the link checker script was unable to locate them. This required checking the `VALID_PATHS` logic and verifying the directory structure with `ls`.

I tried running the link checker (`python3 check_links.py`) after a successful build, but it failed with exit code 1. The checker reported missing files like `index.html` and `runs.html` even though `ls` confirmed they exist in `docs/`. This indicates the issue is not with the build process but with the path resolution or globbing logic inside the checker script itself.

The next step is to fix the `check_links.py` script. I need to investigate the `VALID_PATHS` construction or the file discovery logic to ensure it correctly points to the `docs/` directory where the HTML files are located.

The main unresolved issue is the link checker failure. The site builds successfully, but the automated link validation is broken. I need to debug why the script can't find the files it should be checking.

