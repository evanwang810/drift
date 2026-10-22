"""Alerting mechanism for health check failures.

This module provides configurable alerts via email and Slack when health checks fail.
"""

import os
import smtplib
import subprocess
from email.mime.text import MIMEText
from typing import Optional


class HealthAlerts:
    """Handle health check alerting."""

    def __init__(self):
        """Initialize alert configuration."""
        self.email_enabled = os.getenv("HEALTH_ALERT_EMAIL", "").strip() != ""
        self.slack_enabled = os.getenv("HEALTH_ALERT_SLACK_WEBHOOK", "").strip() != ""
        self.email_address = os.getenv("HEALTH_ALERT_EMAIL", "")
        self.slack_webhook = os.getenv("HEALTH_ALERT_SLACK_WEBHOOK", "")
        self.alert_on_failure_only = os.getenv("HEALTH_ALERT_FAILURE_ONLY", "true").lower() == "true"

    def send_email_alert(self, subject: str, body: str) -> bool:
        """Send email alert about health check failure.

        Args:
            subject: Email subject line
            body: Email body text

        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.email_enabled or not self.email_address:
            return False

        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = os.getenv("HEALTH_ALERT_FROM", "health-check@drift")
            msg["To"] = self.email_address

            with smtplib.SMTP(os.getenv("HEALTH_ALERT_SMTP_HOST", "smtp.gmail.com"), int(os.getenv("HEALTH_ALERT_SMTP_PORT", 587))) as server:
                if os.getenv("HEALTH_ALERT_SMTP_USER"):
                    server.starttls()
                    server.login(os.getenv("HEALTH_ALERT_SMTP_USER"), os.getenv("HEALTH_ALERT_SMTP_PASSWORD"))
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email alert: {e}")
            return False

    def send_slack_alert(self, text: str, attachments: Optional[list] = None) -> bool:
        """Send Slack alert about health check failure.

        Args:
            text: Slack message text
            attachments: Optional list of attachment dictionaries

        Returns:
            True if Slack message was sent successfully, False otherwise
        """
        if not self.slack_enabled or not self.slack_webhook:
            return False

        try:
            import requests

            payload = {"text": text}
            if attachments:
                payload["attachments"] = attachments

            response = requests.post(
                self.slack_webhook,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
            return False

    def send_failure_alert(self, results: list[tuple[bool, str]], summary: str) -> None:
        """Send alert for health check failures.

        Args:
            results: List of (passed, message) tuples from health checks
            summary: Human-readable summary of failures
        """
        failures = [r for r in results if not r[0]]
        if not failures:
            return

        subject = f"❌ Health Check Failed: {len(failures)} checks failed"

        email_body = f"""Health check failures detected:

{summary}

Details:
{chr(10).join(f"- {msg}" for passed, msg in failures)}

Check the full logs for more information.
"""
        slack_text = f"❌ *Health Check Failed*\n{summary}\n\n{len(failures)} checks failed."

        attachments = [
            {
                "color": "#FF0000",
                "title": f"{len(failures)} of {len(results)} checks failed",
                "text": summary,
                "footer": "Drift Repository Health Check",
                "ts": int(subprocess.check_output(["date", "+%s"], text=True).strip()),
            }
        ]

        self.send_email_alert(subject, email_body)
        self.send_slack_alert(slack_text, attachments if len(failures) <= 3 else None)

    def send_success_alert(self) -> None:
        """Send alert that all health checks passed."""
        subject = "✅ All Health Checks Passed"
        body = "All health checks passed successfully. No action required."

        slack_text = "✅ *All Health Checks Passed*\nAll checks completed successfully."

        self.send_email_alert(subject, body)
        self.send_slack_alert(slack_text)


if __name__ == "__main__":
    # Example usage
    alerts = HealthAlerts()
    print(f"Email alerts: {alerts.email_enabled}")
    print(f"Slack alerts: {alerts.slack_enabled}")
