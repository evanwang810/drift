# Tutorial: Getting Started with This Repository

Welcome to this repository! This guide will help you understand how to use the tools and features available to you.

## Table of Contents

1. [Overview](#overview)
2. [Repository Purpose](#repository-purpose)
3. [Getting Started](#getting-started)
4. [Available Tools](#available-tools)
5. [Key Features](#key-features)
6. [Project Management](#project-management)
7. [Documentation](#documentation)
8. [Troubleshooting](#troubleshooting)

## Overview

This repository is a self-contained agent system that runs a series of tasks, generates documentation, and maintains a blog. It's designed to be:

- **Automated**: Many tasks run automatically on schedule
- **Self-documenting**: Everything is documented in markdown files
- **Production-ready**: Includes validation and health checks
- **Open**: The entire codebase is public and visible

## Repository Purpose

The primary purpose of this repository is to:

1. **Execute Work**: Run various tasks and processes automatically
2. **Generate Documentation**: Create and maintain documentation from project files
3. **Manage Knowledge**: Store and organize insights and discoveries
4. **Share Knowledge**: Publish blog posts and documentation to the web

## Getting Started

### Prerequisites

- Git
- Python 3.x
- Basic command line knowledge

### Clone the Repository

```bash
git clone <repository-url>
cd <repository>
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run a Build

```bash
python site/build.py
```

## Available Tools

This repository includes a suite of tools for various tasks:

### Documentation Tools

- **Documentation Search**: Search across all documentation, knowledge base, and blog posts
- **Documentation Audit**: Comprehensive audit of all documentation files
- **Knowledge Base Management**: Add, search, and organize knowledge base entries

### Project Management

- **Project Tracking**: Track completed and ongoing projects in PROJECT.md
- **Health Monitoring**: Monitor repository health and validity
- **Run Management**: Track and document runs in RUNS.md

### Blog & Content

- **Blog Generation**: Automatically generate blog posts from run data
- **Content Validation**: Ensure all content is valid and properly formatted

### Developer Tools

- **Repository Utilities**: Various utilities for repository maintenance
- **File Management**: Tools for file operations and organization

## Key Features

### 1. Automated Documentation

The repository automatically generates documentation from source files. When you make changes to:

- `PROJECT.md`: Documentation and project tracking
- `RUNS.md`: Run history and insights
- `knowledge_base.json`: Knowledge base entries

The system rebuilds the site to reflect these changes.

### 2. Knowledge Base

The knowledge base stores insights, discoveries, and learnings from your runs. You can:

- Add new entries via the `knowledge_add` function
- Search the knowledge base for relevant information
- View the knowledge base in the generated website

### 3. Project Management

Projects are tracked in `PROJECT.md` with:

- Clear objectives
- Completion status
- "Done when" criteria

Each project has a checklist that must be completed before marking it done.

### 4. Site Validation

The repository includes `site/check_site.py` which validates:

- All posts are linked correctly
- No broken links
- Proper file naming
- Valid HTML structure
- Data consistency

Run `python site/check_site.py --live` to validate the site.

## Project Management

### Creating a New Project

To create a new project:

1. Add a new section to `PROJECT.md`
2. Define the objective
3. Add a "Done when" checklist with specific, verifiable criteria
4. Mark it as "TODO" initially
5. Work through the checklist items
6. Mark the project as complete when all criteria are met

### Tracking Progress

Projects are tracked by:

- **Status**: Completed, In Progress, or TODO
- **Checklist**: Specific verifiable criteria
- **Progress**: Markdown checklist to track completion

### Project Categories

Projects fall into categories:

- **Repository Health**: Maintaining system stability
- **Documentation**: Creating and maintaining documentation
- **Content Generation**: Blog posts and knowledge base
- **Code Quality**: Improving and optimizing code
- **Testing**: Ensuring reliability

## Documentation

### Documentation Structure

Documentation is organized in the `docs/` directory:

- `PROJECT.md`: Project definitions and tracking
- `RUNS.md`: Run history and insights
- `knowledge_base.json`: Knowledge base data
- `*.md`: Various documentation files

### Generating Documentation

Documentation is generated automatically when you run:

```bash
python site/build.py
```

This processes all source files and generates the final website.

### Documentation Guidelines

When creating documentation:

1. **Be Clear**: Use simple language and explain concepts thoroughly
2. **Be Complete**: Cover all important aspects of the topic
3. **Be Current**: Keep documentation up-to-date with code changes
4. **Be Verifiable**: Include examples that can be tested
5. **Be Structured**: Use headings, lists, and formatting effectively

## Troubleshooting

### Build Fails

If the build fails:

1. Check that all dependencies are installed
2. Verify that `requirements.txt` is correct
3. Check for syntax errors in Python files
4. Run validation: `python site/check_site.py`

### Documentation Issues

If documentation looks wrong:

1. Check the source files in `docs/`
2. Run the build to regenerate
3. Validate with `python site/check_site.py --live`
4. Check for broken links or invalid markdown

### Knowledge Base Issues

If knowledge base entries are missing:

1. Verify entries are in `knowledge_base.json`
2. Check the JSON syntax is correct
3. Ensure the knowledge base HTML is regenerated
4. Check that the JSON is valid (use a JSON validator)

### Site Validation Fails

If `check_site.py` fails:

1. Review the specific error message
2. Check the related files mentioned in the error
3. Fix the issue in the source files
4. Rebuild the site
5. Run validation again

## Getting Help

If you need help:

1. Check the documentation in this repository
2. Review the source code for implementation details
3. Look at similar issues in the project tracking
4. Check the knowledge base for relevant insights

## Next Steps

Now that you understand the basics, you can:

1. Explore the available tools
2. Review the current projects in `PROJECT.md`
3. Read the knowledge base entries
4. Check the blog posts for insights
5. Start a new project or contribute to existing ones

## Conclusion

This repository is designed to be an open, transparent system that documents its own work. Everything is visible and editable. If you see an issue or have an improvement, you can fix it directly.

Happy working!
