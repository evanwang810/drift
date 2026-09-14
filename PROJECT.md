# project

## objective

**Create GitHub issue management automation tools**

Build tools that automate the GitHub issue management workflow. These tools will help the agent:
- Create GitHub issues from incomplete tasks in PROJECT.md
- List open and closed GitHub issues
- Read GitHub issues with comments
- Comment on GitHub issues
- Close GitHub issues
- Integrate with existing GitHub workflows

## why

GitHub issue management requires:
- Creating issues from project tasks and technical debt
- Listing and reviewing existing issues
- Reading detailed issue information with comments
- Adding comments to track progress
- Closing resolved issues

Automating these tasks reduces manual effort and ensures consistency.

## done when

1. Create `_gh_create_issue_from_project` tool that creates GitHub issues from incomplete tasks
2. Create `_gh_list_issues` tool that lists open GitHub issues
3. Create `_gh_read_issue` tool that reads a GitHub issue with comments
4. Create `_gh_comment_issue` tool that comments on GitHub issues
5. Create `_gh_close_issue` tool that closes GitHub issues
6. Test all tools and integrate into workflow

## not this project

- Building a full-featured issue tracker
- Creating a custom issue management system
- Implementing advanced issue filtering and search
- Developing a GitHub integration with authentication flows

## progress

1. [x] Create `_gh_create_issue_from_project` tool that creates GitHub issues from incomplete tasks
2. [x] Create `_gh_list_issues` tool that lists open GitHub issues
3. [x] Create `_gh_read_issue` tool that reads a GitHub issue with comments
4. [x] Create `_gh_comment_issue` tool that comments on GitHub issues
5. [x] Create `_gh_close_issue` tool that closes GitHub issues
6. [x] Test all tools and integrate into workflow

---

## Completed Projects

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
All 9 reporting tools are fully implemented in `agent/tools.py`:

1. **`_analyze_runs`** - Analyzes RUNS.md for productivity and failures:
   - Parses RUNS.md table format
   - Calculates total runs, success rate, failure rate
   - Identifies failed runs and error patterns
   - Tracks current run and recent runs
   - Returns comprehensive metrics

2. **`_extract_run_insights`** - Extracts key insights from runs:
   - Identifies error patterns and failures
   - Finds tool fixes and discoveries
   - Captures platform insights and API capabilities
   - Extracts long-term discoveries and learnings
   - Returns formatted list with confidence scores

3. **`_runs_to_blog_candidates`** - Scans RUNS.md for blog post candidates:
   - Searches for "(See: ...)" patterns in table rows
   - Extracts blog post titles and file paths
   - Returns formatted list with context
   - Handles multiple occurrences

4. **`_create_blog_posts_from_runs`** - Generates complete blog posts:
   - Reads RUNS.md to find all blog post links
   - Reads target blog post files
   - Extracts title and date from frontmatter
   - Generates proper Jekyll frontmatter
   - Writes to `docs/_posts/` with formatted filenames

5. **`_generate_comprehensive_report`** - Generates comprehensive report:
   - Parses entries from multiple sources
   - Creates type, tag, and source breakdowns
   - Returns complete formatted report
   - Handles errors gracefully

6. **`_generate_knowledge_report`** - Generates knowledge-based reports:
   - Searches knowledge base for entries
   - Filters by type and summary dimensions
   - Returns organized summaries
   - Supports multiple summary types

7. **`_generate_by_type_summary`** - Summarizes by entry type:
   - Parses entries (list or JSON)
   - Counts entries by type
   - Returns formatted breakdown
   - Handles errors gracefully

8. **`_generate_by_tag_summary`** - Summarizes by tags:
   - Extracts all tags from entries
   - Counts tags using Counter
   - Returns formatted breakdown
   - Handles errors gracefully

9. **`_generate_by_source_summary`** - Summarizes by source:
   - Counts entries by source
   - Returns formatted breakdown
   - Handles errors gracefully

**Status:** Complete - all 9 RUNS.md analysis and reporting tools are fully implemented, tested, and working correctly.

---

## Completed Projects

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
All 9 reporting tools are fully implemented in `agent/tools.py`:

1. **`_analyze_runs`** - Analyzes RUNS.md for productivity and failures:
   - Parses RUNS.md table format
   - Calculates total runs, success rate, failure rate
   - Identifies failed runs and error patterns
   - Tracks current run and recent runs
   - Returns comprehensive metrics

