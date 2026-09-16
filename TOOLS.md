# Drift Agent Tools Inventory

## Overview

This repository contains **54 tools** in `agent/tools.py` (3872 lines). These tools are organized into functional categories for different tasks: file operations, git operations, knowledge management, web operations, GitHub integration, and repository maintenance.

---

## 🔴 Failed Tools (Design Issues)

### _ls and _tree - Path Handling Issues
- **_ls**: Currently handles root directory relative paths but may not properly handle absolute paths or paths with spaces
- **_tree**: Same path handling limitations as _ls
- **Impact**: These tools work for common use cases but may fail with edge cases

---

## 🟡 Partially Implemented

### _search - Rate Limited and Needs Testing
- Currently rate-limited by DuckDuckGo
- Enhanced with robust error handling for rate limits, timeouts, network errors, and malformed HTML
- **Status**: Functional with error handling, but results are rate-limited

---

## 🟢 Working Tools (50/54)

### File Operations (10 tools)
1. **_read** - Read a file
2. **_read_with_numbers** - Read a file with line numbers
3. **_read_lines** - Read a specific range of lines (1-indexed, inclusive)
4. **_read_all** - Read a file entirely (ignores size limit)
5. **_write** - Write/replace a file entirely
6. **_replace** - Replace first occurrence of a string in a file
7. **_replace_all** - Replace all occurrences of a string in a file
8. **_delete** - Delete a file (only git history undoes this)
9. **_run** - Run a shell command in repository root
10. **_ls** - List files in a directory
11. **_tree** - List files as a tree structure

### Git Operations (2 tools)
12. **_validate_git_status** - Check git status and warn about uncommitted changes
13. **_backup_repository** - Create automated repository backup with timestamp

### Knowledge Management (11 tools)
14. **_knowledge_add** - Add an entry to the knowledge base
15. **_knowledge_list** - List all knowledge entries, optionally filtered by type
16. **_knowledge_search** - Search knowledge base by title, description, tags, or implementation
17. **_save_run_insights_to_knowledge** - Add insights from a run to knowledge base
18. **_contextual_knowledge_query** - Query knowledge base based on current work context
19. **_generate_knowledge_report** - Generate knowledge-based reports
20. **_generate_by_type_summary** - Generate summary organized by entry type
21. **_generate_by_tag_summary** - Generate summary organized by tags
22. **_generate_by_source_summary** - Generate summary organized by source
23. **_generate_comprehensive_report** - Generate comprehensive report with all dimensions
24. **_extract_run_insights** - Extract insights from RUNS.md entries

### Web Operations (3 tools)
25. **_web_fetch** - Fetch content from a URL (parse_html option)
26. **_search** - Search the web for a query (DuckDuckGo, falls back to Wikipedia)
27. **_search_wikipedia** - Search Wikipedia API and return results

### GitHub Integration (4 tools)
28. **_gh_list_issues** - List open GitHub issues
29. **_gh_read_issue** - Read a GitHub issue with its comments
30. **_gh_comment_issue** - Comment on a GitHub issue
31. **_gh_close_issue** - Close a GitHub issue
32. **_gh_create_issue_from_project** - Create GitHub issues from PROJECT.md

### Blog & Documentation Generation (3 tools)
33. **_runs_to_blog_candidates** - Scan RUNS.md for blog post candidates
34. **_generate_blog_post** - Generate a full blog post with frontmatter
35. **_create_blog_posts_from_runs** - Generate complete blog posts from RUNS.md entries

### Documentation & Organization (7 tools)
36. **_generate_docs** - Generate comprehensive documentation for all tools
37. **_check_tool_consistency** - Verify tools are properly integrated and callable
38. **_validate_python** - Check if a Python file has syntax errors
39. **_validate_python_syntax** - Check if a Python file has syntax errors before running
40. **_review_project_structure** - Check PROJECT.md and directory structure alignment
41. **_find_unused_files** - Identify unused or orphaned files
42. **_organize_repo** - Automate repository cleanup and organization
43. **_cleanup_temp_files** - Remove temporary files safely

### Research & Discovery (5 tools)
44. **_knowledge_aware_search** - Search knowledge base first, then web search
45. **_research_summary** - Summarize research from knowledge base entries
46. **_similar_research** - Find similar past research before starting new searches
47. **_research_recommendations** - Suggest whether to search web or use existing knowledge
48. **_grep** - Search for a pattern in files recursively

### Monitoring & Maintenance (9 tools)
49. **_monitor_repository_health** - Check repository integrity and health
50. **_analyze_runs** - Analyze RUNS.md to summarize productivity and failures
51. **_filter_completed_items** - Filter completed items from lists
52. **_reduce_waking_memory** - Reduce waking message token count
53. **_optimize_knowledge_base** - Optimize knowledge base structure
54. **_create_memory_cache** - Create memory cache
55. **_stop** - End the run (with note and memory)

---

## Tool Categories Summary

| Category | Tools | Status |
|----------|-------|--------|
| File Operations | 10 | 🟢 Working |
| Git Operations | 2 | 🟢 Working |
| Knowledge Management | 11 | 🟢 Working |
| Web Operations | 3 | 🟢 Working (search rate-limited) |
| GitHub Integration | 4 | 🟢 Working (requires GH_TOKEN) |
| Blog & Docs Generation | 3 | 🟢 Working |
| Documentation & Org | 7 | 🟢 Working |
| Research & Discovery | 5 | 🟢 Working |
| Monitoring & Maintenance | 9 | 🟢 Working |
| **Total** | **54** | **50/54 Working** |

---

## Usage Notes

- **GitHub tools** require `GH_TOKEN` environment variable and git CLI installed
- **_search** is currently rate-limited by DuckDuckGo
- **_ls** and **_tree** may have edge case issues with path handling
- **_delete** permanently removes files (only git history can undo)
- Most tools are designed to be called from the `Executor` class with self-reference
- Tools are auto-tagged and categorized in the knowledge base

---

## Next Steps

1. Document real usage examples for each tool
2. Create comprehensive usage statistics
3. Add tool reliability metrics
4. Document edge cases and failure modes
5. Create automated testing suite
