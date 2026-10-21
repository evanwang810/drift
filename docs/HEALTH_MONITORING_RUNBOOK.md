# Health Monitoring Runbook

## Overview

This runbook documents the health monitoring procedures for the repository. The system runs automated health checks after every build and provides visibility into the repository's health status through a dashboard.

## Purpose

- **Detect issues early**: Identify problems before they become critical
- **Provide visibility**: Show current health status at a glance
- **Enable monitoring**: Track health over time and detect trends
- **Support maintenance**: Guide troubleshooting when issues occur

## Health Checks

### Current Checks (12 total)

1. **index.html exists** - Verifies the home page is built
2. **posts reachable** - Verifies all blog posts are linked from home page
3. **posts render** - Verifies all posts render as HTML without markdown syntax
4. **runs.json valid** - Verifies runs.json is a valid JSON array
5. **runs.json complete** - Verifies runs.json has every run from RUNS.md
6. **runs.json tokens** - Verifies runs.json has token counts (80%+ should be non-zero)
7. **runs.html loads** - Verifies the timeline page loads runs.json with a script
8. **runs.html draws** - Verifies the timeline page draws with SVG or canvas
9. **no dead links** - Verifies no dead links exist on any page
10. **no duplicate posts** - Verifies no duplicate post titles exist
11. **no orphaned posts** - Verifies no orphaned posts exist (unlinked)
12. **all posts named correctly** - Verifies all posts use YYYY-MM-DD format

### Alert Levels

- **None**: All checks passing
- **Warning**: Some checks failing, but no critical issues
- **Critical**: One or more critical checks failing

## Running Health Checks

### Manual Health Check

To run the health checks manually:

```bash
python site/check_site.py --live
```

To run automated health check:

```bash
python site/auto_health_check.py
```

### Automated After Every Build

The health check should run automatically after every build. Update the build script to include:

```python
import subprocess
import sys

# After building the site
result = subprocess.run(
    [sys.executable, "site/auto_health_check.py"],
    cwd=ROOT,
    capture_output=True,
    text=True
)
if result.returncode != 0:
    print("Health check failed:", result.stderr)
    sys.exit(1)
```

## Health Dashboard

The health dashboard provides a visual overview of the repository's health status.

**URL**: `https://evanwang810.github.io/drift/health_dashboard.html`

### Dashboard Features

- **Overall Status**: Shows current health status (all green = good)
- **Summary Cards**: Displays passed, failed, and warning counts
- **Individual Checks**: Lists all 12 checks with their current status
- **Check History**: Shows last check time, build hash, and commit time
- **Actions**: Buttons to run health check, view log, and view runbook

## Monitoring Procedures

### Daily Monitoring

1. Check the health dashboard at least once daily
2. Look for any red indicators or failed checks
3. Address any critical alerts immediately

### Weekly Monitoring

1. Review health check history for trends
2. Check for recurring issues
3. Update runbook based on lessons learned

### Build Monitoring

1. Health checks should run automatically after every build
2. Verify health checks pass before deploying
3. If health checks fail, investigate and fix before deploying

## Troubleshooting

### Health Checks Failing

**Step 1**: Run manual health check
```bash
python site/check_site.py --live
```

**Step 2**: Check individual check failures
- Look at the output for specific failed checks
- Fix the underlying issue (broken links, missing files, etc.)

**Step 3**: Rebuild the site
```bash
python site/build.py
```

**Step 4**: Re-run health checks
```bash
python site/check_site.py --live
```

**Step 5**: Verify fix
- Ensure all checks pass
- Check health dashboard shows all green

### Dashboard Not Loading

**Potential Causes**:
- health_status.json file missing or corrupted
- JavaScript disabled in browser
- File permissions issue

**Solutions**:
1. Ensure health_status.json exists and is readable
2. Verify JavaScript is enabled
3. Check browser console for errors

### Automated Health Check Not Running

**Potential Causes**:
- Build script doesn't call auto_health_check.py
- auto_health_check.py has errors
- File permissions issue

**Solutions**:
1. Check build script includes health check call
2. Verify auto_health_check.py syntax with `python -m py_compile`
3. Check permissions on health_status.json

## Maintenance

### Regular Updates

- Review health checks quarterly to ensure they remain relevant
- Add new checks as needed for new features
- Update runbook with new procedures

### Backup

- health_status.json is backed up with the repository
- No special backup needed for health monitoring data

### Performance

- Health checks should complete within 60 seconds
- If checks are slow, consider optimizing or caching results
- Automated checks run during build process, so they don't affect user experience

## Best Practices

1. **Run checks before deploying**: Always verify health checks pass before deploying
2. **Address issues promptly**: Don't let failed checks accumulate
3. **Review logs regularly**: Check health check output for patterns
4. **Update runbook**: Document any new procedures or lessons learned
5. **Keep checks simple**: Each check should have a single, clear purpose

## Alerting (Future Enhancement)

To add alerting, consider:

1. **Email alerts**: Send email when critical checks fail
2. **Slack alerts**: Send Slack messages to team channel
3. **GitHub Actions**: Create workflow that fails if health checks fail
4. **Monitoring service**: Use a service like Datadog or Prometheus

## Success Criteria

The health monitoring system is successful when:

- ✅ All 12 health checks pass consistently
- ✅ Health dashboard loads and displays correctly
- ✅ Health checks run automatically after every build
- ✅ Issues are detected and resolved before they affect users
- ✅ Monitoring procedures are followed consistently
- ✅ Runbook is up to date and followed
- ✅ No critical alerts occur for 30 consecutive days

## Contact

For questions or issues with health monitoring, contact the repository owner or maintainers.
