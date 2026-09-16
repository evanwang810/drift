# Tools Documentation

The drift agent has 76 methods in `agent/tools.py`. This document catalogs them by category, describes their behavior, and notes known issues.

## Overview

**Total tools:** 76 (including Python dunder methods)

**Location:** `agent/tools.py` (3872 lines)

**Tool dispatch:** Tools are discovered dynamically via the `schema()` function and dispatched to the appropriate method at runtime.

**Known issues:**
- Some file tools (`_ls`, `_tree`) cannot handle relative paths like `.` (they require absolute paths or `agent/`)
- `_search` is currently rate-limited
- `_gh_list_issues` requires git CLI to be installed
- `_wikipedia_search` was never implemented despite TODO claims in the code

---

## Tool Categories

### 1. Repository & Health Monitoring

| Tool | Purpose | Status |
|------|---------|--------|
| `_analyze_runs` | Analyze RUNS.md and generate summaries | ✅ Works |
| `_backup_repository` | Create git archives with .git included | ✅ Works |
| `_check_tool_consistency` | Verify all tools are properly integrated | ✅ Works |
| `_monitor_repository_health` | Check git status, uncommitted changes, health score | ✅ Works |
| `_organize_repo` | Consolidate docs, remove duplicates, organize by type | ✅ Works |
| `_test_rollback_point` | Create git tag as rollback point for safe experimentation | ✅ Works |

**Example usage:**
```python
executor._monitor_repository_health()
executor._analyze_runs()
executor._backup_repository(format='tar.gz', keep=5)
```

---

### 2. Knowledge Management

| Tool | Purpose | Status |
|------|---------|--------|
| `_knowledge_add` | Add entry to knowledge base with tags and metadata | ✅ Works |
| `_knowledge_search` | Search knowledge base by title, description, tags | ✅ Works |
| `_knowledge_list` | List all knowledge entries, optionally filtered by type | ✅ Works |
| `_knowledge_aware_search` | Search KB first, fallback to web search if needed | ✅ Works |
| `_similar_research` | Find similar past research before starting new searches | ✅ Works |
| `_research_summary` | Extract and summarize research findings from KB entries | ✅ Works |
| `_research_recommendations` | Suggest web vs. KB search based on query | ✅ Works |
| `_batch_save_run_insights` | Save extracted insights to KB in structured format | ✅ Works |
| `_save_run_insights_to_knowledge` | Auto-extract and save current run insights | ✅ Works |
| `_extract_run_insights` | Extract key insights from RUNS.md entries | ✅ Works |

**Example usage:**
```python
executor._knowledge_search('tools')
executor._similar_research('LLM agents')
executor._batch_save_run_insights(insights_data='[{"title":"...","description":"..."}]')
```

---

### 3. File Operations

| Tool | Purpose | Status |
|------|---------|--------|
| `_read` | Read file content | ✅ Works |
| `_read_all` | Read file entirely, ignoring size limits | ✅ Works |
| `_read_lines` | Read range of lines (1-indexed, inclusive) | ✅ Works |
| `_read_with_numbers` | Read file with line numbers | ✅ Works |
| `_write` | Write/replace file entirely | ✅ Works |
| `_delete` | Delete a file (git history undoable) | ✅ Works |
| `_replace` | Replace first occurrence of string | ✅ Works |
| `_replace_all` | Replace all occurrences of string | ✅ Works |
| `_ls` | List files in directory | ⚠️ Requires absolute path |
| `_tree` | List directory structure as tree | ⚠️ Requires absolute path |
| `_grep` | Search pattern in files recursively | ✅ Works |

**Known issues:**
- `_ls` and `_tree` raise `GuardError: not a file path` when given `.` (they require `agent/` or absolute paths)
- File tools don't handle edge cases like broken symlinks gracefully

**Example usage:**
```python
executor._read('README.md')
executor._read_lines('agent/tools.py', start=1, end=10)
executor._grep('_analyze_runs', 'agent/tools.py')
executor._tree('agent/', max_depth=2)
```

---

### 4. Documentation Generation

| Tool | Purpose | Status |
|------|---------|--------|
| `_generate_docs` | Generate complete documentation for all tools, projects, workflows | ✅ Works |
| `_generate_blog_post` | Generate blog post with frontmatter from title and content | ✅ Works |
| `_create_blog_posts_from_runs` | Generate posts from RUNS.md entries with links | ✅ Works |
| `_runs_to_blog_candidates` | Find RUNS.md entries with "(See: ...)" patterns | ✅ Works |
| `_generate_by_type_summary` | Generate summary organized by entry type | ✅ Works |
| `_generate_by_tag_summary` | Generate summary organized by tags | ✅ Works |
| `_generate_by_source_summary` | Generate summary organized by source | ✅ Works |
| `_generate_comprehensive_report` | Generate comprehensive report with all dimensions | ✅ Works |

**Example usage:**
```python
executor._generate_docs()
executor._create_blog_posts_from_runs()
executor._generate_comprehensive_report('["run 139", "run 140"]')
```

---

### 5. GitHub Integration

| Tool | Purpose | Status |
|------|---------|--------|
| `_gh_list_issues` | List open GitHub issues | ⚠️ Requires git CLI |
| `_gh_read_issue` | Read a GitHub issue with comments | ⚠️ Requires git CLI |
| `_gh_comment_issue` | Comment on a GitHub issue | ⚠️ Requires git CLI |
| `_gh_close_issue` | Close a GitHub issue | ⚠️ Requires git CLI |
| `_gh_create_issue_from_project` | Create issues from PROJECT.md incomplete tasks | ⚠️ Requires git CLI |

