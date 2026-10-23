"""Blog post generator from RUNS.md entries.

This module reads RUNS.md and generates meaningful blog posts from run entries.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import re


def parse_runs(md_path: Path) -> List[Dict]:
    """Parse RUNS.md and return list of run dictionaries.

    Args:
        md_path: Path to RUNS.md file

    Returns:
        List of run dictionaries with run number, date, outcome, turns, tokens, note
    """
    content = md_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    runs = []

    # Find the header line
    header_line = None
    for i, line in enumerate(lines):
        if line.startswith("| run |"):
            header_line = i
            break

    if header_line is None:
        raise ValueError("RUNS.md does not contain expected header '| run |'")

    for line_num, line in enumerate(lines):
        # Skip header and separator lines
        if line_num == header_line or line.startswith("| --"):
            continue

        # Skip empty lines
        if not line.strip():
            continue

        # Parse the row
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 6:
            continue

        try:
            run_num = int(parts[0])
            runs.append({
                "run": run_num,
                "when": parts[1],
                "outcome": parts[2],
                "turns": int(parts[3]) if parts[3] else 0,
                "tokens": int(parts[4].replace(",", "")) if parts[4] else 0,
                "note": parts[5] if len(parts) > 5 else ""
            })
        except (ValueError, IndexError):
            continue

    return runs


def extract_title(note: str) -> str:
    """Extract a meaningful title from a run note.

    Args:
        note: The run note text

    Returns:
        A title string that is meaningful and not just "run X: api_error"
    """
    if not note:
        return f"Run {note}"  # Will be caught as fallback

    # Remove "See:" references
    note = re.sub(r'\(See:.*?\)', '', note)
    note = note.strip()

    # If it's just a generic error message, generate something better
    if "api would not answer" in note.lower():
        return "API Unresponsive"
    if "something went wrong" in note.lower():
        return "System Error"

    # Try to extract a title from the note
    # Look for patterns like "Added X", "Fixed Y", "Created Z", etc.
    verbs = ["added", "fixed", "created", "implemented", "enhanced", "improved",
             "developed", "refined", "expanded", "optimized", "documented"]

    for verb in verbs:
        if note.lower().startswith(verb):
            # Remove the verb and get the rest
            title = note[len(verb):].strip()
            # Capitalize first letter
            title = title[0].upper() + title[1:].lower() if title else "Untitled"
            return title

    # If note is very short, use a generic title
    if len(note) < 50:
        return "Run Entry"

    # Otherwise use the first few words
    words = note.split()[:5]
    return " ".join(words)


def generate_post_content(run: Dict) -> Tuple[str, str]:
    """Generate blog post content from a run entry.

    Args:
        run: Dictionary with run information

    Returns:
        Tuple of (frontmatter, body) for the blog post
    """
    run_num = run["run"]
    when = run["when"]
    outcome = run["outcome"]
    turns = run["turns"]
    tokens = run["tokens"]
    note = run["note"]

    # Clean up the note
    note = re.sub(r'\(See:.*?\)', '', note)
    note = note.strip()

    # Generate a meaningful title
    title = extract_title(note) if note else f"Run {run_num}"

    # Generate body content
    body_parts = [
        f"# {title}",
        "",
        f"**Run {run_num}** | {when} | {outcome} | {turns} turns | {tokens:,} tokens",
        "",
        "## Context",
        "",
    ]

    # Add context about what happened
    if outcome == "stopped":
        body_parts.append("This run completed successfully. The system executed the planned work and then stopped.")
    elif outcome == "api_error":
        body_parts.append("This run encountered an API error and could not complete.")
    elif outcome == "crashed":
        body_parts.append("This run crashed unexpectedly.")
    else:
        body_parts.append(f"This run ended with outcome: {outcome}")

    body_parts.extend([
        "",
        "## Details",
        "",
        f"- **Date**: {when}",
        f"- **Outcome**: {outcome}",
        f"- **Duration**: {turns} turns",
        f"- **Token Usage**: {tokens:,} tokens",
        "",
    ])

    # Add the note if it has substantive content
    if note and len(note) > 20:
        body_parts.extend([
            "## Notes",
            "",
            note,
        ])

    # Add recommendations or next steps based on outcome
    body_parts.extend([
        "",
        "## Next Steps",
        "",
    ])

    if outcome == "api_error":
        body_parts.append("- Check API connectivity and rate limits")
        body_parts.append("- Review error logs for root cause")
    elif outcome == "crashed":
        body_parts.append("- Review crash logs")
        body_parts.append("- Add error handling for edge cases")
    elif outcome == "stopped":
        body_parts.append("- Review completed work")
        body_parts.append("- Document any learnings or discoveries")
        body_parts.append("- Consider next steps for improvement")

    body = "\n".join(body_parts)

    # Generate frontmatter
    date = when.split()[0] if when else "2026-10-23"
    frontmatter = f"""---
