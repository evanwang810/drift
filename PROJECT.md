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

## Next Project

### Tool Inventory Review
**Objective:** Review the TOOLS.md file and agent/tools.py to ensure they are in sync, identify any discrepancies, and document any issues found.

**Status:** TODO

**Done when:**
1. List all tools in TOOLS.md
2. List all tools in agent/tools.py
3. Compare the two lists and identify any discrepancies
4. Document any missing tools or outdated entries
5. Update either TOOLS.md or agent/tools.py to align them

**History:** None yet
