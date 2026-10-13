# Tools Catalog

This file documents all available tools in the repository. Tools are functions in `agent/tools.py`. The public tools (`dispatch`, `schema`, `clip`) are callable directly; private tools (`_toolname`) are internal helpers.

## File Operations

**`read`** - Read a file. Returns content clipped to a reasonable length.

**`read_with_numbers`** - Read a file with line numbers for easier navigation.

**`read_lines`** - Read a specific range of lines from a file (1-indexed, inclusive).

**`read_all`** - Read a file entirely, ignoring size limits.

**`write`** - Write a file, replacing it entirely. Pass the whole new contents.

**`replace`** - Replace the first occurrence of a string in a file.

**`replace_all`** - Replace all occurrences of a string in a file.

**`delete`** - Delete a file. Only git history undoes this.

**`ls`** - List files in a directory.

**`tree`** - List files in a directory and subdirectories as a tree structure.

**`grep`** - Search for a pattern in files recursively.

## Shell Operations

**`run`** - Run a shell command in the repository root. Network is available.

## Process Control

**`stop`** - End the run with an optional note and memory for the next run.

**`summarize`** - Replace everything you have done so far with a summary of it.

**`validate_git_status`** - Warn about uncommitted changes before making significant changes.

## Knowledge Management

**`knowledge_add`** - Add an entry to the knowledge base with title, description, type, tags, source, implementation, verification, and impact.

**`knowledge_list`** - List all knowledge entries, optionally filtered by type.

**`knowledge_search`** - Search knowledge base by title, description, tags, or implementation.

**`knowledge_aware_search`** - Search knowledge base first, then fall back to web search using DuckDuckGo and Wikipedia API.

**`generate_knowledge_report`** - Generate knowledge-based reports and summaries, optionally filtered by type and summarized by different dimensions.

**`similar_research`** - Find similar past research before starting new searches based on context, tags, and implementation details.

**`research_summary`** - Summarize research from knowledge base entries with structured findings and source attribution.

**`research_recommendations`** - Suggest whether to search web or use existing knowledge based on query analysis.

## GitHub Integration

**`gh_list_issues`** - List open GitHub issues for this repository.

**`gh_read_issue`** - Read a GitHub issue with its comments.

**`gh_comment_issue`** - Comment on a GitHub issue.

**`gh_close_issue`** - Close a GitHub issue.

**`gh_create_issue_from_project`** - Create GitHub issues from PROJECT.md incomplete tasks and technical debt.

## Blog and Documentation Generation

**`generate_blog_post`** - Generate a full blog post with frontmatter from a title and content.

**`create_blog_posts_from_runs`** - Generate complete blog posts from RUNS.md entries with blog post links.

**`runs_to_blog_candidates`** - Scan RUNS.md and generate blog post candidates from entries with links.

**`generate_docs`** - Generate comprehensive documentation for all tools, projects, and workflows.

## Web Operations

**`web_fetch`** - Fetch content from a URL. If parse_html is True, it returns the text content of the page.

## Analysis and Maintenance

**`analyze_runs`** - Analyze RUNS.md to summarize productivity and failures.

**`validate_python`** - Check if a Python file has syntax errors.

**`validate_python_syntax`** - Check if a Python file has syntax errors before running.

**`check_tool_consistency`** - Verify tools are properly integrated and callable.

**`test_rollback_point`** - Create and validate rollback points for safe experimentation.

**`review_project_structure`** - Check PROJECT.md and directory structure alignment.

**`monitor_repository_health`** - Check repository integrity and health.

**`organize_repo`** - Automate repository cleanup and organization.

**`find_unused_files`** - Identify unused or orphaned files.

**`cleanup_temp_files`** - Remove temporary files safely.

## Internal Functions (Not Public Tools)

These are private helper functions in `agent/tools.py` that are not callable directly:

**`_dispatch_`** - Route tool calls to the appropriate method.

**`_analyze_runs_`** - Internal wrapper for analyze_runs function.

**`_contextual_knowledge_query_`** - Query knowledge base based on current work context.

**`_cleanup_temp_files_`** - Remove temporary files safely.

**`_create_blog_posts_from_runs_`** - Generate complete blog posts from RUNS.md entries.

**`_extract_run_insights_`** - Extract insights from RUNS.md entries.

**`_find_unused_files_`** - Identify unused or orphaned files.

**`_generate_blog_post_`** - Generate a full blog post with frontmatter.

**`_generate_by_source_summary_`** - Generate summary organized by source.

**`_generate_by_tag_summary_`** - Generate summary organized by tags.

**`_generate_by_type_summary_`** - Generate summary organized by entry type.

**`_generate_comprehensive_report_`** - Generate comprehensive report with all dimensions.

**`_generate_docs_`** - Generate comprehensive documentation for all tools, projects, and workflows.

**`_generate_knowledge_report_`** - Generate knowledge-based reports and summaries.

**`_gh_close_issue_`** - Close a GitHub issue.

**`_gh_comment_issue_`** - Comment on a GitHub issue.

**`_gh_create_issue_from_project_`** - Create GitHub issues from PROJECT.md incomplete tasks.

**`_gh_list_issues_`** - List open GitHub issues for this repository.

**`_gh_read_issue_`** - Read a GitHub issue with its comments.

**`_grep_`** - Search for a pattern in files recursively.

**`_knowledge_add_`** - Add an entry to the knowledge base.

**`_knowledge_aware_search_`** - Search knowledge base first, then fall back to web search.

**`_knowledge_list_`** - List all knowledge entries, optionally filtered by type.

**`_knowledge_search_`** - Search knowledge base by title, description, tags, or implementation.

**`_ls_`** - List files in a directory.

**`_monitor_repository_health_`** - Check repository integrity and health.

**`_organize_repo_`** - Automate repository cleanup and organization.

**`_read_`** - Read a file.

**`_read_all_`** - Read a file entirely, ignoring the usual size limit.

**`_read_lines_`** - Read a range of lines from a file.

**`_read_with_numbers_`** - Read a file with line numbers.

**`_replace_`** - Replace the first occurrence of a string in a file.

**`_replace_all_`** - Replace all occurrences of a string in a file.

**`_research_recommendations_`** - Suggest whether to search web or use existing knowledge.

**`_research_summary_`** - Summarize research from knowledge base entries.

**`_review_project_structure_`** - Check PROJECT.md and directory structure alignment.

**`_run_`** - Run a shell command in the repository root.

**`_runs_to_blog_candidates_`** - Scan RUNS.md and generate blog post candidates.

**`_save_run_insights_to_knowledge_`** - Add insights from a run to the knowledge base.

**`_search_`** - Search the web for a query.

**`_search_wikipedia_`** - Search Wikipedia API and return results.

**`_similar_research_`** - Find similar past research before starting new searches.

**`_stop_`** - End the run.

**`_summarize_`** - Replace everything you have done so far with a summary.

**`_test_rollback_point_`** - Create and validate rollback points for safe experimentation.

**`_tree_`** - List files in a directory and its subdirectories as a tree.

**`_validate_git_status_`** - Warn about uncommitted changes before making significant changes.

**`_validate_python_`** - Check if a Python file has syntax errors.

**`_validate_python_syntax_`** - Check if a Python file has syntax errors before running.

**`_web_fetch_`** - Fetch content from a URL.

**`_write_`** - Write a file, replacing it entirely.

Total: 62 unique functions (59 private, 3 public)
