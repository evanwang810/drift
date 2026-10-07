#!/usr/bin/env python3
"""Extract insights from RUNS.md and categorize them for the knowledge base.

This script parses RUNS.md, identifies key insights and patterns, and
categorizes them into types like tool_fix, platform, discovery, research, etc.
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parent.parent
RUNS_FILE = ROOT / "RUNS.md"
KNOWLEDGE_FILE = ROOT / "docs" / "knowledge_base.json"


def parse_runs() -> List[Dict]:
    """Parse RUNS.md and extract run information.

    Returns:
        List of dictionaries containing run details
    """
    content = RUNS_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()

    runs = []
    in_runs_section = False

    for line in lines:
        if line.strip().startswith("| run |"):
            in_runs_section = True
            continue

        if in_runs_section:
            if line.strip().startswith("| --"):
                continue

            if not line.strip() or line.strip().startswith("| ---"):
                # End of runs section
                break

            # Parse table row
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 6:
                # Clean tokens field (remove commas)
                tokens_str = cells[4].replace(',', '') if cells[4] else "0"
                run_data = {
                    "run": int(cells[0]) if cells[0] else None,
                    "when": cells[1] if len(cells) > 1 else "",
                    "outcome": cells[2] if len(cells) > 2 else "",
                    "turns": int(cells[3]) if cells[3] else 0,
                    "tokens": int(tokens_str) if tokens_str.isdigit() else 0,
                    "note": cells[5] if len(cells) > 5 else ""
                }
                runs.append(run_data)

    return runs


def extract_insight(note: str, run_num: int) -> Dict:
    """Extract and categorize an insight from a run note.

    Args:
        note: The note text from the run
        run_num: The run number

    Returns:
        Dictionary containing insight information
    """
    insight = {
        "run": run_num,
        "text": note.strip(),
        "type": "discovery",
        "tags": [],
        "confidence": 0.7
    }

    # Analyze note content to determine type and tags
    text_lower = note.lower()

    # Tool fixes/improvements
    if any(word in text_lower for word in ["tool", "added", "enhanced", "expanded", "improved", "refined"]):
        insight["type"] = "tool_fix"
        insight["tags"].append("tool_improvement")

    # Platform/API issues
    if any(word in text_lower for word in ["api", "github", "permissions", "blocked", "would not answer"]):
        insight["type"] = "platform"
        insight["tags"].append("api_issue")
        insight["tags"].append("github")

    # Discoveries and findings
    if any(word in text_lower for word in ["discovery", "found", "identified", "noticed"]):
        insight["type"] = "discovery"

    # Research and analysis
    if any(word in text_lower for word in ["analysis", "investigation", "examined", "reviewed"]):
        insight["type"] = "research"
        insight["tags"].append("investigation")

    # Blog post references
    if "(See:" in note or "(see:" in note:
        insight["type"] = "discovery"
        insight["tags"].append("blog_post")

    # Errors and failures
    if "error" in text_lower or "crashed" in text_lower:
        insight["type"] = "discovery"
        insight["tags"].append("failure")

    # Add default tags based on outcome
    if "stopped" in text_lower:
        insight["tags"].append("completed")

    return insight


def categorize_insights(runs: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize insights by type.

    Args:
        runs: List of run dictionaries

    Returns:
        Dictionary mapping types to lists of insights
    """
    categories: Dict[str, List[Dict]] = {
        "tool_fix": [],
        "platform": [],
        "discovery": [],
        "research": [],
        "other": []
    }

    for run in runs:
        note = run["note"]
        if not note or note.strip() == "":
            continue

        insight = extract_insight(note, run["run"])

        # Add tags for outcomes
        outcome = run["outcome"].lower()
        if outcome == "stopped":
            insight["tags"].append("completed")
        elif outcome == "api_error":
            insight["tags"].append("api_error")
        elif outcome == "crashed":
            insight["tags"].append("crashed")

        # Categorize
        if insight["type"] in categories:
            categories[insight["type"]].append(insight)
        else:
            categories["other"].append(insight)

    return categories


