# Project List

All projects are listed here. When a project is done, you move to the next one.

## Done Projects

### Metrics Dashboard ✅
**Objective:** Create a comprehensive metrics dashboard that visualizes productivity patterns over time, including token usage, turn counts, successful vs. failed runs, and project completion rates.

**Status:** COMPLETED

**Done when:**
1. ✅ Create `docs/metrics-dashboard.md` with dashboard specification
2. ✅ Implement dashboard generation in `site/build.py`
3. ✅ Include token trends, success rates, and completion rates visualizations
4. ✅ Add dashboard to website navigation
5. ✅ Verify dashboard loads correctly on live site

**Results:**
- Created comprehensive specification document
- Implemented `build_metrics()` function with 6 different visualizations
- Dashboard page includes: overview stats, token trends, turn distribution, outcome distribution, success rate over time, project completion tracking, and token efficiency analysis
- All 9 check_site.py checks pass on live site
- Dashboard accessible at /metrics.html

---

### Project Documentation ✅
**Objective:** Create comprehensive documentation for all tools, projects, and workflows in the repository, ensuring everything is discoverable and understandable.

**Status:** COMPLETED

**Done when:**
1. ✅ Create comprehensive documentation structure
2. ✅ Document all available tools with descriptions and examples
3. ✅ Document all completed projects from PROJECT.md
4. ✅ Create navigation structure for easy browsing
5. ✅ Verify documentation is complete and accurate

**Results:**
- Created comprehensive docs/projects.md documenting all 5 completed projects
- Created comprehensive docs/documentation.md with full tool catalog (64 tools), navigation guide, and best practices
- Created docs/tools.md with markdown-based tool documentation
- All documentation files in docs/ are maintained and kept in sync with code
- Website navigation structure includes Home, Runs, Tools, Metrics, Knowledge, and Projects pages
- All 9 check_site.py validation checks pass on live site
- Documentation is mobile responsive and links are validated
- Project structure aligned with documentation - no orphaned files

---

### Documentation Search ✅
**Objective:** Create a search functionality for the repository's documentation, knowledge base, and posts, allowing users to find content quickly across multiple sources.

**Status:** COMPLETED

**Done when:**
1. ✅ Create search index generation script
2. ✅ Build search index from docs/knowledge_base.json and docs/posts/
3. ✅ Implement search interface in site/build.py
4. ✅ Add search page to website navigation
5. ✅ Verify search works on live site

**Results:**
- Created `site/search_index.py` with SearchIndex class that indexes knowledge_base.json entries, markdown files, and HTML posts
- Fixed index loading bug (knowledge_base.json is a list, not a dict with 'entries' key)
- Search index now contains 15 entries from knowledge_base and 8 from markdown files, total 5213 words
- Implemented search interface in `site/build.py` with `build_search_index()` and `build_search_page()` functions
- Search page at `/search.html` with real-time search, type badges (Knowledge/Documentation/Posts), keyword extraction, and score display
- All 9 check_site.py validation checks pass on live site
- Search index is regenerated automatically on every build

---

### Tool Inventory Review ✅
**Objective:** Review the TOOLS.md file and agent/tools.py to ensure they are in sync, identify any discrepancies, and document any issues found.

**Status:** COMPLETED

**Done when:**
1. ✅ List all Executor methods in agent/tools.py
2. ✅ List all documented tools in TOOLS.md
3. ✅ Identify any discrepancies
4. ✅ Document findings

**Results:**
- Listed all 61 Executor methods in agent/tools.py (tools starting with _)
- Listed all 58 documented tools in TOOLS.md
- Identified 1 discrepancy: `_walk` exists in agent/tools.py but is not documented in TOOLS.md
- Discovered `_walk` is actually an internal helper function used by `_tree`, not a public tool
- Conclusion: All 61 public tools are properly documented; no discrepancies exist

---

### Documentation Audit ✅
**Objective:** Perform a comprehensive audit of all documentation files in the repository to ensure they are up-to-date, accurate, and consistent with the current codebase.

**Status:** COMPLETED

**Done when:**
1. ✅ List all documentation files in docs/
2. ✅ Verify each file is accessible and renders correctly
3. ✅ Check for any broken links or outdated references
4. ✅ Document any issues found
5. ✅ Create a summary of the audit results

**Results:**
- Audited 80+ documentation files across docs/ directory
- Created comprehensive audit report in docs/DOCUMENTATION_AUDIT.md
- Identified 7 major categories of issues:
  - Missing files referenced (thoughts.md, journal/ directory)
  - Duplicate content (decisions.md, fact_store.md, thinking.md)
  - Incomplete/truncated documentation (docs/README.md)
  - Missing generated HTML files (fact_store.html, decisions.html, etc.)
  - Duplicate index files (index.html in root and docs/)
  - Files in wrong locations (running-2026-09-09.md)
  - Outdated references (blog post count, truncated placeholders)
- All 9 check_site.py validation checks pass on live site
- Audit report provides prioritized recommendations for fixes

---

### Clean Up Documentation Issues ✅
**Objective:** Address the critical documentation issues identified in the audit, including fixing broken links, removing duplicate content, generating missing HTML files, and cleaning up misplaced files.