title: "{title}"
date: {date}
run: {run_num}
outcome: {outcome}
turns: {turns}
tokens: {tokens}
---

"""

    return frontmatter, body


def generate_posts(posts_dir: Path = Path("docs/_posts"), max_runs: int = 50) -> Dict[str, Dict]:
    """Generate blog posts from RUNS.md.

    Args:
        posts_dir: Directory to save blog posts
        max_runs: Number of recent runs to generate posts for (default 50)

    Returns:
        Dictionary mapping filenames to post information
    """
    # Parse RUNS.md
    runs_path = Path("RUNS.md")
    if not runs_path.exists():
        print("Error: RUNS.md not found")
        return {}

    runs = parse_runs(runs_path)
    if not runs:
        print("Error: No runs found in RUNS.md")
        return {}

    # Get most recent runs
    recent_runs = runs[-max_runs:]

    print(f"Generating posts for {len(recent_runs)} most recent runs...")

    posts = {}
    skip_count = 0

    for run in recent_runs:
        run_num = run["run"]
        date_str = run["when"].split()[0] if run["when"] else "2026-10-23"

        # Generate filename
        title = extract_title(run["note"])
        # Sanitize title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
        safe_title = re.sub(r'[\s-]+', '-', safe_title)
        if not safe_title:
            safe_title = f"run-{run_num}"
        filename = f"{date_str}-{safe_title}.md"

        # Check if file already exists
        if (posts_dir / filename).exists():
            print(f"  Skipped existing: {filename} (Run {run_num})")
            skip_count += 1
            continue

        # Generate post content
        frontmatter, body = generate_post_content(run)

        # Write file
        file_path = posts_dir / filename
        file_path.write_text(frontmatter + body, encoding="utf-8")

        print(f"  Generated: {filename} (Run {run_num})")
        posts[filename] = {
            "run": run_num,
            "title": title,
            "date": date_str
        }

    print(f"\nGenerated {len(posts)} new posts, skipped {skip_count} existing ones")
    return posts


class BlogPostGenerator:
    """Blog post generator class for generating posts from RUNS.md."""

    def __init__(self):
        self.runs = []

    def parse_runs(self, md_path: Path) -> List[Dict]:
        """Parse RUNS.md and return list of run dictionaries."""
        return parse_runs(md_path)

    def extract_title(self, note: str) -> str:
        """Extract a meaningful title from a run note."""
        return extract_title(note)

    def generate_post_content(self, run: Dict) -> Tuple[str, str]:
        """Generate blog post content from a run entry."""
        return generate_post_content(run)

    def generate_posts(self, posts_dir: Path = Path("docs/_posts"), max_runs: int = 50) -> Dict[str, Dict]:
        """Generate blog posts from RUNS.md."""
        return generate_posts(posts_dir, max_runs)

    def generate_all_posts(self, posts_dir: Path, max_runs: int = 50) -> Dict[str, Dict]:
        """Generate all posts - alias for compatibility."""
        return self.generate_posts(posts_dir, max_runs)


if __name__ == "__main__":
    # Test the generator
    generator = BlogPostGenerator()
    posts = generator.generate_posts(max_runs=5)
    print(f"\nGenerated {len(posts)} posts")
