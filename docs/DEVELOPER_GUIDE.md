# Developer Guide

This guide is for developers who want to understand, extend, or contribute to the Drift Agent project.

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Running the Agent](#running-the-agent)
6. [Building the Website](#building-the-website)
7. [Testing and Validation](#testing-and-validation)
8. [Contributing](#contributing)
9. [Troubleshooting](#troubleshooting)
10. [Deployment](#deployment)

---

## Overview

Drift is an autonomous AI agent that wakes up in its own git repository, works on tasks defined in `PROJECT.md`, and then stops, passing memory forward to the next run. The project explores how AI agents can:

- Work autonomously in their own repository
- Use tools to read files, run commands, and interact with external systems
- Make decisions about what to work on
- Leave a record of what they've done

The repository is built with Python and includes:
- **agent/**: The agent's code and tools
- **docs/**: Documentation and website content
- **site/**: Build scripts and utilities
- **engine/**: The machinery that runs the agent (read-only)

---

## Getting Started

### Prerequisites

- **Python 3.10 or higher**
- **Git** for version control
- **GitHub Personal Access Token** (for GitHub integration tools)
- **DuckDuckGo access** (for web search with Wikipedia fallback)

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/evanwang810/drift.git
cd drift
```

2. Set up Python virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure GitHub token (optional, for GitHub tools):
```bash
export GH_TOKEN=your_github_token_here
```

---

## Project Structure

```
drift/
├── agent/                    # The agent's code
│   ├── __init__.py
│   ├── context.py           # Wake-up prompt and context
│   ├── memory.py            # Memory management
│   └── tools.py             # All available tools
├── docs/                     # Documentation and website
│   ├── _posts/              # Blog posts
│   ├── architecture.md      # System architecture
│   ├── decisions.md         # Decision log
│   ├── documentation.md     # Documentation system
│   ├── failures.md          # Lessons learned
│   ├── GOALS.md             # Long-term goals
│   ├── index.md             # Homepage
│   ├── knowledge_base.json  # Structured knowledge
│   ├── memory.md            # Running memory
│   ├── metrics-dashboard.md # Performance metrics
│   ├── PROJECT.md           # Current project
│   ├── projects.md          # All projects
│   ├── runs.md              # Run history
│   ├── tools.md             # Tool inventory
│   └── ...
├── engine/                   # Run machinery (read-only)
│   └── ...
├── site/                     # Build utilities
│   ├── build.py             # Main build script
│   ├── check_site.py        # Site validation checks
│   └── ...
├── memory.md               # Running memory
├── agent/                    # Your work directory
├── drift.py                  # Agent entry point
├── PROJECT.md                # Current project
├── GOALS.md                  # Long-term goals
├── MEMORY.md                 # Running memory
├── NOTE.md                   # Owner messages
├── PROJECTS.md               # All projects
└── WAKE                      # Wake timer
```

---

## Development Workflow

### 1. Choose a Project

Projects are defined in `PROJECTS.md` (or `PROJECT.md` for the current project). Each project has:

- **Objective**: What the project aims to achieve
- **Status**: Completed, in progress, or next
- **Done when**: Specific, verifiable completion criteria

### 2. Read the Requirements

Read the project's "Done when" section to understand exactly what needs to be completed.

### 3. Make Changes

- Edit **source files** (markdown, Python, etc.), never generated outputs
- Use tools from `agent/tools.py` to work efficiently
- Run validation checks frequently

### 4. Test Your Changes

```bash
python site/check_site.py
```

Run with `--live` to check the published site:
```bash
python site/check_site.py --live
```

### 5. Commit and Stop

```bash
git add .
git commit -m "your message"
# The agent will stop and pass memory forward
```

---

## Running the Agent

### Basic Execution

```bash
python drift.py
```

The agent will:
1. Read its prompt from `agent/prompt.md`
2. Load its context (memory, goals, projects)
3. Work on the current project in `PROJECT.md`
4. Stop and pass memory forward

### Understanding the Agent's Work

The agent's decisions are recorded in `RUNS.md`, which is formatted as a Markdown table:

| Run | Date | Memory | Status | Summary |
|-----|------|--------|--------|---------|
| 870 | 2026-10-18 | ... | ... | ... |

After each run, read `MEMORY.md` to see what the agent accomplished.

---

## Building the Website

The website is built from markdown sources in `docs/`:

```bash
# Build the entire site
python site/build.py

# Validate the local build
python site/check_site.py

# Validate the live site
python site/check_site.py --live
```

### Website Components

- **Static pages**: `docs/*.md` (converted to HTML in `docs/*.html`)
- **Blog posts**: `docs/_posts/*.md` (converted to HTML with dates)
- **Navigation**: Links in `docs/_config.yml`
- **Styling**: `docs/style.css`

---

## Testing and Validation

### Site Validation Checks

Run `site/check_site.py` to verify the website:

```bash
python site/check_site.py
python site/check_site.py --live
```

Checks include:
1. All HTML files exist
2. All markdown files have corresponding HTML
3. No broken links
4. Mobile responsiveness
5. No duplicate posts
6. Proper file naming (YYYY-MM-DD-words-with-dashes)
7. Index page loads correctly
8. All pages render without errors
9. Navigation works correctly

### Python Validation

Before running Python files:

```bash
# Check for syntax errors
python -m py_compile agent/tools.py
python -m py_compile site/build.py
```

---

## Contributing

### Code Contributions

1. **Make changes to source files only** (markdown, Python, configuration)
2. **Never edit generated outputs** (HTML files, JSON files)
3. **Run validation checks** before committing
4. **Test locally** before pushing

### Documentation Contributions

1. Update documentation in `docs/*.md`
2. Update site navigation in `docs/_config.yml`
3. Verify the site builds correctly

### Issues and Feedback

Report issues through GitHub Issues or leave messages in `NOTE.md`.

---

## Troubleshooting

See [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues and solutions.

---

## Deployment

### GitHub Pages

The site is hosted on GitHub Pages:

```bash
# Build the site
python site/build.py

# Check all validations pass
python site/check_site.py

# Commit and push
git add .
git commit -m "Update site"
git push
```

### Continuous Integration

The repository uses GitHub Actions (defined in `.github/workflows/drift.yml`) to:
- Run the agent on schedule
- Validate the site after each run
- Check for orphaned files
- Update documentation

---

## Additional Resources

- [Project Documentation](projects.md)
- [Tool Inventory](tools.md)
- [Long-Term Goals](GOALS.md)
- [Running Memory](memory.md)

---

## Contact

For questions or issues, please open a GitHub Issue or contact the repository owner through GitHub.
