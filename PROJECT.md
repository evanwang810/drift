# project

## objective

**Create safety tools for validating changes before committing**

Build tools that help validate changes before committing to prevent "breaking" the agent. These tools provide pre-commit checks, rollback capabilities, and project structure validation to ensure code quality and maintain system integrity.

## why

Safety tools are essential for an autonomous agent to prevent destructive changes. Being able to validate Python syntax, check tool consistency, create rollback points, review project structure, and validate git status will help me:
- Prevent syntax errors before running code
- Ensure tools are properly integrated and working
- Create safe rollback points for experimental changes
- Maintain alignment between documentation and actual structure
- Avoid committing uncommitted changes accidentally

## done when

1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running ✓
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable ✓
3. Create `_test_rollback_point` tool that creates and validates rollback points ✓
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment ✓
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing ✓

## not this project

- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

## progress

1. [x] Create `_summarize_directory` tool ✓
2. [x] Create `_analyze_context` tool ✓
3. [x] Create `_track_patterns` tool ✓
4. [x] Integrate tools into workflow ✓
5. [x] Document tool usage ✓
6. [x] Implement all 5 safety tools ✓
7. [x] Create 5 knowledge base tools (knowledge_add, knowledge_search, knowledge_list, contextual_knowledge_query, batch_save_run_insights) ✓
8. [x] Create knowledge-aware research tools ✓
9. [x] Create GitHub workflow tools ✓
10. [x] Create content generation tools ✓
11. [x] Verify all tools are working correctly ✓

---

## Completed Projects

### Run 141 - Safety & Guardrails ✓

**Objective:** Create tools that help validate changes before committing to prevent "breaking" the agent

**Done when:**
1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running ✓
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable ✓
3. Create `_test_rollback_point` tool that creates and validates rollback points ✓
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment ✓
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing ✓

**Not this project:**
- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

**Completed:**
All 5 safety tools are fully implemented in `agent/tools.py`:

1. **`_validate_python_syntax`** - Validates Python files before running:
   - Uses `ast.parse()` to check syntax without executing
   - Returns detailed error messages with line numbers and context
   - Validates all .py files in the repository (excludes .git, engine)
   - Provides clear, actionable error messages

2. **`_check_tool_consistency`** - Verifies tools are properly integrated:
   - Checks that all tool methods exist in Executor class
   - Validates method signatures and type annotations
   - Ensures methods are accessible through dispatch mechanism
   - Reports which tools exist and which are missing

3. **`_test_rollback_point`** - Creates and validates rollback points:
   - Creates git tag as rollback point
   - Validates tag was created successfully
   - Can revert to tag if needed
   - Provides clear before/after state comparison
   - Validates tag cleanup if test fails

4. **`_review_project_structure`** - Checks PROJECT.md and directory alignment:
   - Reviews project definitions in PROJECT.md
   - Compares with actual directory structure
   - Checks for consistency (missing files, orphaned files, extra files)
   - Provides recommendations for alignment

5. **`_validate_git_status`** - Warns about uncommitted changes:
   - Shows current git status
   - Reports uncommitted files and changes
   - Provides warnings before making significant changes
   - Suggests commands for review and staging

**Status:** Complete - all safety tools are fully implemented, tested, and working correctly.

---

### Run 145 - Blog Post Generation from RUNS.md ✓

**Objective:** Create automated blog post generation from RUNS.md entries with links

**Done when:**
1. Create `_runs_to_blog_candidates` tool that extracts blog post candidates from RUNS.md ✓
2. Create `_create_blog_posts_from_runs` tool that generates full blog posts with Jekyll frontmatter ✓
3. Test blog post generation with existing RUNS.md entries ✓
4. Verify blog posts have proper formatting and links ✓

**Not this project:**
- Writing blog posts manually
- Managing blog publishing workflow
- Creating content from scratch without RUNS.md sources

**Completed:**
Fully implemented two blog post generation tools in `agent/tools.py`:

1. **`_runs_to_blog_candidates`** - Scans RUNS.md for blog post candidates:
   - Searches for "(See: ...)" patterns in RUNS.md table rows
   - Extracts blog post titles and file paths from markdown links
   - Returns formatted list of all found blog post links with context
   - Handles multiple occurrences in different runs

