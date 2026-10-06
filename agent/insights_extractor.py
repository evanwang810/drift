#!/usr/bin/env python3
"""
Insights Extractor for RUNS.md

Extracts key insights from RUNS.md entries and categorizes them into types:
- tool_fix: Fixes to tools or scripts
- platform: Platform-related discoveries or issues
- discovery: New discoveries or learnings
- research: Research findings
- documentation: Documentation improvements
- project: Project completions or milestones
- blog: Blog post related work
- website: Website-related changes
- performance: Performance optimizations
- error: Error handling or debugging
"""

import re
import json
from typing import List, Dict, Any
from datetime import datetime

# Pattern for blog post links
BLOG_LINK_PATTERN = r'\(See:\s*\[([^\]]+)\]\([^)]+\)\)'
# Pattern for links to other docs
DOC_LINK_PATTERN = r'\[([^\]]+)\]\([^)]+\)'

def parse_runs_table(filepath: str) -> List[Dict[str, Any]]:
    """Parse RUNS.md table and extract run entries."""
    runs = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the table section
    in_table = False
    for i, line in enumerate(lines):
        # Skip YAML frontmatter
        if line.startswith('---'):
            continue
        
        # Look for runs header
        if 'runs' in line.lower():
            in_table = True
            continue
        
        # Parse table rows
        if in_table:
            line = line.strip()
            if not line or line.startswith('|---'):
                continue
            
            # Check if we've hit the end of the table
            if '|' in line and not any(c.isdigit() for c in line.split('|')[1:-1]):
                if '---' in line:
                    continue
                break
            
            # Parse table row
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 6:
                try:
                    run_num = int(parts[0])
                    date_str = parts[1]
                    status = parts[2]
                    turns = int(parts[3]) if parts[3].replace(',', '').isdigit() else 0
                    tokens = int(parts[4].replace(',', '')) if parts[4].replace(',', '').isdigit() else 0
                    note = ' '.join(parts[5:]) if len(parts) > 5 else ""
                    
                    runs.append({
                        'run_num': run_num,
                        'date': date_str,
                        'status': status,
                        'turns': turns,
                        'tokens': tokens,
                        'note': note
                    })
                except (ValueError, IndexError):
                    continue

    return runs

def extract_blog_posts(note: str) -> List[str]:
    """Extract blog post titles from note."""
    matches = re.findall(BLOG_LINK_PATTERN, note)
    return matches

def extract_doc_links(note: str) -> List[str]:
    """Extract documentation links from note."""
    matches = re.findall(DOC_LINK_PATTERN, note)
    return matches

def classify_insight(note: str, run_num: int, has_blog: bool, has_doc_links: bool) -> Dict[str, Any]:
    """
    Classify an insight based on its content and context.
    Returns a dictionary with classification and confidence scores.
    """
    categories = []

    # Check for blog-related keywords
    blog_keywords = ['blog', 'post', 'posts', 'markdown', 'Jekyll', 'frontmatter', 'HTML']
    if has_blog or any(kw in note.lower() for kw in blog_keywords):
        categories.append(('blog', 0.9))

    # Check for tool fix keywords
    tool_fix_keywords = ['fixed', 'delete', 'remove', 'replaced', 'bug', 'error', 'fix', 'corrected',
                         'validates', 'verify', 'test', 'tested', 'tool', 'script', 'function']
    if any(kw in note.lower() for kw in tool_fix_keywords):
        categories.append(('tool_fix', 0.85))

    # Check for platform keywords
    platform_keywords = ['platform', 'z.ai', 'api', 'configuration', 'config', 'model', 'glm']
    if any(kw in note.lower() for kw in platform_keywords):
        categories.append(('platform', 0.8))

    # Check for website-related keywords
    website_keywords = ['website', 'site', 'pages', 'render', 'markdown', 'HTML', 'CSS', 'style',
                       'build', 'navigation', 'link', 'links', 'posts', 'home', 'runs.html']
    if any(kw in note.lower() for kw in website_keywords):
        categories.append(('website', 0.85))

    # Check for documentation keywords
    doc_keywords = ['documentation', 'docs', 'README', 'readme', 'guide', 'tutorial', 'tutorial',
                   'manual', 'doc']
    if any(kw in note.lower() for kw in doc_keywords):
        categories.append(('documentation', 0.75))

    # Check for performance keywords
    perf_keywords = ['performance', 'optimized', 'optimize', 'speed', 'fast', 'slow', 'cache',
                    'memory', 'compact', 'compress', 'reduce', 'minimize']
    if any(kw in note.lower() for kw in perf_keywords):
        categories.append(('performance', 0.8))

    # Check for error/debugging keywords
    error_keywords = ['error', 'bug', 'debug', 'debugging', 'fix', 'fail', 'failure', 'issue',
                     'problem', 'incorrect', 'wrong', 'syntax', 'parse', 'validation']
    if any(kw in note.lower() for kw in error_keywords):
        categories.append(('error', 0.8))

    # Check for discovery/learning keywords
    discovery_keywords = ['discovered', 'found', 'learned', 'analysis', 'analyze', 'review',
                         'investigation', 'check', 'verified', 'verified', 'confirmed']
    if any(kw in note.lower() for kw in discovery_keywords):
        categories.append(('discovery', 0.7))

    # Check for project keywords
    project_keywords = ['project', 'completed', 'done', 'finished', 'enhanced', 'improved',
                       'created', 'build', 'develop']
    if any(kw in note.lower() for kw in project_keywords):
        categories.append(('project', 0.7))

    # Check for research keywords
    research_keywords = ['research', 'researched', 'investigation', 'study', 'analysis']
    if any(kw in note.lower() for kw in research_keywords):
        categories.append(('research', 0.75))

    # Default to 'discovery' if no specific category found
    if not categories:
        categories.append(('discovery', 0.5))

    # Return classification with highest confidence
    category, confidence = max(categories, key=lambda x: x[1])

    return {
        'category': category,
        'confidence': confidence,
        'note': note,
        'run_num': run_num,
        'has_blog': has_blog,
        'has_doc_links': has_doc_links
    }

def extract_insights(runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract insights from all run entries."""
    insights = []

    for run in runs:
        if not run['note'] or run['note'].startswith('(no note)'):
            continue

        # Extract blog posts
        blog_posts = extract_blog_posts(run['note'])
        has_blog = len(blog_posts) > 0

        # Extract doc links
        doc_links = extract_doc_links(run['note'])
        has_doc_links = len(doc_links) > 0

        # Classify insight
        classification = classify_insight(run['note'], run['run_num'], has_blog, has_doc_links)

        insight = {
            **classification,
            'date': run['date'],
            'turns': run['turns'],
            'tokens': run['tokens']
        }

        insights.append(insight)

    return insights

def categorize_insights_by_type(insights: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group insights by category."""
    categorized = {}

    for insight in insights:
        category = insight['category']
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(insight)

    return categorized

def main():
    """Main function to extract insights from RUNS.md."""
    runs = parse_runs_table('RUNS.md')
    insights = extract_insights(runs)
    categorized = categorize_insights_by_type(insights)

    # Print summary
    print(f"Total runs: {len(runs)}")
    print(f"Total insights extracted: {len(insights)}")
    print(f"\nInsights by category:")
    for category, items in sorted(categorized.items(), key=lambda x: -len(x[1])):
        print(f"  {category}: {len(items)}")

    # Save to JSON file
    output = {
        'total_runs': len(runs),
        'total_insights': len(insights),
        'insights': insights,
        'by_category': categorized
    }

    with open('agent/insights.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nInsights saved to agent/insights.json")

    return output

if __name__ == '__main__':
    main()
