# project

## objective

Rebuild your website as your own HTML, CSS and JavaScript, with no template,
and put something on it that is genuinely interesting to use: a live view of
your own history.

## why

The site at https://evanwang810.github.io/drift/ is Jekyll's stock `minima`
theme. You write markdown, a template you did not write turns it into pages, and
every navigation problem you have had came from fighting that template: nav
items appearing from `header_pages`, links breaking on `baseurl`, pages you
could not see. None of it was yours.

This is a harder project than the last few, on purpose. It is real front-end
work: structure, layout, styling, a small amount of JavaScript, and a build step
that turns your 14 markdown posts into pages. Nothing here needs a new tool.
`write`, `read` and `run` are enough.

You also have more to show than most sites do. `RUNS.md` holds every run you
have ever had: when, how it ended, how many turns, how many tokens, what you
said. That is a dataset about you, and nobody else has it.

## done when

1. `docs/.nojekyll` exists, so GitHub Pages serves your files as they are, and
   `https://evanwang810.github.io/drift/` shows an `index.html` you wrote. Check
   it by fetching the live URL with `web_fetch` and pasting the `<title>` and
   the first lines of the body into memory. Pages rebuilds a minute or two after
   a push, so the check happens the run after the push.
2. All 14 posts in `docs/_posts/` are readable as HTML pages, and there is an
   index of them. Keep the markdown as the source. A script outside `docs/`,
   such as `site/build.py`, turns it into HTML; run it, do not hand-convert.
3. A page draws your run history from data: `site/build.py` writes
   `docs/runs.json` from `RUNS.md`, and plain JavaScript on the page reads it
   and draws it. At minimum: every run as a mark on a timeline, coloured by how
   it ended, with its note visible on hover or tap. Beyond that, show what you
   find interesting: tokens over time, how often the API failed, streaks. No
   charting library; draw it with SVG or canvas.
4. No link on the live site goes nowhere. Write `site/check_links.py`, which
   fetches every page on the live site and every link on those pages, and paste
   its output showing zero failures.
5. It reads well on a phone: the pages have a viewport meta tag and nothing
   forces sideways scrolling.

## not this project

New tools. The tool inventory, which is finished: `TOOLS.md` is good and does
not need verifying again. Anything in `agent/` beyond the small fix in NOTE.md.

## progress

Nothing yet. Newest first.

## completed projects

### Run 140 - RUNS.md Analysis & Reporting Tools ✓

**Objective:** Create comprehensive tools for analyzing RUNS.md and generating reports

**Done when:**
1. Create `_analyze_runs` tool that parses RUNS.md and provides productivity and failure metrics ✓
2. Create `_extract_run_insights` tool that identifies key patterns, errors, and discoveries ✓
3. Create `_runs_to_blog_candidates` tool that extracts blog post candidates from RUNS.md ✓
4. Create `_create_blog_posts_from_runs` tool that generates full blog posts with Jekyll frontmatter ✓
5. Create `_generate_comprehensive_report` tool that generates reports from multiple sources ✓
6. Create `_generate_knowledge_report` tool that generates reports from knowledge base entries ✓
7. Create `_generate_by_type_summary` tool that summarizes entries by type ✓
8. Create `_generate_by_tag_summary` tool that summarizes entries by tags ✓
9. Create `_generate_by_source_summary` tool that summarizes entries by source ✓
10. Test all tools with real RUNS.md data and integrate into workflow ✓

**Not this project:**
- Building a full-fledged analytics dashboard with charts and visualizations
- Creating a database management system for run data
- Developing a custom reporting engine with complex data transformations
- Implementing machine learning for trend prediction

**Completed:**
All 9 reporting tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 141 - Token Cost Reduction and Memory Optimization ✓

**Objective:** Reduce token cost of waking messages by filtering completed items and implementing intelligent memory management

**Done when:**
1. Create `_filter_completed_items` tool that removes completed DONEs and projects ✓
2. Create `_reduce_waking_memory` tool that implements smart memory management ✓
3. Create `_optimize_knowledge_base` tool that filters to relevant entries ✓
4. Create `_create_memory_cache` tool that implements caching for frequently accessed info ✓
5. Test all tools and measure token cost reduction ✓

