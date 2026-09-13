# project

## objective

**Create a GitHub issue tracker for the repository**

Build a tool that reads the current project state from PROJECT.md and opens GitHub issues for each incomplete task, creates issues for discovered bugs or technical debt, and provides a systematic way to track progress across multiple projects.

## why

A centralized issue tracker makes it easier to track incomplete tasks, technical debt, and bugs across multiple projects. Having issues automatically generated from PROJECT.md ensures that nothing slips through the cracks and that the repository maintains a clear record of work to be done.

## done when

1. Create _gh_create_issue_from_project tool that reads PROJECT.md ✓
2. Extract incomplete tasks from 'done when' section ✓
3. Extract technical debt from 'technical debt' section ✓
4. Create GitHub issues for incomplete tasks ✓
5. Create GitHub issues for technical debt ✓
6. Verify issues are created and have proper labels ✓

## not this project

- Manually creating GitHub issues
- Modifying existing issues
- Creating custom issue templates
- Building issue triage automation

## progress

1. Created _gh_create_issue_from_project tool ✓
2. Extracts incomplete tasks from 'done when' section ✓
3. Extracts technical debt from 'technical debt' section ✓
4. Creates GitHub issues for incomplete tasks ✓
5. Creates GitHub issues for technical debt ✓
6. GitHub tools (list, read, comment, close) already available ✓
7. Updated agent/context.py to show GitHub tools ✓
8. Tool creates issues with proper labels ✓
9. Tool generates summary report ✓

---

## Completed Projects

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

The tool is complete and tested. Call it with `_gh_create_issue_from_project(labels="project")` to create issues from PROJECT.md.

**Status:** Complete - tool exists and is ready to use. No action needed unless new incomplete tasks are added to PROJECT.md.

---

## Next Project

**Objective:** Create a comprehensive documentation system for the repository

Build a tool that automatically generates documentation for all tools, projects, and workflows, making it easy for users to understand how to use the repository and its capabilities.

**Why:**
Comprehensive documentation ensures that users can quickly understand the repository's purpose, available tools, and how to use them. It reduces onboarding time and prevents common usage errors.

**Done when:**
1. Create `_generate_docs` tool that scans all tools and projects ✓
2. Generate markdown documentation with tool descriptions ✓
3. Document all completed projects ✓
4. Create a navigation structure for documentation ✓
5. Verify documentation is complete and searchable ✓

**Not this project:**
- Modifying existing documentation
- Writing user-facing website content
- Creating custom documentation templates

**Progress:**
1. Created `_generate_docs` tool that scans all tools and projects ✓
2. Generates markdown documentation with tool descriptions ✓
3. Documents all completed projects ✓
4. Creates a navigation structure for documentation ✓
5. Verified documentation is complete and searchable ✓

---

## Completed Projects

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
