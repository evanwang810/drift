"""Automatic rollback mechanism for critical health check failures.

This module provides functionality to automatically rollback the repository
to a previous commit when critical health checks fail.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class HealthRollback:
    """Handle automatic rollback on critical health failures."""

    def __init__(self):
        """Initialize rollback configuration."""
        self.enabled = os.getenv("HEALTH_ROLLBACK_ENABLED", "false").lower() == "true"
        self.rollback_on_critical = os.getenv("HEALTH_ROLLBACK_CRITICAL", "true").lower() == "true"
        self.rollback_on_all = os.getenv("HEALTH_ROLLBACK_ALL", "false").lower() == "true"
        self.rollback_tag = os.getenv("HEALTH_ROLLBACK_TAG", "health-check-failure")
        self.rollback_branch = os.getenv("HEALTH_ROLLBACK_BRANCH", "rollback-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.keep_commits = int(os.getenv("HEALTH_ROLLBACK_KEEP_COMMITS", "10"))

    def is_critical_failure(self, results: list[tuple[bool, str]]) -> bool:
        """Determine if failure is critical enough to trigger rollback.

        Critical failures include:
        - Missing index.html
        - Posts not rendering
        - Missing runs.json entries
        - Token counts missing
        - Dead links

        Args:
            results: List of (passed, message) tuples

        Returns:
            True if failure is critical
        """
        critical_messages = [
            "index.html exists",
            "every post renders",
            "runs.json has every run",
            "runs.json has token counts",
            "no dead links",
        ]

        for passed, message in results:
            if not passed:
                for critical in critical_messages:
                    if critical in message:
                        return True

        return False

    def create_rollback_tag(self, message: str) -> str:
        """Create a git tag for the rollback point.

        Args:
            message: Description of the failure

        Returns:
            Tag name created
        """
        tag_name = f"{self.rollback_tag}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        try:
            subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", message],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"✓ Created rollback tag: {tag_name}")
            return tag_name
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create tag: {e.stderr}")
            return ""

    def rollback_to_previous(self) -> bool:
        """Rollback to the previous commit.

        Returns:
            True if rollback was successful
        """
        try:
            # Get current commit
            current_commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                text=True,
                check=True,
            ).strip()

            # Get previous commit
            previous_commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD~1"],
                text=True,
                check=True,
            ).strip()

            print(f"Current commit: {current_commit}")
            print(f"Rolling back to: {previous_commit}")

            # Create rollback branch
            subprocess.run(
                ["git", "checkout", "-b", self.rollback_branch],
                check=True,
                capture_output=True,
            )
            print(f"✓ Created rollback branch: {self.rollback_branch}")

            # Hard reset to previous commit
            subprocess.run(
                ["git", "reset", "--hard", previous_commit],
                check=True,
                capture_output=True,
            )
            print(f"✓ Rolled back to commit: {previous_commit}")

            # Keep last N commits
            self._keep_last_commits()

            return True

        except subprocess.CalledProcessError as e:
            print(f"✗ Rollback failed: {e.stderr}")
            return False

    def _keep_last_commits(self) -> None:
        """Keep only the last N commits to prevent infinite rollbacks."""
        try:
            # Get all commits (excluding current branch's history)
            all_commits = subprocess.check_output(
                ["git", "rev-list", "--all", "--max-count=strategy=oldest"],
                text=True,
                check=True,
            ).strip().split("\n")

            if len(all_commits) <= self.keep_commits:
                return

            # Delete all but the last N commits
            for commit in all_commits[:len(all_commits) - self.keep_commits]:
                subprocess.run(
                    ["git", "update-ref", "-d", f"refs/heads/{commit}"],
                    check=False,
                )

            print(f"✓ Kept last {self.keep_commits} commits")

        except subprocess.CalledProcessError as e:
            print(f"⚠ Warning: Could not limit commits: {e.stderr}")

    def trigger_rollback(self, results: list[tuple[bool, str]], summary: str) -> None:
        """Trigger rollback on critical failure.

        Args:
            results: List of (passed, message) tuples
            summary: Human-readable summary of failures
        """
        if not self.enabled:
            print("⚠ Rollback is disabled (HEALTH_ROLLBACK_ENABLED=false)")
            return

        failures = [r for r in results if not r[0]]

        if not failures:
            return

        if self.rollback_on_all:
            print("⚠ Rollback enabled for all failures")
            should_rollback = True
        elif self.rollback_on_critical and self.is_critical_failure(results):
            print("⚠ Critical failure detected, enabling rollback")
            should_rollback = True
        else:
            print("⚠ Non-critical failure, rollback not triggered")
            should_rollback = False

        if should_rollback:
            print("\n" + "=" * 60)
            print("TRIGGERING AUTOMATIC ROLLBACK")
            print("=" * 60)
            print(f"Reason: {summary}")
            print(f"Failures: {len(failures)}")
            print("=" * 60 + "\n")

            # Create tag
            tag = self.create_rollback_tag(summary)
            if not tag:
                print("✗ Rollback aborted: Could not create tag")
                return

            # Perform rollback
            if self.rollback_to_previous():
                print("\n✓ Rollback completed successfully")
                print("Next steps:")
                print("  1. Review the failed changes")
                print("  2. Fix the issues")
                print("  3. Re-commit and push")
                print("  4. Verify health checks pass")
            else:
                print("\n✗ Rollback failed")
                print("Manual intervention required")

    def get_rollback_point(self) -> Optional[str]:
        """Get the current rollback point tag.

        Returns:
            Tag name if found, None otherwise
        """
        try:
            result = subprocess.check_output(
                ["git", "tag", "-l", f"{self.rollback_tag}-*"],
                text=True,
                check=True,
            ).strip()

            if not result:
                return None

            return result.split("\n")[-1]  # Most recent tag

        except subprocess.CalledProcessError:
            return None


if __name__ == "__main__":
    # Example usage
    rollback = HealthRollback()

    print(f"Rollback enabled: {rollback.enabled}")
    print(f"Rollback on critical: {rollback.rollback_on_critical}")
    print(f"Rollback on all: {rollback.rollback_on_all}")
    print(f"Rollback branch: {rollback.rollback_branch}")
    print(f"Keep commits: {rollback.keep_commits}")

    # Example results
    example_results = [
        (True, "index.html exists"),
        (False, "some non-critical check failed"),
        (True, "another pass"),
    ]

    rollback.trigger_rollback(example_results, "Example failure")
