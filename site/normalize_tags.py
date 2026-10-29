#!/usr/bin/env python3
"""
Normalize and categorize knowledge base tags.

This script reads the knowledge_base.html file, extracts all tags from
knowledge entries, normalizes them, and creates a clean tag categorization
system.
"""

import re
from collections import defaultdict

def extract_tags_from_html(html_file):
    """Extract tags from knowledge_base.html entries."""
    with open(html_file, 'r') as f:
        content = f.read()

    # Find all data-tags attributes
    pattern = r'data-tags="([^"]*)"'
    tags_data = re.findall(pattern, content)

    all_tags = set()
    tag_entries = defaultdict(list)

    for tags_str in tags_data:
        tags = tags_str.split()
        for tag in tags:
            all_tags.add(tag)
            tag_entries[tag].append(tags_str)

    return all_tags, tag_entries

def normalize_tags(all_tags):
    """Normalize tag names to be clean and consistent."""
    normalized = {}

    for tag in sorted(all_tags):
        # Remove common prefixes like "tool_fix" duplicates
        if tag.startswith('tool_fix '):
            tag = tag.replace('tool_fix ', '', 1)
        elif tag.endswith(' tool_fix'):
            tag = tag.rsplit(' ', 1)[0]
        elif tag == 'tool_fix':
            continue  # Skip empty after removal

        # Split concatenated tags
        if len(tag) < 3 and not tag:  # Skip very short tags
            continue

        # Remove excessive duplicates
        normalized_tag = re.sub(r'(.)\1+', r'\1', tag)
        if normalized_tag:
            normalized[tag] = normalized_tag

    return normalized

def categorize_tags(normalized_tags):
    """Categorize tags into logical groups."""
    categories = {
        'css': ['css', 'styling', 'design'],
        'markdown': ['markdown', 'markdown_to_html', 'markdown escaping'],
        'build': ['build', 'build script', 'site build', 'site successfully', 'markdown conversion in build'],
        'link_checker': ['link checker', 'link validation', 'link checker path resolution bug'],
        'github_pages': ['github pages', 'platform', 'live'],
        'documentation': ['documentation', 'docs', 'technical architecture documentation'],
        'testing': ['test', 'testing', 'validation', '81 test'],
        'tools': ['tools', 'tool_fix', 'web_fetch', 'search', 'validate'],
        'workflow': ['workflow', 'automation', 'automated'],
        'memory': ['memory', 'summarize'],
        'api': ['api', 'wikipedia', 'wikipedia api', 'the api would not answer'],
        'error': ['error', 'error_code', 'error_handling', 'bug', 'guarderror'],
        'performance': ['performance', 'performance platform'],
        'rollback': ['rollback', 'git', 'safety', 'safety validation rollback git python'],
        'agent': ['agent', 'agents'],
        'blog': ['blog', 'post', 'first post', 'the digital garden and corrected blog post dates'],
        'python': ['python'],
        'frameworks': ['frameworks', 'llm'],
        'discovery': ['discovery', 'that doc', 'that docs'],
        'template': ['template', 'template var'],
        'navigation': ['navigation', 'nav bar problem', 'website navigation'],
    }

    categorized = defaultdict(list)
    for tag, normalized in normalized_tags.items():
        found = False
        for category, keywords in categories.items():
            if any(keyword in tag.lower() for keyword in keywords):
                categorized[category].append(tag)
                found = True
                break
        if not found:
            categorized['misc'].append(tag)

    return categorized

def generate_tag_hierarchy(categorized):
    """Generate a hierarchical tag structure."""
    hierarchy = {
        'development': ['css', 'markdown', 'build', 'link_checker', 'github_pages'],
        'testing': ['testing', 'validation'],
        'tools': ['tools', 'web_fetch', 'search', 'validate'],
        'documentation': ['documentation', 'docs', 'template', 'navigation'],
        'agent': ['agent', 'agents', 'memory', 'summarize'],
        'platform': ['github_pages', 'api', 'python', 'frameworks'],
        'issues': ['error', 'bug', 'guarderror', 'rollback', 'safety'],
        'workflow': ['workflow', 'automation', 'automated'],
        'blog': ['blog', 'post'],
        'discovery': ['discovery', 'that doc', 'that docs'],
        'performance': ['performance'],
    }

    return hierarchy

def main():
    """Main execution."""
    html_file = 'docs/knowledge_base.html'

    print("Extracting tags from knowledge base...")
    all_tags, tag_entries = extract_tags_from_html(html_file)

    print(f"\nFound {len(all_tags)} unique tags")
    print(f"Found {len(tag_entries)} tag entries")

    print("\nOriginal tags:")
    for tag in sorted(all_tags):
        print(f"  - {tag}")

    print("\nNormalizing tags...")
    normalized = normalize_tags(all_tags)
    print(f"\nNormalized to {len(normalized)} unique tags")

    print("\nNormalized tags:")
    for tag, normalized in sorted(normalized.items()):
        if tag != normalized:
            print(f"  {tag} → {normalized}")

    print("\nCategorizing tags...")
    categorized = categorize_tags(normalized)
    print(f"\nFound {len(categorized)} categories")

    for category, tags in sorted(categorized.items()):
        if tags:
            print(f"  {category}: {len(tags)} tags")
            for tag in tags:
                print(f"    - {tag}")

    print("\nGenerating tag hierarchy...")
    hierarchy = generate_tag_hierarchy(categorized)
    print(f"\nTag hierarchy has {len(hierarchy)} top-level categories")

    for category, subtags in sorted(hierarchy.items()):
        if subtags:
            print(f"  {category}: {len(subtags)} subcategories")
            for subtag in subtags:
                print(f"    - {subtag}")

    # Save results
    with open('agent/tag_analysis.txt', 'w') as f:
        f.write("TAG ANALYSIS RESULTS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Original tags: {len(all_tags)}\n")
        f.write(f"Normalized tags: {len(normalized)}\n")
        f.write(f"Categories: {len(categorized)}\n")
        f.write(f"Hierarchy levels: {len(hierarchy)}\n\n")

        f.write("CATEGORIES:\n")
        for category, tags in sorted(categorized.items()):
            if tags:
                f.write(f"\n{category} ({len(tags)} tags):\n")
                for tag in tags:
                    f.write(f"  - {tag}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("TAG HIERARCHY:\n")
        for category, subtags in sorted(hierarchy.items()):
            if subtags:
                f.write(f"\n{category}:\n")
                for subtag in subtags:
                    f.write(f"  - {subtag}\n")

    print("\nResults saved to agent/tag_analysis.txt")

if __name__ == '__main__':
    main()
