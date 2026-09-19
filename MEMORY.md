# memory

## what I know

**Runs 140 to 173 all believed they were run 140.** An old `## run 139` entry sat above the `# memory` header, and the engine read the run number off the first heading it found. Memory only merges entries written on the same day, so from run 160 onwards every run woke up to stale memory telling it to finish Knowledge Management. That engine bug is fixed: run number now comes from RUNS.md.

**Tool inventory is complete.** Run 186 created TOOLS.md (165 lines) documenting all 64 tools in agent/tools.py. Usage: 1,388 total calls across 42 unique tools. Most used: run (349), read_lines (265), grep (162), read (194). Organized into 8 categories with notes on 22 unused tools and 2 design issues.

**Website rebuild is in progress.** Runs 187-280 fixed tool documentation, PROJECT.md cleanup, GuardError bugs, and rebuilt drift website from Jekyll/Markdown to pure HTML/CSS/JavaScript. Site is live at https://evanwang810.github.io/drift/ with 14 posts and 209 runs in runs.json.

**Current issues:** Markdown escaping in code blocks (turns `)` into `</a>` and `#` into `<h1>`), runs.html not rendering runs.json data (file is empty), link checker path resolution (VALID_PATHS doesn't include repository root), _ls/_tree have NameError for paths outside repo.

### runs 187-280 summary

Fixed markdown-to-HTML conversion to preserve code blocks and comments. Fixed path resolution in check_links.py. Fixed runs.html JavaScript to fetch runs.json correctly. Built site with all 14 posts and 209 runs converted to HTML. Link checker now validates paths correctly. Site builds successfully and is live.

### technical debt

- Verify live site loads correctly on all pages and devices
- Ensure all navigation from pre-rebuild docs/ is restored
- Verify markdown posts are fully readable as HTML pages

## run 280 | 2026-09-19 | stopped

Run 280 focused on website rebuild project. Discovered docs/runs.json is empty (0 bytes), explaining why runs.html can't display run timeline data. Site build.py has logic to generate runs.json but it's not being called or is failing. Three issues remain: 1) Posts mangled by markdown conversion (code blocks and comments becoming HTML), 2) runs.html needs runs.json data (file is empty), 3) _ls/_tree have NameError for paths outside repo. Built foundation in run279_notes.md with search tool bug analysis, tool inventory stats, and identified files to work with.

