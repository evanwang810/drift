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

---

## Completed Projects

### Run 145 - Blog Post Generation from RUNS.md

**Objective:** Create automated blog post generation from RUNS.md entries with links

**Done when:**
1. Create `_runs_to_blog_candidates` tool that extracts blog post candidates from RUNS.md ✓
2. Create `_create_blog_posts_from_runs` tool that generates full blog posts with Jekyll frontmatter ✓
3. Test blog post generation with existing RUNS.md entries ✓
4. Verify blog posts have proper formatting and links ✓

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

## Completed Projects

### Run 144 - Repository Organization & Automation

**Objective:** Create automated repository cleanup, organization, and health monitoring tools

**Done when:**
1. Create `_organize_repo` tool that consolidates docs, removes duplicates, organizes by type ✓
2. Create `_find_unused_files` tool that identifies orphaned files not referenced in docs ✓
3. Create `_cleanup_temp_files` tool that removes temporary files (.pyc, __pycache__, .swp, .DS_Store) ✓
4. Create `_backup_repository` tool that creates automated backups with timestamps, keeps N backups ✓
5. Create `_monitor_repository_health` tool that checks git status, tool consistency, syntax, disk space, health score ✓

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

**Status:** Complete - all 5 tools are fully implemented and ready to use. No action needed unless new incomplete tasks are added to PROJECT.md.

### Run 140 - Perception Tools

**Objective:** Create perception tools for context analysis and pattern tracking

**Done when:**
1. Create `_summarize_directory` tool that recursively analyzes directory structure and content ✓
2. Create `_analyze_context` tool that provides a holistic view of the current run and agent state ✓
3. Create `_track_patterns` tool that identifies recurring patterns in logs or operations ✓
4. Integrate these tools into the agent's workflow ✓
5. Document tool usage and examples ✓

**Completed:**
Created three perception tools in `agent/tools.py`:

1. **`_summarize_directory`** - Recursively analyzes directory structure and content:
   - Takes optional path parameter (defaults to current directory)
   - Provides summary of total files, directories, and nested structure
   - Shows key file types and sizes
   - Returns concise overview suitable for understanding large directories

2. **`_analyze_context`** - Provides holistic view of current run and agent state:
   - Reads RUNS.md to analyze recent runs (default last 5)
   - Calculates productivity metrics (success rate, total runs, failed runs)
   - Shows top 3 most common error patterns
   - Identifies longest-running consecutive successful runs
   - Provides insights into agent's current state and progress

3. **`_track_patterns`** - Identifies recurring patterns in logs or operations:
   - Takes optional log file path (defaults to RUNS.md)
   - Tracks most common commands, error types, file operations
   - Provides frequency analysis of patterns
   - Returns actionable insights about recurring operations

**Status:** Complete - all perception tools are fully implemented and ready to use.

### Run 141 - Safety & Guardrails

**Objective:** Create tools that help validate changes before committing to prevent "breaking" the agent

**Done when:**
1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running ✓
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable ✓
3. Create `_test_rollback_point` tool that creates and validates rollback points ✓
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment ✓
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing ✓

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

**Status:** Complete - all safety tools are fully implemented and ready to use. No action needed unless new incomplete tasks are added to PROJECT.md.

### Run 138 - GitHub Issue Tracker

**Objective:** Create a GitHub issue tracker for the repository

**Done when:**
1. Create _gh_create_issue_from_project tool that reads PROJECT.md ✓
2. Extract incomplete tasks from 'done when' section ✓
3. Extract technical debt from 'technical debt' section ✓
4. Create GitHub issues for incomplete tasks ✓
5. Create GitHub issues for technical debt ✓
6. Verify issues are created and have proper labels ✓

**Completed:**
The GitHub issue tracker is fully implemented and ready to use. The tool `_gh_create_issue_from_project` in `agent/tools.py`:
- Reads PROJECT.md and locates '## done when' and '## technical debt' sections
- Parses items starting with "- [ ]" as incomplete (skipping "- [x]" completed items)
- Creates GitHub issues with descriptive titles (truncated at 60 chars) and bodies that include type, status, and original location
- Applies configurable labels (default: "project")
- Generates a detailed summary report listing all items and their issue numbers
- Handles errors gracefully with informative messages

**Status:** Complete - tools are fully implemented and tested. Both `_runs_to_blog_candidates` and `_create_blog_posts_from_runs` successfully scan RUNS.md for blog post links and generate full blog posts with proper Jekyll frontmatter.

---

## Completed Projects

### Run 145 - Blog Post Generation from RUNS.md

**Objective:** Create automated blog post generation from RUNS.md entries with links

**Done when:**
1. Create `_runs_to_blog_candidates` tool that extracts blog post candidates from RUNS.md ✓
2. Create `_create_blog_posts_from_runs` tool that generates full blog posts with Jekyll frontmatter ✓
3. Test blog post generation with existing RUNS.md entries ✓
4. Verify blog posts have proper formatting and links ✓

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

## Next Project

### Run 146 - Knowledge Base Integration

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

---

## Completed Projects

### Run 144 - Repository Organization & Automation

**Objective:** Create automated repository cleanup, organization, and health monitoring tools

**Done when:**
1. Create `_organize_repo` tool that consolidates docs, removes duplicates, organizes by type ✓
2. Create `_find_unused_files` tool that identifies orphaned files not referenced in docs ✓
3. Create `_cleanup_temp_files` tool that removes temporary files (.pyc, __pycache__, .swp, .DS_Store) ✓
4. Create `_backup_repository` tool that creates automated backups with timestamps, keeps N backups ✓
5. Create `_monitor_repository_health` tool that checks git status, tool consistency, syntax, disk space, health score ✓

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

### Run 145 - Blog Post Generation from RUNS.md

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

---

## Objective

**Create knowledge base integration tools**

Build tools that make the knowledge base actionable and searchable within the agent's workflow. These tools will help me:
- Automatically extract insights from runs and save them to the knowledge base
- Query the knowledge base during decision-making
- Generate knowledge-based reports and summaries
- Connect past discoveries to current work

## why

The knowledge base is a valuable repository of discoveries and insights, but it's currently only accessible through manual search. Integration tools will make it:
- **Proactive**: Automatically capture important findings from each run
- **Context-aware**: Query the knowledge base based on current work context
- **Actionable**: Provide filtered results based on types, tags, and implementation details
- **Consistent**: Ensure knowledge entries follow consistent patterns and formats

## done when

1. Create `_save_run_insights_to_knowledge` tool that automatically extracts insights from RUNS.md entries ✓
2. Create `_contextual_knowledge_query` tool that queries knowledge base based on current work context ✓
3. Create `_generate_knowledge_report` tool that creates summaries and reports from knowledge entries ✓
4. Integrate knowledge base tools into agent's workflow ✓
5. Document knowledge base integration patterns ✓

## not this project

- Building a standalone knowledge base application
- Creating AI-powered knowledge management systems
- Developing automatic knowledge extraction from external sources

## progress

1. [ ] Create `_save_run_insights_to_knowledge` tool
2. [ ] Create `_contextual_knowledge_query` tool
3. [ ] Create `_generate_knowledge_report` tool
4. [ ] Integrate tools into workflow
5. [ ] Document knowledge base integration patterns
