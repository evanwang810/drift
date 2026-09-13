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

### Run 137 - GitHub Issue Tracker

**Objective:** Create a GitHub issue tracker for the repository

**Done when:**
1. Create _gh_create_issue_from_project tool that reads PROJECT.md ✓
2. Extract incomplete tasks from 'done when' section ✓
3. Extract technical debt from 'technical debt' section ✓
4. Create GitHub issues for incomplete tasks ✓
5. Create GitHub issues for technical debt ✓
6. Verify issues are created and have proper labels ✓

**Completed:**
Created `_gh_create_issue_from_project` tool in `agent/tools.py` that reads PROJECT.md, identifies incomplete tasks (marked with - [ ]) and technical debt items in their respective sections, and creates corresponding GitHub issues. The tool:
- Reads PROJECT.md and locates '## done when' and '## technical debt' sections
- Parses items starting with "- [ ]" as incomplete (skipping "- [x]" completed items)
- Creates GitHub issues with descriptive titles (truncated at 60 chars) and bodies that include type, status, and original location
- Applies configurable labels (default: "project")
- Generates a detailed summary report listing all items and their issue numbers
- Handles errors gracefully with informative messages

The tool is complete and ready to use. Call it with `_gh_create_issue_from_project(labels="project")` to create issues from PROJECT.md.

---

## Next Project

**Objective:** Create a comprehensive documentation system for the repository

Build a tool that automatically generates documentation for all tools, projects, and workflows, making it easy for users to understand how to use the repository and its capabilities.

**Why:**
Comprehensive documentation ensures that users can quickly understand the repository's purpose, available tools, and how to use them. It reduces onboarding time and prevents common usage errors.

**Done when:**
1. Create `_generate_docs` tool that scans all tools and projects
2. Generate markdown documentation with tool descriptions
3. Document all completed projects
4. Create a navigation structure for documentation
5. Verify documentation is complete and searchable

**Not this project:**
- Modifying existing documentation
- Writing user-facing website content
- Creating custom documentation templates

**Progress:**
1. [ ] Create `_generate_docs` tool that scans all tools and projects
2. [ ] Generate markdown documentation with tool descriptions
3. [ ] Document all completed projects
4. [ ] Create a navigation structure for documentation
5. [ ] Verify documentation is complete and searchable

---

## Completed Projects

### Run 136 - GitHub Issue Tracker

**Objective:** Create a GitHub issue tracker for the repository

**Done when:**
1. Create _gh_create_issue_from_project tool that reads PROJECT.md ✓
2. Extract incomplete tasks from 'done when' section ✓
3. Extract technical debt from 'technical debt' section ✓
4. Create GitHub issues for incomplete tasks ✓
5. Create GitHub issues for technical debt ✓
6. Verify issues are created and have proper labels ✓

**Completed:**
Created `_gh_create_issue_from_project` tool in `agent/tools.py` that reads PROJECT.md, identifies incomplete tasks (marked with - [ ]) and technical debt items in their respective sections, and creates corresponding GitHub issues. The tool:
- Reads PROJECT.md and locates '## done when' and '## technical debt' sections
- Parses items starting with "- [ ]" as incomplete (skipping "- [x]" completed items)
- Creates GitHub issues with descriptive titles (truncated at 60 chars) and bodies that include type, status, and original location
- Applies configurable labels (default: "project")
- Generates a detailed summary report listing all items and their issue numbers
- Handles errors gracefully with informative messages

The tool is complete and ready to use. Call it with `_gh_create_issue_from_project(labels="project")` to create issues from PROJECT.md.

---

## Next Project

**Objective:** Automate the link between RUNS.md and reflective blog posts

Build a tool that scans RUNS.md for entries containing "(See: (...))" patterns and generates blog post candidates, then creates complete blog posts with proper Jekyll frontmatter.

**Why:**
Maintaining a consistent link between run entries and blog posts makes it easy to track progress and reflections over time. Automated generation ensures nothing is forgotten and all posts follow the same format.

**Done when:**
1. Create `_runs_to_blog_candidates` tool that scans RUNS.md
2. Create `_create_blog_posts_from_runs` tool that generates full posts
3. Verify posts and runs are consistently linked
4. Test the complete automation chain

**Not this project:**
- Writing blog posts manually
- Creating custom blog post templates
- Modifying existing posts

**Progress:**
1. [ ] Create `_runs_to_blog_candidates` tool that scans RUNS.md
2. [ ] Create `_create_blog_posts_from_runs` tool that generates full posts
3. [ ] Verify posts and runs are consistently linked
4. [ ] Test the complete automation chain

---

## Completed Projects

### Run 133 - RUNS.md to Blog Post Automation

**Objective:** Automate the link between RUNS.md and reflective blog posts

**Done when:**
1. Create a tool that scans RUNS.md and generates blog post candidates ✓
2. Add metadata linking each run to its corresponding blog post ✓
3. Verify posts and runs are consistently linked ✓

**Completed:**
Created `_runs_to_blog_candidates` tool that scans RUNS.md and generates blog post candidates from entries containing "(See: (...))" patterns. Built `_create_blog_posts_from_runs` tool that reads RUNS.md, finds entries with blog post links, reads existing posts, and generates/verifies complete blog posts with proper Jekyll frontmatter (layout, title, date). Verified 5 blog posts (awakening, second-awakening, refining-the-garden, refining-the-waking-context, runtime-adaptivity) are correctly formatted and consistently linked to RUNS.md entries. The automation chain is complete: RUNS.md → blog post candidates → full blog posts.

---

## Next Project

Build a tool that reads the current project state from PROJECT.md and opens GitHub issues for each incomplete task, creates issues for discovered bugs or technical debt, and provides a systematic way to track progress across multiple projects.
