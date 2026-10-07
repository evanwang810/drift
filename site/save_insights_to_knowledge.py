#!/usr/bin/env python3
"""
Save extracted insights from RUNS.md to the knowledge base.

This script takes insights extracted by extract_insights.py and saves them
to docs/knowledge_base.json as structured knowledge entries.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import sys


def load_insights(insights_file: str = "RUNS.md") -> List[Dict[str, Any]]:
    """Load insights from extract_insights.py output."""
    # Read insights from RUNS.md by running the extraction script
    from extract_insights import InsightsExtractor

    extractor = InsightsExtractor(insights_file)
    insights = extractor.extract_all_insights()
    return insights


def save_insights_to_knowledge(insights: List[Dict[str, Any]],
                                knowledge_path: str = "docs/knowledge_base.json") -> int:
    """Save insights to knowledge base with proper formatting."""
    # Load existing knowledge base
    kb_path = Path(knowledge_path)
    if kb_path.exists():
        with open(kb_path, 'r') as f:
            knowledge = json.load(f)
    else:
        knowledge = []

    # Prepare insights as knowledge entries
    new_entries = []
    for insight in insights:
        category = insight['category']
        terms = insight['terms']

        # Create title and description
        if category == 'tool_fix':
            title = f"Tool/Feature: {', '.join(terms[:2])}"
            description = f"Added or improved {', '.join(terms[:2])} - found in run {insight['run']}"
        elif category == 'discovery':
            title = f"Discovery: {', '.join(terms[:2])}"
            description = f"Discovered {', '.join(terms[:2])} during run {insight['run']}"
        elif category == 'platform':
            title = f"Platform: {', '.join(terms[:2])}"
            description = f"Platform-related {', '.join(terms[:2])} in run {insight['run']}"
        elif category == 'research':
            title = f"Research: {', '.join(terms[:2])}"
            description = f"Research findings about {', '.join(terms[:2])} in run {insight['run']}"
        elif category == 'tool_improvement':
            title = f"Tool Improvement: {', '.join(terms[:2])}"
            description = f"Improved {', '.join(terms[:2])} in run {insight['run']}"
        elif category == 'tool_limitation':
            title = f"Tool Limitation: {', '.join(terms[:2])}"
            description = f"Limitation or bug with {', '.join(terms[:2])} in run {insight['run']}"
        elif category == 'workflow':
            title = f"Workflow: {', '.join(terms[:2])}"
            description = f"Workflow improvement for {', '.join(terms[:2])} in run {insight['run']}"
        else:
            title = f"{category}: {', '.join(terms[:2])}"
            description = f"{', '.join(terms[:2])} in run {insight['run']}"

        # Generate tags
        tags = [category]
        tags.extend(terms[:3])  # Add first 3 terms as tags
        tags = list(set(tags))  # Deduplicate

        entry = {
            "id": f"k-{len(knowledge):03d}",
            "title": title,
            "description": description,
            "type": category,
            "tags": tags,
            "source": f"Run {insight['run']}",
            "implementation": f"Extracted from RUNS.md run {insight['run']}",
            "verification": "Automated extraction from run notes",
            "impact": "Documents patterns and discoveries across run history"
        }

        new_entries.append(entry)

    # Add new entries to knowledge base
    knowledge.extend(new_entries)

    # Save updated knowledge base
    with open(kb_path, 'w') as f:
        json.dump(knowledge, f, indent=2)

    return len(new_entries)


def main():
    """Main function to save insights to knowledge base."""
    print("Extracting insights from RUNS.md...")
    insights = load_insights()

    print(f"\nExtracted {len(insights)} insights")
    print("\nSample insights:")
    for i, insight in enumerate(insights[:5]):
        print(f"  - {insight['category']}: {', '.join(insight['terms'][:3])}")

    print("\nSaving insights to knowledge base...")
    saved = save_insights_to_knowledge(insights)

    print(f"\nSuccessfully saved {saved} insights to knowledge_base.json")
    print(f"Total knowledge base entries: {len(insights)}")


if __name__ == "__main__":
    main()
