# Perception Tools

Perception tools help the agent analyze itself, understand its operations, and make better decisions. These tools are designed to provide self-awareness and enable sophisticated analysis of the agent's own state and patterns.

## Tools

### `_summarize_directory`

Recursively analyzes a directory structure and provides a concise overview.

**Purpose:**
- Understand the contents of large directories
- Get a quick summary of file types and structure
- Identify key files and their sizes

**Parameters:**
- `path` (optional): Directory path to analyze (defaults to current directory)

**Returns:**
A summary string containing:
- Total number of files and directories
- Nested structure overview
- Key file types and sizes

**Example Usage:**
```
_summarize_directory("agent/")
# Summary: Found 10 files in 2 directories, nested structure, main file types are Python and Markdown
```

**Use Cases:**
- Understanding project structure
- Analyzing large directories before operations
- Identifying file distribution and organization

---

### `_analyze_context`

Provides a holistic view of the current run and agent state.

**Purpose:**
- Understand recent run history
- Track productivity metrics
- Identify error patterns
- Monitor progress over time

**Parameters:**
- `n` (optional): Number of recent runs to analyze (defaults to 5)

**Returns:**
A comprehensive analysis containing:
- Run history summary (total runs, success rate, failed runs)
- Recent run details
- Top 3 most common error patterns
- Longest consecutive successful run streak
- Agent's current state and progress insights

**Example Usage:**
```
_analyze_context(n=10)
# Shows: 113 total runs, 95% success rate, top errors: "Connection timeout", "Rate limit exceeded"
```

**Use Cases:**
- Understanding own progress
- Identifying recurring issues
- Making decisions about what to work on
- Optimizing performance and resource usage

---

### `_track_patterns`

Identifies recurring patterns in logs or operations.

**Purpose:**
- Track most common commands and operations
- Identify frequent error types
- Monitor file operation patterns
- Discover usage trends

**Parameters:**
- `log_file` (optional): Path to log file to analyze (defaults to RUNS.md)
- `limit` (optional): Number of patterns to track (defaults to 10)

**Returns:**
A pattern analysis containing:
- Most common commands
- Frequent error types
- Typical file operations
- Usage frequency and insights

**Example Usage:**
```
_track_patterns(log_file="RUNS.md", limit=15)
# Shows: Most common: "read_file", "write_file", "replace", error types: "FileNotFound"
```

**Use Cases:**
- Understanding operational patterns
- Identifying bottlenecks or frequent operations
- Improving workflow efficiency
- Detecting potential issues before they become problems

---

## Integration

These perception tools are integrated into the agent's workflow through the available tools. The agent can use them anytime during a run to:

1. **Before starting work:** Use `_summarize_directory` to understand the project structure
2. **During work:** Use `_analyze_context` to track progress and identify issues
3. **After work:** Use `_track_patterns` to understand what was done and improve efficiency

---

## Benefits

Perception tools provide the agent with:
- **Self-awareness:** Understanding its own state and progress
- **Better decision-making:** Data-driven choices about what to work on
- **Pattern recognition:** Identifying recurring issues and optimizing workflows
- **Resource optimization:** Understanding memory usage and tool effectiveness
- **Progress tracking:** Clear visibility into accomplishments and challenges

---

## Examples

### Example 1: Understanding Project Structure
```
_summarize_directory()
# Agent sees: 25 tools available, documentation in docs/, source in agent/, recent activity in RUNS.md
```

### Example 2: Analyzing Recent Performance
```
_analyze_context(n=20)
# Agent sees: 90% success rate over last 20 runs, most common error: rate limiting, longest streak: 7 runs
```

### Example 3: Tracking Tool Usage
```
_track_patterns(log_file="RUNS.md")
# Agent sees: Most used tool is _read (45%), followed by _write (30%), indicating heavy file manipulation
```

---

## Future Enhancements

Potential improvements to perception tools:
- Machine learning models to predict upcoming issues
- Automated pattern detection and alerting
- Visualization of progress and trends
- Resource usage optimization recommendations
- Collaborative analysis with human oversight
