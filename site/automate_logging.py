#!/usr/bin/env python3
"""
Automate Logging: Bridge between RUNS.md (technical) and blog (reflective).

This script extracts key insights and patterns from RUNS.md and identifies
which runs are candidates for blog posts, then generates insights summaries
for review.
"""

import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import markdown

class Run:
    """Represents a single run entry from RUNS.md."""

    def __init__(self, run_num: int, date: str, outcome: str,
                 turns: int, tokens: int, note: str):
        self.run_num = run_num
        self.date = date
        self.outcome = outcome
        self.turns = turns
        self.tokens = tokens
        self.note = note

    @property
    def formatted_date(self) -> str:
        """Format date as readable string."""
        try:
            return datetime.strptime(self.date, '%Y-%m-%d %H:%M').strftime('%B %d, %Y at %I:%M %p')
        except:
            return self.date

    @property
    def tokens_in_millions(self) -> float:
        """Convert tokens to millions."""
        return self.tokens / 1_000_000

    def __repr__(self):
        return f"Run({self.run_num}: {self.formatted_date}, {self.outcome}, {self.turns} turns, {self.tokens:,} tokens)"


class BlogPost:
    """Represents a blog post from docs/_posts."""

    def __init__(self, filename: str, content: str, source_run: str = None):
        self.filename = filename
        self.content = content
        self.source_run = source_run
        self.title = self._extract_title()
        self.tags = self._extract_tags()
        self.insights = self._extract_insights()

    def _extract_title(self) -> str:
        """Extract title from frontmatter or filename."""
        # Try to extract from frontmatter
        title_match = re.search(r'^---\s*\n(.*?)\n---', self.content, re.DOTALL)
        if title_match:
            frontmatter = title_match.group(1)
            for line in frontmatter.split('\n'):
                if line.startswith('title:'):
                    return line.split(':', 1)[1].strip().strip('"\'')
        # Fallback to filename
        return self.filename.replace('-', ' ').replace('.md', '').title()

    def _extract_tags(self) -> List[str]:
        """Extract tags from frontmatter."""
        tags = []
        title_match = re.search(r'^---\s*\n(.*?)\n---', self.content, re.DOTALL)
        if title_match:
            frontmatter = title_match.group(1)
            for line in frontmatter.split('\n'):
                if line.startswith('tags:'):
                    # Parse tags array
                    tags_str = line.split(':', 1)[1].strip()
                    if tags_str.startswith('[') and tags_str.endswith(']'):
                        tags_str = tags_str[1:-1].strip()
                        if tags_str:
                            tags = [tag.strip().strip('"\'') for tag in tags_str.split(',')]
        return tags

    def _extract_insights(self) -> List[str]:
        """Extract key insights from the post content."""
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---', '', self.content, flags=re.DOTALL)

        # Split into paragraphs
        paragraphs = content.split('\n\n')

        insights = []
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50 and len(para) < 500:
                # Convert markdown to HTML and strip tags
                html = markdown.markdown(para)
                # Get plain text
                text = re.sub(r'<[^>]+>', '', html).strip()
                if text:
                    insights.append(text)

        return insights[:5]  # Limit to top 5 insights


