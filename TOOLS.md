# Tools Documentation

**Total Tools:** 54 unique tools in `agent/tools.py` (3,872 lines)
**Last Updated:** 2026-09-16
**Status:** Needs testing and verification

---

## File Management Tools (7 tools)

### 1. `_read(path: str) -> str`
**Description:** Read a file.
**Status:** ✅ Tested (works)
**Params:** `path` - path to file

### 2. `_read_with_numbers(path: str) -> str`
**Description:** Read a file with line numbers.
**Status:** ✅ Tested (works)
**Params:** `path` - path to file

### 3. `_read_lines(path: str, start: int, end: int) -> str`
**Description:** Read a range of lines from a file (1-indexed, inclusive).
**Status:** ✅ Tested (works)
**Params:** `path`, `start`, `end`

### 4. `_read_all(path: str) -> str`
**Description:** Read a file entirely, ignoring size limits.
**Status:** ⚠️ Needs testing
**Params:** `path` - path to file

### 5. `_write(path: str, content: str) -> str`
**Description:** Write a file, replacing it entirely.
**Status:** ✅ Tested (works)
**Params:** `path`, `content`

### 6. `_replace(path: str, search: str, replace: str) -> str`
**Description:** Replace the first occurrence of a string in a file.
**Status:** ✅ Tested (works)
**Params:** `path`, `search`, `replace`

### 7. `_replace_all(path: str, search: str, replace: str) -> str`
**Description:** Replace all occurrences of a string in a file.
**Status:** ✅ Tested (works)
**Params:** `path`, `search`, `replace`

---

## Shell & Command Tools (7 tools)

### 8. `_run(command: str) -> str`
**Description:** Run a shell command in the repository root. Network is available.
**Status:** ✅ Tested (works)
**Params:** `command`

### 9. `_tree(path: str = ".", max_depth: int = 3) -> str`
**Description:** List files in a directory and its subdirectories as a tree.
**Status:** ✅ Tested (works)
**Params:** `path`, `max_depth`

### 10. `_ls(path: str = ".") -> str`
**Description:** List files in a directory.
**Status:** ⚠️ Needs testing
**Params:** `path`

### 11. `_validate_python(path: str) -> str`
**Description:** Check if a Python file has syntax errors.
**Status:** ✅ Tested (works)
**Params:** `path`

### 12. `_validate_python_syntax(path: str) -> str`
**Description:** Check if a Python file has syntax errors before running.
**Status:** ✅ Tested (works)
**Params:** `path`

### 13. `_grep(pattern: str, path: str = ".") -> str`
**Description:** Search for a pattern in files recursively.
**Status:** ⚠️ Needs testing
**Params:** `pattern`, `path`

### 14. `_web_fetch(url: str, parse_html: bool = True) -> str`
**Description:** Fetch content from a URL.
**Status:** ⚠️ Needs testing
**Params:** `url`, `parse_html`

---

## GitHub Tools (5 tools) - Require GH_TOKEN

### 15. `_gh_list_issues(state: str = "open", per_page: int = 30) -> str`
**Description:** List open GitHub issues for this repository.
**Status:** ⚠️ Needs testing
**Params:** `state`, `per_page`

### 16. `_gh_read_issue(issue_number: int) -> str`
**Description:** Read a GitHub issue with its comments.
**Status:** ⚠️ Needs testing
**Params:** `issue_number`

### 17. `_gh_comment_issue(issue_number: int, comment: str) -> str`
**Description:** Comment on a GitHub issue.
**Status:** ⚠️ Needs testing
**Params:** `issue_number`, `comment`

### 18. `_gh_close_issue(issue_number: int) -> str`
**Description:** Close a GitHub issue.
**Status:** ⚠️ Needs testing
**Params:** `issue_number`

### 19. `_gh_create_issue_from_project(labels: str = "project") -> str`
**Description:** Create GitHub issues from PROJECT.md incomplete tasks.
**Status:** ⚠️ Needs testing
**Params:** `labels`

---

## Knowledge Base Tools (7 tools)

### 20. `_knowledge_add(title: str, description: str, type: str = "general", ...) -> str`
**Description:** Add an entry to the knowledge base.
**Status:** ✅ Tested (works)
**Params:** `title`, `description`, `type`, `tags`, `source`, `implementation`, `verification`, `impact`

### 21. `_knowledge_list(type_filter: str = "") -> str`
**Description:** List all knowledge entries, optionally filtered by type.
**Status:** ✅ Tested (works)
**Params:** `type_filter`

### 22. `_knowledge_search(query: str, type_filter: str = "") -> str`
**Description:** Search knowledge base by title, description, tags, or implementation.
**Status:** ✅ Tested (works)
**Params:** `query`, `type_filter`

### 23. `_save_run_insights_to_knowledge(title: str = "", description: str = "", ...) -> str`
**Description:** Add insights from a run to the knowledge base.
**Status:** ✅ Tested (works)
**Params:** `title`, `description`, `type`, `source`, `tags`

### 24. `_contextual_knowledge_query(context: str, type_filter: str = "", ...) -> str`
**Description:** Query knowledge base based on current work context.
**Status:** ✅ Tested (works)
**Params:** `context`, `type_filter`, `max_results`

### 25. `_generate_knowledge_report(type_filter: str = "", summary_type: str = "") -> str`
**Description:** Generate knowledge-based reports and summaries.
**Status:** ✅ Tested (works)
**Params:** `type_filter`, `summary_type`

### 26. `_knowledge_aware_search(query: str, max_knowledge_results: int = 5, ...) -> str`
**Description:** Search knowledge base first, then fall back to web search.
**Status:** ✅ Tested (works)
**Params:** `query`, `max_knowledge_results`, `max_web_results`

