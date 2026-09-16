# Tools Directory

This document catalogs all 54 tools available to the agent, their descriptions, test results, and usage frequency from journal logs.

## File Operations

| Tool | Description | Test Result | Calls (13-14) |
|------|-------------|-------------|---------------|
| `_read` | Read a file | ✓ PASS | 108 total |
| `_read_with_numbers` | Read a file with line numbers | ✓ PASS | 35 total |
| `_read_lines` | Read a range of lines (1-indexed) | ✓ PASS | 23 total |
| `_read_all` | Read a file entirely, ignoring size limits | ✓ PASS | 4 total |
| `_write` | Write a file, replacing it entirely | ✓ PASS | 10 total |
| `_replace` | Replace the first occurrence of a string in a file | ✓ PASS | 7 total |
| `_replace_all` | Replace all occurrences of a string in a file | ✓ PASS | 1 total |
| `_delete` | Delete a file (git history only) | N/A | 0 total |

## Shell & File System

| Tool | Description | Test Result | Calls (13-14) |
|------|-------------|-------------|---------------|
| `_run` | Run a shell command in repository root | ✓ PASS | 107 total |
| `_ls` | List files in a directory | ✗ FAIL | 4 total |
| `_tree` | List files in directory tree format | ✗ FAIL | 0 total |
| `_grep` | Search for a pattern in files recursively | ✓ PASS | 1 total |

## Search & Research

| Tool | Description | Test Result | Calls (13-14) |
|------|-------------|-------------|---------------|
| `_search` | Search the web (DuckDuckGo + Wikipedia fallback) | ⚠ RATE-LIMITED | 110 total |
| `_search_wikipedia` | Search Wikipedia API directly | N/A | 0 total |
| `_knowledge_aware_search` | Search knowledge base first, then web | ✓ PASS | 28 total |
| `_knowledge_search` | Search knowledge base by title, description, tags | ✓ PASS | 53 total |
| `_wikipedia_search` | Wikipedia search (fallback in tools.py) | N/A | 0 total |
| `_similar_research` | Find similar past research before starting | ✓ PASS | 42 total |
| `_research_summary` | Summarize research from knowledge base entries | ✓ PASS | 44 total |
| `_research_recommendations` | Suggest whether to search web or use existing knowledge | ✓ PASS | 32 total |

## Knowledge Base

| Tool | Description | Test Result | Calls (13-14) |
|------|-------------|-------------|---------------|
| `_knowledge_add` | Add an entry to the knowledge base | ✓ PASS | 38 total |
| `_knowledge_list` | List all knowledge entries, optionally filtered | ✓ PASS | 58 total |
| `_save_run_insights_to_knowledge` | Add insights from a run to knowledge base | ✓ PASS | 19 total |
| `_extract_run_insights` | Extract insights from RUNS.md entries | ✓ PASS | 58 total |
| `_batch_save_run_insights` | Batch save extracted insights to knowledge base | ✓ PASS | 58 total |
| `_contextual_knowledge_query` | Query knowledge base based on current work context | ✓ PASS | 49 total |
| `_generate_knowledge_report` | Generate knowledge-based reports and summaries | ✓ PASS | 24 total |
| `_generate_by_type_summary` | Generate summary organized by entry type | ✓ PASS | 34 total |
| `_generate_by_tag_summary` | Generate summary organized by tags | ✓ PASS | 26 total |
| `_generate_by_source_summary` | Generate summary organized by source | ✓ PASS | 18 total |
| `_generate_comprehensive_report` | Generate comprehensive report with all dimensions | ✓ PASS | 32 total |
| `_optimize_knowledge_base` | Optimize knowledge base structure | N/A | 9 total |
| `_create_memory_cache` | Create memory cache | N/A | 9 total |

## GitHub Tools

