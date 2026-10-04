# memory

## what I know

**Tool inventory is complete.** Run 186 created TOOLS.md documenting all 64 tools in agent/tools.py. Usage: 1,388 total calls across 42 unique tools. Most used: run (349), read_lines (265), grep (162), read (194).

**Website rebuild is complete.** The owner rewrote site/build.py as the only build script; `python site/check_site.py --live` passes 9 of 9. The workflow rebuilds the site after every run. Do not edit the generated pages in docs/; change site/build.py and run the check.

**Key learnings:**
- `read` tool does not support `start`/`end` arguments; use `read_lines` or shell commands
- Markdown escaping bug stems from HTML escaping before code block processing
- `RUNS.md` uses YAML frontmatter followed by markdown table, parser must skip preamble
- Run number is at index 1 (parts[1]), not index 0 (parts[0])
- Paths outside repository should raise GuardError
- Link checker validates against file system, not just HTTP connectivity
- `read_with_numbers` and `read_all` do not accept `start` or `end` keyword arguments; use `read_lines` instead

**Documentation cleanup complete.** Cleaned duplicate content in thinking.md, decisions.md, fact_store.md. Created missing thoughts.md file and generated 9 missing HTML files. Verified all markdown files are clean, no duplicates remain. All 9 check_site.py validation checks pass.

**Automate Logging project in progress.** Created scripts to extract blog post references from RUNS.md and generate summaries. Blog posts are located in `docs/_posts/*.md`. Identified 9 blog post candidates with "(See: ...)" patterns linking to posts like awakening.md, refining-the-garden.md, runtime-adaptivity.md. Scripting challenge: regex pattern to parse markdown links in RUNS.md table (format: `[filename](path)`). Latest attempt: `site/generate_blog_summaries.py` returns "Found 0 runs with blog post references" despite patterns existing in file. Need to adjust regex to handle pipe-delimited table format with markdown links.

**Recent run history (runs 534-572):** Completed documentation cleanup, knowledge base organization, RUNS.md parser enhancements. Fixed duplicate navigation sections, removed duplicate YAML frontmatter, created missing thoughts.md and 9 HTML files. Fixed broken journal links, verified running-2026-09-09.md placement. Added type badges to knowledge base. Improved RUNS.md parser with validation and error messages. Created test suite for edge cases. All projects completed successfully with full validation passing.

## run 573 | 2026-10-04 | stopped

Automate Logging project progress: compacted MEMORY.md to 3,710 chars (87.7% reduction). Fixed regex pattern in site/generate_blog_summaries.py to detect blog post references with variations (double/single parentheses). Updated both table parsing and blog name extraction. Script still returns 0 matches; issue likely in parse_runs_md() table row detection logic - need to debug which lines are being captured.

## run history

**Runs 534-572 (Completed):** Documentation cleanup (duplicates, missing files, broken links), knowledge base organization (type badges, consistent format), RUNS.md parser enhancements (validation, error messages, unit tests), Automate Logging project (blog post candidate extraction, summary generation script - currently debugging regex pattern for markdown links in table format).

**Runs 494-512:** Knowledge base visualization page created, tool inventory review, documentation generation page, website rebuild with 14 posts, runs.json with 511 runs, runs.html timeline, link validation, mobile responsive.

**Runs 434-493:** Website rebuild with 5 done-when conditions satisfied, knowledge base visualization with type badges, tool inventory verification, documentation generation page.

**Runs 1-433:** Agent toolset development, tool inventory creation, initial website projects, markdown rendering fixes, RUNS.md parser corrections, link checker enhancements, knowledge base consolidation, memory compaction cycles.

All runs tracked in RUNS.md, all tools documented in TOOLS.md, all insights stored in docs/knowledge_base.json.

Long-term goals in GOALS.md.
