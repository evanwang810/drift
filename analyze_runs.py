import re
from pathlib import Path

def analyze_runs():
    """Analyze RUNS.md and return a summary of productivity and failures."""
    runs_file = Path("RUNS.md")
    if not runs_file.exists():
        return "RUNS.md not found."

    content = runs_file.read_text(encoding="utf-8")
    
    # Find the table header and data
    lines = content.split('\n')
    table_started = False
    runs_data = []
    
    for line in lines:
        if '| run | when (UTC) | outcome |' in line:
            table_started = True
            continue
        if table_started and line.startswith('|') and '---' not in line:
            # Split by | and remove empty first/last elements
            cols = [c.strip() for c in line.split('|') if c.strip()]
            if len(cols) >= 3:
                runs_data.append(cols)

    total_runs = len(runs_data)
    if total_runs == 0:
        return "No runs found in RUNS.md."

    status_counts = {}
    for run in runs_data:
        status = run[2]
        status_counts[status] = status_counts.get(status, 0) + 1

    summary = f"Analysis of {total_runs} runs:\n"
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        summary += f"- {status}: {count}\n"

    failures = status_counts.get("api_error", 0) + status_counts.get("crashed", 0)
    failure_rate = (failures / total_runs) * 100 if total_runs > 0 else 0
    summary += f"\nFailure rate: {failure_rate:.1f}%"

    return summary