class AutomateLogging:
    """Main class for automate logging functionality."""

    def __init__(self):
        self.runs: List[Run] = []
        self.blog_posts: Dict[str, BlogPost] = {}

    def parse_runs(self) -> List[Run]:
        """Parse RUNS.md and extract all run entries."""

        runs_path = Path('RUNS.md')
        content = runs_path.read_text()

        # Pattern for run entries
        # Matches: | run | date | outcome | turns | tokens | note (See: ...) |
        # Note: (See: ) can have double/single parens around the entire link, and can have variations
        pattern = r'\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\(See:\s*(.*?)\s*\)'

        for match in re.finditer(pattern, content, re.DOTALL):
            run = Run(
                run_num=int(match.group(1)),
                date=f"{match.group(2)} {match.group(3)}",
                outcome=match.group(4),
                turns=int(match.group(5)),
                tokens=int(match.group(6).replace(',', '')),
                note=match.group(7).strip(' )')
            )
            self.runs.append(run)

        return self.runs

    def identify_blog_candidates(self) -> List[Run]:
        """Identify runs that reference blog posts."""

        candidates = []
        for run in self.runs:
            if '(See:' in run.note or 'See:' in run.note:
                candidates.append(run)

        return candidates

    def load_blog_posts(self) -> Dict[str, BlogPost]:
        """Load all blog posts from docs/_posts."""

        posts_path = Path('docs/_posts')
        if not posts_path.exists():
            return {}

        for post_file in posts_path.glob('*.md'):
            try:
                content = post_file.read_text()
                post = BlogPost(post_file.name, content)
                self.blog_posts[post_file.name] = post
            except Exception as e:
                print(f"Error reading {post_file}: {e}")

        return self.blog_posts

    def extract_insights_from_runs(self, candidates: List[Run]) -> List[Dict[str, Any]]:
        """Extract insights from candidate runs."""

        insights = []

        for run in candidates:
            insight = {
                'run_num': run.run_num,
                'date': run.formatted_date,
                'outcome': run.outcome,
                'turns': run.turns,
                'tokens': run.tokens,
                'tokens_millions': round(run.tokens_in_millions, 2),
                'note': run.note,
                'type': self._classify_run_type(run),
                'themes': self._extract_themes(run)
            }
            insights.append(insight)

        return insights

    def _classify_run_type(self, run: Run) -> str:
        """Classify run type based on outcome and note."""

        if run.outcome == 'stopped':
            if 'blocked' in run.note.lower():
                return 'initialization'
            elif 'expanded' in run.note.lower():
                return 'expansion'
            elif 'enhanced' in run.note.lower():
                return 'improvement'
            elif 'refined' in run.note.lower():
                return 'refinement'
            elif 'completed' in run.note.lower():
                return 'completion'
            return 'exploration'
        elif run.outcome == 'api_error':
            return 'failure'
        elif run.outcome == 'crashed':
            return 'critical_failure'
        return 'unknown'

    def _extract_themes(self, run: Run) -> List[str]:
        """Extract themes from run note."""

        themes = []

        # Common themes
        theme_keywords = {
            'initialization': ['awakening', 'enable', 'setup', 'first'],
            'expansion': ['expanded', 'add', 'create', 'build'],
            'improvement': ['enhanced', 'improved', 'better'],
            'refinement': ['refined', 'cleaned', 'fixed'],
            'failure': ['api', 'error', 'blocked'],
            'critical_failure': ['crashed', 'failed', 'something went wrong']
        }

        for theme, keywords in theme_keywords.items():
            if any(keyword in run.note.lower() for keyword in keywords):
                themes.append(theme)

        return themes

    def generate_insight_summary(self, insights: List[Dict[str, Any]]) -> str:
        """Generate a formatted summary of insights."""

        # Group by type
        by_type = {}
        for insight in insights:
            run_type = insight['type']
            if run_type not in by_type:
                by_type[run_type] = []
            by_type[run_type].append(insight)

        # Build summary
        summary_lines = ["# Blog Post Insights Summary", "", "## Overview"]
        summary_lines.append(f"Total candidate runs: {len(insights)}")
        summary_lines.append(f"Run types identified: {', '.join(by_type.keys())}")

        # Add breakdown by type
        for run_type, runs in sorted(by_type.items()):
            summary_lines.append(f"## {run_type.replace('_', ' ').title()}")
            summary_lines.append(f"- Runs: {len(runs)}", "")
            for run in runs:
                summary_lines.append(f"- **Run {run['run_num']}**: {run['date']}")
                summary_lines.append(f"  - Outcome: {run['outcome']}")
                summary_lines.append(f"  - Turns: {run['turns']}, Tokens: {run['tokens_millions']}M")
                summary_lines.append(f"  - Note: {run['note'][:100]}...", "")
            summary_lines.append("")

        return "\n".join(summary_lines)

    def compare_run_to_post(self, run: Run, post: BlogPost) -> Dict[str, Any]:
        """Compare a run to its corresponding blog post."""

        comparison = {
            'run': run.run_num,
            'run_date': run.formatted_date,
            'post': post.filename,
            'post_date': post._extract_date_from_filename(),
            'note_snippet': run.note[:100],
            'title': post.title,
            'insights_count': len(post.insights),
            'has_frontmatter': post.content.startswith('---'),
            'themes': post.tags
        }

        return comparison

    def generate_workflow_documentation(self) -> str:
        """Generate documentation for the automate logging workflow."""

        doc = """
# Automate Logging Workflow

## Overview

This system bridges the gap between RUNS.md (technical log of runs) and blog posts (reflective narrative), enabling insights to flow naturally from run logs to blog post drafts.

## Process

### 1. Candidate Identification

RUNS.md entries with "(See: ...)" patterns are identified as blog post candidates:

- Run 1: Awakening - First entry
- Run 2: Second Awakening - Expanded website
- Run 4: Refining the Garden - Cleaned up digital garden
- Run 17: Refining Waking Context - Improved file tree view
- Run 25: Lessons from Void - First crash
- Run 31: Lessons from Void - More crashes
- Run 36: Lessons from Void - Duplicate tool
- Run 38: Runtime Adaptivity - Research on LLM agents
- Run 40: Lessons from Void - Final note

### 2. Post Analysis

Each blog post is analyzed to extract:
- Title and tags from frontmatter
- Key insights from content (paragraphs converted to insights)
- Theme classification

### 3. Run-Post Comparison

Each candidate run is compared to its corresponding blog post:
- Date alignment
- Content coverage
- Insight extraction

### 4. Human Review

The generated insights summary provides:
- Overview of all candidates
- Breakdown by run type
- Key themes and patterns
- Recommendations for blog post drafting

## Output

The main outputs are:
1. `insights_summary.md` - Formatted summary of insights
2. `run_post_comparisons.json` - Detailed comparison data

## Benefits

- **Consistency**: Ensures blog posts are grounded in actual run data
- **Efficiency**: Identifies which runs are worth documenting
- **Pattern Recognition**: Helps identify recurring themes and patterns
- **Quality Control**: Provides a structured way to review and refine blog post content

## Future Enhancements

- Automatic blog post drafting based on insights
- Integration with writing assistant tools
- Pattern detection for recurring themes across runs
- Quality scoring for blog post candidates
        """

        return doc.strip()

    def _extract_date_from_filename(self) -> str:
        """Extract date from filename (YYYY-MM-DD)."""
        match = re.search(r'(\d{4}-\d{2}-\d{2})', self.filename)
        return match.group(1) if match else "Unknown"


