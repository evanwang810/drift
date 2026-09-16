# Drift Agent Tools Inventory

Complete inventory of 64 tools available to the Drift Agent.

## Failed Tools

### Tools That Fail When Called

| Tool | Failure | Reason |
|------|---------|--------|
| `_read` | **Bad Arguments Error** | PROJECT.md documentation calls `_read(path, start, end)` but the tool signature is `_read(path: str)`. When PROJECT.md is read, it triggers this error. The tool itself works correctly when called with only `path` argument. |

**Note:** This failure only occurs when reading PROJECT.md, not when calling the tool directly. The tool works correctly with its documented signature.

## Usage Statistics

- **2026-09-13.md**: 730 total calls to 24 tools
- **2026-09-14.md**: 658 total calls to 35 tools
- **Combined**: 1,388 total calls across 42 unique tools

Most frequently used tools in order:
1. **run** (349 total calls: 137 + 212)
2. **read_lines** (265 total calls: 154 + 111)
3. **grep** (162 total calls: 79 + 83)
4. **read** (194 total calls: 118 + 76)
5. **replace** (143 total calls: 83 + 60)
6. **read_all** (31 total calls: 22 + 9)
7. **read_with_numbers** (27 total calls: 19 + 8)
8. **stop** (34 total calls: 19 + 15)
9. **ls** (19 total calls: 15 + 4)
10. **write** (10 total calls: 24 + 6)

## Tool List

### File Operations

| Tool | Description | Real Arguments | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|-----------|-----------|
| `_read` | Read a file | path: str | 118 | 76 |
| `_read_with_numbers` | Read file with line numbers | path: str | 19 | 8 |
| `_read_lines` | Read range of lines (1-indexed) | path: str, start: int, end: int | 154 | 111 |
| `_read_all` | Read entire file (ignore size limit) | path: str | 22 | 9 |
| `_write` | Write file, replacing entirely | path: str, content: str | 24 | 6 |
| `_replace` | Replace first occurrence of string | path: str, search: str, replace: str | 83 | 60 |
| `_replace_all` | Replace all occurrences of string | path: str, search: str, replace: str | 34 | 2 |
| `_delete` | Delete a file (git history undoes) | path: str | 1 | 0 |

### Shell Operations

| Tool | Description | Real Arguments | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|-----------|-----------|
| `_run` | Run shell command (network available) | command: str | 137 | 212 |
| `_ls` | List files in directory | path: str (default: ".") | 15 | 4 |
| `_tree` | List directory as tree structure | path: str, max_depth: int | 0 | 1 |
| `_grep` | Search for pattern recursively | pattern: str, path: str | 79 | 83 |

### Knowledge Management

| Tool | Description | Real Arguments | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|-----------|-----------|
| `_knowledge_add` | Add entry to knowledge base | title, description, type, tags, source, implementation, verification, impact | 0 | 7 |
| `_knowledge_list` | List knowledge entries | type_filter: str | 0 | 7 |
| `_knowledge_search` | Search knowledge base | query: str, type_filter: str | 0 | 2 |
| `_save_run_insights_to_knowledge` | Save run insights to knowledge | title, description, type, source, tags | 0 | 4 |
| `_extract_run_insights` | Extract insights from RUNS.md | - | 0 | 5 |
| `_batch_save_run_insights` | Batch save insights to knowledge | insights_data: str | 0 | 3 |
| `_contextual_knowledge_query` | Query knowledge with context | context: str, type_filter: str, max_results: int | 0 | 2 |
| `_generate_knowledge_report` | Generate knowledge-based reports | type_filter, summary_type | 0 | 3 |
| `_generate_by_type_summary` | Generate summary by type | entries: list | 0 | 3 |
| `_generate_by_tag_summary` | Generate summary by tag | entries: list | 0 | 3 |
| `_generate_by_source_summary` | Generate summary by source | entries: list | 0 | 3 |
| `_generate_comprehensive_report` | Generate comprehensive report | entries: list | 0 | 3 |
| `_optimize_knowledge_base` | Optimize knowledge base structure | - | 0 | 0 |
| `_create_memory_cache` | Create memory cache | - | 0 | 0 |
| `_reduce_waking_memory` | Reduce waking message token count | - | 0 | 0 |
| `_filter_completed_items` | Filter completed TODO items | - | 0 | 0 |

### Research Tools

