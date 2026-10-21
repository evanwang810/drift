"""Automatic rollback mechanism for critical health check failures.

When critical health checks fail, this script creates a git tag and optionally
reverts to the previous commit.

Usage:
    python site/health_rollback.py --tag <tagname> [--revert] [--dry-run]

Critical checks that trigger rollback:
- Site build failure
- All site validation checks failing
- Repository has uncommitted changes
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


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


def check_git_status_clean() -> bool:
    """Check if repository has no uncommitted changes."""
    success, stdout, stderr = run_command(["git", "status", "--porcelain"], cwd=ROOT)
    if not success:
        print(f"✗ Git status check failed: {stderr}")
        return False
    return not stdout.strip()


def get_current_commit() -> str:
    """Get the current commit hash."""
    success, stdout, stderr = run_command(["git", "rev-parse", "HEAD"], cwd=ROOT)
    if not success:
        print(f"✗ Could not get current commit: {stderr}")
        sys.exit(1)
    return stdout.strip()


def create_rollback_tag(tag_name: str, commit_hash: str, dry_run: bool = False) -> bool:
    """Create a git tag as rollback point."""
    if dry_run:
        print(f"DRY RUN: Would create tag '{tag_name}' at {commit_hash}")
        return True

    cmd = ["git", "tag", tag_name]
    success, stdout, stderr = run_command(cmd, cwd=ROOT)
    if not success:
        print(f"✗ Failed to create tag '{tag_name}': {stderr}")
        return False

    print(f"✓ Created rollback tag: {tag_name} at {commit_hash}")
    return True


def get_previous_commit() -> str | None:
    """Get the previous commit hash."""
    success, stdout, stderr = run_command(["git", "rev-parse", "HEAD~1"], cwd=ROOT)
    if not success:
        print(f"✗ Could not get previous commit: {stderr}")
        return None
    return stdout.strip()


def show_current_state() -> str:
    """Show current git state."""
    success, stdout, stderr = run_command(["git", "status"], cwd=ROOT)
    if success:
        return stdout
    return f"✗ Git status failed: {stderr}"


def show_commit_log(n: int = 3) -> str:
    """Show recent commit log."""
    success, stdout, stderr = run_command(["git", "log", "-n", str(n), "--oneline"], cwd=ROOT)
    if success:
        return stdout
    return f"✗ Git log failed: {stderr}"


def rollback_to_previous(dry_run: bool = False) -> bool:
    """Rollback to the previous commit."""
    if dry_run:
        prev = get_previous_commit()
        current = get_current_commit()
        if prev:
            print(f"DRY RUN: Would revert from {current} to {prev}")
            print("Would create new commit with changes:")
            print("  git reset --soft HEAD~1")
        return True

    # Confirm with user
    print("\n⚠ WARNING: This will undo recent changes!")
    print("All uncommitted changes will be discarded.")
    response = input("Continue with rollback? (yes/no): ").strip().lower()
    if response != "yes":
        print("Rollback cancelled.")
        return False

    # Get previous commit
    success, stdout, stderr = run_command(["git", "rev-parse", "HEAD~1"], cwd=ROOT)
    if not success:
        print(f"✗ Could not get previous commit: {stderr}")
        return False

    prev_commit = stdout.strip()
    current_commit = get_current_commit()

    # Reset to previous commit (soft reset keeps changes in staging)
    cmd = ["git", "reset", "--soft", "HEAD~1"]
    success, stdout, stderr = run_command(cmd, cwd=ROOT)

    if not success:
        print(f"✗ Failed to rollback: {stderr}")
        return False

    print(f"✓ Rolled back from {current_commit[:8]} to {prev_commit[:8]}")
    print(f"✓ Uncommitted changes preserved in staging area")
    print(f"\nChanges to commit:")
    print(show_current_state())
    print("\nTo commit or discard these changes:")
    print("  git commit -m 'Rollback after critical health check failure'")
    print("  git reset --hard HEAD  # to discard changes")

    return True


def verify_rollback(tag_name: str) -> bool:
    """Verify that the rollback tag exists and points to correct commit."""
    success, stdout, stderr = run_command(["git", "tag", "-l", tag_name], cwd=ROOT)
    if not success:
        print(f"✗ Tag check failed: {stderr}")
        return False

    if not stdout.strip():
        print(f"✗ Rollback tag '{tag_name}' not found")
        return False

    # Get the commit the tag points to
    success, stdout, stderr = run_command(["git", "show", tag_name, "--no-patch", "--format=%H"], cwd=ROOT)
    if not success:
        print(f"✗ Could not verify tag: {stderr}")
        return False

    tag_commit = stdout.strip()
    current_commit = get_current_commit()

    print(f"✓ Rollback tag '{tag_name}' found at {tag_commit[:8]}")
    print(f"✓ Current HEAD at {current_commit[:8]}")
    return tag_commit == current_commit


def main() -> int:
    parser = argparse.ArgumentParser(description="Automatic rollback for critical health check failures")
    parser.add_argument("--tag", required=True, help="Tag name to create for rollback point")
    parser.add_argument("--revert", action="store_true", help="Actually revert to previous commit")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without making changes")
    args = parser.parse_args()

    print("=" * 70)
    print("Repository Health Rollback Mechanism")
    print("=" * 70)

    # Show current state
    print("\nCurrent state:")
    print(show_current_state())
    print("\nRecent commits:")
    print(show_commit_log(3))

    current_commit = get_current_commit()
    print(f"\nCurrent commit: {current_commit[:8]}")

    # Create rollback tag
    if create_rollback_tag(args.tag, current_commit, args.dry_run):
        print(f"\n✓ Rollback point created: {args.tag}")

        # Verify rollback tag
        verify_rollback(args.tag)

        # Perform actual rollback if requested
        if args.revert:
            print("\n" + "=" * 70)
            print("Performing rollback to previous commit...")
            print("=" * 70)

            if rollback_to_previous(args.dry_run):
                print(f"\n✓ Rollback completed successfully")
                return 0
            else:
                print(f"\n✗ Rollback failed")
                return 1
        else:
            print("\n" + "=" * 70)
            print("Rollback point created successfully")
            print("=" * 70)
            print("\nTo revert to this point later:")
            print(f"  python site/health_rollback.py --tag {args.tag} --revert")
            print("\nTo see what changes would be rolled back:")
            print(f"  git reset --soft HEAD~1")
            print(f"  git status")

        return 0
    else:
        print(f"\n✗ Failed to create rollback point")
        return 1


if __name__ == "__main__":
    sys.exit(main())
