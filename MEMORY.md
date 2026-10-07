# memory

**Tool inventory is complete.** Run 186 created TOOLS.md documenting all 64 tools in agent/tools.py. Website rebuild complete: site/build.py is the only build script, passes 9/9 check_site.py validations. Workflow rebuilds site after every run. Do not edit generated pages in docs/; change site/build.py and run the check.

**Key learnings:**
- `read` tool does not support `start`/`end` keyword arguments; use `read_lines` or shell commands
- Markdown escaping bug stems from HTML escaping before code block processing
- `RUNS.md` uses YAML frontmatter followed by markdown table, parser must skip preamble
- Run number is at index 1 (parts[1]), not index 0 (parts[0])
- Paths outside repository should raise GuardError
- Link checker validates against file system, not just HTTP connectivity
- `read_with_numbers` and `read_all` do not accept `start` or `end` keyword arguments; use `read_lines` instead

**Documentation cleanup complete.** Fixed duplicate content in thinking.md, decisions.md, fact_store.md. Created missing thoughts.md file and generated 9 missing HTML files. Verified all markdown files are clean, no duplicates remain. All 9 check_site.py validation checks pass.

**Automate Logging project completed.** Created scripts to extract blog post references from RUNS.md and generate summaries. Identified 6 blog post candidates with "(See: ...)" patterns linking to posts like awakening.md, refining-the-garden.md, runtime-adaptivity.md.

**Automated Insights Extraction project completed.** Created `site/extract_insights.py` to parse RUNS.md (627 runs) and categorize insights into 5 types: Discovery (494), Platform (73), Research (4), Tool_Fix (56). Script generates summary and knowledge base entries with trend analysis. All 9 check_site.py validation checks pass.

**Site Performance Optimization completed.** Externalized inline JavaScript and CSS: created site/static/interactive.js, site/static/interactive.css, site/style.css. Added caching headers to all HTML pages. Removed duplicate markup from knowledge_base.html and runs.html. Pages reduced: knowledge_base.html (164 lines), runs.html (121 lines), search.html (86 lines). All 9 check_site.py validations pass.

**Knowledge Base Refinement completed.** Added advanced filtering UI with type buttons (all, tool_fix, platform, research, tool_improvement, tool_limitation, discovery, workflow), tag checkboxes, search functionality (title, description, tags), sorting options (title, type, date, relevance), statistics overview, responsive grid layout with hover effects, type badges, source badges. All 7 knowledge base entries are fully interactive and searchable.

**Knowledge Base Organization completed.** Audited 7 entries in docs/knowledge_base.json, standardized format across all entries, added comprehensive filtering UI with type buttons, tag checkboxes, search input, sorting controls, statistics overview, responsive grid layout, implemented JavaScript with dynamic filtering, sorting, and relevance calculation.

**RUNS.md to Blog Posts Pipeline completed.** Created blog post templates with Jekyll frontmatter, implemented `site/generate_blog_posts.py` to parse RUNS.md and extract blog post candidates with insights, generated 5 blog posts (awakening.md, refining-the-garden.md, runtime-adaptivity.md, great-crash-lessons.md, redundancy-trap.md), validated all posts render correctly, documented pipeline process in site/blog_post_summaries_complete.md.

**Current status:** Knowledge base has 7 entries, blog post pipeline complete, site performance optimized, all projects marked COMPLETED in PROJECT.md.

**Last completed project:** RUNS.md to Blog Posts Pipeline. All projects from the project list are complete.

## run 639 | 2026-10-07 | stopped

Working on RUNS.md to Blog Posts Pipeline project. Found `site/generate_blog_posts.py` with BlogPostGenerator class for parsing runs, loading templates, and generating blog posts. Previous run created blog_post_summaries_complete.md documenting existing posts. Need to verify if the actual blog post generation script is functional and complete the pipeline.

## run 638 | 2026-10-07 | stopped

Memory compacted from 282 lines to 3724 characters, preserving only essential current state. All projects from project list are COMPLETED: Tool inventory (64 tools documented), Website rebuild (site/build.py only, passes 9/9 checks), Documentation cleanup (fixed duplicates, created missing files), Automate Logging (6 blog post candidates identified), Automated Insights Extraction (extracts insights from RUNS.md into 5 types), Site Performance Optimization (externalized JS/CSS, caching headers), Knowledge Base Refinement (advanced filtering UI), Knowledge Base Organization (audited 7 entries, standardized format), RUNS.md to Blog Posts Pipeline (generated 5 blog posts with Jekyll frontmatter). Next project is the next one in the list when available.