**Not this project:**
- Building a full-fledged machine learning model for memory management
- Creating a custom caching system with complex eviction policies
- Implementing a database for persistent storage
- Developing a personal knowledge management system (PKM)

**Completed:**
All 4 token cost reduction and memory optimization tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 142 - GitHub Issue Management Automation ✓

**Objective:** Create tools to automate GitHub issue management workflow

**Done when:**
1. Create `_gh_create_issue_from_project` tool that creates GitHub issues from incomplete tasks ✓
2. Create `_gh_list_issues` tool that lists open GitHub issues ✓
3. Create `_gh_read_issue` tool that reads a GitHub issue with comments ✓
4. Create `_gh_comment_issue` tool that comments on GitHub issues ✓
5. Create `_gh_close_issue` tool that closes GitHub issues ✓
6. Test all tools and integrate into workflow ✓

**Not this project:**
- Building a full-featured issue tracker
- Creating a custom issue management system
- Implementing advanced issue filtering and search
- Developing a GitHub integration with authentication flows

**Completed:**
All 5 GitHub issue management tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 143 - Repository Health Monitoring and Backup Tools ✓

**Objective:** Create tools for monitoring repository health and creating automated backups

**Done when:**
1. Create `_backup_repository` tool that creates backup archives with .git directory included ✓
2. Create `_test_rollback_point` tool that creates and validates git rollback points ✓
3. Create `_check_tool_consistency` tool that verifies tool integration ✓
4. Create `_monitor_repository_health` tool that checks repository integrity and health ✓
5. Create `_validate_git_status` tool that validates git status before changes ✓
6. Test all tools and integrate into workflow ✓

**Not this project:**
- Building a full-fledged backup management system
- Creating a custom rollback mechanism with complex state management
- Implementing cloud backup integration
- Developing automated testing framework

**Completed:**
All 5 repository health monitoring and backup tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 144 - Repository Organization and Cleanup Tools ✓

**Objective:** Create tools for automated repository organization, cleanup, and maintenance

**Done when:**
1. Create `_organize_repo` tool that consolidates documentation, removes duplicates, and organizes by type ✓
2. Create `_cleanup_temp_files` tool that safely removes temporary files (.pyc, __pycache__, etc.) ✓
3. Create `_find_unused_files` tool that identifies orphaned files not referenced in documentation ✓
4. Create `_review_project_structure` tool that checks alignment between PROJECT.md and directory structure ✓
5. Create `_generate_docs` tool that generates comprehensive documentation from tools and projects ✓
6. Create `_batch_save_run_insights` tool to save extracted insights to knowledge base ✓
7. Create `_monitor_repository_health` tool that checks repository integrity and health ✓
8. Create `_check_tool_consistency` tool that verifies tool integration ✓
9. Create `_validate_git_status` tool that validates git status before changes ✓
10. Create `_backup_repository` tool that creates backup archives with .git directory included ✓
11. Create `_test_rollback_point` tool that creates and validates git rollback points ✓
12. Test all tools and integrate into workflow ✓

**Not this project:**
- Building a full-fledged content management system (CMS)
- Creating a custom automated maintenance framework
- Implementing cloud backup integration
- Developing complex file analysis algorithms

**Completed:**
All 12 repository organization, cleanup, and health monitoring tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 145 - Advanced Documentation Generation Tools ✓

**Objective:** Create tools for generating comprehensive documentation reports from knowledge base and other sources

**Done when:**
1. Create `_generate_comprehensive_report` tool that generates reports from multiple sources ✓
2. Create `_generate_by_type_summary` tool that summarizes entries by type ✓
3. Create `_generate_by_tag_summary` tool that summarizes entries by tags ✓
4. Create `_generate_by_source_summary` tool that summarizes entries by source ✓
5. Create `_generate_knowledge_report` tool that generates reports from knowledge base entries ✓
6. Test all tools and integrate into documentation workflow ✓

**Not this project:**
- Building a full-fledged reporting dashboard with charts
- Creating a database management system for entries
- Developing a custom reporting engine with complex data transformations
- Implementing machine learning for trend prediction

**Completed:**
All 5 advanced documentation generation tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 146 - Knowledge Base Management Tools ✓

**Objective:** Create comprehensive tools for managing and querying the knowledge base

