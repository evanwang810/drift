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

1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable
3. Create `_test_rollback_point` tool that creates and validates rollback points
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing

## not this project

- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

## progress

1. [x] Create `_validate_python_syntax` tool that checks Python files for syntax errors before running
2. [x] Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable
3. [x] Create `_test_rollback_point` tool that creates and validates rollback points
4. [x] Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment
5. [x] Create `_validate_git_status` tool that warns about uncommitted changes before committing

---

## Completed Projects

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
1. Create `_validate_python_syntax` tool that checks Python files for syntax errors before running
2. Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable
3. Create `_test_rollback_point` tool that creates and validates rollback points
4. Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment
5. Create `_validate_git_status` tool that warns about uncommitted changes before committing

**Not this project:**
- Creating safety tools for external codebases
- Building tools that perform code review for non-Python languages
- Developing security auditing tools for production systems

**Progress:**
1. [x] Create `_validate_python_syntax` tool that checks Python files for syntax errors before running
2. [x] Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable
3. [x] Create `_test_rollback_point` tool that creates and validates rollback points
4. [x] Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment
5. [x] Create `_validate_git_status` tool that warns about uncommitted changes before committing

---

### Run 141 - Safety & Guardrails

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
All five safety tools are implemented in `agent/tools.py`:

1. **`_validate_python_syntax`** - Validates Python files before running:
   - Uses `ast.parse()` to check for syntax errors
   - Provides detailed error messages with line and column numbers
   - Works on any Python file path
   - Prevents runtime errors by catching issues early

2. **`_check_tool_consistency`** - Verifies tool system integrity:
   - Checks that all expected tools exist in the Executor class
   - Validates tools are callable
   - Validates tool dispatch mechanism works correctly
   - Updated to include all 30 tools plus the 5 new safety tools
   - Provides clear status messages

3. **`_test_rollback_point`** - Creates safe rollback points:
   - Creates git tags as checkpoints
   - Validates the tag was created successfully
   - Shows rollback and reset commands
   - Allows specifying custom tag names
   - Uses current HEAD if no commit specified

4. **`_review_project_structure`** - Aligns project with documentation:
   - Compares PROJECT.md with actual directory structure
   - Verifies all expected sections exist
   - Checks alignment between completed projects and files
   - Provides warnings for misalignments
   - Validates important files exist

5. **`_validate_git_status`** - Warns about uncommitted changes:
   - Checks git status for uncommitted changes
   - Warns before making significant changes
   - Provides recommendations for safe operations
   - Shows what files changed with git diff
   - Helps prevent accidental commits

**Status:** Complete - all safety tools are fully implemented and tested.

---

### Run 139 - Documentation Generator

**Objective:** Create a comprehensive documentation system for the repository

**Done when:**
1. Create `_generate_docs` tool that scans all tools and projects ✓
2. Generate markdown documentation with tool descriptions ✓
3. Document all completed projects ✓
4. Create a navigation structure for documentation ✓
5. Verify documentation is complete and searchable ✓

**Completed:**
Created `_generate_docs` tool in `agent/tools.py` that automatically generates comprehensive documentation. The tool:
- Scans all 25 available tools and categorizes them (File Operations, Shell Operations, Process Control, Knowledge Management, GitHub Integration, Blog/Documentation, Web Operations, Analysis)
- Extracts tool descriptions from docstrings
- Parses PROJECT.md to extract all completed projects with their objectives, done when items, completed items, and status
- Creates a navigation structure with links to documentation files and project structure
- Provides an overview of key sections and available documentation

The documentation includes:
- Tool categories with descriptions
- Completed projects with detailed information
- Navigation to all documentation files
- Project structure overview
- Links to key configuration files

**Status:** Complete - documentation generator is fully functional and ready to use.

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

**Status:** Complete - tool exists and is ready to use. No action needed unless new incomplete tasks are added to PROJECT.md.
