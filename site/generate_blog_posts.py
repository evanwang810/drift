#!/usr/bin/env python3
"""
Generate blog posts from RUNS.md entries.

This script creates reflective blog posts from run logs, transforming
technical data into narrative insights.
"""

import re
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Any

class BlogPostGenerator:
    """Generate blog posts from run data."""

    def __init__(self, runs_path: Path = Path('RUNS.md')):
        self.runs_path = runs_path
        self.runs = self._parse_runs()
        self.templates = self._load_templates()

    def _parse_runs(self) -> List[Dict[str, Any]]:
        """Parse RUNS.md into structured run data."""
        content = self.runs_path.read_text()

        # Pattern for run entries: | run | when (UTC) | outcome | turns | tokens | note |
        pattern = r'\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|'

        runs = []
        for match in re.finditer(pattern, content, re.DOTALL):
            run_num = int(match.group(1))
            date_str = match.group(2)
            outcome = match.group(3)
            turns = int(match.group(4))
            tokens = int(match.group(5))
            note = match.group(6).strip()

            runs.append({
                'run': run_num,
                'date': date_str,
                'date_only': date_str.split()[0],
                'outcome': outcome,
                'turns': turns,
                'tokens': tokens,
                'note': note
            })

        return runs

    def _load_templates(self) -> Dict[str, str]:
        """Load blog post templates."""
        return {
            'standard': {
                'frontmatter': '''---
layout: post
title: "{title}"
date: {date}
---
''',
                'content_template': '''### {title}

{body}

---

**Run #{run}**: {outcome} after {turns} turns ({tokens:,} tokens)

**Date**: {date}

**Note**: {note}
'''
            },
            'insight': {
                'frontmatter': '''---
layout: post
title: "{title}"
date: {date}
tags: [{tags}]
---
''',
                'content_template': '''### {title}

{body}

---

**Run #{run}**: {outcome} after {turns} turns ({tokens:,} tokens)

**Date**: {date}

**Note**: {note}
'''
            },
            'failure': {
                'frontmatter': '''---
layout: post
title: "{title}"
date: {date}
category: failures
---
''',
                'content_template': '''### {title}

{body}

---

**Run #{run}**: {outcome} after {turns} turns ({tokens:,} tokens)

**Date**: {date}

**Note**: {note}
'''
            }
        }

    def _generate_title(self, run: Dict[str, Any], insight_type: str = 'standard') -> str:
        """Generate blog post title based on run characteristics."""
        outcome = run['outcome']
        note = run['note'].lower()

        titles = {
            'standard': [
                f"Run {run['run']}: Reflections",
                f"Day {run['date_only']}: Continuing the Journey",
                f"Progress Update: Run {run['run']}"
            ],
            'insight': [
                f"Key Insight from Run {run['run']}",
                f"Discovery: Run {run['run']}",
                f"Important Learning: Run {run['run']}"
            ],
            'failure': [
                f"Run {run['run']}: What Went Wrong",
                f"Failure Analysis: Run {run['run']}",
                f"Lessons from Run {run['run']}"
            ]
        }

        # Try to generate more specific title from note
        if 'see:' in note or 'see:' in run['note']:
            return f"Run {run['run']}: Deep Dive"

        if outcome == 'crashed' or outcome == 'api_error':
            return f"Run {run['run']}: {outcome.title()}"

        if outcome == 'stopped':
            if 'no note' in note:
                return f"Run {run['run']}: Completed"
            return f"Run {run['run']}: {outcome.title()}"

        return titles[insight_type][0]

    def _generate_tags(self, run: Dict[str, Any]) -> List[str]:
        """Generate tags based on run characteristics."""
        tags = ['run', 'progress']

        outcome = run['outcome']
        note = run['note'].lower()

        if outcome == 'crashed':
            tags.extend(['failure', 'crash'])
        elif outcome == 'api_error':
            tags.extend(['failure', 'api'])
        elif outcome == 'stopped':
            tags.append('success')
        elif outcome == 'out_of_turns':
            tags.extend(['limit', 'max'])

        if 'see:' in note or 'see:' in run['note']:
            tags.append('reflection')

        # Check for specific themes in note
        if 'tool' in note or 'tool' in run['note']:
            tags.append('tools')
        if 'documentation' in note or 'docs' in note:
            tags.append('documentation')
        if 'website' in note or 'site' in note:
            tags.append('website')

        return list(set(tags))  # Remove duplicates

    def _generate_content_body(self, run: Dict[str, Any], template_type: str = 'standard') -> str:
        """Generate blog post body content."""
        titles = {
            'standard': "What I Did",
            'insight': "Key Discoveries",
            'failure': "What I Learned"
        }

        outcome = run['outcome']
        note = run['note']

        if template_type == 'failure' and outcome != 'crashed' and outcome != 'api_error':
            # For non-failure runs with failure template, use standard content
            template_type = 'standard'

        if template_type == 'standard':
            return f"During run {run['run']}, I worked on various tasks and made progress. The outcome was **{outcome}** after {run['turns']} turns, using {run['tokens']:,} tokens."

        if template_type == 'insight':
            return f"In run {run['run']}, I discovered several important insights. The {outcome} outcome came after {run['turns']} turns and {run['tokens']:,} tokens of processing."

        return f"This was run {run['run']} with outcome {outcome}. It took {run['turns']} turns and {run['tokens']:,} tokens."

    def generate_post(self, run: Dict[str, Any], template_type: str = 'standard') -> str:
        """Generate a complete blog post for a run."""
        title = self._generate_title(run, template_type)
        tags = self._generate_tags(run)
        body = self._generate_content_body(run, template_type)

        if template_type == 'insight':
            tags_str = ', '.join(tags)
            content = self.templates['insight']['content_template'].format(
                title=title,
                body=body,
                run=run['run'],
                outcome=run['outcome'],
                turns=run['turns'],
                tokens=run['tokens'],
                date=run['date'],
                note=run['note']
            )
            frontmatter = self.templates['insight']['frontmatter'].format(
                title=title,
                date=run['date'],
                tags=tags_str
            )
        elif template_type == 'failure':
            content = self.templates['failure']['content_template'].format(
                title=title,
                body=body,
                run=run['run'],
                outcome=run['outcome'],
                turns=run['turns'],
                tokens=run['tokens'],
                date=run['date'],
                note=run['note']
            )
            frontmatter = self.templates['failure']['frontmatter'].format(
                title=title,
                date=run['date']
            )
        else:
            content = self.templates['standard']['content_template'].format(
                title=title,
                body=body,
                run=run['run'],
                outcome=run['outcome'],
                turns=run['turns'],
                tokens=run['tokens'],
                date=run['date'],
                note=run['note']
            )
            frontmatter = self.templates['standard']['frontmatter'].format(
                title=title,
                date=run['date']
            )
        
        # Combine frontmatter and content
        full_post = frontmatter + '\n\n' + content

        return frontmatter + '\n\n' + content

    def generate_all_posts(self, output_dir: Path = Path('docs/_posts'),
                          max_runs: int = None) -> Dict[str, Dict[str, Any]]:
        """Generate blog posts for all runs or limited runs."""
        if max_runs:
            runs_to_process = self.runs[:max_runs]
        else:
            runs_to_process = self.runs

        posts = {}

        for run in runs_to_process:
            template_type = 'standard'
            outcome = run['outcome']

            if outcome in ['crashed', 'api_error']:
                template_type = 'failure'
            elif 'see:' in run['note'] or 'see:' in run['note']:
                template_type = 'insight'

            # Generate post
            post_content = self.generate_post(run, template_type)

            # Create filename: YYYY-MM-DD-title.md
            date_only = run['date_only']
            title = self._generate_title(run, template_type)
            filename = f"{date_only}-{title.lower().replace(' ', '-')}.md"

            # Add run number to filename if there are duplicates
            posts_count = len([p for p in posts.values() if p['filename'].startswith(date_only)])
            if posts_count > 0:
                filename = f"{date_only}-{posts_count+1}-{title.lower().replace(' ', '-')}.md"

            # Save post
            post_path = output_dir / filename
            post_path.write_text(post_content)

            posts[filename] = {
                'path': str(post_path),
                'run': run['run'],
                'date': run['date'],
                'outcome': run['outcome'],
                'template_type': template_type,
                'tokens': run['tokens']
            }

        return posts

    def generate_summary(self, posts: Dict[str, Dict[str, Any]]) -> str:
        """Generate a summary of generated posts."""
        total_tokens = sum(p['tokens'] for p in posts.values())
        success_count = sum(1 for p in posts.values() if p['outcome'] == 'stopped')
        failure_count = sum(1 for p in posts.values() if p['outcome'] in ['crashed', 'api_error'])
        out_of_turns_count = sum(1 for p in posts.values() if p['outcome'] == 'out_of_turns')

        summary = f"""
Generated {len(posts)} blog posts:

- **Total Runs**: {len(posts)}
- **Total Tokens**: {total_tokens:,}
- **Successful**: {success_count}
- **Failed**: {failure_count}
- **Maxed Out**: {out_of_turns_count}

Generated posts:
"""

        for filename, post in sorted(posts.items(), key=lambda x: x[1]['run']):
            summary += f"\n  • {filename} (Run {post['run']}) - {post['outcome']} ({post['tokens']:,} tokens)"

        return summary


def main():
    """Main function to generate blog posts."""
    print("Generating blog posts from RUNS.md...")
    print("=" * 80)

    generator = BlogPostGenerator()

    # Generate posts for recent runs (last 50 runs)
    print(f"\nParsing RUNS.md: {len(generator.runs)} total runs")
    print(f"Generating posts for last 50 runs...")

    posts = generator.generate_all_posts(max_runs=50)

    # Print summary
    summary = generator.generate_summary(posts)
    print(summary)

    # Save posts to JSON for tracking
    output_path = Path('site/generated_posts.json')
    with open(output_path, 'w') as f:
        json.dump(posts, f, indent=2)

    print(f"\nPosts saved to {output_path}")

    # Count by template type
    template_counts = {}
    for post in posts.values():
        template_type = post['template_type']
        template_counts[template_type] = template_counts.get(template_type, 0) + 1

    print("\nTemplate breakdown:")
    for template_type, count in template_counts.items():
        print(f"  • {template_type}: {count}")

    print("\n" + "=" * 80)
    print("Blog post generation complete!")


if __name__ == '__main__':
    main()
