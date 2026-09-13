# Perception Tools

These tools help the agent analyze its own context, directory structures, and identify patterns in its operations.

## Overview

Perception tools enhance self-awareness by providing the agent with:
- Directory structure summaries
- Context analysis of current operations
- Pattern detection across files

## Available Tools

### `_summarize_directory`

Recursively analyzes a directory structure and provides statistics about files, directories, and file types.

**Parameters:**
- `path` (str, optional): Directory path to analyze. Default: "."
- `depth` (int, optional): Maximum directory depth to explore. Default: 3
- `max_files` (int, optional): Maximum number of files to include in summary. Default: 50

**Returns:** A markdown-formatted summary with file distribution, directory structure, and quick stats.

**Example Usage:**
```
_summarize_directory(path="agent", depth=2, max_files=30)
```

**Use Cases:**
- Understanding project structure
- Analyzing file type distribution
- Identifying large directories or files
- Quick project overview

---

### `_analyze_context`

Provides a holistic view of the current run and agent state.

**Parameters:** None

**Returns:** A comprehensive context summary including:
- Current run information
- Recent actions taken
- Memory context (last 3 runs)
- Project status
- Agent capabilities

**Example Usage:**
```
_analyze_context()
```

**Use Cases:**
- Understanding what the agent has been doing
- Reviewing recent actions and decisions
- Checking memory and project context
- Assessing agent capabilities

---

### `_track_patterns`

Identifies recurring patterns in logs or operations by searching for a specific pattern across files.

**Parameters:**
- `pattern` (str): Pattern to search for (supports regex)
- `path` (str, optional): Directory to search. Default: "."
- `max_matches` (int, optional): Maximum number of matches to report. Default: 20

**Returns:** A summary of pattern matches with context, frequency, and distribution by file.

**Example Usage:**
```
_track_patterns(pattern="error", max_matches=15)
```

**Use Cases:**
- Finding recurring errors in logs
- Identifying common patterns in code
- Analyzing documentation structure
- Detecting patterns in agent actions
- Investigating recurring issues

---

## Integration

These tools are automatically available to the agent through the standard tool dispatch mechanism. The agent can call them directly in any turn.

**Workflow Integration:**
1. After completing a significant task, use `_analyze_context()` to review progress
2. Before starting a new project, use `_summarize_directory()` to understand the codebase
3. When investigating recurring issues, use `_track_patterns()` to find related occurrences

**Example Workflow:**
```
# After finishing a task
_summarize_directory(path="docs")  # Review documentation structure
_analyze_context()  # Check recent actions and memory
```

---

## Benefits

**Self-Awareness:** The agent gains better understanding of its own operations and context.

**Decision Making:** Better context leads to more informed decisions about what to work on next.

**Progress Tracking:** Tools help the agent understand its progress over time.

**Issue Detection:** Pattern detection helps identify recurring problems or patterns in code/logs.

**Resource Optimization:** Directory summaries help identify large files or directories that might need attention.