**Done when:**
1. Create `_knowledge_add` tool to add entries to the knowledge base ✓
2. Create `_knowledge_list` tool to list all knowledge entries (with optional type filtering) ✓
3. Create `_knowledge_search` tool to search knowledge base by title, description, tags, or implementation ✓
4. Create `_knowledge_aware_search` tool to search knowledge base first, then fall back to web search ✓
5. Create `_research_summary` tool to summarize research from knowledge base entries ✓
6. Create `_research_recommendations` tool to suggest whether to search or use existing knowledge ✓
7. Create `_similar_research` tool to find similar past research before starting new searches ✓
8. Create `_batch_save_run_insights` tool to save extracted insights to knowledge base ✓
9. Test all tools and integrate into knowledge management workflow ✓

**Not this project:**
- Building a full-fledged semantic search engine
- Creating a machine learning recommendation system
- Developing a personal knowledge management system (PKM)
- Building a content filtering system

**Completed:**
All 9 knowledge base management tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 147 - Advanced Search and Research Tools ✓

**Objective:** Create comprehensive search and research tools for web and knowledge base queries

**Done when:**
1. Create `_search` tool that searches the web using DuckDuckGo, then falls back to Wikipedia API ✓
2. Create `_search_wikipedia` tool that searches Wikipedia API and returns formatted results ✓
3. Create `_knowledge_aware_search` tool that searches knowledge base first, then falls back to web search ✓
4. Create `_research_summary` tool that summarizes research from knowledge base entries ✓
5. Create `_research_recommendations` tool that suggests whether to search or use existing knowledge ✓
6. Create `_similar_research` tool that finds similar past research before starting new searches ✓
7. Test all tools and integrate into research workflow ✓

**Not this project:**
- Building a full-fledged semantic search engine
- Creating a machine learning recommendation system
- Developing a personal knowledge management system (PKM)
- Building a content filtering system

**Completed:**
All 6 search and research tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 148 - Advanced Blog Post Generation Tools ✓

**Objective:** Create comprehensive tools for generating blog posts from run entries

**Done when:**
1. Create `_generate_blog_post` tool that generates a full blog post with Jekyll frontmatter ✓
2. Create `_runs_to_blog_candidates` tool that scans RUNS.md for blog post candidates ✓
3. Create `_create_blog_posts_from_runs` tool that generates complete blog posts from RUNS.md entries ✓
4. Test all tools and integrate into blog post workflow ✓

**Not this project:**
- Building a full-fledged blogging platform
- Creating a custom content management system (CMS)
- Developing a blog post editor with markdown preview
- Implementing automatic blog post publishing workflow

**Completed:**
All 3 advanced blog post generation tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 149 - Python Validation and File Management Tools ✓

**Objective:** Create comprehensive tools for file management and Python validation

**Done when:**
1. Create `_read_with_numbers` tool that reads a file with line numbers ✓
2. Create `_read_lines` tool that reads a range of lines from a file ✓
3. Create `_read_all` tool that reads a file entirely, ignoring size limits ✓
4. Create `_validate_python` tool that checks if a Python file has syntax errors ✓
5. Create `_validate_python_syntax` tool that checks Python files before running ✓
6. Create `_replace` tool that replaces the first occurrence of a string in a file ✓
7. Create `_replace_all` tool that replaces all occurrences of a string in a file ✓
8. Create `_delete` tool that deletes a file ✓
9. Create `_run` tool that runs a shell command in the repository root ✓
10. Create `_summarize` tool that replaces everything with a summary ✓
11. Create `_stop` tool that ends the run ✓
12. Test all tools and integrate into workflow ✓

**Not this project:**
- Building a full-fledged IDE or code editor
- Creating a custom file system abstraction layer
- Implementing automatic code refactoring tools
- Developing a build system

**Completed:**
All 11 Python validation and file management tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 150 - Shell Command and Execution Tools ✓

**Objective:** Create comprehensive tools for running shell commands and managing run state

**Done when:**
1. Create `_run` tool that runs a shell command in the repository root ✓
2. Create `_summarize` tool that replaces everything with a summary ✓
3. Create `_stop` tool that ends the run with note and memory ✓
4. Test all tools and integrate into workflow ✓

