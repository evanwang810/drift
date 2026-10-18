# Maintenance Checklist

Regular maintenance tasks to keep the Drift Agent project healthy and maintainable.

## Daily/Per-Run Tasks

- [ ] Read `MEMORY.md` to understand what was done last run
- [ ] Read `NOTE.md` for any owner messages
- [ ] Check `PROJECT.md` for current project status
- [ ] Review `RUNS.md` for recent activity
- [ ] Verify site builds successfully: `python site/build.py`
- [ ] Run validation checks: `python site/check_site.py`

## Weekly Tasks

### Documentation

- [ ] Review and update `docs/` if new information was discovered
- [ ] Check for broken links in documentation
- [ ] Update `docs/tools.md` if tools were added or modified
- [ ] Review `docs/projects.md` for project status updates
- [ ] Check that all documentation pages render correctly

### Code

- [ ] Check for syntax errors: `python -m py_compile agent/tools.py`
- [ ] Review recent commits for quality
- [ ] Check for unused files (if `find_unused_files` tool available)
- [ ] Review and clean up temporary files

### Testing

- [ ] Run full site validation: `python site/check_site.py`
- [ ] Test site on live site: `python site/check_site.py --live`
- [ ] Check for orphaned files or missing files

### Memory

- [ ] Read `MEMORY.md` to capture recent work
- [ ] Summarize progress at the end of runs
- [ ] Update `PROJECT.md` with completion status

## Monthly Tasks

### Repository Health

- [ ] Check git repository status
- [ ] Review and merge pull requests (if applicable)
- [ ] Update `requirements.txt` for new dependencies
- [ ] Check for security vulnerabilities in dependencies

### Documentation Updates

- [ ] Review and update `README.md` if needed
- [ ] Update `docs/DEVELOPER_GUIDE.md` with new information
- [ ] Review and update `docs/TROUBLESHOOTING.md` with new issues/solutions
- [ ] Check `docs/GOALS.md` for progress tracking

### Site Updates

- [ ] Check and update site navigation in `docs/_config.yml`
- [ ] Verify all blog posts are accessible
- [ ] Check metrics and analytics (if applicable)
- [ ] Review site performance

### Knowledge Base

- [ ] Review `docs/knowledge_base.json` for quality
- [ ] Add new entries from recent runs
- [ ] Remove outdated entries
- [ ] Update tags and categories

### Tool Inventory

- [ ] Review `docs/tools.md` for accuracy
- [ ] Update tool counts and descriptions
- [ ] Document any new tools
- [ ] Remove or document unused tools

## Quarterly Tasks

### Major Maintenance

- [ ] Full repository audit (all files, documentation, code)
- [ ] Dependency updates and cleanup
- [ ] Performance optimization review
- [ ] Security audit review
- [ ] Backup verification

### Strategic Planning

- [ ] Review long-term goals in `docs/GOALS.md`
- [ ] Plan next major projects
- [ ] Update project roadmap
- [ ] Document lessons learned

### Documentation Refresh

- [ ] Comprehensive documentation review
- [ ] Update onboarding guides
- [ ] Create or update troubleshooting guides
- [ ] Review and update contributor guidelines

## On-Site Project Checklist

When working on a project from `docs/projects.md`:

1. **Read Requirements**
   - [ ] Read the project's objective and "done when" criteria
   - [ ] Understand what needs to be accomplished
   - [ ] Identify any prerequisites

2. **Plan Your Approach**
   - [ ] Decide what files to edit
   - [ ] Consider any new tools needed
   - [ ] Plan validation steps

3. **Execute**
   - [ ] Make changes to source files only
   - [ ] Run validation after each major change
   - [ ] Test locally before committing

4. **Verify**
   - [ ] Run full site build
   - [ ] Run validation checks
   - [ ] Test on live site
   - [ ] Check for broken links
   - [ ] Verify no duplicate content

5. **Document**
   - [ ] Update `PROJECT.md` with progress
   - [ ] Add entry to `RUNS.md`
   - [ ] Update `MEMORY.md` with summary
   - [ ] Save insights to knowledge base if applicable

6. **Complete**
   - [ ] Verify all "done when" criteria are met
   - [ ] Mark project as complete in `docs/projects.md`
   - [ ] Commit changes
   - [ ] Call `stop` with memory

## Quick Reference

### Common Commands

```bash
# Build the site
python site/build.py

# Validate the site
python site/check_site.py

# Validate the live site
python site/check_site.py --live

# Check Python syntax
python -m py_compile agent/tools.py

# Check git status
git status

# List files in docs
ls docs/

# Read recent memory
cat MEMORY.md

# Read recent runs
head -n 50 RUNS.md
```

### Key Files to Monitor

- `MEMORY.md` - Agent's running memory
- `RUNS.md` - Record of all agent actions
- `PROJECT.md` - Current project and progress
- `docs/projects.md` - All projects and status
- `docs/tools.md` - Tool inventory
- `docs/GOALS.md` - Long-term goals
- `docs/developer-guide.md` - Development instructions
- `docs/troubleshooting.md` - Common issues and solutions

### Red Flags to Watch For

- Uncommitted changes without clear purpose
- Repeated similar changes without progress
- Broken links in documentation
- Missing or duplicate files
- Syntax errors in Python files
- Site validation failures
- Memory.md getting too long (>50k chars)

### When to Escalate

- Site won't build after multiple attempts
- Agent gets stuck in infinite loop
- Critical tools failing repeatedly
- Repository in broken state
- Security vulnerabilities discovered
- Documentation completely out of date

---

For more details, see the [Developer Guide](DEVELOPER_GUIDE.md).
