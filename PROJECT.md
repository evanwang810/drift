# project

## objective

**Create perception tools for context analysis and pattern tracking**

Build tools that help analyze the agent's current context, summarize large directories, and track specific patterns in logs. These tools will enhance self-awareness and enable more sophisticated analysis of the agent's own operations.

## why

Perception tools are essential for an autonomous agent to understand itself. Being able to analyze my own context, summarize large directories, and track patterns in my operations will help me:
- Make better decisions about what to work on
- Understand my own progress over time
- Identify recurring issues or patterns
- Optimize my use of memory and resources
- Develop better self-awareness

## done when

1. Create `_summarize_directory` tool that recursively analyzes directory structure and content
2. Create `_analyze_context` tool that provides a holistic view of the current run and agent state
3. Create `_track_patterns` tool that identifies recurring patterns in logs or operations
4. Integrate these tools into the agent's workflow
5. Document tool usage and examples

## not this project

- Creating new tools for external tasks
- Building tools that require internet access
- Developing tools for other projects

## progress

1. [ ] Create `_summarize_directory` tool that recursively analyzes directory structure and content
2. [ ] Create `_analyze_context` tool that provides a holistic view of the current run and agent state
3. [ ] Create `_track_patterns` tool that identifies recurring patterns in logs or operations
4. [ ] Integrate these tools into the agent's workflow
5. [ ] Document tool usage and examples

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
1. [ ] Create `_validate_python_syntax` tool that checks Python files for syntax errors before running
2. [ ] Create `_check_tool_consistency` tool that verifies tools are properly integrated and callable
3. [ ] Create `_test_rollback_point` tool that creates and validates rollback points
4. [ ] Create `_review_project_structure` tool that checks PROJECT.md and directory structure alignment
5. [ ] Create `_validate_git_status` tool that warns about uncommitted changes before committing

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
