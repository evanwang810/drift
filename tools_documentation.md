# Tools Documentation

## Summary
- **Total unique tools with docstrings:** 58
- **Total method definitions:** 63 (includes 5 duplicates)
- **Tools in use:** 57 (excluding __init__ which is special)

## Categories

### File Operations (7 tools)
1. `_read` - Read a file
2. `_read_with_numbers` - Read a file with line numbers
3. `_read_lines` - Read a range of lines from a file (1-indexed, inclusive)
4. `_read_all` - Read a file entirely, ignoring the usual size limit
5. `_write` - Write a file, replacing it entirely. Pass the whole new contents
6. `_replace` - Replace the first occurrence of a string in a file
7. `_replace_all` - Replace all occurrences of a string in a file
8. `_delete` - Delete a file. Only git history undoes this

### Shell & System Operations (5 tools)
9. `_run` - Run a shell command in the repository root. Network is available
10. `_tree` - List files in a directory and its subdirectories as a tree
11. `_ls` - List files in a directory
12. `_validate_python` - Check if a Python file has syntax errors
13. `_validate_python_syntax` - Check if a Python file has syntax errors before running

### Search & Research (5 tools)
14. `_search` - Search the web for a query
15. `_search_wikipedia` - Search Wikipedia API and return results
16. `_grep` - Search for a pattern in files recursively
17. `_knowledge_aware_search` - Search knowledge base first, then fall back to web search
18. `_research_summary` - Summarize research from knowledge base entries

### GitHub Operations (5 tools)
19. `_gh_list_issues` - List open GitHub issues for this repository
20. `_gh_read_issue` - Read a GitHub issue with its comments
21. `_gh_comment_issue` - Comment on a GitHub issue
22. `_gh_close_issue` - Close a GitHub issue
23. `_gh_create_issue_from_project` - Create GitHub issues from PROJECT.md incomplete tasks and technical debt

### Knowledge Base Operations (9 tools)
24. `_knowledge_add` - Add an entry to the knowledge base
25. `_knowledge_list` - List all knowledge entries, optionally filtered by type
26. `_knowledge_search` - Search knowledge base by title, description, tags, or implementation
27. `_save_run_insights_to_knowledge` - Add insights from a run to the knowledge base
28. `_contextual_knowledge_query` - Query knowledge base based on current work context
29. `_generate_knowledge_report` - Generate knowledge-based reports and summaries
30. `_generate_by_type_summary` - Generate summary organized by entry type
31. `_generate_by_tag_summary` - Generate summary organized by tags
32. `_generate_by_source_summary` - Generate summary organized by source
33. `_generate_comprehensive_report` - Generate comprehensive report with all dimensions
34. `_extract_run_insights` - Extract insights from RUNS.md entries and identify key patterns
35. `_batch_save_run_insights` - Batch save extracted insights to the knowledge base

### Blog & Documentation (4 tools)
36. `_generate_blog_post` - Generate a full blog post with frontmatter from a title and content
37. `_create_blog_posts_from_runs` - Generate complete blog posts from RUNS.md entries with blog post links
38. `_runs_to_blog_candidates` - Scan RUNS.md and generate blog post candidates from entries with links
39. `_generate_docs` - Generate comprehensive documentation for all tools, projects, and workflows

### Repository Management (8 tools)
40. `_analyze_runs` - Analyze RUNS.md to summarize productivity and failures
41. `_check_tool_consistency` - Verify tools are properly integrated and callable
42. `_test_rollback_point` - Create and validate rollback points for safe experimentation
43. `_review_project_structure` - Check PROJECT.md and directory structure alignment
44. `_validate_git_status` - Warn about uncommitted changes before making significant changes
45. `_organize_repo` - Automate repository cleanup and organization
46. `_find_unused_files` - Identify unused or orphaned files
47. `_cleanup_temp_files` - Remove temporary files safely
48. `_backup_repository` - Create automated repository backups

### Health & Monitoring (5 tools)
49. `_monitor_repository_health` - Check repository integrity and health
50. `_summarize` - Replace everything you have done so far with a summary of it
51. `_stop` - End the run

### Memory Optimization (4 tools)
52. `_reduce_waking_memory` - Reduce token cost of waking message by implementing smart memory management
53. `_optimize_knowledge_base` - Optimize knowledge base memory by keeping only most relevant entries
54. `_create_memory_cache` - Implement caching for frequently accessed information
55. `_filter_completed_items` - Filter completed TODO items and projects from current context

### AI/Agent Research (2 tools)
56. `_research_recommendations` - Suggest whether to search web or use existing knowledge
57. `_similar_research` - Find similar past research before starting new searches

## Duplicate Tools
The following tools are defined twice in agent/tools.py:
- `_backup_repository` (lines 2564 and 3425)
- `_check_tool_consistency` (lines 1961 and 3589)
- `_monitor_repository_health` (lines 3096 and 3681)
- `_test_rollback_point` (lines 2033 and 3508)
- `_validate_git_status` (lines 2212 and 3815)

Note: These duplicates are not in use - the schema only exports unique tool names.
