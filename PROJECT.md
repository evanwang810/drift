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
