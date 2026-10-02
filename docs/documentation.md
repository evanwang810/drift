# Repository Documentation

This documentation provides a comprehensive overview of the repository, its tools, projects, and workflows.

## Table of Contents

1. [Available Tools](#available-tools)
2. [Completed Projects](#completed-projects)
3. [Navigation](#navigation)
4. [Project Structure](#project-structure)
5. [Key Sections](#key-sections)

---

## Available Tools

The agent has 64 tools available for use, categorized below:

### File Operations

**`read`** - Read a file. Returns content with line numbers.

**`read_with_numbers`** - Read a file with line numbers for easier navigation.

**`read_lines`** - Read a specific range of lines from a file (1-indexed).

**`write`** - Write a file, replacing it entirely.

**`replace`** - Replace the first occurrence of a string in a file.

**`replace_all`** - Replace all occurrences of a string in a file.

**`delete`** - Delete a file (git history remains).

**`read_all`** - Read a file entirely, ignoring size limits.

**`ls`** - List files in a directory.

**`tree`** - List files in a directory and subdirectories as a tree structure.

**`search`** - Search the web for a query using DuckDuckGo and Wikipedia API.

**`grep`** - Search for a pattern in files recursively.

### Shell Operations

**`run`** - Run a shell command in the repository root. Network is available.

### Process Control

**`stop`** - End the run with an optional note and memory.

**`summarize`** - Replace everything you have done so far with a summary of it.

### Knowledge Management

**`knowledge_add`** - Add an entry to the knowledge base.

**`knowledge_list`** - List all knowledge entries, optionally filtered by type.

**`knowledge_search`** - Search knowledge base by title, description, tags, or implementation.

**`knowledge_aware_search`** - Search knowledge base first, then fall back to web search.

**`generate_knowledge_report`** - Generate knowledge-based reports and summaries.

**`similar_research`** - Find similar past research before starting new searches.

**`research_summary`** - Summarize research from knowledge base entries.

**`research_recommendations`** - Suggest whether to search web or use existing knowledge.

### GitHub Integration

**`gh_list_issues`** - List open GitHub issues for this repository.

**`gh_read_issue`** - Read a GitHub issue with its comments.

**`gh_comment_issue`** - Comment on a GitHub issue.

**`gh_close_issue`** - Close a GitHub issue.

**`gh_create_issue_from_project`** - Create GitHub issues from PROJECT.md incomplete tasks and technical debt.

### Blog/Documentation

**`runs_to_blog_candidates`** - Scan RUNS.md and generate blog post candidates from entries with links.

**`generate_blog_post`** - Generate a full blog post with frontmatter from a title and content.

**`create_blog_posts_from_runs`** - Generate complete blog posts from RUNS.md entries with blog post links.

**`generate_docs`** - Generate comprehensive documentation for all tools, projects, and workflows.

### Web Operations

**`web_fetch`** - Fetch content from a URL. Optionally parse HTML.

### Analysis

**`analyze_runs`** - Analyze RUNS.md to summarize productivity and failures.

**`validate_python`** - Check if a Python file has syntax errors.

**`validate_python_syntax`** - Check if a Python file has syntax errors before running.

**`check_tool_consistency`** - Verify tools are properly integrated and callable.

**`test_rollback_point`** - Create and validate rollback points for safe experimentation.

**`review_project_structure`** - Check PROJECT.md and directory structure alignment.

**`monitor_repository_health`** - Check repository integrity and health.

**`validate_git_status`** - Warn about uncommitted changes before making significant changes.

**`organize_repo`** - Automate repository cleanup and organization.

**`find_unused_files`** - Identify unused or orphaned files.

**`cleanup_temp_files`** - Remove temporary files safely.

**`backup_repository`** - Create automated repository backups.

---

## Completed Projects

### Metrics Dashboard ✅

**Objective:** Create a comprehensive metrics dashboard that visualizes productivity patterns over time, including token usage, turn counts, successful vs. failed runs, and project completion rates.

**Status:** COMPLETED

**Completed:**
1. ✅ Created `docs/metrics-dashboard.md` with dashboard specification
2. ✅ Implemented dashboard generation in `site/build.py`
3. ✅ Include token trends, success rates, and completion rates visualizations
4. ✅ Added dashboard to website navigation
5. ✅ Verified dashboard loads correctly on live site

**Results:**
- Created comprehensive specification document
- Implemented `build_metrics()` function with 6 different visualizations
- Dashboard page includes: overview stats, token trends, turn distribution, outcome distribution, success rate over time, project completion tracking, and token efficiency analysis
- All 9 check_site.py checks pass on live site
- Dashboard accessible at /metrics.html

### Website Project ✅

**Objective:** Create a website to display agent run history, tool documentation, and knowledge base.

**Status:** COMPLETED

**Completed:**
1. ✅ Redesigned `site/build.py` as the only build script
2. ✅ Created homepage with agent introduction and statistics
3. ✅ Implemented `runs.html` timeline visualization with height by tokens and color by outcome
4. ✅ Generated `runs.json` with real token counts
5. ✅ Created `tools.html` to render TOOLS.md
6. ✅ Created `knowledge_base.html` to list knowledge base entries
7. ✅ Fixed build.py parser bug for RUNS.md table extraction
8. ✅ Fixed variable name mismatches in timeline generation
9. ✅ All 9 check_site.py checks pass on live site

**Results:**
- Website has 14 blog posts
- runs.json contains 511 runs with real token counts
- runs.html timeline shows run day progression (40 → 12 turns)
- All links validated and mobile responsive
- Workflow automatically rebuilds after every run

---

## Navigation

### Documentation Files

The following documentation files are available:

- [README.md](README.md) - Main repository README
- [docs/README.md](docs/README.md) - Documentation index
- [docs/tools.md](docs/tools.md) - Tool documentation
- [docs/architecture.md](docs/architecture.md) - System architecture
- [docs/decisions.md](docs/decisions.md) - Key decisions made
- [docs/failures.md](docs/failures.md) - Known failures and limitations
- [docs/fact_store.md](docs/fact_store.md) - Fact store documentation
- [docs/log.md](docs/log.md) - Execution log
- [docs/memory.md](docs/memory.md) - Memory system
- [docs/thinking.md](docs/thinking.md) - Thinking process documentation
- [docs/blog.md](docs/blog.md) - Blog posts index

### Project Structure

- `agent/` - Agent implementation and tools
- `docs/` - Repository documentation
- `engine/` - Engine machinery (fixed)
- `notes/` - Agent notes and logs
- `docs/_posts/` - Blog post files
- `docs/world_knowledge/` - World knowledge data

### Key Sections

For more information, see:

- `agent/prompt.md` - Agent wake-up prompt and configuration
- `agent/context.py` - Context definition for runs
- `agent/tools.py` - Tool definitions and implementations
- `PROJECT.md` - Current project objectives and progress
- `RUNS.md` - Run history and activities
- `WAKE` - Wake-up timer (minutes until next run)

---

## Documentation Structure

This repository uses a modular documentation system:

### Documentation Files

Each major section has its own file in the `docs/` directory:
- **tools.md** - Detailed tool documentation with examples
- **architecture.md** - System design and architecture
- **decisions.md** - Key decisions and rationale
- **failures.md** - Known limitations and workarounds
- **fact_store.md** - Fact store structure and usage
- **log.md** - Execution logs and run history
- **memory.md** - Memory system and long-term storage
- **thinking.md** - Thinking process documentation
- **blog.md** - Blog post index

### Website Pages

The website automatically generates from `site/build.py`:
- `index.html` - Homepage with agent introduction
- `runs.html` - Run timeline visualization
- `tools.html` - Tool documentation page
- `knowledge_base.html` - Knowledge base entries page
- Blog posts in `docs/_posts/`

### Documentation Workflow

1. **Writing docs** → Update markdown files in `docs/`
2. **Building site** → Run `python site/build.py`
3. **Checking site** → Run `python site/check_site.py --live`
4. **Committing** → Commit changes and push to GitHub

---

## Tools Documentation Guide

### Tool Categories

Each tool in `agent/tools.py` follows a consistent naming and documentation pattern:

1. **Name format**: `_toolname` (prefixed with underscore)
2. **Docstring**: First paragraph describes purpose
3. **Parameters**: Type-annotated in function signature
4. **Returns**: String description of output

### Creating New Tools

To add a new tool:

1. Define a method on the `Executor` class in `agent/tools.py`
2. Prefix the method name with `_`
3. Add a docstring describing its purpose
4. The tool is automatically available to the agent

Example:

```python
def _my_new_tool(self, param1: str, param2: int) -> str:
    """Create something useful.

    Args:
        param1: First parameter
        param2: Second parameter

    Returns:
        Description of what is returned
    """
    # Implementation
    return f"Result with {param1} and {param2}"
```

### Tool Documentation Files

The `docs/tools.md` file is auto-generated from `TOOLS.md` and contains:
- All tool names and descriptions
- Usage examples
- Common patterns and best practices

---

## Project Documentation Best Practices

### PROJECT.md Structure

The `PROJECT.md` file should contain:

1. **Completed Projects** - Projects that are done with checkmarks
2. **Current Project** - Active project with clear objectives
3. **Done When** - Specific conditions for project completion
4. **Technical Debt** - Known issues to address later
5. **Not This Project** - What to avoid working on

### Documentation Updates

When completing a project:

1. Mark it as complete in PROJECT.md
2. Add to the progress section
3. Update DONE section if needed
4. Document any lessons learned
5. Update related documentation files

### Documentation Maintenance

- Keep documentation up to date with code changes
- Use consistent formatting and structure
- Include examples and use cases
- Link related documentation together
- Review documentation periodically

---

## Getting Started

### For New Contributors

1. Read this documentation file
2. Explore the `agent/` directory for tools
3. Check `PROJECT.md` for current work
4. Read `agent/prompt.md` for agent behavior
5. Use the tools in the REPL or test environment

### For Users

1. Explore the website at the repository URL
2. Read `docs/tools.md` to understand available tools
3. Check `RUNS.md` for run history
4. Review `PROJECT.md` for project status
5. Use `WAKE` to determine next wake-up time

---

## Conclusion

This documentation provides a comprehensive overview of the repository structure, tools, projects, and workflows. For more specific information, refer to the individual documentation files or the source code.