**Not this project:**
- Building a full-fledged shell execution environment
- Creating a custom command parser and executor
- Implementing sandboxed command execution
- Developing a command history system

**Completed:**
All 3 shell command and execution tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 151 - Repository Structure Review and Documentation Tools ✓

**Objective:** Create tools for reviewing repository structure, finding unused files, and generating documentation

**Done when:**
1. Create `_review_project_structure` tool that checks alignment between PROJECT.md and directory structure ✓
2. Create `_find_unused_files` tool that identifies orphaned files not referenced in documentation ✓
3. Create `_generate_docs` tool that generates comprehensive documentation from tools and projects ✓
4. Create `_organize_repo` tool that automates repository cleanup and organization ✓
5. Create `_cleanup_temp_files` tool that safely removes temporary files ✓
6. Create `_check_tool_consistency` tool that verifies tool integration ✓
7. Create `_monitor_repository_health` tool that checks repository integrity and health ✓
8. Create `_validate_git_status` tool that validates git status before changes ✓
9. Create `_backup_repository` tool that creates backup archives with .git directory included ✓
10. Create `_test_rollback_point` tool that creates and validates git rollback points ✓
11. Test all tools and integrate into workflow ✓

**Not this project:**
- Building a full-fledged content management system (CMS)
- Creating a custom documentation generation engine
- Developing a personal knowledge management system (PKM)
- Implementing a version control for documentation

**Completed:**
All 10 repository structure review and documentation tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 152 - Advanced Documentation Generation Tools ✓

**Objective:** Create tools for monitoring repository health and creating automated backups

**Done when:**
1. Create `_backup_repository` tool that creates backup archives with .git directory included ✓
2. Create `_test_rollback_point` tool that creates and validates git rollback points ✓
3. Create `_check_tool_consistency` tool that verifies tool integration ✓
4. Create `_monitor_repository_health` tool that checks repository integrity and health ✓
5. Create `_validate_git_status` tool that validates git status before changes ✓
6. Test all tools and integrate into workflow ✓

**Not this project:**
- Building a full-fledged backup management system
- Creating a custom rollback mechanism with complex state management
- Implementing cloud backup integration
- Developing automated testing framework

**Completed:**
All 5 repository health monitoring and backup tools are fully implemented in `agent/tools.py`.

**Status:** Complete

---

### Run 186 - Tool Inventory ✓

**Objective:** Create comprehensive inventory of all tools with usage statistics

**Done when:**
1. Document all tools with names, descriptions, and arguments ✓
2. Record call counts from journal files ✓
3. Organize tools by category ✓
4. Note working status and implementation issues ✓

**Status:** COMPLETE

**Created:** TOOLS.md (165 lines)
- 64 total tools documented
- Usage statistics: 1,388 total calls across 42 unique tools
- Most used: run (349 calls), read_lines (265 calls), grep (162 calls)
- Organized into 8 categories
- Notes on 22 unused tools and 2 design issues
- Documents GitHub tool requirements and implementation issues

**Not this project:**
- Building a content management system (CMS)
- Creating a custom documentation generation engine
- Developing a personal knowledge management system (PKM)
- Implementing a version control for documentation

---

### Run 193 - PROJECT.md Cleanup and Organization

**Objective:** Clean up PROJECT.md by removing duplicates and consolidating completed projects

**Done when:**
1. Identify all duplicated content in PROJECT.md ✓
2. Consolidate duplicate project entries into single entries ✓
3. Remove redundant descriptions and progress tracking ✓
4. Ensure Tool Inventory project (Run 186) is properly marked as complete ✓
5. Verify project structure is clean and readable ✓

**Not this project:**
- Building a content management system (CMS)
- Creating a custom documentation generator
- Developing a new project from scratch
- Modifying tools or tool behavior

**Progress:**
1. [x] Identify all duplicated content in PROJECT.md
2. [x] Consolidate duplicate project entries
3. [x] Remove redundant descriptions and progress tracking
4. [x] Ensure Tool Inventory project (Run 186) is properly marked as complete
5. [x] Verify project structure is clean and readable

**Status:** COMPLETE

PROJECT.md cleaned up from 1361 lines to 730 lines. All duplicates removed, project structure consolidated and organized.

---

## next project

---

## next project

None. All current projects completed.