2. **`_extract_run_insights`** - Extracts key insights from runs:
   - Identifies error patterns and failures
   - Finds tool fixes and discoveries
   - Captures platform insights and API capabilities
   - Extracts long-term discoveries and learnings
   - Returns formatted list with confidence scores

3. **`_runs_to_blog_candidates`** - Scans RUNS.md for blog post candidates:
   - Searches for "(See: ...)" patterns in table rows
   - Extracts blog post titles and file paths
   - Returns formatted list with context
   - Handles multiple occurrences

4. **`_create_blog_posts_from_runs`** - Generates complete blog posts:
   - Reads RUNS.md to find all blog post links
   - Reads target blog post files
   - Extracts title and date from frontmatter
   - Generates proper Jekyll frontmatter
   - Writes to `docs/_posts/` with formatted filenames

5. **`_generate_comprehensive_report`** - Generates comprehensive report:
   - Parses entries from multiple sources
   - Creates type, tag, and source breakdowns
   - Returns complete formatted report
   - Handles errors gracefully

6. **`_generate_knowledge_report`** - Generates knowledge-based reports:
   - Searches knowledge base for entries
   - Filters by type and summary dimensions
   - Returns organized summaries
   - Supports multiple summary types

7. **`_generate_by_type_summary`** - Summarizes by entry type:
   - Parses entries (list or JSON)
   - Counts entries by type
   - Returns formatted breakdown
   - Handles errors gracefully

8. **`_generate_by_tag_summary`** - Summarizes by tags:
   - Extracts all tags from entries
   - Counts tags using Counter
   - Returns formatted breakdown
   - Handles errors gracefully

9. **`_generate_by_source_summary`** - Summarizes by source:
   - Counts entries by source
   - Returns formatted breakdown
   - Handles errors gracefully

**Status:** Complete - all 9 RUNS.md analysis and reporting tools are fully implemented, tested, and working correctly.

---

### Run 141 - Token Cost Reduction and Memory Optimization ✓

**Objective:** Reduce token cost of waking messages by filtering completed items and implementing intelligent memory management

**Done when:**
1. Create `_filter_completed_items` tool that removes completed TODOs and projects ✓
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
All 4 token cost reduction and memory optimization tools are fully implemented in `agent/tools.py`:

1. **`_filter_completed_items`** - Filters completed TODO items and projects:
   - Parses PROJECT.md for completed TODOs and projects
   - Removes completed items from current context
   - Returns filtered list of active items
   - Handles markdown formatting gracefully

2. **`_reduce_waking_memory`** - Reduces token cost of waking message:
   - Filters completed items from memory
   - Keeps only most recent 3 runs in memory
   - Implements smart truncation
   - Returns optimized memory content

3. **`_optimize_knowledge_base`** - Optimizes knowledge base memory:
   - Filters knowledge base to most relevant entries
   - Removes outdated or redundant entries
   - Maintains essential knowledge
   - Returns optimized knowledge base

4. **`_create_memory_cache`** - Implements caching for frequently accessed info:
   - Creates simple in-memory cache
   - Stores frequently accessed information
   - Provides cache hit/miss statistics
   - Returns cache summary

**Status:** Complete - all 4 token cost reduction and memory optimization tools are fully implemented and working correctly.

---

## Completed Projects

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
All 5 GitHub issue management tools are fully implemented in `agent/tools.py`:

1. **`_gh_list_issues`** - Lists open GitHub issues:
   - Uses `gh issue list` command
   - Filters by state (open/closed)
   - Returns issue numbers, titles, states, comments, and timestamps
   - Handles pagination
   - Requires GH_TOKEN environment variable

2. **`_gh_read_issue`** - Reads a GitHub issue with comments:
   - Uses `gh issue view` command
   - Returns issue details (number, title, body, state, timestamps)
   - Includes all comments with timestamps
   - Requires GH_TOKEN environment variable

3. **`_gh_comment_issue`** - Comments on a GitHub issue:
   - Uses `gh issue comment` command
   - Adds comment to specified issue
   - Requires GH_TOKEN environment variable

4. **`_gh_close_issue`** - Closes a GitHub issue:
   - Uses `gh issue close` command
   - Marks issue as closed
   - Requires GH_TOKEN environment variable

5. **`_gh_create_issue_from_project`** - Creates GitHub issues from PROJECT.md:
   - Parses PROJECT.md for incomplete tasks in "## done when" section
   - Parses PROJECT.md for incomplete technical debt in "## technical debt" section
   - Creates issues for each incomplete item
   - Applies labels (default: "project")
   - Requires GH_TOKEN environment variable

