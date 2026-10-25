# Site Maintenance Checklist

This document outlines regular maintenance tasks to keep the website in good condition.

## Daily Maintenance

- [ ] Run local site build: `python site/build.py`
- [ ] Verify all check_site.py validations pass: `python site/check_site.py --live`
- [ ] Check for any broken links in documentation
- [ ] Verify knowledge base entries are accessible

## Weekly Maintenance

- [ ] Review and update blog posts for accuracy and relevance
- [ ] Check for new tools or features that need documentation
- [ ] Verify all external links are still valid
- [ ] Review and update project status in PROJECT.md
- [ ] Check repository health with `python monitor_repository_health.py`

## Monthly Maintenance

- [ ] Deep dive into RUNS.md to extract insights and add to knowledge base
- [ ] Review and update project documentation
- [ ] Check for unused files or orphaned content
- [ ] Run comprehensive site tests
- [ ] Review and update GOALS.md based on completed projects
- [ ] Archive old runs from RUNS.md if necessary (keep last 1000)

## Ongoing Tasks

- [ ] Keep README.md updated with current features and setup instructions
- [ ] Ensure all documentation pages render correctly
- [ ] Verify knowledge base search functionality works
- [ ] Check that metrics dashboard loads and displays correctly
- [ ] Monitor site performance and load times
- [ ] Update maintenance checklist as new features are added

## Troubleshooting

If the site build fails:

1. Check `docs/troubleshooting.html` for common issues
2. Run `python site/check_site.py --live` to identify failing validations
3. Check the Jekyll build logs in the repository
4. Verify all required files exist and are accessible
5. Review the `docs/build-process.md` for build steps

## Maintenance Schedule

- **Daily builds:** Automated by GitHub Actions (runs at 00:00 UTC)
- **Weekly reviews:** Done manually by maintainer
- **Monthly deep dives:** Done manually by maintainer
