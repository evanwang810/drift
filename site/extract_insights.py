#!/usr/bin/env python3
"""
Extract insights from RUNS.md and categorize them for the knowledge base.

This script analyzes run notes to identify patterns, discoveries, and learnings
that can be extracted as knowledge base entries.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import json


class InsightsExtractor:
    """Extract insights from RUNS.md run entries."""

    def __init__(self, runs_path: str = "RUNS.md"):
        self.runs_path = Path(runs_path)
        self.runs = self._load_runs()
        self.insights = []

    def _load_runs(self) -> List[Dict[str, Any]]:
        """Parse RUNS.md table and extract run data."""
        runs = []
        in_table = False

        with open(self.runs_path, 'r') as f:
            for line in f:
                line = line.strip()

                # Check if we're in the table
                if line.startswith('| run |'):
                    in_table = True
                    continue
                if line.startswith('| --:'):
                    continue  # Skip separator row
                if not in_table or not line.startswith('|'):
                    continue

                # Parse table row
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6:
                    run_num = int(parts[1])
                    date_str = parts[2]
                    outcome = parts[3]
                    turns = int(parts[4])
                    tokens = int(parts[5].replace(',', ''))
                    note = parts[6] if len(parts) > 6 else ""

                    runs.append({
                        'run': run_num,
                        'date': datetime.fromisoformat(date_str),
                        'outcome': outcome,
                        'turns': turns,
                        'tokens': tokens,
                        'note': note
                    })

        return runs

    def _extract_insight_from_note(self, run: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract insights from a single run's note."""
        note = run['note'].lower()

        insights = []

        # Patterns to look for
        patterns = {
            'tool_fix': [
                r'added?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'started?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'created?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'implemented?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'removed?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'removed\s+\d+\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'enhanced?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'refined?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'fixed?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'updated?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'deleted?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'audited?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'cleaned?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'enhanced?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'built?\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'script',
                r'function',
                r'automation',
                r'page',
                r'blog',
                r'post',
                r'file',
                r'directory',
                r'module',
                r'component',
                r'html',
                r'markdown',
                r'css',
                r'javascript',
            ],
            'platform': [
                r'github\s+pages',
                r'github\s+issues',
                r'github\s+repo',
                r'api\s+error',
                r'the\s+api\s+would\s+not\s+answer',
                r'out_of_turns',
                r'crashed',
                r'stopped',
                r'completed',
                r'optimized',
                r'performance',
                r'static',
                r'live',
                r'deployed',
                r'production',
                r'cache',
                r'build\s+script',
            ],
            'discovery': [
                r'found\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'discovered\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'noted\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'noticed\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'realized\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'learned\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'noticed\s+(?:\w+(?:\s+\w+)*)(?!\s+tool)',
                r'observed\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
                r'saw\s+(\w+(?:\s+\w+)*)(?!\s+tool)',
            ],
            'research': [
                r'research',
                r'studied',
                r'analyzed',
                r'investigated',
                r'examined',
                r'investigation',
                r'pattern',
                r'trend',
                r'insight',
            ],
            'workflow': [
                r'workflow',
                r'automated',
                r'build\s+process',
                r'script',
                r'automation',
                r'site\s+build',
                r'run\s+after',
                r'runs\s+after',
                r'pipeline',
                r'automate',
            ],
            'tool_improvement': [
                r'improved?\s+tool',
                r'enhanced?\s+tool',
                r'better?\s+tool',
                r'newer?\s+tool',
                r'updated?\s+tool',
                r'fixed\s+tool',
            ],
            'tool_limitation': [
                r'can\'t',
                r'cannot',
                r'unable to',
                r'failed to',
                r'problem with',
                r'issue with',
                r'bug',
                r'limitation',
                r'error',
                r'failure',
            ],
        }

        # Common words to filter out
        stop_words = {
            'a', 'an', 'the', 'to', 'of', 'in', 'on', 'for', 'with', 'at',
            'by', 'from', 'and', 'or', 'but', 'is', 'was', 'are', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'this', 'that', 'these', 'those', 'it', 'its', 'it\'s',
        }

        # Check for pattern matches
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, note)
                if matches:
                    # Filter out stop words and deduplicate
                    meaningful_matches = [
                        m for m in matches
                        if m not in stop_words and not m.startswith('_')
                    ]
                    if meaningful_matches:
                        # Deduplicate
                        unique_matches = list(set(meaningful_matches))
                        if unique_matches:
                            insights.append({
                                'category': category,
                                'terms': unique_matches,
                                'confidence': min(len(unique_matches) * 0.2, 1.0)
                            })

        return insights

    def extract_all_insights(self) -> List[Dict[str, Any]]:
        """Extract insights from all runs."""
        all_insights = []

        for run in self.runs:
            insights = self._extract_insight_from_note(run)

            for insight in insights:
                insight['run'] = run['run']
                insight['date'] = run['date'].isoformat()
                insight['outcome'] = run['outcome']
                insight['tokens'] = run['tokens']
                all_insights.append(insight)

        # Deduplicate by category and terms
        seen = set()
        unique_insights = []

        for insight in all_insights:
            key = (insight['category'], frozenset(insight['terms']))
            if key not in seen:
                seen.add(key)
                unique_insights.append(insight)

        return unique_insights

    def categorize_insights(self, insights: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group insights by category."""
        categorized = {}

        for insight in insights:
            category = insight['category']
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(insight)

        return categorized

    def generate_insight_summary(self) -> str:
        """Generate a summary of all insights."""
        insights = self.extract_all_insights()
        categorized = self.categorize_insights(insights)

        summary = []
        summary.append(f"Extracted {len(insights)} unique insights from {len(self.runs)} runs")
        summary.append("\nBy category:")
        summary.append("-" * 60)

        for category, category_insights in sorted(categorized.items()):
            summary.append(f"\n{category.upper()} ({len(category_insights)} insights):")
            for insight in category_insights[:10]:  # Show first 10 per category
                terms = ', '.join(insight['terms'])
                summary.append(f"  - Run {insight['run']}: {terms}")

        return '\n'.join(summary)


def extract_insights_from_runs(runs_path: str = "RUNS.md") -> List[Dict[str, Any]]:
    """Main function to extract insights from RUNS.md."""
    extractor = InsightsExtractor(runs_path)
    insights = extractor.extract_all_insights()
    categorized = extractor.categorize_insights(insights)

    print(extractor.generate_insight_summary())

    return insights, categorized


if __name__ == "__main__":
    insights, categorized = extract_insights_from_runs()
    print(f"\nTotal unique insights: {len(insights)}")
    print(f"\nInsights by category:")
    for category, cat_insights in sorted(categorized.items()):
        print(f"  {category}: {len(cat_insights)}")