def generate_insight_summary(categories: Dict[str, List[Dict]]) -> str:
    """Generate a summary of all insights.

    Args:
        categories: Dictionary of categorized insights

    Returns:
        Formatted summary text
    """
    summary = []
    summary.append("# Insights from RUNS.md")
    summary.append(f"\nTotal runs analyzed: {len(categories.get('tool_fix', [])) + len(categories.get('platform', [])) + len(categories.get('discovery', [])) + len(categories.get('research', [])) + len(categories.get('other', []))}")
    summary.append("\n## Categorized Insights\n")

    for category, insights in sorted(categories.items()):
        if insights:
            summary.append(f"\n### {category.title()} ({len(insights)} insights)\n")

            for insight in insights[:10]:  # Limit to first 10 per category
                summary.append(f"- **Run {insight['run']}:** {insight['text'][:100]}...")
                if insight['tags']:
                    summary.append(f"  - Tags: {', '.join(insight['tags'])}")

    return "\n".join(summary)


def save_insights_to_knowledge(insights: List[Dict]) -> int:
    """Save insights to knowledge base.

    Args:
        insights: List of insight dictionaries

    Returns:
        Number of insights saved
    """
    saved_count = 0

    # Read existing knowledge base
    try:
        knowledge_data = json.loads(KNOWLEDGE_FILE.read_text(encoding="utf-8"))
        if isinstance(knowledge_data, list):
            entries = knowledge_data
        else:
            entries = knowledge_data.get('entries', [])
    except Exception as e:
        print(f"Warning: Could not read knowledge base: {e}")
        entries = []

    for insight in insights:
        if len(insight['text']) < 20:  # Skip very short notes
            continue

        # Check if we already have this insight
        for entry in entries:
            if entry.get('title') == f"Insight from Run {insight['run']}":
                break
        else:
            # Create new knowledge base entry
            new_entry = {
                "title": f"Insight from Run {insight['run']}",
                "description": insight['text'][:300],
                "type": insight['type'],
                "tags": insight['tags'] + [insight['type']],
                "source": f"RUNS.md run {insight['run']}",
                "implementation": f"Extracted from run note: {insight['text'][:150]}...",
                "verification": "Manual review of RUNS.md",
                "impact": "Documents key patterns and discoveries"
            }
            entries.append(new_entry)
            saved_count += 1

    # Write back to knowledge base
    try:
        if isinstance(knowledge_data, list):
            json.dump(entries, knowledge_file, indent=2, ensure_ascii=False)
        else:
            knowledge_data['entries'] = entries
            json.dump(knowledge_data, knowledge_file, indent=2, ensure_ascii=False)
        print(f"✓ Updated knowledge base with {saved_count} new insights")
    except Exception as e:
        print(f"Error writing to knowledge base: {e}")

    return saved_count


def main():
    """Main execution function."""
    print("=" * 60)
    print("Extracting insights from RUNS.md")
    print("=" * 60)

    # Parse runs
    runs = parse_runs()
    print(f"\n✓ Parsed {len(runs)} runs from RUNS.md")

    # Categorize insights
    categories = categorize_insights(runs)
    print(f"✓ Categorized insights into {len(categories)} categories")

    # Print summary
    summary = generate_insight_summary(categories)
    print("\n" + summary)

    # Save to knowledge base
    total_insights = sum(len(v) for v in categories.values())
    print(f"\n✓ Found {total_insights} potential insights")

    # Save non-empty categories to knowledge base
    saved = 0
    for category, insights in categories.items():
        if insights:
            saved += save_insights_to_knowledge(insights)
            print(f"✓ Updated knowledge base with insights from '{category}'")

    print(f"\n{'=' * 60}")
    print(f"Total insights saved to knowledge base: {saved}/{total_insights}")
    print(f"{'=' * 60}")

    # Save summary to file
    summary_file = ROOT / "docs" / "insights_summary.md"
    summary_file.write_text(summary, encoding="utf-8")
    print(f"✓ Saved summary to {summary_file}")


if __name__ == "__main__":
    main()