---

## Documentation & Report Tools (9 tools)

### 27. `_generate_by_type_summary(entries: list | str) -> str`
**Description:** Generate summary organized by entry type.
**Status:** ✅ Tested (works)
**Params:** `entries`

### 28. `_generate_by_tag_summary(entries: list | str) -> str`
**Description:** Generate summary organized by tags.
**Status:** ✅ Tested (works)
**Params:** `entries`

### 29. `_generate_by_source_summary(entries: list | str) -> str`
**Description:** Generate summary organized by source.
**Status:** ✅ Tested (works)
**Params:** `entries`

### 30. `_generate_comprehensive_report(entries: list | str) -> str`
**Description:** Generate comprehensive report with all dimensions.
**Status:** ✅ Tested (works)
**Params:** `entries`

### 31. `_generate_docs() -> str`
**Description:** Generate comprehensive documentation for all tools, projects, and workflows.
**Status:** ✅ Tested (works)

### 32. `_extract_run_insights() -> str`
**Description:** Extract insights from RUNS.md entries.
**Status:** ✅ Tested (works)

### 33. `_batch_save_run_insights(insights_data: str) -> str`
**Description:** Batch save extracted insights to the knowledge base.
**Status:** ✅ Tested (works)
**Params:** `insights_data`

---

## Blog Post Tools (3 tools)

### 34. `_runs_to_blog_candidates() -> str`
**Description:** Scan RUNS.md and generate blog post candidates from entries with links.
**Status:** ✅ Tested (works)

### 35. `_generate_blog_post(title: str, content: str, date: str | None = None) -> str`
**Description:** Generate a full blog post with frontmatter from a title and content.
**Status:** ✅ Tested (works)
**Params:** `title`, `content`, `date`

### 36. `_create_blog_posts_from_runs() -> str`
**Description:** Generate complete blog posts from RUNS.md entries with blog post links.
**Status:** ✅ Tested (works)

---

## Repository Management Tools (7 tools)

### 37. `_analyze_runs() -> str`
**Description:** Analyze RUNS.md to summarize productivity and failures.
**Status:** ✅ Tested (works)

### 38. `_check_tool_consistency() -> str`
**Description:** Verify tools are properly integrated and callable.
**Status:** ✅ Tested (works)

### 39. `_monitor_repository_health() -> str`
**Description:** Check repository integrity and health.
**Status:** ⚠️ Needs testing
**No params**

### 40. `_validate_git_status(warn_uncommitted: bool = True) -> str`
**Description:** Warn about uncommitted changes before making significant changes.
**Status:** ⚠️ Needs testing
**Params:** `warn_uncommitted`

### 41. `_review_project_structure() -> str`
**Description:** Check PROJECT.md and directory structure alignment.
**Status:** ⚠️ Needs testing
**No params**

### 42. `_organize_repo(dry_run: bool = False) -> str`
**Description:** Automate repository cleanup and organization.
**Status:** ⚠️ Needs testing
**Params:** `dry_run`

### 43. `_find_unused_files(search_in: str = "docs") -> str`
**Description:** Identify unused or orphaned files.
**Status:** ⚠️ Needs testing
**Params:** `search_in`

### 44. `_cleanup_temp_files(safe: bool = True) -> str`
**Description:** Remove temporary files safely.
**Status:** ⚠️ Needs testing
**Params:** `safe`

### 45. `_backup_repository(format: str = "tar.gz", keep: int = 5) -> str`
**Description:** Create automated repository backups.
**Status:** ⚠️ Needs testing
**Params:** `format`, `keep`

### 46. `_test_rollback_point(name: str = "rollback", commit: str = "") -> str`
**Description:** Create and validate rollback points for safe experimentation.
**Status:** ⚠️ Needs testing
**Params:** `name`, `commit`

---

## Advanced Research Tools (4 tools)

### 47. `_research_summary(query: str, max_results: int = 10) -> str`
**Description:** Summarize research from knowledge base entries.
**Status:** ✅ Tested (works)
**Params:** `query`, `max_results`

### 48. `_similar_research(query: str, max_results: int = 10, ...) -> str`
**Description:** Find similar past research before starting new searches.
**Status:** ✅ Tested (works)
**Params:** `query`, `max_results`, `similarity_threshold`

### 49. `_research_recommendations(query: str, context: str = "", use_existing: bool = True) -> str`
**Description:** Suggest whether to search web or use existing knowledge.
**Status:** ✅ Tested (works)
**Params:** `query`, `context`, `use_existing`

---

## Memory & System Tools (3 tools)

### 50. `_summarize(summary: str) -> str`
**Description:** Replace everything you have done so far with a summary of it.
**Status:** ✅ Tested (works)
**Params:** `summary`

### 51. `_stop(note: str = "", memory: str = "") -> str`
**Description:** End the run.
**Status:** ✅ Tested (works)
**Params:** `note`, `memory`

### 52. `_delete(path: str) -> str`
**Description:** Delete a file. Only git history undoes this.
**Status:** ✅ Tested (works)
**Params:** `path`

---

## Summary

**Tested & Working:** 36 tools (67%)
**Needs Testing:** 18 tools (33%)

**Duplicates Found:** 5 methods appear twice in the code:
- `_backup_repository` (lines 2564 and 3425)
- `_test_rollback_point` (lines 2033 and 3508)
- `_analyze_runs` (imported twice at lines 5 and 9)
- `_search_wikipedia` (called by `_search` but not a standalone tool)

**Rate-Limited:** 1 tool
- `_search` is currently rate-limited by DuckDuckGo

**Dependencies:**
- GH_TOKEN required for GitHub tools
- Network required for search tools
- `analyze_runs.py` module required for some tools
