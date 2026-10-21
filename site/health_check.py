"""Automated health checks for the repository.

Run it from anywhere:
    python site/health_check.py [--live]

Checks:
1. Site builds successfully
2. All check_site.py validations pass
3. No uncommitted changes
4. Repository is clean and valid
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
LIVE = "https://evanwang810.github.io/drift/"


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[bool, str, str]:
    """Run a shell command and return success status, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_build_success(live: bool = False) -> tuple[bool, str]:
    """Check that the site builds successfully."""
    cmd = ["python", "site/build.py"]
    if live:
        cmd.append("--live")
    
    success, stdout, stderr = run_command(cmd, cwd=ROOT)
    if success:
        return True, "Site builds successfully"
    else:
        return False, f"Build failed: {stderr.strip()}"


def check_site_validations(live: bool = False) -> tuple[bool, str]:
    """Check that all site validation checks pass."""
    cmd = ["python", "site/check_site.py"]
    if live:
        cmd.append("--live")
    
    success, stdout, stderr = run_command(cmd, cwd=ROOT)
    if success:
        # Count pass/fail
        lines = stdout.split('\n')
        pass_count = sum(1 for line in lines if line.strip().startswith("PASS"))
        return True, f"All site validations pass: {pass_count}/{len(lines)}"
    else:
        return False, f"Site validation failed:\n{stdout}"


def check_git_status() -> tuple[bool, str]:
    """Check that there are no uncommitted changes."""
    success, stdout, stderr = run_command(["git", "status", "--porcelain"], cwd=ROOT)
    if not success:
        return False, f"Git command failed: {stderr}"
    
    if stdout.strip():
        changed_files = [line[3:].strip() for line in stdout.strip().split('\n')]
        return False, f"Uncommitted changes: {', '.join(changed_files)}"
    else:
        return True, "Repository is clean (no uncommitted changes)"


def check_json_files() -> tuple[bool, str]:
    """Check that all JSON files are valid."""
    issues = []
    
    # Check RUNS.md structure
    runs_md = ROOT / "RUNS.md"
    if runs_md.exists():
        content = runs_md.read_text(encoding="utf-8")
        if "| run |" not in content:
            issues.append("RUNS.md missing expected table header")
        else:
            # Count data rows (not headers or separators)
            lines = content.split('\n')
            header_idx = next((i for i, line in enumerate(lines) if line.startswith("| run |")), -1)
            if header_idx >= 0:
                data_rows = sum(1 for line in lines[header_idx+1:] if line.startswith("| ") and "|" in line[1:3])
                if data_rows == 0:
                    issues.append("RUNS.md has no data rows")
    
    # Check knowledge_base.json
    kb_json = DOCS / "knowledge_base.json"
    if kb_json.exists():
        success, stdout, stderr = run_command(["python", "-m", "json.tool", str(kb_json)])
        if not success:
            issues.append(f"knowledge_base.json is invalid JSON: {stderr.strip()}")
    else:
        issues.append("knowledge_base.json not found")
    
    # Check runs.json if it exists
    runs_json = DOCS / "runs.json"
    if runs_json.exists():
        success, stdout, stderr = run_command(["python", "-m", "json.tool", str(runs_json)])
        if not success:
            issues.append(f"runs.json is invalid JSON: {stderr.strip()}")
    
    if issues:
        return False, "JSON validation issues:\n" + "\n".join(f"  - {issue}" for issue in issues)
    else:
        return True, "All JSON files are valid"


def check_no_colon_in_posts() -> tuple[bool, str]:
    """Check that no post files have colons in their names (Windows compatibility)."""
    posts_dir = DOCS / "_posts"
    if not posts_dir.exists():
        return True, "_posts directory not found (nothing to check)"
    
    colon_posts = []
    for post_file in posts_dir.glob("*.md"):
        if ":" in post_file.name:
            colon_posts.append(post_file.name)
    
    if colon_posts:
        return False, f"Posts with colons in names (Windows incompatible):\n  - " + "\n  - ".join(colon_posts)
    else:
        return True, "No posts have colons in names"


def check_post_naming() -> tuple[bool, str]:
    """Check that all posts follow YYYY-MM-DD-words-with-dashes naming convention."""
    posts_dir = DOCS / "_posts"
    if not posts_dir.exists():
        return True, "_posts directory not found (nothing to check)"
    
    invalid_posts = []
    for post_file in posts_dir.glob("*.md"):
        # Expected pattern: YYYY-MM-DD-title.md
        if not re.match(r'^\d{4}-\d{2}-\d{2}-[^/\\:*?"<>|]+\.(md|html)$', post_file.name):
            invalid_posts.append(post_file.name)
    
    if invalid_posts:
        return False, f"Posts with invalid naming:\n  - " + "\n  - ".join(invalid_posts[:5])
    else:
        return True, "All posts follow YYYY-MM-DD-title naming convention"


def check_no_duplicate_posts() -> tuple[bool, str]:
    """Check that no posts have duplicate titles."""
    posts_dir = DOCS / "_posts"
    if not posts_dir.exists():
        return True, "_posts directory not found (nothing to check)"
    
    titles = {}
    for post_file in posts_dir.glob("*.md"):
        # Extract title from file name (remove date prefix)
        name = post_file.stem
        # Date prefix is first 10 chars
        if len(name) >= 10:
            title_candidate = name[10:].replace("-", " ")
        else:
            title_candidate = name
        
        if title_candidate in titles:
            titles[title_candidate].append(post_file.name)
        else:
            titles[title_candidate] = [post_file.name]
    
    duplicates = {title: files for title, files in titles.items() if len(files) > 1}
    if duplicates:
        return False, f"Posts with duplicate titles:\n" + "\n".join(
            f"  '{title}': {', '.join(files)}" for title, files in duplicates.items()
        )
    else:
        return True, "No duplicate post titles"


def main() -> int:
    """Run all health checks and return exit code."""
    live = "--live" in sys.argv
    checks = [
        ("Build Success", check_build_success, live),
        ("Site Validations", check_site_validations, live),
        ("Git Status", check_git_status, None),
        ("JSON Files", check_json_files, None),
        ("No Colons in Posts", check_no_colon_in_posts, None),
        ("Post Naming", check_post_naming, None),
        ("No Duplicate Posts", check_no_duplicate_posts, None),
    ]
    
    results: list[tuple[bool, str]] = []
    
    for name, check_func, check_live in checks:
        live_arg = "--live" if check_live else ""
        try:
            success, message = check_func(live_arg)
            results.append((success, name, message))
            print(f"{'✓' if success else '✗'} {name}")
            print(f"  {message}")
        except Exception as e:
            results.append((False, name, f"Exception: {str(e)}"))
            print(f"✗ {name}")
            print(f"  Exception: {str(e)}")
        print()
    
    # Print summary
    passed = sum(1 for _, _, _ in results if _[0])
    total = len(results)
    print(f"\nHealth Check Summary: {passed}/{total} checks passed")
    
    if passed == total:
        print("✓ All health checks passed!")
        return 0
    else:
        print("✗ Some health checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
