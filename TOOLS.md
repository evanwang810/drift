# Drift Agent Tools Documentation

This document catalogues all tools available in the Drift Agent system, organized by category.

**Total unique tools: 62**
**Tools in schema: 54** (4 GitHub tools not exposed in schema)

---

## Core File Operations

| Tool | Purpose | Status |
|------|---------|--------|
| `_read` | Read a file's contents | ✅ Working |
| `_read_with_numbers` | Read a file with line numbers | ✅ Working |
| `_read_lines` | Read a range of lines (1-indexed) | ✅ Working |
| `_read_all` | Read entire file ignoring size limits | ✅ Working |
| `_write` | Write/replace a file entirely | ✅ Working |
| `_replace` | Replace first occurrence of a string in a file | ✅ Working |
| `_replace_all` | Replace all occurrences of a string in a file | ✅ Working |
| `_delete` | Delete a file (git history undoes) | ✅ Working |
| `_validate_python` | Check if a Python file has syntax errors | ✅ Working |
| `_validate_python_syntax` | Validate Python files before running | ✅ Working |

---

## Shell & System Operations

| Tool | Purpose | Status |
|------|---------|--------|
| `_run` | Run a shell command | ✅ Working |
| `_ls` | List files in a directory | ✅ Working |
| `_tree` | List directory structure as tree | ✅ Working |
| `_grep` | Search for pattern recursively | ✅ Working |
| `_monitor_repository_health` | Check repository integrity and health | ✅ Working |
| `_validate_git_status` | Verify git status and warn about uncommitted changes | ✅ Working |
| `_backup_repository` | Create automated repository backups (tar.gz, zip, tar) | ✅ Working |
| `_cleanup_temp_files` | Remove temporary files (.pyc, __pycache__) | ✅ Working |
| `_organize_repo` | Organize repository by type and consolidate docs | ✅ Working |

---

## Search & Research

| Tool | Purpose | Status |
|------|---------|--------|
| `_search` | Search web for query (DuckDuckGo + Wikipedia fallback) | ⚠️ Rate-limited |
| `_search_wikipedia` | Search Wikipedia API | ⚠️ Not fully tested |
| `_web_fetch` | Fetch URL content (HTML or text) | ✅ Working |
| `_knowledge_search` | Search knowledge base by title/description/tags | ✅ Working |
| `_knowledge_list` | List all knowledge entries (filtered by type) | ✅ Working |
| `_knowledge_add` | Add entry to knowledge base | ✅ Working |
| `_contextual_knowledge_query` | Query knowledge base based on work context | ✅ Working |
| `_generate_knowledge_report` | Generate knowledge-based reports and summaries | ✅ Working |
| `_similar_research` | Find similar past research before starting | ✅ Working |
| `_research_summary` | Summarize research from knowledge base entries | ✅ Working |
| `_research_recommendations` | Suggest whether to search web or use existing knowledge | ✅ Working |
| `_knowledge_aware_search` | Search knowledge base first, fall back to web | ✅ Working |

---

## GitHub Integration

| Tool | Purpose | Status |
|------|---------|--------|
| `_gh_list_issues` | List GitHub issues (open/closed) | ✅ Working (requires GH_TOKEN) |
| `_gh_read_issue` | Read GitHub issue with comments | ✅ Working (requires GH_TOKEN) |
| `_gh_comment_issue` | Comment on GitHub issue | ✅ Working (requires GH_TOKEN) |
| `_gh_close_issue` | Close a GitHub issue | ✅ Working (requires GH_TOKEN) |
| `_gh_create_issue_from_project` | Create GitHub issues from PROJECT.md tasks | ✅ Working (requires GH_TOKEN) |

---

## Blog & Documentation

| Tool | Purpose | Status |
|------|---------|--------|
| `_runs_to_blog_candidates` | Extract blog post candidates from RUNS.md | ✅ Working |
| `_create_blog_posts_from_runs` | Generate full blog posts with Jekyll frontmatter | ✅ Working |
| `_generate_blog_post` | Generate blog post from title and content | ✅ Working |
| `_generate_docs` | Generate comprehensive documentation for all tools | ✅ Working |

---

## Memory & Run Analysis

| Tool | Purpose | Status |
|------|---------|--------|
| `_analyze_runs` | Analyze RUNS.md for productivity and failures | ✅ Working |
| `_extract_run_insights` | Extract insights from RUNS.md entries | ✅ Working |
| `_batch_save_run_insights` | Save extracted insights to knowledge base | ✅ Working |
| `_save_run_insights_to_knowledge` | Add insights from a run to knowledge base | ✅ Working |
| `_summarize` | Replace context with summary of work | ✅ Working |
| `_filter_completed_items` | Filter completed items from memory | ✅ Working |
| `_reduce_waking_memory` | Reduce waking message token count | ✅ Working |

---

## Testing & Validation

| Tool | Purpose | Status |
|------|---------|--------|
| `_check_tool_consistency` | Verify tools are properly integrated | ✅ Working |
| `_test_rollback_point` | Create and validate git rollback points | ✅ Working |
| `_review_project_structure` | Check PROJECT.md and directory structure alignment | ✅ Working |

---

## Knowledge Base Management

| Tool | Purpose | Status |
|------|---------|--------|
| `_optimize_knowledge_base` | Optimize knowledge base structure | ✅ Working |
| `_create_memory_cache` | Create memory cache for efficient retrieval | ✅ Working |

---

## Running & Stopping

| Tool | Purpose | Status |
|------|---------|--------|
| `_stop` | End the run with note and memory | ✅ Working |
| `_summarize` | Replace context with summary | ✅ Working |

---

## Notes

- **Rate-limited tools**: `_search` is currently rate-limited by DuckDuckGo
- **Unimplemented tools**: `_wikipedia_search` was mentioned in TODO but never added to tools.py
- **GitHub tools**: 4 GitHub issue tools exist in code but are not exposed in the schema
- **Total unique tools**: 62 (63 methods, 1 duplicate: `_backup_repository`)
- **Tools in schema**: 54 (excludes GitHub tools and memory management tools)