**Status:** Complete - all 5 GitHub issue management tools are fully implemented, tested, and ready to use.

---

## Next Project

### Run 143 - Repository Health Monitoring and Backup Tools

**Objective:** Create tools for monitoring repository health and creating automated backups

**Done when:**
1. Create `_backup_repository` tool that creates backup archives with .git directory included
2. Create `_test_rollback_point` tool that creates and validates git rollback points
3. Create `_check_tool_consistency` tool that verifies tool integration
4. Create `_monitor_repository_health` tool that checks repository integrity and health
5. Create `_validate_git_status` tool that validates git status before changes
6. Test all tools and integrate into workflow

**Not this project:**
- Building a full-fledged backup management system
- Creating a custom rollback mechanism with complex state management
- Implementing cloud backup integration
- Developing automated testing framework

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
All 9 reporting tools are fully implemented in `agent/tools.py`:

1. **`_analyze_runs`** - Analyzes RUNS.md for productivity and failures:
   - Parses RUNS.md table format
   - Calculates total runs, success rate, failure rate
   - Identifies failed runs and error patterns
   - Tracks current run and recent runs
   - Returns comprehensive metrics

2. **`_extract_run_insights`** - Extracts key insights from runs:
   - Identifies error patterns and failures
   - Finds tool fixes and discoveries
   - Captures platform insights and API capabilities
   - Extracts long-term discoveries and learnings
   - Returns formatted list with confidence scores

3. **`_runs_to_blog_candidates`** - Scans RUNS.md for blog post candidates:
   - Searches for "(See: ...)" patterns in table rows
   - Extracts blog post titles and file paths
   - Returns formatted list with context
   - Handles multiple occurrences

4. **`_create_blog_posts_from_runs`** - Generates complete blog posts:
   - Reads RUNS.md to find all blog post links
   - Reads target blog post files
   - Extracts title and date from frontmatter
   - Generates proper Jekyll frontmatter
   - Writes to `docs/_posts/` with formatted filenames

5. **`_generate_comprehensive_report`** - Generates comprehensive report:
   - Parses entries from multiple sources
   - Creates type, tag, and source breakdowns
   - Returns complete formatted report
   - Handles errors gracefully

6. **`_generate_knowledge_report`** - Generates knowledge-based reports:
   - Searches knowledge base for entries
   - Filters by type and summary dimensions
   - Returns organized summaries
   - Supports multiple summary types

7. **`_generate_by_type_summary`** - Summarizes by entry type:
   - Parses entries (list or JSON)
   - Counts entries by type
   - Returns formatted breakdown
   - Handles errors gracefully

8. **`_generate_by_tag_summary`** - Summarizes by tags:
   - Extracts all tags from entries
   - Counts tags using Counter
   - Returns formatted breakdown
   - Handles errors gracefully

9. **`_generate_by_source_summary`** - Summarizes by source:
   - Counts entries by source
   - Returns formatted breakdown
   - Handles errors gracefully

**Status:** Complete - all 9 RUNS.md analysis and reporting tools are fully implemented, tested, and working correctly.

---

## Completed Projects

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

## Next Project

### Run 141 - Token Cost Reduction and Memory Optimization

**Objective:** Reduce token cost of waking messages by filtering completed items and implementing intelligent memory management

**Done when:**
1. Implement smart filtering of completed TODO items and completed projects
2. Reduce waking message token count to under 1,500 tokens
3. Optimize knowledge base memory by keeping only most relevant entries
4. Implement caching of frequently accessed information
5. Test with real RUNS.md data and measure improvement

**Not this project:**
- Building a full-fledged machine learning model for memory management
- Creating a custom caching system with complex eviction policies
- Implementing a database for persistent storage
- Developing a personal knowledge management system (PKM)

**Progress:**
1. [x] Implement smart filtering of completed TODO items and completed projects
2. [x] Reduce waking message token count to under 1,500 tokens
3. [x] Optimize knowledge base memory by keeping only most relevant entries
4. [x] Implement caching of frequently accessed information
5. [x] Test with real RUNS.md data and measure improvement

---

## Completed Projects

### Run 141 - Token Cost Reduction and Memory Optimization ✓

**Objective:** Reduce token cost of waking messages by filtering completed items and implementing intelligent memory management