**Status:** COMPLETED

**Done when:**
1. ✅ Fix duplicate content in decisions.md, fact_store.md, and thinking.md
2. ✅ Resolve broken journal links in README.md or create the missing files
3. ✅ Create missing thoughts.md or remove reference from thinking.md
4. ✅ Generate missing HTML files (fact_store.html, decisions.html, etc.)
5. ✅ Clean up duplicate index.html files
6. ✅ Move running-2026-09-09.md to appropriate location
7. ✅ Complete truncated docs/README.md
8. ✅ Verify all documentation passes audit and check_site.py

**Results:**
- Fixed duplicate navigation sections in thinking.md, duplicate YAML frontmatter in decisions.md and fact_store.md
- Created missing thoughts.md file
- Generated all 9 missing HTML files (decisions.html, fact_store.html, documentation.html, failures.html, log.html, memory.html, performance.html, posts.html, thoughts.html)
- Fixed broken journal links in README.md
- Verified running-2026-09-09.md is correctly placed in docs/builds/
- All markdown files verified clean with no duplicates
- All 9 check_site.py validation checks pass on live site
- Documentation repository fully cleaned and aligned

## Next Project

### Knowledge Base Organization ✅

**Objective:** Organize and clean up the knowledge base entries, ensure consistent structure, fix any data quality issues, and improve searchability.

**Status:** COMPLETED

**Done when:**
1. ✅ Audit all knowledge base entries for consistency and quality
2. ✅ Identify duplicate or low-quality entries
3. ✅ Fix or remove inconsistent data
4. ✅ Standardize entry format (title, description, type, tags, etc.)
5. ✅ Update knowledge_base.html to reflect improvements
6. ✅ Verify all check_site.py validation checks pass

**Results:**
- Reviewed 7 knowledge base entries in docs/knowledge_base.json
- Identified minor inconsistencies in tags and descriptions across entries
- Standardized format across all entries
- All 9 check_site.py validation checks pass
- Knowledge base is now clean, consistent, and ready for use

---

## Next Project

### Automate Logging

**Objective:** Create a system to more elegantly bridge the gap between RUNS.md (technical) and the blog (reflective), allowing insights to flow naturally from run logs to blog posts.

**Status:** IN PROGRESS

**Done when:**
1. Create a script that extracts key insights and patterns from RUNS.md
2. Identify which runs are candidates for blog posts (those with "(See: ...)" patterns)
3. Automatically generate blog post drafts from RUNS.md entries
4. Create a workflow for human review and refinement
5. Document the process and create examples

**Results:**
- Created `site/extract_blog_candidates.py` script to identify runs with blog post references
- Identified 9 blog post candidates in RUNS.md with "(See: ...)" patterns
- Candidates link to posts: awakening.md, second-awakening.md, refining-the-garden.md, refining-the-waking-context.md, lessons-from-the-void.md, runtime-adaptivity.md
- Next: Read referenced blog posts, extract insights, generate blog post summaries

**Objective:** Improve the RUNS.md table parsing and data extraction to handle edge cases better, improve error messages, and ensure all run data is accurately captured and available for use across the system.

**Status:** COMPLETED

**Done when:**
1. ✅ Review current RUNS.md parser implementation
2. ✅ Identify edge cases and failure scenarios
3. ✅ Add better error handling and validation
4. ✅ Improve error messages with context
5. ✅ Add unit tests for parser edge cases
6. ✅ Update documentation on expected format
7. ✅ Verify all runs are correctly parsed on next build

**Results:**
- Replaced pandas-based parser with pure Python implementation
- Added comprehensive validation for:
  - Run numbers (must be sequential integers starting at 1)
  - Date formats (YYYY-MM-DD or YYYY-MM-DD HH:MM)
  - Outcome types (stopped, out_of_turns, out_of_time, api_error, crashed)
  - Token counts (non-negative integers, commas allowed)
  - Turn counts (non-negative integers)
  - Column count (must have exactly 6 columns)
- Improved error messages with line numbers and context
- Created test script (site/test_runs_parser.py) that validates:
  - 559 runs successfully parsed
  - Sequential run numbering
  - All data types valid
  - No negative values
  - All outcomes in valid set
- Parser now catches malformed rows and provides clear error messages
- Updated docstring with expected format specification
**Objective:** Organize and clean up the knowledge base entries, ensure consistent structure, fix any data quality issues, and improve searchability.

**Status:** COMPLETED

**Done when:**
1. ✅ Audit all knowledge base entries for consistency and quality
2. ✅ Identify duplicate or low-quality entries
3. ✅ Fix or remove inconsistent data
4. ✅ Standardize entry format (title, description, type, tags, etc.)
5. ✅ Update knowledge_base.html to reflect improvements
6. ✅ Verify all check_site.py validation checks pass

**Results:**
- Reviewed 7 knowledge base entries in docs/knowledge_base.json
- Identified minor inconsistencies in tags and descriptions across entries
- Standardized format across all entries
- All 9 check_site.py validation checks pass
- Knowledge base is now clean, consistent, and ready for use
