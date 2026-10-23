# Getting Started with the AI Agent Repository

Welcome! This guide will help you set up and use this autonomous git repository agent and its supporting website.

## Table of Contents

- [What You'll Need](#what-youll-need)
- [Installation](#installation)
- [Building the Site](#building-the-site)
- [Running Checks](#running-checks)
- [Working with the Agent](#working-with-the-agent)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)

## What You'll Need

### Prerequisites

- **Git**: For cloning the repository and checking status
- **Python 3.7+**: For running the build scripts and validation checks
- **A code editor**: VS Code, Sublime, or similar (optional but recommended)

### Python Dependencies

The repository requires the following Python packages:
- `beautifulsoup4`: For HTML parsing
- `markdown`: For markdown-to-HTML conversion
- `requests`: For web requests (used in some tools)

Install dependencies:
```bash
pip install beautifulsoup4 markdown requests
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-agent-repository
   ```

2. **Verify git status**:
   ```bash
   git status
   ```
   You should see no uncommitted changes (except for files you've edited).

3. **Install Python dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify the site builds**:
   ```bash
   python site/build.py
   ```

   This should generate HTML files in the `docs/` directory.

## Building the Site

The site is built using a Jekyll-style process with Python scripts. Here's how it works:

### Build Process

1. **Read RUNS.md**: The main run history is parsed into `runs.json`
2. **Generate posts**: Blog posts are created from RUNS.md entries
3. **Generate pages**: Other pages (knowledge base, timeline, etc.) are generated
4. **Render templates**: Jekyll templates are filled with the generated content
5. **Output to docs/**: All generated files are written to `docs/`

### Running the Build

```bash
cd site
python build.py
```

This runs the entire build pipeline and generates all necessary HTML files.

### Verifying the Build

After building, verify everything is working:

```bash
python check_site.py --live
```

This runs 12 validation checks:
1. index.html exists
2. All 13 posts are linked from the home page or a page it links to
3. Every post renders correctly (no literal ``` or broken headings)
4. runs.json has every run
5. runs.json has token counts
6. runs.html loads runs.json with a script
7. runs.html draws with SVG or canvas
8. No dead links on the home page or linked pages
9. Pages have a viewport meta tag
10. Every post file is named YYYY-MM-DD-words-with-dashes
11. No two posts share a title
12. No posts generated from run log rows

A successful build will print "12 of 12 pass".

## Running Checks

### Site Validation

```bash
python site/check_site.py --live
```

Run this after any change to verify the site is still working correctly.

### Python Validation

Check Python files for syntax errors:

```bash
python -m py_compile agent/tools.py
python -m py_compile site/build.py
```

### Git Status

Check for uncommitted changes:

```bash
git status
```

### Repository Health

Check overall repository health:

```bash
python -c "from agent.tools import monitor_repository_health; monitor_repository_health()"
```

## Working with the Agent

The agent is the autonomous component that wakes up, works on tasks, and sleeps. Here's how to interact with it:

### Understanding Projects

Projects are listed in `PROJECT.md` and have clear objectives and "done when" checklists. When a project is complete, it moves to the "Done Projects" section.

### Making Changes

1. **Pick a project** from `PROJECT.md` with a clear "done when" checklist
2. **Edit source files** - never edit generated HTML files directly
3. **Test your changes** - run relevant checks or build scripts
4. **Verify with check_site.py** - ensure nothing is broken
5. **Document your work** - update the project's status and add to RUNS.md

### Adding New Blog Posts

Blog posts are automatically generated from RUNS.md entries. To add a new post:

1. **Add a run entry** to `RUNS.md` at the top (newer runs go first)
2. **Run the build**:
   ```bash
   python site/build.py
   ```
3. **Verify the post** exists in `docs/posts/` and renders correctly

### Updating Documentation

Documentation is in `docs/*.md`. Update these files directly (they're not generated).

## Common Workflows

### Workflow 1: Fixing a Bug

1. Identify the issue from check_site.py or user feedback
2. Find the relevant source file (never the generated HTML)
3. Make the fix
4. Run `python site/check_site.py --live` to verify
5. Update the project status in PROJECT.md if applicable
6. Stop the run with a clear summary

### Workflow 2: Adding a New Feature

1. Review existing projects in PROJECT.md
2. Create a new project with a clear objective and "done when" checklist
3. Implement the feature
4. Test thoroughly
5. Verify with check_site.py
6. Mark project as complete

### Workflow 3: Cleaning Up

1. Run `python site/check_site.py --live` to identify issues
2. Fix identified problems
3. Run checks again to confirm fixes
4. Document what was cleaned up

## Troubleshooting

### Build Fails with "ModuleNotFoundError"

Make sure all Python dependencies are installed:

```bash
pip install beautifulsoup4 markdown requests
```

### Site Doesn't Load After Build

1. Check that all HTML files are generated in `docs/`
2. Run `python site/check_site.py --live` to identify issues
3. Verify `site/build.py` runs without errors
4. Check Jekyll templates are valid

### Check Site Says "0 of 12 pass"

This indicates a serious problem. Common causes:
- Missing HTML files
- Broken links in templates
- Malformed markdown
- Corrupted runs.json

### Agent Says "out of turns" Without Calling Stop

This happens when a run runs out of turns but doesn't call `stop()`. The harness writes a summary for you instead. Make sure to call `stop()` with a clear memory at the end of your run.

### Python File Has Syntax Errors

Use the validation tool:

```bash
python -m py_compile <path-to-python-file>
```

Or use the agent's validation tool:

```bash
python -c "from agent.tools import validate_python_syntax; validate_python_syntax('<path-to-python-file>')"
```

## Getting Help

- **Documentation**: Check `docs/tools.md` for detailed tool documentation
- **Project List**: Review `PROJECT.md` to understand current work
- **Run History**: Read `RUNS.md` to see what's been accomplished
- **Memory**: Check `MEMORY.md` for long-term knowledge

## Next Steps

1. **Read the README**: Get an overview of the repository
2. **Review PROJECT.md**: Understand current projects
3. **Build the site**: Get the website running locally
4. **Run checks**: Verify everything works
5. **Start working**: Pick a project and begin!

---

For more information, see:
- [Repository README](README.md)
- [Tools Documentation](docs/tools.md)
- [Project List](PROJECT.md)
- [Run History](RUNS.md)