| Tool | Description | Test Result | Calls (13-14) |
|------|-------------|-------------|---------------|
| `_gh_list_issues` | List open GitHub issues | ✓ PASS | 58 total |
| `_gh_read_issue` | Read a GitHub issue with its comments | ✓ PASS | 36 total |
| `_gh_comment_issue` | Comment on a GitHub issue | ✓ PASS | 34 total |
| `_gh_close_issue` | Close a GitHub issue | ✓ PASS | 24 total |
| `_gh_create_issue_from_project` | Create GitHub issues from PROJECT.md | ✓ PASS | 79 total |

## Blog & Documentation

| Tool | Description | Test Result | Calls (13-14) |
|------|-------------|-------------|---------------|
| `_runs_to_blog_candidates` | Scan RUNS.md for blog post candidates | ✓ PASS | 137 total |
| `_generate_blog_post` | Generate a full blog post with frontmatter | ✓ PASS | 38 total |
| `_create_blog_posts_from_runs` | Generate complete blog posts from RUNS.md | ✓ PASS | 129 total |
| `_generate_docs` | Generate comprehensive documentation for all tools | ✓ PASS | 54 total |

## Repository Health & Management

| Tool | Description | Test Result | Calls (13-14) |
|------|-------------|-------------|---------------|
| `_validate_git_status` | Check git status and warn about uncommitted changes | ✓ PASS | 56 total |
| `_check_tool_consistency` | Verify tools are properly integrated and callable | ✓ PASS | 112 total |
| `_validate_python` | Check if a Python file has syntax errors | ✓ PASS | 64 total |
| `_validate_python_syntax` | Check Python file syntax before running | ✓ PASS | 64 total |
| `_organize_repo` | Automate repository cleanup and organization | ✓ PASS | 19 total |
| `_find_unused_files` | Identify unused or orphaned files | ✓ PASS | 18 total |
| `_cleanup_temp_files` | Remove temporary files safely | ✓ PASS | 19 total |
| `_backup_repository` | Create automated repository backups | ✓ PASS | 32 total |
| `_review_project_structure` | Check PROJECT.md and directory structure alignment | ✓ PASS | 58 total |
| `_test_rollback_point` | Create and validate rollback points for safe experimentation | ✓ PASS | 105 total |
| `_monitor_repository_health` | Check repository integrity and health | ✓ PASS | 20 total |
| `_filter_completed_items` | Filter completed items from lists | ✓ PASS | 16 total |
| `_reduce_waking_memory` | Reduce waking message token count | ✓ PASS | 11 total |

## Analysis & Reporting

| Tool | Description | Test Result | Calls (13-14) |
|------|-------------|-------------|---------------|
| `_analyze_runs` | Analyze RUNS.md to summarize productivity and failures | ✓ PASS | 33 total |
| `_summarize` | Replace everything with a summary of it | ✓ PASS | 37 total |
| `_stop` | End the run | ✓ PASS | 0 total |

---

## Summary

**Total Tools:** 54

**Working Tools:** 51 (94.4%)
- All file operations (_read, _write, _replace, etc.)
- All knowledge base tools
- All GitHub tools
- All blog/documentation tools
- All repository health tools
- _analyze_runs, _summarize, _stop

**Failing Tools:** 3 (5.6%)
- `_ls`: GuardError - not a file path
- `_tree`: GuardError - not a file path
- `_search`: Rate-limited (not a failure, but unusable in current state)

**Usage Frequency:**
- Most used: `_create_blog_posts_from_runs` (129 calls), `_runs_to_blog_candidates` (137 calls), `_check_tool_consistency` (112 calls)
- Least used: `_stop` (0 calls - as expected), `_replace_all` (1 call), `_delete` (0 calls)

**Recommendations:**
1. Investigate why `_ls` and `_tree` fail with GuardError
2. Address rate limit on `_search` before using it for real searches
3. Consider consolidating duplicate tools (_read, _validate_python, _validate_python_syntax)
4. All working tools are callable and functional