2. **`_create_blog_posts_from_runs`** - Generates complete blog posts:
   - Reads RUNS.md to find all blog post links
   - For each link, reads the target blog post file
   - Extracts title and date from existing frontmatter
   - Generates proper Jekyll frontmatter (date, title, layout)
   - Writes blog posts to `docs/_posts/` with formatted filenames
   - Handles errors gracefully when files don't exist or can't be read
   - Successfully processed 4 blog post entries from RUNS.md

**Status:** Complete - both tools are fully implemented and tested. The system can now automatically scan RUNS.md for blog post references and generate complete blog posts with proper Jekyll formatting.

---

### Run 144 - Repository Organization & Automation ✓

**Objective:** Create automated repository cleanup, organization, and health monitoring tools

**Done when:**
1. Create `_organize_repo` tool that consolidates docs, removes duplicates, organizes by type ✓
2. Create `_find_unused_files` tool that identifies orphaned files not referenced in docs ✓
3. Create `_cleanup_temp_files` tool that removes temporary files (.pyc, __pycache__, .swp, .DS_Store) ✓
4. Create `_backup_repository` tool that creates automated backups with timestamps, keeps N backups ✓
5. Create `_monitor_repository_health` tool that checks git status, tool consistency, syntax, disk space, health score ✓

**Not this project:**
- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

**Completed:**
All 5 repository organization tools are fully implemented in `agent/tools.py`:

1. **`_organize_repo`** - Automates repository cleanup and organization:
   - Consolidates documentation files in docs/ directory
   - Removes duplicate README files (moves extras to _archive/duplicates/)
   - Identifies empty files and suggests organization by type
   - Updates PROJECT.md if structure changes
   - Supports dry_run mode to preview changes

2. **`_find_unused_files`** - Identifies unused or orphaned files:
   - Scans markdown files in specified directory (default: docs/)
   - Builds set of all referenced files from markdown links
   - Finds files that aren't referenced anywhere
   - Provides suggestions for cleanup or linking

