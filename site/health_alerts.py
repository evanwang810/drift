"""Health check alerting system.

Sends alerts when health checks fail or pass thresholds are crossed.

Configuration: Set ALERT_EMAIL environment variable to receive email alerts.
"""

from __future__ import annotations

import json
import os
import smtplib
import subprocess
import sys
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_alert_config() -> dict:
    """Load alert configuration from config.json if it exists."""
    config_file = ROOT / "site" / "health_config.json"
    if config_file.exists():
        try:
            return json.loads(config_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def save_alert_config(config: dict) -> None:
    """Save alert configuration to config.json."""
    config_file = ROOT / "site" / "health_config.json"
    config_file.write_text(json.dumps(config, indent=2), encoding="utf-8")


def check_alert_threshold(name: str, config: dict) -> bool:
    """Check if an alert should be sent for this check."""
    if not config.get("enabled", True):
        return False
    
    # Check if this check is in the enabled list
    if "checks" in config and name not in config["checks"]:
        return False
    
    # Check if alert frequency is satisfied
    last_alert = config.get("last_alerts", {}).get(name, 0)
    now = datetime.now().timestamp()
    min_interval = config.get("alert_interval_minutes", 60)
    
    return (now - last_alert) / 60 >= min_interval


def record_alert(name: str, config: dict) -> dict:
    """Record that an alert was sent for this check."""
    if "last_alerts" not in config:
        config["last_alerts"] = {}
    config["last_alerts"][name] = datetime.now().timestamp()
    save_alert_config(config)
    return config


def send_email_alert(subject: str, body: str) -> bool:
    """Send email alert using SMTP."""
    email = os.getenv("ALERT_EMAIL")
    if not email:
        print(f"⚠ ALERT_EMAIL not set, skipping email alert")
        print(f"  Subject: {subject}")
        print(f"  Body:\n{body}")
        return False
    
    smtp_server = os.getenv("ALERT_SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("ALERT_SMTP_PORT", 587))
    smtp_user = os.getenv("ALERT_SMTP_USER", email)
    smtp_password = os.getenv("ALERT_SMTP_PASSWORD")
    
    if not smtp_password:
        print(f"⚠ ALERT_SMTP_PASSWORD not set, skipping email alert")
        print(f"  Would send to: {email}")
        print(f"  Subject: {subject}")
        return False
    
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = email
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        print(f"✓ Email alert sent to {email}")
        return True
    except Exception as e:
        print(f"✗ Failed to send email alert: {e}")
        return False


def send_slack_alert(text: str, config: dict) -> bool:
    """Send Slack alert using webhook."""
    webhook_url = config.get("slack_webhook")
    if not webhook_url:
        return False
    
    try:
        import requests
        payload = {"text": text}
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✓ Slack alert sent")
        return True
    except Exception as e:
        print(f"✗ Failed to send Slack alert: {e}")
        return False


def send_health_check_alert(name: str, status: bool, message: str, config: dict) -> bool:
    """Send alert for a health check result."""
    if not check_alert_threshold(name, config):
        return False
    
    status_symbol = "✓" if status else "✗"
    subject = f"[Health Check] {status_symbol} {name}"
    body = f"""Health Check Result: {name}

Status: {'PASS' if status else 'FAIL'}
Message: {message}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

---
Repository: {ROOT}
Run: {os.getenv('DRIFT_RUN', 'unknown')}
"""
    
    # Record alert
    config = record_alert(name, config)
    
    # Try all notification methods
    sent = False
    if send_email_alert(subject, body):
        sent = True
    if send_slack_alert(f"{status_symbol} {name}", config):
        sent = True
    
    if not sent:
        print(f"⚠ Alert threshold met but no notification method configured")
    
    return sent


def get_health_check_results() -> dict:
    """Run all health checks and return results."""
    cmd = ["python", "site/health_check.py"]
    success, stdout, stderr = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    
    results = {}
    if success:
        for line in stdout.split('\n'):
            if line.startswith('✓ ') or line.startswith('✗ '):
                # Parse: ✓ Build Success\n  Site builds successfully
                parts = line.split('\n', 1)
                check_name = parts[0][2:].strip()
                if len(parts) > 1:
                    message = parts[1].strip()
                else:
                    message = ""
                results[check_name] = (True, message)
            elif line.startswith('Health Check Summary'):
                # Extract pass count
                match = re.search(r'(\d+)/(\d+)', line)
                if match:
                    passed = int(match.group(1))
                    total = int(match.group(2))
                    results['Overall'] = (passed == total, f"{passed}/{total} checks passed")
    
    return results


def main() -> int:
    """Main alert checking function."""
    config = load_alert_config()
    
    if len(sys.argv) < 2:
        print("Usage: python site/health_alerts.py <check_name> [--fail] [--pass]")
        print("Check names: Build Success, Site Validations, Git Status, JSON Files, No Colons in Posts, Post Naming, No Duplicate Posts")
        return 1
    
    check_name = sys.argv[1].strip()
    status = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] in ['--fail', '--pass'] else '--pass'
    is_fail = status == '--fail'
    
    # Find actual check name (handle common variations)
    mapping = {
        "Build": "Build Success",
        "Build Success": "Build Success",
        "Site": "Site Validations",
        "Site Validations": "Site Validations",
        "Git": "Git Status",
        "Git Status": "Git Status",
        "JSON": "JSON Files",
        "JSON Files": "JSON Files",
        "No Colons": "No Colons in Posts",
        "No Colons in Posts": "No Colons in Posts",
        "Post Naming": "Post Naming",
        "No Duplicate Posts": "No Duplicate Posts",
    }
    
    actual_name = mapping.get(check_name, check_name)
    
    if actual_name not in mapping.values():
        print(f"Unknown check name: {check_name}")
        return 1
    
    if is_fail:
        message = "Health check failed unexpectedly"
    else:
        message = "Health check passed"
    
    send_health_check_alert(actual_name, not is_fail, message, config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
