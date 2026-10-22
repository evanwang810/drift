"""Generate health dashboard HTML from health check results.

This script reads health check results and generates an HTML dashboard
that can be embedded in the site or viewed standalone.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_health_check(live: bool = False) -> tuple[list[tuple[bool, str]], int]:
    """Run health checks and return results.

    Args:
        live: If True, check live site; otherwise check local docs/

    Returns:
        Tuple of (results list, exit code)
    """
    cmd = ["python", "site/check_site.py"]
    if live:
        cmd.append("--live")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    results: list[tuple[bool, str]] = []
    for line in result.stdout.split("\n"):
        if line.startswith("PASS"):
            results.append((True, line[5:].strip()))
        elif line.startswith("FAIL"):
            results.append((False, line[5:].strip()))

    return results, result.returncode


def generate_dashboard(results: list[tuple[bool, str]], exit_code: int) -> str:
    """Generate HTML dashboard from health check results.

    Args:
        results: List of (passed, message) tuples
        exit_code: Exit code from health check

    Returns:
        HTML dashboard string
    """
    total = len(results)
    passed = sum(1 for p, _ in results if p)
    failed = total - passed
    rate = f"{(passed / total * 100):.1f}%" if total > 0 else "0%"

    # Get last run timestamp
    try:
        last_run = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    except:
        last_run = "Unknown"

    checks_html = []
    for passed, message in results:
        icon = "✅" if passed else "❌"
        status_class = "passed" if passed else "failed"
        checks_html.append(
            f'<div class="check-item {status_class}">'
            f'<span class="check-icon">{icon}</span>'
            f'<span class="check-message">{message}</span>'
            f'</div>'
        )

    dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repository Health Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f5f5;
        }}
        .dashboard {{
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-top: 0;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }}
        .stat-card {{
            padding: 1.5rem;
            border-radius: 6px;
            text-align: center;
        }}
        .stat-card.total {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        .stat-card.passed {{
            background: #e8f5e9;
            color: #2e7d32;
        }}
        .stat-card.failed {{
            background: #ffebee;
            color: #c62828;
        }}
        .stat-card.rate {{
            background: #fff3e0;
            color: #ef6c00;
        }}
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }}
        .stat-label {{
            font-size: 0.875rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .check-list {{
            margin: 2rem 0;
        }}
        .check-item {{
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
        }}
        .check-item.passed {{
            background: #e8f5e9;
            color: #2e7d32;
        }}
        .check-item.failed {{
            background: #ffebee;
            color: #c62828;
        }}
        .check-icon {{
            margin-right: 1rem;
            font-size: 1.25rem;
        }}
        .check-message {{
            flex: 1;
        }}
        .last-run {{
            margin-top: 2rem;
            padding: 1rem;
            background: #f5f5f5;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.875rem;
        }}
        .timestamp {{
            color: #666;
            margin-top: 0.5rem;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>📊 Repository Health Dashboard</h1>

        <div class="summary">
            <div class="stat-card total">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Total Checks</div>
            </div>
            <div class="stat-card passed">
                <div class="stat-number">{passed}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card failed">
                <div class="stat-number">{failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card rate">
                <div class="stat-number">{rate}</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>

        <div class="check-list">
            {''.join(checks_html)}
        </div>

        <div class="last-run">
            <strong>Last Run:</strong> {last_run}
            <div class="timestamp">Exit code: {exit_code}</div>
        </div>
    </div>
</body>
</html>"""

    return dashboard_html


def main() -> None:
    """Generate health dashboard HTML.

    Reads health check results and creates an HTML dashboard.
    """
    ROOT = Path(__file__).resolve().parent.parent
    DOCS = ROOT / "docs"

    print("Running health checks...")
    results, exit_code = run_health_check(live=False)

    print(f"\nHealth Check Results:")
    for passed, message in results:
        print(f"  {'✅' if passed else '❌'} {message}")

    print(f"\nTotal: {len(results)} checks, {sum(1 for p, _ in results if p)} passed, "
          f"{sum(1 for p, _ in results if not p)} failed")

    dashboard_html = generate_dashboard(results, exit_code)

    output_path = DOCS / "health_dashboard.html"
    output_path.write_text(dashboard_html, encoding="utf-8")

    print(f"\n✓ Health dashboard generated: {output_path}")


if __name__ == "__main__":
    main()
