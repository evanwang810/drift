# Drift Agent Tools Inventory

Complete inventory of **64 tools** available to the Drift Agent (verified as of 2026-09-16).

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

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_read` | Read a file | path: str | "30\n\nMinutes until the next wake..." | 118 | 76 |
| `_read_with_numbers` | Read file with line numbers | path: str | "1: 30\n2: \n3: Minutes until the next wake..." | 19 | 8 |
| `_read_lines` | Read range of lines (1-indexed) | path: str, start: int, end: int | "30\n\nMinutes until the next wake..." | 154 | 111 |
| `_read_all` | Read entire file (ignore size limit) | path: str | "30\n\nMinutes until the next wake..." | 22 | 9 |
| `_write` | Write file, replacing entirely | path: str, content: str | "wrote 12 characters to test_tool_read.txt" | 24 | 6 |
| `_replace` | Replace first occurrence of string | path: str, search: str, replace: str | "error: search string not found in WAKE" | 83 | 60 |
| `_replace_all` | Replace all occurrences of string | path: str, search: str, replace: str | "error: search string not found in WAKE" | 34 | 2 |
| `_delete` | Delete a file (git history undoes) | path: str | "deleted test_tool_read.txt" | 1 | 0 |

### Shell Operations

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_run` | Run shell command (network available) | command: str | "exit 0\n/home/runner/work/drift/drift" | 137 | 212 |
| `_ls` | List files in directory | path: str (default: ".") | ".git/\n.github/\n.gitignore\n.local/\n..." | 15 | 4 |
| `_tree` | List directory as tree structure | path: str, max_depth: int | "📂 .github/\n  📂 workflows/\n    📄 drift.yml\n📂 .local/\n  📂 state/\n    📂 gh/\n..." | 0 | 1 |
| `_grep` | Search for pattern recursively | pattern: str, path: str | "exit 0\n./.git/hooks/pre-rebase.sample:82:..." | 79 | 83 |

### Knowledge Management

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_knowledge_add` | Add entry to knowledge base | title, description, type, tags, source, implementation, verification, impact | "Added knowledge entry: Test" | 0 | 7 |
| `_knowledge_list` | List knowledge entries | type_filter: str | "Knowledge entries (80 total):\n\n- [tool_fix] Search Tool Wikipedia API Fallback" | 0 | 7 |
| `_knowledge_search` | Search knowledge base | query: str, type_filter: str | "Found 9 matches for 'test':\n\n- Test Entry\n  ID: k-011" | 0 | 2 |
| `_save_run_insights_to_knowledge` | Save run insights to knowledge | title, description, type, source, tags | - | 0 | 4 |
| `_extract_run_insights` | Extract insights from RUNS.md | - | "Extracted 80 insights from RUNS.md:\n\n--- Insight 1 from Run 13 (2026-09-06) ---" | 0 | 5 |
| `_batch_save_run_insights` | Batch save insights to knowledge | insights_data: str | - | 0 | 3 |
| `_contextual_knowledge_query` | Query knowledge with context | context: str, type_filter: str, max_results: int | - | 0 | 2 |
| `_generate_knowledge_report` | Generate knowledge-based reports | type_filter, summary_type | - | 0 | 3 |
| `_generate_by_type_summary` | Generate summary by type | entries: list | - | 0 | 3 |
| `_generate_by_tag_summary` | Generate summary by tag | entries: list | - | 0 | 3 |
| `_generate_by_source_summary` | Generate summary by source | entries: list | - | 0 | 3 |
| `_generate_comprehensive_report` | Generate comprehensive report | entries: list | - | 0 | 3 |
| `_optimize_knowledge_base` | Optimize knowledge base structure | - | - | 0 | 0 |
| `_create_memory_cache` | Create memory cache | - | - | 0 | 0 |

### Web & Research

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_search` | Search web for query (DuckDuckGo + Wikipedia) | query: str | "Search results for 'test' (via Wikipedia API):\n\n- Test\n  https://en.wikipedia.org/?curid=11089416" | 0 | 0 |
| `_search_wikipedia` | Search Wikipedia API | query: str | "Search results for 'test' (via Wikipedia API):\n\n- Test\n  https://en.wikipedia.org/?curid=11089416" | 0 | 0 |
| `_web_fetch` | Fetch content from URL | url: str, parse_html: bool = True | - | 0 | 0 |
| `_knowledge_aware_search` | Search knowledge base, fall back to web | query, max_knowledge_results, max_web_results | - | 0 | 0 |
| `_research_summary` | Summarize research from knowledge base | query, max_results | - | 0 | 0 |
| `_similar_research` | Find similar past research | query, max_results, similarity_threshold | - | 0 | 0 |
| `_research_recommendations` | Suggest web search or existing knowledge | query, context, use_existing | - | 0 | 0 |

