#!/usr/bin/env python3
"""
Automated Insights Extraction from RUNS.md

Parses RUNS.md table format and extracts key insights:
- Error patterns and failures
- Tool fixes and discoveries
- Platform insights and API capabilities
- Long-term discoveries and learnings

Output:
- Extracted insights with confidence scores
- Knowledge base entries
- Visualizations
"""

import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from collections import defaultdict
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not installed. Visualizations will be skipped.")


class RUNSInsightExtractor:
    """Extract and categorize insights from RUNS.md"""

    def __init__(self, runs_path: str = "RUNS.md"):
        self.runs_path = Path(runs_path)
        self.runs = []
        self.insights = []
        self.patterns = {
            "tool_fix": [
                r"Fixed.*tool",
                r"Tool.*fix",
                r"Deleted.*tool",
                r"Removed.*tool",
                r"Implemented.*tool",
                r"Added.*tool",
                r"Improved.*tool",
            ],
            "platform": [
                r"Platform",
                r"API",
                r"GitHub",
                r"z\.ai",
                r"glm-",
            ],
            "research": [
                r"Research",
                r"studied",
                r"investigated",
                r"analyzed",
                r"discovered",
            ],
            "discovery": [
                r"Found",
                r"Discovered",
                r"Note:",
                r"Key insight",
                r"important",
            ],
            "error": [
                r"api_error",
                r"crashed",
                r"error",
                r"bug",
                r"problem",
                r"fail",
                r"failed",
            ],
        }

    def parse_runs(self) -> List[Dict[str, Any]]:
        """Parse RUNS.md table into structured data"""
        with open(self.runs_path, "r") as f:
            content = f.read()

        # Find all table rows (content rows, not header)
        table_rows = re.findall(r"\|([^|]+)\|", content)

        # Skip header row (first match)
        if len(table_rows) < 6:
            raise ValueError("Could not find RUNS.md table")

        table_rows = table_rows[1:]

        for row in table_rows:
            row = row.strip()
            if not row or "|" not in row:
                continue

            # Parse columns
            cols = [col.strip() for col in row.split("|")]
            if len(cols) < 6:
                continue

            try:
                run_num = int(cols[0])
                timestamp_str = cols[1]
                outcome = cols[2]
                turns = int(cols[3])
                tokens = int(cols[4].replace(",", ""))
                note = cols[5] if len(cols) > 5 else ""

                self.runs.append({
                    "run": run_num,
                    "timestamp": self._parse_timestamp(timestamp_str),
                    "outcome": outcome,
                    "turns": turns,
                    "tokens": tokens,
                    "note": note,
                })
            except (ValueError, IndexError):
                continue

        return self.runs

    def _parse_timestamp(self, ts_str: str) -> datetime:
        """Parse UTC timestamp string"""
        # Handle "2026-09-06 20:39" format
        match = re.match(r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})", ts_str)
        if match:
            return datetime.strptime(f"{match.group(1)} {match.group(2)}", "%Y-%m-%d %H:%M")
        return datetime.now()

    def categorize_note(self, note: str) -> List[str]:
        """Categorize a note based on patterns"""
        categories = []

        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, note, re.IGNORECASE):
                    categories.append(category)
                    break

        return categories

    def extract_insights(self) -> List[Dict[str, Any]]:
        """Extract insights from all runs"""
        for run in self.runs:
            if not run["note"] or run["note"] == "(no note)":
                continue

            categories = self.categorize_note(run["note"])

            insight = {
                "run": run["run"],
                "timestamp": run["timestamp"],
                "outcome": run["outcome"],
                "turns": run["turns"],
                "tokens": run["tokens"],
                "note": run["note"],
                "categories": categories,
                "confidence": self._calculate_confidence(run["note"], categories),
            }

            self.insights.append(insight)

        return self.insights

    def _calculate_confidence(self, note: str, categories: List[str]) -> float:
        """Calculate confidence score for an insight"""
        base_score = 0.5

        # Increase score if multiple categories match
        base_score += min(len(categories) * 0.1, 0.4)

        # Increase score if note contains keywords
        keywords = ["fix", "implement", "complete", "discovered", "found", "note:"]
        keyword_count = sum(1 for kw in keywords if kw.lower() in note.lower())
        base_score += min(keyword_count * 0.1, 0.1)

        return round(base_score, 2)

    def generate_insights_report(self) -> str:
        """Generate human-readable insights report"""
        report = []

        for insight in self.insights:
            categories_str = ", ".join(insight["categories"]) or "none"
            report.append(
                f"Run {insight['run']} ({insight['timestamp']}): "
                f"[{categories_str}] {insight['note']}"
            )

        return "\n".join(report)

    def generate_knowledge_entries(self) -> List[Dict[str, Any]]:
        """Generate knowledge base entries"""
        entries = []

        for insight in self.insights:
            entry = {
                "title": self._generate_title(insight),
                "description": insight["note"][:200],
                "type": "discovery",
                "tags": ",".join(insight["categories"]),
                "source": f"Run {insight['run']}",
                "timestamp": insight["timestamp"].isoformat(),
                "tokens": insight["tokens"],
                "confidence": insight["confidence"],
                "implementation": self._get_implementation(insight),
                "verification": "Verified from RUNS.md",
                "impact": self._get_impact(insight),
            }
            entries.append(entry)

        return entries

    def _generate_title(self, insight: Dict) -> str:
        """Generate a title for the insight"""
        note = insight["note"]

        # Try to find a clear title
        title_match = re.search(
            r"^(Fixed|Implemented|Added|Removed|Completed|Discovered|Found|Created):(.*)$",
            note,
            re.IGNORECASE
        )

        if title_match:
            return title_match.group(1).capitalize() + ": " + title_match.group(2).strip()
        elif insight["categories"]:
            return f"Insight from Run {insight['run']}: {note[:50]}"
        else:
            return f"Run {insight['run']} note"

    def _get_implementation(self, insight: Dict) -> str:
        """Generate implementation details"""
        note = insight["note"]
        categories = insight["categories"]

        if "tool_fix" in categories:
            return "Modified agent/tools.py to fix bugs, add features, or remove duplicate methods"
        elif "platform" in categories:
            return "Updated platform configuration or API integration"
        elif "research" in categories:
            return "Conducted research and analysis on LLM agents, tools, or platforms"
        elif "error" in categories:
            return "Identified and addressed errors, crashes, or API failures"
        else:
            return "Discovered through run execution and documentation"

    def _get_impact(self, insight: Dict) -> str:
        """Generate impact description"""
        categories = insight["categories"]

        if "tool_fix" in categories:
            return "Improved tool functionality and reliability"
        elif "platform" in categories:
            return "Enhanced platform integration and capabilities"
        elif "research" in categories:
            return "Provided insights for future work and improvements"
        elif "error" in categories:
            return "Reduced errors and improved system stability"
        else:
            return "Contributes to ongoing improvement and documentation"

    def generate_visualizations(self):
        """Generate visualizations of the insights"""
        if not self.insights:
            print("No insights to visualize")
            return

        if not HAS_MATPLOTLIB:
            print("Skipping visualizations (matplotlib not installed)")
            return

        # Create output directory
        output_dir = Path("docs/insights")
        output_dir.mkdir(exist_ok=True)

        # 1. Token usage over time
        self._plot_tokens_over_time(output_dir)

        # 2. Insights by category
        self._plot_category_distribution(output_dir)

        # 3. Insights per run
        self._plot_insights_per_run(output_dir)

        # 4. Outcome distribution
        self._plot_outcome_distribution(output_dir)

        print(f"Visualizations saved to {output_dir}")

    def _plot_tokens_over_time(self, output_dir: Path):
        """Plot token usage over time"""
        insights_by_run = {i["run"]: i for i in self.insights}
        runs_data = sorted(insights_by_run.values(), key=lambda x: x["timestamp"])

        if len(runs_data) < 2:
            return

        dates = [i["timestamp"] for i in runs_data]
        tokens = [i["tokens"] for i in runs_data]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, tokens, marker='o', linewidth=2, markersize=4)

        ax.set_title("Token Usage Over Time", fontsize=14)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Tokens", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        plt.tight_layout()
        plt.savefig(output_dir / "tokens_over_time.png", dpi=150, bbox_inches='tight')
        plt.close()

    def _plot_category_distribution(self, output_dir: Path):
        """Plot distribution of insight categories"""
        category_counts = defaultdict(int)

        for insight in self.insights:
            for category in insight["categories"]:
                category_counts[category] += 1

        if not category_counts:
            return

        categories = list(category_counts.keys())
        counts = list(category_counts.values())

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(categories, counts, color='steelblue')

        ax.set_title("Insights by Category", fontsize=14)
        ax.set_xlabel("Category", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                   f'{int(height)}',
                   ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(output_dir / "category_distribution.png", dpi=150, bbox_inches='tight')
        plt.close()

    def _plot_insights_per_run(self, output_dir: Path):
        """Plot insights per run"""
        run_insights = defaultdict(list)

        for insight in self.insights:
            run_insights[insight["run"]].append(insight)

        runs = sorted(run_insights.keys())
        counts = [len(run_insights[r]) for r in runs]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(runs, counts, color='coral', alpha=0.7)

        ax.set_title("Insights Per Run", fontsize=14)
        ax.set_xlabel("Run Number", fontsize=12)
        ax.set_ylabel("Number of Insights", fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig(output_dir / "insights_per_run.png", dpi=150, bbox_inches='tight')
        plt.close()

    def _plot_outcome_distribution(self, output_dir: Path):
        """Plot distribution of outcomes"""
        outcome_counts = defaultdict(int)

        for insight in self.insights:
            outcome_counts[insight["outcome"]] += 1

        outcomes = list(outcome_counts.keys())
        counts = list(outcome_counts.values())

        colors = {
            "stopped": "green",
            "api_error": "red",
            "crashed": "darkred",
            "out_of_turns": "orange",
            "out_of_time": "orange",
        }

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(outcomes, counts,
                     color=[colors.get(o, 'gray') for o in outcomes])

        ax.set_title("Insights by Outcome", fontsize=14)
        ax.set_xlabel("Outcome", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig(output_dir / "outcome_distribution.png", dpi=150, bbox_inches='tight')
        plt.close()


def main():
    """Main entry point"""
    print("=" * 60)
    print("Automated Insights Extraction from RUNS.md")
    print("=" * 60)

    # Initialize extractor
    extractor = RUNSInsightExtractor()

    # Parse RUNS.md
    print("\nParsing RUNS.md...")
    extractor.parse_runs()
    print(f"✓ Parsed {len(extractor.runs)} runs")

    # Extract insights
    print("\nExtracting insights...")
    extractor.extract_insights()
    print(f"✓ Extracted {len(extractor.insights)} insights")

    # Print summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total runs: {len(extractor.runs)}")
    print(f"Total insights: {len(extractor.insights)}")

    category_counts = defaultdict(int)
    for insight in extractor.insights:
        for category in insight["categories"]:
            category_counts[category] += 1

    print("\nInsights by category:")
    for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {category}: {count}")

    outcome_counts = defaultdict(int)
    for insight in extractor.insights:
        outcome_counts[insight["outcome"]] += 1

    print("\nInsights by outcome:")
    for outcome, count in sorted(outcome_counts.items(), key=lambda x: -x[1]):
        print(f"  {outcome}: {count}")

    # Generate report
    print("\n" + "=" * 60)
    print("SAMPLE INSIGHTS")
    print("=" * 60)
    for i, insight in enumerate(extractor.insights[:10], 1):
        categories = ", ".join(insight["categories"]) or "none"
        print(f"\n{i}. Run {insight['run']} [{categories}]")
        print(f"   {insight['note'][:100]}...")

    # Generate knowledge entries
    print("\n" + "=" * 60)
    print("GENERATING KNOWLEDGE BASE ENTRIES")
    print("=" * 60)

    entries = extractor.generate_knowledge_entries()
    print(f"✓ Generated {len(entries)} knowledge entries")

    # Save to JSON
    output_file = Path("docs/insights/extracted_insights.json")
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w") as f:
        json.dump({
            "metadata": {
                "total_runs": len(extractor.runs),
                "total_insights": len(extractor.insights),
                "extraction_date": datetime.now().isoformat(),
            },
            "insights": entries,
        }, f, indent=2)

    print(f"✓ Saved to {output_file}")

    # Generate visualizations
    print("\nGenerating visualizations...")
    extractor.generate_visualizations()

    # Save insights report
    report_file = Path("docs/insights/insights_report.txt")
    report_file.parent.mkdir(exist_ok=True)

    with open(report_file, "w") as f:
        f.write(extractor.generate_insights_report())

    print(f"✓ Saved insights report to {report_file}")

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
