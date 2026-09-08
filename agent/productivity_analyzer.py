import os
from analyze_runs import analyze_runs

class ProductivityAnalyzer:
    """Tool to analyze the agent's productivity and failure patterns from RUNS.md."""
    
    def _analyze_productivity(self):
        """Analyze RUNS.md and return a summary of productivity and failures."""
        return analyze_runs()

def register_tools(tools_class):
    # This is a placeholder; the actual registration happens by adding methods to agent/tools.py
    pass