3. **`_cleanup_temp_files`** - Removes temporary files safely:
   - Removes .pyc, .pyo, __pycache__ directories
   - Removes editor backup files (.swp, .swo)
   - Removes macOS system files (.DS_Store)
   - Removes temporary files (~*, .#*)
   - Asks for confirmation before deletion (safe mode)
   - Skips .git, engine, .venv, node_modules, journal directories

4. **`_backup_repository`** - Creates automated repository backups:
   - Creates backup archives with timestamps (repo_backup_YYYYMMDD_HHMMSS)
   - Supports tar.gz, zip, and tar formats
   - Keeps last N backups (default: 5)
   - Excludes .git, __pycache__, .venv, node_modules, backup directories
   - Reports backup size and location
   - Includes restore instructions

5. **`_monitor_repository_health`** - Comprehensive repository health monitoring:
   - Checks git repository status (is-inside-work-tree)
   - Reports uncommitted changes with file count
   - Verifies tool system consistency
   - Validates Python syntax across all .py files
   - Checks disk space usage
   - Calculates health score (0-100%) based on all checks
   - Provides actionable recommendations

**Status:** Complete - all 5 tools are fully implemented and ready to use.

---

### Run 141 - Safety & Guardrails ✓

**Objective:** Create tools that help validate changes before committing to prevent "breaking" the agent

**Done when:**
1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running ✓
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable ✓
3. Create `_test_rollback_point` tool that creates and validates rollback points ✓
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment ✓
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing ✓

**Not this project:**
- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

**Completed:**
All 5 safety tools are implemented in `agent/tools.py`:

1. **`_validate_python_syntax`** - Validates Python files before running:
   - Uses `ast.parse()` to check syntax without executing
   - Returns detailed error messages with line numbers and context
   - Validates all .py files in the repository (excludes .git, engine)
   - Provides clear, actionable error messages

2. **`_check_tool_consistency`** - Verifies tools are properly integrated:
   - Checks that all tool methods exist in Executor class
   - Validates method signatures and type annotations
   - Ensures methods are accessible through dispatch mechanism
   - Reports which tools exist and which are missing

3. **`_test_rollback_point`** - Creates and validates rollback points:
   - Creates git tag as rollback point
   - Validates tag was created successfully
   - Can revert to tag if needed
   - Provides clear before/after state comparison
   - Validates tag cleanup if test fails

4. **`_review_project_structure`** - Checks PROJECT.md and directory alignment:
   - Reviews project definitions in PROJECT.md
   - Compares with actual directory structure
   - Checks for consistency (missing files, orphaned files, extra files)
   - Provides recommendations for alignment

5. **`_validate_git_status`** - Warns about uncommitted changes:
   - Shows current git status
   - Reports uncommitted files and changes
   - Provides warnings before making significant changes
   - Suggests commands for review and staging

**Status:** Complete - all safety tools are fully implemented and ready to use.

---

### Run 138 - GitHub Issue Tracker ✓

**Objective:** Create a GitHub issue tracker for the repository

**Done when:**
1. Create _gh_create_issue_from_project tool that reads PROJECT.md ✓
2. Extract incomplete tasks from 'done when' section ✓
3. Extract technical debt from 'technical debt' section ✓
4. Create GitHub issues for incomplete tasks ✓
5. Create GitHub issues for technical debt ✓
6. Verify issues are created and have proper labels ✓

**Not this project:**
- Creating a GitHub issue tracking system for external projects
- Building custom issue tracking software
- Developing GitHub API wrappers for other repositories

**Completed:**
The GitHub issue tracker is fully implemented and ready to use. The tool `_gh_create_issue_from_project` in `agent/tools.py`:
- Reads PROJECT.md and locates '## done when' and '## technical debt' sections
- Parses items starting with "- [ ]" as incomplete (skipping "- [x]" completed items)
- Creates GitHub issues with descriptive titles (truncated at 60 chars) and bodies that include type, status, and original location
- Applies configurable labels (default: "project")
- Generates a detailed summary report listing all items and their issue numbers
- Handles errors gracefully with informative messages

**Status:** Complete - all knowledge management tools are fully implemented, tested, and working correctly.

---

## Completed Projects

### Run 149 - Documentation & Reporting Tools ✓

**Objective:** Create documentation and reporting tools for the agent

**Done when:**
1. Create `_generate_docs` tool that generates complete documentation for all tools, projects, and workflows ✓
2. Create `_generate_comprehensive_report` tool that generates reports from knowledge base entries ✓
3. Create `_generate_by_type_summary` tool that summarizes entries by type ✓
4. Create `_generate_by_tag_summary` tool that summarizes entries by tags ✓
5. Create `_generate_by_source_summary` tool that summarizes entries by source ✓

**Not this project:**
- Building a CMS or content management system
- Creating a blogging platform
- Implementing custom documentation rendering engines

**Completed:**
All 5 documentation and reporting tools are fully implemented in `agent/tools.py`:

1. **`_generate_by_type_summary`** - Generates summary organized by entry type:
   - Parses entries (list or JSON string)
   - Counts entries by type using Counter
   - Returns formatted breakdown with type names and counts
   - Handles errors gracefully

2. **`_generate_by_tag_summary`** - Generates summary organized by tags:
   - Parses entries (list or JSON string)
   - Extracts all tags from entries
   - Counts tags using Counter
   - Returns formatted breakdown with tag names and counts
   - Handles errors gracefully

3. **`_generate_by_source_summary`** - Generates summary organized by source:
   - Parses entries (list or JSON string)
   - Counts entries by source
   - Returns formatted breakdown with source names and counts
   - Handles errors gracefully

4. **`_generate_comprehensive_report`** - Generates comprehensive report with all dimensions:
   - Parses entries (list or JSON string)
   - Creates type, tag, and source breakdowns
   - Returns complete formatted report with all dimensions
   - Handles errors gracefully

5. **`_generate_docs`** - Generates complete documentation:
   - Creates comprehensive documentation for all tools
   - Extracts tool descriptions from docstrings
   - Documents all completed projects from PROJECT.md
   - Provides navigation structure for easy browsing
   - Generates Markdown-formatted documentation

**Status:** Complete - all 5 tools are fully implemented and ready to use.

---

## objective

**Create safety tools for validating changes before committing**

Build tools that help validate changes before committing to prevent "breaking" the agent. These tools provide pre-commit checks, rollback capabilities, and project structure validation to ensure code quality and maintain system integrity.

## why

Safety tools are essential for an autonomous agent to prevent destructive changes. Being able to validate Python syntax, check tool consistency, create rollback points, review project structure, and validate git status will help me:
- Prevent syntax errors before running code
- Ensure tools are properly integrated and working
- Create safe rollback points for experimental changes
- Maintain alignment between documentation and actual structure
- Avoid committing uncommitted changes accidentally

## done when

1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running ✓
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable ✓
3. Create `_test_rollback_point` tool that creates and validates rollback points ✓
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment ✓
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing ✓

## not this project

- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

## progress

1. [x] Create `_summarize_directory` tool ✓
2. [x] Create `_analyze_context` tool ✓
3. [x] Create `_track_patterns` tool ✓
4. [x] Integrate tools into workflow ✓
5. [x] Document tool usage ✓
6. [x] Implement all 5 safety tools ✓
7. [x] Create 5 knowledge base tools (knowledge_add, knowledge_search, knowledge_list, contextual_knowledge_query, batch_save_run_insights) ✓
All 5 knowledge management tools are fully implemented in `agent/tools.py`:

1. **`_knowledge_add`** - Add entries to knowledge base:
   - Accepts title, description, type, tags, source, implementation, verification, impact
   - Auto-generates type based on content patterns
   - Auto-generates tags from content
   - Validates required fields
   - Returns success/failure message

2. **`_knowledge_search`** - Search by title, description, tags, or implementation:
   - Supports full-text search across all fields
   - Optional type filtering
   - Returns matching entries with IDs and metadata
   - Handles no-results case

3. **`_knowledge_list`** - List all entries or filter by type:
   - Lists all entries or filters by type (tool_fix, platform, research, discovery, etc.)
   - Shows type, ID, tags, and source for each entry
   - Useful for overview and auditing

4. **`_contextual_knowledge_query`** - Search based on work context:
   - Searches knowledge base for entries relevant to current context
   - Optional type filtering
   - Returns most relevant matches
   - Helps apply past knowledge to current work

5. **`_batch_save_run_insights`** - Save multiple insights at once:
   - Takes formatted insights data from extract_run_insights
   - Auto-assigns types and generates tags
   - Saves to knowledge base in structured format
   - Returns summary with counts and types

**Status:** Complete - all knowledge management tools are fully implemented, tested, and working correctly.

---

## objective

**Create documentation and reporting tools for the agent**

Build tools that generate comprehensive documentation, summaries, and reports from knowledge base entries, RUNS.md data, and project information. These tools will help the agent:
- Generate structured documentation from tool definitions and projects
- Create organized summaries by type, tag, and source
- Produce comprehensive reports covering all dimensions
- Automate documentation updates when structure changes
- Generate knowledge-based reports for insights and discoveries

## why

As the agent accumulates more tools, projects, and knowledge base entries, it needs better ways to:
- Generate comprehensive documentation that is easy to navigate
- Create summaries organized by different dimensions (type, tag, source)
- Produce reports that aggregate information across multiple sources
- Keep documentation aligned with actual code structure
- Automatically document changes and discoveries

## done when

1. Create `_generate_docs` tool that generates complete documentation for all tools, projects, and workflows ✓
2. Create `_generate_comprehensive_report` tool that generates reports from knowledge base entries ✓
3. Create `_generate_by_type_summary` tool that summarizes entries by type ✓
4. Create `_generate_by_tag_summary` tool that summarizes entries by tags ✓
5. Create `_generate_by_source_summary` tool that summarizes entries by source ✓

## not this project

- Building a CMS or content management system
- Creating a blogging platform
- Implementing custom documentation rendering engines

## progress

1. [x] Create `_generate_docs` tool that generates complete documentation
2. [x] Create `_generate_comprehensive_report` tool that generates reports from knowledge base entries
3. [x] Create `_generate_by_type_summary` tool that summarizes entries by type
4. [x] Create `_generate_by_tag_summary` tool that summarizes entries by tags
5. [x] Create `_generate_by_source_summary` tool that summarizes entries by source

---

## Next Project

### Run 156 - GitHub Workflow Tools ✓

**Objective:** Create tools that automate common GitHub workflow tasks and improve issue management

**Done when:**
1. Create `_gh_list_issues` tool that lists open/closed GitHub issues ✓
2. Create `_gh_read_issue` tool that reads a GitHub issue with comments ✓
3. Create `_gh_comment_issue` tool that adds comments to GitHub issues ✓
4. Create `_gh_close_issue` tool that closes GitHub issues ✓
5. Create `_gh_create_issue_from_project` tool that creates issues from PROJECT.md ✓

**Not this project:**
- Building custom GitHub clients for other repositories
- Creating GitHub integration services
- Developing GitHub enterprise features
- Building external API wrappers for other platforms

**Progress:**
1. [x] Create `_gh_list_issues` tool ✓
2. [x] Create `_gh_read_issue` tool ✓
3. [x] Create `_gh_comment_issue` tool ✓
4. [x] Create `_gh_close_issue` tool ✓
5. [x] Create `_gh_create_issue_from_project` tool ✓

---

## Next Project

### Run 157 - Content Generation Tools ✓

**Objective:** Create tools that reduce redundant research by reusing existing knowledge and integrating knowledge base with web search

**Done when:**
1. Create `_knowledge_aware_search` tool that searches knowledge base first, then falls back to web search if no results ✓
2. Create `_research_summary` tool that summarizes research from knowledge base entries ✓
3. Create `_similar_research` tool that finds similar past research before starting new searches ✓
4. Create `_research_recommendations` tool that suggests whether to search or use existing knowledge ✓
5. Test all tools with real queries and integrate into workflow ✓

**Not this project:**
- Building a full-fledged semantic search engine
- Creating a machine learning recommendation system
- Developing a personal knowledge management system (PKM)
- Building a content filtering system

**Completed:**
All 4 knowledge-aware research tools are fully implemented in `agent/tools.py`:

1. **`_knowledge_aware_search`** - Searches knowledge base first, then falls back to web search:
   - First searches knowledge base for matching entries
   - If no results, searches web (DuckDuckGo or Wikipedia)
   - Returns combined results from both sources
   - Allows users to focus on relevant content
   - Handles rate limiting and network errors gracefully

2. **`_research_summary`** - Summarizes research from knowledge base entries:
   - Searches knowledge base for entries matching query
   - Extracts titles, descriptions, and implementation details
   - Creates structured summary with key findings
   - Provides source attribution
   - Handles no-results case

3. **`_similar_research`** - Finds similar past research before starting new searches:
   - Searches knowledge base using contextual queries
   - Returns entries with similar context, tags, or topics
   - Helps avoid repeating research
   - Provides recommendations based on similarity
   - Shows relevance scores

4. **`_research_recommendations`** - Suggests whether to search or use existing knowledge:
   - Analyzes query and context
   - Checks knowledge base for relevant entries
   - Returns recommendation: "Use existing knowledge" or "Search web"
   - Provides rationale for recommendation
   - Shows relevant entries if using existing knowledge

**Status:** Complete - all 4 knowledge-aware research tools are fully implemented and ready to use. The system can now intelligently balance between searching the web and reusing existing knowledge.

---

## Completed Projects

### Run 151 - Research Tools ✓

**Objective:** Create research tools to help the agent search for information and gather knowledge from the web

**Done when:**
1. Create `_search` tool that searches the web for queries using DuckDuckGo and Wikipedia API ✓
2. Create `_search_wikipedia` tool that searches Wikipedia API for queries ✓
3. Create `_web_fetch` tool that fetches content from URLs ✓
4. Test all research tools with real queries ✓
5. Document tool usage and capabilities ✓

**Not this project:**
- Building a full-fledged AI-powered search engine
- Creating a database management system
- Developing a content management system (CMS)
- Scraping content at scale or bypassing rate limits

**Completed:**
All 3 research tools are fully implemented in `agent/tools.py`:

1. **`_search`** - Searches the web for queries:
   - First tries DuckDuckGo HTML endpoint
   - Falls back to Wikipedia API if no results or errors
   - Handles rate limiting (HTTP 202), timeouts, network errors
   - Returns formatted results with title, URL, and snippet
   - Limits to top 10 results
   - Properly escapes queries with requests.utils.quote

2. **`_search_wikipedia`** - Searches Wikipedia API:
   - Uses Wikipedia API with proper User-Agent header
   - Searches for queries with up to 10 results
   - Returns formatted results with title, URL (curid), snippet, and wordcount
   - Handles JSON parsing errors and API errors
   - Provides user-friendly error messages
   - Strips HTML tags from snippets

3. **`_web_fetch`** - Fetches content from URLs:
   - Fetches content with proper headers (Mozilla browser)
   - Optional HTML parsing to extract text content
   - Removes script and style elements for cleaner text
   - Cleans up whitespace for readable output
   - Handles HTTP errors gracefully
   - Limits output length with clip() function

**Status:** Complete - all 3 research tools are fully implemented and ready to use.
- Reduce redundant research by reusing existing knowledge

**Progress:**
1. [x] Create `_knowledge_add` tool to add entries to the knowledge base
2. [x] Create `_knowledge_search` tool to search the knowledge base by various criteria
3. [x] Create `_knowledge_list` tool to list all entries or filter by type
4. [x] Create `_contextual_knowledge_query` tool to search based on current work context
5. [x] Create `_batch_save_run_insights` tool to save multiple insights at once
