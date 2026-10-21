"""Automatic rollback on critical health check failures.

This module handles automatic rollback when health checks fail with critical severity.
It creates git rollback points and can revert to previous states if needed.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROLLBACK_DIR = ROOT / "site" / "rollback_points"
HEALTH_STATUS = ROOT / "site" / "health_status.json"


def create_rollback_point(name: str, reason: str, auto_created: bool = False) -> dict:
    """
    Create a git tag as a rollback point.

    Args:
        name: Name for the rollback point
        reason: Reason for creating the rollback point
        auto_created: Whether this was automatically created

    Returns:
        Dict with rollback point information
    """
    timestamp = datetime.now().isoformat()
    commit_hash = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True
    ).stdout.strip()

    # Create directory for rollback points
    ROLLBACK_DIR.mkdir(exist_ok=True)

    # Create rollback point file
    rollback_file = ROLLBACK_DIR / f"{name}.json"
    rollback_data = {
        "name": name,
        "timestamp": timestamp,
        "commit_hash": commit_hash,
        "reason": reason,
        "auto_created": auto_created,
        "check_name": None,
        "check_status": None,
        "rollbacks_used": 0
    }

    rollback_file.write_text(json.dumps(rollback_data, indent=2), encoding="utf-8")

    # Create git tag for this point
    try:
        subprocess.run(
            ["git", "tag", "-f", name],
            cwd=ROOT,
            capture_output=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        print(f"Warning: Failed to create git tag {name} (timeout)")
    except Exception as e:
        print(f"Warning: Failed to create git tag {name}: {e}")

    return rollback_data


def rollback_to_point(rollback_name: str) -> bool:
    """
    Revert to a previous rollback point.

    Args:
        rollback_name: Name of the rollback point

    Returns:
        True if rollback was successful
    """
    rollback_file = ROLLBACK_DIR / f"{rollback_name}.json"

    if not rollback_file.exists():
        print(f"Error: Rollback point '{rollback_name}' not found")
        return False

    rollback_data = json.loads(rollback_file.read_text(encoding="utf-8"))
    commit_hash = rollback_data["commit_hash"]

    print(f"Rolling back to commit {commit_hash} ({rollback_name})...")

    try:
        # Reset to the commit
        subprocess.run(
            ["git", "reset", "--hard", commit_hash],
            cwd=ROOT,
            capture_output=True,
            timeout=30
        )

        # Update rollback count
        rollback_data["rollbacks_used"] = rollback_data.get("rollbacks_used", 0) + 1
        rollback_file.write_text(json.dumps(rollback_data, indent=2), encoding="utf-8")

        # Reset the tag to point to the rollback point
        subprocess.run(
            ["git", "tag", "-f", rollback_name],
            cwd=ROOT,
            capture_output=True,
            timeout=10
        )

        print(f"✓ Successfully rolled back to {rollback_name}")
        return True

    except subprocess.TimeoutExpired:
        print(f"✗ Rollback timed out")
        return False
    except Exception as e:
        print(f"✗ Rollback failed: {e}")
        return False


def get_rollback_points() -> list[dict]:
    """List all available rollback points."""
    if not ROLLBACK_DIR.exists():
        return []

    rollback_points = []
    for file in ROLLBACK_DIR.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            rollback_points.append(data)
        except json.JSONDecodeError:
            continue

    # Sort by timestamp (newest first)
    rollback_points.sort(key=lambda x: x["timestamp"], reverse=True)
    return rollback_points


def check_critical_failures() -> list[tuple[str, str]]:
    """
    Check health_status.json for critical failures.

    Returns:
        List of (check_name, message) tuples for critical failures
    """
    if not HEALTH_STATUS.exists():
        return []

    try:
        data = json.loads(HEALTH_STATUS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    critical_checks = []

    # Check for failed critical checks
    if "checks" in data:
        for check_name, check_data in data["checks"].items():
            if check_data.get("status") == "failed":
                # Critical severity
                critical_checks.append((check_name, check_data.get("message", "")))

    return critical_checks


def auto_rollback_on_failure() -> dict:
    """
    Automatically rollback on critical failures.

    Returns:
        Dict with rollback results
    """
    print("=" * 60)
    print("Health Check Failure Handling")
    print("=" * 60)

    critical_failures = check_critical_failures()

    if not critical_failures:
        print("✓ No critical failures found")
        return {
            "action_taken": "none",
            "message": "No critical failures detected",
            "rollback_point": None
        }

    print(f"\n✗ Found {len(critical_failures)} critical failure(s):")

    # Get last rollback point
    rollback_points = get_rollback_points()
    last_rollback = rollback_points[0] if rollback_points else None

    if last_rollback:
        print(f"\nUsing last rollback point: {last_rollback['name']}")
        print(f"  Commit: {last_rollback['commit_hash']}")
        print(f"  Timestamp: {last_rollback['timestamp']}")
        print(f"  Reason: {last_rollback['reason']}")

        print(f"\nRolling back to {last_rollback['name']}...")
        success = rollback_to_point(last_rollback["name"])

        if success:
            print(f"\n✓ Automatic rollback completed")
            return {
                "action_taken": "auto_rollback",
                "message": f"Rolled back to {last_rollback['name']}",
                "rollback_point": last_rollback["name"],
                "commit_hash": last_rollback["commit_hash"],
                "failure_count": len(critical_failures)
            }
        else:
            print(f"\n✗ Automatic rollback failed")
            return {
                "action_taken": "rollback_failed",
                "message": "Failed to rollback automatically",
                "rollback_point": None,
                "failure_count": len(critical_failures)
            }
    else:
        print("\n⚠ No rollback points available")
        print("  Manual intervention required")
        return {
            "action_taken": "manual_required",
            "message": "No rollback points available, manual intervention required",
            "rollback_point": None,
            "failure_count": len(critical_failures)
        }


def main() -> int:
    """Main entry point for health rollback."""
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Just check for failures
        critical_failures = check_critical_failures()
        if critical_failures:
            print("CRITICAL_FAILURES")
            for name, msg in critical_failures:
                print(f"{name}: {msg}")
            return 1
        else:
            print("NO_FAILURES")
            return 0
    else:
        # Perform auto rollback
        result = auto_rollback_on_failure()
        return 1 if result["action_taken"] in ["auto_rollback", "rollback_failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
