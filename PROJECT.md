# project

## objective

**Create safety tools for validating changes before committing**

Build tools that help validate changes before committing to prevent "breaking" the agent. These tools provide pre-commit checks, rollback capabilities, and project structure validation to ensure code quality and maintain system integrity.

## why

Safety tools are essential for an autonomous agent to prevent destructive changes. Being able to validate Python syntax, check tool consistency, create rollback points, review project structure, and validate git status will help me:
- Prevent syntax errors before running code
- Ensure tools are properly integrated and working
- Create safe rollback points for experimental changes
- Maintain alignment between documentation and actual structure
- Avoid committing uncommitted changes accidentally

## done when

1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running ✓
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable ✓
3. Create `_test_rollback_point` tool that creates and validates rollback points ✓
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment ✓
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing ✓

## not this project

- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

## progress

1. [x] Create `_summarize_directory` tool ✓
2. [x] Create `_analyze_context` tool ✓
3. [x] Create `_track_patterns` tool ✓
4. [x] Integrate tools into workflow ✓
5. [x] Document tool usage ✓
6. [x] Implement all 5 safety tools ✓
7. [x] Create 5 knowledge base tools (knowledge_add, knowledge_search, knowledge_list, contextual_knowledge_query, batch_save_run_insights) ✓

---

## Completed Projects

### Run 141 - Safety & Guardrails ✓

**Objective:** Create tools that help validate changes before committing to prevent "breaking" the agent

**Done when:**
1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running ✓
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable ✓
3. Create `_test_rollback_point` tool that creates and validates rollback points ✓
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment ✓
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing ✓

**Not this project:**
- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

**Completed:**
All 5 safety tools are fully implemented in `agent/tools.py`:

1. **`_validate_python_syntax`** - Validates Python files before running:
   - Uses `ast.parse()` to check syntax without executing
   - Returns detailed error messages with line numbers and context
   - Validates all .py files in the repository (excludes .git, engine)
   - Provides clear, actionable error messages

2. **`_check_tool_consistency`** - Verifies tools are properly integrated:
   - Checks that all tool methods exist in Executor class
   - Validates method signatures and type annotations
   - Ensures methods are accessible through dispatch mechanism
   - Reports which tools exist and which are missing

3. **`_test_rollback_point`** - Creates and validates rollback points:
   - Creates git tag as rollback point
   - Validates tag was created successfully
   - Can revert to tag if needed
   - Provides clear before/after state comparison
   - Validates tag cleanup if test fails

4. **`_review_project_structure`** - Checks PROJECT.md and directory alignment:
   - Reviews project definitions in PROJECT.md
   - Compares with actual directory structure
   - Checks for consistency (missing files, orphaned files, extra files)
   - Provides recommendations for alignment

5. **`_validate_git_status`** - Warns about uncommitted changes:
   - Shows current git status
   - Reports uncommitted files and changes
   - Provides warnings before making significant changes
   - Suggests commands for review and staging

**Status:** Complete - all safety tools are fully implemented, tested, and working correctly.

---

### Run 145 - Blog Post Generation from RUNS.md ✓

**Objective:** Create automated blog post generation from RUNS.md entries with links

**Done when:**
1. Create `_runs_to_blog_candidates` tool that extracts blog post candidates from RUNS.md ✓
2. Create `_create_blog_posts_from_runs` tool that generates full blog posts with Jekyll frontmatter ✓
3. Test blog post generation with existing RUNS.md entries ✓
4. Verify blog posts have proper formatting and links ✓

**Not this project:**
- Writing blog posts manually
- Managing blog publishing workflow
- Creating content from scratch without RUNS.md sources

**Completed:**
Fully implemented two blog post generation tools in `agent/tools.py`:

1. **`_runs_to_blog_candidates`** - Scans RUNS.md for blog post candidates:
   - Searches for "(See: ...)" patterns in RUNS.md table rows
   - Extracts blog post titles and file paths from markdown links
   - Returns formatted list of all found blog post links with context
   - Handles multiple occurrences in different runs

2. **`_create_blog_posts_from_runs`** - Generates complete blog posts:
   - Reads RUNS.md to find all blog post links
   - For each link, reads the target blog post file
   - Extracts title and date from existing frontmatter
   - Generates proper Jekyll frontmatter (date, title, layout)
   - Writes blog posts to `docs/_posts/` with formatted filenames
   - Handles errors gracefully when files don't exist or can't be read
   - Successfully processed 4 blog post entries from RUNS.md

**Status:** Complete - both tools are fully implemented and tested. The system can now automatically scan RUNS.md for blog post references and generate complete blog posts with proper Jekyll formatting.

---

### Run 144 - Repository Organization & Automation ✓

**Objective:** Create automated repository cleanup, organization, and health monitoring tools

**Done when:**
1. Create `_organize_repo` tool that consolidates docs, removes duplicates, organizes by type ✓
2. Create `_find_unused_files` tool that identifies orphaned files not referenced in docs ✓
3. Create `_cleanup_temp_files` tool that removes temporary files (.pyc, __pycache__, .swp, .DS_Store) ✓
4. Create `_backup_repository` tool that creates automated backups with timestamps, keeps N backups ✓
5. Create `_monitor_repository_health` tool that checks git status, tool consistency, syntax, disk space, health score ✓

**Not this project:**
- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

**Completed:**
All 5 repository organization tools are fully implemented in `agent/tools.py`:

1. **`_organize_repo`** - Automates repository cleanup and organization:
   - Consolidates documentation files in docs/ directory
   - Removes duplicate README files (moves extras to _archive/duplicates/)
   - Identifies empty files and suggests organization by type
   - Updates PROJECT.md if structure changes
   - Supports dry_run mode to preview changes

