"""Automated health check runner for the repository.

This script runs after every build and logs the results to health_status.json.
It can also be run manually for testing.

Run from anywhere:   python site/auto_health_check.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEALTH_STATUS = ROOT / "site" / "health_status.json"


def load_health_status() -> dict:
    """Load health status from JSON file."""
    if HEALTH_STATUS.exists():
        import json
        return json.loads(HEALTH_STATUS.read_text(encoding="utf-8"))
    # Return fresh status if file doesn't exist
    return {
        "last_checked": None,
        "checks": {},
        "summary": {"total": 12, "passed": 0, "failed": 0, "warnings": 0, "overall_status": "pending"},
        "alert_level": "none",
        "last_build_hash": None,
        "last_commit_time": None
    }


def save_health_status(data: dict) -> None:
    """Save health status to JSON file."""
    import json
    data["last_checked"] = datetime.now().isoformat()
    HEALTH_STATUS.write_text(json.dumps(data, indent=2), encoding="utf-8")


def run_check_site() -> tuple[bool, str]:
    """Run check_site.py and return (success, output)."""
    try:
        result = subprocess.run(
            [sys.executable, "site/check_site.py", "--live"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output
    except subprocess.TimeoutExpired:
        return False, "check_site.py timed out after 60 seconds"
    except Exception as e:
        return False, f"check_site.py failed with error: {e}"


def update_check_result(data: dict, check_name: str, status: str, message: str = "") -> None:
    """Update a single check result in health status."""
    if "checks" not in data:
        data["checks"] = {}

    data["checks"][check_name] = {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "message": message
    }

    # Update summary counts
    summary = data.get("summary", {"total": 12, "passed": 0, "failed": 0, "warnings": 0})
    summary["total"] = 12
    summary["passed"] += 1 if status == "passed" else 0
    summary["failed"] += 1 if status == "failed" else 0
    summary["warnings"] += 1 if status == "warning" else 0

    # Update alert level
    if status == "failed":
        data["alert_level"] = "critical"
    elif status == "warning" and data["alert_level"] != "critical":
        data["alert_level"] = "warning"

    # Update build info
    data["last_build_hash"] = run_command("git rev-parse --short HEAD 2>/dev/null || echo unknown")
    data["last_commit_time"] = run_command("git show -s --format=%ci HEAD 2>/dev/null || echo unknown")


def run_command(cmd: str) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=ROOT
        )
        return result.stdout.strip() or result.stderr.strip() or ""
    except Exception:
        return ""


def main() -> int:
    """Run automated health check and update status."""
    print("=" * 60)
    print("Automated Health Check")
    print("=" * 60)
    print()

    # Load existing status
    data = load_health_status()
    print(f"Loaded health status from {HEALTH_STATUS}")

    # Run check_site.py
    print("\nRunning check_site.py --live...")
    success, output = run_check_site()

    if success:
        print("✓ check_site.py passed")
        update_check_result(data, "all_checks", "passed", output)
    else:
        print("✗ check_site.py failed")
        update_check_result(data, "all_checks", "failed", output)

    # Extract individual check results from output
    checks_passed = []
    checks_failed = []

    if "PASS" in output:
        checks_passed = [line.split(":")[0].strip() for line in output.split("\n") if "PASS" in line]

    if "FAIL" in output:
        checks_failed = [line.split(":")[0].strip() for line in output.split("\n") if "FAIL" in line]

    # Update individual checks
    if checks_passed:
        for check in checks_passed:
            update_check_result(data, check, "passed")

    if checks_failed:
        for check in checks_failed:
            update_check_result(data, check, "failed")

    # Save updated status
    save_health_status(data)
    print(f"\nUpdated health status in {HEALTH_STATUS}")

    # Print summary
    summary = data.get("summary", {})
    print(f"\nSummary: {summary.get('passed', 0)}/{summary.get('total', 0)} checks passed")
    print(f"Alert level: {data.get('alert_level', 'none').upper()}")

    if checks_failed:
        print("\nFailed checks:")
        for check in checks_failed:
            print(f"  - {check}")

    print()
    print("=" * 60)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
