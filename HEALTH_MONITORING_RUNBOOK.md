# Repository Health Monitoring Runbook

## Overview

This document provides procedures for monitoring and maintaining repository health. The health monitoring system runs automatically after each build and can be triggered manually for ad-hoc checks.

## Health Check System

### Automated Health Checks

The primary health check system is implemented in `site/check_site.py`. It performs 12 validation checks:

1. **index.html exists** - Verifies the main page is present
2. **All posts linked** - Ensures every post is reachable from the home page
3. **Posts render correctly** - Checks that posts are rendered as HTML, not markdown
4. **runs.json completeness** - Verifies runs.json has every run from RUNS.md
5. **Token counts** - Ensures token counts are present and non-zero
6. **runs.html loads data** - Confirms timeline page loads runs.json
7. **runs.html uses canvas** - Verifies timeline draws with SVG or canvas
8. **No dead links** - Checks for broken links on all linked pages
9. **Viewport meta tag** - Ensures mobile responsiveness
10. **Post naming convention** - Validates YYYY-MM-DD-words-with-dashes format
11. **No duplicate titles** - Ensures all posts have unique titles
12. **No auto-generated posts** - Prevents posts from run log rows

### Running Health Checks

#### Local Checks
```bash
python site/check_site.py
```
Checks the files in `docs/` only.

#### Live Site Checks
```bash
python site/check_site.py --live
```
Checks the published site at https://evanwang810.github.io/drift/

### Expected Output

All checks should pass with output like:
```
PASS  index.html exists
PASS  all 13 posts are linked from the home page or a page it links to
...
12 of 12 pass
```

If any checks fail, the script will exit with a non-zero status code.

## Alerting

### Email Alerts

Configure email alerts by setting environment variables:

```bash
export HEALTH_ALERT_EMAIL="your-email@example.com"
export HEALTH_ALERT_FROM="health-check@drift"
export HEALTH_ALERT_SMTP_HOST="smtp.gmail.com"
export HEALTH_ALERT_SMTP_PORT="587"
export HEALTH_ALERT_SMTP_USER="your-email@gmail.com"
export HEALTH_ALERT_SMTP_PASSWORD="your-app-password"
```

### Slack Alerts

Configure Slack alerts by setting:

```bash
export HEALTH_ALERT_SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export HEALTH_ALERT_FAILURE_ONLY="true"
```

When a check fails, the system will:
1. Send an email with details about failures
2. Send a Slack message with a summary and failure count
3. Include detailed information about which checks failed

### Alert Configuration

To reduce noise, set `HEALTH_ALERT_FAILURE_ONLY="true"` to only alert on failures, not on all-green runs.

## Dashboard

The health dashboard provides a visual overview of repository health:

- **Summary Statistics**: Total checks, passed, failed, success rate
- **Check List**: Individual check results with pass/fail status
- **Last Run Information**: Timestamp of the most recent check

Access the dashboard at `health_dashboard.html`.

## Manual Health Checks

### Quick Validation

Before committing changes, run local health checks:
```bash
python site/check_site.py
```

### Comprehensive Validation

Run live site checks to verify deployment:
```bash
python site/check_site.py --live
```

### Site Build Verification

After any build, verify the site builds without errors:
```bash
cd site
python build.py
cd ..
python site/check_site.py
```

## Maintenance Procedures

### Daily Checks

Automated checks run via GitHub Actions (cron: "37 * * * *"). Monitor the workflow run results.

### Weekly Review

Review health check results weekly:
1. Check dashboard for trends
2. Review any alerts that were sent
3. Investigate recurring failures

### Monthly Deep Dive

Perform comprehensive health audit:
1. Review all 12 check results
2. Check for new health risks
3. Update runbook if needed

## Troubleshooting

### Common Issues

#### 1. All Checks Pass Locally, Fail on Live

**Cause**: Local and live site have different content
**Solution**: Deploy local changes before running live checks

#### 2. Token Counts Missing

**Cause**: runs.json not properly generated
**Solution**: Regenerate runs.json and verify it matches RUNS.md

#### 3. Dead Links Detected

**Cause**: Navigation links or post links broken
**Solution**: Check Jekyll templates and post generation

#### 4. Posts Not Rendering

**Cause**: Markdown syntax or file naming issues
**Solution**: Review post content and verify naming convention

### Recovery Procedures

#### When a Critical Check Fails

1. **Document the failure** - Note which check failed and when
2. **Run local checks** - Verify the issue exists locally
3. **Fix the issue** - Address the root cause in source files
4. **Re-run checks** - Verify all checks pass after fix
5. **Deploy** - Push changes and verify live site passes

#### When Multiple Checks Fail

1. **Assess severity** - Identify which checks are critical
2. **Address dependencies** - Fix underlying issues first
3. **Prioritize fixes** - Start with highest impact issues
4. **Test incrementally** - Verify each fix individually

## Monitoring Best Practices

### Proactive Monitoring

- **Automated alerts** - Configure alerts to notify before issues become critical
- **Regular checks** - Ensure automated checks run after every build
- **Dashboard visibility** - Make health status visible to the team

### Alert Thresholds

- **Critical failures** - Immediate alert via email and Slack
- **Recurring failures** - Alert if a check fails 3 times in a row
- **Warning trends** - Flag if success rate drops below 90%

### Response Times

- **Critical alerts** - Acknowledge within 15 minutes
- **Investigation** - Complete within 2 hours
- **Resolution** - Document and implement fix within 24 hours

## Continuous Improvement

### Feedback Loop

1. **Track issues** - Log all health check failures
2. **Analyze patterns** - Identify recurring issues
3. **Implement fixes** - Address root causes
4. **Update runbook** - Document lessons learned

### Health Metrics to Track

- Check success rate (target: 95%+)
- Average time between failures
- Time to resolve failures
- Frequency of manual interventions

## Contact Information

For questions or issues with health monitoring:
- Check the dashboard at `health_dashboard.html`
- Review this runbook for troubleshooting steps
- Contact repository maintainers