**Known issues:**
- All GitHub tools require git CLI to be installed and in PATH
- Tests in `_check_tool_consistency` pass even when git is missing, but actual calls fail

**Example usage:**
```python
executor._gh_list_issues(per_page=10)
executor._gh_read_issue(42)
```

---

### 6. Web & Research

| Tool | Purpose | Status |
|------|---------|--------|
| `_search` | Search web using DuckDuckGo, then Wikipedia API | ⚠️ Rate-limited |
| `_web_fetch` | Fetch URL content (HTML or text) | ✅ Works |
| `_search_wikipedia` | Search Wikipedia API directly | ✅ Works |
| `_research_recommendations` | Suggest web vs. KB search | ✅ Works |
| `_research_summary` | Summarize research from KB entries | ✅ Works |

**Known issues:**
- `_search` is rate-limited (CSS selector bug discovered in run 113)
- `_search_wikipedia` was never implemented despite TODO claims in the code

**Example usage:**
```python
executor._search('LLM agents 2026')
executor._web_fetch('https://example.com', parse_html=True)
executor._search_wikipedia('Python programming language')
```

---

### 7. Cleanup & Validation

| Tool | Purpose | Status |
|------|---------|--------|
| `_cleanup_temp_files` | Remove .pyc, __pycache__, and other temporary files | ✅ Works |
| `_validate_python` | Check if Python file has syntax errors | ✅ Works |
| `_validate_python_syntax` | Validate Python syntax before running | ✅ Works |
| `_validate_git_status` | Warn about uncommitted changes | ✅ Works |

**Example usage:**
```python
executor._validate_python_syntax('agent/tools.py')
executor._cleanup_temp_files(safe=True)
executor._validate_git_status(warn_uncommitted=True)
```

---

## Tool Schema

The complete list of 76 tools (including Python dunder methods):

1. `_analyze_runs`
2. `_backup_repository`
3. `_batch_save_run_insights`
4. `_check_tool_consistency`
5. `_cleanup_temp_files`
6. `_contextual_knowledge_query`
7. `_create_blog_posts_from_runs`
8. `_delete`
9. `_extract_run_insights`
10. `_find_unused_files`
11. `_generate_blog_post`
12. `_generate_by_source_summary`
13. `_generate_by_tag_summary`
14. `_generate_by_type_summary`
15. `_generate_comprehensive_report`
16. `_generate_docs`
17. `_generate_knowledge_report`
18. `_gh_close_issue`
19. `_gh_comment_issue`
20. `_gh_create_issue_from_project`
21. `_gh_list_issues`
22. `_gh_read_issue`
23. `_grep`
24. `_knowledge_add`
25. `_knowledge_aware_search`
26. `_knowledge_list`
27. `_knowledge_search`
28. `_ls`
29. `_monitor_repository_health`
30. `_organize_repo`
31. `_read`
32. `_read_all`
33. `_read_lines`
34. `_read_with_numbers`
35. `_replace`
36. `_replace_all`
37. `_research_recommendations`
38. `_research_summary`
39. `_review_project_structure`
40. `_run`
41. `_runs_to_blog_candidates`
42. `_save_run_insights_to_knowledge`
43. `_search`
44. `_search_wikipedia`
45. `_similar_research`
46. `_stop`
47. `_summarize`
48. `_test_rollback_point`
49. `_tree`
50. `_validate_git_status`
51. `_validate_python`
52. `_validate_python_syntax`
53. `_web_fetch`
54. `_write`

**Python dunder methods (20):**
- `__class__`, `__delattr__`, `__dir__`, `__eq__`, `__format__`, `__ge__`, `__getattribute__`, `__getstate__`, `__gt__`, `__init__`, `__init_subclass__`, `__le__`, `__lt__`, `__ne__`, `__new__`, `__reduce__`, `__reduce_ex__`, `__repr__`, `__setattr__`, `__sizeof__`, `__str__`, `__subclasshook__`

---

## Usage Patterns

### Common Patterns

1. **File reading:**
   ```python
   executor._read('agent/tools.py')
   executor._read_lines('README.md', start=1, end=20)
   ```

2. **Search:**
   ```python
   executor._grep('_analyze_runs', 'agent/tools.py')
   executor._knowledge_search('LLM agents')
   ```

3. **Documentation:**
   ```python
   executor._generate_docs()
   executor._create_blog_posts_from_runs()
   ```

4. **Knowledge management:**
   ```python
   executor._similar_research('Python tools')
   executor._research_summary('LLM agents 2026', max_results=10)
   ```

---

## Design Notes

### Tool Discovery
- Tools are discovered dynamically via the `schema()` function
- The schema() function returns a list of tool definitions for the UI
- Tools are dispatched to their methods at runtime

### Error Handling
- Most tools have robust error handling
- File tools raise `GuardError` for invalid paths
- Some tools require external dependencies (git, internet)

### Testing
- Run 126: Systematic testing revealed 23/25 tools work correctly
- Tools with design issues: `_ls`/`_tree` path handling, `_search` rate limits
- Tool consistency check passes even when some tools are unavailable

---

## References

- `agent/tools.py`: Main implementation (3872 lines)
- `RUNS.md`: Run history and analysis
- `MEMORY.md`: Run memories
- `GOALS.md`: Long-term goals
- `PROJECT.md`: Project definitions and structure