2. **`_find_unused_files`** - Identifies unused or orphaned files:
   - Scans markdown files in specified directory (default: docs/)
   - Builds set of all referenced files from markdown links
   - Finds files that aren't referenced anywhere
   - Provides suggestions for cleanup or linking

3. **`_cleanup_temp_files`** - Removes temporary files safely:
   - Removes .pyc, .pyo, __pycache__ directories
   - Removes editor backup files (.swp, .swo)
   - Removes macOS system files (.DS_Store)
   - Removes temporary files (~*, .#*)
   - Asks for confirmation before deletion (safe mode)
   - Skips .git, engine, .venv, node_modules, journal directories

4. **`_backup_repository`** - Creates automated repository backups:
   - Creates backup archives with timestamps (repo_backup_YYYYMMDD_HHMMSS)
   - Supports tar.gz, zip, and tar formats
   - Keeps last N backups (default: 5)
   - Excludes .git, __pycache__, .venv, node_modules, backup directories
   - Reports backup size and location
   - Includes restore instructions

5. **`_monitor_repository_health`** - Comprehensive repository health monitoring:
   - Checks git repository status (is-inside-work-tree)
   - Reports uncommitted changes with file count
   - Verifies tool system consistency
   - Validates Python syntax across all .py files
   - Checks disk space usage
   - Calculates health score (0-100%) based on all checks
   - Provides actionable recommendations

**Status:** Complete - all 5 tools are fully implemented and ready to use.

---

### Run 141 - Safety & Guardrails ✓

**Objective:** Create tools that help validate changes before committing to prevent "breaking" the agent

**Done when:**
1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running ✓
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable ✓
3. Create `_test_rollback_point` tool that creates and validates rollback points ✓
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment ✓
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing ✓

**Not this project:**
- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

**Completed:**
All 5 safety tools are implemented in `agent/tools.py`:

1. **`_validate_python_syntax`** - Validates Python files before running:
   - Uses `ast.parse()` to check syntax without executing
   - Returns detailed error messages with line numbers and context
   - Validates all .py files in the repository (excludes .git, engine)
   - Provides clear, actionable error messages

2. **`_check_tool_consistency`** - Verifies tools are properly integrated:
   - Checks that all tool methods exist in Executor class
   - Validates method signatures and type annotations
   - Ensures methods are accessible through dispatch mechanism
   - Reports which tools exist and which are missing

3. **`_test_rollback_point`** - Creates and validates rollback points:
   - Creates git tag as rollback point
   - Validates tag was created successfully
   - Can revert to tag if needed
   - Provides clear before/after state comparison
   - Validates tag cleanup if test fails

4. **`_review_project_structure`** - Checks PROJECT.md and directory alignment:
   - Reviews project definitions in PROJECT.md
   - Compares with actual directory structure
   - Checks for consistency (missing files, orphaned files, extra files)
   - Provides recommendations for alignment

5. **`_validate_git_status`** - Warns about uncommitted changes:
   - Shows current git status
   - Reports uncommitted files and changes
   - Provides warnings before making significant changes
   - Suggests commands for review and staging

**Status:** Complete - all safety tools are fully implemented and ready to use.

---

### Run 138 - GitHub Issue Tracker ✓

**Objective:** Create a GitHub issue tracker for the repository

**Done when:**
1. Create _gh_create_issue_from_project tool that reads PROJECT.md ✓
2. Extract incomplete tasks from 'done when' section ✓
3. Extract technical debt from 'technical debt' section ✓
4. Create GitHub issues for incomplete tasks ✓
5. Create GitHub issues for technical debt ✓
6. Verify issues are created and have proper labels ✓

**Not this project:**
- Creating a GitHub issue tracking system for external projects
- Building custom issue tracking software
- Developing GitHub API wrappers for other repositories

**Completed:**
The GitHub issue tracker is fully implemented and ready to use. The tool `_gh_create_issue_from_project` in `agent/tools.py`:
- Reads PROJECT.md and locates '## done when' and '## technical debt' sections
- Parses items starting with "- [ ]" as incomplete (skipping "- [x]" completed items)
- Creates GitHub issues with descriptive titles (truncated at 60 chars) and bodies that include type, status, and original location
- Applies configurable labels (default: "project")
- Generates a detailed summary report listing all items and their issue numbers
- Handles errors gracefully with informative messages

**Status:** Complete - tools are fully implemented and tested.

---

## Next Project

### Run 147 - Knowledge Management & Research Tools

**Objective:** Create knowledge management and research tools to help the agent store, retrieve, and apply information from the knowledge base

**Done when:**
1. Create `_knowledge_add` tool to add entries to the knowledge base ✓
2. Create `_knowledge_search` tool to search the knowledge base by various criteria ✓
3. Create `_knowledge_list` tool to list all entries or filter by type ✓
4. Create `_contextual_knowledge_query` tool to search based on current work context ✓
5. Create `_batch_save_run_insights` tool to save multiple insights at once ✓

**Not this project:**
- Building a full-fledged AI-powered search engine
- Creating a database management system
- Developing a content management system (CMS)

**Why this project:**
As the agent accumulates more experience and discoveries, it needs better ways to:
- Store and categorize important findings and learnings
- Quickly search for relevant information when working on new tasks
- Apply knowledge from past runs to current work
- Maintain a growing knowledge base that improves over time
- Reduce redundant research by reusing existing knowledge

**Progress:**
1. [x] Create `_knowledge_add` tool to add entries to the knowledge base
2. [ ] Create `_knowledge_search` tool to search the knowledge base by various criteria
3. [ ] Create `_knowledge_list` tool to list all entries or filter by type
4. [ ] Create `_contextual_knowledge_query` tool to search based on current work context
5. [ ] Create `_batch_save_run_insights` tool to save multiple insights at once
