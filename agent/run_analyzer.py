import ast
from pathlib import Path
from collections import Counter
import re

class RunAnalyzer:
    """Analyzes RUNS.md to summarize productivity and failures."""
    
    def __init__(self, runs_path: Path):
        self.runs_path = runs_path

    def analyze(self) -> str:
        if not self.runs_path.exists():
            return "RUNS.md not found."
        
        content = self.runs_path.read_text(encoding="utf-8")
        runs = re.split(r"\n## run \d+", content)
        # The first element is usually empty or header
        runs = [r for r in runs if r.strip()]
        
        if not runs:
            return "No runs found in RUNS.md."
        
        total_runs = len(runs)
        stopped_runs = content.count("| stopped")
        api_error_runs = content.count("| api_error")
        
        # Look for common failure patterns or keywords in the summaries
        failures = []
        for run in runs:
            if "error" in run.lower() or "fail" in run.lower():
                # Extract a snippet of the failure
                match = re.search(r"([^.\n]* (?:error|fail|refused)[^.\n]*\.)", run, re.IGNORECASE)
                if match:
                    failures.append(match.group(1).strip())
        
        common_failures = Counter(failures).most_common(5)
        
        summary = [
            f"Analysis of {total_runs} runs:",
            f"- Stopped normally: {stopped_runs}",
            f"- API Errors: {api_error_runs}",
            f"- Success Rate (Normal Stop): {(stopped_runs/total_runs)*100:.1f}%",
            "\nCommon Failure Snippets:",
        ]
        
        for fail, count in common_failures:
            summary.append(f"- ({count}x) {fail}")
            
        if not common_failures:
            summary.append("- No frequent failure patterns identified.")
            
        return "\n".join(summary)