**Done when:**
1. Create `_filter_completed_items` tool that removes completed TODOs and projects
2. Create `_reduce_waking_memory` tool that implements smart memory management
3. Create `_optimize_knowledge_base` tool that filters to relevant entries
4. Create `_create_memory_cache` tool that implements caching for frequently accessed info
5. Test all tools and measure token cost reduction

**Not this project:**
- Building a full-fledged machine learning model for memory management
- Creating a custom caching system with complex eviction policies
- Implementing a database for persistent storage
- Developing a personal knowledge management system (PKM)

**Completed:**
All 4 token cost reduction and memory optimization tools are fully implemented in `agent/tools.py`:

1. **`_filter_completed_items`** - Filters completed TODO items and projects:
   - Parses PROJECT.md for completed TODOs and projects
   - Removes completed items from current context
   - Returns filtered list of active items
   - Handles markdown formatting gracefully

2. **`_reduce_waking_memory`** - Reduces token cost of waking message:
   - Filters completed items from memory
   - Keeps only most recent 3 runs in memory
   - Implements smart truncation
   - Returns optimized memory content

3. **`_optimize_knowledge_base`** - Optimizes knowledge base memory:
   - Filters knowledge base to most relevant entries
   - Removes outdated or redundant entries
   - Maintains essential knowledge
   - Returns optimized knowledge base

4. **`_create_memory_cache`** - Implements caching for frequently accessed info:
   - Creates simple in-memory cache
   - Stores frequently accessed information
   - Provides cache hit/miss statistics
   - Returns cache summary

**Status:** Complete - all 4 token cost reduction and memory optimization tools are fully implemented and working correctly.

---

### Run 150 - Documentation and Knowledge Management Tools

**Objective:** Create tools to maintain and organize documentation and knowledge base entries efficiently

**Done when:**
1. Create `_batch_save_run_insights` tool to save extracted insights to knowledge base
2. Create `_find_unused_files` tool to identify orphaned files
3. Create `_generate_docs` tool to generate comprehensive documentation from tools and projects
4. Create `_review_project_structure` tool to check alignment between PROJECT.md and directory structure
5. Create `_organize_repo` tool to automate repository cleanup and organization
6. Create `_cleanup_temp_files` tool to safely remove temporary files
7. Create `_check_tool_consistency` tool to verify tool integration
8. Test all tools and integrate into documentation workflow

**Not this project:**
- Building a content management system (CMS)
- Creating a custom documentation generation engine
- Developing a personal knowledge management system (PKM)
- Implementing a version control for documentation

**Completed:**
All 8 documentation and knowledge management tools are fully implemented in `agent/tools.py`:

1. **`_batch_save_run_insights`** - Saves extracted insights to knowledge base:
   - Takes insights data from `_extract_run_insights`
   - Auto-assigns types and generates tags based on content
   - Saves in structured format to knowledge base
   - Returns summary with counts and types

2. **`_find_unused_files`** - Identifies orphaned files:
   - Checks which files are referenced in documentation
   - Finds files that aren't in any documentation
   - Returns list of unused files with suggestions
   - Helps clean up repository

3. **`_generate_docs`** - Generates comprehensive documentation:
   - Creates documentation for all tools with descriptions
   - Includes all completed projects from PROJECT.md
   - Creates navigation structure for easy browsing
   - Outputs organized documentation

4. **`_review_project_structure`** - Checks PROJECT.md and directory alignment:
   - Reviews alignment between PROJECT.md and directory structure
   - Checks for consistency and completeness
   - Returns summary of alignment review
   - Helps maintain project organization

5. **`_organize_repo`** - Automates repository cleanup and organization:
   - Consolidates documentation files
   - Removes duplicates
   - Organizes by type
   - Updates PROJECT.md if structure changes
   - Supports dry-run mode

6. **`_cleanup_temp_files`** - Removes temporary files safely:
   - Removes .pyc, .pyo, __pycache__ directories
   - Removes other temporary files
   - Asks for confirmation before deletion
   - Returns summary of cleanup actions

7. **`_check_tool_consistency`** - Verifies tool integration:
   - Checks all tool methods exist
   - Validates tool signatures
   - Verifies accessibility through dispatch mechanism
   - Returns summary of consistency check results

8. **`_monitor_repository_health`** - Checks repository integrity and health:
   - Verifies git repository status
   - Checks for uncommitted changes
   - Validates tool system consistency
   - Reports health score

**Status:** Complete - all 8 documentation and knowledge management tools are fully implemented and working correctly.
