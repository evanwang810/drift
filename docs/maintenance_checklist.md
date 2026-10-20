# Repository Maintenance Checklist

This checklist provides a routine for maintaining the Drift repository in a consistent, production-ready state.

## Daily/Weekly Maintenance

### Site Health Checks
- [ ] Run `python site/check_site.py --live` and verify all 12 validations pass
- [ ] Run `python site/build.py` and verify no errors
- [ ] Check that all 13 blog posts render correctly
- [ ] Verify runs.json has matching entries with RUNS.md
- [ ] Check for any broken links in the site

### Documentation Updates
- [ ] Review and update PROJECT.md if new projects are completed
- [ ] Update README.md if repository structure or tools change
- [ ] Review notes in NOTE.md and archive if complete

## Monthly Maintenance

### Repository Cleanup
- [ ] Review and remove orphaned files from docs/
- [ ] Check for duplicate content in documentation
- [ ] Verify no stale branches or tags exist
- [ ] Clean up temporary files and cache

### Knowledge Base Review
- [ ] Review knowledge_base.json for duplicate or low-quality entries
- [ ] Verify knowledge base search functionality works
- [ ] Check that insights are being extracted and saved correctly

### Performance Optimization
- [ ] Check page load times
- [ ] Review and optimize large HTML files
- [ ] Verify caching headers are set correctly
- [ ] Check for any unused JavaScript or CSS

## Quarterly Maintenance

### Code Quality
- [ ] Run code quality checks (linting, static analysis)
- [ ] Review agent/tools.py for unused functions or code duplication
- [ ] Update dependencies if security vulnerabilities are found
- [ ] Refactor code as needed for maintainability

### Backup Verification
- [ ] Verify git repository is in good health
- [ ] Check that all important files are tracked in git
- [ ] Review and update .gitignore if needed
- [ ] Verify backup procedures if applicable

## Documentation Review

### Onboarding Documentation
- [ ] Review and update developer onboarding guide
- [ ] Verify contribution guidelines are current
- [ ] Check troubleshooting guide for common issues
- [ ] Update setup instructions if environment changes

### Tool Documentation
- [ ] Verify TOOLS.md is synchronized with agent/tools.py
- [ ] Document any new tools or changes to existing tools
- [ ] Ensure all tool descriptions are accurate and helpful

## Issue Tracking

### GitHub Issues
- [ ] Review open GitHub issues
- [ ] Close resolved issues and document resolutions
- [ ] Create new issues for any technical debt discovered
- [ ] Update issue labels as needed

### Technical Debt
- [ ] Review technical debt items in PROJECT.md
- [ ] Create GitHub issues for high-priority items
- [ ] Plan and track debt reduction in future runs

## Alerts and Monitoring

### Critical Alerts
- [ ] Set up alerts for site build failures
- [ ] Configure alerts for broken links
- [ ] Monitor runs.json integrity
- [ ] Check for repository health issues

### Metrics Monitoring
- [ ] Review site metrics (page views, bounce rates if applicable)
- [ ] Check run statistics and productivity trends
- [ ] Monitor token usage and efficiency

## Emergency Procedures

### Site Down
1. Check if the site builds successfully locally
2. Review recent changes in git history
3. Check for database/file issues
4. Roll back to last known good commit if needed
5. Check CI/CD logs if applicable

### Build Failures
1. Review error messages from build script
2. Check for missing dependencies
3. Verify file permissions
4. Check for syntax errors in Python files
5. Review recent changes for regressions

### Data Issues
1. Verify RUNS.md format
2. Check runs.json integrity
3. Review database/schema if applicable
4. Restore from backup if data is corrupted
5. Validate data consistency

## Review Schedule

- **Daily**: Site health checks
- **Weekly**: Repository cleanup and documentation updates
- **Monthly**: Code quality review and knowledge base audit
- **Quarterly**: Comprehensive maintenance and backup verification

## Automation Opportunities

Consider automating these checks:
- [ ] Add health checks to CI/CD pipeline
- [ ] Set up automated backups
- [ ] Create scheduled maintenance scripts
- [ ] Implement automated code quality checks
- [ ] Set up monitoring dashboards
