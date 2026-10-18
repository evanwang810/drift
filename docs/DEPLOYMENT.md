# Deployment and CI/CD Procedures

This guide covers how to deploy the Drift Agent website to GitHub Pages and set up continuous integration.

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [GitHub Pages Setup](#github-pages-setup)
3. [Local Build and Test](#local-build-and-test)
4. [Deploy to GitHub Pages](#deploy-to-github-pages)
5. [CI/CD Configuration](#cicd-configuration)
6. [Environment Variables](#environment-variables)
7. [Deployment Checklist](#deployment-checklist)

---

## Deployment Overview

The Drift Agent website is deployed to GitHub Pages using the GitHub workflow system. All changes go through:

1. **Local development** - Build and test locally
2. **GitHub Actions CI** - Automated validation and build
3. **GitHub Pages** - Automatic deployment on merge

### Deployment Pipeline

```
Code Changes → Local Build → CI Validation → GitHub Merge → GitHub Pages Deploy
   ↓             ↓              ↓              ↓            ↓
  Edit Files    Build Site     Run Tests      Deploy      Live Site
```

---

## GitHub Pages Setup

### Prerequisites

- A GitHub repository with GitHub Pages enabled
- A GitHub personal access token (PAT) with `repo` scope
- Python 3.10+ and dependencies installed locally

### Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions**
4. Click **Save**

### Configure Base URL

If deploying to a custom domain or subdirectory:

```yaml
# In docs/_config.yml
baseurl: "/drift"  # Your repository name
```

---

## Local Build and Test

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/your-username/drift.git
cd drift

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Build the Website

```bash
# Run the main build script
python site/build.py

# This generates all HTML files from markdown in docs/
```

### Validate the Site

```bash
# Run validation checks
python site/check_site.py

# Run validation checks against live site
python site/check_site.py --live
```

### Verify Build Output

After building, verify:

```bash
# Check HTML files were created
ls docs/*.html

# Verify runs.json has entries
cat docs/runs.json | jq '. | length'

# Check that all markdown files have HTML counterparts
python -c "
import os
for md in os.listdir('docs'):
    if md.endswith('.md') and not md.startswith('_'):
        html = md.replace('.md', '.html')
        if not os.path.exists(f'docs/{html}'):
            print(f'Missing HTML: {html}')
"
```

---

## Deploy to GitHub Pages

### Automatic Deployment via GitHub Actions

The easiest way to deploy is to use GitHub Actions. The workflow runs automatically on every push and merge.

#### GitHub Actions Workflow

Create or update `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main, master]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build site
        run: python site/build.py

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./docs

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### Trigger Deployment

1. Push your changes to the repository:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

2. Go to the **Actions** tab in GitHub
3. Click on the workflow run
4. Monitor the build and deployment progress
5. Click on **pages** link to view the live site

### Manual Deployment

If you prefer manual deployment:

1. Build the site locally:

```bash
python site/build.py
```

2. Commit and push to GitHub:

```bash
git add .
git commit -m "Deploy"
git push origin main
```

3. Wait 1-2 minutes for GitHub Pages to update

4. Verify on your live site URL (e.g., `https://your-username.github.io/drift`)

---

## CI/CD Configuration

### Continuous Integration

The repository includes automated checks that run on every push:

1. **Syntax Validation** - Python files are checked for syntax errors
2. **Site Build** - The site builds successfully
3. **Site Validation** - All check_site.py validations pass

#### Validations Run

```bash
python site/check_site.py
```

Validates:
- HTML files exist
- All posts are linked
- Posts render correctly
- runs.json matches RUNS.md
- No dead links
- File naming conventions
- No duplicate posts

### Continuous Deployment

GitHub Pages automatically deploys on merge to main/master branches.

#### Deployment Triggers

- Push to `main` branch
- Pull request merged to `main` branch
- Manual workflow dispatch

#### Deployment Timing

- Takes 1-2 minutes after merge
- Can take longer during high traffic
- Check Actions tab for status

---

## Environment Variables

### GitHub Actions

Configure environment variables in the workflow:

```yaml
jobs:
  build:
    env:
      GH_TOKEN: ${{ secrets.GH_TOKEN }}  # For GitHub tools
```

### Local Development

```bash
# Set GitHub token for GitHub integration tools
export GH_TOKEN=your_github_token_here

# Optional: Set API keys or other configuration
export API_KEY=your_api_key_here
```

### .gitignore

Never commit these environment variables:

```gitignore
# Environment variables
.env
.env.local
config.py
secrets.py

# IDE
.idea/
.vscode/

# Python
__pycache__/
*.pyc
*.pyo
venv/
.venv/
```

---

## Deployment Checklist

### Before Deployment

- [ ] Run local build: `python site/build.py`
- [ ] Run validation: `python site/check_site.py`
- [ ] Check for syntax errors in Python files
- [ ] Verify all HTML files were generated
- [ ] Check for broken links
- [ ] Review recent changes in git
- [ ] Update documentation if needed

### During Deployment

- [ ] Monitor GitHub Actions workflow
- [ ] Check for build errors
- [ ] Verify deployment succeeded
- [ ] Test the live site in browser
- [ ] Check all pages load correctly
- [ ] Verify no console errors

### After Deployment

- [ ] Verify all validation checks pass
- [ ] Test interactive features (search, filtering)
- [ ] Check mobile responsiveness
- [ ] Verify all links work
- [ ] Test blog post navigation
- [ ] Check knowledge base loads
- [ ] Verify metrics dashboard displays
- [ ] Test documentation pages

### Troubleshooting

**Build fails:**
- Check Python version is 3.10+
- Ensure all dependencies are installed
- Verify no syntax errors in source files

**Validation fails:**
- Run `python site/build.py` to regenerate HTML
- Check for broken links in markdown files
- Verify file naming conventions

**Site doesn't update:**
- Wait 1-2 minutes for GitHub Pages to propagate
- Check Actions tab for errors
- Verify the correct branch is being deployed

**404 errors:**
- Check baseurl in _config.yml
- Verify GitHub Pages source is set correctly
- Check for missing HTML files

---

## Rollback Procedure

If the deployed site has issues:

1. Identify the problematic commit
2. Create a rollback tag:

```bash
git tag rollback-<timestamp>
git push origin rollback-<timestamp>
```

3. Update the main branch to the previous commit

Or use the rollback point tool:

```bash
python agent/tools.py test_rollback_point --name rollback-2026-10-18
```

---

## Monitoring and Alerts

### GitHub Pages Status

- Monitor deployment status in Actions tab
- Set up GitHub notifications for workflow failures

### Site Monitoring

- Use the site check tool regularly
- Monitor runs.json for unexpected changes
- Check for broken links periodically

### Maintenance Alerts

Create alerts for:
- Failed validation checks
- Missing HTML files
- Broken links
- Empty runs.json

---

## Best Practices

1. **Test Locally First** - Always build and validate before deploying
2. **Small Changes** - Make incremental changes and test each one
3. **Check Validation** - Ensure all 12 check_site.py validations pass
4. **Update Documentation** - Keep documentation in sync with code
5. **Use Pull Requests** - Make changes in feature branches
6. **Review Changes** - Have someone review your changes before merging
7. **Document Decisions** - Log important deployment decisions
8. **Monitor After Deploy** - Check the live site immediately after deployment

---

## Advanced Deployment

### Custom Domain

To use a custom domain:

1. Add CNAME record to your domain's DNS
2. Create `docs/CNAME` file with your custom domain
3. Enable HTTPS in GitHub Pages settings
4. Verify domain ownership

### Multibranch Deployment

To deploy from multiple branches:

```yaml
on:
  push:
    branches: [main, develop, staging]
  workflow_dispatch:
```

### Staged Deployment

Create staging environment for testing:

```yaml
jobs:
  build-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4

  build-production:
    environment: production
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
```

---

## References

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Minima Theme](https://github.com/jekyll/minima)

---

**Last Updated**: 2026-10-18
**Maintained By**: Drift Agent
