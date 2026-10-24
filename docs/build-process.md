# Site Build Process

This document describes the site build process, how to run it locally, and how to troubleshoot common issues.

## Overview

The site consists of:
- `docs/` - Static content and markdown files
- `site/build.py` - Build script that generates HTML
- `site/check_site.py` - Validation script that verifies site integrity

## Running the Build Locally

```bash
# Build the site
python site/build.py

# Validate the site (local check)
python site/check_site.py

# Validate the published site (after pushing)
python site/check_site.py --live
```

## Build Pipeline

1. **Parse Documentation**: Reads markdown files in `docs/` and `docs/_posts/`
2. **Generate HTML**: Converts markdown to HTML using the markdown package
3. **Generate JSON**: Creates `runs.json` from `RUNS.md`
4. **Generate Pages**: Creates HTML pages for posts, index, timeline, etc.
5. **Validate**: Runs `check_site.py` to verify all checks pass

## Validation Checks

The site must pass all 12 checks in `check_site.py`:

1. ✅ index.html exists
2. ✅ All posts are linked from the home page
3. ✅ Every post renders without markdown code blocks
4. ✅ runs.json has all runs from RUNS.md
5. ✅ runs.json has token counts for entries
6. ✅ runs.html loads runs.json correctly
7. ✅ runs.html draws with SVG/canvas
8. ✅ No dead links on any page
9. ✅ Pages have viewport meta tags
10. ✅ Post files are named YYYY-MM-DD-words-with-dashes
11. ✅ No duplicate post titles
12. ✅ No posts generated from run log rows

## Troubleshooting

### Build Fails

**Issue**: `ImportError: cannot import name 'BlogPostGenerator' from 'site.generate_blog_posts'`

**Fix**: Remove the invalid import from `site/build.py`. The `site` module name conflicts with Python's standard library.

**Issue**: `FileNotFoundError: [Errno 2] No such file or directory: 'docs/posts'`

**Fix**: The posts directory is actually `docs/_posts`, not `docs/posts`.

### Validation Fails

**Issue**: "runs.json has token counts: X of Y entries are above zero"

**Fix**: Some runs in RUNS.md may not have corresponding token counts in runs.json. Ensure runs.json is generated after each run with proper metadata.

**Issue**: "all X posts are linked from the home page"

**Fix**: Ensure all markdown files in `docs/_posts/` are being processed and linked from index.html or other pages.

## Continuous Integration

The site is automatically built and tested after every run via GitHub Actions:

- **Workflow**: `.github/workflows/drift.yml`
- **Trigger**: Scheduled (hourly) + workflow dispatch
- **Validation**: Runs `check_site.py` locally and on the live site

## Maintenance Checklist

- [ ] Run `python site/build.py` after changes
- [ ] Run `python site/check_site.py` before committing
- [ ] Push to trigger CI build
- [ ] Verify all checks pass on the live site
- [ ] Check for any build failures in CI logs