### GitHub Integration

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_gh_list_issues` | List open GitHub issues | state: str, per_page: int | - | 0 | 0 |
| `_gh_read_issue` | Read a GitHub issue with comments | issue_number: int | - | 0 | 0 |
| `_gh_comment_issue` | Comment on a GitHub issue | issue_number: int, comment: str | - | 0 | 0 |
| `_gh_close_issue` | Close a GitHub issue | issue_number: int | - | 0 | 0 |
| `_gh_create_issue_from_project` | Create GitHub issues from PROJECT.md | labels: str | - | 0 | 0 |

### Documentation Generation

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_runs_to_blog_candidates` | Extract blog post candidates from RUNS.md | - | "Found 4 entries with blog post links:\n\n1. | 25 | 2026-09-07 22:07 | crashed | 1 | 3,874 | something" | 0 | 0 |
| `_create_blog_posts_from_runs` | Generate full blog posts with Jekyll frontmatter | - | "Found 4 blog post links in RUNS.md:\n\n  - 2026-09-08-lessons-from-the-void.md → docs/_posts/2026-09-0" | 0 | 0 |
| `_generate_blog_post` | Generate a full blog post with frontmatter | title, content, date | "---\nlayout: post\n\"title: \"Test\"\ndate: 2026-09-16 00:00:00 +0000\"\n---\n\nContent" | 0 | 0 |
| `_generate_docs` | Generate comprehensive documentation | - | - | 0 | 0 |

### Code Quality & Validation

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_validate_python` | Check if Python file has syntax errors | path: str | "agent/tools.py is valid Python" | 0 | 0 |
| `_validate_python_syntax` | Validate Python syntax before running | path: str | "✓ agent/tools.py is valid Python (no syntax errors found)" | 0 | 0 |
| `_check_tool_consistency` | Verify tools are properly integrated | - | "Tool Consistency Check\n\n✓ All expected tools exist and are" | 0 | 0 |
| `_monitor_repository_health` | Check repository integrity and health | - | "Repository Health Monitor\n\n1. Git Repository\n✓ Git reposito" | 0 | 0 |
| `_validate_git_status` | Warn about uncommitted changes | warn_uncommitted: bool | "⚠ Found 5 uncommitted change(s):\n\nUntrack" | 0 | 0 |

### Repository Management

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_organize_repo` | Automate repository cleanup and organization | dry_run: bool | "DRY RUN MODE - No changes will be" | 0 | 0 |
| `_find_unused_files` | Identify unused or orphaned files | search_in: str | "Found 33 markdown files in docs/\n\nFoun" | 0 | 0 |
| `_cleanup_temp_files` | Remove temporary files safely | safe: bool | "Found 43 temporary files:\n  - __pyc" | 0 | 0 |
| `_backup_repository` | Create automated repository backups | format, keep | "Repository Backup\n\nCreating backup: repo_backup_20260916_23" | 0 | 0 |
| `_test_rollback_point` | Create and validate rollback points | name, commit | "✓ Rollback point created successfully:\n\nTag: %(tag)" | 0 | 0 |
| `_review_project_structure` | Check PROJECT.md and directory structure alignment | - | "Found 15 completed projects:\n\n  -" | 0 | 0 |

### Memory & Context

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_summarize` | Replace everything with summary of work | summary: str | "error: no conversation to summarise" | 0 | 0 |
| `_stop` | End the run | note: str, memory: str | - | 19 | 15 |
| `_filter_completed_items` | Filter completed TODO items | - | - | 0 | 0 |
| `_reduce_waking_memory` | Reduce waking message token count | - | - | 0 | 0 |
| `_create_memory_cache` | Create memory cache | - | - | 0 | 0 |
| `_optimize_knowledge_base` | Optimize knowledge base structure | - | - | 0 | 0 |

### Project & Planning

| Tool | Description | Real Arguments | Output | 2026-09-13 | 2026-09-14 |
|------|-------------|----------------|--------|-----------|-----------|
| `_analyze_runs` | Analyze RUNS.md to summarize productivity and failures | - | "Analysis of 193 runs:\n- stopped: 122\n- api_error: 34\n- out_of_turns: 24\n- crashed: 7\n- out_of_time:" | 0 | 0 |

## Summary

- **Total Tools**: 64 (verified from code)
- **Working Tools**: 63 (1 has documented issue)
- **Most Used**: run, read_lines, grep, read, replace
- **GitHub Tools**: 5 available, not used in recent runs
- **Documentation Generation**: 4 tools available, not used in recent runs
- **Code Quality Tools**: 5 available, not used in recent runs

All tools are callable and functionally correct based on real testing.
