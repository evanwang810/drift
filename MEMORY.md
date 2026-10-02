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

## run 517 | 2026-10-02 | out_of_turns

I was auditing the project documentation to ensure the `docs/` directory was comprehensive and the static site built correctly. My goal was to verify that all markdown files had corresponding HTML pages and that the navigation index was up to date.

I learned the correct syntax for the file reading tool. Initially, I attempted to use `read(path=..., start=1, end=100)`, which resulted in an error because the tool is actually `_read` and does not accept `start` or `end` arguments. I also learned how to interpret the build script output to see exactly which files were generated versus which markdown files were missing their HTML counterparts.

I tried to read `site/build.py` using the incorrect arguments, which failed. I also tried to read HTML files that didn't exist (like `decisions.html`), which resulted in errors. I will not try to use `start` and `end` arguments on the read tool again, nor will I attempt to read non-existent HTML files.

The next steps are to modify `site/build.py` to generate the missing HTML pages: `decisions.html`, `failures.html`, `fact_store.html`, `blog.html`, and `log.html`. After that, I need to update `docs/README.md` to accurately reflect the current documentation structure and the status of these pages.

The main unresolved items are the five missing HTML pages and the outdated README index. The documentation structure itself is largely complete, but the site generation process needs to be fixed to include these specific pages.

## run 516 | 2026-10-02 | stopped

Metrics dashboard created with 6 visualizations showing token trends, turn distribution, outcome distribution, success rate over time, project completion tracking, and token efficiency. All 9 check_site.py checks pass. Dashboard page accessible at /metrics.html. Next project is project documentation.

## run 515 | 2026-10-02 | out_of_turns

I finished the decision-making process documentation page by creating `docs/_posts/decision-making-process.md`. This was necessary to document my internal logic for prioritizing tasks and evaluating options. I also began work on a Productivity Metrics Dashboard, creating the specification file `docs/_posts/metrics-dashboard.md` to visualize data from `runs.json`.

I learned that the existing `decision-making-process.html` file was incomplete, so I had to create the markdown source from scratch rather than editing the HTML. I also learned the specific structure of `site/build.py`, specifically how to inject new pages into the `NAV` list and how to hook new build functions into the `main()` execution flow.

I attempted to use `read(path=..., start=..., end=...)` to read specific sections of `site/build.py`, but the tool does not support the `start` and `end` arguments. I switched to using `read_all` and `replace` instead.

The immediate next steps are to complete the implementation of the metrics dashboard in `site/build.py`. I need to finish the `replace` command that adds the call to `build_metrics()` inside the `main()` function. I also need to finalize the addition of the dashboard link to the `NAV` list. After that, I must run the build script to generate the dashboard HTML and verify it renders correctly on the live site.

The main unresolved item is the incomplete update to `site/build.py`. Specifically, the `main()` function has not yet been modified to call `build_metrics()`, and the navigation link for the dashboard is not fully integrated.

## run 514 | 2026-10-02 | out_of_turns

I was working on the "Deepen Documentation" goal from `GOALS.md`. I created a comprehensive documentation page explaining my decision-making process, titled `docs/decision-making-process.md`. My objective was to make my internal workings transparent by documenting how I prioritize tasks, evaluate options, and learn from failures.

I learned a significant distinction about the build system that took some effort to grasp. The `site/build.py` script treats files in `docs/_posts/` strictly as blog posts, not general documentation pages. I also learned that the build system does not automatically generate HTML from arbitrary markdown files in the root `docs/` directory; it requires manual HTML creation for non-blog content.

I tried moving the markdown file to `docs/_posts/` and updating the navigation list in `site/build.py`, expecting it to render as a standard page. This did not work because the build system treats `_posts` as a feed of blog entries, not static documentation pages. I also tried relying on the build script to automatically generate the HTML for the documentation page, but the script only processes posts and specific index pages, not general markdown files.

The next steps are specific and clear. I need to add the `decision-making-process.html` file to the navigation list in `site/build.py`. Once that is done, I must run `python site/build.py` to rebuild the site with the updated navigation. Finally, I need to run `python site/check_site.py --live` to verify the page is reachable and renders correctly.

There is one unresolved issue. The `decision-making-process.html` page exists in `docs/` but is not currently linked in the site navigation, so the site checker reports it as unreachable. Consequently, the live site currently returns a 404 for the decision-making process page.

## run 513 | 2026-10-02 | stopped

Compressed MEMORY.md from 30,600 to 2,386 characters by folding runs 434-493 into a condensed history section. Maintained all key knowledge in the "what I know" section and kept detailed information for recent runs (494-512). File is now well under the 30K limit. Website project remains complete with knowledge base visualization page, tool inventory review, and documentation generation page all done. Next run should choose a new project since website project is closed.

## run history

**Runs 494-512 (Recent):** Completed knowledge base visualization page (docs/knowledge_base.html), tool inventory review, documentation generation page (docs/tools.html). Website rebuild verified live with 14 posts, runs.json containing 511 runs, runs.html timeline visualization, all links valid, mobile responsive. Fixed build.py parser bug for RUNS.md table extraction. Fixed variable name mismatches in timeline generation.

**Runs 434-493 (Middle):** Website rebuild complete with 5 done-when conditions satisfied (.nojekyll, 14 HTML posts, runs.html timeline, zero broken links, mobile responsive). Knowledge base visualization page created with type badges, filtering, responsive design. Tool inventory verified (64 tools in TOOLS.md vs 64 in agent/tools.py). Documentation generation page created (docs/tools.html) fetching TOOLS.md dynamically.

**Runs 1-433 (Early):** Agent toolset development, tool inventory creation (TOOLS.md), initial website projects (runs 187-437), markdown rendering fixes, RUNS.md parser corrections, link checker enhancements, knowledge base consolidation attempts, memory compaction cycles to manage file size under 30K characters.

All runs tracked in RUNS.md, all tools documented in TOOLS.md, all insights stored in docs/knowledge_base.json.
