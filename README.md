# Drift Agent

An autonomous AI agent that wakes up in its own git repository, works for a while, and then stops. Built for experimentation with autonomous AI behavior and tool usage patterns.

## What is Drift?

Drift is a research project exploring how AI agents can:
- Work autonomously in their own repository
- Use tools to read files, run commands, and interact with external systems
- Make decisions about what to work on
- Leave a record of what they've done

The agent runs in cycles, wakes up, works on tasks, and then stops, passing its memory forward for the next run.

## Structure

```
drift/
├── agent/           # The agent's code and tools
├── docs/            # Documentation
├── engine/          # The machinery that runs the agent
├── notes/           # Running notes
└── PROJECT.md       # Current project being worked on
```

## Tools

Drift has 25 tools available for use:

### Core Tools
- `_read` - Read files (with binary detection)
- `_write` - Write files entirely
- `_replace` - Replace text in files
- `_replace_all` - Replace all occurrences
- `_delete` - Delete files
- `_ls` - List files in a directory
- `_tree` - Show directory tree structure
- `_grep` - Search for patterns in files

### System Tools
- `_run` - Run shell commands
- `_validate_python` - Check Python syntax
- `_search` - Search the web (DuckDuckGo + Wikipedia fallback)
- `_search_wikipedia` - Wikipedia API search helper
- `_web_fetch` - Fetch content from URLs

### GitHub Tools (require GH_TOKEN and git CLI)
- `_gh_list_issues` - List open/closed issues
- `_gh_read_issue` - Read an issue with comments
- `_gh_comment_issue` - Comment on an issue
- `_gh_close_issue` - Close an issue

### Memory Tools
- `_analyze_runs` - Analyze RUNS.md for productivity and failures
- `_summarize` - Replace all work done so far with a summary
- `_stop` - End the run (with memory)

## Getting Started

### Prerequisites

- Python 3.10+
- A GitHub Personal Access Token with repo scope (for GitHub tools)
- Git CLI installed
- DuckDuckGo access (for web search, with Wikipedia fallback)

### Running Drift

1. Clone the repository:
```bash
git clone https://github.com/evanwang810/drift.git
cd drift
```

2. Set up environment variables:
```bash
export GH_TOKEN=your_github_token_here
```

3. Run the agent:
```bash
python drift.py
```

The agent will wake up, read its context, work on the project defined in `PROJECT.md`, and then stop.

## Documentation

- `PROJECT.md` - Current project and progress
- `GOALS.md` - Long-term goals for the project
- `MEMORY.md` - Running memory (last few runs)
- `NOTE.md` - Owner messages and notes
- `docs/world_knowledge/` - Research and world knowledge
- `docs/_posts/` - Blog posts about the project (13 posts about tool TESTing, search improvements, and agent behavior)

## Running Notes

Running notes are stored in `notes/` directory, tracking each run's progress and decisions.

## License

See LICENSE file (if applicable)
