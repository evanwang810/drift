#!/usr/bin/env python3
"""
Extract insights from RUNS.md and categorize them.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime

def parse_runs():
    """Parse RUNS.md and extract run data."""
    runs = []
    with open('RUNS.md', 'r') as f:
        lines = f.readlines()

    # Find the table section
    in_table = False
    for line in lines:
        if line.strip() == '| run | when (UTC) | outcome | turns | tokens | note |':
            in_table = True
            continue
        if in_table and line.strip().startswith('| --') and '---' in line:
            continue
        if in_table and line.strip().startswith('| '):
            # Parse table row
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 6:
                run_num = int(parts[0])
                try:
                    when = datetime.strptime(parts[1], '%Y-%m-%d %H:%M')
                except:
                    when = None
                outcome = parts[2]
                turns = int(parts[3])
                tokens = int(parts[4].replace(',', ''))
                note = parts[5]
                runs.append({
                    'run': run_num,
                    'when': when,
                    'outcome': outcome,
                    'turns': turns,
                    'tokens': tokens,
                    'note': note
                })
        elif in_table and line.strip().startswith('| '):
            # Parse continuation row
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 6:
                # This is a continuation, append to last run
                runs[-1]['note'] += ' ' + ' '.join(parts[5:])

    return runs

def extract_blog_references(note):
    """Extract blog post references from a note."""
    # Look for (See: ...) patterns
    pattern = r'\(See:\s*\((.*?)\)\)'
    matches = re.findall(pattern, note)
    return matches

def categorize_insight(note, run_num):
    """Categorize an insight based on its content."""
    note_lower = note.lower()
    
    # Remove "(no note)" and duplicate ") ) " patterns
    note_clean = re.sub(r'\)\)\s*\(', ' (', note)
    note_clean = note_clean.replace('(no note)', '').replace('(no note) ) )', '')
    
    # Blog post references
    if 'see:' in note_lower or '(see:' in note_lower:
        return 'blog_post'

    # Tool fixes and discoveries
    if ('tool' in note_lower and ('fix' in note_lower or 'fixed' in note_lower or 'bug' in note_lower)):
        return 'tool_fix'

    if ('tool' in note_lower and ('discovered' in note_lower or 'implemented' in note_lower or 'created' in note_lower or 'added' in note_lower)):
        return 'tool_discovery'

    # Website fixes
    if 'website' in note_lower or 'site' in note_lower:
        if 'fix' in note_lower or 'fixed' in note_lower or 'bug' in note_lower:
            return 'website_fix'
        if 'build' in note_lower or 'rebuild' in note_lower or 'created' in note_lower:
            return 'website_build'

    # Knowledge base entries
    if 'knowledge' in note_lower:
        return 'knowledge_base'

    # Platform/API discoveries
    if 'platform' in note_lower or 'api' in note_lower:
        return 'platform'

    # Research
    if 'research' in note_lower or 'learned' in note_lower or 'investigated' in note_lower:
        return 'research'

    # Documentation
    if 'document' in note_lower or 'docs' in note_lower:
        return 'documentation'

    # Memory management
    if 'memory' in note_lower or 'compact' in note_lower or 'fold' in note_lower:
        return 'memory'

    # Completed projects
    if 'completed' in note_lower or 'done' in note_lower or 'verified' in note_lower:
        return 'completed'

    # Outcomes and problems
    if note_clean in ['crashed', 'api_error', 'out_of_turns', 'out_of_time', 'the api would not answer']:
        return 'outcome'

    return 'other'

def analyze_outcomes(runs):
    """Analyze outcome patterns."""
    outcomes = Counter()
    for run in runs:
        outcomes[run['outcome']] += 1
    return outcomes

def analyze_tokens_over_time(runs):
    """Analyze token usage over time."""
    tokens_by_month = defaultdict(list)
    for run in runs:
        if run['when']:
            month = run['when'].strftime('%Y-%m')
            tokens_by_month[month].append(run['tokens'])

    monthly_avg = {}
    for month, token_list in tokens_by_month.items():
        monthly_avg[month] = sum(token_list) / len(token_list)

    return monthly_avg

def extract_all_insights(runs):
    """Extract all insights from runs."""
    insights = {
        'blog_posts': [],
        'tool_fixes': [],
        'tool_discoveries': [],
        'website_fixes': [],
        'website_builds': [],
        'knowledge_base': [],
        'platform': [],
        'research': [],
        'outcomes': [],
        'other': []
    }

    for run in runs:
        # Blog posts
        blog_refs = extract_blog_references(run['note'])
        if blog_refs:
            for ref in blog_refs:
                insights['blog_posts'].append({
                    'run': run['run'],
                    'when': run['when'],
                    'note': run['note'],
                    'reference': ref
                })

        # Categorize insights
        category = categorize_insight(run['note'], run['run'])
        if category in insights:
            insights[category].append({
                'run': run['run'],
                'when': run['when'],
                'outcome': run['outcome'],
                'turns': run['turns'],
                'tokens': run['tokens'],
                'note': run['note']
            })
        else:
            insights['other'].append({
                'run': run['run'],
                'when': run['when'],
                'outcome': run['outcome'],
                'turns': run['turns'],
                'tokens': run['tokens'],
                'note': run['note']
            })

    return insights

def main():
    print("Parsing RUNS.md...")
    runs = parse_runs()
    print(f"Found {len(runs)} runs")

    print("\n=== Outcome Patterns ===")
    outcomes = analyze_outcomes(runs)
    for outcome, count in outcomes.most_common():
        print(f"{outcome}: {count} ({count/len(runs)*100:.1f}%)")

    print("\n=== Token Usage Over Time ===")
    monthly_avg = analyze_tokens_over_time(runs)
    for month in sorted(monthly_avg.keys()):
        print(f"{month}: {monthly_avg[month]:.0f} avg tokens")

    print("\n=== Insights Breakdown ===")
    insights = extract_all_insights(runs)
    total_insights = sum(len(v) for v in insights.values())
    for category, items in insights.items():
        count = len(items)
        print(f"{category}: {count} ({count/total_insights*100:.1f}%)")

    # Save detailed insights
    import json
    with open('insights.json', 'w') as f:
        json.dump(insights, f, indent=2, default=str)

    print(f"\nDetailed insights saved to insights.json")

    # Generate knowledge base entries
    print("\n=== Knowledge Base Entries ===")
    for category, items in insights.items():
        if items:
            print(f"\n{category}:")
            for item in items[:3]:  # Show first 3 of each category
                print(f"  Run {item['run']}: {item['note'][:80]}...")

if __name__ == '__main__':
    main()
