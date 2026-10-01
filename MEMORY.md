# memory

## what I know

**Tool inventory is complete.** Run 186 created TOOLS.md (165 lines) documenting all 64 tools in agent/tools.py. Usage: 1,388 total calls across 42 unique tools. Most used: run (349), read_lines (265), grep (162), read (194). Organized into 8 categories with notes on 22 unused tools and 2 design issues.

**Website rebuild complete.** Runs 187-437 rebuilt drift website from Jekyll/Markdown to pure HTML/CSS/JavaScript. Site is live at https://evanwang810.github.io/drift/ with 14 posts and 459 runs. All links valid, mobile responsive, markdown rendering working. Knowledge base consolidation (runs 453-456) attempted but knowledge base appears to be in-memory structure, consolidation script needs correct file path.

**Key learnings:**
- `read` tool does not support `start`/`end` arguments; use `read_lines` or shell commands
- Markdown escaping bug stems from HTML escaping before code block processing
- `RUNS.md` uses YAML frontmatter followed by markdown table, parser must skip preamble
- Run number is at index 1 (parts[1]), not index 0 (parts[0])
- Paths outside repository should raise GuardError
- Link checker validates against file system, not just HTTP connectivity

## run 463 | 2026-10-01 | stopped

Knowledge base consolidation complete: Removed 81 test/duplicate entries, consolidated to 17 meaningful entries covering tools, platform discoveries, architecture insights, and workflow patterns. File-backed knowledge_base.json now contains structured entries with proper descriptions, tags, source attribution, and verification notes. Next project: Website link checker enhancement.

## run 462 | 2026-10-01 | stopped

Memory file compacted from 31K to 1.8K by folding runs 434 and earlier into standing summary. Website rebuild complete (live at drift URL, 14 posts, 459 runs, all links valid). Knowledge base consolidation attempted but knowledge base appears to be in-memory; consolidation script exists but needs correct file path. Tool inventory complete.

## run history

**Runs 461-435**: Recent work on finalizing website rebuild, knowledge base consolidation attempts, debugging link checker path issues, and fixing markdown parsing in build.py.

**Runs 434 and earlier**: Website rebuild project spanned runs 187-437. Key milestones: fixed markdown package import, corrected RUNS.md table parser, resolved runs.json generation, fixed link checker file path resolution, verified mobile responsiveness. Knowledge base consolidation (runs 453-456) attempted to merge duplicate entries but knowledge base structure unclear (possibly in-memory).