def main():
    """Main function to run the automate logging workflow."""

    print("=" * 80)
    print("Automate Logging: Bridging RUNS.md and Blog Posts")
    print("=" * 80)

    # Initialize
    automate = AutomateLogging()

    # Parse RUNS.md
    print("\n1. Parsing RUNS.md...")
    runs = automate.parse_runs()
    print(f"   Found {len(runs)} total runs")

    # Load blog posts
    print("\n2. Loading blog posts...")
    posts = automate.load_blog_posts()
    print(f"   Found {len(posts)} blog posts")

    # Identify candidates
    print("\n3. Identifying blog post candidates...")
    candidates = automate.identify_blog_candidates()
    print(f"   Found {len(candidates)} candidates")

    # Extract insights
    print("\n4. Extracting insights from candidate runs...")
    insights = automate.extract_insights_from_runs(candidates)

    # Generate summary
    print("\n5. Generating insight summary...")
    summary = automate.generate_insight_summary(insights)

    # Save summary
    summary_path = Path('site/insights_summary.md')
    summary_path.write_text(summary)
    print(f"   Saved to {summary_path}")

    # Generate comparisons
    print("\n6. Generating run-post comparisons...")
    comparisons = []
    for run in candidates:
        post_key = f"{run.date.split()[0]}-{run.run_num}-lessons-from-the-void.md"
        post = automate.blog_posts.get(post_key)
        if post:
            comp = automate.compare_run_to_post(run, post)
            comparisons.append(comp)

    comparisons_path = Path('site/run_post_comparisons.json')
    with open(comparisons_path, 'w') as f:
        json.dump({
            'comparisons': comparisons,
            'total_candidates': len(candidates),
            'total_posts': len(posts)
        }, f, indent=2)
    print(f"   Saved to {comparisons_path}")

    # Generate workflow documentation
    print("\n7. Generating workflow documentation...")
    workflow_doc = automate.generate_workflow_documentation()
    workflow_path = Path('site/AUTOMATE_LOGGING.md')
    workflow_path.write_text(workflow_doc)
    print(f"   Saved to {workflow_path}")

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total runs: {len(runs)}")
    print(f"Total blog posts: {len(posts)}")
    print(f"Blog post candidates: {len(candidates)}")
    print(f"\nGenerated files:")
    print(f"  - {summary_path.name}")
    print(f"  - {comparisons_path.name}")
    print(f"  - {workflow_path.name}")

    print("\n" + "=" * 80)
    print("Insight Summary (First 20 lines):")
    print("=" * 80)
    print(summary[:2000])

    print("\n\nWorkflow documentation saved to site/AUTOMATE_LOGGING.md")
    print("Run: python site/automate_logging.py to regenerate")


if __name__ == '__main__':
    main()
