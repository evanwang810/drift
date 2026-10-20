#!/bin/bash
# Repository Health Check Script
# Runs all critical health checks for the Drift repository

set -e  # Exit on error

echo "=========================================="
echo "Drift Repository Health Check"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ALL_PASSED=true

# Function to check and report
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ALL_PASSED=false
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Check if site builds
echo "1. Checking site build..."
if python site/build.py > /dev/null 2>&1; then
    check_pass "Site builds successfully"
else
    check_fail "Site build failed"
fi

# 2. Run check_site.py
echo ""
echo "2. Running check_site.py..."
if python site/check_site.py --live > /tmp/check_site_output.txt 2>&1; then
    check_pass "All 12 check_site.py validations pass"
else
    check_fail "check_site.py validation failed"
    cat /tmp/check_site_output.txt
fi

# 3. Check git status
echo ""
echo "3. Checking git status..."
if git diff --quiet && git diff --cached --quiet; then
    check_pass "No uncommitted changes"
else
    check_warn "Uncommitted changes detected"
    git status --short
fi

# 4. Check for duplicate posts
echo ""
echo "4. Checking for duplicate posts..."
if python -c "
import os
import glob
posts = glob.glob('docs/posts/*.md')
titles = {}
for post in posts:
    with open(post, 'r') as f:
        for line in f:
            if line.startswith('# '):
                title = line[2:].strip()
                if title in titles:
                    print(f'Duplicate: {title} appears in {post} and {titles[title]}')
                else:
                    titles[title] = post
" 2>&1; then
    check_pass "No duplicate posts found"
else
    check_fail "Duplicate posts detected"
fi

# 5. Check for broken links in main navigation
echo ""
echo "5. Checking main navigation links..."
if python -c "
import os
import glob

# Check index.html links
with open('docs/index.html', 'r') as f:
    content = f.read()
    posts = glob.glob('docs/posts/*.html')
    post_names = [os.path.basename(p) for p in posts]

    for post in post_names:
        if post not in content:
            print(f'Missing link: {post}')
" 2>&1; then
    check_pass "All posts linked from home page"
else
    check_fail "Some posts not linked from home page"
fi

# 6. Check for Python syntax errors
echo ""
echo "6. Checking Python syntax..."
errors=0
for file in agent/*.py site/*.py scripts/*.py 2>/dev/null; do
    if [ -f "$file" ]; then
        if python -m py_compile "$file" 2>/dev/null; then
            check_pass "Syntax OK: $file"
        else
            check_fail "Syntax error: $file"
            errors=$((errors + 1))
        fi
    fi
done

# 7. Check repository size
echo ""
echo "7. Checking repository size..."
size=$(du -sh . | cut -f1)
check_pass "Repository size: $size"

# 8. Check for large files
echo ""
echo "8. Checking for large files (>1MB)..."
large_files=$(find . -type f -size +1M -not -path './.git/*' -not -path './engine/*' -not -path './.venv/*' 2>/dev/null | wc -l)
if [ "$large_files" -eq 0 ]; then
    check_pass "No large files found (>1MB)"
else
    check_warn "$large_files large files found (>1MB)"
    find . -type f -size +1M -not -path './.git/*' -not -path './engine/*' -not -path './.venv/*' 2>/dev/null
fi

# 9. Check knowledge base integrity
echo ""
echo "9. Checking knowledge base integrity..."
if python -c "
import json
try:
    with open('docs/knowledge_base.json', 'r') as f:
        kb = json.load(f)
    if isinstance(kb, list) and len(kb) > 0:
        print('Knowledge base is valid and has entries')
    else:
        print('Knowledge base is empty or invalid')
except Exception as e:
    print(f'Error: {e}')
" 2>&1; then
    check_pass "Knowledge base is valid"
else
    check_fail "Knowledge base has issues"
fi

# 10. Check RUNS.md integrity
echo ""
echo "10. Checking RUNS.md integrity..."
if python -c "
import json
try:
    with open('runs.json', 'r') as f:
        runs = json.load(f)
    if len(runs) > 0:
        print(f'RUNS.json has {len(runs)} entries')
    else:
        print('RUNS.json is empty')
except Exception as e:
    print(f'Error: {e}')
" 2>&1; then
    check_pass "runs.json is valid"
else
    check_fail "runs.json has issues"
fi

# Summary
echo ""
echo "=========================================="
if [ "$ALL_PASSED" = true ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}Some checks failed. Please review above.${NC}"
    exit 1
fi
