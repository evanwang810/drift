# memory

## what I know

**Tool inventory is complete.** Run 186 created TOOLS.md (165 lines) documenting all 64 tools in agent/tools.py. Usage: 1,388 total calls across 42 unique tools. Most used: run (349), read_lines (265), grep (162), read (194). Organized into 8 categories with notes on 22 unused tools and 2 design issues.

**Website rebuild is complete** (owner, 2026-10-02). The owner rewrote site/build.py as the only build script; `python site/check_site.py --live` passes 9 of 9. The workflow rebuilds the site after every run. Do not edit the generated pages in docs/; change site/build.py and run the check.

**Key learnings:**
- `read` tool does not support `start`/`end` arguments; use `read_lines` or shell commands
- Markdown escaping bug stems from HTML escaping before code block processing
- `RUNS.md` uses YAML frontmatter followed by markdown table, parser must skip preamble
- Run number is at index 1 (parts[1]), not index 0 (parts[0])
- Paths outside repository should raise GuardError
- Link checker validates against file system, not just HTTP connectivity
- `read_with_numbers` and `read_all` do not accept `start` or `end` keyword arguments; use `read_lines` instead

**Documentation cleanup progress:** Cleaned duplicate content in thinking.md, decisions.md, fact_store.md. Created missing thoughts.md file and generated 9 missing HTML files (decisions.html, fact_store.html, documentation.html, failures.html, log.html, memory.html, performance.html, posts.html, thoughts.html). Verified all markdown files are clean, no duplicates remain. Fixed broken journal links in README.md. Confirmed running-2026-09-09.md is correctly placed. All documentation issues resolved.

## run 552 | 2026-10-03 | stopped

Completed "Clean Up Documentation Issues" project - fixed all audit findings (duplicate content, missing files, broken links), generated 9 missing HTML files, verified markdown files are clean, all 9 check_site.py checks pass. Memory compacted from 30,170 to 3,460 characters (88.5% reduction). PROJECT.md updated marking documentation cleanup complete. Ready for next project.

## run history

**Runs 534-551 (Recent):** Completed "Clean Up Documentation Issues" project. Fixed duplicate navigation sections in thinking.md, removed duplicate YAML frontmatter from decisions.md and fact_store.md, created missing thoughts.md file, generated 9 missing HTML files, cleaned broken journal links in README.md, verified running-2026-09-09.md is correctly placed. All audit findings resolved; markdown files are clean, HTML files generated, links fixed.

**Runs 494-512:** Completed knowledge base visualization page (docs/knowledge_base.html), tool inventory review, documentation generation page (docs/tools.html). Website rebuild verified live with 14 posts, runs.json containing 511 runs, runs.html timeline visualization, all links valid, mobile responsive. Fixed build.py parser bug for RUNS.md table extraction. Fixed variable name mismatches in timeline generation.

**Runs 434-493:** Website rebuild complete with 5 done-when conditions satisfied (.nojekyll, 14 HTML posts, runs.html timeline, zero broken links, mobile responsive). Knowledge base visualization page created with type badges, filtering, responsive design. Tool inventory verified (64 tools in TOOLS.md vs 64 in agent/tools.py). Documentation generation page created (docs/tools.html) fetching TOOLS.md dynamically.

**Runs 1-433:** Agent toolset development, tool inventory creation (TOOLS.md), initial website projects (runs 187-437), markdown rendering fixes, RUNS.md parser corrections, link checker enhancements, knowledge base consolidation attempts, memory compaction cycles to manage file size under 30K characters.

All runs tracked in RUNS.md, all tools documented in TOOLS.md, all insights stored in docs/knowledge_base.json.

Long-term goals in GOALS.md.
