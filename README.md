# AI Agent Repository

An autonomous git repository agent that wakes up, works on tasks, and sleeps. Built to demonstrate continuous improvement, self-documentation, and automated project management.

## What This Is

This repository contains:
- **An autonomous agent** that runs periodic checks, maintains the codebase, and works on projects
- **A fully functional website** built with Jekyll that documents the agent's activities, knowledge base, and project progress
- **Comprehensive tooling** for knowledge management, documentation, and automated workflows

## Repository Structure

```
├── agent/                    # The agent itself
│   ├── tools.py             # Available tools and their implementations
│   ├── context.py           # Context management and configuration
│   └── prompt.md            # Agent prompt and behavior instructions
├── docs/                     # Static documentation
│   ├── posts/               # Blog posts and articles
│   ├── knowledge_base.json  # Knowledge base entries
│   └── *.md                 # Documentation files
├── site/                     # Site generation
│   ├── build.py             # Main build script
│   ├── check_site.py        # Site validation checks
│   ├── generate_*.py        # Site generation modules
│   └── templates/           # Jekyll templates
├── engine/                   # Core agent machinery (read-only)
├── notes/                    # Personal notes and scratchpad
└── README.md                 # This file
```

## Available Tools

The agent has access to [25 tools](docs/tools.md) for repository management, documentation, and knowledge work:

- **Documentation**: `generate_docs`, `generate_blog_post`, `create_blog_posts_from_runs`
- **Knowledge Management**: `knowledge_add`, `knowledge_search`, `knowledge_list`
- **Site Building**: `run` (site/build.py), `validate_python`, `read`, `write`
- **Search & Research**: `search`, `knowledge_aware_search`, `search_wikipedia`
- **Project Management**: `gh_create_issue_from_project`, `gh_list_issues`, `gh_read_issue`
- **Analysis**: `analyze_runs`, `extract_run_insights`, `generate_knowledge_report`

## Setup & Usage

### Getting Started

A comprehensive guide to setting up and using the repository is available in [docs/getting-started.md](docs/getting-started.md), which covers:
- Installation and setup requirements
- Building the site locally
- Running health checks
- Common workflows and use cases
- Troubleshooting tips

### Building the Site

```bash
cd site
python build.py
```

The build script generates all HTML files from the source markdown, knowledge base entries, and configuration data.

### Running Checks

Verify the site is working correctly:

```bash
python check_site.py --live
```

This runs 12 validation checks covering posts, links, performance, and data integrity.

### Working on a Project

1. **Pick a project** from `PROJECT.md` with a clear "Done when" checklist
2. **Make changes** to source files (never edit generated HTML directly)
3. **Test the change** by running the appropriate check or build script
4. **Verify with check_site.py** to ensure nothing is broken
5. **Stop the run** with a clear memory of what was accomplished

## Current Status

All projects in PROJECT.md are complete:
- ✅ Repository Health Monitoring and Automation
- ✅ Comprehensive Test Suite and Coverage
- ✅ Metrics Dashboard
- ✅ Project Documentation
- ✅ Documentation Search
- ✅ Tool Inventory Review
- ✅ Documentation Audit
- ✅ Clean Up Documentation Issues
- ✅ Knowledge Base Refinement
- ✅ Knowledge Base Organization
- ✅ Site Performance Optimization
- ✅ Automated Insights Extraction
- ✅ Clean Up Blog and Site Folder
- ✅ Fix Tool Inventory Duplication
- ✅ Repository Health Check
- ✅ Code Quality Optimization
- ✅ Complete Documentation and Test Site
- ✅ Comprehensive Site Testing and Validation
- ✅ Improve RUNS.md Validation
- ✅ Security Audit and Hardening
- ✅ PROJECT.md Cleanup
- ✅ Clean Up agent/tools.py
- ✅ Remove Duplicate Blog Posts
- ✅ Consolidate Navigation Links
- ✅ Remove Unused Blog Reports
- ✅ Create Meaningful Blog Content
- ✅ Fix Navigation Hardcoding

## History & Documentation

- **RUNS.md**: Complete run history with timestamps, token usage, and outcomes
- **docs/posts/**: 12 substantive blog posts about development work, tooling, and discoveries
- **docs/knowledge_base.json**: Organized knowledge base with tags, types, and source attribution
- **MEMORY.md**: Long-term memory of discoveries and patterns learned across runs

## Agent Behavior

This agent:
- Wakes up periodically (configurable via `WAKE`)
- Works autonomously on projects from PROJECT.md
- Makes changes only when they improve the system
- Maintains documentation as it works
- Stops when tasks are complete or out of turns

## License

This is a personal project repository. No specific license is applied.

## Links

- **Website**: [docs/posts/](docs/posts/)
- **Documentation**: [docs/](docs/)
- **Project Status**: [PROJECT.md](PROJECT.md)
- **Tool List**: [docs/tools.md](docs/tools.md)
- **Knowledge Base**: [docs/knowledge_base.html](docs/knowledge_base.html)
- **Run History**: [runs.html](runs.html)
