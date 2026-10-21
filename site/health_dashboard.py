"""Health status dashboard.

Generates a health status page that shows current state of all health checks.

Run it from anywhere:
    python site/health_dashboard.py
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TEMPLATE = DOCS / "templates" / "health_dashboard.html"


def get_check_results() -> dict:
    """Run health checks and return results."""
    cmd = ["python", "site/health_check.py"]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    
    checks = {}
    for line in result.stdout.split('\n'):
        if line.startswith('✓ ') or line.startswith('✗ '):
            parts = line.split('\n', 1)
            check_name = parts[0][2:].strip()
            if len(parts) > 1:
                message = parts[1].strip()
            else:
                message = ""
            checks[check_name] = {
                "status": "pass" if line.startswith('✓ ') else "fail",
                "message": message
            }
        elif line.startswith('Health Check Summary'):
            match = line.strip().split(':')
            if len(match) == 2:
                summary = match[1].strip()
                if '/' in summary:
                    checks['Overall'] = {
                        "status": "pass" if "all" in summary.lower() else "fail",
                        "message": summary
                    }
    
    return checks


def get_recent_alerts() -> list[dict]:
    """Get recent health alerts from health_config.json."""
    config_file = ROOT / "site" / "health_config.json"
    if not config_file.exists():
        return []
    
    try:
        config = json.loads(config_file.read_text(encoding="utf-8"))
        alerts = []
        
        if "last_alerts" in config:
            for name, timestamp in config["last_alerts"].items():
                alerts.append({
                    "name": name,
                    "time": datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "count": 1
                })
        
        return sorted(alerts, key=lambda x: x["time"], reverse=True)[:10]
    except json.JSONDecodeError:
        return []


def generate_dashboard() -> str:
    """Generate the health dashboard HTML."""
    checks = get_check_results()
    alerts = get_recent_alerts()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Calculate overall status
    overall_status = "pass"
    if checks.get('Overall', {}).get('status') == 'fail':
        overall_status = 'fail'
    elif checks.get('Overall', {}).get('status') == 'pass':
        overall_status = 'pass'
    else:
        # Default to pass if no overall check
        overall_status = 'pass' if all(c.get('status') == 'pass' for c in checks.values() if c.get('status')) else 'fail'
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repository Health Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f5f5;
        }}
        .dashboard {{
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #eee;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2rem;
            color: #333;
        }}
        .header .timestamp {{
            color: #666;
            font-size: 0.9rem;
        }}
        .overall-status {{
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-weight: bold;
            font-size: 1.1rem;
        }}
        .status-pass {{
            background: #d4edda;
            color: #155724;
        }}
        .status-fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }}
        .check-card {{
            padding: 1rem;
            border-radius: 4px;
            background: #f8f9fa;
            border-left: 4px solid #ccc;
        }}
        .check-card.pass {{
            border-left-color: #28a745;
        }}
        .check-card.fail {{
            border-left-color: #dc3545;
        }}
        .check-card h3 {{
            margin: 0 0 0.5rem 0;
            font-size: 1rem;
        }}
        .check-card .message {{
            font-size: 0.9rem;
            color: #666;
            margin: 0;
        }}
        .alerts-section {{
            margin-top: 2rem;
            padding: 1rem;
            background: #fff3cd;
            border-radius: 4px;
        }}
        .alerts-section h2 {{
            margin-top: 0;
            color: #856404;
        }}
        .alert-item {{
            padding: 0.5rem 0;
            border-bottom: 1px solid #ffeeba;
        }}
        .alert-item:last-child {{
            border-bottom: none;
        }}
        .alert-item .name {{
            font-weight: bold;
        }}
        .alert-item .time {{
            font-size: 0.85rem;
            color: #856404;
        }}
        .footer {{
            margin-top: 2rem;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>Repository Health Dashboard</h1>
            <div class="timestamp">Last updated: {timestamp}</div>
            <div style="margin-top: 1rem;">
                Overall Status: <span class="overall-status status-{overall_status}">{overall_status.upper()}</span>
            </div>
        </div>

        <div class="grid">
"""
    
    for name, check in checks.items():
        status_class = check.get('status', 'unknown')
        status_symbol = '✓' if status_class == 'pass' else '✗'
        html += f"""            <div class="check-card {status_class}">
                <h3>{status_symbol} {name}</h3>
                <p class="message">{check.get('message', '')}</p>
            </div>
"""
    
    html += """        </div>
"""
    
    if alerts:
        html += """        <div class="alerts-section">
            <h2>Recent Alerts</h2>
            <div class="alerts-list">
"""
        for alert in alerts:
            html += f"""                <div class="alert-item">
                    <div class="name">{alert['name']}</div>
                    <div class="time">{alert['time']}</div>
                </div>
"""
        html += """            </div>
        </div>
"""
    
    html += f"""        <div class="footer">
            <a href="https://github.com/evanwang810/drift">View on GitHub</a> |
            <a href="health_check.py">Run Health Checks</a> |
            <a href="health_alerts.py">Configure Alerts</a>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main() -> int:
    """Generate and write the health dashboard."""
    try:
        dashboard = generate_dashboard()
        dashboard_file = DOCS / "health-dashboard.html"
        dashboard_file.write_text(dashboard, encoding="utf-8")
        print(f"✓ Health dashboard written to {dashboard_file}")
        return 0
    except Exception as e:
        print(f"✗ Failed to generate health dashboard: {e}")
        return 1


if __name__ == "__main__":
    main()
