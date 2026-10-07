#!/usr/bin/env python3
"""
Automatically extract and categorize key insights from RUNS.md.

This script parses the RUNS.md table format, identifies patterns of errors,
tool fixes, platform discoveries, and long-term learnings, and generates
knowledge base entries for each insight.
"""

import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class InsightExtractor:
    """Extract insights from RUNS.md and categorize them."""

    # Patterns for different types of insights
    PATTERNS = {
        'tool_fix': [
            r'Added\s+(\w+)',
            r'Enhanced\s+(\w+)',
            r'Expanded\s+(\w+)',
            r'Created\s+(\w+)',
            r'Improved\s+(\w+)',
            r'Refined\s+(\w+)',
            r'Moved\s+(\w+)',
            r'Fixed\s+(\w+)',
            r'Optimized\s+(\w+)',
            r'Implemented\s+(\w+)',
            r'Removed\s+(\w+)',
            r'Cleaned\s+(\w+)',
            r'Reorganized\s+(\w+)',
            r'Documented\s+(\w+)',
        ],
        'platform': [
            r'api\s+(would not answer|timeout|error)',
            r'api\s+error',
            r'platform\s+(limit|constraint|capability)',
            r'rate\s+limit',
            r'permission\s+denied',
            r'blocked\s+by\s+permissions',
            r'github\s+pages',
        ],
        'discovery': [
            r'found',
            r'noticed',
            r'observed',
            r'learned',
            r'insight',
            r'strategy',
            r'pattern',
            r'trend',
            r'issue',
        ],
        'research': [
            r'search',
            r'research',
            r'investigate',
            r'explore',
            r'analyze',
            r'summarize',
            r'compile',
        ],
        'workflow': [
            r'workflow',
            r'process',
            r'steps',
            r'procedure',
            r'system',
            r'mechanism',
        ],
    }

    def __init__(self):
        self.insights = []
        self.candidates = []
        self.error_runs = []

    def parse_runs_table(self):
        """Parse the RUNS.md table and extract all runs."""

        runs_path = Path('RUNS.md')
        content = runs_path.read_text()

        # Parse markdown table
        # Pattern: run | date | outcome | turns | tokens | note
        table_pattern = r'\|(\s*\d+\s*)\|\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|'

        self.candidates = []
        for match in re.finditer(table_pattern, content, re.DOTALL):
            run_num = int(match.group(1))
            date_str = f"{match.group(2)} {match.group(3)}"
            outcome = match.group(4)
            turns = int(match.group(5))
            tokens = int(match.group(6))
            note = match.group(7).strip()

            self.candidates.append({
                'run': run_num,
                'date': date_str,
                'outcome': outcome,
                'turns': turns,
                'tokens': tokens,
                'note': note,
            })

        # Categorize runs by outcome
        self.error_runs = [
            c for c in self.candidates
            if c['outcome'] not in ['stopped', 'success']
        ]

        return self.candidates

    def extract_insight_from_note(self, candidate, notes_only=False):
        """Extract potential insights from a run's note."""

        note = candidate['note']
        run_num = candidate['run']
        date = candidate['date']
        outcome = candidate['outcome']
        turns = candidate['turns']
        tokens = candidate['tokens']

        # Skip empty notes
        if not note or note == '-':
            return None

        # Skip runs with "(See: ...)" for now - those are blog candidates
        if '(See:' in note or '(See:' in note:
            return None

        # Analyze patterns in the note
        insight_types = []
        for itype, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, note, re.IGNORECASE):
                    insight_types.append(itype)
                    break

        # If no patterns match, check if it's an error
        if not insight_types and outcome in ['api_error', 'crashed', 'failed']:
            insight_types = ['discovery']

        # If still no patterns, it's a general observation
        if not insight_types:
            insight_types = ['discovery']

        # Deduplicate insight types
        insight_types = list(set(insight_types))

        # Create insight object
        insight = {
            'run': run_num,
            'date': date,
            'outcome': outcome,
            'turns': turns,
            'tokens': tokens,
            'note': note,
            'types': insight_types,
            'title': self._generate_title(note, insight_types),
            'description': self._generate_description(note, insight_types),
            'tags': self._generate_tags(insight_types, note),
            'source': f"Run {run_num}",
            'implementation': f"Run {run_num} - {outcome} with {turns} turns and {tokens} tokens",
            'verification': "Extracted from RUNS.md entry",
            'impact': "Documented for future reference and analysis",
        }

        return insight

    def _generate_title(self, note, insight_types):
        """Generate a title from the note and insight types."""

        # Try to find a meaningful phrase
        # Remove common intro phrases
        cleaned = re.sub(r'^The\s+', '', note)
        cleaned = re.sub(r'^A\s+', '', cleaned)
        cleaned = re.sub(r'^an\s+', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'^It\s+', '', cleaned)
        cleaned = re.sub(r'^I\s+', '', cleaned)

        # Capitalize first letter
        cleaned = cleaned[0].upper() + cleaned[1:] if cleaned else "Observation"

        # Limit length
        if len(cleaned) > 100:
            cleaned = cleaned[:97] + "..."

        return cleaned

    def _generate_description(self, note, insight_types):
        """Generate a description from the note and insight types."""

        # Use the note as the main description
        desc = note

        # Add context based on insight types
        type_context = {
            'tool_fix': 'Tool or feature improvement',
            'platform': 'Platform constraint or capability',
            'discovery': 'New observation or finding',
            'research': 'Research or investigation',
            'workflow': 'Workflow or process change',
        }

        type_desc = ', '.join([type_context.get(t, t) for t in insight_types if t in type_context])

        if type_desc:
            desc = f"{desc} ({type_desc})"

        return desc

    def _generate_tags(self, insight_types, note):
        """Generate tags from insight types and note."""

        tags = []

        # Add insight types as tags
        for t in insight_types:
            tags.append(t)

        # Extract potential keywords
        keywords = re.findall(r'\b(\w{4,})\b', note.lower())
        unique_keywords = list(set(keywords))

        # Add top keywords (exclude common words)
        common_words = {'the', 'and', 'for', 'with', 'from', 'into', 'when', 'what', 'which', 'this', 'that', 'be', 'are', 'was', 'were', 'been', 'have', 'has', 'had'}
        for kw in unique_keywords:
            if len(kw) > 3 and kw not in common_words and kw not in tags:
                tags.append(kw)
                if len(tags) > 5:
                    break

        return tags[:8]  # Limit to 8 tags

    def extract_all_insights(self, notes_only=False):
        """Extract all insights from all candidates."""

        self.insights = []

        for candidate in self.candidates:
            insight = self.extract_insight_from_note(candidate, notes_only)
            if insight:
                self.insights.append(insight)

        return self.insights

    def get_insight_trends(self):
        """Analyze insight trends over time."""

        trends = defaultdict(lambda: {'count': 0, 'tokens': 0, 'turns': 0, 'types': defaultdict(int)})

        for insight in self.insights:
            date = insight['date'].split()[0]  # Extract date only

            trends[date]['count'] += 1
            trends[date]['tokens'] += insight['tokens']
            trends[date]['turns'] += insight['turns']

            for itype in insight['types']:
                trends[date]['types'][itype] += 1

        # Convert to list and sort by date
        sorted_trends = sorted(trends.items(), key=lambda x: x[0])

        return sorted_trends

    def save_insights(self, output_path):
        """Save insights to a JSON file."""

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'extraction_date': datetime.now().isoformat(),
            'total_insights': len(self.insights),
            'total_runs': len(self.candidates),
            'insights': self.insights,
        }

        with open(output, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Saved {len(self.insights)} insights to {output}")

    def print_summary(self):
        """Print a summary of extracted insights."""

        print("=" * 80)
        print(f"EXTRACTED INSIGHTS SUMMARY")
        print("=" * 80)
        print(f"Total runs analyzed: {len(self.candidates)}")
        print(f"Total insights extracted: {len(self.insights)}")
        print(f"Error runs: {len(self.error_runs)}")
        print()

        # Count by type
        type_counts = defaultdict(int)
        for insight in self.insights:
            for itype in insight['types']:
                type_counts[itype] += 1

        print("Insights by type:")
        for itype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {itype}: {count}")
        print()

        # Top insights by run
        print("Top insights (by run number):")
        sorted_insights = sorted(self.insights, key=lambda x: x['run'])
        for insight in sorted_insights[:20]:
            print(f"  Run {insight['run']:3d} [{', '.join(insight['types'])}]: {insight['title'][:60]}")
        print()

        # Error summary
        if self.error_runs:
            print(f"Error runs (out of {len(self.error_runs)}):")
            for candidate in self.error_runs[:10]:
                print(f"  Run {candidate['run']:3d} - {candidate['outcome']:12s} - {candidate['note'][:60]}")
            print()

def main():
    """Main function to extract insights."""

    print("Extracting insights from RUNS.md...")
    print("=" * 80)

    extractor = InsightExtractor()

    # Parse runs table
    print("Parsing RUNS.md...")
    extractor.parse_runs_table()
    print(f"Found {len(extractor.candidates)} runs")
    print()

    # Extract insights
    print("Extracting insights from notes...")
    extractor.extract_all_insights()
    print(f"Extracted {len(extractor.insights)} insights")
    print()

    # Print summary
    extractor.print_summary()

    # Get trends
    print("Analyzing trends...")
    trends = extractor.get_insight_trends()
    print(f"Found trends across {len(trends)} unique dates")
    print()

    # Save insights
    output_path = Path('site/extracted_insights.json')
    extractor.save_insights(output_path)

    print("Insight extraction complete!")

if __name__ == '__main__':
    main()
