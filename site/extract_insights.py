#!/usr/bin/env python3
"""
Automated Insights Extraction from RUNS.md

Extracts key insights, patterns, and discoveries from RUNS.md entries
and categorizes them for knowledge base integration and visualization.
"""

import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any


class InsightExtractor:
    """Extracts insights from RUNS.md entries."""

    def __init__(self, runs_path: str = "RUNS.md"):
        self.runs_path = Path(runs_path)
        self.runs = []
        self.insights = []
        self.categories = {
            "tool_fix": ["tool", "fix", "update", "improve", "enhance", "new", "added"],
            "platform": ["api", "github", "web", "site", "build", "deploy", "hosting"],
            "discovery": ["learned", "found", "noticed", "realized", "discovered"],
            "research": ["explore", "investigate", "analyze", "search"],
            "workflow": ["workflow", "process", "procedure", "method"],
            "error": ["error", "failed", "crash", "bug", "issue"],
        }

    def parse_runs(self) -> List[Dict[str, Any]]:
        """Parse RUNS.md and extract run data."""
        pattern = r'\| (\d+) \| (.*?) \| (.*?) \| (\d+) \| (\d+) \| (.+) \|'

        with open(self.runs_path, 'r') as f:
            content = f.read()

        # Find all run entries
        matches = re.finditer(pattern, content)

        for match in matches:
            run_num = int(match.group(1))
            when = match.group(2)
            outcome = match.group(3)
            turns = int(match.group(4))
            tokens = int(match.group(5))
            note = match.group(6).strip()

            # Parse date
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', when)
            date = date_match.group(1) if date_match else None

            self.runs.append({
                "run": run_num,
                "date": date,
                "when": when,
                "outcome": outcome,
                "turns": turns,
                "tokens": tokens,
                "note": note
            })

        return self.runs

    def categorize_insight(self, note: str) -> Dict[str, Any]:
        """Categorize an insight into types."""
        note_lower = note.lower()

        # Check each category
        for category, keywords in self.categories.items():
            if any(keyword in note_lower for keyword in keywords):
                return {
                    "type": category,
                    "keywords": keywords
                }

        return {
            "type": "general",
            "keywords": []
        }

    def extract_insights_from_runs(self) -> List[Dict[str, Any]]:
        """Extract insights from all runs."""
        if not self.runs:
            self.parse_runs()

        for run in self.runs:
            if run["note"] and run["note"] not in ["", "-", " "]:
                insight = {
                    "run": run["run"],
                    "date": run["date"],
                    "outcome": run["outcome"],
                    "note": run["note"],
                    "categorization": self.categorize_insight(run["note"])
                }
                self.insights.append(insight)

        return self.insights

    def generate_insight_summary(self) -> Dict[str, Any]:
        """Generate a summary of insights by category and date."""
        if not self.insights:
            self.extract_insights_from_runs()

        # Group by category
        by_category = defaultdict(list)
        for insight in self.insights:
            cat = insight["categorization"]["type"]
            by_category[cat].append(insight)

        # Group by date
        by_date = defaultdict(list)
        for insight in self.insights:
            if insight["date"]:
                by_date[insight["date"]].append(insight)

        # Calculate stats
        stats = {
            "total_insights": len(self.insights),
            "by_category": {
                cat: {
                    "count": len(insights),
                    "examples": [insight["note"][:100] for insight in insights[:3]]
                }
                for cat, insights in by_category.items()
            },
            "by_date": {
                date: {
                    "count": len(insights),
                    "outcomes": list(set(i["outcome"] for i in insights))
                }
                for date, insights in by_date.items()
            },
            "insight_trends": {
                "categories_over_time": self._get_trends_by_date(by_category)
            }
        }

        return stats

    def _get_trends_by_date(self, by_category: Dict[str, List]) -> Dict[str, List]:
        """Calculate insight trends over time."""
        trends = {}

        # Get all dates in order
        dates = sorted(set(
            insight["date"]
            for insight in self.insights
            if insight["date"]
        ))

        for date in dates:
            date_insights = [ins for ins in self.insights if ins["date"] == date]
            if not date_insights:
                continue

            category_counts = defaultdict(int)
            for insight in date_insights:
                cat = insight["categorization"]["type"]
                category_counts[cat] += 1

            trends[date] = dict(category_counts)

        return trends

    def save_insights_to_knowledge(self, output_path: str = "docs/insights.json"):
        """Save extracted insights to a JSON file."""
        if not self.insights:
            self.extract_insights_from_runs()

        with open(output_path, 'w') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total_insights": len(self.insights),
                "insights": self.insights
            }, f, indent=2)

        return output_path

    def generate_markdown_report(self, output_path: str = "site/insights_report.md"):
        """Generate a markdown report of insights."""
        if not self.insights:
            self.extract_insights_from_runs()

        stats = self.generate_insight_summary()

        lines = [
            "# Automated Insights Extraction Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Insights Extracted:** {stats['total_insights']}",
            "",
            "## Summary by Category",
            ""
        ]

        # Category summary
        for category, data in sorted(stats["by_category"].items()):
            lines.extend([
                f"### {category.title()} ({data['count']} insights)",
                ""
            ])

            # Show examples
            for example in data["examples"]:
                lines.append(f"- {example}...")
            lines.append("")

        lines.extend([
            "## Insights Over Time",
            "",
            "### Category Trends",
            ""
        ])

        # Trends table
        if stats["insight_trends"]["categories_over_time"]:
            dates = sorted(stats["insight_trends"]["categories_over_time"].keys())
            lines.append("| Date | Total |")
            lines.append("|------|-------|")

            for date in dates:
                total = sum(stats["insight_trends"]["categories_over_time"][date].values())
                lines.append(f"| {date} | {total} |")

            lines.append("")

            # Category breakdown per date
            lines.append("| Date | " + " | ".join(stats["insight_trends"]["categories_over_time"][dates[0]].keys()) + " |")
            lines.append("|------|" + "|".join(["-----"] * len(dates)) + "|")

            for date in dates:
                counts = stats["insight_trends"]["categories_over_time"][date]
                values = [str(counts.get(cat, 0)) for cat in counts.keys()]
                lines.append(f"| {date} | " + " | ".join(values) + " |")

        lines.append("")
        lines.append("## Sample Insights")
        lines.append("")

        # Show some random insights from each category
        for category, insights in stats["by_category"].items():
            lines.extend([
                f"### {category.title()}",
                ""
            ])

            insight_list = insights if isinstance(insights, list) else []
            for insight in insight_list[:5]:
                lines.extend([
                    f"**Run {insight['run']} ({insight['date']}):** {insight['note']}",
                    ""
                ])

        lines.append("## Notes", "")
        lines.append("- Insights are extracted from the 'note' column of RUNS.md", "")
        lines.append("- Categories are determined by keyword matching", "")
        lines.append("- Some insights may be repetitive or minor", "")
        lines.append("- Full insight data is available in `docs/insights.json`")

        with open(output_path, 'w') as f:
            f.write("\n".join(lines))

        return output_path

    def generate_visualization_data(self, output_path: str = "site/insights_visualization.json"):
        """Generate data for visualization."""
        if not self.insights:
            self.extract_insights_from_runs()

        stats = self.generate_insight_summary()

        visualization_data = {
            "insight_counts": {
                "by_category": stats["by_category"],
                "by_date": stats["by_date"]
            },
            "trends": stats["insight_trends"],
            "metadata": {
                "total_runs": len(self.runs),
                "total_insights": stats["total_insights"],
                "run_with_most_insights": max(
                    self.runs, key=lambda x: x["note"] != ""
                )["run"] if any(x["note"] for x in self.runs) else None
            }
        }

        with open(output_path, 'w') as f:
            json.dump(visualization_data, f, indent=2)

        return output_path


def main():
    """Main execution function."""
    extractor = InsightExtractor()

    print("Parsing RUNS.md...")
    extractor.parse_runs()
    print(f"Found {len(extractor.runs)} runs")

    print("\nExtracting insights...")
    insights = extractor.extract_insights_from_runs()
    print(f"Extracted {len(insights)} insights")

    print("\nGenerating summary...")
    stats = extractor.generate_insight_summary()
    print(f"Insights by category:")
    for category, data in sorted(stats["by_category"].items()):
        print(f"  - {category}: {data['count']}")

    print("\nSaving insights to JSON...")
    extractor.save_insights_to_knowledge()

    print("\nGenerating markdown report...")
    extractor.generate_markdown_report()

    print("\nGenerating visualization data...")
    extractor.generate_visualization_data()

    print("\n✅ Insights extraction complete!")
    print(f"\nOutput files:")
    print(f"  - docs/insights.json ({len(insights)} insights)")
    print(f"  - site/insights_report.md")
    print(f"  - site/insights_visualization.json")


if __name__ == "__main__":
    main()