| Tool | Description | Real Arguments | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|-----------|-----------|
| `_search` | Search web (DuckDuckGo + Wikipedia) | query: str | 0 | 0 |
| `_search_wikipedia` | Search Wikipedia API | query: str | 0 | 0 |
| `_knowledge_aware_search` | Search knowledge base, fall back to web | query, max_knowledge_results, max_web_results | 0 | 0 |
| `_research_summary` | Summarize research from knowledge | query: str, max_results: int | 0 | 0 |
| `_similar_research` | Find similar past research | query: str, max_results: int, similarity_threshold: float | 0 | 0 |
| `_research_recommendations` | Suggest web vs knowledge search | query: str, context: str, use_existing: bool | 0 | 0 |
| `_web_fetch` | Fetch content from URL | url: str, parse_html: bool | 1 | 0 |

### GitHub Integration

| Tool | Description | Real Arguments | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|-----------|-----------|
| `_gh_list_issues` | List open GitHub issues | state: str, per_page: int | 2 | 0 |
| `_gh_read_issue` | Read GitHub issue with comments | issue_number: int | 0 | 0 |
| `_gh_comment_issue` | Comment on GitHub issue | issue_number: int, comment: str | 0 | 0 |
| `_gh_close_issue` | Close GitHub issue | issue_number: int | 0 | 0 |
| `_gh_create_issue_from_project` | Create issue from PROJECT.md | labels: str | 0 | 0 |

### Documentation & Blog Tools

| Tool | Description | Real Arguments | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|-----------|-----------|
| `_runs_to_blog_candidates` | Extract blog post candidates from RUNS.md | - | 1 | 1 |
| `_generate_blog_post` | Generate blog post with frontmatter | title: str, content: str, date: str | 0 | 0 |
| `_create_blog_posts_from_runs` | Generate full blog posts from RUNS.md | - | 1 | 0 |
| `_generate_docs` | Generate comprehensive documentation | - | 0 | 2 |

### Repository Operations

| Tool | Description | Real Arguments | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|-----------|-----------|
| `_monitor_repository_health` | Check repository integrity and health | - | 0 | 2 |
| `_validate_git_status` | Verify git status and warn about changes | warn_uncommitted: bool | 1 | 2 |
| `_review_project_structure` | Check PROJECT.md alignment with directory | - | 0 | 2 |
| `_organize_repo` | Consolidate docs, remove duplicates | dry_run: bool | 0 | 0 |
| `_find_unused_files` | Identify orphaned files | search_in: str | 0 | 1 |
| `_cleanup_temp_files` | Remove .pyc, __pycache__, etc. | safe: bool | 0 | 0 |
| `_backup_repository` | Create automated repository backup | format: str, keep: int | 0 | 1 |
| `_check_tool_consistency` | Verify tools are properly integrated | - | 0 | 3 |
| `_validate_python` | Check Python file for syntax errors | path: str | 7 | 4 |
| `_validate_python_syntax` | Parse Python file with ast | path: str | 0 | 4 |

### Process Control

| Tool | Description | Real Arguments | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|-----------|-----------|
| `_stop` | End the run | note: str, memory: str | 19 | 15 |
| `_summarize` | Replace context with summary | summary: str | 5 | 6 |

## Tool Categories

### Category: File Operations (8 tools)
- Core file reading/writing and modification
- Most frequently used: `_read`, `_read_lines`, `_write`, `_replace`

### Category: Shell Operations (4 tools)
- Command execution and file searching
- Most frequently used: `_run`, `_grep`, `_ls`

### Category: Knowledge Management (16 tools)
- Add, search, and generate reports from knowledge base
- Least used: Only 20 total calls across 2 days

### Category: Research Tools (7 tools)
- Web search and research capabilities
- Note: `_search` was never called in journal files despite being available

### Category: GitHub Integration (5 tools)
- Create, read, comment, and close issues
- Require GH_TOKEN and git CLI
- Only 2 total calls across 2 days

### Category: Documentation & Blog (4 tools)
- Generate blog posts and documentation
- Blog tools: 2 total calls (both on 2026-09-13)

### Category: Repository Operations (8 tools)
- Repository maintenance and health checks
- Only 6 total calls across 2 days

### Category: Process Control (2 tools)
- End run and summarize context
- Most frequently used: `_stop` (34 calls total)

## Notes

- **Total tools**: 64 executable tools in `agent/tools.py` (including `__init__`)
- **Unique tools in journal**: 42 tools have been called across both days
- **Unused tools**: 22 tools exist but have never been called (e.g., `_analyze_runs`, `_research_summary`, `_similar_research`, `_research_recommendations`, `_batch_save_run_insights`, `_check_tool_consistency`, etc.)
- **Working tools**: 52 tools work correctly (2 with design issues: `_ls`/`_tree` path handling, `_search` rate-limited)
- **Never implemented despite TODO**: `wikipedia_search` in tools.py (but `_search_wikipedia` exists)
- **GitHub tools**: Require external configuration (GH_TOKEN, git CLI)
- **Rate-limited tools**: `_search` has rate limiting issues
- **Design issues**: `_ls` and `_tree` need better path handling
